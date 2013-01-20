# -*- coding: utf-8 -*-

import re
from datetime import datetime
from markdown import Markdown

from flask import render_template, redirect, request, g, url_for, Markup, abort, flash, escape

from app import app
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




@app.route('/data_table/create', methods=['GET', 'POST'])
def createDataTable():
    return render_template('create_data_table.html')