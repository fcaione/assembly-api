from models.db import db
from datetime import datetime
from flask import request

class Organization(db.Model):
    __tablename__ = "organizations"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    type = db.Column(db.String(150), nullable=False)
    icon = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(500), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,nullable=False, onupdate=datetime.now())
    users = db.relationship("User", secondary="user_organizations")
    owned_by = db.relationship("User", back_populates="organizations_owned")

    def __init__(self, name, type, icon, description, location, owner_id):
        self.name = name
        self.type = type
        self.icon = icon
        self.description = description
        self.owner_id = owner_id
        self.location = location

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "icon": self.icon,
            "description": self.description,
            "owner_id": self.owner_id,
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

