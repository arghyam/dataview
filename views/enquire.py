# -*- coding: utf-8 -*-
import os
import re
import csv
from datetime import datetime
from markdown import Markdown
from flask import Blueprint, render_template, jsonify
from flask import render_template, redirect, request, g, url_for, Markup, abort, flash, escape

from app import app
import models
import utils
from models import Tag
from models import TagMap
from models import Plugin
from models import DataValidation
from models import * 
from forms import *
from sqlalchemy.orm import join
import json
import urllib

mod = Blueprint('enquire', __name__, url_prefix='/enquire')



@mod.route('/create/', methods=['GET', 'POST'])
def createQuery():
    if request.method == 'GET':
        #data required for it is got from the JSON get call getDataSourceDataTable
        return render_template('enquire/create_query.html', title="Enquire",Caption="Query DB",notes="Select Data Tables to build a query")
    if request.method == 'POST':
        slectedTables = request.form["selectedTables"]
        list_data_tables=json.loads(slectedTables)
        csv_datatable_id =""
        for datatable in list_data_tables:
            datatable_id = datatable['datatable']
            csv_datatable_id = str(datatable_id)+'+'+csv_datatable_id
        return csv_datatable_id
        return render_template('enquire/create_query_datatables.html', title="Enquire",Caption="Query DB",notes="Select Data Tables to build a query")





@mod.route('/getDataSourceDataTable/', methods=['GET'])
def getDataSourceDataTable():
    if request.method == 'GET':
        DataSourceDataTable = []
        data_sources = DataSource.query.filter_by().all()
        for data_source in data_sources:
            data_source_dict = {}
            data_source_dict['name']=data_source.data_source_name
            data_source_tables = []
            data_tables = DataTable.query.filter_by(data_table_data_source_id=data_source.data_source_id).all()   
            for data_table in data_tables:
                data_source_tables.append({"name":data_table.data_table_name,"id":data_table.data_table_id})

            data_source_dict['datatable']=data_source_tables
            DataSourceDataTable.append(data_source_dict)
            json_value= "var DataSourceDataTable = "+json.dumps(DataSourceDataTable)+" ;"
        return json_value
