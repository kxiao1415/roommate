from flask import request, g
from functools import wraps
from pyws.service import cache_service
from pyws.constants.cache_constants import REQUEST_LIMIT_KEY, TOKEN_USER_KEY


def validate_json(*expected_args):
    """
    **User Example 1**

        @validate_json()
        def authenticate_user():
            pass

        1. Makes sure that a valid json object is part of the request

    **User Example 2**

        @validate_json('user_name', 'password')
        def authenticate_user():
            pass

        1. Makes sure that a valid json object is part of the request
        2. Makes sure the json object contains 'user_name' and 'password'

    :param expected_args:
    :return:
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                json = request.json
            except:
                raise Exception(u'Payload must be a valid json. '
                                u'Tip: Is Content-Type set to application/json?')

            missing_fields = []
            for expected_arg in expected_args:
                if expected_arg not in json:
                    missing_fields.append(expected_arg)

            if missing_fields:
                raise Exception('Required fields [ {0} ] are missing from json payload.'
                                .format(', '.join(missing_fields)))

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def limit(requests=100, window=60, by="ip", group=None):
    """
    **User Example**

        @limit(requests=100, window=60, by="ip", group=None)
        def authenticate_user():
            pass

        1. Makes sure that only 100 requests are allowed in 60 secs
           for authenticate_user() endpoint by the same ip address

    :param requests: max number of requests allowed
    :param window: duration in secs for the max allowed requests
    :param by: request originator
    :param group: request endpoint
    :return:
    """
    if not callable(by):
        by = { 'ip': lambda: request.remote_addr }[by]

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            local_group = group or request.endpoint
            key = REQUEST_LIMIT_KEY.format(endpoint=local_group, ip=by())

            try:
                remaining = requests - int(cache_service.get(key))
            except (ValueError, TypeError):
                remaining = requests
                cache_service.set(key, 0, timeout_in_sec=None)

            ttl = cache_service.ttl(key)
            if not ttl:
                cache_service.expire(key, window)

            if remaining > 0:
                cache_service.incr(key, 1)
            else:
                raise Exception(u'Too many requests.')

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def auth_required(f):
    """


    :param f:
    :return:
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token_exits = cache_service.exists(TOKEN_USER_KEY.format(token=g.token))
        if token_exits is False:
            Exception(u'Authentication required.')
        return f(*args, **kwargs)
    return decorated_function
