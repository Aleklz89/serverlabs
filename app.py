import os

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_smorest import Api, Blueprint
from flask_login import LoginManager, login_manager

from db import db
from resources.user import blp as UserBlueprint
from resources.category import blp as CategoryBlueprint
from resources.record import blp as RecordBlueprint

from resources.income import blp as IncomeBlueprint


def create_app():
    sign_in = LoginManager()
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Finance REST API"
    app.config["API_VERSION"] = "v1.1.0"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    sign_in.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    api = Api(app)

    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def invalid_token_callback():
        return (
            jsonify(
                {
                    "message": "Signature verification failed",
                    "error": "invalid_token"
                }
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback():
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    api.register_blueprint(IncomeBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(CategoryBlueprint)
    api.register_blueprint(RecordBlueprint)
    api.register_blueprint(mainPage)
    return app


mainPage = Blueprint("index", __name__, description="Default page")


@mainPage.route("/")
def index():
    return jsonify("App's main page!")
