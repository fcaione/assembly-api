from models.db import db
from datetime import datetime

class UserOrganization(db.Model):
    __tablename__ = "user_organizations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,nullable=False, onupdate=datetime.now())

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def json(self):
        return {"id": self.id,
                "name": self.name,
                "email": self.email,
                "password": self.password,
                "created_at": str(self.created_at),
                "updated_at": str(self.updated_at)}
    
