import unittest
from env.slg_env import *
from env.state_handler import ExampleState
from env.terminal_handler import LevelCondition
from env.reward_handler import ExampleReward
from env.time_handler import TimeHandler
from env.utility import get_data_path


class TestSLGEnv(unittest.TestCase):
    def setUp(self):
        pass

    def test_env_init(self):
        env = SLGEnv(ExampleState(), LevelCondition(1), ExampleReward(), TimeHandler())
        self.assertTrue(True)

    def test_env_setup(self):
        env = SLGEnv(ExampleState(), LevelCondition(1), ExampleReward(), TimeHandler())
        self.assertTrue(env.setup('test_client'))

    def test_env_get_state(self):
        env = SLGEnv(ExampleState(), LevelCondition(1), ExampleReward(), TimeHandler())
        env.setup('test_client')
        self.assertEqual(env.get_state(), [1])

    def test_env_save_state(self):
        env = SLGEnv(ExampleState(), LevelCondition(1), ExampleReward(), TimeHandler())
        env.setup('test_client')
        env.save_state()
        import json
        with open(get_data_path() + '/' + 'state.json', 'r+') as f:
            usr_data = json.load(f)
        self.assertEqual(ExampleState().get_state(usr_data), [1])


if __name__ == '__main__':
    unittest.main()
