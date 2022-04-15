import logging
import os
from zipfile import ZIP_DEFLATED, ZipFile
import globals as g
import requests
import json
from Api.download import *
import shutil


class Game:
    '''与游戏有关的操作'''
    @staticmethod
    def get_versions() -> list:
        '''获取游戏版本'''
        url = 'http://launchermeta.mojang.com/mc/game/version_manifest.json'
        r = requests.get(url)
        versions = []
        for version in json.loads(r.content)['versions']:
            versions.append(version['id'])
        return versions

    @staticmethod
    def get_forge(version) -> list:
        '''获取forge版本'''
        url = f'https://bmclapi2.bangbang93.com/forge/minecraft/{version}'
        r = requests.get(url)
        forges = []
        for forge in json.loads(r.content):
            forges.append(forge['version'])
        return forges

    @staticmethod
    def get_optifine(version) -> list:
        '''获取optifine版本'''
        url = f'https://bmclapi2.bangbang93.com/optifine/{version}'
        r = requests.get(url)
        optifines = []
        for optifine in json.loads(r.content):
            optifines.append(
                optifine['mcversion'] + ' ' + optifine['type'] + ' ' + optifine['patch'])
        return optifines

    @staticmethod
    def get_liteloader(version) -> list:
        '''获取liteloader版本'''
        url = f'https://bmclapi2.bangbang93.com/liteloader/list?mcversion={version}'
        r = requests.get(url)
        liteloaders = []
        try:
            liteloaders.append(json.loads(r.content)[
                               'mcversion'] + ' ' + json.loads(r.content)['version'])
        except:
            pass
        return liteloaders

    @staticmethod
    def download_version(name, version,
                         forge_version=""):
        '''下载版本'''
        version_path = os.path.join(g.config['cur_gamepath'], 'versions')
        game_path = os.path.join(version_path, name)
        downloads = [[f'https://bmclapi2.bangbang93.com/version/{version}/client', game_path + f'\\{name}.jar'],
                     [f'https://bmclapi2.bangbang93.com/version/{version}/json', game_path + f'\\{name}.json']]
        if forge_version:  # 附带forge
            downloads.append(
                [f'https://bmclapi2.bangbang93.com/maven/net/minecraftforge/forge/{version}-{forge_version}/forge-{version}-{forge_version}-installer.jar', game_path+f'\\installer.jar'])
            downloads.append(
                [f'https://bmclapi2.bangbang93.com/maven/net/minecraftforge/forge/{version}-{forge_version}/forge-{version}-{forge_version}-userdev.jar', game_path+f'\\userdev.jar'])
        for task in downloads:
            for i in Download.download(task[0], task[1]):
                yield i
        if forge_version:
            Game.install_forge(name, version, forge_version)

        config = {  # 游戏配置信息
            "name": name,
            "version": version,
            "forge_version": forge_version
        }
        json.dump(config, open(f'{game_path}\\config.json', mode='w'))

    @staticmethod
    def install_forge(name, version, forge_version):
        '''安装forge'''
        version_path = os.path.join(g.config['cur_gamepath'], 'versions')
        game_path = os.path.join(version_path, name)
        config = json.load(open(os.path.join(game_path, f'{name}.json')))

        installerpath = game_path+f'\\installer.jar'
        # 获取forge的配置
        zip = ZipFile(installerpath)
        zip.extract('version.json', game_path)
        zip.extract('install_profile.json', game_path)
        forge_config = json.load(
            open(os.path.join(game_path, f'version.json')))

        install_profile = json.load(
            open(os.path.join(game_path, f'install_profile.json')))
        for i in install_profile['libraries']:
            Game.analysis_library(zip, i)
        zip.close()

        # forge-client
        lib_path = os.path.join(g.config['cur_gamepath'], f'libraries')
        userdev_path = game_path+f'\\userdev.jar'
        client_path = os.path.join(
            lib_path, f'net/minecraftforge/forge/{version}-{forge_version}/forge-{version}-{forge_version}-client.jar')
        # 获取需要的文件
        file_subset_list = []
        with ZipFile(userdev_path)as userdev:
            for i in userdev.namelist():
                if 'patches' in i and '.' in i:
                    file_subset_list.append(i)
        Game.stream_conents(userdev_path, client_path, file_subset_list,
                            lambda path: '/'.join(path.split('/')[1:]))

        # 拼接
        Game.splicing(config, forge_config)
        json.dump(config, open(os.path.join(
            game_path, f'{name}.json'), mode='w'))

    @ staticmethod
    def splicing(a, b):
        '''拼接a和b'''
        if isinstance(a, list) and isinstance(b, list):
            for i in b:
                if i not in a:
                    a.append(i)
            return
        for key, val in b.items():
            if key not in a:  # a原来没有key
                a[key] = val
            elif isinstance(a[key], str):
                a[key] = val
            else:
                Game.splicing(a[key], b[key])  # 继续拼接

    @staticmethod
    def analysis_library(forge_zip, lib):
        '''解析lib'''
        lib_path = os.path.join(g.config['cur_gamepath'], f'libraries')
        path = os.path.join(lib_path, lib['downloads']['artifact']['path'])
        url = lib['downloads']['artifact']['url']
        if url:  # 下载
            Download.check_download(path, url)
        else:  # 解压
            path = lib['downloads']['artifact']['path']
            jarpath = 'maven/'+path
            newpath = f'{lib_path}/{path}'
            logging.debug(jarpath)
            logging.debug(newpath)
            forge_zip.extract(jarpath, lib_path)
            shutil.move(f'{lib_path}/{jarpath}', newpath)

    @staticmethod
    def stream_conents(src_zip, dst_zip, file_subset_list, to_path=None):
        '''将压缩文件里的文件提取到另一个压缩文件中'''
        with ZipFile(src_zip, "r", compression=ZIP_DEFLATED) as src_zip_archive:
            with ZipFile(dst_zip, "w", compression=ZIP_DEFLATED) as dst_zip_archive:
                for zitem in src_zip_archive.namelist():
                    if zitem in file_subset_list:
                        with src_zip_archive.open(zitem) as from_item:
                            path = zitem
                            if to_path:  # 进行别的处理
                                path = to_path(zitem)
                            with dst_zip_archive.open(path, "w") as to_item:
                                shutil.copyfileobj(from_item, to_item)

    @staticmethod
    def del_game(name):
        '''删除游戏'''
        version_path = os.path.join(g.config['cur_gamepath'], 'versions')
        game_path = os.path.join(version_path, name)
        shutil.rmtree(game_path)