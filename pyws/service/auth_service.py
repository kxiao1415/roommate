from pyws.service import user_service
from pyws.service import cache_service
from pyws.helper import string_helper
from pyws.constants.cache_constants import USER_TOKEN_KEY, TOKEN_USER_KEY
from pyws.constants.cache_constants import DEFAULT_TIMEOUT_IN_SECS


def authenticate_user(user_name, password):
    user = user_service.get_user_by_user_name(user_name)
    if not user or user.password != password:
        raise Exception('No user matching the user_name and password combination.')

    # retrieve existing token from cache is exists
    if cache_service.exists(USER_TOKEN_KEY.format(user_id=user.id)):
        token = cache_service.get(USER_TOKEN_KEY.format(user_id=user.id))
        extend_cached_auth_keys(user, token)
        return token

    # create token
    token = string_helper.generate_guid()

    # store token in redis
    cache_auth_keys(user, token)

    return token


def cache_auth_keys(user, token):
    cache_service.hmset(TOKEN_USER_KEY.format(token=token), {'id': user.id})
    cache_service.set(USER_TOKEN_KEY.format(user_id=user.id), token)


def extend_cached_auth_keys(user, token):
    cache_service.expire(TOKEN_USER_KEY.format(token=token), timeout_in_sec=DEFAULT_TIMEOUT_IN_SECS)
    cache_service.expire(USER_TOKEN_KEY.format(user_id=user.id), timeout_in_sec=DEFAULT_TIMEOUT_IN_SECS)
