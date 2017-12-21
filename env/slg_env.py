import malaclient.mlxk.mala as mala
from env.state_handler import StateHandler
from env.terminal_handler import TerminalHandler
from env.reward_handler import RewardHandler
from env.time_handler import TimeHandler


def check_setup(fn):
    """
    Check if the environment is set up properly
    """

    def check(*args):
        if not args[0].is_setup:
            raise Exception('Enviroment is not properly setup.')
        return fn(*args)

    return check


class SLGEnv(object):
    """
    SLG game training environment.
    """

    def __init__(self, sh, th, rh, time_h):
        """
        Initial user client.
        :param sh: generate state, see state_handler for more information
        :type sh: StateHandler
        :param th: terminal handler
        :type th: TerminalHandler
        :param rh: reward handler
        :type rh: RewardHandler
        :param time_h: time handler
        :type time_h: TimeHandler
        """
        self.__sh = sh
        self.__rh = rh
        self.__th = th
        self.__time_h = time_h
        self.is_setup = False

    def setup(self, user_name):
        """
        Set up environment for training.
        :return: If no error return True, otherwise False.
        """
        self.user_name = user_name
        self.__client = mala.UserClient(user_name)
        if self.__client.register():
            self.is_setup = True
            self.__time_h.clear_up()
            self.user_id = self.__client.user_id
            return True
        return False

    @check_setup
    def get_state(self):
        """
        Get state using state handler
        :return: state
        """
        return self.__sh.get_state(self.__client.get_user_data())

    @check_setup
    def get_raw_state(self):
        """
        Get state using state handler
        :return: state
        """
        return self.__sh.get_raw_state(self.__client.get_user_data())

    @check_setup
    def save_state(self, file_name='state.json'):
        """
        Save current state to state.json
        """
        import json, utility
        with open(utility.get_data_path() + '/' + file_name, 'w+') as f:
            json.dump(self.__client.get_user_data(), f, indent=2, sort_keys=True)

    @check_setup
    def reward_function(self, prev_state, cur_state, action):
        """
        Reward function
        :param prev_state: previous state
        :param cur_state: current state
        :param action: last action
        :return: reward
        """
        return self.__rh.get_reward(prev_state, cur_state, action)

    @check_setup
    def is_terminal(self):
        """
        Terminate if agent reached a certain state or exceed limit time
        :return: boolean value
        :rtype: bool
        """
        return self.__th.is_terminal(self.__client.get_user_data())

    @check_setup
    def is_exceed_time_limit(self):
        """
        True if total time exceed time limit
        :return: boolean value
        :rtype: bool
        """
        return self.__time_h.total_time > self.__time_h.total_time_limit

    @check_setup
    def action_generator(self):
        """
        Return an action list
        :return: action list
        :rtype: list
        """
        return self.__client.get_action_list()

    @check_setup
    def send_action(self, action):
        action.run()

    @check_setup
    def add_cash(self, num):
        self.__client.add_cash(num)

    @check_setup
    def update_time(self, action):
        self.__time_h.update_time(action)

    def get_state_len(self):
        return len(self.__sh)
