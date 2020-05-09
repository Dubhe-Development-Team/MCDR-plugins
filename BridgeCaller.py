'''
BridgeCaller v0.1

该插件提供数据接口。请使用BCLib中的bcapi。

依赖的库：
- requests
'''

VERSION = "v0.1"

import os
import requests as rq
import threading as thd
import importlib as ilib

global pack_actions,packobj,datapack_lib

pack_actions = ilib.import_module('plugins.BCLib.pack_actions')
packobj = ilib.import_module('plugins.BCLib.packobj')
datapack_lib = ilib.import_module('plugins.BCLib.datapack_lib')

global bgSRV
bgSRV = None

# fast function
HAVE_HELPER_PERMISSION = lambda info,server:server.get_permission_level(info) ==None or server.get_permission_level(info) >= 2
HAVE_ADMIN_PERMISSION = lambda info,server:server.get_permission_level(info) ==None or server.get_permission_level(info) >= 3
NO_PERMISSION = lambda server,info:server.tell(info.player,"§c权限不足")

global tasks,blb
blb = None
tasks = pack_actions.getTaskList()

COMMAND_LINKS = {
    "install":[pack_actions.installPack,True,3],
    "start_download":[pack_actions.startDownload,False,2],
    "chkupdate":[pack_actions.checkUpdate,True,2]
}

def launch_cmd(server,info,launch_target,arg=None):
    if server.get_permission_level(info) ==None or server.get_permission_level(info) >= launch_target[2]:
        if launch_target[1]:
            launch_target[0](server,info,arg)
        else:
            launch_target[0](server,info)
    else:
        NO_PERMISSION(server,info)

def on_load(server,old_plugin):
    global pack_actions,packobj,datapack_lib

    server.logger.info("BridgeCaller {}".format(VERSION))
    # 动态重载
    
    for m in (pack_actions,packobj,datapack_lib):
        server.logger.info('已加载{}'.format(m))
        ilib.reload(m)

    server.add_help_message("!!bc","BridgeCaller插件管理")
    
    for directory in ('bcfile', 'bcfile/tmp', 'bcfile/info','bcfile/cache',
                    'bcfile/cache/sha-256','bcfile/cache/sha-256/pyplugins',
                    'bcfile/cache/sha-256/datapacks','bcfile/filelink',
                    'bcfile/filelink/pyplugins','bcfile/filelink/datapacks'):
        try:
            os.mkdir(directory)
            server.logger.info("创建目录：{}".format(directory))
        except:
            pass
    server.logger.info('已初始化bcfile目录')
    

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
        try:
            if command[1] == None:
                server.reply('未知的命令！')
        except:
            server.reply('未知的命令！')
        try:
            if not COMMAND_LINKS[command[1]][1]:
                launch_cmd(server,info,COMMAND_LINKS[command[1]])
            else:
                launch_cmd(server,info,COMMAND_LINKS[command[1]],command[2])
        except IndexError as exp:
            server.reply(info,'§c参数缺失！ {}'.format(exp))
        except KeyError as exp:
            server.reply(info,'§c参数错误！ {}'.format(exp))
        except Exception as exp:
            server.reply(info,'§c{}'.format(pack_actions.format_err_msg(exp)))
            try:pack_actions.delTask(info.player_bcsign)
            except:pass

