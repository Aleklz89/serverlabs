from sqlalchemy import ForeignKey
from db import db


class IncomeModel(db.Model):
    __tablename__ = "income"

    ID = db.Column(db.Integer, primary_key=True)

    User_ID = db.Column(
        db.Integer,
        ForeignKey("user.ID", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    user = db.relationship("UserModel", foreign_keys=User_ID, back_populates="income")
    User_account = db.Column(db.Float(precision=2), unique=False, nullable=False)


