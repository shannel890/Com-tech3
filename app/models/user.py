from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extension import db

class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)

    memberships = db.relationship('Membership', back_populates='user', cascade="all, delete-orphan")
    messages = db.relationship('Message', back_populates='user', cascade="all, delete-orphan")

    @property
    def password(self):
        raise AttributeError("Password is not readable.")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
