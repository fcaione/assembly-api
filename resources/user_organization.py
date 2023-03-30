from flask import request
from flask_restful import Resource
from models.user_organization import UserOrganization
from models.db import db

class UserOrganizations(Resource):
    def get(self):
        orgs = UserOrganization.find_all()
        return [o.json() for o in orgs]
    
    def post(self):
        data = request.get_json()
        org = UserOrganization(**data)
        org.create()
        return org.json()
    
class SingleUserOrganization(Resource):
    def get(self, org_id):
        org = UserOrganization.find_by_id(org_id)
        return org.json()
    
    def delete(self, id):
        UserOrganization.delete_user_organization(id)
        return {'message': 'Organization Deleted'}, 200
