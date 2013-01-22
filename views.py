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
                    #break after first row. No need to got further
                    break
            #depending on data_table.data_table_upload_complete make it only readable
            return render_template('validate_data_table.html', title="Validation",Caption="Upload a new data set",notes="Select the validation format for each column. This is used for validating the csv columns uploaded by you.",columns=columns,column_list=column_list, data_table=data_table)
                
    ####         ####
    ####  POST   ####
    ####         ####
    else:
        #you can do below things against a temp database? if everything is okay then repeat
        #on actual database??
        columns_list = {} 
        columns_validation_list = [] #get form form
        column_short_name_list = {} 
        columns_data_column_id = {}
        filename = 'data_table_'+str(data_table_id)+".csv"
        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"') 
            first_row = True            
            data_table = DataTable.query.filter_by(data_table_id=data_table_id).first()
            sql = ""
            for row in csv_reader:  
                seq_num = 0 #column numbers
                if first_row:
                    first_row = False  
                    if data_table.data_table_upload_complete != models.UPLOAD_STATUS.ADDED_DATA_COLUMN:
                        #insert data columns
                        create_sql ="CREATE TABLE values_data_table_"+str(data_table_id)+" ("
                        for col in row:
                            print str(seq_num)
                            seq_num = seq_num + 1
                            data_column_name = col
                            data_column_short_name = str(seq_num)+utils.getKey(col)
                            #insert into DataColumn
                            data_column = DataColumn(data_column_name=data_column_name, data_column_short_name=data_column_short_name,data_column_data_table_id=data_table_id)
                            models.db.session.add(data_column)
                            models.db.session.commit()
                            #save for next rows
                            columns_data_column_id[str(seq_num)]=data_column.data_column_id
                            columns_list[str(seq_num)] = data_column_name
                            column_short_name_list[str(seq_num)] = data_column_short_name
                            #TODO create a table called values_data_table_<data_table_id> depending on columns                           
                            create_sql = create_sql+"'"+data_column_short_name+"',"
                        
                        #update the status
                        data_table.data_table_upload_complete = models.UPLOAD_STATUS.ADDED_DATA_COLUMN
                        models.db.session.commit()

                        create_sql = create_sql[:-1]
                        create_sql = create_sql+");"
                        print create_sql
                        rp = models.db.session.execute(create_sql)
                        models.db.session.commit()

                        data_table.data_table_upload_complete = models.UPLOAD_STATUS.CREATED_DATA_TABLE
                        models.db.session.commit()

                else:
                    #insert data
                    sql="insert into values_data_table_"+str(data_table_id)+" values ("
                    for col in row:
                        seq_num = seq_num + 1
                        #data_column_short_name = column_short_name_list[str(seq_num)]
                        #data_column_id = columns_data_column_id[str(seq_num)] 
                        #as of now everything is string
                        sql = sql+"'"+str(col)+"',"
                    sql = sql[:-1]
                    sql = sql +");"
                print sql
                rp = models.db.session.execute(sql)
                models.db.session.commit()

        #4: Forward to view data_table
        print "Its complete"
        return redirect(url_for('viewDataTable', data_table_id=data_table_id), code=303)


@app.route('/view/data_table/<data_table_id>', methods=['GET'])
def viewDataTable(data_table_id):
    #1. get data_table
    #2. get data_source
    #3. get data_columns
    #4. get values_data_table_<data_table_id>
    return render_template('view_data_table.html')

@app.route('/create/data_source', methods=['GET', 'POST'])
def createDataSource():
    #for adding new data source
    return render_template('create_data_source.html',title="Data Source",caption="Create a new data source",notes="You dont need a new data source often. You need only one DataSource per organization. Check all the DataSources you have created until now.")

@app.route('/update/data_source', methods=['GET', 'POST'])
def updateDataSource():
    #update the details of data source
    return render_template('update_data_source.html',title="Data Source",caption="Create a new data source",notes="You dont need a new data source often. You need only one DataSource per organization. Check all the DataSources you have created until now.")

@app.route('/view/data_source/<data_source_id>', methods=['GET'])
def viewDataSource(data_source_id):
    #view a single data source details
    #also display the data_tables under this source with column details and not the actual data
    #button to add a new table
    return render_template('view_data_source.html',title="Data Source",caption="View",notes="You can add data tables to this source or edit the information related to this source.")

@app.route('/list/data_source/', methods=['GET'])
def listAllDataSource():
    #list all the data sources
    #button to browse the single data source
    #button to add a new data source
    return render_template('list_all_data_source.html',title="Data Sources",caption="All your data sources.",notes="Upload a new data table either by creating a new data source or by adding to an existing data source")