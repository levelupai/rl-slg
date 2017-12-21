#coding=utf-8
from base import Action

def create_fast_forward_actions(uc):
    action_list = []
    action_list.append(ActionFastForwardM15(uc))
    action_list.append(ActionFastForwardM30(uc))
    action_list.append(ActionFastForwardH1(uc))
    action_list.append(ActionFastForwardH2(uc))
    action_list.append(ActionFastForwardH5(uc))
    return action_list


class ActionFastForwardM15(Action):
    """快进15分钟"""
    def __init__(self, user_client, **kwargs):
        super(ActionFastForwardM15, self).__init__(user_client)
        self.cmd = 'FastForward'
        self.data = {'minute': 15}
        self.status = -1
        self.get_id()

    def run(self):
        _fast_forward(self.user_client, self.data['minute'])
        return True


class ActionFastForwardM30(ActionFastForwardM15):
    """快进30分钟"""
    def __init__(self, user_client, **kwargs):
        super(ActionFastForwardM30, self).__init__(user_client)
        self.data = {'minute': 30}
        self.get_id()


class ActionFastForwardH1(ActionFastForwardM15):
    """快进1小时"""
    def __init__(self, user_client, **kwargs):
        super(ActionFastForwardH1, self).__init__(user_client)
        self.data = {'minute': 60}
        self.get_id()


class ActionFastForwardH2(ActionFastForwardM15):
    """快进2小时"""
    def __init__(self, user_client, **kwargs):
        super(ActionFastForwardH2, self).__init__(user_client)
        self.data = {'minute': 120}
        self.get_id()


class ActionFastForwardH5(ActionFastForwardM15):
    """快进5小时"""
    def __init__(self, user_client, **kwargs):
        super(ActionFastForwardH5, self).__init__(user_client)
        self.data = {'minute': 300}
        self.get_id()


def _fast_forward(uc, minute):
    #计算出要增加的资源
    energy = uc.user_data['city_count']['energy_recover'] * minute / 60
    mineral = uc.user_data['city_count']['mineral_recover'] * minute / 60
    energy_max = uc.user_data['city_count']['energy_max']
    mineral_max = uc.user_data['city_count']['mineral_max']
    if uc.user_data['base_info']['energy'] + energy > energy_max:
        energy = energy_max - uc.user_data['base_info']['energy']
    if uc.user_data['base_info']['mineral'] + mineral > mineral_max:
        mineral = mineral_max - uc.user_data['base_info']['mineral']
    #加资源
    if energy > 0:
        uc.add_resource('energy', energy)
        uc.user_data['base_info']['energy'] += energy
    if mineral > 0:
        uc.add_resource('mineral', mineral)
        uc.user_data['base_info']['mineral'] += mineral
