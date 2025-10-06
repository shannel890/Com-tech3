from app.extension import db


class Membership(db.Model):
    __tablename__ = 'memberships'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), primary_key=True)
    role = db.Column(db.String(50), nullable=False, default='member')

    user = db.relationship('User', back_populates='memberships')
    group = db.relationship('Group', back_populates='memberships')

