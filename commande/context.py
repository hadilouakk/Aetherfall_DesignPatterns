class Battle:
    def __init__(self, player,enemy,bus,damage_system):
        self.player = player
        self.enemy = enemy
        self.bus = bus
        self.damage_system = damage_system
        self.turn = 1 