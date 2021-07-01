from ..utils.database import db, marshmallow
from passlib.hash import pbkdf2_sha256 as sha256
from marshmallow import fields


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    isVerified = db.Column(db.Boolean, nullable=True, default=False)
    email = db.Column(db.String(120), unique=True, nullable=True)

    @staticmethod
    def create(username, password):
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class UserSchema(marshmallow.Schema):
    class Meta(marshmallow.Schema.Meta):
        model = User
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=False)
