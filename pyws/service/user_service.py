from pyws.data.user_data import UserData
from pyws.helper import data_helper
from pyws.cache import cache_helper
from pyws.data.model.user_model import UserModel
from pyws.data.model.preference_model import PreferenceModel

_user_data = UserData()


def get_user_by_user_id(user_id, include_deleted=False):
    user = _user_data.get(user_id)

    if include_deleted:
        return user

    return data_helper.filter_deleted_model(user)


def get_qualified_users(individual_preference, shared_preference, page=1):
    users = _user_data.get_qualified_users(individual_preference, shared_preference, page=page)
    return users


def get_user_by_user_name(user_name):
    user = _user_data.get_user_by_user_name(user_name)
    return data_helper.filter_deleted_model(user)


def create_user(user_info):
    """
    Create a new user with user info.
    If the user info contains 'preference', create the preference as well.

    :param user_info:
    :return: user id
    """
    new_preference = None
    if 'preference' in user_info:
        new_preference = PreferenceModel(user_info['preference'])
        del user_info['preference']

    new_user = UserModel(user_info)
    new_user.preference = new_preference

    return _user_data.create(new_user)


def update_user(user, user_info):
    return _user_data.update(user, user_info)


def hard_delete_user(user):
    # hard delete the user from the db
    cache_helper.delete_cached_auth_keys_by_user_id(user.id)
    return _user_data.hard_delete(user)
