"""
bcapi

为MCDR插件提供一些难以达到的功能
"""


class Player():
    def __init__(self, server, player_target):
        pass

    def death(self):
        pass

    def kick(self):
        pass

    def execute(self, command):
        pass

    def get_data(self, path):
        pass

    def replace_item(self, slot, item):
        pass

    def move2pos(self, x, y, z):
        pass

    def get_look_block_pos(self):
        pass


class FakePlayer(Player):
    def __init__(self, server, player_name):
        super().__init__(server, player_name)

    def use(self):
        pass

    def attack(self):
        pass
    
    def kill(self):
        pass

    def __del__(self):
        self.kill()
