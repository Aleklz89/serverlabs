import uuid

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from serverlabs.db import users

blp = Blueprint("user", __name__, description="Operations on user")


@blp.route("/user/<string:user_id>")
class User(MethodView):
    def get(self, user_id):
        try:
            return users[user_id]
        except KeyError:
            abort(404, message="User not found")

    def delete(self, user_id):
        try:
            deleted_user = users[user_id]
            del users[user_id]
            return deleted_user
        except KeyError:
            abort(404, message="User not found")


@blp.route("/user")
class UserList(MethodView):
    def get(self):
        return list(users.values())

    def post(self):
        user_data = request.get_json()
        if "name" not in user_data:
            abort(400, message="Need name to create user")
        if user_data["name"] in [u["name"] for u in users.values()]:
            abort(400, message="Name must be unique")
        user_id = uuid.uuid4().hex
        user = {"id": user_id, **user_data}
        users[user_id] = user
        return user