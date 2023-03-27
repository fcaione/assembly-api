from flask import request
from flask_restful import Resource
from models.user import User
from models.db import db
from sqlalchemy.orm import joinedload

class Users(Resource):
    def get(self):
        users = User.find_all()
        return [u.json() for u in users]

    # Create User
    def post(self):
        data = request.get_json()      
        hashed_data = {
            **data,
            "password": bcrypt.generate_password_hash(data["password"]).decode("utf8")
            }
        user = User(**hashed_data)
        user.create()
        return user.json(), 201

class SingleUser(Resource):
    def get(self, user_id):
        user = User.query.options(joinedload(User.organizations)).filter_by(id=user_id).first()
        orgs = [t.json() for t in user.organizations]
        return {**user.json(), "organizations": orgs}

    def put(self, user_id):
        data = request.get_json()
        user = User.find_by_id(user_id)
        for k in data.keys():
            user[k] = data[k]
        db.session.commit()
        return user.json()

    def delete(self, user_id):
        User.delete_user(user_id)
        return {'message': 'User Deleted'}, 200

from app import bcrypt