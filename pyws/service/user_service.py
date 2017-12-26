from pyws.data.user_data import UserData
from pyws.helper import data_helper

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
    return _user_data.delete(user)