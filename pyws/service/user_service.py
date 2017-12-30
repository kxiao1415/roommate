from flask import g

from pyws.data.user_data import UserData
from pyws.helper import data_helper
from pyws.service import cache_service
from pyws.constants.cache_constants import USER_TOKEN_KEY, TOKEN_USER_KEY

_user_data = UserData()


def get_user_by_user_id(user_id):
    user = _user_data.get(user_id)
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
    delete_cached_auth_keys(user, g.token)

    return _user_data.delete(user)

def delete_cached_auth_keys(user, token):
    cache_service.expire(USER_TOKEN_KEY.format(user_id=user.id))
    cache_service.expire(TOKEN_USER_KEY.format(token=token))
