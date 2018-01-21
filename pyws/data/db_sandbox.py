from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
from pyws.data.model.user_model import UserModel
from pyws.data.model.preference_model import PreferenceModel


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)

user_info = {
    # required fields
    'user_name': 'test2',
    'first_name': 'test2',
    'last_name': 'test2',
    'email': 'test2@email.com',
    'password': 'abcxyz'
}

user = UserModel(user_info)

preference_info={
    'gender': 'M'
}

# pref = PreferenceModel(preference_info)
# user.preference=pref
# db.session.add(user)
# db.session.commit()
# pref_2=PreferenceModel({'gender': 'F'})
# user.preference=pref_2
# db.session.add(user)
# db.session.commit()
#
# pref = PreferenceModel({'gender': 'M', 'user_id': user.id})
# db.session.add(pref)
# db.session.commit()



# a=db.session.query(UserModel, PreferenceModel).filter(UserModel.id==PreferenceModel.user_id).filter(UserModel.user_name=='integration_test').first()
# print(a)

a=db.session.query(UserModel).\
    join(UserModel.preference). \
    filter(getattr(PreferenceModel, 'gender')=='F').\
    all()
print(a)
# a.first_name = 'kaitest123'
# pref = PreferenceModel({'gender': 'F', 'user_id': user.id})
# # a.preference = pref
# # db.session.add(a)
# # db.session.commit()roommate_dev@localhost
#
# a.preference = pref
# db.session.add(a)
# db.session.commit()

# print(a.to_json(filter_hidden_columns=True))
