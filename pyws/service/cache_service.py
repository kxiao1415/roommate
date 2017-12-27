from pyws import redis
from pyws.constants.cache_constants import DEFAULT_TIMEOUT_IN_SECS


def set(key, value, timeout_in_sec=DEFAULT_TIMEOUT_IN_SECS):
    """
    Sets a key value pair

    :param key:
    :param value:
    :param timeout_in_sec:
    :return:
    """

    if timeout_in_sec is None:
        # permanent key
        redis.set(key, value)
    else:
        redis.setex(key, timeout_in_sec, value)

def get(key):
    """
    Gets a value from the cache

    :param key:
    :return: stored value for the key
    """
    return redis.get(key)

def expire(key, timeout_in_sec=0):
    """
    Changes the expiration time of a key

    :param key:
    :param timeout_in_sec:
    :return:
    """
    redis.expire(key, timeout_in_sec)
