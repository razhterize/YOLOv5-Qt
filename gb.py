# coding=utf-8
import datetime
import json
import logging
import os
import sys
import threading

import msg_box

CONFIG = dict()
YOLOGGER = logging.getLogger()


def thread_runner(func):
    """Multithreading"""
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=args, kwargs=kwargs).start()
    return wrapper


def clean_log():
    YOLOGGER.info('Start cleaning the log file')
    if os.path.exists('log'):
        file_list = os.listdir('log')
        today = datetime.date.today()
        for file in file_list:
            date = file.split('.')[0].split('-')
            log_date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
            interval = today - log_date
            if abs(interval.days) > 30:
                path = 'log/' + file
                os.remove(path)
                YOLOGGER.info(f'Delete the expiration log: {path}')


def init_logger():
    if not os.path.exists('log'):
        os.mkdir('log')
    YOLOGGER.setLevel(logging.DEBUG)

    formatter = logging.Formatter(fmt='[%(asctime)s] [%(thread)d] %(message)s')

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    YOLOGGER.addHandler(stream_handler)

    file_handler = logging.FileHandler(filename=f'log/{datetime.date.today().isoformat()}.log')
    file_handler.setFormatter(formatter)
    YOLOGGER.addHandler(file_handler)


def init_config():
    global CONFIG
    if not os.path.exists('config'):
        os.mkdir('config')  # make new config folder
        return
    try:
        with open('config/config.json', 'r') as file_settings:
            CONFIG = json.loads(file_settings.read())
    except FileNotFoundError as err_file:
        YOLOGGER.error('Configuration file does not exist: ' + str(err_file))


def record_config(_dict):
    """Write setting parameter to a local config file"""
    global CONFIG
    # Update configuration
    for k, v in _dict.items():
        CONFIG[k] = v
    if not os.path.exists('config'):
        os.mkdir('config')  # Create a Config folder
    try:
        # Write file
        with open('config/config.json', 'w') as file_config:
            file_config.write(json.dumps(CONFIG, indent=4))
    except FileNotFoundError as err_file:
        YOLOGGER.error(err_file)
        msg = msg_box.MsgWarning()
        msg.setText('Parameter preservation failed！')
        msg.exec()


def get_config(key, _default=None):
    global CONFIG
    return CONFIG.get(key, _default)
