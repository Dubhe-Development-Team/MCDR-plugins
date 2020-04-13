'''
BridgeCaller v0.1

依赖的库：
requests
'''

VERSION = "v0.1"

import os
import requests as rq
try:
    from BCLib import *
    print('dbg import')
except:
    try:
        from plugins.BCLib import *
        print('MCDR env import')
    except:
        raise

def on_load(server,old_plugin):
    server.logger.info("BridgeCaller {}".format(VERSION))

    server.add_help_message("!!bc","BridgeCaller插件管理")
    try:
        os.mkdir('bcfile')
        os.mkdir('bcfile/tmp')
        os.mkdir('bcfile/info')
        server.logger.info('已初始化bcfile目录')
    except:pass