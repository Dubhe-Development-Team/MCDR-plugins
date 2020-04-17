# -*- coding: utf-8 -*-
import re
import traceback
import copy
# import requests as rq
import json

HELP_INFO = '''
============= Whitelist helper v0.2.3 =============
§f!!whitelist add <玩家>  §7将玩家添加至白名单
§f!!whitelist remove <玩家>  §7将玩家移出白名单
§f!!whitelist search <玩家>  §7判断玩家是否添加至白名单
§f!!whitelist list  §7列出所有在白名单内的玩家
§f!!whitelist reload  §7从白名单文件重新加载白名单
§f!!whitelist on  §7开启白名单
§f!!whitelist off  §7关闭白名单
§f!!whitelist  §7显示此帮助信息
'''

MLINE = ''''''

MCDR_PREFFIX = "!!"
PROGRAM = "whitelist"
PLUGIN = PROGRAM
NOT_PERMITTED = "§c权限不足"

def get_wl():
    with open("./server/whitelist.json") as wl:
        return [item['name'] for item in json.load(wl)]

def on_load(server, old_module):
    server.add_help_message('!!whitelist', '白名单编辑')

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

    def list_all():
        names = get_wl()
        server.tell(info.player, "白名单中共有{}名玩家:{}".format(len(names), ", ".join(names)))

    def search():
        try:
            target = info.content.split(" ")[2]
            names = get_wl()
            server.tell(info.player, "{}{}在白名单中".format(target, "" if target in names else "不"))
        except:
            server.tell(info.player,"命令错误！请使用!!whitelist查看帮助")


    cmd_mappings = {
        "add": (generate_args("add", "已将 {} 加入白名单"), NOT_PERMITTED, 2),
        "remove": (generate_args("remove", "已将 {} 移出白名单"), NOT_PERMITTED, 2),
        "reload": ([("reload", "已重新读取白名单")], NOT_PERMITTED, 2),
        "on": ([("on","白名单已开启" )], NOT_PERMITTED, 3),
        "off": ([("off", "白名单已关闭")], NOT_PERMITTED, 3),
        "list": list_all,
        "search": search,
    }

    if not content:
        server.tell(info.player, HELP_INFO)
    else:
        sub_cmd = content.split()[0]
        if sub_cmd not in cmd_mappings:
            server.tell(info.player, "unsupported sub cmd {}".format(sub_cmd))
        else:
            config = cmd_mappings[sub_cmd]
            if type(config) is tuple:
                args, error_msg, permission = config
                for cmd, msg in args:
                    execute(cmd, msg, error_msg, permission)
            else:
                config()


def __test__():
    from collections import namedtuple
    Info = namedtuple("Info", ["content", "player"])

    Server = type("FakeServer", (object,), {
        "tell": lambda self, player, msg: print("[server tell msg]:\t" + " ".join([player, msg])),
        "execute": lambda self, *args: print("[server execute]:\t" + " ".join(args)),
        "get_permission_level": lambda self, info: 3,
        })

    server = Server()
    global get_wl
    get_wl = lambda: ["user1", "user2"]

    def fake_info(content, player="fake_user"):
        return Info(content="{}{} {}".format(MCDR_PREFFIX, PLUGIN, content), player=player)

    tests = [
        "add user2",
        "remove user1",
        "reload",
        "on",
        "off",
        "list",
        "search user3",
        "search user1",
        ""
    ]
    for test in tests:
        info = fake_info(test)
        print("[test content]: ", info.content)
        on_info(server, info)

if __name__ == "__main__":
    __test__()


