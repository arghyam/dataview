# -*- coding: utf-8 -*-
import os
import re
import csv
from datetime import datetime
from markdown import Markdown
from flask import render_template, redirect, request, g, url_for, Markup, abort, flash, escape

from app import app
import models
from util import naming_utils
from models import Tag
from models import TagMap
from models import Plugin
from models import * 
from forms import *
from sqlalchemy.orm import join


@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='img/favicon.ico')

@app.route('/')
def index():
    return render_template('generic/home.html',home_tab="active")
