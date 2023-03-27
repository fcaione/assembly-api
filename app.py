from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from models.db import db
from resources.organization import Organizations, SingleOrganization
from resources.user import Users, SingleUser, SignIn
from resources.user_organization import UserOrganizations, SingleUserOrganization
from models import user, organization, user_organization
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

load_dotenv()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost:5432/flask_assembly_db"
app.config['SQLALCHEMY_ECHO'] = True
app.config['JWT_SECRET_KEY'] = os.environ.get("SECRET_KEY")

JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

api.add_resource(Users, "/users")
api.add_resource(SignIn, "/signin")
api.add_resource(SingleUser, "/users/<int:user_id>")
api.add_resource(Organizations, "/organizations")
api.add_resource(SingleOrganization, "/organizations/<int:org_id>")
api.add_resource(UserOrganizations, "/user/organizations")
api.add_resource(SingleUserOrganization, "/user/organizations/<int:id>")

if __name__ == '__main__':
    app.run(debug=True)