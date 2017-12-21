# -*- coding: utf-8 -*-
import time
import copy
import socket
import threading
import sys
import json
import random
import ste_pb2 as sp
import binascii
import rsp
from lib import pbjson
from tcpclient import TcpClient, AppFrame
from Queue import Queue
from struct import pack, unpack
from config import *
from actions.base import *
from actions.build import *
from actions.fastforward import *
from actions.army import *
import logging
from logging.handlers import RotatingFileHandler

def add_log(name, debug=False):
    logger = logging.getLogger(name)
    if debug:
        handler = RotatingFileHandler('%s.log' % name)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    return logger


class UserClient(object):
    def __init__(self, user_name, debug=False):
        self.logger = add_log('mala_%s' % user_name, debug)
        self.user_id = 0
        self.user_name = user_name
        self.tcp_client = TcpClient(self)
        self.tcp_client.setDaemon(True)
        self.tcp_client.start()
        self.user_data = None
        self.action_state = 0
        self.enabled_actions = ['build', 'army', 'fast_forward']

    def on_message(self, message):
        self.logger.debug('on_message#############################')
        self.logger.debug(message)
        self.logger.debug('#######################################')
        if message.result == 0:
            func = rsp.cmd_prot_rsp_method.get(message.cmd)
            if func is None:
                rsp.default_func(self, message)
                return
            self.logger.debug('func_name: ' + func.__name__)
            func(self, message)
        else:
            self.logger.debug(message)

    def send_message(self, cmd, data):
        self.logger.debug('send_message: ' + cmd)
        self.logger.debug(data)
        cs_info = sp.CsInfo(**data)
        cs_info.cmd = getattr(sp, cmd)
        cs_info.id = self.user_id
        send_af = AppFrame()
        send_af.message = cs_info
        send_af.frame_command = cs_info.cmd
        send_af.frame_id = cs_info.id
        self.tcp_client.send(send_af)

    def get_action_list(self):
        """agent使用 获取当前可用的Action"""
        self.update()
        self.full_resource()
        action_list = self._get_action_list()
        if not [a for a in action_list if a.status == 0]:
            if ActionLogin(self).run():
                action_list = self._get_action_list()
        return action_list

    def _get_action_list(self):
        action_list = []
        if 'build' in self.enabled_actions:
            action_list += create_build_actions(self)
        if 'army' in self.enabled_actions:
            action_list += create_army_actions(self)
        if 'fast_forward' in self.enabled_actions:
            action_list += create_fast_forward_actions(self)
        return action_list

    def get_user_data(self):
        """agent使用 获取游戏状态信息"""
        return copy.deepcopy(self.user_data)

    def update(self):
        self._update_progress()

    def _update_progress(self):
        pass

    def login(self):
        self.tcp_client.open()
        if ActionLogin(self).run():
            return True
        self.tcp_client.close()
        return False

    def register(self):
        if self.login():
            ActionMove(self).run()
            return True
        return False

    def heart(self):
        def _heart():
            self.send_message('ReqHeart', {'req_heart': {'revert': 1}})
            t = threading.Timer(30, _heart)
            t.setDaemon(True)
            t.start()
        timer = threading.Timer(30, _heart)
        timer.setDaemon(True)
        timer.start()

    def add_cash(self, cash=1000):
        data = {
            'req_gm': {
                'gm_info': {
                    'gm_cmd': ['add_cash', str(cash)]
                    }
                }
            }
        self.send_message('ReqGM', data)

    def add_resource(self, _type, num):
        num = str(num)
        if _type == 'cash':
            gm_cmd = ['add_cash', num]
        elif _type == 'energy':
            gm_cmd = ['add_resource', '0', num]
        elif _type == 'mineral':
            gm_cmd = ['add_resource', '1', num]
        elif _type == 'crystal':
            gm_cmd = ['add_resource', '2', num]
        elif _type == 'alloy':
            gm_cmd = ['add_resource', '3', num]
        else:
            return
        data = {
            'req_gm': {
                'gm_info': {
                    'gm_cmd': gm_cmd
                    }
                }
            }
        self.send_message('ReqGM', data)

    def full_resource(self):
        energy_max = self.user_data['city_count']['energy_max']
        mineral_max = self.user_data['city_count']['mineral_max']
        energy = energy_max - self.user_data['base_info']['energy']
        mineral = mineral_max - self.user_data['base_info']['mineral']
        if energy > 0:
            self.add_resource('energy', energy)
            self.user_data['base_info']['energy'] = energy_max
        if mineral > 0:
            self.add_resource('mineral', mineral)
            self.user_data['base_info']['mineral'] = mineral_max
        self.logger.debug('add_resource: %s%s' % (energy, mineral))

        if self.user_data['base_info']['crystal'] < 100:
            self.add_resource('crystal', 1000)
            self.user_data['base_info']['crystal'] += 1000
        if self.user_data['base_info']['alloy'] < 100:
            self.add_resource('alloy', 1000)
            self.user_data['base_info']['alloy'] += 1000
