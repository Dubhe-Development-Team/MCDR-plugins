from utils.info import Info
from .packobj import *
import threading as thd

#define global
global PacksTasksNow,DownloadThreads
PacksTasksNow = {}
DownloadThreads = {}

'''
例：{
    "userwrc":<PackOBJ>
}
'''
def format_err_msg(msg):
    msg_list = ['§c'+x for x in str(msg)]
    return ''.join(msg_list)
    


def makeInfo():
    r = Info()
    r.player = '@a'
    return r

def getTaskList():
    return PacksTasksNow

def delTask(name):
    del PacksTasksNow[name]

def isInstalled(name,version=-1):
    pass

def getPackInfo(name):
    pass

###### 内部函数，如果不知道这些函数的作用，请勿调用！#####
def installPack(server,info,name):
    server.logger.info('正在寻找包')
    server.reply(info,'正在寻找包...请稍后')
    PacksTasksNow[info.player_bcsign] = Pack(server,info.player_bcsign)
    PacksTasksNow[info.player_bcsign].from_cloud(name)
    PacksTasksNow[info.player_bcsign].show_status(info)

def startDownload(server,info):
    try:
        DownloadThreads[info.player_bcsign] = thd.Thread(target=PacksTasksNow[info.player_bcsign].start_download(),name="Download Thread")
    except KeyError:
        server.reply(info,'§c目前没有要下载的任务')

def checkUpdate(server,info,name):
    PacksTasksNow[info.player_bcsign] = Pack(server,info.player_bcsign)
    PacksTasksNow[info.player_bcsign].from_local(name)
    
    if PacksTasksNow[info.player_bcsign].chkupdate():
        server.reply(info,'检测到新版本：')
        PacksTasksNow[info.player_bcsign].show_status(info)
    else:
        server.reply(info,'已是最新版本。')