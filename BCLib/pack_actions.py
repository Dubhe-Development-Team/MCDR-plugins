from utils.info import Info
from .packobj import *
import threading as thd
import hashlib as hlib
import os
import shutil

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
    msg_list = ['§c'+x+'§c' for x in str(msg)]
    return ''.join(msg_list)
    
def genSHA_256(filename):
    with open(filename,'rb') as f:
        return hlib.sha256().hexdigest()

def gen_floderSHA(floder,target):
    for i in os.listdir(floder):
        if not os.path.isfile(floder+'/'+i):
            try:
                os.mkdir('{}/{}'.format(target,i))
            except:
                pass
            gen_floderSHA('{}/{}'.format(floder,i),'{}/{}'.format(target,i))
        else:
            with open('{}/{}.sha-256'.format(target,i),'w') as sha:
                sha.write(str(genSHA_256(floder+'/'+i)))


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
def refreshSHA256(server):
    server.logger.info('开始更新SHA-256缓存')
    for i in ('./bcfile/cache/sha-256/pyplugins','./bcfile/cache/sha-256/datapacks'):
        shutil.rmtree(i)
        os.mkdir(i)

    gen_floderSHA('./plugins','./bcfile/cache/sha-256/pyplugins')
    gen_floderSHA('./server/world/datapacks','./bcfile/cache/sha-256/datapacks')
    server.logger.info('SHA-256缓存更新完毕')

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

def removePack(server,info,name):
    pass