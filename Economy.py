# -*- coding: utf-8 -*-
# v2.2.1

import os
import json
import operator


FILE_PATH = './plugins/Economy/'
MAXIMAL_TOPS = 10
cmd_permissions = {
    'top': 1,
    'check': 2,
    'give': 3,
    'take': 3,
    'set': 3
}

HelpMessage = '''
--------Economy 原版经济插件--------
§6!!money help §7查看帮助
§6!!money §7查询余额
§6!!pay <§6§oplayer§6> <§6§oamount§6> §7将你的钱支付给他人
§6!!money top §7查看财富榜
§6!!money check <§6§oplayer§6> §7查询他人余额
§6!!money give <§6§oplayer§6> <§6§oamount§6> §7给予他人钱
§6!!money take <§6§oplayer§6> <§6§oamount§6> §7拿取他人钱
§6!!money set <§6§oplayer§6> <§6§oamount§6> §7设置他人余额
--------------------------------'''



def open_data():
    with open(FILE_PATH + 'economy.json') as open_data:
        return json.load(open_data)


def on_load(server, old):
    server.add_help_message('!!money help', '经济系统帮助')
    if not os.path.exists(FILE_PATH):
        os.makedirs(FILE_PATH)
    if not os.path.exists(FILE_PATH + 'economy.json'):
        with open(FILE_PATH + 'economy.json', 'w') as create:
            create.write(json.dumps([], indent=1))
    global player_data
    player_data = open_data()


def on_unload(server):
    write_data()


def on_player_joined(server, player):
    if money_check(player) == 'none_account':
        player_data.append({'name': '{}'.format(player),'balance': 0.0})
        write_data()


def on_info(server, info):
    # check your self
    if info.content.startswith('!!money'):
        permission = server.get_permission_level(info)
        content = info.content.rstrip(' ').split(' ')
        if info.content == '!!money':
            server.reply(info, '§a您的余额为:§e' + str(money_check(info.player)))
        if len(content) >= 2:
            del content[0]
            commands(server, info, content, permission)

    # pay
    if info.content.startswith('!!pay') and info.is_player:
        content = info.content.rstrip(' ').split(' ')
        if content[0] == '!!pay':
            del content[0]
            player_from = info.player
            player_to = content[0]
            amount = round(float(content[1]), 2)
            if amount <= 0:
                wrong_amount(server, info)
            else:
                return_info = money_pay(player_from, player_to, amount)
                if return_info == 'none_account':
                    none_account(server, info, player_to)
                elif return_info == False:
                    server.reply(info, '§c余额不足!')
                else:
                    server.reply(info, '§a你向§e' + player_to + '§a支付了§e' + str(amount))
                    server.tell(player_to, '§e' + player_from + '§a向你支付了§e' + str(amount))


def commands(server, info, content, permission):
    # help
    if content[0] == 'help':
        server.reply(info, HelpMessage)

    # top
    elif content[0] == 'top' and permission >= cmd_permissions['top'] and len(content) == 1:
        order = 0
        for name, balance in money_top().items():
            order = order + 1
            server.reply(info, '§a' + str(order) + '.§e' + name + '§a:§e' + str(balance))
            if order == MAXIMAL_TOPS:
                break

    # check
    elif content[0] == 'check' and permission >= cmd_permissions['check'] and len(content) == 2:
        player = content[1]
        amount = money_check(player)
        if amount == 'none_account':
            none_account(server, info, player)
        else:
            server.reply(info, '§e' + player + '§a的余额:§e' + str(amount))

    # give
    elif content[0] == 'give' and permission >= cmd_permissions['give'] and len(content) == 3:
        player = content[1]
        amount = round((float(content[2])), 2)
        if amount <= 0:
            wrong_amount(server, info)
        elif money_give(player, amount) == 'none_account':
            none_account(server, info, player)
        else:
            server.reply(info, '§a金钱已给予!')

    # take
    elif content[0] == 'take' and permission >= cmd_permissions['take'] and len(content) == 3:
        player = content[1]
        amount = round((float(content[2])), 2)
        if amount <= 0:
            wrong_amount(server, info)
        elif money_take(player, amount) == 'none_account':
            none_account(server, info, player)
        else:
            server.reply(info, '§a金钱已拿取!')

    # set
    elif content[0] == 'set' and permission >= cmd_permissions['set'] and len(content) == 3:
        player = content[1]
        amount = round(float(content[2]), 2)
        if amount < 0:
            wrong_amount(server, info)
        elif money_set(player, amount) == 'none_account':
            none_account(server, info, player)
        else:
            server.reply(info, '§a将§e' + player + '§a的余额设为:§e' + str(amount))

    # update
    elif content[0] == 'update' and permission >= 3 and len(content) == 1:
        import requests
        with open('./plugins/Economy.py', 'wb') as write:
            write.write(requests.get('https://gitee.com/gu_zt666/MCDR-plugins/raw/Economy/Economy.py').content)
        server.reply(info, '§aEconomy更新成功！')
        server.refresh_changed_plugins()

    # wrong command
    else:
        wrong_cmd(server, info)


def wrong_cmd(server, info):
    server.reply(info, '§c命令格式错误! 使用!!money help查看帮助')


def none_account(server, info, player):
    server.reply(info, '§e' + player + '§a没有账户!')


def wrong_amount(server, info):
    server.reply(info, '§c非法金额！')


def money_pay(player_from, player_to, amount):
    if amount >= 0:
        player_form_amount = money_check(player_to)
        if player_form_amount == 'none_account':
            return 'none_account'
        else:
            amount = round(amount, 2)
            if money_check(player_from) >= amount:
                money_take(player_from, amount)
                money_give(player_to, amount)
                return amount
            else:
                return False

def money_top():
    ordered_list = sorted(player_data, key=operator.itemgetter('balance'), reverse=True)
    return_list = {}
    for player in ordered_list:
        return_list[player['name']] = player['balance']
    return return_list


def money_check(player):
    for data in player_data:
        for values in data.values():
            if values == player:
                return round(data['balance'], 2)
    else:
        return 'none_account'


def money_give(player, amount):
    if amount >= 0:
        amount = round(amount, 2)
        old_amount = money_check(player)
        if old_amount == 'none_account':
            return 'none_account'
        new_amount = float(old_amount + amount)
        if money_set(player, new_amount) != 'none_account':
            return new_amount


def money_take(player, amount):
    if amount >= 0:
        amout = round(amount, 2)
        old_amount = money_check(player)
        if old_amount == 'none_account':
            return 'none_account'
        new_amount = float(old_amount - amount)
        if new_amount < 0:
            new_amount = 0
        return money_set(player, new_amount)


def money_set(player, amount):
    if amount >= 0:
        amount = round(amount, 2)
        if money_check(player) == 'none_account':
            return 'none_account'
        else:
            for data in player_data:
                for values in data.values():
                    if values == player:
                        player_data.remove(data)
                        set_amount = {
                            'name': player,
                            'balance': round(amount, 2)
                        }
                        player_data.append(set_amount)
                        write_data()
                        return amount


def write_data():
    with open(FILE_PATH + 'economy.json', 'w') as create:
        create.write(json.dumps(player_data, indent=1))
