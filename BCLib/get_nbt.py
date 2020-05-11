"""
get_nbt

获取level.dat playerdata scoreboard.dat信息

"""
import os
import nbtlib

global path


# 获取服务器目录
def get_path():
    global path
    path = ""
    for i in open(os.path.join(os.path.abspath(os.path.join(os.getcwd(), "../..")), "config.yml"), "r").readlines():
        if i[0:17] == "working_directory":
            for j in i[19:-1]:
                if j != "/":
                    path += j
                else:
                    path += "\\"
            path = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "../..")), path)
            break
    return path


def get_seed(server):
    global path
    path = os.path.join(get_path(), "world", "level.dat")
    nbt = str(nbtlib.load(path).root['Data']).split(', ')
    seed = "读取失败"
    for i in nbt:
        if i[0:10] == "RandomSeed":
            seed = i[12:-1]
            print(seed)
            break
    server.execute("scoreboard objectives add bc.seed dummy")
    server.execute("scoreboard players set $seed bc.seed " + seed)


def get_id(server):
    pass


def get_scoreboard(server):
    pass


def get_bag(server):
    pass
