from flask import request
from flask_restful import Resource
from models.organization import Organization
from models.db import db
from sqlalchemy.orm import joinedload

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
        org = Organization.query.options(joinedload(Organization.users)).filter_by(id=org_id).first()
        users = [u.json() for u in org.users]
        return {**org.json(), "users": users}
    
    def delete(self, org_id):
        Organization.delete_organization(org_id)
        return {'message': 'Organization Deleted'}, 200


