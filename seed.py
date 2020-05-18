VERSION = "v1.5"


def on_load(server, old_module):
    server.logger.info("种子获取 {}".format(VERSION))
    server.add_help_message("!!seed", "获取服务器种子")


def on_info(server, info):
    if info.is_user:
        if info.content.startswith('!!seed'):
            if server.get_permission_level(info) >= 2:
                args = info.content.split(' ')
                if args[0] == '!!seed':
                    if len(args) == 1:
                        server.execute("seed")
                    else:
                        server.tell(info.player, '输入无效')
            else:
                server.tell(info.player, "你没有权限执行此操作")
    elif info.content.startswith('Seed'):
        seed = info.content[7:-1]
        server.execute('tellraw @a [{"text":"世界种子为： ["},{"text":"' + seed
                       + '","color":"dark_green","underlined":"true","clickEvent":{"action":"copy_to_clipboard","value":"'
                       + seed + '"},"hoverEvent":{"action":"show_text","value":[{"text":"点我复制种子到剪切板"}]}},{"text":"]"}]')
