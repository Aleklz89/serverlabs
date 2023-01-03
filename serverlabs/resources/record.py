import uuid
from datetime import datetime

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from serverlabs.db import records, users, categories

blp = Blueprint("record,", __name__, description="Operation")

@blp.route("/record/<string:record_id>")
class Record(MethodView):
    def get(self, record_id):
        try:
            return records[record_id]
        except KeyError:
            abort(404, message="Record not found")

@blp.route("/record")
class RecordList(MethodView):
    def get(self):
        return list(records.values())


    def post(self):
        record_data = request.get_json()
        if (
                "user_id" not in record_data
                or "category_id" not in record_data
                or "sum" not in record_data
        ):
            abort(
                400,
                message="Bad request. user_id, category_id, sum is required."
            )
        if record_data["user_id"] not in users:
            abort(404, message="User not found")
        if record_data["category_id"] not in categories:
            abort(404, message="Category not found")
        record_id = uuid.uuid4().hex
        record = {
            "id": record_id,
            **record_data,
            "created_at": datetime.now(),
        }
        records[record_id] = record
        return record
