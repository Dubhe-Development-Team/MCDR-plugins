# Backup
[English](https://gitee.com/gu_zt666/MCDR-plugins/blob/Backup/README_EN.MD)

> [MCDReforged](https://github.com/Fallen-Breath/MCDReforged) 存档备份插件
>
> 这是一个存档备份插件
>
> 它可以使管理员使用指令备份存档插件

**MCDaemon**

如果您拥有Linux环境并愿意将本插件移植至MCDaemon。

请创建一个Backup-MCD.py，我将很高兴接受Pull requests。

## 使用方法

| 命令 | 功能 | 权限 |
|---|---|---|
| !!backup help | 查看帮助 | helper |
| !!backup add [name] | 添加备份 | helper |
| !!backup remove [name] | 删除备份 | helper |
| !!backup rename [oldname] [newname] | 重命名备份 | helper |
| !!backup back | 回档 | helper |
| !!backup auto <on/off/[time]> | 自动备份(分钟) | helper |

**注§7： [name] 仅可使用字母、数字、下划线，长度限制为20字符以内       < >可不填**
