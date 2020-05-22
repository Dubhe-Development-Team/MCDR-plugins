# Whitelist
[English](https://gitee.com/gu_zt666/MCDR-plugins/blob/Whitelist/README_EN.MD)

> [MCDReforged](https://github.com/Fallen-Breath/MCDReforged) 白名单管理
>
> 这是一个白名单管理插件
>
> 它可以使管理员无OP情况下管理白名单

**MCDaemon**

如果您拥有Linux环境并愿意将本插件移植至MCDaemon。

请创建一个Whitelist-MCD.py，我将很高兴接受Pull requests。

## 使用方法

| 命令 | 功能 | 权限 |
|---|---|---|
| !!whitelist | 查看帮助 | user |
| !!whitelist add <玩家> | 将玩家添加至白名单 | helper |
| !!whitelist remove <玩家> | 将玩家移出白名单 | helper |
| !!whitelist search <玩家> | 判断玩家是否添加至白名单 | user |
| !!whitelist list | 列出所有在白名单内的玩家 | user |
| !!whitelist reload | 从白名单文件重新加载白名单 | helper |
| !!whitelist on | 开启白名单 | admin |
| !!whitelist off | 关闭白名单 | admin |
