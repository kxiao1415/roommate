import os

from flask import request, g
from functools import wraps
from inspect import getcallargs
from config import Config

from pyws.cache.redis_connector import RedisStore
from pyws.cache.cache_constants import REQUEST_LIMIT_KEY, TOKEN_USER_KEY

_redis_store = RedisStore()


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

            if not isinstance(json, dict):
                raise Exception(u'Payload must be a valid hash.')

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


def validate_file(allowed_extensions=None):
    """
    **User Example 1**

        @validate_file()
        def upload_user_photo(user_id):
            pass

        1. Makes sure 'files' is part of the request

    **User Example 2**

        @validate_file(allowed_extensions=['.png', '.jpg'])
        def upload_user_photo(user_id):
            pass

        1. Makes sure 'files' is part of the request
        2. Makes sure the file extension is allowed

    :param allowed_extensions:
    :return:
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'file' not in request.files:
                raise Exception(u'Missing file part in the request. '
                                u'Tip: Try including "-F file=@image.png".')

            file = request.files['file']

            if file.filename == '':
                raise Exception(u'No file selected.')

            # check to see if the file extension is allowed
            if allowed_extensions:
                file_ext = os.path.splitext(file.filename)[1]
                if file_ext not in allowed_extensions:
                    raise Exception(u'Only files with {0} exts are allowed.'
                                    .format(allowed_extensions))

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
                remaining = requests - int(_redis_store.get(key))
            except (ValueError, TypeError):
                remaining = requests
                _redis_store.set(key, 0, timeout_in_sec=None)

            ttl = _redis_store.ttl(key)
            if not ttl:
                _redis_store.expire(key, window)

            if remaining > 0:
                _redis_store.incr(key, 1)
            else:
                raise Exception(u'Too many requests.')

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def auth_required(*resources):
    """
    **User Example 1**

        @auth_required()
        def delete_user(user_id):
            pass

        1. Makes sure that the caller is authenticated, i.e. There is a valid token in the header

    **User Example 2**

        @auth_required('user_id')
        def delete_user(user_id):
            pass

        1. Makes sure that the caller is authenticated, i.e. There is a valid token in the header
        2. Makes sure that the authenticated caller is allowed to access the user_id

    :param resources:
    :return:
    """

    def user_id_validator(user_id):
        """
        Checked to see if the cached user id corresponding to the token is the same as the accessed user id

        :param user_id:
        :return:
        """
        cached_user_info = _redis_store.hgetall(TOKEN_USER_KEY.format(token=g.token))
        return user_id == cached_user_info['id']

    resource_validator_map = {
        'user_id': user_id_validator
    }

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # bypass authentication with privileged token
            if g.token == Config.SECRET_KEY:
                return f(*args, **kwargs)

            token_exits = _redis_store.exists(TOKEN_USER_KEY.format(token=g.token))
            if token_exits is False:
                raise Exception(u'Authentication required.')

            function_arg_value_dict = getcallargs(f, *args, **kwargs)
            for resource in resources:
                # check to see if the resource is passed in as a function parameter
                if resource not in function_arg_value_dict:
                    raise Exception(u'Resource {0} does not exist in the function arguments.'.format(resource))

                arg_value = function_arg_value_dict[resource]
                # check to see if the caller has access to the resources
                if not resource_validator_map[resource](arg_value):
                    raise Exception(u'User is not allowed to access this resource id {0}.'.format(arg_value))

            return f(*args, **kwargs)
        return decorated_function
    return decorator
