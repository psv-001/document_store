"""
This is module with all utility functions
"""
import sys
import traceback
from enum import Enum
from pymongo.errors import ConnectionFailure
from document_store_api.loggings import logger
from document_store_api.db import DB, client

EXTENSION = ['png', 'jpeg', 'jpg', 'rpt', 'txt', 'doc', 'JPG', 'JPEG', 'PNG', 'RPT', 'TXT', 'DOC', 'PDF', 'pdf', 'CSV', 'csv']

class ResponseValues(Enum):
    """Enum for citation states"""
    SUCCESS = 200
    FAILURE = 400

def check_database():
    '''
    This function checks if database is connected or not
    '''
    check = False
    try:
        client.admin.command('ismaster')
        check = True
    except ConnectionFailure as exp:
        logger.error("Server not available")
        logger.debug(exp)
        traceback.print_exc(file=sys.stdout)
    return check

def check_collection(client_id):
    '''
    This function checks for the collections present in DB
    '''
    collection = None
    if client_id in DB.collection_names():
        collection = DB[client_id]
    else:
        logger.debug('No collection present of name '+client_id)
    return collection

def allowed_file(filename):
    """
    To check the file typeof given file, whether it's an allowed or not
    """
    return '.' in filename and \
       filename.rsplit('.', 1)[1] in EXTENSION
