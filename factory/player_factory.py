from strategy.enemy import Enemy, Stats
from strategy.class_skills import (
    CoupPuissant, ChargeHeroique,
    BouclierArcanique, AttaqueSournoise, EsquiveParfaite
)
from strategy.skills import Fireball


class PlayerFactory:
    
    @staticmethod
    def create(name: str, class_type: str) -> Enemy:
        """Cree un joueur selon la classe choisie"""
        
        if class_type == "guerrier":
            player = Enemy(
                name=name, level=1,
                stats=Stats(hp_max=120, atk=15, intelligence=4, defense=10, agility=6, crit_chance=0.10),
                reward_gold=0
            )
            player.skills = [CoupPuissant(), ChargeHeroique()]
            player.player_class = "Guerrier"
        
        elif class_type == "mage":
            player = Enemy(
                name=name, level=1,
                stats=Stats(hp_max=80, atk=5, intelligence=18, defense=5, agility=8, crit_chance=0.05),
                reward_gold=0
            )
            player.skills = [Fireball(), BouclierArcanique()]
            player.player_class = "Mage"
        
        elif class_type == "voleur":
            player = Enemy(
                name=name, level=1,
                stats=Stats(hp_max=95, atk=12, intelligence=6, defense=6, agility=16, crit_chance=0.25),
                reward_gold=0
            )
            player.skills = [AttaqueSournoise(), EsquiveParfaite()]
            player.player_class = "Voleur"
        
        else:
            raise ValueError(f"Classe inconnue: {class_type}")
        
        return player
