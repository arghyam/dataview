# -*- coding: utf-8 -*-
import os
import re
import csv
from datetime import datetime
from markdown import Markdown

from flask import render_template, redirect, request, g, url_for, Markup, abort, flash, escape

from app import app
import models
import utils
from models import * 
from forms import *


@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='img/favicon.ico')

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    return render_template('upload.html', title="Upload",Caption="Upload a new data set",notes="Upload a new data set")

@app.route('/data_source/create', methods=['GET', 'POST'])
def createDataSource():
    return render_template('create_data_source.html',title="Data Source",caption="Create a new data source",notes="You dont need a new data source often. You need only one DataSource per organization. Check all the DataSources you have created until now.")

@app.route('/data_source/view_all', methods=['GET'])
def viewAllDataSource():
    return render_template('view_all_data_source.html',title="Data Source",caption="View All",notes="All the Data Sources created by you.")

@app.route('/data_source/view/<data_source_id>', methods=['GET'])
def viewDataSource(data_source_id):
    return render_template('view_data_source.html',title="Data Source",caption="View",notes="You can add data tables to this source or edit the information related to this source.")

@app.route('/create/data_table/', methods=['GET', 'POST'])
def uploadDataTable():
    if request.method == 'GET':
        data_source_id = int(request.args.get('data_source_id', ''))       
        sources = DataSource.query.filter_by(data_source_id=data_source_id)
        for data_source in sources:
            return render_template('upload_data_table.html', title="Upload",Caption="Upload a new data set",notes="Upload a new data set", data_source=data_source,data_source_id=data_source_id)
    if request.method == 'POST':
        name = request.form["name"]
        description = request.form["description"]
        data_source_id = int(request.form["data_source_id"])
        uploaded_csv_file =  request.files.get('uploaded_csv_file')
        #1. insert into the data_table
        data_table = DataTable(data_table_name=name, data_table_description=description,data_table_owner_user_id=1,data_table_data_source_id=data_source_id)
        models.db.session.add(data_table)
        models.db.session.commit()

        
        #2. save the file to temp folder
        data_table_id = str(data_table.data_table_id)
        filename = 'data_table_'+data_table_id+".csv"
        uploaded_csv_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        #3. Forward to validate data page with data_table_id
        return redirect(url_for('validateDataTable', data_table_id=data_table_id), code=303)

@app.route('/update/data_table/<data_table_id>', methods=['GET', 'POST'])
def updateDataTable(data_table_id):
    if request.method == 'GET':
        tables = DataTable.query.filter_by(data_table_id=data_table_id)
        for data_table in tables:
            if data_table.data_table_upload_complete == models.UPLOAD_STATUS.INCOMPLETE:
                return render_template('update_data_table.html', title="Update",Caption="Update data set",notes="Upload a new data set", data_table = data_table, data_source_id=data_table.data_table_data_source_id)
    
    if request.method == 'POST':
        name = request.form["name"]
        description = request.form["description"]        
        #1. update the data_table
        data_table = DataTable.query.filter_by(data_table_id=data_table_id).first()

        data_table.data_table_name = name
        data_table.data_table_description = description
        models.db.session.commit()

        
        #2. save the file to temp folder
        if request.files.get('uploaded_csv_file'):
            uploaded_csv_file =  request.files.get('uploaded_csv_file')
            data_table_id = str(data_table.data_table_id)
            filename = 'data_table_'+data_table_id+".csv"
            uploaded_csv_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        #3. Forward to validate data page with data_table_id
        return redirect(url_for('validateDataTable', data_table_id=data_table_id), code=303)


@app.route('/validate/data_table/<data_table_id>', methods=['GET', 'POST'])
def validateDataTable(data_table_id):
    if request.method == 'GET':
        tables = DataTable.query.filter_by(data_table_id=data_table_id)
        for data_table in tables:
            if data_table.data_table_upload_complete == models.UPLOAD_STATUS.INCOMPLETE:
                #1. Read the file, first row, which has headers
                columns = {}
                column_list = []
                filename = 'data_table_'+str(data_table_id)+".csv"
                with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as csvfile:
                    csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"') 
                    seq_num = 0            
                    for row in csv_reader:  
                        for col in row:
                            seq_num = seq_num + 1
                            key = str(seq_num)+utils.getKey(col)
                            columns[key]=col
                            column_list.append(key)

                return render_template('validate_data_table.html', title="Validation",Caption="Upload a new data set",notes="Select the validation format for each column. This is used for validating the csv columns uploaded by you.",columns=columns,column_list=column_list, name=data_table.data_table_name, description=data_table.data_table_description)
            else:
                #send error message
                print "Its complete"



@app.route('/data_table/create', methods=['GET', 'POST'])
def createDataTable():
    return render_template('create_data_table.html')