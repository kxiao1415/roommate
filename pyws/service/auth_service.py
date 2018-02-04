from pyws.service import user_service
from pyws.cache.redis_connector import RedisStore
from pyws.cache import cache_helper
from pyws.helper import string_helper
from pyws.cache.cache_constants import USER_TOKEN_KEY

_redis_store = RedisStore()


def authenticate_user(user_email, password):
    user = user_service.get_user_by_user_email(user_email)
    if not user or user.password != password:
        raise Exception('No user matching the user_email and password combination.')

    # retrieve existing token from cache is exists
    if _redis_store.exists(USER_TOKEN_KEY.format(user_id=user.id)):
        token = _redis_store.get(USER_TOKEN_KEY.format(user_id=user.id))
        cache_helper.extend_cached_auth_keys(token)
        return token

    # create token
    token = string_helper.generate_guid()

    # store token in redis
    cache_helper.cache_auth_keys(user, token)

    return token
