import uuid

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from serverlabs.db import users
from serverlabs.schemas import UserSchema

blp = Blueprint("user", __name__, description="Operations on user")


@blp.route("/user/<string:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        try:
            return users[user_id]
        except KeyError:
            abort(404, message="User not found")

    @blp.response(200, UserSchema)
    def delete(self, user_id):
        try:
            deleted_user = users[user_id]
            del users[user_id]
            return deleted_user
        except KeyError:
            abort(404, message="User not found")


@blp.route("/user")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return list(users.values())

    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def post(self, user_data):
        if user_data["name"] in [u["name"] for u in users.values()]:
            abort(400, message="Name must be unique")
        user_id = uuid.uuid4().hex
        user = {"id": user_id, **user_data}
        users[user_id] = user
        return user