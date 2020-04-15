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
HAVE_HELPER_PERMISSION = lambda info,server:server.get_permission_level(info) ==None or server.get_permission_level(info) >= 2

def automsg(server,info,msg):
    if info.is_player:
        server.tell(info.player,msg)
    else:
        server.logger.info(msg)

def on_load(server,old_plugin):
    server.logger.info("BridgeCaller {}".format(VERSION))

    server.add_help_message("!!bc","BridgeCaller插件管理")
    try:
        for directory in ('bcfile', 'bcfile/tmp', 'bcfile/info'):
            os.mikdir(directory)
        server.logger.info('已初始化bcfile目录')
    except:pass

    # Start background service
    datapack_lib.start_srv(server)
    

def on_unload(server):
    datapack_lib.stop_srv(server)
    
def on_info(server,info):
    command = info.content.split(' ')
    if command[0] == '!!bc':
        if command[1] == 'install':
            if HAVE_HELPER_PERMISSION(info,server): 
                try:
                    server.logger.info('正在寻找包')
                    automsg(server,info,'正在寻找包...请稍后')
                    downpack = pack_search.Pack(command[2],server)
                except:
                    if info.is_player:
                        server.tell(info.player,'§c参数错误！请使用!!bc查看帮助')
                    else:
                        server.logger.info('参数错误！请使用!!bc查看帮助')
                    return #back
                downlist = downpack.downlist
                packlist = downpack.needpack
            
                automsg(server,info,"§l包名:§r§a{}".format(downpack.packname))
                automsg(server,info,"§l将要下载的数据包：(x{})".format(str(len(downlist['datapack']))))
                for dp in downlist['datapack']:
                    automsg(server,info,"- {}:§7§n{}".format(dp,downlist['datapack'][dp]))
                automsg(server,info,"§l将要下载的插件：(x{})".format(str(len(downlist['pyplugin']))))
                for dp in downlist['pyplugin']:
                    automsg(server,info,"- {}:§7§n{}".format(dp,downlist['pyplugin'][dp]))
                automsg(server,info,"§l将要下载的依赖包：(x{})".format(str(len(packlist))))
                for dp in packlist:
                    automsg(server,info,"- {}:§7§n{}".format(dp.packname,dp.packlink))
            
                