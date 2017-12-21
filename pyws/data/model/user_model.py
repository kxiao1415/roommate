from datetime import datetime

from pyws import db
from pyws.data.model.base_model import BaseModel
from pyws.helper import data_helper


class UserModel(db.Model, BaseModel):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    phone = db.Column(db.Integer, index=True, unique=True)
    gender = db.Column(db.Enum('M', 'F', name='gender_enum'))
    short_description = db.Column(db.String(140))
    long_description = db.Column(db.Text)
    education = db.Column(db.String(64))
    estimated_age = db.Column(db.Integer)
    budget_max = db.Column(db.Integer)
    budget_min = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    age_last_modified = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.DateTime)

    # columns that should not be updated manually
    _private_columns = ['id',
                        'created',
                        'age_last_modified',
                        'deleted']

    def __init__(self, obj=None):
        data_helper.filter_private_columns(self, obj)

        db.Model.__init__(self, **obj)

    @classmethod
    def private_columns(cls):
        return cls._private_columns

    def __repr__(self):
        return '<id: {0}>'.format(self.id)
