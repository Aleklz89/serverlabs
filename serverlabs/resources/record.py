import uuid
from datetime import datetime

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from serverlabs.bl import get_records_by_filter
from serverlabs.db import records, users, categories
from serverlabs.schemas import RecordSchema, RecordQuerySchema

blp = Blueprint("record,", __name__, description="Operation")


@blp.route("/record/<string:record_id>")
class Record(MethodView):
    @blp.response(200, RecordSchema)
    def get(self, record_id):
        try:
            return records[record_id]
        except KeyError:
            abort(404, message="Record not found")


@blp.route("/record")
class RecordList(MethodView):
    @blp.arguments(RecordQuerySchema, location="query", as_kwargs=True)
    @blp.response(200, RecordSchema(many=True))
    def get(self, **kwargs):
        user_id = kwargs.get("user_id")
        if not user_id:
            return abort(400, message="Need at least user_id to get records")

        category_id = kwargs.get("category_id")
        if category_id:
            return get_records_by_filter(
                lambda x: (
                    x["user_id"] == user_id
                    and x["category_id"] == category_id
                )
            )
        return get_records_by_filter(lambda x: x["user_id"] == user_id)

    @blp.arguments(RecordSchema)
    @blp.response(200, RecordSchema)
    def post(self, record_data):
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
