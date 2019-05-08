"""
File upload DB postgres model and creates Flask instance
"""
import os
from flask import Flask
from pymongo import MongoClient

app = Flask('document_store_handler')

app.config['DEBUG'] = True

def get_db():
    #url = "mongodb://%s:27017/test" % os.environ.get("MONGODB_HOST", "mongodb")
    url = 'mongodb://escape:escape@mongo:27017/admin'
    #url = "mongodb://192.168.233.3:27017/test" #% os.environ.get("MONGODB_HOST", "mongodb")
    print('****url***', url)
    client = MongoClient(url)
    return client, client.get_default_database()

client, DB = get_db()
