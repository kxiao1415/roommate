from datetime import datetime

from flask import current_app, g, request
from pyws import latest
from pyws.helper.jsonify_response import jsonify_response
from pyws.cache import cache_helper


@latest.before_request
def before_request_callback(*args, **kwargs):
    # keep track of request start time to calculate elapsed time
    g.request_start_time = datetime.utcnow()

    # create a dictionary of lower case header keys and values
    headers_lowercase_keys = {key.lower(): val for key, val in request.headers.items()}

    # set token onto g
    g.token = None
    if 'x-token' in headers_lowercase_keys:
        g.token = headers_lowercase_keys['x-token']

    # extend auth token keys is token is valid
    if cache_helper.verify_auth_token(g.token):
        cache_helper.extend_cached_auth_keys(g.token)

    # log request
    current_app.logger.info(u'>>> start request: {0} {1} {2}'
                            .format(request.method, request.path, request.query_string))


@latest.after_request
def after_request_callback(response):
    # calculate elapsed time for the request
    elapsed = datetime.utcnow() - g.request_start_time

    current_app.logger.info(u'<<< end request: {0} {1} (elapsed = {2} secs)'
                            .format(request.method, request.path, elapsed))

    return response


@latest.teardown_request
def teardown(exc):
    """
    Called after request is completed

    :param exc: exception
    :return:
    """

    if exc is not None:
        current_app.logger.exception(u'Exception: {0}'.format(str(exc)))


@latest.errorhandler(Exception)
def catch_all(exc):
    """
    Catch all exceptions to format a user friendly response

    :param exc: exception
    :return:
    """

    error = {
        'type': 'generic',
        'msg': str(exc)
    }

    return jsonify_response(status_code=400, error=error)
