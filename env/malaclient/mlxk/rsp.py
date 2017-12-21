# -*- coding: utf-8 -*-
import time
import json
import random
from lib import pbjson
import ste_pb2 as sp


def default_func(uc, message):
    uc.logger.debug("=========没有这个协议")

def prot_rsp_new_login(uc, message):
    message = pbjson.pb2dict(message)
    uc.user_data = message['rsp_login']['home_user_data']
    uc.user_id = uc.user_data['base_info']['uin']
    uc.action_state = 1

def _update_source_change_info(uc, data):
    fields = ['mineral', 'energy', 'energy_charge_time', 'mineral_charge_time',
        'power_charge_time', 'score', 'crystal', 'alloy']
    for field in fields:
        uc.user_data['base_info'][field] = data[field]

    fields = ['mineral_recover', 'energy_recover', 'jump_power_recover', 'mineral_max',
        'energy_max', 'jump_power_max', 'mineral_speed_percent', 'energy_speed_percent',
        'energy_speed_percent', 'jump_power_speed_percent', 'upkeep', 'm_upkeep']
    for field in fields:
        uc.user_data['city_count'][field] = data[field]

def _update_progress_info(uc, data):
    data['end_time'] = int(time.time()) + data['totaltime'] + data['speedtime']
    uc.user_data['progress_info'] = data

def _update_building_info(uc, data):
    for building in uc.user_data['building_info']['building_list']:
        if data['inst'] == building['inst']:
            building.update(data)
            return
    uc.user_data['building_info']['building_list'].append(data)

#4. 建造
def prot_rsp_build(uc, message):
    message = pbjson.pb2dict(message)
    _update_source_change_info(uc, message['rsp_build']['source_change_info'])
    _update_progress_info(uc, message['rsp_build']['progress_info'])
    _update_building_info(uc, message['rsp_build']['building_info'])
    uc.user_data['base_info']['cash'] = message['rsp_build']['cash']
    uc.action_state = 1

#5. 升级
def prot_rsp_build_update(uc, message):
    message = pbjson.pb2dict(message)
    _update_source_change_info(uc, message['rsp_build_update']['source_change_info'])
    _update_progress_info(uc, message['rsp_build_update']['progress_info'])
    _update_building_info(uc, message['rsp_build_update']['building_info'])
    uc.user_data['base_info']['cash'] = message['rsp_build_update']['cash']
    uc.action_state = 1

#6. 建造取消
def prot_rsp_build_cancel(uc, message):
    pass
#7. 进度加速
def prot_rsp_progress_speed(uc, message):
    #更新进度条
    progress_inst = message.rsp_progress_speed.progress_info.progress_inst
    if uc.user_data['progress_info'].get('begin'):
        p_i_list = [uc.user_data['progress_info']]
    else:
        p_i_list = uc.user_data['progress_info'].get('progress_info', [])
    for p in p_i_list:
        if p.get('progress_inst') == progress_inst:
            p['end_time'] -= message.rsp_progress_speed.progress_info.speedtime
    #更新道具
    for item in uc.user_data['pack_info']['item_list']:
        if item['item_id'] == message.rsp_progress_speed.item_id:
            item['item_num'] = message.rsp_progress_speed.item_num
    uc.action_state = 1
#8.
def prot_rsp_building_stop(uc, message):
    pass
#9. 进度取消
def prot_rsp_progress_stop(uc, message):
    pass
#10. 编辑蓝图
def prot_rsp_save_ship_plan(uc, message):
    pass
#11. 增加蓝图
def prot_rsp_add_plan_num(uc, message):
    pass
#12. 删除蓝图
def prot_rsp_del_ship_plan(uc, message):
    pass
#13. 造船
def prot_rsp_training(uc, message):
    message = pbjson.pb2dict(message.rsp_training)
    _update_source_change_info(uc, message['source_change_info'])
    _update_progress_info(uc, message['progress_info'])
    uc.user_data['army_info']['training_info'] = message['training_info']
    uc.user_data['base_info']['cash'] = message['cash']
    uc.action_state = 1

#14. 解散舰队
def prot_rsp_soldier_dismiss(uc, message):
    pass
#15. 取消造船队列
def prot_rsp_cancel_training(uc, message):
    pass
#16. 刷新军校
def prot_rsp_refreash_hero(uc, message):
    pass
#17. 招募指挥官
def prot_rsp_recruit_hero(uc, message):
    pass
#18. 解散指挥官
def prot_rsp_delete_hero(uc, message):
    pass
#19. 地图部队信息变更
def prot_rsp_army_info(uc, message):
    uc.user_data['army_info'] = pbjson.pb2dict(message.rsp_army_info)
    uc.action_state = 1

#21. 创建联盟
def prot_rsp_create_union(uc, message):
    pass
#23. 通知有人申请加入
def prot_rsp_notice_join(uc, message):
    pass
#25. 通知邀请加入联盟
def prot_rsp_notice_invite(uc, message):
    pass
#27. 通知拒绝联盟邀请
def prot_rsp_notice_refuse_invite(uc, message):
    pass
#29. 通知拒绝加入联盟
def prot_rsp_notice_refuse_join(uc, message):
    pass
#31. 联盟成员变更通知
def prot_rsp_union_member_change(uc, message):
    pass
#32. 退出联盟
def prot_rsp_quit_union(uc, message):
    pass
#36. 更换联盟领袖
def prot_rsp_change_leader(uc, message):
    pass
#37. 开放联盟申请
def prot_rsp_open_union(uc, message):
    pass
#38. 改变联盟设置
def prot_rsp_notice_union_info_change(uc, message):
    pass
#39. 创建联盟军团
def prot_rsp_create_union_group(uc, message):
    pass
#40. 通知联盟资源变更
def prot_rsp_notice_union_source_change(uc, message):
    pass
#41. 联盟改名
def prot_rsp_change_union_name(uc, message):
    pass
#42. 通知联盟改名
def prot_rsp_notice_change_union_name(uc, message):
    pass
#43. 请求联盟帮助加速
def prot_rsp_union_speed_list_change(uc, message):
    pass
#44. 联盟加速
def prot_rsp_union_need_help(uc, message):
    pass
#47. 部队信息变更
def prot_rsp_army_info_change(uc, message):
    uc.action_state = 1

#48. 空间站信息变更
def prot_rsp_city_change(uc, message):
    uc.user_data['city_change'] = pbjson.pb2dict(message.ext_info.rsp_city_change)
    uc.action_state = 1

#49. 采矿及驻守部队变更
def prot_rsp_out_source_army_change(uc, message):
    pass
#51. 物品及代币变更
def prot_rsp_notice_cash_or_goods_update(uc, message):
    pass
#52. 新增联盟军团
def prot_rsp_add_union_group(uc, message):
    pass
#53. 退出联盟军团
def prot_rsp_exit_union_group(uc, message):
    pass
#55. 创建舰队
def prot_rsp_create_fleet(uc, message):
    uc.action_state = 1
#56. 删除舰队
def prot_rsp_delete_fleet(uc, message):
    pass
#57. 通知宣战信息
def prot_notice_union_fight(uc, message):
    pass

def prot_rsp_notice_fight(uc, message):
    pass
#58. 空间站传送
def prot_rsp_move(uc, message):
    uc.action_state = 1

#59. 维修
def prot_rsp_repair(uc, message):
    pass
#60. 探索结束
def prot_rsp_explore_finish(uc, message):
    pass
#61. 通知探索结束
def prot_notice_explore_info(uc, message):
    pass
#62. 部队加速
def prot_rsp_speed(uc, message):
    pass
#63. 邮件信息
def prot_rsp_get_mail_simple_info(uc, message):
    pass
#64. 邮件详情
def prot_rsp_get_mail_desc(uc, message):
    pass
#65. 删除邮件
def prot_rsp_del_mail(uc, message):
    pass
#66. 保存邮件
def prot_rsp_save_mail(uc, message):
    pass
#67. 发送邮件
def prot_rsp_send_mail(uc, message):
    pass
#68. 收藏邮件
def prot_rsp_mark_mail(uc, message):
    pass
#69. 通知有新邮件
def prot_rsp_notice_mail_change(uc, message):
    pass
#70. 使用道具
def prot_rsp_use_item(uc, message):
    pass

#71. 购买道具
def prot_rsp_buyitem(uc, message):
    bi = message.ext_info.rsp_buyitem
    uc.user_data['base_info']['cash'] = bi.cash
    item_info = {'item_id': bi.item_info.item_id, 'item_num': bi.item_info.item_num}
    item_list = uc.user_data['pack_info'].get('item_list')
    if not item_list:
        uc.user_data['pack_info']['item_list'] = [item_info]
        uc.action_state = 1
        return
    for item in item_list:
        if item['item_id'] == item_info['item_id']:
            item['item_num'] = item_info['item_num']
            uc.action_state = 1
            return
    item_list.append(item_info)
    uc.action_state = 1

#72. 释放英雄
def prot_rsp_prision_change(uc, message):
    pass
#74. 获取太阳系信息
def prot_rsp_map_info(uc, message):
    uc.user_data['map_info'] = pbjson.pb2dict(message.rsp_map_info)
    uc.action_state = 1

#75. 获取星云信息
def prot_rsp_cloud_map(uc, message):
    uc.user_data['cloud_map'] = pbjson.pb2dict(message.rsp_cloud_map)
    uc.action_state = 1

#76. 搜索玩家
def prot_rsp_search_user(uc, message):
    pass
#77. 搜索联盟
def prot_rsp_search_union(uc, message):
    pass
#78. 查找名字
def prot_rsp_check_name(uc, message):
    pass

def prot_rsp_heart(uc, message):
    pass

def prot_rsp_gm(uc, message):
    pass


#server返回的cmd和需要执行的方法 key是一个int型，value是一个方法名。
cmd_prot_rsp_method = {
    sp.RspNewLogin: prot_rsp_new_login,
    sp.RspBuild: prot_rsp_build,
	sp.RspBuildUpdate: prot_rsp_build_update,
	sp.RspBuildCancel: prot_rsp_build_cancel,
	sp.RspProgressSpeed: prot_rsp_progress_speed,
	sp.RspBuildingStop: prot_rsp_building_stop,
    sp.RspProgressStop: prot_rsp_progress_stop,
	sp.RspSaveShipPlan: prot_rsp_save_ship_plan,
	sp.RspAddPlanNum: prot_rsp_add_plan_num,
	sp.RspDelShipPlan: prot_rsp_del_ship_plan,
	sp.RspTraining: prot_rsp_training,
	sp.RspSoldierDismiss: prot_rsp_soldier_dismiss,
	sp.RspCancelTraining: prot_rsp_cancel_training,
	sp.RspRefreashHero: prot_rsp_refreash_hero,
	sp.RspRecruitHero: prot_rsp_recruit_hero,
	sp.RspDeleteHero: prot_rsp_delete_hero,
	sp.RspArmyInfo: prot_rsp_army_info,
	sp.RspCreateUnion: prot_rsp_create_union,
	sp.RspNoticeJoin: prot_rsp_notice_join,
	sp.RspNoticeInvite: prot_rsp_notice_invite,
	sp.RspNoticeRefuseInvite: prot_rsp_notice_refuse_invite,
	sp.RspNoticeRefuseJoin: prot_rsp_notice_refuse_join,
	sp.RspUnionMemberChange: prot_rsp_union_member_change,
	sp.RspQuitUnion: prot_rsp_quit_union,
	sp.RspChangeLeader: prot_rsp_change_leader,
	sp.RspOpenUnion: prot_rsp_open_union,
	sp.RspNoticeUnionInfoChange: prot_rsp_notice_union_info_change,
	sp.RspCreateUnionGroup: prot_rsp_create_union_group,
	sp.RspNoticeUnionSourceChange: prot_rsp_notice_union_source_change,
	sp.RspChangeUnionName: prot_rsp_change_union_name,
	sp.RspNoticeChangeUnionName: prot_rsp_notice_change_union_name,
	sp.RspUnionSpeedListChange: prot_rsp_union_speed_list_change,
	sp.RspUnionNeedHelp: prot_rsp_union_need_help,
	sp.RspArmyInfoChange: prot_rsp_army_info_change,
	sp.RspCityChange: prot_rsp_city_change,
	sp.RspOutSourceArmyChange: prot_rsp_out_source_army_change,
	sp.RspNoticeCashOrGoodsUpdate: prot_rsp_notice_cash_or_goods_update,
	sp.RspAddUnionGroup: prot_rsp_add_union_group,
	sp.RspExitUnionGroup: prot_rsp_exit_union_group,
	sp.RspCreateFleet: prot_rsp_create_fleet,
	sp.RspDeleteFleet: prot_rsp_delete_fleet,
	sp.NoticeUnionFight: prot_notice_union_fight,
	sp.RspNoticeFight: prot_rsp_notice_fight,
	sp.RspMove: prot_rsp_move,
	sp.RspRepair: prot_rsp_repair,
	sp.RspExploreFinish: prot_rsp_explore_finish,
	sp.NoticeExploreInfo: prot_notice_explore_info,
	sp.RspSpeed: prot_rsp_speed,
	sp.RspGetMailSimpleInfo: prot_rsp_get_mail_simple_info,
	sp.RspGetMailDesc: prot_rsp_get_mail_desc,
	sp.RspDelMail: prot_rsp_del_mail,
	sp.RspSaveMail: prot_rsp_save_mail,
	sp.RspSendMail: prot_rsp_send_mail,
	sp.RspMarkMail: prot_rsp_mark_mail,
	sp.RspNoticeMailChange: prot_rsp_notice_mail_change,
	sp.RspUseItem: prot_rsp_use_item,
	sp.RspBuyItem: prot_rsp_buyitem,
	sp.RspPrisonChange: prot_rsp_prision_change,
	sp.RspMapInfo: prot_rsp_map_info,
	sp.RspCloudMap: prot_rsp_cloud_map,
	sp.RspSearchUser: prot_rsp_search_user,
	sp.RspSearchUnion: prot_rsp_search_union,
	sp.RspCheckName: prot_rsp_check_name,
    sp.RspHeart: prot_rsp_heart,
    sp.RspGM: prot_rsp_gm,
}
