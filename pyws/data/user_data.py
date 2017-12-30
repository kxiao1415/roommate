from datetime import datetime

from pyws.data.base_data import db
from pyws.data.base_data import BaseData
from pyws.data.model.user_model import UserModel


class UserData(BaseData):
    def __init__(self):
        self.model_class = UserModel

    def update(self, user, info):
        """
        Update a user with the given info

        :param user: user model
        :param info: dictionary
        :return: updated user model
        """

        for key in info.keys():
            if key in user.__table__.columns.keys():
                setattr(user, key, info[key])

                if key == 'estimated_age':
                    setattr(user, 'age_last_modified', datetime.utcnow())

        db.session.add(user)
        db.session.commit()

        return user

    def delete(self, user):
        """
        Mark user as deleted

        :param user: user model
        :return: True
        """

        user.deleted = datetime.utcnow()
        db.session.add(user)
        db.session.commit()

        return True

    def get_user_by_user_name(self, user_name):
        return db.session.query(self.model_class).filter_by(user_name=user_name).first()
