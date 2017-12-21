#coding=utf-8
import time
from base import *
from ..config import *

def create_build_actions(uc):
    action_list = []
    create_build(uc, action_list)
    create_build_update(uc, action_list)
    return action_list

def create_build(uc, action_list):
    """获取当前可建造的Action"""
    # if self._build_progress_info():
    #     return
    building_list = uc.user_data['building_info']['building_list']
    _type = building_list[0]['type']
    space_station = config_space_station.get(_type)
    count = len([b for b in building_list if b['pos'] / 10 == _type % 100])
    if space_station.ss_slots <= count:
        return
    for build in config_build.values():
        #2.前置建筑需要建造了才能造
        if not _build_prebuild(build, uc.user_data):
            continue
        #3.电力不足了不能造
        if build.build_allbuildcost[0] > uc.user_data['base_info']['energy']:
            continue
        #4.资源不足了不能造
        if build.build_allbuildcost[1] > uc.user_data['base_info']['mineral']:
            continue
        if build.build_allbuildcost[2] > uc.user_data['base_info']['crystal']:
            continue
        if build.build_allbuildcost[3] > uc.user_data['base_info']['alloy']:
            continue
        #5，需要满足build_minss,build_maxss条件
        #level = building_list[0]['level']
        if not build.build_minss:
            continue
        #9.该类型建筑已满
        if _build_high_line(build, uc.user_data):
            continue
        build_type = build.build_id
        pos_s = set(build.build_minss) - set([b['pos'] for b in building_list])
        if not pos_s:
            continue
        pos = pos_s.pop()
        action = ActionBuild(uc, build_type=build_type, pos=pos, time=build.build_allbuildtime)
        action_list.append(action)

def create_build_update(uc, action_list):
    """获取当前可升级的Action"""
    # if self._build_progress_info():
    #     return
    building_list = uc.user_data['building_info']['building_list']
    for building in building_list:
        if building['status'] != 0:
            continue
        build = config_build.get(building['type'])
        build = config_build.get(build.build_nextlevel)
        #2.前置建筑需要建造了才升级
        if not _build_prebuild(build, uc.user_data):
            continue
        #3.电力不足了不升级
        if build.build_buildcost[0] > uc.user_data['base_info']['energy']:
            continue
        #4.资源不足了不升级
        if build.build_buildcost[1] > uc.user_data['base_info']['mineral']:
            continue
        if build.build_buildcost[2] > uc.user_data['base_info']['crystal']:
            continue
        if build.build_buildcost[3] > uc.user_data['base_info']['alloy']:
            continue
        #5，需要满足build_minss,build_maxss条件
        # if building_list[0]['level'] not in build.build_maxss:
        #     continue
        # if build.build_minss != 0:
        #     continue
        #6.需要满足max_level条件
        if build.build_maxlevel <= building['level']:
            continue
        action = ActionBuildUpdate(uc, inst_id=building['inst'], time=build.build_buildtime, build_id=build.build_id)
        action_list.append(action)

class ActionBuild(Action):
    """建造"""
    def __init__(self, user_client, **kwargs):
        super(ActionBuild, self).__init__(user_client)
        self.cmd = 'ReqBuild'
        self.time = kwargs.get('time', 0)
        self.build_id = kwargs.get('build_type')
        self.data = {
            'req_build': {
                'build_type': kwargs.get('build_type', 0),
            	'pos': kwargs.get('pos', 0),
            	'quick': 0,
            	'step': 0
            }
        }
        self.get_id()

    def run(self):
        if super(ActionBuild, self).run():
            progress_speed(self.user_client, self.time)
            return True
        else:
            return False


class ActionBuildUpdate(Action):
    """升级"""
    def __init__(self, user_client, **kwargs):
        super(ActionBuildUpdate, self).__init__(user_client)
        self.cmd = 'ReqBuildUpdate'
        self.time = kwargs.get('time', 0)
        self.build_id = kwargs.get('build_id')
        self.data = {
            'req_build_update': {
                'inst_id': kwargs.get('inst_id', 0),
            	'quick': 0,
            	'step': 0
            }
        }
        self.get_id()

    def run(self):
        if super(ActionBuildUpdate, self).run():
            progress_speed(self.user_client, self.time)
            return True
        else:
            return False


def _build_progress_info(user_data):
    #7.建造队列是否被占用
    if user_data['progress_info'].get('begin'):
        p_i_list = [user_data['progress_info']]
    else:
        p_i_list = user_data['progress_info'].get('progress_info', [])
    for p in p_i_list:
        if not p.get('end_time'):
            p['end_time'] = p['begin'] + p['totaltime'] - p['speedtime']
        if p['type'] == 1 and p['end_time'] + 2 > time.time():
            return True
    return False

def _build_prebuild(build, user_data):
    #2.前置建筑需要建造了才建造或升级
    if not build.build_prebuild:
        return True
    pre2 = []
    for pre in build.build_prebuild:
        for building in user_data['building_info']['building_list']:
            bid = building['type']
            if bid / 100 == pre / 100 and bid % 100 >= pre % 100:
                pre2.append(pre)
                break
    if build.build_prebuild == pre2:
        return True
    return False

def _build_high_line(build, user_data):
    #该类型建筑是否已满
    _type_high_line_map = {
        2: 'ss_estation',  #发电站
        3: 'ss_tstation',  #贸易站
        4: 'ss_shipyard',  #船坞
        5: 'ss_dcenter',  #舰船中心
        6: 'ss_rcenter',  #科研中心
        7: 'ss_defense',  #防卫体系
        8: 'ss_school',  #军事学院
        9: 'ss_prison',  #监狱
        11: 'ss_radar',  #雷达
    }
    building_list = user_data['building_info']['building_list']
    ss_id = building_list[0]['type']
    _type = build.build_id / 100
    if _type == 1:
        return True
    num = len([b for b in building_list if b['type'] / 100 == _type])
    type_name = _type_high_line_map.get(_type)
    if not type_name:
        return False
    if getattr(config_space_station.get(ss_id), type_name) > num:
        return False
    return True
