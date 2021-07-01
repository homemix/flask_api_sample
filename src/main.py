import logging
import os
from flask import Flask, jsonify
from api.config.config import ProductionConfig, TestingConfig, DevelopmentConfig
from api.utils.database import db
from api.utils.responses import response_with
import api.utils.responses as resp
from api.routes.authors import author_routes
from flask_migrate import Migrate
from api.routes.books import book_routes
from api.routes.users import user_routes
from flask_jwt_extended import JWTManager
import flask_monitoringdashboard as dashboard

app = Flask(__name__)

if os.environ.get('WORK_ENV') == 'PROD':
    app_config = ProductionConfig
    app.config.from_object(app_config)
elif os.environ.get('WORK_ENV') == 'TEST':
    app_config = TestingConfig
    app.config.from_object(app_config)
elif os.environ.get('WORK_ENV') == 'DEV':
    app_config = DevelopmentConfig
    app.config.from_object(app_config)
# else:
#     app_config = DevelopmentConfig

# app.config.from_object(app_config)
print(os.environ.get('WORK_ENV'))

# blueprints
app.register_blueprint(author_routes, url_prefix='/api/authors')
app.register_blueprint(book_routes, url_prefix='/api/books')
app.register_blueprint(user_routes, url_prefix='/api/users')


# START GLOBAL HTTP CONFIGURATIONS
@app.after_request
def add_header(response):
    return response


@app.errorhandler(400)
def bad_request(e):
    logging.error(e)
    return response_with(resp.BAD_REQUEST_400)


@app.errorhandler(500)
def server_error(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_500)


@app.errorhandler(404)
def not_found(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_404)


# END GLOBAL HTTP CONFIGURATIONS


db.init_app(app)
flask_migrate = Migrate(app, db)
jwt = JWTManager(app)
dashboard.bind(app)
# with app.app_context():
#     db.create_all()

# logging.basicConfig(stream=sys.)

if __name__ == "__main__":
    app.run()
