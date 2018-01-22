from flask import g
from datetime import datetime

from pyws.data.base_data import db
from pyws.data.base_data import BaseData
from pyws.data.model.user_model import UserModel
from pyws.data.model.preference_model import PreferenceModel
from pyws.cache import cache_helper
from config import Config


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

                if key == 'age':
                    setattr(user, 'age_last_modified', datetime.utcnow())

                if key == 'deleted' and info[key] == True:
                    # delete the cached session key associated with this user
                    cache_helper.delete_cached_auth_keys_by_token(g.token)
                    setattr(user, 'last_deleted_time', datetime.utcnow())

        # update user preference
        if 'preference' in info:
            if user.preference:
                for key in info['preference'].keys():
                    if key in user.preference.__table__.columns.keys():
                        setattr(user.preference, key, info['preference'][key])
            else:
                pref = PreferenceModel(info['preference'])
                user.preference = pref

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
        return db.session.query(UserModel).filter_by(user_name=user_name).first()

    def get_qualified_users(self, individual_preference, shared_preference, page=1):
        """
        Get a list of qualified users

        :param individual_preference:
        :param shared_preference:
        :return:
        """
        query = db.session.query(UserModel)

        for attr, value in individual_preference.items():
            query = query.filter(getattr(UserModel, attr)==value)

        if shared_preference:
            query.join(UserModel.preference)
            for attr, value in shared_preference.items():
                query = query.filter(getattr(PreferenceModel, attr)==value)

        return query.paginate(page, Config.NUMBER_PER_PAGE, False).items
