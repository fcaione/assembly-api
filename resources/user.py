from flask import request
from flask_restful import Resource
from models.user import User
from models.db import db
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import joinedload
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

bcrypt = Bcrypt()

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

class SignIn(Resource):
    def post(self):
        data = request.get_json()
        u = User.query.filter_by(email=data.get("email")).first()
        if not u:
            return f"user with email: {data.get('email')} does not exist"
        if bcrypt.check_password_hash(u.password, data.get("password")):
            access_token = create_access_token(identity=u.id)
            return {"token": access_token, "user_id": u.id}
        return "password incorrect"

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