DOCUMENT API Service
======================
Document Storage Service 

Installation
------------
    # Create virtualenv using venv via
    sudo apt-get install python3.4-venv
    pyvenv-3.4 env
    source env/bin/activate
    # Install required packages
    $ pip install -e .
    
	# Create Keyspace for client demo_client

Running
-------
    # Locally (assuming a platform layer with the Mongo database pre-installed on the local vagrant machine)
    env DATABASE_URL="mongodb://escape:escape@mongo:27017/admin" gunicorn manage:app -c config/prod.py
    # Building Docker
    docker build -t apiservice/document_store_api:<insert tag/version>
    Example - docker build -t document_store_api:0.0.1 .

    # Running Docker Container
    docker run -tdP apiservice/document_store_api:<insert tag/version>
    Example -  docker run -tdP -e MONGOHOST="mongodb://mongodb:27017/test" apiservice/document_store_api:0.0.1

