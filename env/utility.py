def get_path(name):
    import os
    directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, name))
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def get_data_path():
    """
    Get data folder path.
    :return: path to data folder
    """
    return get_path('data')


def get_log_path():
    """
    Get data folder path.
    :return: path to data folder
    """
    return get_path('log')


def read_test_client_state():
    """
    Read state.pkl in data folder.
    :return: user data dictionary
    """
    import json
    with open(get_data_path() + '/' + 'state.json', 'r+') as f:
        usr_data = json.load(f)
    return usr_data


def n2sn(n):
    """
    Convert number to scientific notation.
    :param n: number
    :return: two float number, a and b, n = a * 10 ** b.
    """
    sn = '%e' % n
    a, b = [float(i) for i in sn.split('e')]
    if a > 1:
        a /= 10
        b += 1
    b /= 20
    return a, b


def init_logger(name):
    import logging
    import logging.handlers
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = 0
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)8s - %(message)s')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(console)

    rf = logging.handlers.RotatingFileHandler(get_log_path() + '/' + name +
                                              '.log', maxBytes=10 * 1024 * 1024,
                                              backupCount=5)
    rf.setLevel(logging.DEBUG)
    rf.setFormatter(formatter)
    logger.addHandler(rf)
    return logger


def read_config(file_name='config.json'):
    """
    Read configuration from json file
    :param file_name: config file name
    :return: config object
    """
    import os, json
    config_fp = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'config'))
    with open(config_fp + '/' + file_name) as f:
        config = json.load(f)
    return config


def read_build_cost(build_id):
    """
    Read all build cost from xml
    :param build_id: building id
    :type build_id: int
    :return: all build cost
    :rtype: list
    """
    import env.malaclient.mlxk.config as c
    return c.config_build[build_id].build_allbuildcost


def generate_user_name():
    """
    Generate user name by date time
    :return: user name
    :rtype: str
    """
    import datetime
    return "tc_%s" % datetime.datetime.now().strftime('%Y%m%d%H%M%S')
