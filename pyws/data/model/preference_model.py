from pyws.data.base_data import db
from pyws.data.model.base_model import BaseModel


class PreferenceModel(db.Model, BaseModel):

    __tablename__ = 'preference'

    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Enum('M', 'F', name='gender_enum'))
    education = db.Column(db.Enum('H', 'C', 'G', 'B', name='education_enum'))
    age = db.Column(db.Integer)
    budget_max = db.Column(db.Integer)
    budget_min = db.Column(db.Integer)
    household_size = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

    # preference of the roommate seeker
    _individual_preference_columns = ['age', 'gender', 'education']

    # preference shared by both parties
    _shared_preference_columns = ['budget_max', 'budget_min', 'household_size']

    # hidden_columns
    _hidden_columns = ['user_id']

    def __init__(self, obj=None):
        db.Model.__init__(self, **obj)

    def individual_preference_columns(self):
        return self.individual_preference_columns

    def shared_preference_columns(self):
        return self.shared_preference_columns

    def hidden_columns(self):
        return self._hidden_columns

    def __repr__(self):
        return '<id: {0}>'.format(self.id)
