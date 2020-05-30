"""
BridgeCaller v0.1

该插件提供数据接口。请使用BCLib中的bcapi。

依赖的库：
- requests
"""

VERSION = "v0.1"

import os
import requests as rq
import threading as thd
import importlib as ilib

global SERVER_STARTED, DEBUG
SERVER_STARTED = False

try:
    from .BCLib import *
except:
    from plugins.BCLib import *

global bgSRV
bgSRV = None

# fast function
NO_PERMISSION = lambda server, info: server.tell(info.player, "§c权限不足")

# 调试模式
# 仅用于功能测试，请不要随意开启！
DEBUG = True

global tasks, blb, COMMAND_LINKS
blb = None
tasks = pack_actions.getTaskList()

COMMAND_LINKS = {
}


def launch_cmd(server, info, launch_target, extarg=[]):
    if len(extarg) < launch_target[2]: raise Exception(str('参数过少！,至少需要{}个附加参数'.format(launch_target[2])))
    
    if server.get_permission_level(info) is None or server.get_permission_level(info) >= launch_target[1]:
        launch_target[0](server, info, extarg)
    else:
        NO_PERMISSION(server, info)


def on_load(server, old_plugin):
    # define commands
    global pack_actions, packobj, datapack_lib, COMMAND_LINKS
    COMMAND_LINKS = {
        "install": [pack_actions.installPack, 3, 1], # [callobj, permission_lv, extra_arg_cnt]
        "start": [pack_actions.startDownload, 2, 0],
        "chkupdate": [pack_actions.checkUpdate, 2, 0],
        "refresh_SHA-256": [pack_actions.refreshSHA256, 2, 0],
        "debug": [pack_actions.debug, 1, 0]
    }

    server.logger.info("BridgeCaller {}".format(VERSION))
    # 动态重载
    
    for m in (pack_actions, packobj, datapack_lib):
        server.logger.info('已加载{}'.format(m))
        ilib.reload(m)

    server.add_help_message("!!bc", "BridgeCaller插件管理")
    
    for directory in ('bcfile',
                      'bcfile/tmp',
                      'bcfile/info',
                      'bcfile/cache',
                      'bcfile/cache/sha-256',
                      'bcfile/cache/sha-256/pyplugins',
                      'bcfile/cache/sha-256/datapacks',
                      'bcfile/cache/files',
                      'bcfile/cache/files/pyplugins',
                      'bcfile/cache/files/datapacks',
                      'bcfile/filelink',
                      'bcfile/filelink/pyplugins',
                      'bcfile/filelink/datapacks'):
        try:
            os.mkdir(directory)
            server.logger.info("创建目录：{}".format(directory))
        except:
            pass
    server.logger.info('已初始化bcfile目录')

    # gen file SHA-256
    pack_actions.refreshSHA256(server)

    # Start background service
    # 如果服务器暂未启动，就不启动，等待至服务器启动后再启动服务。
    if SERVER_STARTED:
        datapack_lib.start_srv(server)


def on_unload(server):
    datapack_lib.stop_srv(server)


def on_info(server, info):
    global COMMAND_LINKS
    command = info.content.split(' ')
    if info.player is None:
        info.player_bcsign = '服务器终端'
    else:
        info.player_bcsign = info.player

    global tasks
    if DEBUG:
        if command[0] == '!!bcexec':
            try:
                exec(' '.join(command[1:])), globals(), locals()
                server.reply(info, 'done.')
            except Exception as exp:
                server.reply(info, str(exp))
    if command[0] == '!!bc':
        if len(command) == 1:
            pack_actions.show_help_msg(server, info)
            return 

        # 解析命令
        try:
            CMDCALL = COMMAND_LINKS[command[1]]
        except Exception as exp:
            server.reply(info, '§c参数错误！ {}'.format(pack_actions.format_err_msg(exp)))
            return

        # 运行命令  
        try:
            launch_cmd(server, info, COMMAND_LINKS[command[1]], command[2:])
        except Exception as exp:
            server.reply(info, '§c{}'.format(pack_actions.format_err_msg(exp)))
            try:
                pack_actions.delTask(info.player_bcsign)
            except:
                pass


def on_server_startup(server):
    global SERVER_STARTED
    SERVER_STARTED = True
    # Start background service
    datapack_lib.start_srv(server)
