from flask import request
from flask_restful import Resource
from models.organization import Organization
from models.db import db

class Organizations(Resource):
    def get(self):
        orgs = Organization.find_all()
        return [o.json() for o in orgs]
    
    def post(self):
        data = request.get_json()
        org = Organization(**data)
        org.create()
        return org.json()
    
class SingleOrganization(Resource):
    def get(self, org_id):
        org = Organization.find_by_id(org_id)
        return org.json()
    
    def delete(self, org_id):
        Organization.delete_organization(org_id)
        return {'message': 'Organization Deleted'}, 200


