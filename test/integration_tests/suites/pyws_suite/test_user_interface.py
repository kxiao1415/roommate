import sys
import unittest
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
        cls.user_api.hard_delete_user(cls.test_user_id, cls.privileged_token)

    def test_authenticate_user_positive(self):
        response = self.user_api.authenticate_user(self.test_user_info)

        # Since this test user is already authenticated in the setUpClass()
        # We just need to make sure the token in the response is the same
        self.assertIn('token', response)
        self.assertEqual(response['token'], self.test_user_token)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        suite = unittest.TestSuite()
        suite.addTest(sys.argv[1])
    else:
        suite = unittest.TestLoader().loadTestsFromTestCase(UserTestSuite)

    unittest.TextTestRunner(verbosity=2).run(suite)
