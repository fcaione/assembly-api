from models.db import db
from datetime import datetime

class Organization(db.Model):
    __tablename__ = "organizations"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    type = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,nullable=False, onupdate=datetime.now())
    users = db.relationship("User", secondary="user_organizations")

    def __init__(self, name, type):
        self.name = name
        self.type = type

