import requests as rq
import random as rand
import json,os
from utils.info import Info

def makeInfo():
    r = Info()
    r.player = '@a'
    return r


class Pack():
    def __init__(self,server,fromID=None,isroot=True,downlist={
        "datapack":{},
        "pyplugin":{}
    },needpack=[]):
        
        self.randID = rand.randint(100000,999999)
        self.server = server
        self.isroot = isroot
        self.packlink = ''
        self.meta = {}
        self.downlist = downlist # 传递引用，使所有嵌套共用一个列表，以便管理
        self.needpack = needpack
        self.packname = ""

        if fromID==None:
            self.fromID = '服务器终端'
        else:
            self.fromID = fromID
        
    
    def from_cloud(self,link):
        '''
        ### 从网络获取包
        - link:元文件链接(如：https://gitee.com/gu_zt666/BridgeCaller/raw/master/testdata/testdata.dpmeta)
        '''
        self.packlink = link
        if self.isroot:
            self.server.execute('bossbar add getmeta{} "(由{}发起)正在获取{}的元数据"'.format(self.randID,self.fromID,self.packlink))
            self.server.execute('bossbar set getmeta{} color green'.format(self.randID))
            self.server.execute('bossbar set getmeta{} players @a'.format(self.randID))
        try:
            metafile = rq.get(self.packlink,timeout=60)
            self.meta = metafile.json()
            self.meta['child_plugins'] = []
            self.packname = self.meta['packname']
        except:
            raise
        try:
            self.needpack = self.needpack+[Pack(self.server,self.fromID,False,self.downlist,self.needpack).from_cloud(lib['meta']) for lib in self.meta['lib']]

            for lib in self.meta['downloads']['datapack']:
                self.downlist['datapack'][lib] = self.meta['downloads']['datapack'][lib]
                self.server.logger.info('下载数据包文件源添加: {}'.format(self.downlist['datapack'][lib]))
            for lib in self.meta['downloads']['pyplugin']:
                self.downlist['pyplugin'][lib] = self.meta['downloads']['pyplugin'][lib]
                self.server.logger.info('下载插件文件源添加: {}'.format(self.downlist['pyplugin'][lib]))

            self.server.logger.info('下载文件信息：{}'.format(str(self.downlist)))
        except:
            raise
        
        self.server.execute('bossbar remove getmeta{}'.format(self.randID))
        return self

    def from_local(self,file_name):
        '''
        ### 从本地获取包
        - file_name:文件名(如：/home/wrc/test.dpmeta)
        '''
        pass

    def start_download(self):
        '''
        ### 开始下载
        '''
        for pck in self.needpack:
            pck.meta['child_plugins'].append(self.packname)
            pck.start_download()

        #print("{}start!".format(self.packname))
        with open('bcfile/info/{}.dpmeta'.format(self.packname),'w') as pakinfo:
            json.dump(self.meta,pakinfo)

        # Start download
        if self.isroot:
            for obj in self.downlist['datapack']:
                downloadedf = rq.get(self.downlist['datapack'][obj]).content
                try:
                    with open('server/world/datapacks/{}'.format(obj),'wb') as fobj:
                        fobj.write(downloadedf)
                except:
                    self.server.execute('datapack disable "file/{}"'.format(obj))
                    with open('server/world/datapacks/{}'.format(obj),'wb') as fobj:
                        fobj.write(downloadedf)
                    self.server.execute('datapack enable "file/{}"'.format(obj))
            for obj in self.downlist['pyplugin']:
                downloadedf = rq.get(self.downlist['pyplugin'][obj]).content
                
                with open('plugins/{}'.format(obj),'wb') as fobj:
                    fobj.write(downloadedf)
                
            self.server.execute('reload')
            self.server._ServerInterface__server.command_manager.reload_plugins(makeInfo())

    def check_update(self):
        '''
        ### 检查包更新
        '''
        pass

    def remove(self,mode=0):
        '''
        ### 移除包
        - mode=1:完全移除
        - mode=0:只移除此包和依赖此包的包
        '''
        pass