# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from app import app

__all__ = ['DataSource', 'DataTable', 'DataColumn','Users']

db = SQLAlchemy(app)


class PRIVACY:
    PUBLIC  = 0
    PRIVATE = 1


class UPLOAD_STATUS:
    INCOMPLETE          = 0
    UPLOADED            = 1
    VALIDATED           = 2
    ADDED_DATA_COLUMN   = 3
    CREATED_DATA_TABLE  = 4
    COMPLETE            = 100
# --- Models ------------------------------------------------------------------

class Users(db.Model):
    __tablename__ = 'users'
    user_id     = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String(80), unique=True)
    pw_hash     = db.Column(db.String(80))
    email       = db.Column(db.String(80), unique=True)
    name        = db.Column(db.Unicode(80))

class DataSource(db.Model):
    __tablename__ = 'data_source'
    data_source_id                      = db.Column(db.Integer, primary_key=True)    
    data_source_name                    = db.Column(db.Unicode(200))
    data_source_owner_user_id           = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    data_source_organization_name       = db.Column(db.Unicode(200))
    data_source_organization_adddress   = db.Column(db.Unicode(300))
    data_source_organization_phone      = db.Column(db.String(50))
    data_source_organization_web        = db.Column(db.String(100))

class DataTable(db.Model):
    __tablename__ = 'data_table'
    data_table_id                   = db.Column(db.Integer, primary_key=True)    
    data_table_name                 = db.Column(db.Unicode(500))
    data_table_short_name           = db.Column(db.Unicode(500))
    data_table_owner_user_id        = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    data_table_description          = db.Column(db.Text, default=u'', nullable=False)
    data_table_privacy              = db.Column(db.Integer,  default=PRIVACY.PUBLIC, nullable=False)
    data_table_data_source_id       = db.Column(db.Integer, db.ForeignKey('data_source.data_source_id'), nullable=False)
    data_table_upload_complete      = db.Column(db.Integer,  default=UPLOAD_STATUS.INCOMPLETE, nullable=False)


class DataColumn(db.Model):
    __tablename__ = 'data_column'
    data_column_id                   = db.Column(db.Integer, primary_key=True)        
    data_column_name                 = db.Column(db.Unicode(500))
    data_column_short_name           = db.Column(db.Unicode(500))
    data_column_data_table_id        = db.Column(db.Integer, db.ForeignKey('data_table.data_table_id'), nullable=False)    

class Tag(db.Model):
    __tablename__ = 'tag'
    tag_id                   = db.Column(db.Integer, primary_key=True)        
    tag_name                 = db.Column(db.Unicode(500))

class TagMap((db.Model)):
    __tablename__ = 'tag_map'
    tag_map_id               = db.Column(db.Integer, primary_key=True)
    data_table_id            = db.Column(db.Integer, db.ForeignKey('data_table.data_table_id'), nullable=False)
    tag_id                   = db.Column(db.Integer, db.ForeignKey('tag.tag_id'), nullable=False)


class DataValidation(db.Model):
    __tablename__ = 'data_validation'
    validation_id                   = db.Column(db.Integer, primary_key=True)        
    validation_name                 = db.Column(db.Unicode(500))


class Plugin((db.Model)):
    __tablename__ = 'plugin'
    plugin_id            = db.Column(db.Integer, primary_key=True)
    plugin_key           = db.Column(db.Unicode(100))    
    version              = db.Column(db.Integer)
    plugin_type          = db.Column(db.Integer)
    name                 = db.Column(db.Unicode(100))    
    description          = db.Column(db.Unicode(500))
    author               = db.Column(db.Unicode(500))
    url                  = db.Column(db.Unicode(500))
    image_url            = db.Column(db.Unicode(500))
    status               = db.Column(db.Integer)
    class_name           = db.Column(db.Unicode(500))