'''
BridgeCaller command system

'''

from .pack_actions import *


NO_PERMISSION = lambda server, info: server.tell(info.player, "§c权限不足")

def launch_cmd(server, info, launch_target, extarg=[]):
    '''launch command'''
    if len(extarg) < launch_target[2]: raise Exception(str('参数过少！,至少需要{}个附加参数'.format(launch_target[2])))
    
    if server.get_permission_level(info) is None or server.get_permission_level(info) >= launch_target[1]:
        launch_target[0](server, info, extarg)
    else:
        NO_PERMISSION(server, info)



def subcall(server, info, extra_arg):
    try:
        CMDCALL = CMD_CHART_MAP[extra_arg[0]][extra_arg[1]]
    except Exception as exp:
        server.reply(info, '§c参数错误！ {}'.format(format_err_msg(exp)))
        return

    launch_cmd(server, info, CMDCALL, extra_arg[1:])

# 链接命令
global ROOT, MAIN_CMD_LINK, PACKMAN_CMD_LINK, CACHE_CMD_LINK, CONFIG_CMD_LINK, CMD_CHART_MAP
ROOT = {
    "!!bc":[subcall, 0, 1] # 进行递归解析，先将第一层解析出来，然后再逐步向下解析子命令
}
MAIN_CMD_LINK = {
    "packman": [subcall, 0, 1],
    "cache": [subcall, 0, 1],
    "config": [],
    "reload": [],
    "about": [],
    "help": [show_help_msg, 0, 0]
}
PACKMAN_CMD_LINK = {
    "install": [installPack, 3, 1], # [callobj, permission_lv, extra_arg_cnt]
    "start": [startDownload, 2, 0],
    "chkupdate": [checkUpdate, 2, 0],
}
CACHE_CMD_LINK = {

}
CONFIG_CMD_LINK = {

}
CMD_CHART_MAP = {
    "packman": PACKMAN_CMD_LINK,
    "cache": CACHE_CMD_LINK,
    "config": CONFIG_CMD_LINK,
    "!!bc": MAIN_CMD_LINK
}