from models.db import db
from datetime import datetime
from flask import request
from sqlalchemy.orm import joinedload


class UserOrganization(db.Model):
    __tablename__ = "user_organizations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False)
    role = db.Column(db.String(150), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,nullable=False, onupdate=datetime.now())
    user = db.relationship('User', back_populates="_user_organizations")
    organization = db.relationship('Organization', back_populates='user_organizations')

    def __init__(self, user_id, organization_id, role, is_active):
        self.user_id = user_id
        self.organization_id = organization_id
        self.role = role,
        self.is_active = is_active

    def json(self):
        return {"id": self.id,
                "user_id": self.user_id,
                "organization_id": self.organization_id,
                "role": self.role,
                "is_active": self.is_active,
                "created_at": str(self.created_at),
                "updated_at": str(self.updated_at)
                }
    
    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    
    @classmethod
    def find_all(cls):
        return UserOrganization.query.all()

    @classmethod
    def find_by_id(cls, id):
        return db.get_or_404(cls, id, description=f'user oranization with id:{id} is not available')
    
    @classmethod
    def update_user_organization(cls, id):
        user_org = db.get_or_404(cls, id, description=f'user oranization with id:{id} is not available')
        data = request.get_json()
        user_org.role = data['role']
        user_org.is_active = data['is_active']
        db.session.commit()
        return user_org.json()

    @classmethod
    def delete_user_organization(cls, id):
        user_org = db.get_or_404(cls, id, description=f'user oranization with id:{id} is not available')
        db.session.delete(user_org)
        db.session.commit()
    
