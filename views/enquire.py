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
from util import naming_utils
from models import Tag
from models import TagMap
from models import Plugin
from models import DataValidation
from models import * 
from forms import *
from sqlalchemy.orm import join
import json
import urllib
from util import query

mod = Blueprint('enquire', __name__, url_prefix='/enquire')



@mod.route('/create/', methods=['GET', 'POST'])
def createQuery():
    if request.method == 'GET':
        #data required for it is got from the JSON get call getDataSourceDataTable
        return render_template('enquire/create_query.html', title="Enquire",Caption="Query DB",notes="Select Data Tables to build a query")
    if request.method == 'POST':
        querystep = request.form["querystep"]
        print querystep
        if querystep == "one":
            slectedTables = request.form["selectedTables"]
            list_data_tables=json.loads(slectedTables)
            csv_datatable_id =""
            for datatable in list_data_tables:
                datatable_id = datatable['datatable']
                csv_datatable_id = str(datatable_id)+'+'+csv_datatable_id
            return render_template('enquire/create_query_datatables.html', title="Enquire",Caption="Query DB",notes="Select Data Tables to build a query",csv_datatable_id=csv_datatable_id)
        if querystep == "two":
            query_text = request.form["query"]
            query_json=json.loads(query_text)
            result_query="select * from "
            tables = query.getTables(query_json)
            for key, value in tables.iteritems():
                result_query = result_query+ " "+str(value)+" as "+str(key)+", "
            result_query = result_query[:-2]+" where "
            where_clause = query.getWhereClause(query_json)
            result_query = result_query +where_clause
            values_data_table = models.db.session.execute(result_query)
            print result_query
            return render_template('enquire/query_display.html', title="Enquire",Caption="Query DB",notes="Save the Query Results for future",values_data_table=values_data_table,result_query=result_query)



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


@mod.route('/getDataTables/', methods=['GET'])
def getDataTables():
    if request.method == 'GET':
        datatable_ids = request.args.get('datatable_ids', '')
        datatable_ids_array = datatable_ids.split(' ')
        selectedDataTables = []
        for datatable_id in datatable_ids_array:
            if datatable_id != "":
                datatable = {}            
                DBDataTable = DataTable.query.filter_by(data_table_id=int(datatable_id)).first()
                datatable['name']=DBDataTable.data_table_name
                datatable['id']=DBDataTable.data_table_id
                datacolumns = []
                data_columns = DataColumn.query.filter_by(data_column_data_table_id=int(datatable_id)).all()
                for data_column in data_columns:
                    datacolumns.append({"name":data_column.data_column_name,"id":data_column.data_column_id,"type":"type"})
                datatable["datatable"]=datacolumns             
                selectedDataTables.append(datatable)
        json_value1= "var selectedDataTables = "+json.dumps(selectedDataTables)+" ;"
        return json_value1