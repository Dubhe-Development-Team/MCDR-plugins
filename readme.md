# Economy

[English](https://github.com/zhang-anzhi/Economy/blob/master/readme_en.md)

> [MCDReforged](https://github.com/Fallen-Breath/MCDReforged) 经济插件
>
> 这是一个基础经济插件
>
> 它为其他的需要基于经济系统的插件提供了所需的API

**MCDaemon**

如果您拥有Linux环境并愿意将本插件移植至MCDaemon。

请创建一个Economy-MCD.py，我将很高兴接受Pull requests。

## 使用方法

| 命令 | 功能 |
|---|---|
| !!money help | 查看帮助 |
| !!money | 查询你的余额 |
| !!pay <player> <amount> | 将你的钱支付给他人 |
| !!money top | 查看财富榜 |
| !!money check <player> | 查询他人余额 |
| !!money give <player> <amount> | 给予他人钱 |
| !!money take <player> <amount> | 拿取他人钱（余额不足时减少至0） |
| !!money set <player> <amount> | 设置他人余额 |
| !!money update | 更新插件 |

## 配置~~文件（之后更新）~~

需要进行配置的为插件的前面的常量

### DATA_PATH
默认值:`./plugins/Economy/`

本插件文件存储的位置

### MAXIMAL_TOPS
默认值:`10`

使用`!!money top`时显示的数量

### cmd_permissions
默认值:
```
'top': 1,
'check': 2,
'give': 3,
'take': 3,
'set': 3
```

最低可以使用这些指令的权限等级

## 开发文档

**导入**

在`on_load`中加入以下内容:
```
global Economy
Economy = server.get_plugin_instance('Economy')
```

它具有以下方法:

| 方法 | 功能 |
|---|---|
| money_pay(player_from, player_to, amount) | 将 `player_from`的余额拿取 `amount`给予 `player_to`，然后返回 `amount`。如果没有该玩家，返回 `none_account`；如果余额不足，返回 `False` |
| money_check(player) | 查询`player`的余额，然后返回余额。如果没有查询到该玩家，返回 `none_account` |
| money_give(player, amount) | 给予 `player` `amount`，然后返回修改后的余额。如果没有查询到该玩家，返回 `none_account` |
| money_take(player, amount) | 拿取 `player` `amount`，然后返回修改后的余额。如果没有查询到该玩家，返回 `none_account` |
| money_set(player, amount) | 将 `player`的余额设置为 `amount`，然后返回修改后的余额。如果没有该玩家，返回 `none_account` |
| money_top() | 返回一个按余额从低到高排序后的字典，键为玩家名，值为玩家余额。|

`money_top`将会返回字典如下:
```
{
    'player1': 10
    'player2': 9
    'player3': 8
    'player4': 7
    ......
}
```

**提示**
- 调用这些方法时：

    1.如果返回 `none_account`，表示该玩家没有账户
    
    2.`amount`不能是负数
    
- 当传递实参 `amount`时，请先使用 `round(amount, 2)`约到百分位以避免Bug