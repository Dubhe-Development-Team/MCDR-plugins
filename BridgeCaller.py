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

global tasks,blb
blb = None
tasks = pack_actions.getTaskList()



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
    if info.player == None:
        info.player_bcsign = '服务器终端'
    else:
        info.player_bcsign = info.player

    global tasks
    if command[0] == '!!bc':
        if command[1] == 'install':
            if HAVE_ADMIN_PERMISSION(info,server): 
                
                try: # 因调试需要，为防止错误自动捕获
                    server.logger.info('正在寻找包')
                    server.reply(info,'正在寻找包...请稍后')
                    tasks[info.player_bcsign] = packobj.Pack(server,info.player_bcsign)
                    tasks[info.player_bcsign].from_cloud(command[2])
                    tasks[info.player_bcsign].show_status(info)
                except Exception as exp:
                    server.reply(info,'§c错误: {}'.format(exp))
                    del tasks[info.player_bcsign]
                    return #back
                
            else:
                NO_PERMISSION(server,info)
        elif command[1]=='remove':
            pass
        elif command[1] == 'start_download':
            if HAVE_ADMIN_PERMISSION(info,server): 
                #global pack
                down_thread = thd.Thread(target=tasks[info.player_bcsign].start_download(),name="Download Thread")
            else:
                NO_PERMISSION(server,info)
        elif command[1] == 'chkupdate':
            if HAVE_HELPER_PERMISSION(info,server): 
                tasks[info.player_bcsign] = packobj.Pack(server,info.player_bcsign)
                try:
                    tasks[info.player_bcsign].from_local(command[2])
                except FileNotFoundError as exp:
                    server.reply(info,'§c无效的插件名！ {}'.format(exp))
                    return
                except IndexError as exp:
                    server.reply(info,'§c请输入插件名！ {}'.format(exp))
                    return
                if tasks[info.player_bcsign].chkupdate():
                    tasks[info.player_bcsign].show_status()
                else:
                    server.reply(info,'暂无无可用更新')
        else:
            server.reply(info,"§c命令错误！使用!!bc查看帮助")