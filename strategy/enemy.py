from dataclasses import dataclass
from strategy.enemyAI import Agressive

@dataclass
class Stats:
    hp_max: int
    atk: int
    intelligence: int
    defense: int
    agility: int
    crit_chance: float
    


class Enemy:
    def __init__(self, name: str, level: int, stats: Stats, reward_gold: int,ai=None):
        self.name = name
        self.level = level
        self.stats = stats
        self.reward_gold = reward_gold
        self.hp_current = stats.hp_max
        self.ai = ai
        self.is_defending =False 
        self.statuses = []
        self.shield_points = 0
        self.weapon = None

    def is_alive(self) -> bool:
        return self.hp_current > 0
    def take_damage (self, amount: int):
        self.hp_current = max(0, self.hp_current- amount)
    def decide(self, ctx):
        if self.ai is None:
            raise ValueError("Enemy AI not set")
        return self.ai.choose_action(ctx)
    def add_status(self, status):
        self.statuses.append(status)
    def apply_end_turn_statuses(self, ctx):
       for s in self.statuses[:]:
        s.on_end_turn(self, ctx)
        s.tick()
        if s.is_expired():
            self.statuses.remove(s)
            ctx.bus.publish("log", f"Effet terminé sur {self.name}.")
    def equip_weapon(self, weapon):
        self.weapon = weapon

def get_atk_total(self):
    return self.stats.atk + (self.weapon.atk_bonus if self.weapon else 0)

def get_int_total(self):
    return self.stats.intelligence + (self.weapon.int_bonus if self.weapon else 0)

def get_crit_total(self):
    return self.stats.crit_chance + (self.weapon.crit_bonus if self.weapon else 0.0)        





class Wolf(Enemy):
    def __init__(self):
        super().__init__("Wolf", 1, Stats(50, 8, 0, 3, 7, 0.10), 10,ai=Agressive())

class Skeleton(Enemy):
    def __init__(self):
        super().__init__("Skeleton", 2, Stats(60, 10, 0, 5, 4, 0.05), 15,ai=Agressive())

class Bandit(Enemy):
    def __init__(self):
        super().__init__("Bandit", 2, Stats(55, 12, 0, 4, 10, 0.15), 20,ai=Agressive())