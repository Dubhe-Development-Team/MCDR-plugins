"""
packobj

BridgeCaller包对象(Pack)

"""
import requests as rq
import random as rand
import json, os
from .pack_actions import *


class Pack():
    """
    Pack:包对象

    from_cloud：从云端获取包
    from_local：从本地获取包
    start_download：开始下载
    chkupdate：检查更新
    show_status：显示包信息
    remove：移除包
    """
    def __init__(self, server, fromID=None, isroot=True, downlist={
        "datapack": {},
        "pyplugin": {}
    }, remove_list={
        "datapack": {},
        "pyplugin": {}
    }, needpack=[], needpack_name=[], removepack=[], removepack_name=[]):
        
        self.randID = rand.randint(100000, 999999)
        self.server = server
        self.isroot = isroot
        self.packlink = ''
        self.meta = {}

        self.downlist = downlist    # 传递引用，使所有嵌套共用一个列表，以便管理
        self.needpack_name = needpack_name
        self.needpack = needpack

        self.remove_list = remove_list  # 同downlist
        self.removepack = removepack  # 需要删除的包
        self.removepack_name = removepack_name

        self.packname = ""
        self.version = 0
        self.fromID = fromID
        self.childPacks = []
        self.download_thread = None

    def from_cloud(self, link):
        """
        ### 从网络获取包
        - link:元文件链接(如：https://gitee.com/gu_zt666/BridgeCaller/raw/master/testdata/testdata.dpmeta)
        """
        self.packlink = link
        if self.isroot:
            self.server.execute('bossbar add getmeta{} "(由{}发起)正在获取{}的元数据"'.format(self.randID, self.fromID, self.packlink))
            self.server.execute('bossbar set getmeta{} color green'.format(self.randID))
            self.server.execute('bossbar set getmeta{} players @a'.format(self.randID))

        metafile = rq.get(self.packlink, timeout=60)
        self.meta = metafile.json()
        self.meta['child_plugins'] = []
        if self.meta['packname'] in self.needpack_name:     # check if tp
            self.server.logger.info('已剔除重复包: {}'.format(self.meta['packname']))
            return
        self.__cloud_data_init()
        self.server.execute('bossbar remove getmeta{}'.format(self.randID))
        
        return self

    def from_local(self, file_name, outMCDR=False):
        """
        ### 从本地获取包
        - file_name:文件名(如：/home/wrc/test.dpmeta)
        - outMCDR:是否处于外部
        """
        if not outMCDR:
            file_name = "./bcfile/info/{}.dpmeta".format(file_name)
        
        with open(file_name) as meta:
            self.meta = json.load(meta)
        if self.meta['packname'] in self.removepack_name:     # check if tp
            self.server.logger.info('已剔除重复包: {}'.format(self.meta['packname']))
            return
        self.__local_data_init()

    def start_download_thread(self):
        pass

    def start_download(self):
        """
        ### 开始下载
        """

        if self.isroot:
            self.server.execute('bossbar add down{} "(由{}发起)开始下载……"'.format(self.randID, self.fromID))
            self.server.execute('bossbar set down{} color green'.format(self.randID))
            self.server.execute('bossbar set down{} players @a'.format(self.randID))

            self.server.execute('bossbar add downsub{} "子任务"'.format(self.randID))
            self.server.execute('bossbar set downsub{} color green'.format(self.randID))
            self.server.execute('bossbar set downsub{} players @a'.format(self.randID))

        for pck in self.needpack:
            pck.meta['child_plugins'].append(self.packname)
            pck.start_download()

        # print("{}start!".format(self.packname))
        with open('bcfile/info/{}.dpmeta'.format(self.packname), 'w') as pakinfo:
            json.dump(self.meta, pakinfo)
        
        plugin_cnt = len(self.downlist['pyplugin'])
        datapack_cnt = len(self.downlist['datapack'])
        # Start download
        if self.isroot:
            self.server.execute('bossbar set down{} value 0'.format(self.randID))
            self.server.execute('bossbar set down{} name "(由{}发起)正在下载：需要的数据包"'.format(self.randID, self.fromID))
            self.server.execute('bossbar set downsub{} name "正在下载({}/{})：{}"'.format(self.randID, datapack_cnt, 0, ''))
            self.server.execute('bossbar set downsub{} max {}'.format(self.randID, datapack_cnt))
            
            # Download datapacks
            down_index = 0
            for obj in self.downlist['datapack']:
                down_index += 1
                self.server.execute('bossbar set downsub{} name "正在下载({}/{})：{}"'.format(self.randID, down_index, datapack_cnt, obj))
                
                downloadedf = rq.get(self.downlist['datapack'][obj]).content
                try:
                    with open('server/world/datapacks/{}'.format(obj), 'wb') as fobj:
                        fobj.write(downloadedf)
                except:
                    self.server.execute('datapack disable "file/{}"'.format(obj))
                    with open('server/world/datapacks/{}'.format(obj), 'wb') as fobj:
                        fobj.write(downloadedf)
                    self.server.execute('datapack enable "file/{}"'.format(obj))
            self.server.execute('bossbar set downsub{} value {}'.format(self.randID, down_index))

            # Download plugins
            self.server.execute('bossbar set down{} value 40'.format(self.randID))
            self.server.execute('bossbar set down{} name "(由{}发起)正在下载：需要的插件包"'.format(self.randID, self.fromID))
            self.server.execute('bossbar set downsub{} name "正在下载({}/{})：{}"'.format(self.randID, plugin_cnt, 0, ''))
            self.server.execute('bossbar set downsub{} max {}'.format(self.randID, plugin_cnt))

            down_index = 0
            self.server.execute('bossbar set downsub{} value 0'.format(self.randID))
            
            for obj in self.downlist['pyplugin']:
                down_index += 1
                self.server.execute('bossbar set downsub{} name "正在下载({}/{})：{}"'.format(self.randID, down_index, plugin_cnt, obj))
                downloadedf = rq.get(self.downlist['pyplugin'][obj]).content
                
                with open('plugins/{}'.format(obj), 'wb') as fobj:
                    fobj.write(downloadedf)
                self.server.execute('bossbar set downsub{} value {}'.format(self.randID, down_index))

            self.server.execute('bossbar remove downsub{}'.format(self.randID))
               
            self.server.execute('bossbar set down{} value 80'.format(self.randID))
            self.server.execute('bossbar set down{} name "(由{}发起)正在重新加载以应用所有更改"'.format(self.randID, self.fromID))
            self.server.execute('reload')
            try:
                self.server._ServerInterface__server.command_manager.reload_plugins(makeInfo())     # reload all plugins # old MCDR version
            except:
                self.server.refresh_all_plugins() # new MCDR version
            # refreshSHA256(self.server) # 重载时会自动刷新
            self.server.execute('bossbar remove down{}'.format(self.randID))

    def show_status(self, info):
        self.server.reply(info, "§l包名:§r§a{}".format(self.packname))

        # show download info
        if self.downlist['datapack']:
            self.server.reply(info, "§l将要下载的数据包：(x{})".format(str(len(self.downlist['datapack']))))
        for dp in self.downlist['datapack']:
            self.server.reply(info, "- {}:§7§n{}".format(dp, self.downlist['datapack'][dp]))
        if self.downlist['pyplugin']:
            self.server.reply(info, "§l将要下载的插件：(x{})".format(str(len(self.downlist['pyplugin']))))
        for dp in self.downlist['pyplugin']:
            self.server.reply(info, "- {}:§7§n{}".format(dp, self.downlist['pyplugin'][dp]))
        if self.needpack:
            self.server.reply(info, "§l将要下载的依赖包：(x{})".format(str(len(self.needpack))))
        for dp in self.needpack:
            self.server.reply(info, "- {}:§7§n{}".format(dp.packname, dp.packlink))
        
        # show remove info
        if self.remove_list['datapack']:
            self.server.reply(info, "§l将要移除的数据包：(x{})".format(str(len(self.remove_list['datapack']))))
        for dp in self.remove_list['datapack']:
            self.server.reply(info, "- {}:§7§n{}".format(dp, self.remove_list['datapack'][dp]))
        if self.remove_list['pyplugin']:
            self.server.reply(info, "§l将要移除的插件：(x{})".format(str(len(self.remove_list['pyplugin']))))
        for dp in self.remove_list['pyplugin']:
            self.server.reply(info, "- {}:§7§n{}".format(dp, self.remove_list['pyplugin'][dp]))
        if self.removepack:
            self.server.reply(info, "§l将要移除的依赖包：(x{})".format(str(len(self.removepack))))
        for dp in self.removepack:
            self.server.reply(info, "- {}:§7§n{}".format(dp.packname, dp.packlink))
        
        self.server.reply(info, format_err_msg('温馨提示：请勿下载来路不明的包，这些插件通常都包含了恶意代码。请务必从可信的平台下载包！'))
        self.server.reply(info, '若要开始，请使用!!bc start')

    def chkupdate(self):
        """
        ### 检查包更新
        True:有更新
        False:无更新
        """
        self.packlink = self.meta['update_link']
        vernow = self.meta['packversion']
        self.from_cloud(self.packlink)
        
        return vernow < self.version

    def remove_init(self, name, mode=0):
        """
        ### 移除包
        - mode=1:完全移除
        - mode=0:只移除此包和依赖此包的包
        """
        self.removepack.append(self)
        self.removepack_name.append(self.packname)
        if self.isroot:
            self.server.execute('bossbar add rmp{} "(由{}发起)正在准备移除{}"'.format(self.randID, self.fromID, self.packlink))
            self.server.execute('bossbar set rmp{} color green'.format(self.randID))
            self.server.execute('bossbar set rmp{} players @a'.format(self.randID))

        self.from_local(name)

    def __cloud_data_init(self):
        self.version = self.meta['packversion']
        self.childPacks = self.meta['child_plugins']
        self.packname = self.meta['packname']
        self.needpack_name.append(str(self.packname))
        # print(self.needpack_name) #debug
        self.needpack = self.needpack+[
            Pack(self.server, self.fromID, False, 
                 self.downlist, self.remove_list, self.needpack, self.needpack_name, self.removepack).from_cloud(lib['meta'])
            for lib in self.meta['lib']
        ]

        try:
            while True:
                self.needpack.remove(None)
        except:
            pass

        for lib in self.meta['downloads']['datapack']:
            self.downlist['datapack'][lib] = self.meta['downloads']['datapack'][lib]
            self.server.logger.info('下载数据包文件源添加: {}'.format(self.downlist['datapack'][lib]))
        for lib in self.meta['downloads']['pyplugin']:
            self.downlist['pyplugin'][lib] = self.meta['downloads']['pyplugin'][lib]
            self.server.logger.info('下载插件文件源添加: {}'.format(self.downlist['pyplugin'][lib]))

        self.server.logger.info('下载文件信息：{}'.format(str(self.downlist)))

    def __local_data_init(self):
        self.version = self.meta['packversion']
        self.childPacks = self.meta['child_plugins']
        self.packname = self.meta['packname']
        self.removepack_name.append(str(self.packname))
        if not self.isroot:
            if self.meta['packname'] in self.removepack_name:     # check if tp
                self.server.logger.info('已剔除重复包: {}'.format(self.meta['packname']))
                return


        self.removepack = self.removepack+[
            Pack(self.server, self.fromID, False, 
                 self.downlist, self.remove_list, self.needpack, self.needpack_name, self.removepack).from_local(pack)
            for pack in self.childPacks
        ]

        try:
            while True:
                self.needpack.remove(None)
        except:
            pass

        for lib in self.meta['downloads']['datapack']:
            self.remove_list['datapack'][lib] = self.meta['downloads']['datapack'][lib]
            self.server.logger.info('添加了将要移除的文件: {}'.format(self.downlist['datapack'][lib]))
        for lib in self.meta['downloads']['pyplugin']:
            self.remove_list['pyplugin'][lib] = self.meta['downloads']['pyplugin'][lib]
            self.server.logger.info('添加了将要移除的文件: {}'.format(self.downlist['pyplugin'][lib]))

        self.server.logger.info('移除文件信息{}'.format(str(self.downlist)))
        

    def __del__(self):
        self.server.execute('bossbar remove getmeta{}'.format(self.randID))
        self.server.execute('bossbar remove downsub{}'.format(self.randID))
        self.server.execute('bossbar remove down{}'.format(self.randID))
