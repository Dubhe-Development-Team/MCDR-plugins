import requests as rq
import random as rand
import json,os
try:
    from plugins.BCLib.pack_actions import *
except:
    from BCLib.pack_actions import *

from utils.info import Info


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
        self.version = 0
        self.fromID = fromID
        self.childPacks = []

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
        self.version = self.meta['packversion']

        return self

    def from_local(self,file_name,outMCDR=False):
        '''
        ### 从本地获取包
        - file_name:文件名(如：/home/wrc/test.dpmeta)
        - outMCDR:是否处于外部
        '''
        if not outMCDR:
            file_name = "./bcfile/info/{}.dpmeta".format(file_name)

        with open(file_name) as meta:
            self.meta = json.load(meta)
        self.version = self.meta['packversion']
        self.childPacks = self.meta['child_plugins']
        self.version = self.meta['packversion']
        self.packname = self.meta['packname']

    def start_download(self):
        '''
        ### 开始下载
        '''

        if self.isroot:
            self.server.execute('bossbar add down{} "(由{}发起)开始下载……"'.format(self.randID,self.fromID))
            self.server.execute('bossbar set down{} color green'.format(self.randID))
            self.server.execute('bossbar set down{} players @a'.format(self.randID))

            self.server.execute('bossbar add downsub{} "子任务"'.format(self.randID))
            self.server.execute('bossbar set downsub{} color green'.format(self.randID))
            self.server.execute('bossbar set downsub{} players @a'.format(self.randID))

        for pck in self.needpack:
            pck.meta['child_plugins'].append(self.packname)
            pck.start_download()

        #print("{}start!".format(self.packname))
        with open('bcfile/info/{}.dpmeta'.format(self.packname),'w') as pakinfo:
            json.dump(self.meta,pakinfo)
        
        plugin_cnt = len(self.downlist['pyplugin'])
        datapack_cnt = len(self.downlist['datapack'])
        # Start download
        if self.isroot:
            self.server.execute('bossbar set down{} value 0'.format(self.randID))
            self.server.execute('bossbar set down{} name "(由{}发起)正在下载：需要的数据包"'.format(self.randID,self.fromID))
            self.server.execute('bossbar set downsub{} name "正在下载({}/{})：{}"'.format(self.randID,datapack_cnt,0,''))
            self.server.execute('bossbar set downsub{} max {}'.format(self.randID,datapack_cnt))
            
            # Download datapacks
            down_index = 0
            for obj in self.downlist['datapack']:
                down_index += 1
                self.server.execute('bossbar set downsub{} name "正在下载({}/{})：{}"'.format(self.randID,down_index,datapack_cnt,obj))
                
                downloadedf = rq.get(self.downlist['datapack'][obj]).content
                try:
                    with open('server/world/datapacks/{}'.format(obj),'wb') as fobj:
                        fobj.write(downloadedf)
                except:
                    self.server.execute('datapack disable "file/{}"'.format(obj))
                    with open('server/world/datapacks/{}'.format(obj),'wb') as fobj:
                        fobj.write(downloadedf)
                    self.server.execute('datapack enable "file/{}"'.format(obj))
            self.server.execute('bossbar set downsub{} value {}'.format(self.randID,down_index))
                

            # Download plugins
            self.server.execute('bossbar set down{} value 40'.format(self.randID))
            self.server.execute('bossbar set down{} name "(由{}发起)正在下载：需要的插件包"'.format(self.randID,self.fromID))
            self.server.execute('bossbar set downsub{} name "正在下载({}/{})：{}"'.format(self.randID,plugin_cnt,0,''))
            self.server.execute('bossbar set downsub{} max {}'.format(self.randID,plugin_cnt))

            
            down_index = 0
            self.server.execute('bossbar set downsub{} value 0'.format(self.randID))
            
            for obj in self.downlist['pyplugin']:
                down_index += 1
                self.server.execute('bossbar set downsub{} name "正在下载({}/{})：{}"'.format(self.randID,down_index,plugin_cnt,obj))
                downloadedf = rq.get(self.downlist['pyplugin'][obj]).content
                
                with open('plugins/{}'.format(obj),'wb') as fobj:
                    fobj.write(downloadedf)
                self.server.execute('bossbar set downsub{} value {}'.format(self.randID,down_index))

                
            self.server.execute('bossbar remove downsub{}'.format(self.randID))
               
            self.server.execute('bossbar set down{} value 80'.format(self.randID))
            self.server.execute('bossbar set down{} name "(由{}发起)正在重新加载以应用所有更改"'.format(self.randID,self.fromID))
            self.server.execute('reload')
            self.server._ServerInterface__server.command_manager.reload_plugins(makeInfo()) # reload all plugins
            self.server.execute('bossbar remove down{}'.format(self.randID))

    def show_status(self,info):
        self.server.reply(info,"§l包名:§r§a{}".format(self.packname))
        self.server.reply(info,"§l将要下载的数据包：(x{})".format(str(len(self.downlist['datapack']))))
        for dp in self.downlist['datapack']:
            self.server.reply(info,"- {}:§7§n{}".format(dp,self.downlist['datapack'][dp]))
        self.server.reply(info,"§l将要下载的插件：(x{})".format(str(len(self.downlist['pyplugin']))))
        for dp in self.downlist['pyplugin']:
            self.server.reply(info,"- {}:§7§n{}".format(dp,self.downlist['pyplugin'][dp]))
        self.server.reply(info,"§l将要下载的依赖包：(x{})".format(str(len(self.needpack))))
        for dp in self.needpack:
            self.server.reply(info,"- {}:§7§n{}".format(dp.packname,dp.packlink))
        self.server.reply(info,'若要开始下载此包，请使用!!bc start_download')

    def chkupdate(self):
        '''
        ### 检查包更新
        True:有更新
        False:无更新
        '''
        self.packlink = self.meta['update_link']
        vernow = self.meta['packversion']
        self.from_cloud(self.packlink)
        
        return vernow < self.version
            
    def remove(self,mode=0):
        '''
        ### 移除包
        - mode=1:完全移除
        - mode=0:只移除此包和依赖此包的包
        '''
        pass

    def __del__(self):
        self.server.execute('bossbar remove getmeta{}'.format(self.randID))
        self.server.execute('bossbar remove downsub{}'.format(self.randID))
        self.server.execute('bossbar remove down{}'.format(self.randID))

        