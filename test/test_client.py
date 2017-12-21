import unittest
import random
from env.malaclient.mlxk.mala import UserClient


class TestClient(unittest.TestCase):
    def setUp(self):
        pass

    def test_userclient_init(self):
        client = UserClient('test_client')
        self.assertEqual(client.user_name, 'test_client')

    @unittest.skip('skip new user test')
    def test_newuser_login(self):
        client = UserClient('test_client_' + '%06d' % random.randint(0, 1000000))
        ret = client.login()
        self.assertTrue(ret)

    def test_olduser_login(self):
        client = UserClient('test_client')
        ret = client.login()
        self.assertTrue(ret)

    def test_user_data(self):
        client = UserClient('test_client')
        client.login()
        self.assertEqual(client.get_user_data()['base_info']['level'], 1)


if __name__ == '__main__':
    unittest.main()
