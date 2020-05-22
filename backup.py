import os, shutil, zipfile, re
from time import sleep
VERSION = "v1.0"

global bkup, config_file, backup_file, server_file, auto_time, auto_judge
bkup = False
config_file = "plugin/backup_config.yml"
backup_file = ""
server_file = ""
"""
屏蔽特殊字符
list回档,confirm
删档
重命名
自动备份
"""


def on_load(server, old_module):
    global config_file
    server.logger.info("服务器备份 {}".format(VERSION))
    server.add_help_message("!!backup help", "备份帮助菜单")
    # 如果配置文件不存在就生成一个新的
    if not os.path.exists(config_file):
        f = open(config_file, "a")
        f.write("# the backup file\n")
        f.write("file: backup\n")
        f.close()
    getpath()
    sleep(1)
    if backup_file == "":
        f = open(config_file, "a")
        f.write("# the backup file\n")
        f.write("file: backup\n")
        f.close()
        getpath()
        sleep(1)
    # 判断备份文件夹是否存在，不存在就生成一个
    if not os.path.exists(backup_file):
        os.makedirs(backup_file)


def on_info(server, info):
    global bkup, auto_time, auto_judge
    if info.content.startswith('!!backup'):
        args = info.content.split(' ')
        if args[0] == '!!backup':
            if server.get_permission_level(info) >= 2:
                if len(args) == 1:
                    server.tell(info.player, "使用!!backup help获取备份帮助菜单")
                elif len(args) == 2 and args[1] == "help":
                    backup_help_msg(server, info)
                else:
                    if not bkup:
                        if len(args) == 2 and args[1] == "back":
                            backbackup(server, info)
                        elif len(args) == 3 and args[1] == "add":
                            if re.match("^[A-Za-z0-9_]*$", args[2]):
                                addbackup(server, info, args[2])
                            else:
                                server.tell(info.player, "请使用字母、数字、下划线命名")
                        elif len(args) == 3 and args[1] == "remove":
                            if re.match("^[A-Za-z0-9_]*$", args[2]):
                                removebackup(server, info, args[2])
                            else:
                                server.tell(info.player, "请使用字母、数字、下划线命名")
                        elif len(args) == 3 and args[1] == "auto":
                            if args[2] == "on":
                                auto_judge = 1
                            elif args[2] == "off":
                                auto_judge = 0
                            elif args[2].isdecimal():
                                if 1 <= int(args[2]) <= 30:
                                    auto_time = int(args[2])
                                elif int(args[2]) < 1:
                                    server.tell(info.player, "数太小了！")
                                elif int(args[2]) > 30:
                                    server.tell(info.player, "数太大了！")
                            else:
                                server.tell(info.player, '输入无效')
                        elif len(args) == 4 and args[1] == "rename":
                            if re.match("^[A-Za-z0-9_]*$", args[2]) and re.match("^[A-Za-z0-9_]*$", args[3]):
                                renamebackup(server, info, args[2], args[3])
                            else:
                                server.tell(info.player, "请使用字母、数字、下划线命名")
                        else:
                            server.tell(info.player, '输入无效')
                    else:
                        server.tell(info.player, "§4上一个操作还没结束！")
            else:
                server.tell(info.player, "你没有权限执行此操作")


def backup_help_msg(server, info):
    help_msg = """
§2####################################################§r
§7!!backup help                         §r显示此菜单
§7!!backup add [name]                   §r添加备份
§7!!backup remove [name]                §r删除备份
§7!!backup rename [oldname] [newname]   §r重命名备份
§7!!backup back                         §r回档
§7!!backup auto <on/off/[time]>         §r自动备份(分钟)
§c注§7： §b[name]§r仅可使用字母、数字、下划线       §b< >§r可不填
§2####################################################§r"""
    server.tell(info.player, help_msg)


def addbackup(server, info, name):
    global bkup, backup_file, server_file
    bkup = True
    if not os.path.exists(os.path.join(backup_file, name + ".zip")):
        server.say('§r[server] §9开始备份服务器……')
        f = zipfile.ZipFile(name + '.zip', 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(server_file):
            fpath = dirpath.replace(server_file, '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                if filename == "session.lock":
                    continue
                f.write(os.path.join(dirpath, filename), fpath + filename)
        f.close()
        shutil.move(os.path.join(os.getcwd(), name + ".zip"), os.path.join(os.getcwd(), backup_file))
        server.say('§r[server] §9备份完成')
    else:
        server.tell(info.player, '§e已存在名为§b ' + name + ' §e的备份文件')
    bkup = False


def removebackup(server, info, name):
    pass


def backbackup(server, info):
    pass


def renamebackup(server, info, oldname, newname):
    pass


def autobackup(server, info):
    global bkup, auto_time, auto_judge
    pass


def getpath():
    global config_file, backup_file, server_file
    path = ""
    for i in open(config_file, "r").readlines():
        if i[0:4] == "file":
            for j in i[6:-1]:
                if j != "/":
                    path += j
                else:
                    path += "\\"
            backup_file = os.path.join(os.getcwd(), path)
            break
    path = ""
    for i in open("config.yml", "r").readlines():
        if i[0:17] == "working_directory":
            for j in i[19:-1]:
                if j != "/":
                    path += j
                else:
                    path += "\\"
            server_file = os.path.join(os.getcwd(), path)
            break
