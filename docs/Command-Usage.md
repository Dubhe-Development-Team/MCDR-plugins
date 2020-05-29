当输入无效的参数时，命令的使用方法将会打印在控制台/聊天中，**简单的输入 !!pm 或者 !!permb** 会显示当前用户的权限能够使用的所有命令。

如果输入命令后返回的只有插件版本，那么你没有权限使用任何插件，你需要使用服务器控制台来给自己使用 PermissionsManger 命令的权限。
### 别名
每个平台的可用的别名都列在下方，每个命令的效果都是一样的，所以你可以选择自己喜欢的来使用。


|           MCDR           |
|--------------------------|
| !!PermissionsManger      |
| !!perms                  |
| !!permissions            |
| !!perm                   |
| !!pm                     |

### 什么是上下文(Context)
参数 `context` 在PermissionsManger中使用频率很高，他的意义对大多数的用户可能不是那么显而易见。

Context，在常识中，意味着环境，某个权限，父组，前缀后缀抑或是元数据。

上下文分为两部分，键和值。PermissionsManger提供了默认的两种上下文，服务器和世界上下文，但是可能服务器的其他的插件提供更多可用的上下文，用户的"金钱"上下文可以在使用用户命令时找到。

举个例子，如果我想要在特定的世界设定我的权限，我就会使用世界上下文，解释的更详细些，我们假设这个世界叫做"nether"，我在命令中使用的上下文就将是`world=nether`。

当在命令中使用时，上下文 "key" 和 "value" 使用 `=` 分隔，你可以指定任意多的上下文，但是请记住所有的上下文都应该指定玩家相关的来应用权限之类的东西。

最终，举个例子，我想将 "PermissionsManger.info" 权限在 "nether" 世界设置为 true，只有在 "factions" 服务器有效，命令将会是：

`!!PermissionsManger user PermissionsManger set PermissionsManger.info true server=factions world=nether`.

这就是用来接收上下文的命令的相同的格式。

> 最终，给老用户的一些提醒，在命令的最后添加两个额外的 `[服务器] [世界]` 参数仍然被支持！

# 概览
#### 参数键值：
* `<必需>` - 运行指令时你 *必需* 指定这个参数
* `[可选]` - 如果没有指定将会使用默认

如果你想在参数中添加空格，你必须像这样 `" "` 使用引号把参数包起来。

下方使用的别名 (!!pm) 可以使用上方介绍的别名中的任意一个替换。

### 基础
*  [!!pm](#pm)
*  [!!pm `sync`](#pm-sync)
*  [!!pm `info`](#pm-info)
*  [!!pm `verbose` \<on | record | off | paste\> [filter]](#pm-verbose)
*  [!!pm `tree` [selection] [max level] [player]](#pm-tree)
*  [!!pm `search` \<permission\>](#pm-search)
*  [!!pm `check` \<user\> \<permission\>](#pm-check)
*  [!!pm `networksync`](#pm-networksync)
*  [!!pm `import` \<file\>](#pm-import)
*  [!!pm `export` \<file\>](#pm-export)
*  [!!pm `reloadconfig`](#pm-reloadconfig)
*  [!!pm `bulkupdate`](#pm-bulkupdate)
*  [!!pm `migration`](#pm-migration)
*  [!!pm `creategroup` \<group\>](#pm-creategroup)
*  [!!pm `deletegroup` \<group\>](#pm-deletegroup)
*  [!!pm `listgroups`](#pm-listgroups)
*  [!!pm `createtrack` \<track\>](#pm-createtrack)
*  [!!pm `deletetrack` \<track\>](#pm-deletetrack)
*  [!!pm `listtracks`](#pm-listtracks)

### 用户   (!!pm user \<user\> ...)
*  [!!pm user \<user\> `info`](#pm-user-user-info)
*  [!!pm user \<user\> `permission`](#permission---pm-user-user-permission---pm-group-group-permission-)
*  [!!pm user \<user\> `parent`](#parent---pm-user-user-parent---pm-group-group-parent-)
*  [!!pm user \<user\> `meta`](#meta---pm-user-user-meta---pm-group-group-meta-)
*  [!!pm user \<user\> `editor`](#pm-user-user-editor)
*  [!!pm user \<user\> `switchprimarygroup` \<group\>](#pm-user-user-switchprimarygroup)
*  [!!pm user \<user\> `promote` \<track\> [context...]](#pm-user-user-promote)
*  [!!pm user \<user\> `demote` \<track\> [context...]](#pm-user-user-demote)
*  [!!pm user \<user\> `showtracks`](#pm-user-user-showtracks)
*  [!!pm user \<user\> `clear` [context...]](#pm-user-user-clear)

### 组   (!!pm group \<group\> ...)
*  [!!pm group \<group\> `info`](#pm-group-group-info)
*  [!!pm group \<group\> `permission`](#permission---pm-user-user-permission---pm-group-group-permission-)
*  [!!pm group \<group\> `parent`](#parent---pm-user-user-parent---pm-group-group-parent-)
*  [!!pm group \<group\> `meta`](#meta---pm-user-user-meta---pm-group-group-meta-)
*  [!!pm group \<group\> `editor`](#pm-group-group-editor)
*  [!!pm group \<group\> `listmembers` [page]](#pm-group-group-listmembers)
*  [!!pm group \<group\> `setweight` \<weight\>](#pm-group-group-setweight)
*  [!!pm group \<group\> `showtracks`](#pm-group-group-showtracks)
*  [!!pm group \<group\> `clear` [context...]](#pm-group-group-clear)
*  [!!pm group \<group\> `rename` \<new name\>](#pm-group-group-rename)
*  [!!pm group \<group\> `clone` \<name of clone\>](#pm-group-group-clone)

### 权限   (!!pm user \<user\> permission ... | !!pm group \<group\> permission ...)
*  [`info`](#pm-usergroup-usergroup-permission-info)
*  [`set` \<node\> \<true/false\> [context...]](#pm-usergroup-usergroup-permission-set)
*  [`unset` \<node\> [context...]](#pm-usergroup-usergroup-permission-unset)
*  [`settemp` \<node\> \<true/false\> \<duration\> [context...]](#pm-usergroup-usergroup-permission-settemp)
*  [`unsettemp` \<node\> [context...]](#pm-usergroup-usergroup-permission-unsettemp)
*  [`check` \<node\> [context...]](#pm-usergroup-usergroup-permission-check)
*  [`checkinherits` \<node\> [context...]](#pm-usergroup-usergroup-permission-checkinherits)

### 继承   (!!pm user \<user\> parent ... | !!pm group \<group\> parent ...)
*  [`info`](#pm-usergroup-usergroup-parent-info)
*  [`set` \<group\> [context...]](#pm-usergroup-usergroup-parent-set)
*  [`add` \<group\> [context...]](#pm-usergroup-usergroup-parent-add)
*  [`remove` \<group\> [context...]](#pm-usergroup-usergroup-parent-remove)
*  [`settrack` \<track\> \<group\> [context...]](#pm-usergroup-usergroup-parent-settrack)
*  [`addtemp` \<group\> \<duration\> [context...]](#pm-usergroup-usergroup-parent-addtemp)
*  [`removetemp` \<group\> [context...]](#pm-usergroup-usergroup-parent-removetemp)
*  [`clear` [context...]](#pm-usergroup-usergroup-parent-clear)
*  [`cleartrack` \<track\> [context...]](#pm-usergroup-usergroup-parent-cleartrack)

### 元数据   (!!pm user \<user\> meta ... | !!pm group \<group\> meta ...)
*  [`info`](#pm-usergroup-usergroup-meta-info)
*  [`set` \<key\> \<value\> [context...]](#pm-usergroup-usergroup-meta-set)
*  [`unset` \<key\> [context...]](#pm-usergroup-usergroup-meta-unset)
*  [`settemp` \<key\> \<value\> \<duration\> [context...]](#pm-usergroup-usergroup-meta-settemp)
*  [`unsettemp` \<key\> [context...]](#pm-usergroup-usergroup-meta-unsettemp)
*  [`addprefix` \<priority\> \<prefix\> [context...]](#pm-usergroup-usergroup-meta-addprefix)
*  [`addsuffix` \<priority\> \<suffix\> [context...]](#pm-usergroup-usergroup-meta-addsuffix)
*  [`removeprefix` \<priority\> [prefix] [context...]](#pm-usergroup-usergroup-meta-removeprefix)
*  [`removesuffix` \<priority\> [suffix] [context...]](#pm-usergroup-usergroup-meta-removesuffix)
*  [`addtempprefix` \<priority\> \<prefix\> \<duration\> [context...]](#pm-usergroup-usergroup-meta-addtempprefix)
*  [`addtempsuffix` \<priority\> \<suffix\> \<duration\> [context...]](#pm-usergroup-usergroup-meta-addtempsuffix)
*  [`removetempprefix` \<priority\> [prefix] [context...]](#pm-usergroup-usergroup-meta-removetempprefix)
*  [`removetempsuffix` \<priority\> [suffix] [context...]](#pm-usergroup-usergroup-meta-removetempsuffix)
*  [`clear` [context...]](#pm-usergroup-usergroup-meta-clear)

### 轨道   (!!pm track \<track\> ...)
*  [!!pm track \<track\> `info`](#pm-track-track-info)
*  [!!pm track \<track\> `append` \<group\>](#pm-track-track-append)
*  [!!pm track \<track\> `insert` \<group\> \<position\>](#pm-track-track-insert)
*  [!!pm track \<track\> `remove` \<group\>](#pm-track-track-remove)
*  [!!pm track \<track\> `clear`](#pm-track-track-clear)
*  [!!pm track \<track\> `rename` \<new name\>](#pm-track-track-rename)
*  [!!pm track \<track\> `clone` \<name of clone\>](#pm-track-track-clone)

### 日志   (!!pm log ...)
*  [!!pm log `recent` [user] [page]](#pm-log-recent)
*  [!!pm log `search` \<query\> [page]](#pm-log-search)
*  [!!pm log `notify` [on|off]](#pm-log-notify)
*  [!!pm log `export` \<file\>](#pm-log-export)
*  [!!pm log `userhistory` \<user\> [page]](#pm-log-userhistory)
*  [!!pm log `grouphistory` \<group\> [page]](#pm-log-grouphistory)
*  [!!pm log `trackhistory` \<track\> [page]](#pm-log-trackhistory)

# 命令细节

### 基础
___
#### `!!pm`  
**权限**: n/a  
基础的 PermissionsManger 命令。将会打印用户有权限使用的所有的命令，包含每个命令的基础信息，和接受的参数。

___
#### `!!pm sync`  
**权限**: PermissionsManger.sync  
刷新所有加载的数据，如果存储中有变化，那么这个命令将会将服务器的信息添加存储中的更改。

___
#### `!!pm info`  
**权限**: PermissionsManger.info  
列出 PermissionsManger 的一些信息/数据，包括 debug 输出，统计，设置和配置中的一些重要的值。

___
#### `!!pm verbose`  
**权限**: PermissionsManger.verbose  
**参数**:  
* `<on|record|off|paste>` - 启用或禁用日志，或者粘贴日志输出
* `[filter]` - 排序输出使用的过滤器

控制 PermissionsManger 日志输出系统，这允许你坚挺所有对玩家的权限检查，当插件检查了玩家的权限，检查会被 verbose handler 处理。

如果你的过滤器匹配了权限检查，你就会被通知。

`on` 将会启用这个系统，并且当过滤器匹配时在聊天栏向你发送警告。`record` 会做相同的事，但是不会向你发送聊天中的警告。`off` 将会关闭这个系统，`paste` 将会把前 3500 个结果上传到 GitHub 的 pastebin，并向你提供链接。

过滤器用来匹配玩家检查到的权限的开头，你可以使用 `&`（与）和 `|`（或）符号，或者用 `!` 来否定一个匹配。`( )` 也是支持的。

**例子:**    
* `Permissions & (essentials | worldedit)` - 匹配每个检查 Permissions 的以 "essentials" 或 "worldedit" 开头的权限。
* `!Permissions & !anticheat` - 匹配每个对不是 Permissions 的玩家的对以不是 "anticheat" 开头的权限的检查。
* `anticheat & !anticheat.check` - matches any checks starting with "anticheat" but not starting with "anticheat.check"    

___
#### `!!pm tree`  
**权限**: PermissionsManger.tree  
**参数**:  
* `[selection]` - 树的根 (指定 `.` 包含所有的权限)
* `[max level]` - 最多返回多少子分支 (换句话说，树的宽度)
* `[player]` - 检查的在线玩家的名称

生成注册在服务器的权限的树来查看，树由服务器中的插件的数据提供而构建，当插件检查权限时这棵树将会扩大。

所有的参数都是可选的。默认的选择是 `.` （只是一个点，代表所有），默认的最大等级是 `5`。

选择允许你只生成树的一部分，比如，选择 `PermissionsManger.user` 将只会返回树中以 `PermissionsManger.user` 开头的分支。

Max level 允许你定义最多包括的子分支，举个例子，如果你设置最大等级为 `2`，"PermissionsManger.user" 将会被返回，但是 "PermissionsManger.user.info" 将不会被显示。

___
#### `!!pm search`  
**权限**: PermissionsManger.search  
**参数**:  
* `<permission>` - 搜索的权限

搜索所有用户/组的特定权限，返回分页的所有条目的列表。

___
#### `!!pm check`  
**权限**: PermissionsManger.check  
**参数**:  
* `<user>` - 检查的玩家
* `<permission>` - 检查的权限

执行一个普通的对在线玩家的权限检查，返回结果，这个检查与其他插件的权限检查的结果相同。

___
#### `!!pm networksync`  
**权限**: PermissionsManger.sync  
刷新所有存储提供的缓存数据，接着（如果提供了的话）使用消息服务来请求连接的其他的服务器并请求所有服务器同步。

___
#### `!!pm import`  
**权限**: PermissionsManger.import  
**参数**:  
* `<file>` - 导入的文件

从文件导入 PermissionsManger 的数据，文件必须是一列命令，以 "!!PermissionsManger" 开头，这个文件可以使用 export 命令生成，文件必须在插件的目录下。

___
#### `!!pm export`  
**权限**: PermissionsManger.export  
**参数**:  
* `<file>` - 导出的文件

将 PermissionsManger 的数据导出到一个文件，这个文件也可以作为一个备份，或者在 PermissionsManger 的安装之间转移数据。这个文件可以使用 import 命令重新导入，生成的文件在插件的目录下。

___
#### `!!pm reloadconfig`  
**权限**: PermissionsManger.reloadconfig  
重载配置文件的部分值。不是所有的条目都会被这个命令重载，有些需要一次完全的服务器重启才能生效（比如存储的设置）。

___
#### `!!pm creategroup`  
**权限**: PermissionsManger.creategroup  
**参数**:  
* `<name>` - 组的名称

创建一个新的组。

___
#### `!!pm deletegroup`  
**权限**: PermissionsManger.deletegroup  
**参数**:  
* `<name>` - 组的名称

永久的删除一个组。

___
#### `!!pm listgroups`  
**权限**: PermissionsManger.listgroups  
显示当前的所有的组。

___
#### `!!pm createtrack`  
**权限**: PermissionsManger.createtrack  
**参数**:  
* `<name>` - 路线名称

创建新的路线。

___
#### `!!pm deletetrack`  
**权限**: PermissionsManger.deletetrack  
**参数**:  
* `<name>` - 路线的名称

永久删除一个路线。

___
#### `!!pm listtracks`  
**权限**: PermissionsManger.listtracks  
显示当前所有的路线。

___

### 用户   (!!pm user \<user\> ...)
___
#### `!!pm user <user> info`  
**权限**: PermissionsManger.user.info  
显示一个用户的信息，包括用户名，主组，继承组，和当前的上下文。

___
#### `!!pm user <user> editor`  
**权限**: PermissionsManger.user.editor  
开启编辑指定的用户的权限的网页接口，当更改保存后，你将会收到一条命令，使用后使更改生效。

___
#### `!!pm user <user> switchprimarygroup`  
**权限**: PermissionsManger.user.switchprimarygroup  
**参数**:  
* `<group>` - 切换的组

这个命令允许你更改用户的主组，如果他们还不是这个组的成员，他们将被添加到新的组。这不应该作为 "parent set" 命令的替代，他们的现有的主组将不会被移除，而是作为继承组（一个用户可以有多个继承组）。

如果 `primary-group-calculation` 选项被设置为不是 "stored" 的其他东西，你应该使用 `parent add`(#pm-usergroup-usergroup-parent-add) 或者 `parent set`(#pm-usergroup-usergroup-parent-set) 命令而不是这个命令。

___
#### `!!pm user <user> promote`  
**权限**: PermissionsManger.user.promote  
**参数**:  
* `<track>` - 升级遵循的路线
* `[context...]` - 升级使用的上下文

这个命令将会沿着一条路线提升玩家，命令会检查玩家在给出的上下文里是否在这个路线上，如果用户没有在这条路线，他们将会被加入这条路线的第一个组，如果玩家在这条路线上的不止一个组，命令将会执行失败。在其他情况下，玩家将会被成功提升，并将会被从现有的组移除。如果路线动作影响了用户的主组，他们也会被更新。

___
#### `!!pm user <user> demote`  
**权限**: PermissionsManger.user.demote  
**参数**:  
* `<track>` - 降级的遵循的路线
* `[context...]` - 降级使用的上下文

这个命令将会沿着一条路线降级玩家，命令会检查玩家在给出的上下文里是否在这个路线上，如果用户没有在这条路线，或者玩家在这条路线上的不止一个组，命令将会执行失败。在其他情况下，玩家将会被成功降级，并将会被从现有的组移除。如果路线动作影响了用户的主组，他们也会被更新。

___
#### `!!pm user <user> showtracks`  
**权限**: PermissionsManger.user.showtracks  
显示玩家当前所在的全部路线。

___
#### `!!pm user <user> clear`  
**权限**: PermissionsManger.user.clear  
**参数**:  
* `[context...]` - 用于过滤的上下文

清除玩家的权限，继承组和元数据。

___
### 组   (!!pm group \<group\> ...)
___
#### `!!pm group <group> info`  
**权限**: PermissionsManger.group.info  
显示一个组的信息。

___
#### `!!pm group <group> editor`  
**权限**: PermissionsManger.group.editor  
开启编辑指定的组的权限的网页接口，当更改保存后，你将会收到一条命令，使用后使更改生效。

___
#### `!!pm group <group> listmembers`  
**权限**: PermissionsManger.group.listmembers  
**参数**:  
* `[page]` - 查看的页数

显示直接继承这个组的用户/组

___
#### `!!pm group <group> setweight`  
**权限**: PermissionsManger.group.setweight  
**参数**:  
* `<weight>` - 设置的权重

设置组的权重值，这决定了决定用户的权限的顺序。越大的值代表越高的权重。

___
#### `!!pm group <group> showtracks`  
**权限**: PermissionsManger.group.showtracks  
显示一个组所在的所有的路线。

___
#### `!!pm group <group> clear`  
**权限**: PermissionsManger.group.clear  
**参数**:  
* `[context...]` - 用于过滤的上下文

清除组的权限，继承组和元数据。

___
#### `!!pm group <group> rename`  
**权限**: PermissionsManger.group.rename  
**参数**:  
* `<new name>` - 组的新的名称

更改组的名称，注意任何组的成员都不会知道这个变更，他们还将在原来的旧组的组名。如果你希望更新这些状态，你应该使用块变更特性来更新存在的条目。

___
#### `!!pm group <group> clone`  
**权限**: PermissionsManger.group.clone  
**参数**:  
* `<new name>` - 复制的名称

创建一个组的不同名称的拷贝。

___
### 权限   (!!pm user \<user\> permission ... | !!pm group \<group\> permission ...)
___
#### `!!pm user/group <user|group> permission info`  
**权限**: PermissionsManger.user.permission.info 或 PermissionsManger.group.permission.info  
显示一个用户/组拥有的所有的权限。

___
#### `!!pm user/group <user|group> permission set`  
**权限**: PermissionsManger.user.permission.set or PermissionsManger.group.permission.set  
**参数**:  
* `<node>` - 设置的权限节点
* `<true|false>` - 设置权限的值
* `[context...]` - 设置权限的上下文

设置（或给予）某个用户/组一个权限，提供 false 值将会否定这个权限。

___
#### `!!pm user/group <user|group> permission unset`  
**权限**: PermissionsManger.user.permission.unset or PermissionsManger.group.permission.unset  
**参数**:  
* `<node>` - 取消设置的权限节点
* `[context...]` - 取消设置权限的上下文

取消设置一个用户或组的权限节点。

___
#### `!!pm user/group <user|group> permission settemp`  
**权限**: PermissionsManger.user.permission.settemp or PermissionsManger.group.permission.settemp  
**参数**:  
* `<node>` - 设置的权限节点
* `<true|false>` - 设置的权限的值
* `<duration>` - 权限过期的时间
* `[context...]` - 权限设置的上下文

给一个玩家/组设置临时权限，提供 false 值将会否定这个权限。持续时间应为时间段或者一个标准的 Unix 时间戳，比如 "3d13h45m" 将会设置权限在 3 天, 13 小时 45 分钟后过期。"1482694200" 会设置过期时间为 7:30PM 于 25th December 2016。

___
#### `!!pm user/group <user|group> permission unsettemp`  
**权限**: PermissionsManger.user.permission.unsettemp or PermissionsManger.group.permission.unsettemp  
**参数**:  
* `<node>` - 取消设置的权限节点
* `[context...]` - 取消设置权限的上下文

取消设置一个用户或组的临时权限节点。

___
#### `!!pm user/group <user|group> permission check`  
**权限**: PermissionsManger.user.permission.check or PermissionsManger.group.permission.check  
**参数**:  
* `<node>` - 检查的权限节点
* `[context...]` - 检查的权限节点的上下文

检查一个组或者玩家有特定的权限

___
#### `!!pm user/group <user|group> permission checkinherits`  
**权限**: PermissionsManger.user.permission.checkinherits or PermissionsManger.group.permission.checkinherits  
**参数**:  
* `<node>` - 检查的权限节点
* `[context...]` - 检查的权限节点的上下文

检查一个组或者玩家继承了特定的权限，如果是，从哪里继承的。

___

### 继承组   (!!pm user \<user\> parent ... | !!pm group \<group\> parent ...)
___
#### `!!pm user/group <user|group> parent info`  
**权限**: PermissionsManger.user.parent.info or PermissionsManger.group.parent.info  
显示一个用户/组的继承的组

___
#### `!!pm user/group <user|group> parent set`  
**权限**: PermissionsManger.user.parent.set or PermissionsManger.group.parent.set  
**参数**:  
* `<group>` - 设置的组
* `[context...]` - 设置的组的上下文

设置一个用户/组的继承组，不像是 "parent add" 命令，这个命令将会清空所有已经存在的组。"add" 命令只会简单的将组添加到已经存在的组里，如果命令执行时没有上下文环境，这个插件也会更新玩家的主组。

___
#### `!!pm user/group <user|group> parent add`  
**权限**: PermissionsManger.user.parent.add or PermissionsManger.group.parent.add  
**参数**:  
* `<group>` - 添加的组
* `[context...]` - 添加的组用的上下文

添加一个集成组到一个玩家/组，不像是 "parent set" 命令，这个命令只会将组添加进已经存在的组的列表。没有已经存在的继承组会被移除，用户的主组也不会被影响。

___
#### `!!pm user/group <user|group> parent remove`  
**权限**: PermissionsManger.user.parent.remove or PermissionsManger.group.parent.remove  
**参数**:  
* `<group>` - 移除的组
* `[context...]` - 移除的组的上下文

移除一个用户/组的继承组。

___
#### `!!pm user/group <user|group> parent settrack`  
**权限**: PermissionsManger.user.parent.settrack or PermissionsManger.group.parent.settrack  
**参数**:  
* `<track>` - 设置的路线
* `<group>` - 设置的组，或者这个路线的组的相对位置
* `[context...]` - 设置的组的上下文

设置用户/组在给出的路线的位置，这个跟 set 命令相同，除了这个将会清除在指定的路线上已经存在的组，其他继承组不会被影响。

___
#### `!!pm user/group <user|group> parent addtemp`  
**权限**: PermissionsManger.user.parent.addtemp or PermissionsManger.group.parent.addtemp  
**参数**:  
* `<group>` - 添加的组
* `<duration>` - 组的过期时间
* `[context...]` - 添加组的上下文

给一个玩家/组添加临时继承组。持续时间应为时间段或者一个标准的 Unix 时间戳，比如 "3d13h45m" 将会设置权限在 3 天, 13 小时 45 分钟后过期。"1482694200" 会设置过期时间为 7:30PM 于 25th December 2016。

___
#### `!!pm user/group <user|group> parent removetemp`  
**权限**: PermissionsManger.user.parent.removetemp or PermissionsManger.group.parent.removetemp  
**参数**:  
* `<group>` - 移除的组
* `[context...]` - 移除的组的上下文

移除一个用户/组的临时继承组。

___
#### `!!pm user/group <user|group> parent clear`  
**权限**: PermissionsManger.user.parent.clear or PermissionsManger.group.parent.clear  
**参数**:  
* `[context...]` - 用于过滤的上下文

移除所有继承组。

___
#### `!!pm user/group <user|group> parent cleartrack`  
**权限**: PermissionsManger.user.parent.cleartrack or PermissionsManger.group.parent.cleartrack  
**参数**:  
* `<track>` - 移除的路线
* `[context...]` - 用于过滤的上下文

移除指定路线的玩家/组的所有继承组。

___

### 元数据   (!!pm user \<user\> meta ... | !!pm group \<group\> meta ...)
___
#### `!!pm user/group <user|group> meta info`  
**权限**: PermissionsManger.user.meta.info or PermissionsManger.group.meta.info  
显示用户/组的继承元数据，前缀和后缀。

___
#### `!!pm user/group <user|group> meta set`  
**权限**: PermissionsManger.user.meta.set or PermissionsManger.group.meta.set  
**参数**:  
* `<key>` - 设置的键值
* `<value>` - 设置的键值的值
* `[context...]` - 设置的元数据的上下文

设置用户/组的键值对元数据，这些值可以用于读取并且可以通过其他使用 Vault 或者 Sponge Permissions API 的插件更改。

___
#### `!!pm user/group <user|group> meta unset`  
**权限**: PermissionsManger.user.meta.unset or PermissionsManger.group.meta.unset  
**参数**:  
* `<key>` - 取消设置的键
* `[context...]` - 取消设置的元数据的上下文

取消设置一个用户或组的元数据键值。

___
#### `!!pm user/group <user|group> meta settemp`  
**权限**: PermissionsManger.user.meta.settemp or PermissionsManger.group.meta.settemp  
**参数**:  
* `<key>` - 设置的键值
* `<value>` - 设置的键的值
* `<duration>` - 元数据过期的时间
* `[context...]` - 设置的元数据的上下文

给一个玩家/组设置临时元数据键值，提供 false 值将会否定这个权限。持续时间应为时间段或者一个标准的 Unix 时间戳，比如 "3d13h45m" 将会设置权限在 3 天, 13 小时 45 分钟后过期。"1482694200" 会设置过期时间为 7:30PM 于 25th December 2016。

___
#### `!!pm user/group <user|group> meta unsettemp`  
**权限**: PermissionsManger.user.meta.unsettemp or PermissionsManger.group.meta.unsettemp  
**参数**:  
* `<key>` - 取消设置的键
* `[context...]` - 取消设置的元数据的上下文

取消设置一个用户或组的临时元数据。

___
#### `!!pm user/group <user|group> meta addprefix`  
**权限**: PermissionsManger.user.meta.addprefix or PermissionsManger.group.meta.addprefix  
**参数**:  
* `<priority>` - 添加前缀的优先度
* `<prefix>` - 实际的前缀字符串
* `[context...]` - 添加前缀的上下文

给一个玩家/组设置前缀，使用 " " 来添加空格。

___
#### `!!pm user/group <user|group> meta addsuffix`  
**权限**: PermissionsManger.user.meta.addsuffix or PermissionsManger.group.meta.addsuffix  
**参数**:  
* `<priority>` - 添加后缀的优先度
* `<suffix>` - 实际的后缀字符串
* `[context...]` - 添加后缀的上下文

给一个玩家/组设置后缀，使用 " " 来添加空格。

___
#### `!!pm user/group <user|group> meta removeprefix`  
**权限**: PermissionsManger.user.meta.removeprefix or PermissionsManger.group.meta.removeprefix  
**参数**:  
* `<priority>` - 移除前缀的优先度
* `<prefix>` - 实际的前缀字符串
* `[context...]` - 添加前缀的上下文

给一个玩家/组移除前缀，使用 " " 来添加空格。

___
#### `!!pm user/group <user|group> meta removesuffix`  
**权限**: PermissionsManger.user.meta.removesuffix or PermissionsManger.group.meta.removesuffix  
**参数**:  
* `<priority>` - 移除后缀的优先度
* `<suffix>` - 实际的后缀字符串
* `[context...]` - 添加后缀的上下文

给一个玩家/组移除后缀，使用 " " 来添加空格。

___
#### `!!pm user/group <user|group> meta addtempprefix`  
**权限**: PermissionsManger.user.meta.addtempprefix or PermissionsManger.group.meta.addtempprefix  
**参数**:  
* `<priority>` - 添加前缀的优先度
* `<prefix>` - 实际的前缀字符串
* `<duration>` - 前缀过期的时间
* `[context...]` - 添加前缀的上下文

给一个玩家/组设置临时前缀，提供 false 值将会否定这个权限。持续时间应为时间段或者一个标准的 Unix 时间戳，比如 "3d13h45m" 将会设置权限在 3 天, 13 小时 45 分钟后过期。"1482694200" 会设置过期时间为 7:30PM 于 25th December 2016。

___
#### `!!pm user/group <user|group> meta addtempsuffix`  
**权限**: PermissionsManger.user.meta.addtempsuffix or PermissionsManger.group.meta.addtempsuffix  
**参数**:  
* `<priority>` - 添加后缀的优先度
* `<suffix>` - 实际的后缀字符串
* `<duration>` - 后缀过期的时间
* `[context...]` - 添加后缀的上下文

给一个玩家/组设置临时后缀，提供 false 值将会否定这个权限。持续时间应为时间段或者一个标准的 Unix 时间戳，比如 "3d13h45m" 将会设置权限在 3 天, 13 小时 45 分钟后过期。"1482694200" 会设置过期时间为 7:30PM 于 25th December 2016。

___
#### `!!pm user/group <user|group> meta removetempprefix`  
**权限**: PermissionsManger.user.meta.removetempprefix or PermissionsManger.group.meta.removetempprefix  
**参数**:  
* `<priority>` - 移除前缀的优先度
* `<prefix>` - 实际的前缀字符串
* `[context...]` - 添加前缀的上下文

给一个玩家/组移除临时前缀，使用 " " 来添加空格。

___
#### `!!pm user/group <user|group> meta removetempsuffix`  
**权限**: PermissionsManger.user.meta.removetempsuffix or PermissionsManger.group.meta.removetempsuffix  
**参数**:  
* `<priority>` - 移除后缀的优先度
* `<suffix>` - 实际的后缀字符串
* `[context...]` - 添加后缀的上下文

给一个玩家/组移除临时后前缀，使用 " " 来添加空格。

___
#### `!!pm user/group <user|group> meta clear`  
**权限**: PermissionsManger.user.meta.clear or PermissionsManger.group.meta.clear  
**参数**:  
* `[context...]` - 用于过滤的上下文

移除所有的元数据，前后缀。

___

### 路线   (!!pm track \<track\> ...)
___
#### `!!pm track <track> info`  
**权限**: PermissionsManger.track.info  
显示路线中的组。

___
#### `!!pm track <track> append`  
**权限**: PermissionsManger.track.info  
**参数**:  
* `<group>` - 添加的组

在路线结尾追加一个组。

___
#### `!!pm track <track> insert`  
**权限**: PermissionsManger.track.insert  
**参数**:  
* `<group>` - 插入的组
* `<position>` - 插入的组的位置

在指定的路线的位置插入一个组，为 1 的位置将会是路径的开始。

___
#### `!!pm track <track> remove`  
**权限**: PermissionsManger.track.remove  
**参数**:  
* `<group>` - 移除的组

从路线移除一个组。

___
#### `!!pm track <track> clear`  
**权限**: PermissionsManger.track.clear  
移除路线中的所有的组。

___
#### `!!pm track <track> rename`  
**权限**: PermissionsManger.track.rename  
**参数**:  
* `<new name>` - 路线的新名称

更改路线的名称。

___
#### `!!pm track <track> clone`  
**权限**: PermissionsManger.track.clone  
**参数**:  
* `<new name>` - 拷贝的名称

创建路线的不同名称的拷贝。

___

### 日志   (!!pm log ...)
___
#### `!!pm log recent`  
**权限**: PermissionsManger.log.recent  
**参数**:  
* `[user]` - 用于过滤的名称、UUID
* `[page]` - 查看的页数

显示最近的动作。

___
#### `!!pm log search`  
**权限**: PermissionsManger.log.search  
**参数**:  
* `<query>` - 查询的查询
* `[page]` - 查看的页数

搜索匹配查询的所有日志条目。

___
#### `!!pm log notify`  
**权限**: PermissionsManger.log.notify  
**参数**:  
* `[on|off]` - 是否开启

开关向发送者发送提醒的功能。

___
#### `!!pm log export`  
**权限**: PermissionsManger.log.export  
**参数**:  
* `<file>` - the file to export to

将日志导出为一列命令，可以被 "!!pm import" 命令识别，这个特性应该尽量不使用，推荐使用 "!!pm export" 命令。

___
#### `!!pm log userhistory`  
**权限**: PermissionsManger.log.userhistory  
**参数**:  
* `<user>` - 搜索的玩家
* `[page]` - 查看的页数

搜索有关给出玩家的日志。

___
#### `!!pm log grouphistory`  
**权限**: PermissionsManger.log.grouphistory  
**参数**:  
* `<group>` - 搜索的组
* `[page]` - 查看的页数

搜索有关给出组的日志。

___
#### `!!pm log trackhistory`  
**权限**: PermissionsManger.log.trackhistory  
**参数**:  
* `<track>` - 搜索的路线
* `[page]` - 查看的页数

搜索有关给出路线的日志。

___

# 指令权限

**注意**: 你可以使用通配符
* **All commands** - PermissionsManger.*
* **All user commands** - PermissionsManger.user.*
* **All group commands** - PermissionsManger.group.*
* **All track commands** - PermissionsManger.track.*
* **All log commands** - PermissionsManger.log.*

### 基础
*  PermissionsManger.sync
*  PermissionsManger.info
*  PermissionsManger.verbose
*  PermissionsManger.tree
*  PermissionsManger.search
*  PermissionsManger.check
*  PermissionsManger.import
*  PermissionsManger.export
*  PermissionsManger.reloadconfig
*  PermissionsManger.migration
*  PermissionsManger.creategroup
*  PermissionsManger.deletegroup
*  PermissionsManger.listgroups
*  PermissionsManger.createtrack
*  PermissionsManger.deletetrack
*  PermissionsManger.listtracks

### 用户
*  PermissionsManger.user.info
*  PermissionsManger.user.permission.info
*  PermissionsManger.user.permission.set
*  PermissionsManger.user.permission.unset
*  PermissionsManger.user.permission.settemp
*  PermissionsManger.user.permission.unsettemp
*  PermissionsManger.user.permission.check
*  PermissionsManger.user.permission.checkinherits
*  PermissionsManger.user.parent.info
*  PermissionsManger.user.parent.set
*  PermissionsManger.user.parent.add
*  PermissionsManger.user.parent.remove
*  PermissionsManger.user.parent.addtemp
*  PermissionsManger.user.parent.removetemp
*  PermissionsManger.user.parent.clear
*  PermissionsManger.user.meta.info
*  PermissionsManger.user.meta.set
*  PermissionsManger.user.meta.unset
*  PermissionsManger.user.meta.settemp
*  PermissionsManger.user.meta.unsettemp
*  PermissionsManger.user.meta.addprefix
*  PermissionsManger.user.meta.addsuffix
*  PermissionsManger.user.meta.removeprefix
*  PermissionsManger.user.meta.removesuffix
*  PermissionsManger.user.meta.addtempprefix
*  PermissionsManger.user.meta.addtempsuffix
*  PermissionsManger.user.meta.removetempprefix
*  PermissionsManger.user.meta.removetempsuffix
*  PermissionsManger.user.meta.clear
*  PermissionsManger.user.editor
*  PermissionsManger.user.switchprimarygroup
*  PermissionsManger.user.showtracks
*  PermissionsManger.user.promote
*  PermissionsManger.user.demote
*  PermissionsManger.user.clear

### 组
*  PermissionsManger.group.info
*  PermissionsManger.group.permission.info
*  PermissionsManger.group.permission.set
*  PermissionsManger.group.permission.unset
*  PermissionsManger.group.permission.settemp
*  PermissionsManger.group.permission.unsettemp
*  PermissionsManger.group.permission.check
*  PermissionsManger.group.permission.checkinherits
*  PermissionsManger.group.parent.info
*  PermissionsManger.group.parent.set
*  PermissionsManger.group.parent.add
*  PermissionsManger.group.parent.remove
*  PermissionsManger.group.parent.addtemp
*  PermissionsManger.group.parent.removetemp
*  PermissionsManger.group.parent.clear
*  PermissionsManger.group.meta.info
*  PermissionsManger.group.meta.set
*  PermissionsManger.group.meta.unset
*  PermissionsManger.group.meta.settemp
*  PermissionsManger.group.meta.unsettemp
*  PermissionsManger.group.meta.addprefix
*  PermissionsManger.group.meta.addsuffix
*  PermissionsManger.group.meta.removeprefix
*  PermissionsManger.group.meta.removesuffix
*  PermissionsManger.group.meta.addtempprefix
*  PermissionsManger.group.meta.addtempsuffix
*  PermissionsManger.group.meta.removetempprefix
*  PermissionsManger.group.meta.removetempsuffix
*  PermissionsManger.group.meta.clear
*  PermissionsManger.group.editor
*  PermissionsManger.group.listmembers
*  PermissionsManger.group.showtracks
*  PermissionsManger.group.setweight
*  PermissionsManger.group.clear
*  PermissionsManger.group.rename
*  PermissionsManger.group.clone

### 路线
*  PermissionsManger.track.info
*  PermissionsManger.track.append
*  PermissionsManger.track.insert
*  PermissionsManger.track.remove
*  PermissionsManger.track.clear
*  PermissionsManger.track.rename
*  PermissionsManger.track.clone

### 日志
*  PermissionsManger.log.recent
*  PermissionsManger.log.search
*  PermissionsManger.log.notify
*  PermissionsManger.log.export
*  PermissionsManger.log.userhistory
*  PermissionsManger.log.grouphistory
*  PermissionsManger.log.trackhistory
