from utility import *


class StateHandler(object):
    def __init__(self):
        pass

    def get_state(self, usr_data):
        """
        Get state from user data
        :param usr_data: user data
        :type usr_data: dict
        :return: state
        :rtype: list
        """
        return []

    def get_raw_state(self, usr_data):
        """
        Get unprocessed state from user data
        :param usr_data: user data
        :return:
        """
        return []

    def __len__(self):
        return 0


class ExampleState(StateHandler):
    def get_state(self, usr_data):
        """
        An example
        :param usr_data: user data
        :type usr_data: dict
        :return: level of base
        :rtype: list
        """
        return [usr_data['base_info']['level']]

    def get_raw_state(self, usr_data):
        """
        An example
        :param usr_data: user data
        :type usr_data: dict
        :return: level of base
        :rtype: list
        """
        return [usr_data['base_info']['level']]

    def __len__(self):
        return 1


class ResourceOnly(StateHandler):
    def get_state(self, usr_data):
        """
        State only generate from resource
        :param usr_data: user data
        :type usr_data: dict
        :return: 12-dim vector
        :rtype: list
        """
        state = []
        base_info = usr_data['base_info']
        # four resource
        state += n2sn(base_info['energy'])
        state += n2sn(base_info['mineral'])
        state += n2sn(base_info['crystal'])
        state += n2sn(base_info['alloy'])
        # source increment over time
        city_count = usr_data['city_count']
        state += n2sn(city_count['energy_recover'])
        state += n2sn(city_count['mineral_recover'])
        return state

    def get_raw_state(self, usr_data):
        state = []
        base_info = usr_data['base_info']
        state += [base_info['energy'], base_info['mineral'], base_info['crystal'], base_info['alloy']]
        city_count = usr_data['city_count']
        state += [city_count['energy_recover'], city_count['mineral_recover']]
        return state

    def __len__(self):
        return 12
