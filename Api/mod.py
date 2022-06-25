import re
from bs4 import BeautifulSoup, element
import requests
from Api.download import Download
import globals as g


class Mod:
    '''与模组有关的操作'''

    @staticmethod
    def search_mod(name):
        '''搜索模组'''
        g.logapi.info(f'搜索模组:{name}')
        url = f'https://search.mcmod.cn/s?key={name}'
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'lxml')
        search_result_list = soup.find_all('div', class_='result-item')
        _search_result_list = []

        for i in search_result_list:
            info = Mod.parse_search_result(i)
            if info:
                _search_result_list.append(info)

        return _search_result_list

    @staticmethod
    def parse_search_result(search_result: element.Tag):
        '''解析搜索结果'''
        result = {}
        g.logapi.info(f'解析搜索结果')
        try:
            head = search_result.find('div', class_='head')

            target_blank = head.find_all('a')[-1]
            name = target_blank.text
            mcmode_url = target_blank['href']

            result['name'] = name
            result['mcmod_url'] = mcmode_url

            describe = search_result.find('div', class_='body').text
            result['describe'] = describe

            pattern = r'https://www.curseforge.com/minecraft/mc-mods/.*?</strong>'

            html = requests.get(mcmode_url).text
            result['curseforge_url'] = re.findall(
                pattern, html)[0].replace('</strong>', '')
        except:
            pass

        return result

    @staticmethod
    def get_mod_files(info):
        '''获取模组文件'''
        g.logapi.info(f'获取模组文件:{info["name"]}')
        url = info['curseforge_url']+'/files/all'
        files = []

        html = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'Referer': 'https://www.curseforge.com/'
        }).text
        soup = BeautifulSoup(html, 'lxml')
        trs = soup.find_all('tr')
        for tr in trs:
            files.append(Mod.get_mod_file_info(tr))

        return files

    @staticmethod
    def get_mod_file_info(tr: element.Tag):
        result = {}

        td = tr.find_all('td')[1]
        a = td.find_all('a')

        result['name'] = a.text
        result['url'] = a['href']

        return result

    def download_mod_file(self, info, path):
        '''下载模组文件'''
        url = 'https://www.curseforge.com/'+info['url']
        g.logapi.info(f'下载模组文件:{url}')

        for i in Download.download(url, path):
            yield i
