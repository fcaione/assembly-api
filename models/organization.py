from models.db import db
from datetime import datetime
from flask import request

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

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    @classmethod
    def find_all(cls):
        return Organization.query.all()
    
    @classmethod
    def find_by_id(cls, id):
        return db.get_or_404(cls, id, description=f'Record with id:{id} is not available')
    
    @classmethod
    def update_organization(cls, id):
        org = db.get_or_404(cls, id, description=f'Record with id:{id} is not available')
        data = request.get_json()
        org.name = data['name']
        org.type = data['type']
        db.session.commit()
        return org.json()
    
    @classmethod
    def delete_organization(cls, id):
        org = db.get_or_404(cls, id, description=f'Record with id:{id} is not available')
        db.session.delete(org)
        db.session.commit()

