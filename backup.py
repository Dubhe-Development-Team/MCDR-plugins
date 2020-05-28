import os, shutil, zipfile, re
from time import sleep
import time

VERSION = "v1.0"

global bkup, config_file, backup_file, server_file, auto_time, autotime, auto_judge, backup, gara, backtime, backupname, stop
bkup = False
config_file = "plugins/backup_config.yml"
backup_file = ""
server_file = ""
auto_time = 15
auto_judge = False
backup = []
gara = False
backtime = 0
autotime = 0
backupname = "null"
stop = False
"""
备份
屏蔽特殊字符
list回档,confirm
删档
重命名
自动备份
时间区重置
"""


def debug(server, info):
    global bkup, config_file, backup_file, server_file, auto_time, auto_judge
    server.tell(info.player, ' 备份状态 ：' + str(bkup))
    server.tell(info.player, ' 配置目录 ：' + str(config_file))
    server.tell(info.player, ' 备份目录 ：' + str(backup_file))
    server.tell(info.player, '服务器目录：' + str(server_file))
    server.tell(info.player, ' 备份间隔 ：' + str(auto_time))
    server.tell(info.player, ' 自动备份 ：' + str(auto_judge))


def on_load(server, old_module):
    global config_file
    server.logger.info("服务器备份 {}".format(VERSION))
    server.add_help_message("!!backup help", "备份帮助菜单")
    # 如果配置文件不存在就生成一个新的
    if not os.path.exists(config_file):
        f = open(config_file, "a+")
        f.write("# the backup file\n")
        f.write("file: backup\n")
        f.close()
    getpath()
    sleep(1)
    if backup_file == "":
        f = open(config_file, "a+")
        f.write("# the backup file\n")
        f.write("file: backup\n")
        f.close()
        getpath()
        sleep(1)
    # 判断备份文件夹是否存在，不存在就生成一个
    if not os.path.exists(backup_file):
        os.makedirs(backup_file)


def on_server_startup(server):
    bktime()


def on_mcdr_stop(server):
    global stop
    stop = True


def on_info(server, info):
    global bkup, auto_time, auto_judge, backupname, gara
    if info.content.startswith('!!backup'):
        args = info.content.split(' ')
        if args[0] == '!!backup':
            if server.get_permission_level(info) >= 2:
                if len(args) == 1:
                    server.tell(info.player, "§r[Backup] 使用!!backup help获取备份帮助菜单")
                elif len(args) == 2 and args[1] == "help":
                    backup_help_msg(server, info)
                elif len(args) == 2 and args[1] == "auto":
                    autobackuplist(server, info)
                elif len(args) == 2 and args[1] == "debug":
                    debug(server, info)
                else:
                    if not bkup:
                        if len(args) == 2 and args[1] == "back":
                            listbackup(server, info)
                        elif len(args) == 3 and args[1] == "add":
                            if re.match("^[A-Za-z0-9_]{1,20}$", args[2]):
                                addbackup(server, info, args[2])
                            else:
                                server.tell(info.player, "§r[Backup] 请使用字母、数字、下划线命名，并且长度不要超过20")
                        elif len(args) == 3 and args[1] == "remove":
                            if re.match("^[A-Za-z0-9_]{1,20}$", args[2]):
                                removebackup(server, info, args[2])
                            else:
                                server.tell(info.player, "§r[Backup] 请使用字母、数字、下划线命名，并且长度不要超过20")
                        elif len(args) == 3 and args[1] == "back":
                            if re.match("^[A-Za-z0-9_]{1,20}$", args[2]):
                                server.tell(info.player, "§r[Backup] 请在5秒内再次点击回档")
                                if backupname == "null":
                                    backupname = args[2]
                                    backbackup(server, args[2])
                                elif args[2] == backupname:
                                    backupname = "null"
                                    backbackup(server, args[2])
                                else:
                                    backupname = args[2]
                                    gara = False
                                    backbackup(server, args[2])
                            else:
                                server.tell(info.player, "§r[Backup] 请使用字母、数字、下划线命名，并且长度不要超过20")
                        elif len(args) == 3 and args[1] == "auto":
                            if args[2] == "on":
                                auto_judge = True
                            elif args[2] == "off":
                                auto_judge = False
                            elif args[2].isdecimal():
                                if 1 <= int(args[2]) <= 30:
                                    if auto_judge == 1:
                                        auto_time = int(args[2])
                                    else:
                                        server.tell(info.player, "§r[Backup] 请先启动自动备份")
                                elif int(args[2]) < 1:
                                    server.tell(info.player, "§r[Backup] 数太小了！")
                                elif int(args[2]) > 30:
                                    server.tell(info.player, "§r[Backup] 数太大了！")
                            else:
                                server.tell(info.player, '§r[Backup] 输入无效')
                        elif len(args) == 4 and args[1] == "rename":
                            if re.match("^[A-Za-z0-9_]{1,20}$", args[2]) and re.match("^[A-Za-z0-9_]{1,20}$", args[3]):
                                renamebackup(server, info, args[2], args[3])
                            else:
                                server.tell(info.player, "§r[Backup] 请使用字母、数字、下划线命名，并且长度不要超过20")
                        else:
                            server.tell(info.player, '§r[Backup] 输入无效')
                    else:
                        server.tell(info.player, "§r[Backup] §4上一个操作还没结束！")
            else:
                server.tell(info.player, "§r[Backup] 你没有权限执行此操作")


def bktime():
    global backtime, autotime, gara, stop
    while True:
        if stop:
            return
        backtime += 1
        autotime += 1
        if backtime >= 5:
            backup_time = 5
            gara = False
        if autotime >= 120:
            autotime = 120
        sleep(1)


def backup_help_msg(server, info):
    help_msg = """
§2#########################################################§r
§7!!backup help                         §r显示此菜单
§7!!backup add [name]                    §r添加备份
§7!!backup remove [name]                 §r删除备份
§7!!backup rename [oldname] [newname]     §r重命名备份
§7!!backup back                         §r回档
§7!!backup auto <on/off/[time]>           §r自动备份(分钟)
§c注§7： §b[name]§r仅可使用字母、数字、下划线       §b< >§r可不填
§2#########################################################§r"""
    server.tell(info.player, help_msg)


def addbackup(server, info, name):
    global bkup, backup_file, server_file
    bkup = True
    if not os.path.exists(os.path.join(backup_file, name + ".zip")):
        server.say('§r[Backup] §9开始备份服务器……')
        server.execute("save-all")
        sleep(3)
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
        server.say('§r[Backup] §9备份完成')
    else:
        server.tell(info.player, '§r[Backup] §e已存在名为§b ' + name + ' §e的备份文件')
    bkup = False


def removebackup(server, info, name):
    global bkup, backup_file
    bkup = True
    if os.path.exists(os.path.join(backup_file, name + ".zip")):
        server.tell(info.player, '§r[Backup] 删除备份文件中')
        os.remove(os.path.join(backup_file, name + ".zip"))
        server.tell(info.player, '§r[Backup] 删除完成')
    else:
        server.tell(info.player, '§r[Backup] §5未找到名为§b ' + name + ' §5的备份文件')
    bkup = False


def listbackup(server, info):
    global bkup, backup_file, backup
    for filename in os.listdir(backup_file):
        if filename[-4:] == ".zip":
            backup.append(filename[:-4])
    if not backup:
        server.tell(info.player, '§r[Backup] 没有可回档文件')
    else:
        server.tell(info.player, '§r[Backup] 获取中......')
        for i in backup:
            server.execute('tellraw ' + info.player + ' [{"text":"["},{"text":"' + i +
                           '","color":"dark_green","clickEvent":{"action":"run_command","value":"!!backup back ' + i +
                           '"},"hoverEvent":{"action":"show_text","value":[{"text":"点我恢复此存档"}]}},{"text":"]"}]')
            sleep(0.5)


def backbackup(server, name):
    global backup_file, server_file, bkup, backup, gara, backtime
    if not gara:
        gara = True
        backtime = 0
    else:
        gara = False
        bkup = True
        if os.path.exists(os.path.join(backup_file, name + ".zip")):
            server.stop()
            while True:
                if not server.is_server_running():
                    filelist = os.listdir(server_file)
                    for f in filelist:
                        filepath = os.path.join(server_file, f)
                        if os.path.isfile(filepath):
                            os.remove(filepath)
                        elif os.path.isdir(filepath):
                            shutil.rmtree(filepath, True)
                    sleep(1)
                    fz = zipfile.ZipFile(os.path.join(backup_file, name + ".zip"), 'r')
                    for file in fz.namelist():
                        fz.extract(file, server_file)
                    server.logger.info("回档完成")
                    sleep(0.5)
                    server.logger.info("正在启动服务器")
                    server.start()
                    bkup = False
                    return
                sleep(1)


def renamebackup(server, info, oldname, newname):
    global bkup, backup_file
    bkup = True
    if os.path.exists(os.path.join(backup_file, oldname + ".zip")):
        os.rename(os.path.join(backup_file, oldname + ".zip"), os.path.join(backup_file, newname + ".zip"))
        server.tell(info.player, '§r[Backup] 完成')
    else:
        server.tell(info.player, '§r[Backup] §5未找到名为§b ' + oldname + ' §5的备份文件')
    bkup = False


def autobackup(server, info):
    global auto_time, autotime, auto_judge, stop
    while True:
        if stop:
            return
        if auto_judge:
            if autotime >= auto_time * 60:
                addbackup(server, info, time.strftime("%Y%m%d%H%M%S", time.localtime()))
                autotime = 0
        sleep(1)


def autobackuplist(server, info):
    global auto_time, auto_judge
    server.tell(info.player, '自动备份：' + str(auto_judge))
    server.tell(info.player, '备份间隔：' + str(auto_time))


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
