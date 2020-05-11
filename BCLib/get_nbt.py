"""
get_nbt

获取level.dat playerdata scoreboard.dat信息

"""
import os
import nbtlib

global path
global seed

# 获取服务器目录
def get_path():
    global path
    path = ""
    # 获取MCDRconfig文件
    for i in open(os.path.join(os.path.abspath(os.path.join(os.getcwd(), "../..")), "config.yml"), "r").readlines():
        # 读取服务器目录
        if i[0:17] == "working_directory":
            for j in i[19:-1]:
                # 目录中 "/" 转为 "\"
                if j != "/":
                    path += j
                else:
                    path += "\\"
            # 获取完成
            path = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "../..")), path)
            break
    return path


# 获取世界种子
def get_seed(server):
    global path
    # 获取level.dat文件
    path = os.path.join(get_path(), "world", "level.dat")
    # 文件内容分成列表
    nbt = str(nbtlib.load(path).root['Data']).split(', ')
    # 读取失败赋值不变
    global seed
    seed = "读取失败"
    for i in nbt:
        # 获取种子
        if i[0:10] == "RandomSeed":
            seed = i[12:-1]
            print(seed)
            break


# 获取玩家真实ID
def get_id(server):
    pass


# 获取计分板
def get_scoreboard(server):
    pass


# 获取玩家背包
def get_bag(server):
    pass
