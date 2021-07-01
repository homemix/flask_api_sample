from flask import Blueprint, request
from ..utils.responses import response_with
from ..utils import responses as resp
from ..models.users import User, UserSchema
from ..utils.database import db, marshmallow
from flask_jwt_extended import create_access_token
from ..utils.token import generate_verification_token, confirm_verification_token

user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        data['password'] = User.generate_hash(data['password'])
        user_schema = UserSchema()
        user = user_schema.load(data)
        username = user.get('username')
        password = user.get('password')
        result = user_schema.dump(User.create(username=username, password=password))
        return response_with(resp.SUCCESS_201, value={'user': user})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@user_routes.route('/login', methods=['POST'])
def authenticate_user():
    try:
        data = request.get_json()
        if data.get('email'):
            current_user = User.find_by_email(data['email'])
        elif data.get('username'):
            current_user = User.find_by_username(data['username'])
        if not current_user:
            return response_with(resp.SERVER_ERROR_404)
        if current_user and not current_user.isVerified:
            return response_with(resp.BAD_REQUEST_400)
        if User.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=current_user.username)
            return response_with(resp.SUCCESS_201, value={
                'message': 'Logged in as {}'.format(current_user.username),
                "access_token": access_token})
        else:
            return response_with(resp.UNAUTHORIZED_401)
    except Exception as e:
        return response_with(resp.INVALID_INPUT_422)


@user_routes.route('/confirm/<token>', methods=['GET'])
def verify_email(token):
    try:
        email = confirm_verification_token(token)

    except:
        return response_with(resp.SERVER_ERROR_404)

    user = User.query.filter_by(email=email).first_or_404()
    if user.isVerified:
        return response_with(resp.INVALID_INPUT_422)
    else:
        user.isVerified = True
        db.session.add(user)
        db.session.commit()
        return response_with(resp.SUCCESS_200, value={
            'message': 'E-mail verified, you can proceed to login now.'
        })
