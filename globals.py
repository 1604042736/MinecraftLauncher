# -*- coding: utf-8 -*-
'''存放全局数据'''
import json
import logging
import datetime
import os

logfile = f'Logs\\{datetime.datetime.now().strftime("%Y-%m-%d-%H")}.log'
logformat = logging.Formatter(
    '[%(threadName)s=>%(funcName)s]:[%(asctime)s][%(levelname)s]:%(message)s', '%Y-%m-%d,%H:%M:%S')

logapi = logging.getLogger()  # 日志接口
logapi.setLevel(logging.DEBUG)

# 将日志打印到文件和控制台中
try:
    os.makedirs('Logs')
except:
    pass
fh = logging.FileHandler(logfile, mode='w', encoding='utf-8')
fh.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(logformat)
fh.setFormatter(logformat)

logapi.addHandler(ch)
logapi.addHandler(fh)

dmr = None  # 线程管理

# 配置
config = {  # 默认配置
    "cur_gamepath": ".minecraft",
    "all_gamepath": [
        ".minecraft"
    ],
    "player_name": "Player",
    "cur_version": "",
    "width": 1000,
    "height": 618,
    "maxmem": 1024,
    "minmem": 256,
    "javapath": "javaw"
}

try:
    for key, val in json.load(open('config.json', encoding='utf-8')).items():
        config[key] = val  # 保证默认配置中有配置文件中没有的内容
except:
    pass

if not os.path.exists(config['cur_gamepath']+'/versions/'+config['cur_version']):
    config['cur_version'] = ''
