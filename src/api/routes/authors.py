from flask import Blueprint, request
from ..utils.responses import response_with
from ..utils import responses as resp
from ..models.authors import Author, AuthorSchema
from ..utils.database import db
from flask_jwt_extended import jwt_required

author_routes = Blueprint('author_routes', __name__)


@author_routes.route('/', methods=['POST'])
@jwt_required()
def create_author():
    try:
        data = request.get_json()
        author_schema = AuthorSchema()
        author_class = Author
        author = author_schema.load(data)
        print(author)
        first_name = author.get('first_name')
        last_name = author.get('last_name')
        result = author_schema.dump(author_class.create(first_name=first_name, last_name=last_name))
        return response_with(resp.SUCCESS_201, value={'authors': result})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@author_routes.route('/', methods=['GET'])
def get_author_list():
    fetched = Author.query.all()
    author_schema = AuthorSchema(many=True, only=['first_name', 'last_name', 'id', 'created', 'books'])
    author = author_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={'authors': author})


@author_routes.route('/<int:author_id>', methods=['GET'])
def get_author_detail(author_id):
    fetched = Author.query.get_or_404(author_id)
    author_schema = AuthorSchema()
    author = author_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_author_detail(id):
    data = request.get_json()
    get_author = Author.query.get_or_404(id)
    get_author.first_name = data['first_name']
    get_author.last_name = data['last_name']
    db.session.add(get_author)
    db.session.commit()
    author_schema = AuthorSchema()
    author = author_schema.dump(get_author)
    return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route('/<int:id>', methods=['PATCH'])
@jwt_required()
def modify_author_detail(id):
    data = request.get_json()
    get_author = Author.query.get(id)
    if data.get('first_name'):
        get_author.first_name = data['first_name']
    if data.get('last_name'):
        get_author.last_name = data['last_name']
    db.session.add(get_author)
    db.session.commit()
    author_schema = AuthorSchema()
    author = author_schema.dump(get_author)
    return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_author(id):
    get_author=Author.query.get_or_404(id)
    db.session.delete(get_author)
    db.session.commit()
    return response_with(resp.SUCCESS_204)
