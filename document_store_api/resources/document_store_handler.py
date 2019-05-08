'''
Code for document store handler
'''
import sys
import hashlib
import traceback
import datetime
import pymongo
from pymongo.errors import DuplicateKeyError
from flask import request, make_response
from flask_restful import Resource
from bson.objectid import ObjectId
from bson.binary import Binary
from document_store_api.utils.utils import check_collection, allowed_file,\
                                           ResponseValues, check_database
from document_store_api.loggings import logger

class DocumentDownloadHandler(Resource):
    '''
    Class handling Create/delete operations
    '''

    def post(self):
        '''
        POST - /postdocuments
        '''
        logger.debug("POST")
        results = {}
        client_id = request.headers.get('x-client')
        resp_code = None

        #checks if database is available or not
        if check_database() is not True:
            logger.debug('DB connection error')
            traceback.print_stack(limit=1)
            results = {'message' : 'Server is not available'}
            return results, ResponseValues.FAILURE.value

        if client_id is None:
            logger.debug('Client_id not found')
            traceback.print_stack(limit=1)
            results = {'message' : 'Client_id not found'}
            resp_code = ResponseValues.FAILURE.value
            return results, resp_code

        # Checks for Collection avaialbility
        if check_collection(client_id) is not None:
            collection_name = check_collection(client_id)
        else:
            logger.debug('No Collection of name '+str(client_id)+' is present')
            traceback.print_stack(limit=1)
            results = {'message' : 'Server is not available'}
            resp_code = ResponseValues.FAILURE.value
            return results, resp_code

        try:
            uploaded_file = request.files['file_content']
        except Exception:
            logger.debug('File not found')
            traceback.print_exc(file=sys.stdout)
            results = {'message' : 'File not found'}
            resp_code = ResponseValues.FAILURE.value
            return results, resp_code

        file_name = request.form.get("file_name")
        file_format = request.form.get("file_format")
        file_identity = request.form.get("file_identity")

        if uploaded_file and allowed_file(uploaded_file.filename):
            file_content = Binary(uploaded_file.read())
            code = hashlib.sha256(file_content)
            hashcode = code.hexdigest()
        else:
            logger.debug('File format not supported')
            traceback.print_stack(limit=1)
            results = {'message' : 'Server is not available'}
            resp_code = ResponseValues.FAILURE.value
            return results, resp_code

        # If correct data is provided insertion operation is performed
        # Checks for file duplication before inserting
        if file_name is not None and file_format is not None:

            inputs = {"file_name" : file_name,\
                      "file_format" : file_format,\
                      "file_identity" : file_identity,\
                      "file_content" : file_content,\
                      "sha256" : hashcode,\
                      "date_time" : datetime.datetime.utcnow()
                     }
            try:
                res = collection_name.insert_one(inputs)
                logger.info('posted successfully for id '+ str(res.inserted_id))
                results['message'] = "Data inserted successfully"
                results['_id'] = str(res.inserted_id)
                resp_code = ResponseValues.SUCCESS.value
            except DuplicateKeyError as exp:
                logger.debug('File Duplication')
                logger.debug(exp)
                traceback.print_exc(file=sys.stdout)
                results = {'message' : 'file already exists'}
                resp_code = ResponseValues.FAILURE.value
        else:
            logger.debug('file_name or file_format is missing')
            traceback.print_stack(limit=1)
            results = {'message' : 'Server is not available'}
            resp_code = ResponseValues.FAILURE.value
        return results, resp_code

    def delete(self, getid=None):
        '''
        DELETE - /deletedocuments/<getid>
        '''
        client_id = request.headers.get('x-client')
        id_valid = None
        resp_code = None

        # Checks if database is available or not
        if check_database() is not True:
            logger.debug('DB connection error')
            traceback.print_stack(limit=1)
            results = {'message' : 'Server is not available'}
            resp_code = ResponseValues.FAILURE.value
            return results, resp_code

        #Checks if valid id provided
        if getid and ObjectId.is_valid(getid):
            id_valid = True
        else:
            logger.debug('Correct Id is not provided for delete operation')
            traceback.print_stack(limit=1)
            results = {'message' : 'Server is not available'}
            resp_code = ResponseValues.FAILURE.value
            return results, resp_code

        if client_id is None:
            logger.debug('Client_id not found')
            traceback.print_stack(limit=1)
            results = {'message' : 'Client_id not found'}
            resp_code = ResponseValues.FAILURE.value
            return results, resp_code

        if check_collection(client_id) is not None:
            collection_name = check_collection(client_id)
        else:
            logger.debug('No Collection of name '+str(client_id)+' is present')
            traceback.print_stack(limit=1)
            results = {'message' : 'Server is not available'}
            resp_code = ResponseValues.FAILURE.value
            return results, resp_code

        if id_valid and collection_name.find({"_id" : ObjectId(getid)}).count() != 0:
            collection_name.remove({"_id" : ObjectId(getid)})
            logger.info('data deleted successfully for '+getid)
            results = {'message':'data deleted successfully for '+getid}
            resp_code = ResponseValues.SUCCESS.value
        else:
            logger.info('No document present for '+getid)
            traceback.print_stack(limit=1)
            results = {'message':'Server is not available'}
            resp_code = ResponseValues.FAILURE.value
        return results, resp_code

class DocumentLoadHandler(Resource):
    '''
    Class for GET operations
    '''
    def get(self, getid=None):
        '''
        GET - /getdocuments
        GET using ObjectId - /getdocuments/<getid>
        '''
        jlist = []
        client_id = request.headers.get('x-client')
        resp_code = None

        #Checks if database is available or not
        if check_database() is not True:
            logger.debug('DB connection error')
            traceback.print_stack(limit=1)
            results = {'message' : 'Server is not available'}
            return results, ResponseValues.FAILURE.value

        if client_id is None:
            logger.debug('Client_id not found')
            traceback.print_stack(limit=1)
            results = {'message' : 'Client_id not found'}
            return results, ResponseValues.FAILURE.value

        if check_collection(client_id) is not None:
            collection_name = check_collection(client_id)
        else:
            logger.debug('No Collection of name '+str(client_id)+' is present')
            traceback.print_stack(limit=1)
            results = {'message' : 'Server is not available'}
            resp_code = ResponseValues.FAILURE.value
            return results, resp_code

        # Get Document based on id provided and Display
        if getid and ObjectId.is_valid(getid):
            if collection_name.find({"_id" : ObjectId(getid)}).count() == 0:
                logger.debug('Data not present for this ObjectId')
                traceback.print_stack(limit=1)
                results = {'message':'Serever is not available'}
                resp_code = ResponseValues.FAILURE.value
                return results, resp_code
            else:
                cursor = collection_name.find({"_id" : ObjectId(getid)})
                for param in cursor:
                    results = {}
                    results['file_name'] = param['file_name']
                    results['file_format'] = param['file_format']
                    results['file_content'] = param['file_content']
                    jlist.append(results)
                blob = Binary((jlist[-1])["file_content"])
                file_name = (jlist[-1])["file_name"]
                file_format = (jlist[-1])["file_format"]
                response = make_response(blob)
                response.headers["Content-Type"] = file_format
                response.headers["Content-Disposition"] = 'inline; filename=%s'\
                                                      %file_name
                logger.info('file downloaded successfully')
                return response

        # Get Information of all Documents stored in DB.
        elif getid is None:
            cursor = collection_name.find().sort("date_time", pymongo.ASCENDING)
            for param in cursor:
                results = {}
                results['_id'] = str(param['_id'])
                results['file_name'] = param['file_name']
                results['file_format'] = param['file_format']
                results['date_time'] = param['date_time'].strftime("%Y-%m-%dT%H:%M:%SZ")
                results['file_identity'] = param['file_identity']
                jlist.append(results)
            logger.info('List sent successfully')
            resp_code = ResponseValues.SUCCESS.value
            return {'json_list': jlist}, resp_code
        else:
            logger.debug('Invalid Id provided')
            traceback.print_stack(limit=1)
            results = {'message' : 'Server is not available'}
            resp_code = ResponseValues.FAILURE.value
            return results, resp_code
