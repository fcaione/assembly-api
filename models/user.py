from models.db import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,nullable=False, onupdate=datetime.now())
    organizations = db.relationship("user_organizations", foreign_keys="organization_id")

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
    
