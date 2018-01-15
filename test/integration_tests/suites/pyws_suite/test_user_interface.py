import sys
import unittest
from datetime import datetime, timedelta

from test.integration_tests.test_config import TestConfig
from api_bindings import user_api


class UserTestSuite(unittest.TestCase):

    user_api = None

    test_user_info = {
        'user_name': 'test',
        'first_name': 'test_first_name',
        'last_name': 'test_last_name',
        'email': 'test@email.com',
        'password': 'abcxyz'
    }

    test_user_id = None
    test_user_token = None
    privileged_token = TestConfig.privileged_token

    @classmethod
    def setUpClass(cls):
        cls.user_api = user_api.UserApi()

        # create a test user
        response = cls.user_api.create_user(cls.test_user_info)
        cls.test_user_id = response['user']['id']

        response = cls.user_api.authenticate_user(cls.test_user_info)
        cls.test_user_token = response['token']

    @classmethod
    def tearDownClass(cls):
        response = cls.user_api.hard_delete_user(cls.test_user_id, cls.privileged_token)
        if 'success' not in response:
            raise Exception('The test user was not deleted.')

    def test_authenticate_user_pos(self):
        """test successfully authenticate the test user"""

        response = self.user_api.authenticate_user(self.test_user_info)

        # Since this test user is already authenticated in the setUpClass()
        # We just need to make sure the token in the response is the same
        self.assertIn('token', response)
        self.assertEqual(response['token'], self.test_user_token)

    def test_authenticate_user_with_invalid_user_info_neg(self):
        """test authenticate test user with invalid user info"""

        # case 1. wrong password
        user_info = {
            'user_name': 'test',
            'password': 'wrong password'
        }

        response = self.user_api.authenticate_user(user_info)
        self.assertIn('error', response)

        # case 2. wrong user_name
        user_info = {
            'user_name': 'wrong name',
            'password': 'abcxyz'
        }

        response = self.user_api.authenticate_user(user_info)
        self.assertIn('error', response)


        # case 3. no password
        user_info = {
            'user_name': 'test'
        }

        response = self.user_api.authenticate_user(user_info)
        self.assertIn('error', response)
        self.assertEqual(response['error']['msg'],
                         'Required fields [ password ] are missing from json payload.')

        # case 4. no user_name
        user_info = {
            'password': 'abcxyz'
        }

        response = self.user_api.authenticate_user(user_info)
        self.assertIn('error', response)
        self.assertEqual(response['error']['msg'],
                         'Required fields [ user_name ] are missing from json payload.')

    def test_create_user_filter_private_columns_pos(self):
        """test private columns are correctly filtered when creating a user"""

        one_hour_ago = (datetime.utcnow() - timedelta(hours=1)).isoformat()

        user_info = {
            # required fields
            'user_name': 'integration_test',
            'first_name': 'integration_test_first_name',
            'last_name': 'integration_test_last_name',
            'email': 'integration_test@email.com',
            'password': 'abcxyz',

            # private fields
            'id': -1,
            'created': one_hour_ago,
            'age_last_modified': one_hour_ago,
            'profile_photo': 'test/path/photo.png',
            'deleted': one_hour_ago
        }

        response = self.user_api.create_user(user_info)

        try:
            self.assertIn('user', response)
            self.assertNotEqual(response['user']['id'], -1)
            self.assertNotEqual(response['user']['created'], one_hour_ago)
            self.assertNotEqual(response['user']['age_last_modified'], one_hour_ago)
            self.assertEqual(response['user']['profile_photo'], None)
            self.assertEqual(response['user']['deleted'], None)
        finally:
            # hard delete this user
            response = self.user_api.hard_delete_user(response['user']['id'], self.privileged_token)
            self.assertIn('success', response)

    def test_create_user_hide_hidden_columns_in_response_pos(self):
        """test hidden columns are correctly hidden in the create_user response"""

        user_info = {
            # required fields
            'user_name': 'integration_test',
            'first_name': 'integration_test_first_name',
            'last_name': 'integration_test_last_name',
            'email': 'integration_test@email.com',
            'password': 'abcxyz'
        }

        response = self.user_api.create_user(user_info)

        try:
            self.assertIn('user', response)
            self.assertNotIn('password', response['user'])
        finally:
            # hard delete this user
            response = self.user_api.hard_delete_user(response['user']['id'], self.privileged_token)
            self.assertIn('success', response)

    def test_create_user_missing_req_fields_neg(self):
        """test create user with missing last_name and password"""

        user_info = {
            'user_name': 'test',
            'first_name': 'test_first_name',
            'email': 'test@email.com'
        }
        response = self.user_api.create_user(user_info)
        self.assertIn('error', response)
        self.assertEqual(response['error']['msg'],
                         'Required fields [ last_name, password ] are missing from json payload.')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        suite = unittest.TestSuite()
        suite.addTest(sys.argv[1])
    else:
        suite = unittest.TestLoader().loadTestsFromTestCase(UserTestSuite)

    unittest.TextTestRunner(verbosity=2).run(suite)
