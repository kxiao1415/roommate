import sys, os
import unittest
from datetime import datetime, timedelta

from test.integration_tests.test_config import TestConfig
from api_bindings import user_api


class UserTestSuite(unittest.TestCase):

    user_api = None

    test_user_info = {
        'user_name': 'test',
        'email': 'k.xiao1415@gmail.com',
        'password': 'abcxyz',
        'gender': 'M',
        'age': 30,
        'preference': {
            'gender': 'F',
            'age_group': '30-35'
        }
    }

    test_user_id = None
    test_user_token = None
    privileged_token = TestConfig.PRIVILEGED_TOKEN

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

    def test_get_user_pos(self):
        """test successfully get a user"""

        response = self.user_api.get_user(self.test_user_id)
        self.assertIn('user', response)
        self.assertIn('preference', response['user'])

    def test_get_user_non_existing_user_neg(self):
        """test get a user that does not exist"""

        response = self.user_api.get_user(-1)
        self.assertIn('error', response)

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
            'email': 'k.xiao1415@gmail.com',
            'password': 'wrong password'
        }

        response = self.user_api.authenticate_user(user_info)
        self.assertIn('error', response)
        self.assertEqual(response['error']['msg'],
                         'No user matching the email and password combination.')

        # case 2. wrong user_email
        user_info = {
            'email': 'wrong email',
            'password': 'abcxyz'
        }

        response = self.user_api.authenticate_user(user_info)
        self.assertIn('error', response)
        self.assertEqual(response['error']['msg'],
                         'No user matching the email and password combination.')

        # case 3. no info
        user_info = {}

        response = self.user_api.authenticate_user(user_info)
        self.assertIn('error', response)
        self.assertEqual(response['error']['msg'],
                         'Required fields [ email, password ] are missing from json payload.')

    def test_create_user_pos(self):
        """test successfully creating a user"""

        user_info = {
            # required fields
            'user_name': 'integration_test',
            'email': 'integration_test@email.com',
            'password': 'abcxyz',

            # preference
            'preference': {
                'gender': 'M',
                'age_group': '21-25'
            }
        }

        response = self.user_api.create_user(user_info)

        try:
            self.assertIn('user', response)

            # make sure 'password' is not in the response
            self.assertNotIn('password', response['user'])

            # make sure private fields are properly handled
            self.assertNotEqual(response['user']['id'], None)
            self.assertNotEqual(response['user']['created_time'], None)
            self.assertNotEqual(response['user']['age_last_modified'], None)
            self.assertEqual(response['user']['profile_photo'], None)
            self.assertEqual(response['user']['last_deleted_time'], None)

            # make sure preference is created
            for key in user_info['preference']:
                self.assertEqual(response['user']['preference'][key],
                                 user_info['preference'][key])

        finally:
            # hard delete this user
            response = self.user_api.hard_delete_user(response['user']['id'], self.privileged_token)
            self.assertIn('success', response)

    def test_create_user_missing_req_fields_neg(self):
        """test create user with missing required fields"""

        # missing user_name and password
        user_info = {
            'email': 'test@email.com'
        }
        response = self.user_api.create_user(user_info)
        self.assertIn('error', response)
        self.assertEqual(response['error']['msg'],
                         'Required fields [ user_name, password ] are missing from json payload.')

    def test_create_user_with_not_allowed_fields_neg(self):
        """test create user with not allowed fields"""

        # Fields 'pref_test' are not allowed
        user_info = {
            'user_name': 'integration_test',
            'email': 'integration_test@email.com',
            'password': 'abcxyz',
            'preference': {
                'gender': 'M',
                'age_group': '30-35',
                'pref_test': 'not allowed'
            }
        }
        response = self.user_api.create_user(user_info)
        self.assertIn('error', response)
        self.assertEqual(response['error']['msg'],
                         "These fields {'preference': ['pref_test']} "
                         "are not allowed in the json payload.")

    def test_create_user_without_valid_json_payload_neg(self):
        """test create user without a valid json payload"""

        user_info = 'not a hash'

        response = self.user_api.create_user(user_info)
        self.assertIn('error', response)
        self.assertEqual(response['error']['msg'],
                         'Payload must be a valid hash.')

    def test_update_user_pos(self):
        """test successfully update a user"""

        # create a user
        user_info = {
            'user_name': 'integration_test',
            'email': 'integration_test@email.com',
            'password': 'abcxyz'
        }

        create_response = self.user_api.create_user(user_info)

        # make sure preference is not in the response
        self.assertIn('user', create_response)
        self.assertNotIn('preference', create_response['user'])

        # authenticate
        auth_response = self.user_api.authenticate_user(user_info)

        # update a user
        update_user_info = {
            'user_name': 'update_test',
            'email': 'update_test@email.com',
            'age': 30,

            # preference
            'preference': {
                'age_group': '35-40',
                'gender': 'F'
            }
        }

        update_response = self.user_api.update_user(create_response['user']['id'],
                                                    update_user_info,
                                                    auth_response['token'])

        try:
            self.assertIn('success', update_response)

            # get the new user info
            get_response = self.user_api.get_user(create_response['user']['id'])

            # make sure public fields are updated
            public_fields = ['user_name', 'email', 'age']
            for field in public_fields:
                self.assertEqual(update_user_info[field], get_response['user'][field])

            # make sure private field 'age_last_modified' is updated
            self.assertNotEqual(get_response['user']['age_last_modified'],
                                create_response['user']['age_last_modified'])

            # make sure preference is created
            self.assertIn('preference', get_response['user'])
            # make sure preference is created
            for key in update_user_info['preference']:
                self.assertEqual(get_response['user']['preference'][key],
                                 update_user_info['preference'][key])

        finally:
            # hard delete this user
            response = self.user_api.hard_delete_user(create_response['user']['id'], self.privileged_token)
            self.assertIn('success', response)

    def test_update_user_deleted_pos(self):
        """test successfully delete a user"""

        # create a user
        user_info = {
            'user_name': 'integration_test',
            'email': 'integration_test@email.com',
            'password': 'abcxyz'
        }

        create_response = self.user_api.create_user(user_info)

        # authenticate
        auth_response = self.user_api.authenticate_user(user_info)

        update_user_info = {
            'deleted': True
        }

        update_response = self.user_api.update_user(create_response['user']['id'],
                                                    update_user_info,
                                                    auth_response['token'])

        try:
            self.assertIn('success', update_response)

            # get the new user info
            get_response = self.user_api.get_user(create_response['user']['id'])
            self.assertIn('error', get_response)

            # authenticate the user
            auth_response = self.user_api.authenticate_user(user_info)
            self.assertIn('error', auth_response)

        finally:
            # hard delete this user
            response = self.user_api.hard_delete_user(create_response['user']['id'], self.privileged_token)
            self.assertIn('success', response)

    def test_update_user_without_auth_neg(self):
        """test update user without authentication token"""

        response = self.user_api.update_user(self.test_user_id, {}, None)
        self.assertIn('error', response)
        self.assertEqual(response['error']['msg'], 'Authentication required.')

    def test_update_user_wrong_user_id_neg(self):
        """test update wrong user"""

        response = self.user_api.update_user(-1, {}, self.test_user_token)
        self.assertIn('error', response)
        self.assertEqual(response['error']['msg'],
                         'User is not allowed to access this resource id -1.')

    def test_update_user_password_neg(self):
        """test update user with password"""

        user_info = {
            'password': 'not allowed with this end point'
        }

        response = self.user_api.update_user(self.test_user_id,
                                             user_info,
                                             self.test_user_token)

        self.assertIn('error', response)
        self.assertEqual(response['error']['msg'],
                         'Please refer to /reset_password/ end point for password update.')

    def test_upload_and_delete_user_photo_pos(self):
        """test successfully upload, then delete a user photo"""

        # upload a user photo
        response = self.user_api.upload_user_photo(self.test_user_id,
                                                   os.path.join(TestConfig.IMAGES_DIR, 'test.png'),
                                                   self.test_user_token)
        self.assertIn('success', response)

        # make sure user info is updated
        get_response = self.user_api.get_user(self.test_user_id)
        self.assertIn('user', get_response)
        self.assertEqual(get_response['user']['profile_photo'],
                         'user_{0}/photos/test.png'.format(self.test_user_id))

        # delete user photo
        response = self.user_api.delete_user_photo(self.test_user_id,
                                                   self.test_user_token)
        self.assertIn('success', response)

        # make sure user info is updated
        get_response = self.user_api.get_user(self.test_user_id)
        self.assertIn('user', get_response)
        self.assertEqual(get_response['user']['profile_photo'], None)

    def test_get_qualified_users_pos(self):
        """test successfully get a list of users given the filter criteria"""

        filter_criteria = {
            'gender': 'M',
            'age_group': '25-30'
        }
        response = self.user_api.get_quailified_users(filter_criteria)

        self.assertIn('users', response)
        self.assertEqual(1, len(response['users']))

    def test_send_password_reset_email_pos(self):
        """test get success in the api response"""

        response = self.user_api.get_password_reset_email(self.test_user_info['email'])
        self.assertIn('success', response)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        suite = unittest.TestSuite()
        suite.addTest(sys.argv[1])
    else:
        suite = unittest.TestLoader().loadTestsFromTestCase(UserTestSuite)

    unittest.TextTestRunner(verbosity=2).run(suite)
