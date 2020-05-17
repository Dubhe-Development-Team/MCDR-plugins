from time import sleep
VERSION = "v1.0"


def on_load(server, old_module):
    server.logger.info("服务器控制 {}".format(VERSION))

    server.add_help_message("!!server help", "服务器管理帮助")
    server.add_help_message("!!tps help", "tps帮助菜单")


def on_info(server, info):
    if info.is_user:
        if info.content.startswith('!!tps'):
            args = info.content.split(' ')
            if args[0] == '!!tps':
                if len(args) == 1:
                    server.execute('debug start')
                    sleep(1)
                    server.execute('debug stop')
                elif len(args) == 2 and args[1] == 'help':
                    server.tell(info.player, '\n§2#§r      §7!!tps [秒数]  §r指定获取多少秒内的tps    §2#§r\n')
                elif len(args) == 2 and args[1].isdigit() and 1.0 <= float(args[1]) <= 60:
                    server.execute('debug start')
                    sleep(float(args[1]))
                    server.execute('debug stop')
                elif len(args) == 2 and args[1].isdigit() and float(args[1]) < 1.0:
                    server.tell(info.player, '数太小了!')
                elif len(args) == 2 and args[1].isdigit() and float(args[1]) > 60:
                    server.tell(info.player, '你想获取多久？')
                else:
                    server.tell(info.player, '输入无效')

        if info.content.startswith('!!server'):
            args = info.content.split(' ')
            if args[0] == '!!server':
                if server.get_permission_level(info) >= 2:
                    if len(args) == 1:
                        server.tell(info.player, '请输入!!server help 查看帮助菜单')
                    elif len(args) == 2:
                        if args[1] == 'help':
                            show_help_msg(server, info)
                        elif args[1] == 'stop':
                            server.stop_exit()
                        elif args[1] == 'restart':
                            server.restart()
                        else:
                            server.tell(info.player, '输入无效')
                    else:
                        server.tell(info.player, '输入无效')
                else:
                    server.tell(info.player, "你没有权限执行此操作")
    elif info.content.startswith('Stopped debug profiling after'):
        server.say(info.content.replace('Stopped debug profiling after ', '', 1))


def show_help_msg(server, info):
    help_msg = """
§2###############################################§r
§7!!server help       §r显示此菜单
§7!!server stop       §r关闭服务器
§7!!server restart    §r重启服务器
§2###############################################§r"""
    server.tell(info.player, help_msg)
