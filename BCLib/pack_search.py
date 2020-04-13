import requests as rq
import random as rand
import json,os

class Pack():
    def __init__(self,meta_link,server,isroot=True):
        metafile = rq.get(meta_link,timeout=60)
        self.isroot = isroot
        self.meta = metafile.json()

        self.downlist = []
        self.needpack = []

        if len(self.meta['lib'])>=0:
            for lib in self.meta['lib']:
                needpack.append(Pack(meta['lib']['meta'],server,False))