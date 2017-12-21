import random
import logging
import time


class ExampleAgent(object):
    def __init__(self, env):
        """
        Initialization

        :param env: training environment
        """
        self.env = env
        self.logger = logging.getLogger('ExampleAgent')

    def run(self):
        """
        Single episode of agent

        """
        self.logger.info('Episode start')
        t = 0
        prev_state = self.env.get_state()
        action = 0
        while not self.env.is_terminal():
            cur_state = self.env.get_state()
            self.logger.debug('\tState: %s' % cur_state)
            if t != 0:
                reward = self.env.reward_function(cur_state, prev_state)
                self.logger.debug('\tReward: %s' % reward)
                self.value_update(prev_state, action, reward)
                self.logger.debug('\tValue update')
            action_list = self.env.action_generator()
            self.logger.info('\tAction list: %s' % [a.data for a in action_list])
            action = self.policy(cur_state, action_list)
            self.logger.info('\tSelected action: %s' % action.data)
            self.env.send_action(action)
            prev_state = cur_state
            self.logger.info('\tWaiting')
            self.wait_step(action_list, 10)
            t += 1
        self.logger.info('Episode finished')

    def value_update(self, prev_state, action, reward):
        """
        Update value function

        :param prev_state: previous state
        :param action: last action
        :param reward: reward
        """
        pass

    def policy(self, cur_state, action_list):
        """
        Policy for agent

        :param cur_state: current state for making decision
        :param action_list: available action list
        :return: selected action
        """
        return action_list[random.randint(0, len(action_list) - 1)]

    def wait_step(self, action_list, max_wait_s=600):
        """
        Wait until step finish

        :param action_list: action list
        :param max_wait_s: max wait seconds
        """
        wait_s = 0
        new_list = self.env.action_generator()
        while [a.id for a in action_list] == [a.id for a in new_list] and wait_s < max_wait_s:
            if len(new_list) > 1:
                wait_s += 1
            time.sleep(1)
            new_list = self.env.action_generator()
