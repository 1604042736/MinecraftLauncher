import globals as g
import os
from Api.thread import *
import time
from zipfile import ZIP_DEFLATED, ZipFile
import globals as g
import requests
import json
from Api.download import *
import shutil


class Game:
    '''与游戏有关的操作'''
    class_path = {}  # class所对的路径

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

        config = {  # 游戏配置信息
            "name": name,
            "version": version,
            "forge_version": forge_version
        }
        json.dump(config, open(f'{game_path}\\config.json', mode='w'))

        if forge_version:
            Game.install_forge(name, version, forge_version)

    @staticmethod
    def install_forge(name, version, forge_version, thread_shift=0):
        '''安装forge'''
        Game.class_path = {}

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

        thread_count = threading.active_count()+thread_shift

        for i in install_profile['libraries']:
            Game.analysis_library(zip, i)
        for i in forge_config['libraries']:
            Game.analysis_library(zip, i)

        while threading.active_count() > thread_count:
            g.logapi.debug(f'剩余线程{threading.active_count()}({thread_count})')
            time.sleep(1)
        g.logapi.debug(f'剩余线程{threading.active_count()}({thread_count})')

        lib_path = os.path.join(g.config['cur_gamepath'], f'libraries')
        # forge-client
        '''
        userdev_path = game_path+f'\\userdev.jar'
        client_path = os.path.join(
            lib_path, f'net/minecraftforge/forge/{version}-{forge_version}/forge-{version}-{forge_version}-client.jar')
        # 获取需要的文件
        file_subset_list = []

        with ZipFile(userdev_path) as userdev:
            for i in userdev.namelist():
                if 'patches' in i and '.' in i:
                    file_subset_list.append(i)
        Game.stream_conents(userdev_path, client_path, file_subset_list,
                            lambda path: '/'.join(path.split('/')[1:]))'''

        # client
        client_mapping = Game.get_client(install_profile, 'MAPPINGS', lib_path)
        client_binpatch = Game.get_client(
            install_profile, 'BINPATCH', lib_path)

        client_extra = Game.get_special_client(
            install_profile, 'MC_EXTRA', lib_path)+'.jar'
        client_slim = Game.get_special_client(
            install_profile, 'MC_SLIM', lib_path)+'.jar'
        client_srg = Game.get_special_client(
            install_profile, 'MC_SRG', lib_path)+'.jar'
        client_patched = Game.get_special_client(
            install_profile, 'PATCHED', lib_path)+'.jar'

        zip.extract(client_binpatch[1:], game_path)
        client_binpatch = os.path.abspath(game_path+f'{client_binpatch}')

        for i in install_profile['processors']:
            Game.execute(i,
                         lib_path,
                         game_path + f'\\{name}.jar',
                         client_extra,
                         client_slim,
                         client_srg,
                         client_patched,
                         client_binpatch,
                         client_mapping
                         )

        zip.close()
        # 拼接
        Game.splicing(config, forge_config)
        json.dump(config, open(os.path.join(
            game_path, f'{name}.json'), mode='w'))

    @staticmethod
    def get_special_client(install_profile, key, lib_path):
        '''获取特殊的client'''
        val = install_profile["data"][key]["client"]
        a = val[1:-1]
        b, c = a.split(':', 1)
        d = b.replace('.', '/')
        e = '/'.join(c.split(':')[:-1])
        f = c.replace(':', '-').replace('@', '.')
        return os.path.abspath(os.path.join(lib_path, d+'/'+e+'/'+f))

    @staticmethod
    def get_client(install_profile, key, lib_path):
        '''获取install_profile["data"][key]["client"]'''
        val = install_profile["data"][key]["client"]
        if val[0] == '[':
            return os.path.abspath(os.path.join(lib_path, Game.turn_to_path(val)))
        else:
            return val

    @staticmethod
    def turn_to_path(name):
        '''转换成path'''
        a = name[1:-1]
        b, c = a.split(':', 1)
        d = b.replace('.', '/')
        e = c.replace(':', '-').replace('@', '.')
        return d+'/'+e

    @staticmethod
    def execute(processor, lib_path, minecraft, extra, slim, srg, patched, binpatch, mapping):
        '''执行'''
        g.logapi.info(f'执行{processor["jar"]}')
        args = ''

        args += '-cp '

        classpath = []
        for i in processor['classpath']:
            classpath.append(os.path.abspath(Game.class_path[i]))
        classpath.append(os.path.abspath(Game.class_path[processor["jar"]]))

        args += '"'+';'.join(classpath)+'" '

        mainclass = ''
        jar = processor['jar']
        if 'installertools' in jar:
            mainclass = 'net.minecraftforge.installertools.ConsoleTool'
        elif 'jarsplitter' in jar:
            mainclass = 'net.minecraftforge.jarsplitter.ConsoleTool'
        elif 'md-5' in jar:
            mainclass = ' net.md_5.specialsource.SpecialSource'
        elif 'binarypatcher' in jar:
            mainclass = 'net.minecraftforge.binarypatcher.ConsoleTool'
        args += mainclass

        for i in processor['args']:
            if i[0] == '[':
                i = os.path.abspath(Game.class_path[i[1:-1]])
            args += ' '+i

        args = args.replace('{MINECRAFT_JAR}', minecraft)
        args = args.replace('{MC_SLIM}', slim)
        args = args.replace('{MC_EXTRA}', extra)
        args = args.replace('{MC_SRG}', srg)
        args = args.replace('{PATCHED}', patched)
        args = args.replace('{BINPATCH}', binpatch)
        args = args.replace('{MAPPINGS}', mapping)

        order = f'java {args}'
        g.logapi.debug(order)
        os.system(order)

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
    @Thread.func_thread
    def analysis_library(forge_zip, lib):
        '''解析lib'''
        time.sleep(0.5)
        g.logapi.debug(f'解析{lib["name"]}')
        lib_path = os.path.join(g.config['cur_gamepath'], f'libraries')
        path = os.path.join(lib_path, lib['downloads']['artifact']['path'])
        url = lib['downloads']['artifact']['url']
        Game.class_path[lib["name"]] = path
        if url:  # 下载
            Download.check_download(path, url)
        else:  # 解压
            path = lib['downloads']['artifact']['path']
            jarpath = 'maven/'+path
            newpath = f'{lib_path}/{path}'
            try:
                os.makedirs(os.path.dirname(newpath))
            except:
                pass
            g.logapi.debug(f'将{jarpath}移动到{newpath}')
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
