import unittest
from env.reward_handler import *
from env.time_handler import *


class TestRewardHandler(unittest.TestCase):
    def setUp(self):
        pass

    def test_step_time_related_reward(self):
        time_h = TimeHandler()
        rh = StepTimeRelated(time_h)

        class TestAction():
            pass

        action = TestAction()
        action.cmd = "Build"
        action.build_id = 401
        action.time = 16
        time_h.last_idle_time = 10
        self.assertGreater(rh.get_reward([], [], action), 0.50)
        self.assertLess(rh.get_reward([], [], action), 0.51)
        action.build_id = 103
        action.time = 9600
        time_h.last_idle_time = 600
        self.assertEqual(rh.get_reward([], [], action), 1.0)


if __name__ == '__main__':
    unittest.main()
