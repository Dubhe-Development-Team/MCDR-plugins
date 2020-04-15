# BridgeCaller

**注意！该插件还在开发中！本文档中提及的所有特性，都有可能在正式版本中删除或更改！**

BridgeCaller是一个对Minecraft数据包提供高级操作支持的插件。该插件可以让数据包使用随机数，调用系统时间等高级操作。该插件同时还可以对插件进行管理，无需服主自行替换。

该插件依赖于API [MCDReforged](https://github.com/Fallen-Breath/MCDReforged)。

## 插件管理功能
该插件可以直接安装插件或数据包。此操作需要helper权限。

命令列表：

| 命令 | 所需权限 | 作用 |
| :--------| :-----| :----- |
| !!bc | All | 显示帮助信息 |
| !!bc install <包链接> | Admin | 从指定链接安装包|
| !!bc remove <包名> | Admin | 移除包 **注意：如果有依赖此包的包，也会一起移除！**
| !!bc enable <包名> | Helper | 启用包 |
| !!bc disable <包名> | Helper | 禁用包 |
| !!bc update \[包名\] | Helper | 从包元数据中指定的链接升级包，包名留空以对所有包进行更新检测 |
| !!bc reload | Helper | 重载所有的包 |
| !!bc list | All | 显示所有已安装的包
| !!bc listall | All | 显示所有插件和数据包
| !!bc search <包名> | All | 查询是否已安装此包
| !!bc on | Admin | 启用bc包管理功能 |
| !!bc off | Admin | 禁用bc包管理功能 |

## 数据包支持
该功能将会为数据包提供高级功能支持。

**提供的功能：**
### **随机数**
待补充
### **获取系统时间**
待补充
