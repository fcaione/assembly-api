from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from models.db import db
from models import user, organization, user_organization
from resources import user, organization, user_organization
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost:5432/flask_assembly_db"
app.config['SQLALCHEMY_ECHO'] = True

api = Api(app)

db.init_app(app)
migrate = Migrate(app, db)

@app.route("/signin", methods=["POST"])
def signin():
    data = request.get_json()
    u = user.User.query.filter_by(email=data.get("email")).first()
    print(u.password)
    print(data.get("password"))
    if bcrypt.check_password_hash(u.password, data.get("password")):
        return "nice"
    return "bad"

api.add_resource(user.Users, "/users")
api.add_resource(user.SingleUser, "/users/<int:user_id>")
api.add_resource(organization.Organizations, "/organizations")
api.add_resource(organization.SingleOrganization, "/organizations/<int:org_id>")
api.add_resource(user_organization.UserOrganizations, "/user/organizations")
api.add_resource(user_organization.SingleUserOrganization, "/user/organizations/<int:id>")

if __name__ == '__main__':
    app.run(debug=True)