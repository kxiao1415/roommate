from pyws.service import user_service
from pyws.helper import string_helper


def authenticate_user(user_name, password):
    user = user_service.get_user_by_user_name(user_name)
    if not user or user.password != password:
        raise Exception('No user matching the user_name and password combination.')

    # create token
    token = string_helper.generate_guid()

    # store token in redis


    return token
