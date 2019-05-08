#!/usr/bin/env python3.4
"""
The script contains the functions to register various resources/routes in
the application
"""
from flask_restful import Api
from flask_cors import CORS
from document_store_api.resources import document_store_handler
from document_store_api.resources import create_collection
def register_module(app):
    """ Register all the routes for this module """
    register_routes(app)
    register_cors(app)

def register_routes(app):
    """ Register API Routes """
    api = Api(app, prefix='/docstore_handler/v1')

    """API for creating new collection for new Client"""
    api.add_resource(
        create_collection.CreateCollection,
        '/collection',
    ),
    """API's for READ, INSERT, DELETE operation"""
    api.add_resource(
        document_store_handler.DocumentDownloadHandler,
        '/postdocuments',
        '/deletedocuments',
        '/deletedocuments/<getid>'
    ),
    api.add_resource(
        document_store_handler.DocumentLoadHandler,
        '/getdocuments',
        '/getdocuments/<getid>'
    )


def register_cors(app):
    """ Enable Cross Origin Resource Sharing for the module """
    cors = CORS(app, resource={r"/docstore_handler/*":{"origins": "*"}})
