from utils.info import Info

#define global
global PacksTasksNow
PacksTasksNow = {}

'''
例：{
    "userwrc":<PackOBJ>
}
'''

def makeInfo():
    r = Info()
    r.player = '@a'
    return r

def getTaskList():
    return PacksTasksNow

def isInstalled(name,version=-1):
    pass

def getPackInfo(name):
    pass
