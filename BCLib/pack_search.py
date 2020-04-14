import requests as rq
import random as rand
import json,os

class Pack():
    def __init__(self,meta_link,server,isroot=True,downlist={
        "datapack":{},
        "pyplugin":{}
    },needpack=[]):
        try:
            metafile = rq.get(meta_link,timeout=60)
        except:
            raise
        self.isroot = isroot
        self.meta = metafile.json()
        self.downlist = downlist # 传递引用，使所有嵌套共用一个列表，以便管理
        self.needpack = needpack
        self.packname = self.meta['packname']
        self.packlink = meta_link
        
        try:
            self.needpack = [Pack(lib['meta'],server,False) for lib in self.meta['lib']]

            for lib in self.meta['downloads']['datapack']:
                self.downlist['datapack'][lib] = self.meta['downloads']['datapack'][lib]
                server.logger.info('下载数据包文件源添加: {}'.format(self.downlist['datapack'][lib]))
            for lib in self.meta['downloads']['pyplugin']:
                self.downlist['pyplugin'][lib] = self.meta['downloads']['pyplugin'][lib]
                server.logger.info('下载插件文件源添加: {}'.format(self.downlist['pyplugin'][lib]))

            server.logger.info('下载文件信息：{}'.format(str(downlist)))
        except:
            raise

    def get_downlist(self):
        return self.downlist

    def download(self):
        pass