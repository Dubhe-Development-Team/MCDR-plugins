# -*- coding: utf-8 -*-
# Version 0.3.2
import time
global RESTART_ABORTED
RESTART_ABORTED=False

global IN_RESTARTING
IN_RESTARTING = False

def stop_server(server,delay=15):
	global RESTART_ABORTED
	RESTART_ABORTED = False
	server.execute('title @a times 0 200 0')
	server.execute('title @a subtitle "§b请利用这段时间内暂停手上的工作，准备好关闭。"')
	server.execute('tellraw @a ["",{"text":"服务器将在15秒后关闭"}]')
	for i in range(delay,0,-1):
		#server.logger.info(str("ABORT STATUS:{}".format(str(RESTART_ABORTED))))
		server.execute('title @a title "§e警告！服务器将在§4§l{}秒§r§e后关闭！"'.format(str(i)))
		
		server.logger.info("准备关闭服务器..({}s)".format(str(i)))
		time.sleep(1)
	server.execute('title @a clear')
	server.execute('title @a times 0 200 0')
	server.execute('title @a title "§c正在关闭服务器……"')
	server.execute('title @a subtitle ""')
	server.execute('stop')

def reboot_server(server,delay=15,player="服务器终端"):
	if player==None:
		player='服务器终端'
	global RESTART_ABORTED
	RESTART_ABORTED = False
	server.execute('title @a times 0 200 0')
	server.execute('title @a subtitle "§b请利用这段时间内暂停手上的工作，准备好重启。"')
	server.logger.info("{}秒后服务器将会重新启动，由{}发起".format(str(delay),player))
	server.execute('tellraw @a [{"text":""},{"text":"服务器将在§c§l'+str(delay)+'§r秒后重启(由§c'+player+'§r发起)，请利用这段时间中断手上的工作，准备好重启。若要中断重启，请使用"},{"color":"white","text":"!!restart abort","underlined":true,"clickEvent":{"action":"suggest_command","value":"!!restart abort"}}]')
	for i in range(delay,0,-1):
		if RESTART_ABORTED:
			RESTART_ABORTED = False

			global IN_RESTARTING
			IN_RESTARTING = False

			server.execute('title @a clear')
			server.execute('title @a reset')
			time.sleep(0.1)
			server.execute('title @a subtitle ""')
			server.execute('title @a title "§c服务器重启已终止。"')
			
			return
		#server.logger.info(str("ABORT STATUS:{}".format(str(RESTART_ABORTED))))
		server.execute('title @a title "§e警告！服务器将在§4§l{}秒§r§e后重启！"'.format(str(i)))
		
		server.logger.info("准备重新启动...({}s)".format(str(i)))
		time.sleep(1)
	server.execute('title @a clear')
	server.execute('title @a times 0 200 0')
	server.execute('title @a title "§c正在重新启动服务器……"')
	server.execute('title @a subtitle ""')
	server.restart()
	IN_RESTARTING = False


def on_load(server,a2):
	server.add_help_message('!!reload', '重新加载数据包')
	#server.add_help_message('!!shutdown', '关闭服务器')
	server.add_help_message('!!restart', '重启服务器')

def on_info(server, info):
	global IN_RESTARTING
	if info.content == '!!reload':
		if server.get_permission_level(info) ==None or server.get_permission_level(info) >= 2:
			server.tell(info.player,"正在重新加载...")
			server.say('服务器正在重新加载数据包，可能会出现冻结的情况。请在此时间内停止手上的工作，并等待恢复正常。')
			server.execute('reload')
			server.tell(info.player,"已重新加载！")
		else:
			server.tell(info.player,"§c权限不足")
	if info.content == '!!restart':			
		if server.get_permission_level(info) ==None or server.get_permission_level(info) >= 2:
			if IN_RESTARTING:
				server.logger.info("服务器已在重新启动，无法再次重新启动")
				server.tell(info.player,'§c服务器已经在重新启动！')
				return
			else:
				IN_RESTARTING = True
				reboot_server(server,15,info.player)
		else:
			server.tell(info.player,"§c权限不足")
	if info.content == '!!restart abort':
		if server.get_permission_level(info) ==None or server.get_permission_level(info) >= 2:
			if IN_RESTARTING:
				server.logger.info("重新启动已被终止")
				global RESTART_ABORTED
				RESTART_ABORTED = True
			else:
				if info.player==None:
					server.logger.info('服务器未在重启！')
				else:
					server.tell(info.player,"§c服务器未在重启！")
		else:
			server.tell(info.player,"§c权限不足")
# if server.get_permission_level(info) ==None or server.get_permission_level(info) >= 3:
# 		if info.content == '!!shutdown':
# 			server.logger.info("准备关闭服务器...")
# 			stop_server(server)
