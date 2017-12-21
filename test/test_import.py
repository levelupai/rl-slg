import unittest
from env import env_test


class TestEnvImport(unittest.TestCase):
    def setUp(self):
        pass

    def test_import(self):
        self.assertEqual(env_test.state, 'ok')

    def test_google_protobuf(self):
        import google.protobuf as pb
        self.assertIsNotNone(pb.__version__)

    def test_redis(self):
        import redis
        self.assertIsNotNone(redis.__version__)


if __name__ == '__main__':
    unittest.main()
