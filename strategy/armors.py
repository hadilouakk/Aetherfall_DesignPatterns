"""
Armures du jeu
"""
from dataclasses import dataclass


@dataclass
class Armor:
    name: str
    def_bonus: int = 0
    int_bonus: int = 0

# armures de base du jeu
LEATHER_ARMOR = Armor("Armure de cuir", def_bonus=3)
MYSTIC_ROBE = Armor("Robe mystique", def_bonus=2, int_bonus=3)
IRON_PLATE = Armor("Plastron de fer", def_bonus=6)
