#coding=utf-8
import random
from base import Action
from ..config import *

def create_army_actions(uc):
    actions = []
    actions += _create_training_actions(uc)
    return actions

def _create_training_actions(uc):
    uc.logger.debug("_create_training_actions=======================start")
    actions = []
    #取所有现有建筑的ID
    bids = [b['type'] for b in uc.user_data['building_info']['building_list']]
    #看有没有船坞
    building_list = uc.user_data['building_info']['building_list']
    shipyard_list = [b for b in building_list if str(b['type'])[0] == '4']
    uc.logger.debug('shipyard_list: %s' % shipyard_list)
    if not shipyard_list:
        uc.logger.debug('----------------1')
        return [] #没有船坞
    #船坞上限,空位
    for sy in shipyard_list:
        sy['shipyard_index'] = config_shipyard.get(sy['type']).shipyard_index
        sy['open_num'] = sy['shipyard_index']
        sy['shipyard_shiptype'] = config_shipyard.get(sy['type']).shipyard_shiptype
        training_info = uc.user_data['army_info'].get('training_info')
        if training_info and training_info.get('ship_yard_id') == sy['inst_id']:
            sy['open_num'] -= training_info['army_desc']['soldier_num']
    uc.logger.debug('shipyard_list: %s' % shipyard_list)
    #遍历图纸
    for p in uc.user_data['plan_info']['planing_info']:
        inst_id = p['inst_id']
        ship_id = p['ship_id']
        shipyard_list1 = [sy for sy in shipyard_list if ship_id in sy['shipyard_shiptype']]
        if not shipyard_list1:
            continue #没有合适它的船坞
        ship = config_ship.get(ship_id)
        uc.logger.debug('inst_id: %s, ship_id: %s' % (inst_id, ship_id))
        uc.logger.debug('ship: %s' % ship.__dict__)
        if ship.ship_rank != 0: #需要设计中心
            if 500 + ship.ship_rank not in bids:
                uc.logger.debug('ship.ship_rank: %s' % ship.ship_rank)
                uc.logger.debug('----------------2')
                continue  #没有设计中心
        #工程船到上限
        if ship.ship_type == 2:
            ss = config_space_station.get(building_list[0]['type'])
            cnt = sum([a['soldier_num'] for a in uc.user_data['army_info']['army'] if a['soldier_type'] == 2])
            if cnt >= ss.ss_engships:
                uc.logger.debug('cnt: %s, ss.ss_engships: %s' % (cnt, ss.ss_engships))
                uc.logger.debug('----------------3')
                continue
        #资源不够
        uc.logger.debug('cslots: %s' % ship.ship_cslots)
        uc.logger.debug(uc.user_data['base_info'])
        if ship.ship_cslots[0] > uc.user_data['base_info']['energy']:
            uc.logger.debug('----------------4')
            continue
        if ship.ship_cslots[1] > uc.user_data['base_info']['mineral']:
            uc.logger.debug('----------------5')
            continue
        if ship.ship_cslots[2] > uc.user_data['base_info']['crystal']:
            uc.logger.debug('----------------6')
            continue
        if ship.ship_cslots[3] > uc.user_data['base_info']['alloy']:
            uc.logger.debug('----------------7')
            continue
        ship_yard_id = random.choice(shipyard_list1)['type']
        action = ActionTraining(uc, soldier_type=inst_id, ship_yard_id=ship_yard_id)
        actions.append(action)
        uc.logger.debug('action: %s' % action.data)
    return actions


class ActionTraining(Action):
    """造船"""
    def __init__(self, user_client, **kwargs):
        super(ActionTraining, self).__init__(user_client)
        self.cmd = 'ReqTraining'
        self.data = {
            'req_training':{
                'army_desc': {
                    'soldier_type': kwargs.get('soldier_type'),      #部队类型，设计图纸 inst_id
            	    'soldier_num': kwargs.get('soldier_num', 1),       #部队数量
            	    'total_hp': 0,		#总血量
            	    'total_shiled': 0,   #能量
            	    'full_soldier': 0,    #满血船的数量
            	    'shiled': 0,
            	    'shiled_time': 0
                },
            	'mineral': 0,
            	'energy': 0,
            	'crystal': 0,
            	'alloy': 0,
            	'use_time': 0,
            	'step': 0,			#新手引导step
            	'ship_yard_id': kwargs.get('ship_yard_id', 0),	#船坞inst_id
            }
        }
        self.get_id()


class ActionCreateFleet(Action):
    """创建舰队"""
    def __init__(self, user_client, **kwargs):
        super(ActionCreateFleet, self).__init__(user_client)
        self.cmd = 'ReqCreateFleet'
        self.data = {
            'ext_info':{
                'req_create_fleet':{
                    'army_desc': [{
                        'soldier_type': kwargs.get('inst_id'),      #部队类型，设计图纸 inst_id
                	    'soldier_num': 2,       #部队数量
                	    'total_hp': 0,		#总血量
                	    'total_shiled': 0,   #能量
                	    'full_soldier': 0,    #满血船的数量
                	    'shiled': 0,
                	    'shiled_time': 0
                    }],
                    'hero_inst_id': 0,
                    'inst_id': 1,
                    'fleet_name': 'yuan'
                }
            }
        }
        self.get_id()


class ActionArmyAction(Action):
    """舰队行为"""
    def __init__(self, user_client, **kwargs):
        super(ActionArmyAction, self).__init__(user_client)
        self.cmd = 'ReqArmyAction'
        pos = kwargs.get('target_position')
        self.data = {
            'req_army_action':{
                'taget_position': pos,
            	'from_position': self.user_client.user_data['base_info']['position'],
                'army_info': {
                    'show_info': {
                        'id': self.user_client.user_id,
                        'name': self.user_client.user_name,
                        'type': 1,
                        'inst_id': 0,
                        'refer_pos': pos,
                        'target': pos
                    },
                	'army_desc': [{
                        'soldier_type': 7,      #部队类型，设计图纸 inst_id
                	    'soldier_num': 1,       #部队数量
                	    'total_hp': 0,		#总血量
                	    'total_shiled': 0,   #能量
                	    'full_soldier': 0,    #满血船的数量
                	    'shiled': 0,
                	    'shiled_time': 0
                    }],
                	'army_source': [{
                        'type': 1,
                        'num': 2
                    }],
                	# 'hero_inst_id': 4,
                	# 'sys_id_list': [5],
                	# 'true_from': {
                    #         'k': 1,
                    # 	    's': 2,
                    # 	    'x': 3,
                    #         'y': 3
                    # },    #真实出发地
                	'true_target': pos,
                	# 'ftl_speed': 8,
                	# 'sol_speed': 9,
                	# 'ftl_cd': 10,
                }
            }
        }
        self.get_id()


class ActionMapInfo(Action):
    """获取太阳系信息"""
    def __init__(self, user_client, **kwargs):
        super(ActionMapInfo, self).__init__(user_client)
        self.cmd = 'ReqMapInfo'
        my_pos =  self.user_client.user_data['base_info']['position']
        self.data = {
            'req_map_info':{
                'k': kwargs.get('k', my_pos['k']),
            	's': kwargs.get('s', my_pos['s']),
            	'first_flag': kwargs.get('first_flag', 0)
            }
        }
        self.get_id()
