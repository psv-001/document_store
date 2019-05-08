'''
Code for creating Collection for each x-client
'''
import traceback
import pymongo
from flask import request
from flask_restful import Resource
from document_store_api.db import DB
from document_store_api.loggings import logger
from document_store_api.utils.utils import ResponseValues, check_database

class CreateCollection(Resource):
    '''
    Class handling Create collection for Each Client
    '''
    def post(self):
        '''
        POST - /collections
        '''
        data = request.json
        results = {}

        # Checks for database
        if check_database() is not True:
            print('PPPPPP')
            logger.debug('DB connection error')
            traceback.print_stack(limit=1)
            results = {'message' : 'Server is not available'}
            return results, ResponseValues.FAILURE.value

        if data['client_name'] is None:
            logger.debug('Client name not provided')
            traceback.print_stack(limit=1)
            results['message'] = 'Please provide client name'
            return results, ResponseValues.FAILURE.value

        # Create Collection for client with unique indexing
        collection = DB[data['client_name']]\
                     .create_index([("sha256", pymongo.ASCENDING)], unique=True)
        logger.info('Collection Created Successfully')
        results['message'] = 'Collection created successfully'
        results['collection_name'] = data['client_name']
        return results, ResponseValues.SUCCESS.value
