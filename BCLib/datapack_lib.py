'''
# datapack_lib

'''
import threading as thd
import time
from datetime import datetime

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


def get_date(server):
    server.execute("scoreboard objectives add bc_date dummy")

    while True:
        d = datetime.today()

        server.execute("scoreboard players set #year bc.date " + str(d.year))
        server.execute("scoreboard players set #month bc.date " + str(d.month))
        server.execute("scoreboard players set #day bc.date " + str(d.day))
        server.execute("scoreboard players set #hour bc.date " + str(d.hour))
        server.execute("scoreboard players set #minute bc.date " + str(d.minute))
        server.execute("scoreboard players set #second bc.date " + str(d.second))
        server.execute("scoreboard players set #week bc.date " + str(d.isoweekday()))
        time.sleep(1)
