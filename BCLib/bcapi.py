
'''
BridgeCaller API

isInstalled:
    查询插件是否已经安装。可以指定对应版本。如：
        >>>isInstalled('BridgeCaller')
        True

getPackInfo:
    获得指定的包信息。如果包不存在，会返回None。如：
        >>>getPackInfo('BridgeCaller').packname
        'BridgeCaller'
        >>>getPackInfo('pack2')
        None
        
         

'''
def isInstalled(name,version=-1):
    pass

def getPackInfo(name):
    pass