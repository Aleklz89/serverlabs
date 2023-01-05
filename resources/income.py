from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, NoResultFound

from db import db
from models import IncomeModel, UserModel
from schemas import IncomeSchema

blp = Blueprint("income", __name__, description="Operations on income")


@blp.route("/income/<string:income_id>")
class Income(MethodView):
    @blp.response(200, IncomeSchema)
    def get(self, account_id):
        return IncomeModel.query.get_or_404(account_id)


@blp.route("/income")
class AccountList(MethodView):
    @blp.response(200, IncomeSchema(many=True))
    def get(self):
        return IncomeModel.query.all()

    @blp.arguments(IncomeSchema)
    @blp.response(200, IncomeSchema)
    def post(self, account_data):
        income = IncomeModel(**account_data)
        user_id = account_data.get("User_ID")

        try:
            user = UserModel.query.filter(UserModel.ID == user_id).one()

            db.session.add(user)
            db.session.add(income)
            db.session.commit()
        except NoResultFound:
            abort(404, message="User not found")
        except IntegrityError:
            db.session.rollback()

            income = IncomeModel.query.filter(IncomeModel.User_ID == user_id).one()
            income.User_account += account_data.get("User account")

            db.session.add(income)
            db.session.commit()
        finally:
            return income
