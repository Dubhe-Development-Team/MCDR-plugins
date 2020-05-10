'''
# datapack_lib

'''
import threading as thd


global bgSRV
bgSRV = None
global STOP_SIGN
STOP_SIGN = 0

def start_srv(server):
    global bgSRV
    bgSRV = thd.Thread(target=lambda:dpService(server),name='Datapack_lib服务线程')
    bgSRV.start()


def stop_srv(server):
    global STOP_SIGN
    STOP_SIGN = 1
    


def dpService(server):
    '''数据包辅助服务'''
    server.logger.info('datapack_lib已启动')
    global STOP_SIGN
    while True:
        if STOP_SIGN:return