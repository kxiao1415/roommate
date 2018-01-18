import json

from test.integration_tests.suites.pyws_suite.bindings_base import network_helpers


class UserApi(object):

    def authenticate_user(self, user_info):
        data = network_helpers.http_request('/users/authenticate/', data=user_info, verb='POST')
        return json.loads(data)

    def create_user(self, user_info):
        data = network_helpers.http_request('/users/', data=user_info, verb='POST')
        return json.loads(data)

    def get_user(self, user_id):
        data = network_helpers.http_request('/users/{0}'.format(user_id), verb='GET')
        return json.loads(data)

    def update_user(self, user_id, user_info, token):
        data = network_helpers.http_request('/users/{0}'.format(user_id), token=token, data=user_info, verb='PUT')
        return json.loads(data)

    def hard_delete_user(self, user_id, token):
        data = network_helpers.http_request('/users/{0}'.format(user_id), token=token, verb='DELETE')
        return json.loads(data)
