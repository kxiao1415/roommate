from test.integration_tests.suites.pyws_suite.bindings_base import network_helpers


class UserApi(object):

    def authenticate_user(self, user_info):
        return network_helpers.http_request('/users/authenticate/', data=user_info, verb='POST')

    def create_user(self, user_info):
        return network_helpers.http_request('/users/', data=user_info, verb='POST')

    def get_user(self, user_id):
        return network_helpers.http_request('/users/{0}/'.format(user_id), verb='GET')

    def update_user(self, user_id, user_info, token):
        return network_helpers.http_request('/users/{0}/'.format(user_id), token=token, data=user_info, verb='PUT')

    def hard_delete_user(self, user_id, token):
        return network_helpers.http_request('/users/{0}/'.format(user_id), token=token, verb='DELETE')

    def upload_user_photo(self, user_id, file_path, token):

        files = {"file": open(file_path, 'rb')}

        return network_helpers.post_file_to_url('/users/{0}/photos/'.format(user_id),
                                                token,
                                                files=files)

    def delete_user_photo(self, user_id, token):
        return network_helpers.http_request('/users/{0}/photos/'.format(user_id), token=token, verb='DELETE')

    def get_quailified_users(self, filter_criteria):

        query_param = []
        for filter in filter_criteria:
            query_param.append('{0}={1}'.format(filter, filter_criteria[filter]))

        interface = '/users/?{0}'.format('&'.join(query_param))

        return network_helpers.http_request(interface, verb='GET')

    def get_password_reset_email(self, email):

        interface = '/password_reset_email/?email={0}'.format(email)

        return network_helpers.http_request(interface, verb='GET')
