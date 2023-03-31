from flask import request
from flask_restful import Resource
from models.organization import Organization
from models.user import User
from models.user_organization import UserOrganization
from models.db import db
from sqlalchemy.orm import joinedload
from flask_jwt_extended import get_jwt_identity, jwt_required
import json

class Organizations(Resource):
    def get(self):
        orgs = Organization.find_all()
        return [o.json() for o in orgs]
    
    @jwt_required()
    def post(self):
        identity = get_jwt_identity()
        user = User.find_by_id(identity)
        if user:
            data = request.get_json()
            org = Organization(**data)
            org.create()
            return org.json()
        return {"msg": "user not authenticated"}
    
class SingleOrganization(Resource):
    def get(self, org_id):
        org = Organization.find_by_id(org_id)

        if org is None:
            return {"message": f"Organization with id {org_id} not found"}, 404
        user_organizations = [{
            "user": u.user.json(),
            "role": u.role,
            "is_active": u.is_active
        } for u in org.user_organizations]
        
        return {**org.json(),  "users": user_organizations}
    
    @jwt_required()
    def delete(self, org_id):
        Organization.delete_organization(org_id)
        return {'message': 'Organization Deleted'}, 200