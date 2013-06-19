import os
import re
import csv
from datetime import datetime
from markdown import Markdown
from flask import Blueprint, render_template, jsonify
from flask import render_template, redirect, request, g, url_for, Markup, abort, flash, escape

from app import app
import models
from models import Tag
from models import TagMap
from models import Plugin
from models import * 
from forms import *
import settings

import plugins
from util import *
from util import file_utils


from sqlalchemy.orm import join

mod = Blueprint('admin', __name__, url_prefix='/admin')

@mod.route('/list/plugins', methods=['GET'])
def adminListPlugins():
    plugin_all = Plugin.query.filter_by().all()
    #pass the returned value to template for display 
    
    plugins_folder = settings.PLUGIN_PATH
    plugin_class_files = file_utils.list_plugins(plugins_folder)
    for plugin_class in plugin_class_files:
        obj = file_utils.get_class("plugins."+plugin_class+"."+file_utils.getClassNameFromFileName(plugin_class))
        print obj.plugin_key
    return render_template('admin/admin_list_plugins.html',title="List of Plugins",caption="",notes="List of Available Plugins",explore_tab="active",plugin_all=plugin_all)
