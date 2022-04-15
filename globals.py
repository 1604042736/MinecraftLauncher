'''存放全局数据'''
import os
import json
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s][%(levelname)s]: %(message)s')

dmr = None  # 下载管理

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
    "javapath": "javaw",
    "theme": "light_lightgreen.xml"
}

try:
    for key, val in json.load(open('config.json', encoding='utf-8')).items():
        config[key] = val  # 保证默认配置中有配置文件中没有的内容
except:
    pass
