"""This is model for DB operations"""
import os
import datetime
#from _api.db import app, DB, session_commit

# Create the  ReportHistory Class
class ReportHistory(DB.Model):
    """This class is used for table creation"""
    __tablename__ = 'ReportHistory'

    report_id = DB.Column(DB.Integer, primary_key=True)
    store_id = DB.Column(DB.Integer, nullable=True)
    citation_id = DB.Column(DB.Integer)
    name = DB.Column(DB.String(255))
    client_id = DB.Column(DB.String(255))
    report_status = DB.Column(DB.String(255), nullable=True)
    job_uuid = DB.Column(DB.String(255), nullable=True)
    result_uuid = DB.Column(DB.String(255), nullable=True)
    generated_by = DB.Column(DB.String(255), nullable=True)
    start_time = DB.Column(DB.String(255), nullable=True)
    job_type = DB.Column(DB.String(255), nullable=True)

    def __init__(self, args):
        self.store_id = args['store_id']
        self.client_id = args['client_id']
        self.citation_id = args['citation_id']
        self.name = args['name']
        self.report_status = args['report_status']
        self.generated_by = args['generated_by']
        self.job_uuid = args['job_uuid']
        self.result_uuid = args['result_uuid']
        self.start_time = args['start_time']
        self.job_type = args['job_type']


    def add(self, post):
        """This will add object to DB"""
        DB.session.add(post)
        return session_commit()

    def update(self):
        """This will update object in the DB"""
        return session_commit()

    def delete(self, post):
        """This will delete object from the DB"""
        DB.session.delete(post)
        return session_commit()

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'report_id' : self.report_id,
            'store_id': self.store_id,
            'citation_id': self.citation_id,
            'name': self.name,
            'report_status' : self.report_status,
            'generated_by' : self.generated_by,
            'client_id' : self.client_id,
            'job_uuid' : self.job_uuid,
            'result_uuid' : self.result_uuid,
            'start_time' : self.start_time,
            'job_type' : self.job_type
        }
