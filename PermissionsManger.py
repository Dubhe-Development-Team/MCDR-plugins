# -*- coding: utf-8 -*-
import re
import traceback
import copy
import json

HELP_INFO = '''
============= Whitelist helper v0.0.1 =============
!!pm                     打印用户有权限使用的所有的命令，包含每个命令的基础信息，和接受的参数
!!pm user <user> ...     编辑用户权限
!!pm group <group> ...   编辑权限组权限
'''

MLINE = ''''''

MCDR_PREFFIX = "!!"
PROGRAM = "pm","perm","permissions","perms","PermissionsManger"
PLUGIN = PROGRAM
NOT_PERMITTED = "§c权限不足"

def on_load(server, old_module):
    server.add_help_message('!!PermissionsManger', '权限管理')

def on_info(server, info):
    content = info.content.strip()[len(MCDR_PREFFIX):]
    if not content.startswith(PLUGIN):
        return
    content = content[len(PLUGIN):].strip()
    def generate_args(sub_cmd, msg_template):
        pattern = '(?<={} )\S+'.format(sub_cmd)
        for name in re.findall(pattern, content):
            yield "{} {}".format(sub_cmd, name), msg_template.format(name)

    def execute(cmd,  msg, error_msg, permission):
        if server.get_permission_level(info) >= permission:
            server.execute("{} {}".format(PROGRAM, cmd))
            server.tell(info.player, msg)
        else:
            server.tell(info.player, error_msg)


    def help():
        server.tell(info.player, HELP_INFO)


if __name__ == "__main__":
    __test__()
