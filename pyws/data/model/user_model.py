from datetime import datetime
from sqlalchemy_utils import EncryptedType

from config import Config
from pyws.data.base_data import db
from pyws.data.model.base_model import BaseModel
from pyws.data.model.preference_model import PreferenceModel

class UserModel(db.Model, BaseModel):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Unicode(64), index=True, unique=True, nullable=False)
    email = db.Column(EncryptedType(db.Unicode(64), Config.SECRET_KEY), index=True, unique=True, nullable=False)
    phone = db.Column(EncryptedType(db.Integer, Config.SECRET_KEY), index=True, unique=True)
    gender = db.Column(db.Enum('M', 'F', name='gender_enum'))
    short_description = db.Column(db.Unicode(140))
    long_description = db.Column(db.UnicodeText)
    education = db.Column(db.Enum('H', 'C', 'G', 'B', name='education_enum'))
    age = db.Column(db.Integer)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    age_last_modified = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    last_deleted_time = db.Column(db.DateTime)
    password = db.Column(EncryptedType(db.Unicode(64), Config.SECRET_KEY), nullable=False)
    profile_photo = db.Column(db.Unicode(140))
    preference = db.relationship(PreferenceModel,
                                 backref='user',
                                 cascade='all, delete-orphan',
                                 uselist=False,
                                 lazy='joined')

    # columns that should not be updated manually
    _private_columns = ['id',
                        'created_time',
                        'age_last_modified',
                        'profile_photo',
                        'last_deleted_time']

    # columns that should not be return in the api
    _hidden_columns = ['password']

    # columns that are required
    _required_columns = ['user_name',
                         'email',
                         'password']

    # map of relationships to models
    _relationships = {'preference': PreferenceModel}

    def __init__(self, obj=None):
        db.Model.__init__(self, **obj)

    @classmethod
    def private_columns(cls):
        return cls._private_columns

    @classmethod
    def required_columns(cls):
        return cls._required_columns

    @classmethod
    def hidden_columns(cls):
        return cls._hidden_columns

    @classmethod
    def relationships(cls):
        return cls._relationships

    def __repr__(self):
        return '<id: {0}>'.format(self.id)
