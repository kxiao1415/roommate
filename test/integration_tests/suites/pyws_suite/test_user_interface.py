import sys, os
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
        'password': 'abcxyz',
        'gender': 'M',
        'preference': {
            'gender': 'F',
            'age': 30
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
            'user_name': 'test',
            'password': 'wrong password'
        }

        response = self.user_api.authenticate_user(user_info)
        self.assertIn('error', response)
        self.assertEqual(response['error']['msg'],
                         'No user matching the user_name and password combination.')

        # case 2. wrong user_name
        user_info = {
            'user_name': 'wrong name',
            'password': 'abcxyz'
        }

        response = self.user_api.authenticate_user(user_info)
        self.assertIn('error', response)
        self.assertEqual(response['error']['msg'],
                         'No user matching the user_name and password combination.')

        # case 3. no info
        user_info = {}

        response = self.user_api.authenticate_user(user_info)
        self.assertIn('error', response)
        self.assertEqual(response['error']['msg'],
                         'Required fields [ user_name, password ] are missing from json payload.')

    def test_create_user_pos(self):
        """test successfully creating a user"""

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
            'created_time': one_hour_ago,
            'age_last_modified': one_hour_ago,
            'profile_photo': 'test/path/photo.png',
            'last_deleted_time': one_hour_ago,

            # preference
            'preference': {
                'gender': 'M',
                'age': 25
            }
        }

        response = self.user_api.create_user(user_info)

        try:
            self.assertIn('user', response)

            # make sure 'password' is not in the response
            self.assertNotIn('password', response['user'])

            # make sure private fields are properly handled
            self.assertNotEqual(response['user']['id'], -1)
            self.assertNotEqual(response['user']['created_time'], one_hour_ago)
            self.assertNotEqual(response['user']['age_last_modified'], one_hour_ago)
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

        # missing last_name and password
        user_info = {
            'user_name': 'test',
            'first_name': 'test_first_name',
            'email': 'test@email.com'
        }
        response = self.user_api.create_user(user_info)
        self.assertIn('error', response)
        self.assertEqual(response['error']['msg'],
                         'Required fields [ last_name, password ] are missing from json payload.')

    def test_create_user_with_not_allowed_fields_neg(self):
        """test create user with not allowed fields"""

        # Fields 'test' and 'pref_test' are not allowed
        user_info = {
            'test': 'not allowed',
            'user_name': 'integration_test',
            'first_name': 'integration_test_first_name',
            'last_name': 'integration_test_last_name',
            'email': 'integration_test@email.com',
            'password': 'abcxyz',
            'preference': {
                'gender': 'M',
                'age': 30
            }
        }
        response = self.user_api.create_user(user_info)
        self.assertIn('error', response)
        self.assertEqual(response['error']['msg'],
                         "These fields {'user': ['test']} "
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
            'first_name': 'integration_test_first_name',
            'last_name': 'integration_test_last_name',
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
        one_hour_ago = (datetime.utcnow() - timedelta(hours=1)).isoformat()

        update_user_info = {
            'user_name': 'update_test',
            'first_name': 'update_test_first_name',
            'last_name': 'update_test_last_name',
            'email': 'update_test@email.com',
            'age': 30,
            'password': 'new password',

            # private columns
            'id': -1,
            'created_time': one_hour_ago,
            'age_last_modified': one_hour_ago,
            'profile_photo': 'test/path/photo.png',
            'last_deleted_time': one_hour_ago,

            # preference
            'preference': {
                'age': 35,
                'gender': 'F'
            }
        }

        update_response = self.user_api.update_user(create_response['user']['id'],
                                                    update_user_info,
                                                    auth_response['token'])

        try:
            self.assertIn('success', update_response)

            # make sure the new password is saved by authenticating
            sec_auth_response = self.user_api.authenticate_user(update_user_info)
            self.assertIn('token', sec_auth_response)
            self.assertEqual(sec_auth_response['token'], auth_response['token'])

            # get the new user info
            get_response = self.user_api.get_user(create_response['user']['id'])

            # make sure public fields are updated
            public_fields = ['user_name', 'first_name', 'last_name', 'email', 'age']
            for field in public_fields:
                self.assertEqual(update_user_info[field], get_response['user'][field])

            # make sure non-update-able private fields are not updated
            non_update_able_private_fields = ['id', 'created_time', 'profile_photo', 'last_deleted_time']
            for field in non_update_able_private_fields:
                self.assertEqual(get_response['user'][field], create_response['user'][field])

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
            'first_name': 'integration_test_first_name',
            'last_name': 'integration_test_last_name',
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
            'gender': 'M'
        }
        response = self.user_api.get_quailified_users(filter_criteria)

        self.assertIn('users', response)
        self.assertEqual(1, len(response['users']))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        suite = unittest.TestSuite()
        suite.addTest(sys.argv[1])
    else:
        suite = unittest.TestLoader().loadTestsFromTestCase(UserTestSuite)

    unittest.TextTestRunner(verbosity=2).run(suite)
