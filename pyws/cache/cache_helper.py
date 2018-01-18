from pyws.cache.redis_connector import RedisStore
from pyws.cache.cache_constants import DEFAULT_TIMEOUT_IN_SECS
from pyws.cache.cache_constants import USER_TOKEN_KEY, TOKEN_USER_KEY

_redis_store = RedisStore()


def verify_auth_token(token):
    if _redis_store.hgetall(TOKEN_USER_KEY.format(token=token)):
        return True
    return False


def delete_cached_auth_keys_by_token(token):
    user_id = _redis_store.hgetall(TOKEN_USER_KEY.format(token=token))['id']
    _redis_store.expire(USER_TOKEN_KEY.format(user_id=user_id))
    _redis_store.expire(TOKEN_USER_KEY.format(token=token))


def delete_cached_auth_keys_by_user_id(user_id):
    token = _redis_store.get(USER_TOKEN_KEY.format(user_id=user_id))
    _redis_store.expire(USER_TOKEN_KEY.format(user_id=user_id))
    _redis_store.expire(TOKEN_USER_KEY.format(token=token))


def cache_auth_keys(user, token):
    _redis_store.hmset(TOKEN_USER_KEY.format(token=token), {'id': user.id})
    _redis_store.set(USER_TOKEN_KEY.format(user_id=user.id), token)


def extend_cached_auth_keys(token):
    user_id = _redis_store.hgetall(TOKEN_USER_KEY.format(token=token))['id']
    _redis_store.expire(TOKEN_USER_KEY.format(token=token), timeout_in_sec=DEFAULT_TIMEOUT_IN_SECS)
    _redis_store.expire(USER_TOKEN_KEY.format(user_id=user_id), timeout_in_sec=DEFAULT_TIMEOUT_IN_SECS)
