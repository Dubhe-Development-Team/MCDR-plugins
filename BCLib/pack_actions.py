from utils.info import Info
from .packobj import *
import threading as thd
import hashlib as hlib
import os
import shutil

# define global
global PacksTasksNow, DownloadThreads
PacksTasksNow = {}
DownloadThreads = {}

'''
例：{
    "userwrc":<PackOBJ>
}
'''


def format_err_msg(msg):
    msg_list = ['§c' + x + '§c' for x in str(msg)]
    return ''.join(msg_list)


def genSHA_256(filename):
    with open(filename, 'rb') as f:
        return hlib.sha256().hexdigest()


def gen_floderSHA(floder, target):
    for i in os.listdir(floder):
        if not os.path.isfile(floder + '/' + i):
            try:
                os.mkdir('{}/{}'.format(target, i))
            except:
                pass
            gen_floderSHA('{}/{}'.format(floder, i), '{}/{}'.format(target, i))
        else:
            with open('{}/{}.sha-256'.format(target, i), 'w') as sha:
                sha.write(str(genSHA_256(floder + '/' + i)))


def makeInfo():
    r = Info()
    r.player = '@a'
    return r


def getTaskList():
    return PacksTasksNow


def delTask(name):
    del PacksTasksNow[name]


def isInstalled(name, version=-1):
    pass


def getPackInfo(name):
    pass


###### 内部函数，如果不知道这些函数的作用，请勿调用！#####
def show_help_msg(server, info):
    help_msg = """
###############################################
§7!!bc    §r显示帮助信息
§7!!bc install <包链接>   §r从指定链接安装包
§7!!bc remove <包名>    §r移除包 注意：如果有依赖此包的包，也会一起移除！
§7!!bc enable <包名>    §r启用包
§7!!bc disable <包名>    §r禁用包
§7!!bc update [包名]    §r从包元数据中指定的链接升级包，包名留空以对所有包进行更新检测
§7!!bc reload    §r重载所有的包
§7!!bc regen-SHA-256    §r重新计算SHA-256缓存，在同文件判断出现问题时可以使用
§7!!bc SHA-256 <路径>    §r查询对应文件的SHA-256，在下文详细解释
§7!!bc list    §r显示所有已安装的包
§7!!bc listall    §r显示所有插件和数据包
§7!!bc search <包名>    §r查询是否已安装此包
§7!!bc on    §r启用bc包管理功能
§7!!bc off    §r禁用bc包管理功能
查看更多帮助，请前往：§9§nhttps://gitee.com/gu_zt666/BridgeCaller"""

    server.reply(info, help_msg)


def refreshSHA256(server):
    server.logger.info('开始更新SHA-256缓存')
    for i in ('./bcfile/cache/sha-256/pyplugins', './bcfile/cache/sha-256/datapacks'):
        shutil.rmtree(i)
        os.mkdir(i)

    gen_floderSHA('./plugins', './bcfile/cache/sha-256/pyplugins')
    gen_floderSHA('./server/world/datapacks', './bcfile/cache/sha-256/datapacks')
    server.logger.info('SHA-256缓存更新完毕')


def installPack(server, info, name):
    server.logger.info('正在寻找包')
    server.reply(info, '正在寻找包...请稍后')
    try:
        del PacksTasksNow[info.player_bcsign]
    except:
        pass
    PacksTasksNow[info.player_bcsign] = Pack(server, info.player_bcsign)
    PacksTasksNow[info.player_bcsign].from_cloud(name)
    PacksTasksNow[info.player_bcsign].show_status(info)


def startDownload(server, info):
    try:
        DownloadThreads[info.player_bcsign] = thd.Thread(target=PacksTasksNow[info.player_bcsign].start_download(),
                                                         name="BridgeCaller: Download Thread")
    except KeyError:
        server.reply(info, '§c目前没有要下载的任务')


def checkUpdate(server, info, name):
    PacksTasksNow[info.player_bcsign] = Pack(server, info.player_bcsign)
    PacksTasksNow[info.player_bcsign].from_local(name)

    if PacksTasksNow[info.player_bcsign].chkupdate():
        server.reply(info, '检测到新版本：')
        PacksTasksNow[info.player_bcsign].show_status(info)
    else:
        server.reply(info, '已是最新版本。')


def removePack(server, info, name):
    pass
