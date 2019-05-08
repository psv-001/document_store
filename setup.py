from setuptools import setup, find_packages
setup(
    name='document_store_api',
    description='document_store Data Service',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
       'psycopg2',
       'Flask-SQLAlchemy',
       'Flask',
       'Flask-Migrate',
       'Flask-Script',
       'Flask_cors',
       'Flask_compress',
       'Flask_restful',       
       'Werkzeug',
       'gunicorn',
       'pymongo',
       'flask-PyMongo'
    ]
)
