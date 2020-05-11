# BridgeCaller

**注意！该插件还在开发中！本文档中提及的所有特性，都有可能在正式版本中删除或更改！**

BridgeCaller是一个对Minecraft数据包提供更多原版数据包无法达到的功能的插件。该插件可以让数据包使用随机数，调用系统时间等功能。该插件同时还可以对插件进行管理，无需服主自行替换。


## 使用方法
**_插件尚未开发完毕，可能无法使用！_**
1. 克隆本仓库到本地
2. 将文件夹BCLib和BridgeCaller.py复制到MCDR的plugins文件夹下

## 运行环境
- [Python 3.X ](https://python.org)
- [MCDReforged](https://github.com/Fallen-Breath/MCDReforged)（版本>=alpha 0.7，否则部分功能无法工作）
- 确保服务器支持rcon连接


## 插件管理功能
该插件可以直接安装插件或数据包。

命令列表：

| 命令 | 所需权限 | 作用 |
| :--------| :-----| :----- |
| !!bc | All | 显示帮助信息 |
| !!bc install <包链接> | Admin | 从指定链接安装包|
| !!bc remove <包名> | Admin | 移除包 **注意：如果有依赖此包的包，也会一起移除！**
| !!bc enable <包名> | Helper | 启用包 |
| !!bc disable <包名> | Help | 禁用包 |
| !!bc update <包名> | Helper | 从包元数据中指定的链接升级包 |
| !!bc reload | Helper | 重载所有的包 |
| !!bc regen-SHA-256 | Helper | 重新计算SHA-256缓存，在同文件判断出现问题时可以使用 |
| !!bc SHA-256 <路径> | All | 查询对应文件的SHA-256，在下文详细解释 |
| !!bc list | All | 显示所有已安装的包
| !!bc listall | All | 显示所有插件和数据包
| !!bc search <包名> | All | 查询是否已安装此包
| !!bc on | Admin | 启用bc包管理功能 |
| !!bc off | Admin | 禁用bc包管理功能 |

### SHA-256
使用方法：!!bc SHA-256 <路径>

<路径>为**类型**+**路径**

支持的类型为：
- pyplugins：Python插件
- datapacks：数据包

如：\
!!bc SHA-256 pyplugins/BridgeCaller.py \
!!bc SHA-256 datapacks/dp1.zip


## 数据包支持
该功能将为数据包提供一些数据包无法达到或很难达到的功能的接口。

**提供的功能：**
#### 随机数
待补充
#### 获取系统时间
bc随时在获取系统时间
保存在计分板**bc.time**中
具体时间分别储存在虚拟玩家**$year**,**$month**,**$day**,**$hour**,**$minute**,**$second**,**$week**中
