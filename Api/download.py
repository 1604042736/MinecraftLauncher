import time
import globals as g
import os
import requests


class Download:
    '''下载操作'''
    @staticmethod
    def download(url, path):
        '''下载'''
        if url=='':
            return
        try:
            # 创建这个路径
            os.makedirs(os.path.dirname(path))
        except:
            pass

        with open(path, 'wb')as fileobj:
            while True:
                try:
                    rsp = requests.get(url, stream=True, timeout=5)
                    offset = 0
                    for chunk in rsp.iter_content(chunk_size=10240):
                        if not chunk:
                            break
                        fileobj.seek(offset)  # 设置指针位置
                        fileobj.write(chunk)  # 写入文件
                        offset = offset + len(chunk)
                        proess = offset / \
                            int(rsp.headers['Content-Length']) * 100  # 进度
                        yield int(proess)
                    break
                except Exception as e:
                    g.logapi.error(e)
                    if url:
                        g.logapi.info(f'尝试重新下载"{url}"')
                        time.sleep(0.5)

    @staticmethod
    def check_download(path, url, redownload=False):
        '''检查文件是否下载'''
        if not redownload and os.path.exists(path):
            return
        g.logapi.info(f'下载"{url}"到"{path}"')
        for i in Download.download(url, path):
            g.logapi.debug(f'"{url}"下载进度: {i}/100')
