from flask import jsonify, request
from flask_smorest import abort

from serverlabs import app

USERS = [
    {
        "id": 1,
        "name": "First_User"
    }
]

CATEGORIES = [
    {
        "id": 1,
        "name": "Food"
    },
]

NOTES = [
    {
        "id": 1,
        "user_id": 1,
        "category_id": 1,
        "date_time": [2023, 23, 10, 18, 54],
        "cost": 3000
    },
]


@app.route("/user", methods=['POST'])
def create_user():
    new_user = request.get_json()
    try:
        if new_user["name"]:
            id_presence = False
            user_id = 1
            while not id_presence:
                id_exist = next((user for user in USERS if user["id"] == user_id), None)
                if id_exist:
                    user_id += 1
                else:
                    id_presence = True
            user = {
                "id": user_id,
                "name": new_user["name"]
            }
            USERS.append(user)
            return jsonify(user)
        else:
            return jsonify({"Bad request": "Some parameters missed."})
    except Exception:
        return jsonify({"Bad request": "Wrong data."})


@app.route("/users")
def get_users():
    cur_ui = request.args.get('id', default=None, type=int)
    if cur_ui:
        user_exist = next((user for user in USERS if user["id"] == cur_ui), None)
        if user_exist:
            return jsonify({"user": user_exist})
        else:
            return jsonify({"error": "User not found."})
    else:
        return jsonify({"users": USERS})


@app.route("/category", methods=['POST'])
def create_category():
    new_category = request.get_json()
    try:
        if new_category["name"]:
            id_presence = False
            category_id = 1
            while not id_presence:
                id_exist = next((category for category in CATEGORIES if category["id"] == category_id), None)
                if id_exist:
                    category_id += 1
                else:
                    id_presence = True
            category = {
                "id": category_id,
                "name": new_category["name"]
            }
            CATEGORIES.append(category)
            return jsonify(category)
        else:
            return jsonify({"error": "Not all parameters set."})
    except Exception:
        return jsonify({"error": "Invalid category data."})


@app.route("/categories")
def get_categories():
    category_id = request.args.get('id', default=None, type=int)
    if category_id:
        category_exist = next((category for category in CATEGORIES if category["id"] == category_id), None)
        if category_exist:
            return jsonify({"category": category_exist})
        else:
            return jsonify({"error": "Category not found."})
    else:
        return jsonify({"categories": CATEGORIES})


@app.route("/notes")
def get_notes():
    return jsonify({"notes": NOTES})


@app.route("/note", methods=['POST'])
def create_notes():
    note_id = request.args.get('id', default=None, type=int)
    user_id = request.args.get('user_id', default=None, type=int)
    category_id = request.args.get('category_id', default=None, type=int)
    if note_id:
        found_note = next((note for note in NOTES if note["id"] == note_id), None)
        if found_note:
            return jsonify({"note": found_note})
        else:
            return jsonify({"error": "Note not found."})
    else:
        if user_id:
            if category_id:
                notes = list(
                    filter(lambda note: note['user_id'] == user_id and note["category_id"] == category_id,
                           NOTES))
                if len(notes) > 0:
                    return jsonify({"notes": notes})
                else:
                    return jsonify({"error": "Notes from this user in this category not found."})
            else:
                notes = list(filter(lambda note: note['user_id'] == user_id, NOTES))
                if len(notes) > 0:
                    return jsonify({"notes": notes})
                else:
                    return jsonify({"error": "Notes from this user not found."})
        else:
            return jsonify({"notes": NOTES})


@app.route("/user_notes")
def user_notes():
    note_id = request.args.get('id', default=None, type=int)
    user_id = request.args.get('user_id', default=None, type=int)
    if note_id:
        found_note = next((note for note in NOTES if note["id"] == note_id), None)
        if found_note:
            return jsonify({"note": found_note})
        else:
            return jsonify({"error": "Note not found."})
    else:
        if user_id:
            notes = list(filter(lambda note: note['user_id'] == user_id, NOTES))
            if len(notes) > 0:
                return jsonify({"notes": notes})
            else:
                return jsonify({"error": "Notes from this user not found."})
        else:
            return jsonify({"notes": NOTES})
