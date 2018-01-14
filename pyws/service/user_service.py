from flask import g

from pyws.data.user_data import UserData
from pyws.helper import data_helper
from pyws.service.cache import cache_service

_user_data = UserData()


def get_user_by_user_id(user_id, include_deleted=False):
    user = _user_data.get(user_id)

    if include_deleted:
        return user

    return data_helper.filter_deleted_model(user)


def get_user_by_user_name(user_name):
    user = _user_data.get_user_by_user_name(user_name)
    return data_helper.filter_deleted_model(user)


def create_user(user_info):
    return _user_data.create(user_info)


def update_user(user, user_info):
    return _user_data.update(user, user_info)


def delete_user(user):
    # delete the cached session key associated with this user
    cache_service.delete_cached_auth_keys_by_token(g.token)

    return _user_data.delete(user)

def hard_delete_user(user):
    # hard delete the user from the db
    cache_service.delete_cached_auth_keys_by_user_id(user.id)
    return _user_data.hard_delete(user)