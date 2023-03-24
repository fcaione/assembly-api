from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from models.db import db
from models import organization, user, user_organization
from resources import user, organization

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost:5432/flask_assembly_db"
app.config['SQLALCHEMY_ECHO'] = True

api = Api(app)

db.init_app(app)
migrate = Migrate(app, db)

api.add_resource(user.Users, "/users")
api.add_resource(user.SingleUser, "/users/<int:user_id>")
api.add_resource(organization.Organizations, "/organizations")
api.add_resource(organization.SingleOrganization, "/organizations/<int:org_id>")

if __name__ == '__main__':
    app.run(debug=True)