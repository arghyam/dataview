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

mod = Blueprint('enquire', __name__, url_prefix='/enquire')



@mod.route('/create/', methods=['GET', 'POST'])
def createQuery():
    if request.method == 'GET':
        data_tables = DataTable.query.filter_by().all()    
        return render_template('enquire/create_query.html', title="Enquire",Caption="Query DB",notes="Select Data Tables to build a query", data_tables=data_tables)
