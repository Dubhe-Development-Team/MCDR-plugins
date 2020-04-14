import requests as rq
import random as rand
import json,os

class Pack():
    def __init__(self,meta_link,server,isroot=True,downlist=[],needpack=[]):
        metafile = rq.get(meta_link,timeout=60)
        self.isroot = isroot
        self.meta = metafile.json()
        self.downlist = downlist # 传递引用，使所有嵌套共用一个列表，以便管理
        self.needpack = needpack

        self.downlist = []
        self.needpack = [Pack(lib['meta'],server,False) for lib in self.meta['lib']]