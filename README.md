# server_change
一个兼容 [MCDReforged](https://github.com/Fallen-Breath/MCDReforged) 的用于群组服切换服务器的插件

## 简介

玩家可使用这个插件来方便的在群组服进行切换，无需使用/server

### 使用

| 指令 | 功能 | 权限 |
|---|---|---|
| !!sc | 切换服务器 | user |

### 配置

本插件没做配置文件，修改插件变量即可

`server_ids`列表是你的群组服的子服ID

`server_nams`列表是想要显示的服务器名称

请确保`server_ids`列表与`server_names`列表长度一致，否则会报错