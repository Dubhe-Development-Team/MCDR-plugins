"""
# datapack_lib


"""
import os
import nbtlib
import threading as thd
import time
import random
from datetime import datetime

global bgSRV
bgSRV = None
global STOP_SIGN
STOP_SIGN = 0   # debug


def start_srv(server):
    global bgSRV
    bgSRV = thd.Thread(target=lambda: dpService(server), name='BridgeCaller: Datapack_lib服务线程')
    bgSRV.start()


def stop_srv(server):
    global STOP_SIGN
    STOP_SIGN = 1


def dpService(server):
    """数据包辅助服务"""
    # service start code
    thd.Thread(target=lambda: initialization(server), name="BridgeCaller: 初始化服务").start()
    thd.Thread(target=lambda: get_time(server), name="BridgeCaller: 时间获取服务").start()
    thd.Thread(target=lambda: rand(server), name="BridgeCaller: 随机数服务").start()
    thd.Thread(target=lambda: get_seed(server), name="BridgeCaller: 种子获取服务").start()
    server.logger.info('datapack_lib已启动')
    global STOP_SIGN
    while True:
        if STOP_SIGN:
            return


def initialization(server):
    server.execute("scoreboard objectives add bc dummy")


def get_time(server):
    global STOP_SIGN
    time.sleep(3)
    if not server.is_rcon_running():
        server.logger.info("服务器未开启rcon，时间获取服务已关闭")
        return
    while True:
        if STOP_SIGN:
            return
        if server.rcon_query("scoreboard players get #time bc") == "#time has 1 [bc]":
            d = datetime.today()
            server.execute("scoreboard players set #time bc 0")
            server.execute("scoreboard objectives add bc.time dummy")
            server.execute("scoreboard players set $year bc.time " + str(d.year))
            server.execute("scoreboard players set $month bc.time " + str(d.month))
            server.execute("scoreboard players set $day bc.time " + str(d.day))
            server.execute("scoreboard players set $hour bc.time " + str(d.hour))
            server.execute("scoreboard players set $minute bc.time " + str(d.minute))
            server.execute("scoreboard players set $second bc.time " + str(d.second))
            server.execute("scoreboard players set $week bc.time " + str(d.isoweekday()))
        time.sleep(1)


def rand(server):
    global STOP_SIGN
    time.sleep(3)
    if not server.is_rcon_running():
        server.logger.info("服务器未开启rcon，随机数服务已关闭")
        return
    while True:
        if STOP_SIGN:
            return
        if server.rcon_query("scoreboard players get #random bc") == "#random has 1 [bc]":
            server.execute("scoreboard players set #random bc 0")
            server.execute("scoreboard objectives add bc.rand dummy")
            server.execute("scoreboard players set $random bc.rand " + str(random.randint(-100000, 100000)))
        time.sleep(1)


# 获取世界种子
def get_seed(server):
    # 获取level.dat文件
    path = os.path.join(get_path(), "world", "level.dat")
    # 文件内容分成列表
    levelnbt = str(nbtlib.load(path).root['Data']).split(', ')
    # 读取失败赋值不变
    seed = "null"
    for i in levelnbt:
        # 获取种子
        if i[0:10] == "RandomSeed":
            seed = i[12:-1]
            break
    if seed == "null":
        server.logger.info("世界种子读取失败")
    else:
        server.logger.info("世界种子为： " + str(seed))


# 获取玩家真实ID
def get_id():
    pass


# 获取玩家背包
def get_bag():
    pass


# 获取服务器目录
def get_path():
    path = ""
    # 获取MCDR config文件
    for i in open(os.path.join(os.getcwd(), "config.yml"), "r").readlines():
        # 读取服务器目录
        if i[0:17] == "working_directory":
            for j in i[19:-1]:
                # 目录中 "/" 转为 "\"
                if j != "/":
                    path += j
                else:
                    path += "\\"
            # 获取完成
            path = os.path.join(os.getcwd(), path)
            break
    return path
