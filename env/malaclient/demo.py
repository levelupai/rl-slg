#coding=utf-8
# import sys
# sys.path.append('path')
import time
import random
from mlxk.config import *
from mlxk.actions.build import *
from mlxk.actions.army import *
from mlxk.actions.base import *
from mlxk.actions.fastforward import *
from mlxk.mala import UserClient

def build(uc):
    uc.add_cash(1000)
    cnt1 = 0
    while True:
        time.sleep(1)
        action_list = uc.get_action_list()
        print 'action_list: ', [a.data for a in action_list]
        if action_list:
            action = action_list[random.randint(0, len(action_list) - 1)]
            print 'action run: ', action.id, type(action.id)
            if action.run():
                cnt1 += 1
                print(cnt1)
            else:
                print "失败"
            #print uc.user_data['progress_info']
            print uc.user_data['building_info']['building_list']
            if cnt1 == 10:
                return

def create_fleet(uc):
    action_list = uc.get_action_list()
    print([a.data for a in action_list])
    # ActionTraining(uc, soldier_type=1, ship_yard_id=4).run()
    # progress_speed0(uc)
    if action_list:
        action = action_list[0]
        print(action.data)
        print action.run()

def army(uc):
    "采矿"
    ActionMapInfo(uc, first_flag=0).run()
    time.sleep(1)
    #return
    # print uc.user_data['map_info'].keys()
    # print uc.user_data['map_info']['mapmonsternode_list']
    msnl = [msn for msn in uc.user_data['map_info']['mapsoucenode_list'] if msn['armyinst'] == -1]
    #msnl = [msn for msn in uc.user_data['map_info']['mapcitynode_list']]
    print len(msnl)
    if msnl:
        pos = msnl[3]['position']
        print ActionArmyAction(uc, target_position=pos).run()
        time.sleep(10)

def main():
    uc = UserClient("ly39", True)
    uc.enabled_actions.remove('fast_forward')
    uc.enabled_actions.remove('army')
    # if not uc.register():
    #     return
    # uc.add_cash(10000)
    if not uc.login():
        return
    # build(uc)
    print uc.user_id
    #print uc.user_data['base_info']['position']
    uc.full_resource()
    #army(uc)
    uc.enabled_actions.remove('build')
    uc.enabled_actions.append('army')
    create_fleet(uc)

if __name__ == '__main__':
    main()
