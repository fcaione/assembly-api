from models.db import db
from datetime import datetime
from flask import request

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(255), unique=True)
    profile_picture = db.Column(db.String(500), nullable=False, default="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png")
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,nullable=False, onupdate=datetime.now())
    organizations = db.relationship("Organization",secondary="user_organizations")
    organizations_owned = db.relationship("Organization", back_populates="owned_by")
    _user_organizations = db.relationship('UserOrganization', back_populates='user', cascade='all, delete')


    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def json(self):
        return {"id": self.id,
                "name": self.name,
                "email": self.email,
                "password": self.password,
                "profile_picture": self.profile_picture,
                "created_at": str(self.created_at),
                "updated_at": str(self.updated_at)}
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    @classmethod
    def find_all(cls):
        return User.query.all()

    @classmethod
    def find_by_id(cls, id):
        return db.get_or_404(cls, id, description=f'Record with id:{id} is not available')
    
    @classmethod
    def update_user(cls, id):
        user = db.get_or_404(cls, id, description=f'Record with id:{id} is not available')
        data = request.get_json()
        user.email = data['email']
        user.name = data['name']
        user.password = data['password']
        db.session.commit()
        return user.json()

    @classmethod
    def delete_user(cls, id):
        user = db.get_or_404(cls, id, description=f'Record with id:{id} is not available')
        db.session.delete(user)
        db.session.commit()
