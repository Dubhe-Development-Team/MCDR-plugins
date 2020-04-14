'''
BridgeCaller v0.1

依赖的库：
requests
'''

VERSION = "v0.1"

import os
import requests as rq
try:
    from BCLib import *
    print('dbg import')
except:
    try:
        from plugins.BCLib import *
        print('MCDR env import')
    except:
        raise


HAVE_HELPER_PERMISSION = lambda info,server:server.get_permission_level(info) ==None or server.get_permission_level(info) >= 2

def on_load(server,old_plugin):
    server.logger.info("BridgeCaller {}".format(VERSION))

    server.add_help_message("!!bc","BridgeCaller插件管理")
    try:
        for directory in ('bcfile', 'bcfile/tmp', 'bcfile/info'):
            os.mikdir(directory)
        server.logger.info('已初始化bcfile目录')
    except:pass

def on_info(server,info):
    command = info.content.split(' ')
    if command[0] == '!!bc':
        if command[1] == 'install':
            if HAVE_HELPER_PERMISSION(info,server):
                try:
                    downpack = pack_search.Pack(command[2],server)
                except:
                    if info.is_player:
                        server.tell(info.player,'§c参数错误！请使用!!bc查看帮助')
                    else:
                        server.logger.info('参数错误！请使用!!bc查看帮助')
                    return #back
                