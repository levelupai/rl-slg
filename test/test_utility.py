import unittest
from env.utility import *


class TestStateHandler(unittest.TestCase):
    def setUp(self):
        pass

    def test_n2sn(self):
        sn = n2sn(130)
        self.assertTupleEqual(sn, (0.13, 0.15))
        sn = n2sn(9000)
        self.assertTupleEqual(sn, (0.9, 0.2))

    def test_example_config(self):
        config = read_config('config.example.json')
        self.assertEqual(config['user_name'], 'test_client')

    def test_generate_user_name(self):
        un = generate_user_name()
        self.assertEqual(len(un), 26)


if __name__ == '__main__':
    unittest.main()
