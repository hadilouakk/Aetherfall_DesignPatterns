from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Stats:
    hp_max: int
    atk: int
    agility: int
    crit_chance:float

class Player(ABC):
    @abstractmethod
    def base_stats(self) -> Stats :
        ...

class Warrior (Player):
    def base_stats(self) -> Stats:
        return Stats (120,15,18,10,9,4,0.1) 
class MageClass(Player):
    def base_stats(self) -> Stats:
        return Stats(80, 5, 18, 4, 8, 0.15)

class ThiefClass(Player):
    def base_stats(self) -> Stats:
        return Stats(90, 12, 6, 6, 15, 0.25)