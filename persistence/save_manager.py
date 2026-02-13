import json
import os

SAVE_FILE = "savegame.json"


class SaveManager:
    
    @staticmethod
    def save(player, inventory, quest, current_zone="village"):
        """Sauvegarde l etat complet du jeu en JSON"""
        data = {
            "player": {
                "name": player.name,
                "level": player.level,
                "hp_current": player.hp_current,
                "hp_max": player.stats.hp_max,
                "atk": player.stats.atk,
                "intelligence": player.stats.intelligence,
                "defense": player.stats.defense,
                "agility": player.stats.agility,
                "crit_chance": player.stats.crit_chance,
            },
            "inventory": inventory.to_dict(),
            "quest": quest.to_dict(),
            "current_zone": current_zone,
        }
        
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erreur de sauvegarde : {e}")
            return False
    
    @staticmethod
    def load():
        """Charge une sauvegarde depuis le fichier JSON"""
        if not os.path.exists(SAVE_FILE):
            return None
        
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except (json.JSONDecodeError, IOError) as e:
            print(f"Erreur de chargement : {e}")
            return None
    
    @staticmethod
    def save_exists():
        return os.path.exists(SAVE_FILE)
    
    @staticmethod
    def delete_save():
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
