from flask import request
from flask_restful import Resource
from models.user_organization import UserOrganization
from models.user import User
from models.db import db
from flask_jwt_extended import get_jwt_identity, jwt_required


class UserOrganizations(Resource):
    def get(self):
        orgs = UserOrganization.find_all()
        return [o.json() for o in orgs]
    
    @jwt_required()
    def post(self):
        identity = get_jwt_identity()
        user = User.find_by_id(identity)
        if user:
            data = request.get_json()
            org = UserOrganization(**data)
            org.create()
            return org.json()
        return {"msg": "unauthorized"}
    
class SingleUserOrganization(Resource):
    def get(self, org_id):
        org = UserOrganization.find_by_id(org_id)
        return org.json()
    
    @jwt_required()
    def delete(self, id):
        identity = get_jwt_identity()
        user = User.find_by_id(identity)
        if user:
            UserOrganization.delete_user_organization(id)
            return {'message': 'Organization Deleted'}, 200
        return {"msg": "unauthorized"}
    
    @jwt_required()
    def put(self, id):
        identity = get_jwt_identity()
        user = User.find_by_id(identity)
        if user:
            UserOrganization.update_user_organization(id)
            return {"msg": "updated"}
        return {"msg": "unauthorized"}
