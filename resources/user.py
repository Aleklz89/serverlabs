from flask.views import MethodView
from flask_jwt_extended import jwt_required, create_access_token
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, NoResultFound
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from db import db
from models import UserModel
from schemas import UserSchema

blp = Blueprint("user", __name__, description="Operations on user")


@blp.route("/user/<string:username>")
class User(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id):
        return UserModel.query.get_or_404(user_id)

    @jwt_required()
    @blp.response(200, UserSchema)
    def delete(self, user_id):
        raise NotImplementedError("Not implemented now")


@blp.route("/user")
class UserList(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()


@blp.route("/checkin/reg")
class CheckIn(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def post(self, user_data):
        username = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )

        try:
            db.session.add(username)
            db.session.commit()
        except IntegrityError:
            abort(400, message="This username is already used")

        return username


@blp.route("/checkin/log")
class Log(MethodView):
    @blp.arguments(UserSchema)
    def post(self, cabinet):
        user = UserModel(**cabinet)
        cabinet_name = cabinet.get("username")
        access_token = 'successful login!'

        try:
            checkin = UserModel.query.filter(UserModel.username == cabinet_name).one()
            if checkin and pbkdf2_sha256.verify(cabinet["password"], checkin.password):
                access_token = create_access_token(identity=user.ID)
            db.session.add(checkin)
            db.session.commit()
        except NoResultFound:
            abort(404, message="No account with such username")
        except IntegrityError:
            abort(400, message="Wrong type of data!")
        return {"access_token": access_token}
