# -*- coding: utf-8 -*-
# v1.9.0

import json

# 请配置以下两个变量
# Please configure the fallowing 2 variables
server_ids = ["lobby", "survial", "creative"]
server_names = ["主城", "生存", "创造"]



def on_load(server, old):
    server.add_help_message('!!sc', '切换服务器')


def on_info(server, info):
    if info.content == "!!sc" and len(server_ids) == len(server_names):
        server.tell(info.player, "§a请点击要更换的服务器")
        for order in range(0, len(server_ids)):
            server.execute("tellraw " + info.player + " " + server_choose(server_names[order], server_ids[order]))
    elif info.content == "!!sc" and len(server_ids) == len(server_names):
        server.tell(info.player, "§c服务器列表配置错误！")


def server_choose(server_name, server_id):
    return json.dumps(
        [
            {
                "text": "§a[{}]".format(server_name),
                "clickEvent":{
                    "action":"run_command",
                    "value":"/server {}".format(server_id)
                }
            }
        ]
    )