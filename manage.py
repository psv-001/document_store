#!/usr/bin/env python3.4
"""
This script implements creation of WSGI Application instance and
registering of modules(apiservices available and resources)
"""
from flask import Flask
from flask_pymongo import PyMongo
from flask_compress import Compress
from flask_script import Manager
from flask_migrate import  Migrate, MigrateCommand
from document_store_api.app import register_module
from document_store_api.db import app, DB

manager = Manager(app)
migrate = Migrate(app, DB)
manager.add_command('DB', MigrateCommand)
Compress(app)
register_module(app)
if __name__ == '__main__':
    manager.run()
