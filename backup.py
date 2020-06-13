import os, shutil, zipfile, re, threading, yaml, time
from pathlib import Path

VERSION = "v5.2"
# 初始化全局变量
bkup = False
files = ["config.yml", "plugins/backup_config.yml", "", ""]
auto_time = None
auto_judge = None
times = [0, 10]
bkname = ["null", "null"]
stop = [False, False]


# DEBUG
def debug(server, info):
    if info.is_player:
        server.tell(info.player, ' 备份状态： ' + str(bkup))
        server.tell(info.player, ' 配置目录： ' + str(files[1]))
        server.tell(info.player, ' 备份目录： ' + str(files[2]))
        server.tell(info.player, ' 开服目录： ' + str(files[3]))
        server.tell(info.player, ' 备份间隔： ' + str(auto_time))
        server.tell(info.player, ' 自动备份： ' + str(auto_judge))
        server.tell(info.player, ' 备份计时： ' + str(times[0]))
        server.tell(info.player, ' 回档计时： ' + str(times[1]))
        server.tell(info.player, ' 回档名字： ' + str(bkname[0]))
        server.tell(info.player, ' 回档玩家： ' + str(bkname[1]))
    else:
        server.logger.info(' 备份状态： ' + str(bkup))
        server.logger.info(' 配置目录： ' + str(files[1]))
        server.logger.info(' 备份目录： ' + str(files[2]))
        server.logger.info(' 开服目录： ' + str(files[3]))
        server.logger.info(' 备份间隔： ' + str(auto_time))
        server.logger.info(' 自动备份： ' + str(auto_judge))
        server.logger.info(' 备份计时： ' + str(times[0]))
        server.logger.info(' 回档计时： ' + str(times[1]))
        server.logger.info(' 回档名字： ' + str(bkname[0]))
        server.logger.info(' 回档玩家： ' + str(bkname[1]))


# 首次加载
def on_load(server, old_module):
    server.logger.info("服务器备份 {}".format(VERSION))
    server.add_help_message("!!backup help", "备份帮助菜单")
    # 配置文件不存在就生成一个
    if not os.path.exists(files[1]):
        createyml()
    getyml()
    time.sleep(1)
    # 备份文件夹不存在就生成一个
    if not os.path.exists(files[2]):
        os.makedirs(files[2])


# 服务器启动完成
def on_server_startup(server):
    threading.Thread(target=lambda: bktime(), name="backup: 备份计时服务").start()
    threading.Thread(target=lambda: autobackup(server), name="backup: 自动备份服务").start()


# 服务器关闭
def on_server_stop(server, return_code):
    global stop
    stop = [True, True]


# 标准输入
def on_info(server, info):
    global bkup, auto_time, auto_judge, bkname, times
    # 玩家指令
    if info.is_player:
        if info.content.startswith('!!backup'):
            args = info.content.split(' ')
            if args[0] == '!!backup':
                if server.get_permission_level(info) >= 2:
                    if len(args) == 1:
                        server.tell(info.player, "§r[Backup] 使用 !!backup help 获取备份帮助菜单")
                    elif len(args) == 2 and args[1] == "help":
                        backup_help_msg(server, info)
                    elif len(args) == 2 and args[1] == "auto":
                        autobackuplist(server, info)
                    elif len(args) == 2 and args[1] == "debug":
                        if server.get_permission_level(info) >= 3:
                            debug(server, info)
                        else:
                            server.tell(info.player, "§r[Backup] 权限不足")
                    else:
                        if not bkup:
                            if len(args) == 2 and args[1] == "back":
                                listbackup(server, info)
                            elif len(args) == 2 and args[1] == "confirm":
                                if times[1] < 10 and bkname[1] == info.player:
                                    threading.Thread(target=lambda: backbackup(server, info, bkname[0]), name="backup: 回档服务").start()
                                else:
                                    times[1] = 10
                                    server.tell(info.player, '§r[Backup] 输入无效')
                            elif len(args) == 3 and args[1] == "add":
                                if re.match("^[A-Za-z0-9_]{1,20}$", args[2]):
                                    threading.Thread(target=lambda: addbackup(server, info, args[2]), name="backup: 添加备份服务").start()
                                else:
                                    server.tell(info.player, "§r[Backup] 请使用字母、数字、下划线命名，并且长度不要超过20")
                            elif len(args) == 3 and args[1] == "remove":
                                if re.match("^[A-Za-z0-9_]{1,20}$", args[2]):
                                    threading.Thread(target=lambda: removebackup(server, info, args[2]), name="backup: 删除备份服务").start()
                                else:
                                    server.tell(info.player, "§r[Backup] 请使用字母、数字、下划线命名，并且长度不要超过20")
                            elif len(args) == 3 and args[1] == "back":
                                if re.match("^[A-Za-z0-9_]{1,20}$", args[2]):
                                    bkname[0] = args[2]
                                    bkname[1] = info.player
                                    times[1] = 0
                                    server.tell(info.player, "§r[Backup] 请在10秒内输入 !!backup confirm 确认回档")
                                else:
                                    server.tell(info.player, "§r[Backup] 请使用字母、数字、下划线命名，并且长度不要超过20")
                            elif len(args) == 3 and args[1] == "auto":
                                if args[2] == "on":
                                    auto_judge = True
                                    changeyml("auto_backup", "True")
                                    server.tell(info.player, "§r[Backup] 已开启自动备份")
                                elif args[2] == "off":
                                    auto_judge = False
                                    changeyml("auto_backup", "False")
                                    server.tell(info.player, "§r[Backup] 已关闭自动备份")
                                elif args[2].isdecimal():
                                    if 1 <= int(args[2]) <= 60:
                                        if auto_judge == 1:
                                            auto_time = int(args[2])
                                            changeyml("auto_backup_time", int(args[2]))
                                            times[0] = 0
                                            server.tell(info.player, '§r[Backup] 已将自动备份间隔改为 {} 分钟'.format(args[2]))
                                        else:
                                            server.tell(info.player, "§r[Backup] 请先启动自动备份")
                                    elif int(args[2]) < 1:
                                        server.tell(info.player, "§r[Backup] 数太小了！")
                                    elif int(args[2]) > 60:
                                        server.tell(info.player, "§r[Backup] 数太大了！")
                                else:
                                    server.tell(info.player, '§r[Backup] 输入无效')
                            elif len(args) == 4 and args[1] == "rename":
                                if re.match("^[A-Za-z0-9_]{1,20}$", args[2]) and re.match("^[A-Za-z0-9_]{1,20}$", args[3]):
                                    threading.Thread(target=lambda: renamebackup(server, info, args[2], args[3]), name="backup: 重命名备份服务").start()
                                else:
                                    server.tell(info.player, "§r[Backup] 请使用字母、数字、下划线命名，并且长度不要超过20")
                            else:
                                server.tell(info.player, '§r[Backup] 输入无效')
                        else:
                            server.tell(info.player, "§r[Backup] §4上一个操作还没结束！")
                else:
                    server.tell(info.player, "§r[Backup] 你没有权限执行此操作")
    # 后台指令
    else:
        if info.content.startswith('!!backup'):
            args = info.content.split(' ')
            if args[0] == '!!backup':
                if server.is_server_running():
                    if len(args) == 1:
                        server.logger.info("§r[Backup] 使用 !!backup help 获取备份帮助菜单")
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
                            elif len(args) == 2 and args[1] == "confirm":
                                if times[1] < 10 and bkname[1] == "#console":
                                    threading.Thread(target=lambda: backbackup(server, info, bkname[0]), name="backup: 回档服务").start()
                                else:
                                    times[1] = 10
                                    server.logger.info("§r[Backup] 输入无效")
                            elif len(args) == 3 and args[1] == "add":
                                if re.match("^[A-Za-z0-9_]{1,20}$", args[2]):
                                    threading.Thread(target=lambda: addbackup(server, info, args[2]), name="backup: 新建备份服务").start()
                                else:
                                    server.logger.info("§r[Backup] 请使用字母、数字、下划线命名，并且长度不要超过20")
                            elif len(args) == 3 and args[1] == "remove":
                                if re.match("^[A-Za-z0-9_]{1,20}$", args[2]):
                                    threading.Thread(target=lambda: removebackup(server, info, args[2]), name="backup: 删除备份服务").start()
                                else:
                                    server.logger.info("§r[Backup] 请使用字母、数字、下划线命名，并且长度不要超过20")
                            elif len(args) == 3 and args[1] == "back":
                                if re.match("^[A-Za-z0-9_]{1,20}$", args[2]):
                                    bkname[0] = args[2]
                                    bkname[1] = "#console"
                                    times[1] = 0
                                    server.logger.info("§r[Backup] 请在10秒内输入 !!backup confirm 确认回档")
                                else:
                                    server.logger.info("§r[Backup] 请使用字母、数字、下划线命名，并且长度不要超过20")
                            elif len(args) == 3 and args[1] == "auto":
                                if args[2] == "on":
                                    auto_judge = True
                                    changeyml("auto_backup", "True")
                                    server.logger.info("§r[Backup] 已开启自动备份")
                                elif args[2] == "off":
                                    auto_judge = False
                                    changeyml("auto_backup", "False")
                                    server.logger.info("§r[Backup] 已关闭自动备份")
                                elif args[2].isdecimal():
                                    if 1 <= int(args[2]) <= 60:
                                        if auto_judge == 1:
                                            auto_time = int(args[2])
                                            changeyml("auto_backup_time", int(args[2]))
                                            times[0] = 0
                                            server.logger.info('§r[Backup] 已将自动备份间隔改为 {} 分钟'.format(args[2]))
                                        else:
                                            server.logger.info("§r[Backup] 请先启动自动备份")
                                    elif int(args[2]) < 1:
                                        server.logger.info("§r[Backup] 数太小了！")
                                    elif int(args[2]) > 60:
                                        server.logger.info("§r[Backup] 数太大了！")
                                else:
                                    server.logger.info("§r[Backup] 输入无效")
                            elif len(args) == 4 and args[1] == "rename":
                                if re.match("^[A-Za-z0-9_]{1,20}$", args[2]) and re.match("^[A-Za-z0-9_]{1,20}$", args[3]):
                                    threading.Thread(target=lambda: renamebackup(server, info, args[2], args[3]), name="backup: 重命名备份服务").start()
                                else:
                                    server.logger.info("§r[Backup] 请使用字母、数字、下划线命名，并且长度不要超过20")
                            else:
                                server.logger.info("§r[Backup] 输入无效")
                        else:
                            server.logger.info("§r[Backup] §4上一个操作还没结束！")

                else:
                    server.logger.info("服务器还未启动完成!")


# 备份计时器
def bktime():
    global times, bkname, stop
    while True:
        if stop[0]:
            stop[0] = False
            return
        times[0] += 1
        times[1] += 1
        if times[0] >= 3600:
            times[0] = 3600
        if times[1] >= 10:
            times[1] = 10
            bkname = ["null", "null"]
        time.sleep(1)


# 备份帮助菜单
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
    if info.is_player:
        server.tell(info.player, help_msg)
    else:
        server.logger.info(help_msg)


# 新建备份
def addbackup(server, info, name):
    global bkup, times
    bkup = True
    times[0] = 0
    if not os.path.exists(os.path.join(files[2], name + ".zip")):
        server.say('§r[Backup] §9开始备份服务器……')
        server.logger.info('§r[Backup] §9开始备份服务器……')
        server.execute("save-all")
        time.sleep(3)
        f = zipfile.ZipFile(name + '.zip', 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(files[3]):
            fpath = dirpath.replace(files[3], '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                if filename == "session.lock":
                    continue
                f.write(os.path.join(dirpath, filename), fpath + filename)
        f.close()
        shutil.move(os.path.join(os.getcwd(), name + ".zip"), os.path.join(os.getcwd(), files[2]))
        times[0] = 0
        server.say('§r[Backup] §9备份完成')
        server.logger.info('§r[Backup] §9备份完成')
    else:
        if info.is_player:
            server.tell(info.player, '§r[Backup] §e已存在名为§b {} §e的备份文件'.format(name))
        else:
            server.logger.info('§r[Backup] §e已存在名为§b {} §e的备份文件'.format(name))
    bkup = False


# 删除备份
def removebackup(server, info, name):
    global bkup
    bkup = True
    if os.path.exists(os.path.join(files[2], name + ".zip")):
        if info.is_player:
            server.tell(info.player, '§r[Backup] 删除备份文件中...')
            os.remove(os.path.join(files[2], name + ".zip"))
            server.tell(info.player, '§r[Backup] 删除完成')
        else:
            server.logger.info("§r[Backup] 删除备份文件中...")
            os.remove(os.path.join(files[2], name + ".zip"))
            server.logger.info("§r[Backup] 删除完成")
    else:
        if info.is_player:
            server.tell(info.player, '§r[Backup] §5未找到名为§b {} §e的备份文件'.format(name))
        else:
            server.logger.info('§r[Backup] §5未找到名为§b {} §e的备份文件'.format(name))
    bkup = False


# 备份列表
def listbackup(server, info):
    backup = []
    for filename in os.listdir(files[2]):
        if filename[-4:] == ".zip":
            backup.append(filename[:-4])
    if not backup:
        if info.is_player:
            server.tell(info.player, '§r[Backup] 没有可回档文件')
        else:
            server.logger.info('§r[Backup] 没有可回档文件')
    else:
        if info.is_player:
            server.tell(info.player, '§r[Backup] 获取中......')
            for i in backup:
                server.execute('tellraw {a} [{{"text":"[Backup] ["}},{{"text":"{b}","color":"dark_green","clickEvent":{{"action":"run_command","value":"!!backup back {b}"}},"hoverEvent":{{"action":"show_text","value":[{{"text":"点我恢复此存档"}}]}}}},{{"text":"]"}}]'.format(a=info.player, b=i))
                time.sleep(0.5)
            server.tell(info.player, '§r[Backup] 获取完成，点击存档名进行回档!')
        else:
            server.logger.info('§r[Backup] 获取中......')
            for i in backup:
                server.logger.info('§r[Backup] [§2{}§r]'.format(i))
                time.sleep(0.5)
            server.logger.info('§r[Backup] 获取完成，输入!!backup back [name] 回档!')


# 回档
def backbackup(server, info, name):
    global bkup, times
    bkup = True
    times[1] = 10
    addbackup(server, info, time.strftime("%Y%m%d%H%M%S", time.localtime()))
    if os.path.exists(os.path.join(files[2], name + ".zip")):
        server.stop()
        while True:
            if not server.is_server_running():
                time.sleep(0.5)
                server.logger.info('§r[Backup] 正在删除原服务端......')
                filelist = os.listdir(files[3])
                for f in filelist:
                    filepath = os.path.join(files[3], f)
                    if os.path.isfile(filepath):
                        os.remove(filepath)
                    elif os.path.isdir(filepath):
                        shutil.rmtree(filepath, True)
                server.logger.info('§r[Backup] 删除完成')
                time.sleep(1)
                server.logger.info('§r[Backup] 正在解压备份......')
                fz = zipfile.ZipFile(os.path.join(files[2], name + ".zip"), 'r')
                for file in fz.namelist():
                    fz.extract(file, files[3])
                server.logger.info("解压完成")
                time.sleep(0.5)
                server.logger.info("回档完成")
                time.sleep(0.5)
                server.start()
                bkup = False
                return
            time.sleep(1)
    else:
        if info.is_player:
            server.tell(info.player, '§r[Backup] §5未找到名为§b {} §e的备份文件'.format(name))
        else:
            server.logger.info('§r[Backup] §5未找到名为§b {} §e的备份文件'.format(name))


# 重命名备份
def renamebackup(server, info, oldname, newname):
    global bkup
    bkup = True
    if os.path.exists(os.path.join(files[2], oldname + ".zip")):
        os.rename(os.path.join(files[2], oldname + ".zip"), os.path.join(files[2], newname + ".zip"))
        if info.is_player:
            server.tell(info.player, '§r[Backup] 完成')
        else:
            server.logger.info("§r[Backup] 完成")
    else:
        if info.is_player:
            server.tell(info.player, '§r[Backup] §5未找到名为§b {} §5的备份文件'.format(oldname))
        else:
            server.logger.info('§r[Backup] §5未找到名为§b {} §5的备份文件'.format(oldname))
    bkup = False


# 自动备份
def autobackup(server):
    global stop
    while True:
        if stop[1]:
            stop[1] = False
            return
        if auto_judge and times[0] >= auto_time * 60 and not bkup:
            server.say("开始自动备份!")
            server.logger.info('开始自动备份!')
            threading.Thread(target=lambda: addbackup(server, None, time.strftime("%Y%m%d%H%M%S", time.localtime())), name="backup: 新建备份服务").start()
        time.sleep(1)


# 自动备份状态
def autobackuplist(server, info):
    if info.is_player:
        server.tell(info.player, '自动备份：' + str(auto_judge))
        server.tell(info.player, '备份间隔：' + str(auto_time))
    else:
        server.logger.info('自动备份：' + str(auto_judge))
        server.logger.info('备份间隔：' + str(auto_time))


# 获取配置文件
def getyml():
    global files, auto_time, auto_judge
    # 读 MCDR config 配置文件
    with open(files[0], 'r', encoding="utf-8") as f:
        yml = yaml.load(f.read(), Loader=yaml.FullLoader)
    files[3] = yml["working_directory"]
    # 读 backup_config 配置文件
    with open(files[1], 'r', encoding="utf-8") as f:
        yml = yaml.load(f.read(), Loader=yaml.FullLoader)
    files[2] = Path()/yml["file"]
    auto_time = int(yml["auto_backup_time"])
    if yml["auto_backup"].lower() == "true":
        auto_judge = True
    elif yml["auto_backup"].lower() == "false":
        auto_judge = False


# 创建配置文件
def createyml():
    with open(files[1], "a+") as f:
        f.write('# the backup file\n')
        f.write('# [Default: backup]\n')
        f.write('file: backup\n\n')
        f.write('# Whether to allow auto backup\n')
        f.write('# true to allow\n')
        f.write('# false to refuse\n')
        f.write('# [Default: false]\n')
        f.write('auto_backup: false\n\n')
        f.write('# The auto backup interbal\n')
        f.write('# need to set "auto_backup: true"\n')
        f.write('# The time should a int type\n')
        f.write('# The time should more than or equal to 1\n')
        f.write('# The time should less than or equal to 60\n')
        f.write('# [Default: 15]\n')
        f.write('auto_backup_time: 15\n')


# 更改配置文件
def changeyml(key, value):
    with open(files[1], 'r', encoding="utf-8") as f:
        lines = f.readlines()
    with open(files[1], 'w', encoding='utf-8') as f:
        for line in lines:
            if line.startswith("#"):
                f.write(line)
            else:
                leftstr = line.split(":")[0]
                if key == leftstr:
                    f.write("{}: {}\n".format(leftstr, value))
                else:
                    f.write(line)
