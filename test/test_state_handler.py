import unittest
from env.utility import read_test_client_state
from env.state_handler import *


class TestStateHandler(unittest.TestCase):
    def setUp(self):
        pass

    def test_example_get_state(self):
        sh = ExampleState()
        self.assertEqual(sh.get_state(read_test_client_state()), [1])


if __name__ == '__main__':
    unittest.main()
