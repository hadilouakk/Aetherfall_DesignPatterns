from strategy.items import Weapon

class WeaponFactory:
    @staticmethod
    def create(weapon_type: str) -> Weapon:
        mapping = {
            "sword": Weapon("Épée", atk_bonus=5, crit_bonus=0.05),
            "staff": Weapon("Bâton", int_bonus=6, crit_bonus=0.02),
            "dagger": Weapon("Dague", atk_bonus=3, crit_bonus=0.10),
        }
        if weapon_type not in mapping:
            raise ValueError(f"Unknown weapon type: {weapon_type}")
        return mapping[weapon_type]