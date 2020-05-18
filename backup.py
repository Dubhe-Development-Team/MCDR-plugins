import os, shutil, zipfile
VERSION = "v1.0"

global bkup
bkup = False


def on_load(server, old_module):
    server.logger.info("服务器备份 {}".format(VERSION))
    server.add_help_message("!!backup", "备份帮助菜单")


def on_info(server, info):
    global bkup
    if info.content.startswith('!!backup'):
        args = info.content.split(' ')
        if args[0] == '!!backup':
            if not bkup:
                if server.get_permission_level(info) >= 2:
                    if len(args) == 1:
                        backup_help_msg(server, info)
                    elif len(args) == 2:
                        backup(server, info, args[1])
                    else:
                        server.tell(info.player, '输入无效')
                else:
                    server.tell(info.player, "你没有权限执行此操作")
            else:
                server.tell(info.player, "§4上一个备份还没结束！")


def backup_help_msg(server, info):
    help_msg = """
§2###############################################§r
§7!!backup [name]       §r备份服务器
§2###############################################§r"""
    server.tell(info.player, help_msg)


def backup(server, info, name):
    global bkup
    bkup = True
    path = ""
    for i in open(os.path.join(os.getcwd(), "config.yml"), "r").readlines():
        if i[0:17] == "working_directory":
            for j in i[19:-1]:
                if j != "/":
                    path += j
                else:
                    path += "\\"
            path = os.path.join(os.getcwd(), path)
            break
    file = "backup/" + name + ".zip"
    if not os.path.exists(file):
        server.say('§r[server] §9开始备份服务器……')
        f = zipfile.ZipFile(name + '.zip', 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(path):
            fpath = dirpath.replace(path, '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                if filename == "session.lock":
                    continue
                f.write(os.path.join(dirpath, filename), fpath + filename)
        f.close()
        shutil.move(os.path.join(os.getcwd(), name + ".zip"), os.path.join(os.getcwd(), "backup"))
        server.say('§r[server] §9备份完成')
    else:
        server.tell(info.player, '§e已存在名为§b ' + name + ' §e的备份文件')
    bkup = False
