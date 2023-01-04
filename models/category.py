from db import db


class CategoryModel(db.Model):
    __tablename__ = "category"

    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(128), unique=True, nullable=False)

    record = db.relationship(
        "RecordModel",
        back_populates="category",
        lazy="dynamic",
    )
