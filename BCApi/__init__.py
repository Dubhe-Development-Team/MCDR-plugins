'''
BridgeCaller API
'''

__all__ = ['lock','player']

class FeatureNotEnable(Exception):
    '''BridgeCaller功能未启用'''
    def __init__(self, arg):
        self.args = arg


class PackError(Exception):
    '''BridgeCaller包错误'''
    def __init__(self, arg):
        self.args = arg


class NoSuchPlayerError(Exception):
    '''BridgeCaller无法载入对应玩家档案错误'''
    def __init__(self, arg):
        self.args = arg


class MCCommandError(Exception):
    '''BridgeCaller命令执行错误'''
    def __init__(self, arg):
        self.args = arg




