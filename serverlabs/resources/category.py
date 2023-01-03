import uuid

from flask.views import MethodView
from flask_smorest import Blueprint

from serverlabs.db import categories
from serverlabs.schemas import CategorySchema

blp = Blueprint("category", __name__, description="Operations on category")


@blp.route("/category/<string:category_id>")
class Category(MethodView):
    def get(self, category_id):
        return categories[category_id]


@blp.route("/category")
class CategoryList(MethodView):
    def get(self):
        return list(categories.values())

    @blp.arguments(CategorySchema)
    def post(self, category_data):
        category_id = uuid.uuid4().hex
        category = {
            "id": category_id,
            **category_data,
        }
        categories[category_id] = category
        return category