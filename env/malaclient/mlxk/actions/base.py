#coding=utf-8
import time
import redis
from ..config import *


class ActionStore(object):
    """把action持久化"""
    def __init__(self):
        self.r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, password='random')

    def get_id(self, action):
        rkey = 'action:%s:%s' % (action.cmd, str(action.data))
        _id = self.r.get(rkey)
        if _id is None:
            _id = self.r.incr('action_maxid')
            self.r.set(rkey, _id)
        action.id = int(_id)


action_store = ActionStore()


class Action(object):
    """游戏action类的基类"""
    def __init__(self, user_client):
        self.store = action_store
        self.user_client = user_client
        self.id = 0
        self.cmd = None
        self.data = None
        self.time = 0
        self.status = 0

    def run(self):
        if self.cmd is None or self.data is None:
            return False
        self.user_client.action_state = 0
        for j in range(3):
            self.user_client.send_message(self.cmd, self.data)
            for i in range(30):
                time.sleep(0.1)
                if self.user_client.action_state == 1:
                    return True
            time.sleep(1)
        return False

    def get_id(self):
        self.store.get_id(self)


class ActionBuyItem(Action):
    """购买"""
    def __init__(self, user_client, **kwargs):
        super(ActionBuyItem, self).__init__(user_client)
        self.cmd = 'ReqBuyItem'
        self.data = {
            'ext_info':{
                'req_buyitem': {
                    'item_id': kwargs.get('item_id', 0),
            	    'item_num': kwargs.get('item_num', 0)
                }
            }
        }
        self.get_id()


class ActionMove(Action):
    """移动"""
    def __init__(self, user_client, **kwargs):
        super(ActionMove, self).__init__(user_client)
        self.cmd = 'ReqMove'
        pos = {'k': 0, 's': 0, 'x': 0, 'y': 0}
        self.data = {
            'ext_info':{
                'req_move': {
                    'target_position': kwargs.get('target_position', pos),
            	    'from_position': kwargs.get('from_position', pos)
                }
            }
        }
        self.get_id()


class ActionLogin(Action):
    """登陆"""
    def __init__(self, user_client):
        super(ActionLogin, self).__init__(user_client)
        self.cmd = 'ReqNewLogin'
        self.data = {
            'req_login': {
                'user_name': user_client.user_name,
                'password': '',
                'type': 0,
                'language': 'English',
                'phone_type': 1,
                'source_ver': '0.0.1',
                'app_ver': '0.0.1',
            }
        }
        self.get_id()


class ActionProgressSpeed(Action):
    """加速"""
    def __init__(self, user_client, **kwargs):
        super(ActionProgressSpeed, self).__init__(user_client)
        self.cmd = 'ReqProgressSpeed'
        self.data = {
            'req_progress_speed': {
                'progress_inst_id': kwargs.get('progress_inst_id', 0),
            	'item_id': kwargs.get('item_id', 0)
            }
        }
        self.get_id()


def progress_speed0(uc):
    """agent使用 给建造加速"""
    #取进度条信息
    def get_progress():
        if uc.user_data['progress_info'].get('begin'):
            p_i_list = [uc.user_data['progress_info']]
        else:
            p_i_list = uc.user_data['progress_info'].get('progress_info', [])
        for p in p_i_list:
            if p['type'] == 1 and p['end_time'] > time.time():
                return p
        return None
    progress = get_progress()
    if progress is None:
        return 0 #不需要加速
    #取加速道具
    item_id = 0
    remaining_time = time.time() - progress['end_time']
    for i in range(17, 26):
        if config_items[i].item_param1 > remaining_time:
            item_id = i
            break
    if item_id == 0:
        return -1 #没有合适的加速道具
    if self.user_data['base_info'].get('cash', 0) < config_items[item_id].item_price:
        return -2 #没有钱买道具
    #购买加速道具
    action_buy = ActionBuyItem(uc, item_num=1, item_id=item_id)
    if not action_buy.run():
        return -3 #购买失败
    #使用道具加速
    action = ActionProgressSpeed(uc, progress_inst_id=progress['progress_inst'], item_id=item_id)
    if action.run():
        return 1 #加速成功
    return -5 #加速失败

def progress_speed(uc, remaining_time):
    """给建造加速"""
    #取进度条信息
    def get_progress():
        if uc.user_data['progress_info'].get('begin'):
            p_i_list = [uc.user_data['progress_info']]
        else:
            p_i_list = uc.user_data['progress_info'].get('progress_info', [])
        for p in p_i_list:
            if p['type'] == 1 and p['end_time'] > time.time():
                return p
        return None
    progress = get_progress()
    if progress is None:
        return 0 #不需要加速
    #取加速道具
    item_id = 0
    for i in range(17, 26):
        if config_items[i].item_param1 > remaining_time:
            item_id = i
            break
    if item_id == 0:
        return -1 #没有合适的加速道具
    if uc.user_data['base_info'].get('cash', 0) < config_items[item_id].item_price:
        #return -2 #没有钱买道具
        uc.add_cash(10000)
        time.sleep(1)
    #购买加速道具
    action_buy = ActionBuyItem(uc, item_num=1, item_id=item_id)
    if not action_buy.run():
        return -3 #购买失败
    #使用道具加速
    action = ActionProgressSpeed(uc, progress_inst_id=progress['progress_inst'], item_id=item_id)
    if action.run():
        return 1 #加速成功
    return -5 #加速失败
