from flask import Blueprint, request
from ..utils.responses import response_with
from ..utils import responses as resp
from ..models.books import BookSchema, Book
from ..utils.database import db
from flask_jwt_extended import jwt_required

book_routes = Blueprint('book_routes', __name__)


@book_routes.route('/', methods=['POST'])
@jwt_required()
def create_book():
    try:
        data = request.get_json()
        book_schema = BookSchema()
        book_class = Book
        book = book_schema.load(data)
        title = book.get('title')
        year = book.get('year')
        author_id = book.get('author_id')
        result = book_schema.dump(book_class.create(title=title, year=year, author_id=author_id))
        return response_with(resp.SUCCESS_201, value={'book': result})

    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@book_routes.route('/', methods=['GET'])
def get_book_list():
    fetched = Book.query.all()
    book_schema = BookSchema(many=True, only=['author_id', 'title', 'year'])
    books = book_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"books": books})


@book_routes.route('/<int:id>', methods=['GET'])
def get_book_detail(id):
    fetched = Book.query.get_or_404(id)
    book_schema = BookSchema()
    books = book_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"books": books})


@book_routes.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_book_detail(id):
    data = request.get_json()
    get_book = Book.query.get_or_404(id)
    get_book.title = data['title']
    get_book.year = data['year']
    db.session.add(get_book)
    db.session.commit()
    book_schema = BookSchema()
    book = book_schema.dump(get_book)
    return response_with(resp.SUCCESS_200, value={"book": book})


@book_routes.route('/<int:id>', methods=['PATCH'])
@jwt_required()
def modify_book_detail(id):
    data = request.get_json()
    get_book = Book.query.get_or_404(id)
    if data.get('title'):
        get_book.title = data['title']
    if data.get('year'):
        get_book.year = data['year']
    db.session.add(get_book)
    db.session.commit()
    book_schema = BookSchema()
    book = book_schema.dump(get_book)
    return response_with(resp.SUCCESS_200, value={"book": book})


@book_routes.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_book(id):
    get_book = Book.query.get_or_404(id)
    db.session.delete(get_book)
    db.session.commit()
    return response_with(resp.SUCCESS_204)
