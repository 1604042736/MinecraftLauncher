import globals as g


class ManageGamePath:
    '''管理游戏路径'''

    @staticmethod
    def get_all_path():
        '''获得所有路径'''
        return g.config['all_gamepath']

    @staticmethod
    def get_cur_path():
        '''获取当前路径'''
        return g.config['cur_gamepath']

    @staticmethod
    def settocurpath(gamepath):
        '''设置为当前路径'''
        g.config['cur_gamepath'] = gamepath

    @staticmethod
    def delpath(gamepath):
        '''删除路径'''
        g.config['all_gamepath'].remove(gamepath)
        if g.config['cur_gamepath'] == gamepath:
            g.config['cur_gamepath'] = g.config['all_gamepath'][0] if g.config['all_gamepath'] else ''

    @staticmethod
    def addpath(gamepath):
        '''添加路径'''
        g.config['all_gamepath'].append(gamepath)
        if g.config['cur_gamepath'] == '':
            g.config['cur_gamepath'] = gamepath
