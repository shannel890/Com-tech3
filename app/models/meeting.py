from app.extension import db

class Meeting(db.Model):
    __tablename__ = 'meetings'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)

    group = db.relationship('Group', back_populates='meetings')