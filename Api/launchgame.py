# -*- coding: utf-8 -*-
import json
import os
import threading
import time
from zipfile import ZipFile
from Api.download import *
import globals as g
from Api.thread import Thread
import globals as g
import platform
import sys


class LaunchGame:
    '''
    启动游戏
    参考https://minecraft.fandom.com/zh/wiki/%E6%95%99%E7%A8%8B/%E7%BC%96%E5%86%99%E5%90%AF%E5%8A%A8%E5%99%A8?amp%3Bvariant=zh
    '''
    system_name = platform.system().lower()
    system_version = platform.version()

    maxbit = sys.maxsize
    if maxbit > 2**32:
        arch = 'x64'
    else:
        arch = 'x86'

    native_end = {  # 不同系统下native的后缀
        'windows': '.dll',
        'linux': '.so'
    }

    features = {
        "is_demo_user": False,
        "has_custom_resolution": True
    }

    def __init__(self, name, redownload=False) -> None:
        # 尽量使用绝对路径
        self.path = os.path.abspath(os.path.join(os.path.join(
            g.config['cur_gamepath'], 'versions'), name))  # 游戏路径
        self.lib_path = os.path.abspath(os.path.join(
            g.config['cur_gamepath'], 'libraries'))
        self.native_path = os.path.join(self.path, f'{name}-natives')
        self.asset_path = os.path.abspath(
            os.path.join(g.config['cur_gamepath'], 'assets'))
        self.config = json.load(
            open(os.path.join(self.path, f'{name}.json')))  # json文件

        self.name = name
        self.classpath = []  # -cp后的参数
        self.cp_memory = {}  # classpath记忆
        self.redownload = redownload  # 是否是重新下载

        self.total = 0  # 总任务
        self.cur = 0  # 当前任务进度

    def launch(self, javapath='javaw',
               playername='Player',
               width=1000,
               height=618,
               maxmem=1024,
               minmem=256):
        '''启动'''
        thread_count = threading.active_count()+1
        for _ in self.analysis_libraries():
            pass
        for _ in self.analysis_assets():
            pass

        while threading.active_count() > thread_count:  # 等待所有任务完成
            yield int(self.cur/self.total*100)
            time.sleep(1)  # 防止界面卡死
            g.logapi.debug(f'剩余线程: {threading.active_count()}({thread_count})')
            g.logapi.debug(f'当前进度: {self.cur}/{self.total}')
        g.logapi.debug(f'剩余线程: {threading.active_count()}({thread_count})')

        self.classpath.append(os.path.join(self.path, f'{self.name}.jar'))

        # jvm参数必须放在游戏参数前!!!
        args = f'cd "{os.path.abspath(g.config["cur_gamepath"])}" & start {javapath} '
        args += f'-XX:+UseG1GC '
        args += f'-XX:-UseAdaptiveSizePolicy '
        args += f'-XX:-OmitStackTraceInFastThrow '
        args += f'-Dfml.ignoreInvalidMinecraftCertificates=True -Dfml.ignorePatchDiscrepancies=True -Dlog4j2.formatMsgNoLookups=true '

        if self.system_name == 'windows':  # 专门处理
            args += f'-Dos.name="Windows 10" '
            args += f'-Dos.version=10.0 '

        for i in self.config['arguments']['jvm']:
            if isinstance(i, str):
                args += i+' '
            elif isinstance(i, dict):
                if 'rules' in i:
                    if self.check_rule(i['rules']):
                        if isinstance(i['value'], str):
                            args += i['value']+' '

        args += f'-Xmn{minmem}m '
        args += f'-Xmx{maxmem}m '
        args += f'{self.config["mainClass"]} '

        for i in self.config['arguments']['game']:
            if isinstance(i, str):
                args += i+' '
            elif isinstance(i, dict):
                if 'rules' in i:
                    if self.check_rule(i['rules']):
                        if isinstance(i['value'], str):
                            args += i['value']+' '
                        else:
                            args += ' '.join(i['value'])+' '

        args = args.replace('${auth_player_name}', playername)
        args = args.replace('${version_name}', self.config["id"])
        args = args.replace('${game_directory}',
                            f'"{os.path.abspath(g.config["cur_gamepath"])}"')
        args = args.replace('${assets_root}', f'"{self.asset_path}"')
        args = args.replace('${assets_index_name}',
                            self.config["assetIndex"]["id"])
        args = args.replace('${auth_uuid}', '000000000000300C95C489********86')
        args = args.replace('${auth_access_token}',
                            '000000000000300C95C489********86')
        args = args.replace('${user_type}', 'Legacy')
        args = args.replace('${version_type}', 'MinecraftLaucnher')
        args = args.replace('${resolution_width}', str(width))
        args = args.replace('${resolution_height}', str(height))
        args = args.replace('${natives_directory}', f'"{self.native_path}"')
        args = args.replace('${launcher_name}', 'MinecraftLauncher')
        args = args.replace('${launcher_version}', '1')
        args = args.replace('${classpath}', f'"{";".join(self.classpath)}"')

        args = args.replace('/', '\\')
        g.logapi.info(args)
        os.system(args)
        g.logapi.info('完成启动')

    def analysis_assets(self, sep=False):
        '''解析所有asset'''
        g.logapi.info(f'解析asset')
        url = self.config['assetIndex']['url']
        name = self.config['assetIndex']['id']+'.json'
        indexes_path = os.path.join(self.asset_path, 'indexes')
        # assets/indexes/{版本名}.json
        indexes_file = os.path.join(indexes_path, name)
        Download.check_download(indexes_file, url, self.redownload)
        indexes = json.load(open(indexes_file))
        l = len(indexes['objects'])
        self.total += l
        thread_count = threading.active_count()
        for _, val in indexes['objects'].items():
            self.analysis_asset(val)

        if sep:  # 独立调用
            while threading.active_count() > thread_count:  # 等待所有任务完成
                yield int(self.cur/self.total*100)
                time.sleep(1)  # 防止界面卡死
                g.logapi.debug(
                    f'剩余线程: {threading.active_count()}({thread_count})')
                g.logapi.debug(f'当前进度: {self.cur}/{self.total}')

    @Thread.func_thread
    def analysis_asset(self, val):
        '''解析asset'''
        time.sleep(0.5)
        try:
            objects_path = os.path.join(self.asset_path, 'objects')
            hash = val['hash']
            object_url = f'http://resources.download.minecraft.net/{hash[:2]}/{hash}'
            object_path = os.path.join(objects_path, f'{hash[:2]}/{hash}')
            Download.check_download(object_path, object_url, self.redownload)
        except Exception as e:
            g.logapi.error(e)
        self.cur += 1  # 任务完成

    def analysis_libraries(self, sep=False):
        '''解析json文件中的所有library'''
        g.logapi.info('解析libraries')
        l = len(self.config['libraries'])
        self.total += l
        thread_count = threading.active_count()
        for _, lib in enumerate(self.config['libraries']):
            self.analysis_library(lib)

        if sep:  # 独立调用
            while threading.active_count() > thread_count:  # 等待所有任务完成
                yield int(self.cur/self.total*100)
                time.sleep(1)  # 防止界面卡死
                g.logapi.debug(
                    f'剩余线程: {threading.active_count()}({thread_count})')
                g.logapi.debug(f'当前进度: {self.cur}/{self.total}')

    @Thread.func_thread
    def analysis_library(self, lib):
        '''解析json文件中的library'''
        time.sleep(0.5)
        g.logapi.debug(f'解析{lib["name"]}')
        try:
            if 'classifiers' in lib['downloads']:  # 有classifiers的为natives库
                try:
                    native_name = lib['natives'][self.system_name]
                    path = os.path.join(
                        self.lib_path, lib['downloads']['classifiers'][native_name]['path'])
                    url = lib['downloads']['classifiers'][native_name]['url']
                    Download.check_download(path, url, self.redownload)
                    if 'rules' in lib and not self.check_rule(lib['rules']):
                        return
                    self.unzip_native(path)
                except KeyError as e:
                    g.logapi.error(e)
            else:
                if 'rules' in lib and not self.check_rule(lib['rules']):
                    return
                path = os.path.join(
                    self.lib_path, lib['downloads']['artifact']['path'])
                url = lib['downloads']['artifact']['url']
                Download.check_download(path, url, self.redownload)
                self.add_classpath(path)
        except Exception as e:
            g.logapi.error(e)

        self.cur += 1  # 任务完成

    def classpath_thread(self, path, url):
        Download.check_download(path, url, self.redownload)
        self.add_classpath(path)

    def native_thread(self, path, url):
        Download.check_download(path, url, self.redownload)
        self.unzip_native(path)

    def add_classpath(self, path):
        '''添加classpath'''
        path = path.replace('/', '\\')
        file = path.split('\\')[-1]
        # a-b-c.d.e.jar
        # a-b为name
        # c.d.e为version
        t = file.split('-')
        if len(t) > 2:
            name = '-'.join(file.split('-')[:2])
        else:
            name = '-'.join(file.split('-')[:1])
        version = '.'.join(file.split('-')[-1].split('.')[:-1])
        g.logapi.debug(f'{path},{version}')
        # 选择没有出现过的或者最新的版本
        if name not in self.cp_memory or self.compare_cp_version(version, self.cp_memory[name][0]):
            if name in self.cp_memory:  # 原先有的
                self.classpath.remove(self.cp_memory[name][1])
            self.classpath.append(path)
            self.cp_memory[name] = (version, path)

    def compare_cp_version(self, a, b):
        '''比较classpath的版本'''
        # 拆分开来
        va = map(int, a.split('.'))
        vb = map(int, b.split('.'))
        for i, j in zip(va, vb):
            if i > j:
                return True
        return False

    def unzip_native(self, path):
        '''解压native'''
        g.logapi.info(f'解压"{path}"')
        zip = ZipFile(path)
        for name in zip.namelist():
            if name.endswith(self.native_end[self.system_name]):
                zip.extract(name, self.native_path)

    def check_rule(self, rules):
        '''检查rule,返回结果'''
        result = False  # 结果

        for rule in rules:
            if 'os' in rule:
                # 只要匹配上了就可以退出
                if 'name' in rule['os'] and rule['os']['name'] == self.system_name:
                    result = self.check_action(rule['action'])
                    break
                elif 'arch' in rule['os'] and rule['os']['arch'] == self.arch:
                    result = self.check_action(rule['action'])
                    break
            elif 'features' in rule:
                # 只要匹配上了就可以退出
                for key, val in rule['features'].items():
                    if self.features[key] != val:
                        result = False
                        break
                else:
                    result = self.check_action(rule['action'])
                    break
            else:  # 只有一个action的rule不能当成最终结果
                result = self.check_action(rule['action'])

        return result

    def check_action(self, action):
        '''检查行动'''
        return action == 'allow'
