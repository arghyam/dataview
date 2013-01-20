# -*- coding: utf-8 -*-

import logging

from app import app
app.config.from_object(__name__)
try:
    app.config.from_object('settings')
except ImportError:
    import sys
    print >> sys.stderr, "Please create a settings.py"
    print >> sys.stderr, "Error."

import models, views


log_file_handler = logging.FileHandler(app.config['LOGFILE'])
log_file_handler.setLevel(logging.WARNING)
app.logger.addHandler(log_file_handler)


if __name__ == '__main__':
    models.db.create_all()
    app.run('0.0.0.0', port=5000, debug=True)