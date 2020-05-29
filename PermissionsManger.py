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

