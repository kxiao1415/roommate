from flask_redis import FlaskRedis
from pyws.constants.cache_constants import DEFAULT_TIMEOUT_IN_SECS

# redis connection, initiated in create_app()
redis = FlaskRedis()


def hmset(key, hash_dict, timeout_in_sec=DEFAULT_TIMEOUT_IN_SECS):
    """
    Sets the value of a key to dictionary

    :param key:
    :param hash_dict: dictionary object
    :param timeout_in_sec:
    :return:
    """
    redis.hmset(key, hash_dict)

    if timeout_in_sec is not None:
        redis.expire(key, timeout_in_sec)


def hgetall(key):
    """
    Gets the dictionary value of the key

    :param key:
    :return:
    """
    return redis.hgetall(key)


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


def ttl(key):
    """
    Gets time-to-live for a key

    :param key:
    :return:
    """
    redis.ttl(key)


def incr(key, num):
    """
    Increment the value of the key by the num

    :param key:
    :param num:
    :return:
    """
    redis.incr(key, num)


def exists(key):
    """
    Checks to see if key exists

    :param key:
    :return:
    """
    return redis.exists(key)
