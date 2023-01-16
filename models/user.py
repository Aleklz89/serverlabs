from db import db


class UserModel(db.Model):
    __tablename__ = "user"

    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    income = db.relationship(
        "IncomeModel",
        back_populates="user",
        lazy="dynamic",
    )

    record = db.relationship(
        "RecordModel",
        back_populates="user",
        lazy="dynamic",
    )

