from ..utils.database import db, marshmallow
from marshmallow import fields
from ..models.books import BookSchema


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    created = db.Column(db.DateTime, server_default=db.func.now())
    books = db.relationship('Book', backref='Author', cascade="all,delete-orphan")

    def __init__(self, first_name, last_name, books=[]):
        self.first_name = first_name
        self.last_name = last_name
        self.books = books

    @staticmethod
    def create(first_name, last_name):
        author=Author(first_name=first_name,last_name=last_name)
        db.session.add(author)
        db.session.commit()
        # return self


class AuthorSchema(marshmallow.Schema):
    class Meta(marshmallow.Schema.Meta):
        model = Author
        sqla_session = db.session

    id = fields.String(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    created = fields.String(dump_only=True)
    books = fields.Nested(BookSchema, many=True, only=['title', 'year', 'id'])
