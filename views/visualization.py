# -*- coding: utf-8 -*-
import os
import re
import csv
from datetime import datetime
from markdown import Markdown
from flask import Blueprint, render_template, jsonify
from flask import render_template, redirect, request, g, url_for, Markup, abort, flash, escape

import json

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

mod = Blueprint('visualization', __name__, url_prefix='/visualization')

@mod.route('/create/<plugin_key>/', methods=['GET'])
def createVisualizations(plugin_key):
    #get the list of all the available visualizations from plugin table
    #TODO: plugin_visualizations_all = Plugin.query.filter_by(plugin_type=1, status=1)
    visual_plugin = Plugin.query.filter_by(plugin_key=plugin_key).first()
    data_type = request.args.get('data_type', '')
    data_key = request.args.get('data_key', '')
    if data_key != "":
        data_key =int(data_key)
    else:
        data_key = 0

    #only for table as of now
    data_table_id = data_key

    #1. get data_table
    data_table = DataTable.query.filter_by(data_table_id=data_table_id).first()
    data_table_data_source_id = data_table.data_table_data_source_id
    title=data_table.data_table_name
    caption = data_table.data_table_description


    #2. get data_columns
    data_columns = DataColumn.query.filter_by(data_column_data_table_id=data_table_id)
    no_of_data_columns = data_columns.count()

    #pass the returned value to template for display 
    return render_template('visualization_plugins/'+visual_plugin.plugin_key+".html",title=visual_plugin.name,caption="",notes="Please select the columns and click create.",explore_tab="active",visual_plugin=visual_plugin,data_columns=data_columns, user_action="select",data_key=data_key,data_type=data_type)


@mod.route('/bargraph', methods=['POST'])
def bargraph():
    print request.form 
    visual_plugin = Plugin.query.filter_by(plugin_key="bargraph").first()

    ################# DATA RELATED ###########################################
    data_type = request.form.get('data_type', '')
    data_key = request.form.get('data_key', '')
    name_column = request.form.get('name_column', '').strip()
    value_column = request.form.get('value_column', '').strip()

    if data_key != "":
        data_key =int(data_key)
    else:
        data_key = 0

    #only for table as of now
    data_table_id = data_key

    data_table = DataTable.query.filter_by(data_table_id=data_table_id).first()
    data_table_data_source_id = data_table.data_table_data_source_id
    title=data_table.data_table_name
    caption = data_table.data_table_description
    notes = "Notes"
    

    #1a. Get tags
    #tags = models.db.session.query(Tag, TagMap).filter_by(TagMap.data_table_id=data_table_id).all()
    tags = models.db.session.query(Tag).select_from(join(Tag, TagMap)).filter(TagMap.data_table_id==data_table_id).all()
    #models.db.session.query(Tag, TagMap).filter(Tag.tag_id==TagMap.tag_id).filter(TagMap.data_table_id=='xavier@yahoo.com').all()

    #2. get data_source
    data_source = DataSource.query.filter_by(data_source_id=data_table_data_source_id).first()
    data_source_owner_user_id = data_source.data_source_owner_user_id
    data_owner =Users.query.filter_by(user_id=data_source_owner_user_id).first()
    #3. get data_columns
    data_columns = DataColumn.query.filter_by(data_column_data_table_id=data_table_id)
    no_of_data_columns = data_columns.count()
    #4. get values_data_table_<data_table_id>
    sql="select * from values_data_table_"+str(data_table_id)
    values_data_table = models.db.session.execute(sql)
    data_array =[]
    values_array = []
    values_array.append(name_column)
    values_array.append(value_column)
    data_array.append(values_array)
    for row in values_data_table:
        values_array = []
        print unicode(row[name_column])
        values_array.append(unicode(row[name_column]))
        values_array.append(int(row[value_column]))
        data_array.append(values_array)
    print json.dumps(data_array,ensure_ascii=False)
    #pass the returned value to template for display 
    return render_template("visualization_plugins/bargraph.html",title=request.form['title'],caption="",notes="Please click on save to save the visualization",explore_tab="active",visual_plugin=visual_plugin, values_data_table=values_data_table, data_table=data_table,data_source=data_source, data_columns=data_columns,no_of_data_columns=no_of_data_columns,data_owner=data_owner,data_table_id=data_table_id,tags=tags,user_action="try",selected_columns=request.form,data_array=json.dumps(data_array,ensure_ascii=False)  )

