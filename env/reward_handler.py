from utility import read_build_cost
from env.time_handler import *


def c2r(build_id, terminal):
    """
    Convert build cost to reward
    :param build_id: building id
    :type build_id: int
    :param terminal: terminal building
    :type terminal: int
    :return: reward
    :rtype: float
    """
    cost = read_build_cost(terminal)
    all_cost = [float(i) for i in cost]
    build_cost = read_build_cost(build_id)
    build_cost = [float(i) for i in build_cost]
    for i in range(4):
        if all_cost[i] == 0:
            build_cost[i] = 1
            continue
        build_cost[i] /= all_cost[i]
    return sum(build_cost) / 4.0


class RewardHandler(object):
    def get_reward(self, prev_state, cur_state, action):
        pass


class ExampleReward(RewardHandler):
    def get_reward(self, prev_state, cur_state, action):
        return 0


class StepTimeRelated(RewardHandler):
    def __init__(self, th):
        """
        Init.
        :param th: time handler
        :type th: TimeHandler
        """
        self.th = th

    def get_reward(self, prev_state, cur_state, action):
        import math
        if action.cmd == "FastForward":
            return 0
        c_t = 2
        f_t = max(0, self.th.last_idle_time - c_t * action.time)
        r = c2r(action.build_id, 103)
        r_a = r * math.exp(-f_t)
        return r_a


class TotalTimeRelated(RewardHandler):
    def __init__(self, th, goal_time=468000):
        """
        Init.
        :param th: time handler
        :type th: TimeHandler
        """
        self.th = th
        self.goal_time = goal_time
    def get_reward(self, prev_state, cur_state, action):
        if not action.cmd == "ReqBuildUpdate":
            return 0
        if not action.build_id == 103:
            return 0
        else:
            c_t = 2.14e-6
            f_t = max(0, self.goal_time - self.th.total_time)
            r_a = c_t * f_t
        return r_a
