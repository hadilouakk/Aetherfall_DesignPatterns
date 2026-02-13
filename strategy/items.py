from dataclasses import dataclass

@dataclass
class Weapon:
    name: str
    atk_bonus: int = 0
    int_bonus: int = 0
    crit_bonus: float = 0.0