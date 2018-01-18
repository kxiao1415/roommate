from flask import g
from datetime import datetime

from pyws.data.base_data import db
from pyws.data.base_data import BaseData
from pyws.data.model.user_model import UserModel
from pyws.cache import cache_helper


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

                if key == 'deleted' and info[key] == True:
                    # delete the cached session key associated with this user
                    cache_helper.delete_cached_auth_keys_by_token(g.token)
                    setattr(user, 'last_deleted_time', datetime.utcnow())

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

    def hard_delete(self, user):
        """
        Hard delete user from db

        :param user: user model
        :return:
        """
        db.session.delete(user)
        db.session.commit()

    def get_user_by_user_name(self, user_name):
        """
        Get a user model by user_name

        :param user_name:
        :return:
        """
        return db.session.query(self.model_class).filter_by(user_name=user_name).first()
