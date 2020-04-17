'''
# BridgeCaller v0.1

依赖的库：
- requests
'''

VERSION = "v0.1"

import os
import requests as rq
import threading as thd
try:
    from BCLib import *
    print('dbg import')
except:
    try:
        from plugins.BCLib import *
        print('MCDR env import')
    except:
        raise

global bgSRV
bgSRV = None

# fast function
HAVE_HELPER_PERMISSION = lambda info,server:server.get_permission_level(info) ==None or server.get_permission_level(info) >= 2
HAVE_ADMIN_PERMISSION = lambda info,server:server.get_permission_level(info) ==None or server.get_permission_level(info) >= 3
NO_PERMISSION = lambda server,info:server.tell(info.player,"§c权限不足")

global pack,blb
blb = None
pack = None



def on_load(server,old_plugin):

    server.logger.info("BridgeCaller {}".format(VERSION))

    server.add_help_message("!!bc","BridgeCaller插件管理")
    try:
        for directory in ('bcfile', 'bcfile/tmp', 'bcfile/info'):
            os.mkdir(directory)
        server.logger.info('已初始化bcfile目录')
    except:pass

    # Start background service
    datapack_lib.start_srv(server)
    

def on_unload(server):
    datapack_lib.stop_srv(server)
    
def on_info(server,info):
    command = info.content.split(' ')
    global pack
    if command[0] == '!!bc':
        if command[1] == 'install':
            if HAVE_ADMIN_PERMISSION(info,server): 
                
                # try: # 因调试需要，为防止错误自动捕获
                server.logger.info('正在寻找包')
                server.reply(info,'正在寻找包...请稍后')
                pack = pack_search.Pack(server,info.player)
                pack.from_cloud(command[2])
                pack.show_status(info)
                # except:
                #     if info.is_player:
                #         server.tell(info.player,'§c参数错误！请使用!!bc查看帮助')
                #     else:
                #         server.logger.info('参数错误！请使用!!bc查看帮助')
                #     return #back
                
            else:
                NO_PERMISSION(server,info)
        elif command[1]=='remove':
            pass
        elif command[1] == 'start_download':
            if HAVE_ADMIN_PERMISSION(info,server): 
                #global pack
                pack.start_download()
            else:
                NO_PERMISSION(server,info)