# -*- coding = None utf-8 -*-
import xml.dom.minidom
import os
xml_path = os.path.split(os.path.realpath(__file__))[0] + "/config_xml/"

class ConfigModel(object):
    pass

def _set_data(obj, item, name, _type="int", sep='|'):
    data = None
    try:
        data = item.getElementsByTagName(name)[0].firstChild.data
    except:
        setattr(obj, name, data)
        return

    if _type == 'int':
        data = int(data)
    elif _type == 'list_int':
        data = [int(i) for i in data.split(sep)]

    setattr(obj, name, data)

def get_config_build():
    dom = xml.dom.minidom.parse(xml_path + "build_s.xml")
    config_model_dict = {}
    for item in dom.documentElement.getElementsByTagName('Build'):
        obj = ConfigModel()
        _set_data(obj, item, 'build_id')
        _set_data(obj, item, 'build_resid')
        #_set_data(obj, item, 'build_name', 'list_str', ',')
        _set_data(obj, item, 'build_classid')
        _set_data(obj, item, 'build_classname', 'str')
        _set_data(obj, item, 'build_level')
        _set_data(obj, item, 'build_maxlevel')
        _set_data(obj, item, 'build_nextlevel')
        _set_data(obj, item, 'build_prebuild', 'list_int')
        _set_data(obj, item, 'build_buildtime')
        _set_data(obj, item, 'build_allbuildtime')
        _set_data(obj, item, 'build_buildcost', 'list_int')
        _set_data(obj, item, 'build_allbuildcost', 'list_int')
        _set_data(obj, item, 'build_upkeep', 'list_int')
        _set_data(obj, item, 'build_unbuild')
        _set_data(obj, item, 'build_desc', 'str')
        _set_data(obj, item, 'build_buff')
        _set_data(obj, item, 'build_param0')
        _set_data(obj, item, 'build_param1')
        _set_data(obj, item, 'build_minss', 'list_int', ',')
        _set_data(obj, item, 'build_maxss', 'list_int', ',')
        _set_data(obj, item, 'build_power')
        config_model_dict[obj.build_id] = obj
    return config_model_dict

def get_config_space_station():
    dom = xml.dom.minidom.parse(xml_path + "spacestation_s.xml")
    config_model_dict = {}
    names = [
        "ss_id",
        "ss_fleets",
        "ss_engships",
        "ss_estation",
        "ss_tstation",
        "ss_shipyard",
        "ss_dcenter",
        "ss_rcenter",
        "ss_defense",
        "ss_school",
        "ss_fleetsp",
        "ss_engshipsp",
        "ss_estationp",
        "ss_tstationp",
        "ss_shipyardp",
        "ss_dcenterp",
        "ss_rcenterp",
        "ss_defensep",
        "ss_schoolp",
        "ss_slots",
        "ss_slotsp",
        "ss_slotsall",
        "ss_helpcounts",
        "ss_helpcountsp",
        "ss_outpost",
        "ss_outpostp",
        "ss_hp",
        "ss_hpp",
        "ss_hpr",
        "ss_hprp",
        "ss_sp",
        "ss_spp",
        "ss_ac",
        "ss_acp",
        "ss_spr",
        "ss_sprp",
        "ss_prison",
        "ss_prisonp",
        "ss_radar",
        "ss_radarp"
    ]
    for item in dom.documentElement.getElementsByTagName('SpaceStation'):
        obj = ConfigModel()
        [_set_data(obj, item, name) for name in names]
        config_model_dict[obj.ss_id] = obj
    return config_model_dict

def get_config_items():
    dom = xml.dom.minidom.parse(xml_path + "items_s.xml")
    config_model_dict = {}
    for item in dom.documentElement.getElementsByTagName('ItemsData'):
        obj = ConfigModel()
        _set_data(obj, item, 'item_id')
        _set_data(obj, item, 'item_name', 'str')
        _set_data(obj, item, 'item_icon')
        _set_data(obj, item, 'item_func')
        _set_data(obj, item, 'item_functofunc')
        _set_data(obj, item, 'item_funcparam')
        _set_data(obj, item, 'item_param1')
        _set_data(obj, item, 'item_duration')
        _set_data(obj, item, 'item_desc', 'str')
        _set_data(obj, item, 'item_show', 'str')
        _set_data(obj, item, 'item_class')
        _set_data(obj, item, 'item_uselevel')
        _set_data(obj, item, 'item_inventoryuse')
        _set_data(obj, item, 'item_isgoods')
        _set_data(obj, item, 'item_price')
        _set_data(obj, item, 'item_isugoods')
        _set_data(obj, item, 'item_uprice')
        _set_data(obj, item, 'item_reputation')
        _set_data(obj, item, 'item_type')
        config_model_dict[obj.item_id] = obj
    return config_model_dict

def get_config_ship():
    dom = xml.dom.minidom.parse(xml_path + "ship_s.xml")
    config_model_dict = {}
    names = [
        'ship_id',
        'ship_resid',
        'ship_rank',
        'ship_type',
        'ship_cp',
        'ship_mod1',
        'ship_mod2',
        'ship_mod3',
        'ship_mod4'
    ]
    for item in dom.documentElement.getElementsByTagName('Ship'):
        obj = ConfigModel()
        [_set_data(obj, item, name) for name in names]
        _set_data(obj, item, 'ship_name', 'str')
        _set_data(obj, item, 'ship_cslots', 'list_int', ',')
        _set_data(obj, item, 'ship_buff', 'list_int', ',')
        config_model_dict[obj.ship_id] = obj
    return config_model_dict

def get_config_shipyard():
    dom = xml.dom.minidom.parse(xml_path + "shipyard_s.xml")
    config_model_dict = {}
    names = [
        'shipyard_id',
        'shipyard_speed',
        'shipyard_index',
        'shipyard_speedp',
        'shipyard_indexp'
    ]
    for item in dom.documentElement.getElementsByTagName('Shipyard'):
        obj = ConfigModel()
        [_set_data(obj, item, name) for name in names]
        _set_data(obj, item, 'shipyard_shiptype', 'list_int', ',')
        config_model_dict[obj.shipyard_id] = obj
    return config_model_dict

def get_config_135():
    dom = xml.dom.minidom.parse(xml_path + "135_s.xml")
    config_model_dict = {}
    for item in dom.documentElement.getElementsByTagName('StarNode'):
        obj = ConfigModel()
        _set_data(obj, item, 'sysName', 'str')
        _set_data(obj, item, 'inst')
        _set_data(obj, item, 'nodeList', 'list_int')
        _set_data(obj, item, 'len', 'list_str')
        _set_data(obj, item, 'pos', 'list_str')
        config_model_dict[obj.sysName] = obj
    return config_model_dict

def get_config_power_station():
    dom = xml.dom.minidom.parse(xml_path + "powerstation_s.xml")
    config_model_dict = {}
    names = [
        'ps_id',
        'ps_eregain',
        'ps_maxe',
        'ps_eregainp',
        'ps_maxep',
    ]
    for item in dom.documentElement.getElementsByTagName('PowerStation'):
        obj = ConfigModel()
        [_set_data(obj, item, name) for name in names]
        config_model_dict[obj.ps_id] = obj
    return config_model_dict

def get_config_space_build():
    dom = xml.dom.minidom.parse(xml_path + "spacebuild_s.xml")
    config_model_dict = {}
    names = [
        'sb_id',
        'sb_resid',
        'sb_nextbuild',
        'sb_prebuild',
        'sb_needres',
        'sb_repairres',
        'sb_rank',
        'sb_maxrank',
        'sb_hp',
        'sb_type',
        'sb_isunionbuild',
        'sb_workshipcount',
        'sb_mainspeed',
        'sb_subspeed',
        'sb_repairspeed',
        'sb_coverrange',
        'sb_influence',
        'sb_onstar',
        'sb_needrank',
        'sb_gathermin',
        'sb_ac',
        'sb_shield',
        'sb_sr',
        'sb_attackrange',
        'sb_traprange',
        #'sb_wp',
        'sb_battlepoint'
    ]
    for item in dom.documentElement.getElementsByTagName('SpaceBuild'):
        obj = ConfigModel()
        [_set_data(obj, item, name) for name in names]
        _set_data(obj, item, 'sb_name', 'list_str', ',')
        _set_data(obj, item, 'sb_classname', 'str')
        _set_data(obj, item, 'sb_desc', 'str')
        config_model_dict[obj.sb_id] = obj
    return config_model_dict

def get_config_trade_station():
    dom = xml.dom.minidom.parse(xml_path + "tradestation_s.xml")
    config_model_dict = {}
    names = [
        'ts_id',
        'ts_mregain',
        'ts_maxm',
        'ts_mregainp',
        'ts_maxmp',
    ]
    for item in dom.documentElement.getElementsByTagName('TradeStation'):
        obj = ConfigModel()
        [_set_data(obj, item, name) for name in names]
        config_model_dict[obj.ts_id] = obj
    return config_model_dict

config_build = get_config_build()
config_space_station = get_config_space_station()
config_items = get_config_items()
config_ship = get_config_ship()
config_shipyard = get_config_shipyard()
config_135 = get_config_135()
config_power_station = get_config_power_station()
config_space_build = get_config_space_build()
config_trade_station = get_config_trade_station()
