from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError

from db import db
from models import CategoryModel
from schemas import CategorySchema

blp = Blueprint("category", __name__, description="Operations on category")


@blp.route("/category/<string:category_name>")
class Category(MethodView):
    @blp.response(200, CategorySchema)
    def get(self, category_id):
        return CategoryModel.query.get_or_404(category_id)


@blp.route("/category")
class CategoryList(MethodView):
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        return CategoryModel.query.all()

    @blp.arguments(CategorySchema)
    @blp.response(200, CategorySchema)
    def post(self, category_data):
        category = CategoryModel(**category_data)

        try:
            db.session.add(category)
            db.session.commit()
        except IntegrityError:
            abort(400, message="This category already exists")

        return category
