# Economy

[简体中文](https://github.com/zhang-anzhi/Economy/blob/master/readme.md)

> A Economic Plugin for [MCDReforged](https://github.com/Fallen-Breath/MCDReforged)
>
> This is a basic economy plugin
>
> It provides the API needed by other economic plugins

**MCDaemon**

If you have a Linux environment and want to import Economy as a 
[MCDaemon](https://github.com/kafuuchino-desu/MCDaemon) plugin.
Please pull requests Economy-MCD, I shall be glad to accept it.


## Usage

| Command | Function |
|---|---|
| !!money help | Show help message |
| !!money | Check your balance |
| !!pay <player> <amount> | Pay your money to other player |
| !!money top | Show the tops |
| !!money check <player> | Check player balance |
| !!money give <player> <amount> | Give money to player |
| !!money take <player> <amount> | Take money from player(If not enough, set to 0) |
| !!money set <player> <amount> | Set balance to player |
| !!money update | Update plugin |

## Configuration

The previous constant of the plugin need to be configured.

### DATA_PATH
Default:`./plugins/Economy/`

Storage path that this plugin use

### MAXIMAL_TOPS
Default:`10`

Display players when use`!!money top`

### cmd_permissions
Default:
```
'top': 1,
'check': 2,
'give': 3,
'take': 3,
'set': 3
```

The minimum permission needed to use these commands

## Develop Document

**Import**

Add these things to `on_load`:
```
global Economy
Economy = server.get_plugin_instance('Economy')
```

It has these following methods:

| Method | Function |
|---|---|
| money_pay(player_from, player_to, amount) | Take `player_from` `amount`to `player_to`, return `amount`. If can not find player, return `none_account`; if balance is not enough, return `False` |
| money_check(player) | Check balance from `player`, then return the balance. If can not find player, return `none_account` |
| money_give(player, amount) | Give `player` `amount`, return balance before change. If can not find player, return `none_account` |
| money_take(player, amount) | Take `player` `amount`, return balance before change. If can not find player, return `none_account` |
| money_set(player, amount) | Set `player`'s balance to `amount`，return balance before change. If can not find player, return `none_account` |
| money_top() | Return a dictionary sorted by balance from top to bottom, the key is player name, the value is player balance. |

`money_top` will return a dictionary like this:
```
{
    'player1': 10
    'player2': 9
    'player3': 8
    'player4': 7
    ......
}
```

**Tips**

- When you call these methods：
    
    1.If the return is `none_account`, which means this player has no account
    
    2.`amount` can not be a negative number

- When you call methods which needs to pass the information `amount`, please use `round(amount, 2)'`to round to the hundredth place to avoid bugs
