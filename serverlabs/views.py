from flask import jsonify, request

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
        "name": "Food",
    },
]

NOTES = [
    {
        "id": 1,
        "user_id": 1,
        "category_id": 1,
        "date_time": (2022, 23, 10, 18, 54),
        "cost": 3000
    },
]

# GET /users
# POST /user


@app.route("/users")
def get_users():
    return jsonify({"users": USERS})


@app.route("/user", methods=['POST'])
def create_user():
    user_data = request.get_json()
    USERS.append(user_data)
    print(USERS)
    return jsonify(user_data)

# GET /categories
# POST /category


@app.route("/categories")
def get_categories():
    return jsonify({"categories": CATEGORIES})


@app.route("/category", methods=['POST'])
def create_category():
    category_data = request.get_json()
    CATEGORIES.append(category_data)
    return jsonify(category_data)

# GET /categories
# POST /category


@app.route("/notes")
def get_notes():
    return jsonify({"notes": NOTES})


@app.route("/note", methods=['POST'])
def create_notes():
    note_data = request.get_json()
    NOTES.append(note_data)
    return jsonify(note_data)


@app.route("/user_notes")
def user_notes():
    note_id = request.args.get('id', default=None, type=int)
    user_id = request.args.get('user_id', default=None, type=int)
    if note_id:
        found_note = next((record for record in NOTES if record["id"] == note_id), None)
        if found_note:
            return jsonify({"note": found_note})
        else:
            return jsonify({"error": "Note not found."})
    else:
        if user_id:
            records = list(filter(lambda record: record['user_id'] == user_id, NOTES))
            if len(records) > 0:
                return jsonify({"notes": records})
            else:
                return jsonify({"error": "Notes from this user not found."})
        else:
            return jsonify({"notes": NOTES})