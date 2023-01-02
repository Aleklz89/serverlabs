import uuid
from datetime import datetime

from flask import jsonify, request
from flask_smorest import abort

from serverlabs import app
from serverlabs.bl import get_records_by_filter

from serverlabs.db import categories, users, records

# POST /user
# POST /category
# POST /<user_id>/records
# GET /<user_id>/records/<category_id>


@app.post('/user')
def create_user():
    user_data = request.get_json()
    if "name" not in user_data:
        abort(400, message="Need name to create user")
    if user_data["name"] in [u["name"] for u in users.values()]:
        abort(400, message="Name must be unique")
    user_id = uuid.uuid4().hex
    user = {"id": user_id, **user_data}
    users[user_id] = user
    return jsonify(user)


@app.get('/users')
def get_users():
    return jsonify(list(users.values()))


@app.post('/category')
def create_category():
    category_data = request.get_json()
    category_id = uuid.uuid4().hex
    category = {
        "id": category_id,
        **category_data,
    }
    categories[category_id] = category
    return jsonify(category)


@app.post('/record')
def create_record():
    record_data = request.get_json()
    if (
        "user_id" not in record_data
        and "category_id" not in record_data
        and "sum" not in record_data
    ):
        abort(400, message="Bad request. user_id is required.")
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
    return jsonify(record)


@app.route('/categories')
def get_categories():
    return jsonify(list(categories.values()))


@app.route('/records')
def get_records_by_user_id():
    args = request.args.to_dict()
    user_id = args.get("user_id")
    if not user_id:
        return {"error": "Need at least user_id to get records"}, 400

    category_id = args.get("category_id")
    if category_id:
        return get_records_by_filter(
            lambda x: (
                x["user_id"] == user_id and x["category_id"] == category_id
            )
        )
    return get_records_by_filter(lambda x: x["user_id"] == user_id)

