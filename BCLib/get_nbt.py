"""
get_nbt

获取level.dat playerdata scoreboard.dat信息

"""
import os
import nbtlib
import threading as thd

global bgSRV
bgSRV = None
global STOP_SIGN
STOP_SIGN = 0


def start_srv(server):
    global bgSRV
    bgSRV = thd.Thread(target=lambda: nbtService(server), name='BridgeCaller: NBT获取线程')
    bgSRV.start()


def stop_srv(server):
    global STOP_SIGN
    STOP_SIGN = 1


def nbtService(server):
    """nbt获取服务"""
    # 获取NBT
    server.logger.info(get_seed(server))
    # 这个还没完成，需要接口
    server.logger.info(get_scoreboard(server, "$year", "bc.time"))
    global STOP_SIGN
    while True:
        if STOP_SIGN:
            return


# 获取服务器目录
def get_path():
    path = ""
    # 获取MCDRconfig文件
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


# 获取世界种子
def get_seed(server):
    # 获取level.dat文件
    path = os.path.join(get_path(), "world", "level.dat")
    # 文件内容分成列表
    levelnbt = str(nbtlib.load(path).root['Data']).split(', ')
    # 读取失败赋值不变
    seed = "读取失败"
    for i in levelnbt:
        # 获取种子
        if i[0:10] == "RandomSeed":
            seed = i[12:-1]
            break
    return "地图种子为： " + str(seed)


# 获取玩家真实ID
def get_id(server):
    pass


# 获取计分板
def get_scoreboard(server, player, scoreboard):
    # 获取scoreboard.dat文件
    path = os.path.join(get_path(), "world", "data", "scoreboard.dat")
    scbdnbt = str(nbtlib.load(path).root['data'])
    # 将player部分变为列表
    for i in 1, 2, 3:
        nbt = scbdnbt.split("[")[i].split("]")[0]
        if "Objective" in nbt:
            scbdnbt = nbt.split("}, {")
            # 去除元素中大括号
            nbt = []
            for j in scbdnbt:
                if "{" or "}" in j:
                    nbt.append(j.strip('{}'))
                else:
                    nbt.append(j)
            break
    # 判断玩家计分板与输入值是否符合
    value = ['', '', '']
    for i in nbt:
        i = i.split(", ")
        for j in i:
            # print(j)
            if "Objective" in j:
                value[0] = j[12:-1]
            if "Name" in j:
                value[1] = j[7:-1]
            if "Score" in j:
                value[2] = j[7:]
        if player == value[1] and scoreboard == value[0]:
            return "玩家 " + player + " 的 " + scoreboard + " 计分板值为 " + value[2]


# 获取玩家背包
def get_bag(server):
    pass
