'''
# datapack_lib

'''
import threading as thd


global bgSRV
bgSRV = None

def start_srv(server):
    global bgSRV
    bgSRV = thd.Thread(target=lambda:dpService(server),name='Datapack_lib服务线程')
    bgSRV.start()

def stop_srv(server):
    global bgSRV
    bgSRV._stop()
    server.logger.info('Datapack_lib服务已终止')


def dpService(server):
    '''数据包辅助服务'''
    server.logger.info('datapack_lib已启动')
    while True:
        pass
        #TODO: service code 