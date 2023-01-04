from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, NoResultFound

from db import db
from models import RecordModel, CategoryModel
from schemas import RecordSchema, RecordQuerySchema

blp = Blueprint("record", __name__, description="Operations on record")


@blp.route("/record/<string:record_id>")
class Record(MethodView):
    @blp.response(200, RecordSchema)
    def get(self, record_id):
        return RecordModel.query.get_or_404(record_id)


@blp.route("/record")
class RecordList(MethodView):
    @blp.arguments(RecordQuerySchema, location="query", as_kwargs=True)
    @blp.response(200, RecordSchema(many=True))
    def get(self, **kwargs):
        user_id = kwargs.get("User_ID")

        if not user_id:
            abort(400, "Bad request: Username needed")

        query = RecordModel.query.filter(RecordModel.User_ID == user_id)

        category_id = kwargs.get("Category_ID")

        if category_id:
            query = query.filter(RecordModel.Category_ID == category_id)

        return query.all()

    @blp.arguments(RecordSchema)
    @blp.response(200, RecordSchema)
    def post(self, record_data):
        record = RecordModel(**record_data)
        category_id = record_data.get("Category_ID")

        try:
            category = CategoryModel.query.filter(CategoryModel.ID == category_id).one()

            db.session.add(category)
            db.session.add(record)
            db.session.commit()
        except NoResultFound:
            abort(404, message="Data not found")
        except IntegrityError:
            abort(400, message="Ooops, creating record went wrong!")

        return record
