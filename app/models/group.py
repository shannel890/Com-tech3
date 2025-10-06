from app.extension import db

class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    memberships = db.relationship('Membership', back_populates='group', cascade="all, delete-orphan")
    messages = db.relationship('Message', back_populates='group', cascade="all, delete-orphan")
    meetings = db.relationship('Meeting', back_populates='group', cascade="all, delete-orphan")

from app.models.meeting import Meeting

