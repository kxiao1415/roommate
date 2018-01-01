import redis
from config import Config

from pyws.service.cache.cache_constants import DEFAULT_TIMEOUT_IN_SECS


class RedisStore(object):

    def __init__(self):
        self.conn = redis.StrictRedis(host=Config.REDIS_HOST,
                                      port=Config.REDIS_PORT,
                                      db=Config.REDIS_DB,
                                      decode_responses=True)

    def hmset(self, key, hash_dict, timeout_in_sec=DEFAULT_TIMEOUT_IN_SECS):
        """
        Sets the value of a key to dictionary

        :param key:
        :param hash_dict: dictionary object
        :param timeout_in_sec:
        :return:
        """
        self.conn.hmset(key, hash_dict)

        if timeout_in_sec is not None:
            self.conn.expire(key, timeout_in_sec)


    def hgetall(self, key):
        """
        Gets the dictionary value of the key

        :param key:
        :return:
        """
        return self.conn.hgetall(key)

    def hmget(self, key, member, *args):
        """
        Gets the value of a member

        :param key:
        :param member:
        :return:
        """

        return self.conn.hmget(key, member, *args)

    def set(self, key, value, timeout_in_sec=DEFAULT_TIMEOUT_IN_SECS):
        """
        Sets a key value pair

        :param key:
        :param value:
        :param timeout_in_sec:
        :return:
        """
        if timeout_in_sec is None:
            # permanent key
            self.conn.set(key, value)
        else:
            self.conn.setex(key, timeout_in_sec, value)


    def get(self, key):
        """
        Gets a value from the cache

        :param key:
        :return: stored value for the key
        """
        return self.conn.get(key)


    def expire(self, key, timeout_in_sec=0):
        """
        Changes the expiration time of a key

        :param key:
        :param timeout_in_sec:
        :return:
        """
        self.conn.expire(key, timeout_in_sec)


    def ttl(self, key):
        """
        Gets time-to-live for a key

        :param key:
        :return:
        """
        self.conn.ttl(key)


    def incr(self, key, num):
        """
        Increment the value of the key by the num

        :param key:
        :param num:
        :return:
        """
        self.conn.incr(key, num)


    def exists(self, key):
        """
        Checks to see if key exists

        :param key:
        :return:
        """
        return self.conn.exists(key)
