import requests as rq
import random as rand
import json,os

class Pack():
    def __init__(self,server,isroot=True,downlist={
        "datapack":{},
        "pyplugin":{}
    },needpack=[]):
        
        self.server = server
        self.isroot = isroot
        self.packlink = ''
        self.meta = {}
        self.downlist = downlist # 传递引用，使所有嵌套共用一个列表，以便管理
        self.needpack = needpack
        self.packname = ""
        
    
    def from_cloud(self,link):
        '''
        ### 从网络获取包
        - link:元文件链接(如：https://gitee.com/gu_zt666/BridgeCaller/raw/master/testdata/testdata.dpmeta)
        '''

        self.packlink = link
        try:
            metafile = rq.get(self.packlink,timeout=60)
            self.meta = metafile.json()
            self.packname = self.meta['packname']
        except:
            raise
        try:
            self.needpack = self.needpack+[Pack(self.server,False,self.downlist,self.needpack).from_cloud(lib['meta']) for lib in self.meta['lib']]

            for lib in self.meta['downloads']['datapack']:
                self.downlist['datapack'][lib] = self.meta['downloads']['datapack'][lib]
                self.server.logger.info('下载数据包文件源添加: {}'.format(self.downlist['datapack'][lib]))
            for lib in self.meta['downloads']['pyplugin']:
                self.downlist['pyplugin'][lib] = self.meta['downloads']['pyplugin'][lib]
                self.server.logger.info('下载插件文件源添加: {}'.format(self.downlist['pyplugin'][lib]))

            self.server.logger.info('下载文件信息：{}'.format(str(self.downlist)))
        except:
            raise

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
            pck.start_download()

        #print("{}start!".format(self.packname))
        with open('bcfile/info/{}'.format(self.packname),'w') as pakinfo:
            json.dump(self.meta,pakinfo)

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