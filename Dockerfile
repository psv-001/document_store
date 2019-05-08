FROM ubuntu:14.04


# Install required OS packages
RUN apt-get update -y && apt-get install -y build-essential tar gcc libffi-dev libev4 libev-dev libpq-dev && apt-get install -y python3-dev  python3-pip && apt-get install -y vim

# Set some environment variables for PIP installation and db management
ENV CQLENG_ALLOW_SCHEMA_MANAGEMENT="True"

# Expose a port for gunicorn to listen on
EXPOSE 8000

# Make a workdir and virtualenv
WORKDIR /opt/document_store
RUN pip3 install virtualenv
RUN virtualenv flask
RUN . flask/bin/activate

#Install pymongo
# Install everything else
#RUN make clean
#RUN pip3 install -e .

ADD ./Makefile /opt/document_store
ADD ./setup.py /opt/document_store
RUN make clean
RUN pip3 install -e .
ADD . /opt/document_store
CMD gunicorn manage:app --reload --config config/prod.py --log-level debug --log-file - --access-logfile -
