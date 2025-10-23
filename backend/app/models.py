from app import db
from datetime import datetime


class Family(db.Model):
    """Family model - represents a family/household"""
    
    __tablename__ = 'families'
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    family_name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship - one family has many members
    # cascade='all, delete-orphan' means when family is deleted, all members are deleted too
    members = db.relationship('Person', backref='family', cascade='all, delete-orphan', lazy=True)
    
    def to_dict(self):
        """Convert family object to dictionary"""
        return {
            'id': self.id,
            'family_name': self.family_name,
            'address': self.address,
            'members': [member.to_dict() for member in self.members],
            'member_count': len(self.members),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Family {self.family_name}>'


class Person(db.Model):
    """Person model - represents an individual member of a family"""
    
    __tablename__ = 'persons'
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    family_id = db.Column(db.Integer, db.ForeignKey('families.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert person object to dictionary"""
        return {
            'id': self.id,
            'family_id': self.family_id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Person {self.name}>'
