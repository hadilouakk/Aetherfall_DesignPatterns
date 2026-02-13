from abc import ABC, abstractmethod
import random
from factory.enemy_factory import EnemyFactory
from strategy.consumables import HealthPotion, Bomb, Antidote


class Event(ABC):
    @abstractmethod
    def trigger(self, player, inventory, quest, bus):
        """Déclenche l événement"""
        ...


class CombatEvent(Event):
    """Rencontre aleatoire avec un ennemi"""
    def __init__(self, enemy_type=None):
        self.enemy_type = enemy_type
    
    def trigger(self, player, inventory, quest, bus):
        if self.enemy_type:
            enemy = EnemyFactory.create(self.enemy_type)
        else:
            # ennemi aleatoire
            enemy = EnemyFactory.create(random.choice(["wolf", "skelton", "bandit"]))
        
        bus.publish("log", f"\n Un {enemy.name} apparaît !")
        return {"type": "combat", "enemy": enemy}


class ChestEvent(Event):
    """Coffre avec objet ou or aleatoire"""
    def __init__(self, chest_id=None, contains_key=False):
        self.chest_id = chest_id or f"chest_{random.randint(100,999)}"
        self.contains_key = contains_key
    
    def trigger(self, player, inventory, quest, bus):
        if self.contains_key:
            bus.publish("log", "\n Vous trouvez un coffre ancien...")
            bus.publish("log", " Il contient la Clé du Donjon !")
            quest.advance("key_found")
            return {"type": "key_found"}
        
        # loot aleatoire
        loot_table = [
            (HealthPotion(), "une Potion de soin"),
            (Bomb(), "une Bombe"),
            (Antidote(), "un Antidote"),
        ]
        item, desc = random.choice(loot_table)
        
        if inventory.is_full():
            bus.publish("log", f"\n Coffre trouvé contenant {desc}... mais votre inventaire est plein !")
            return {"type": "chest_full"}
        
        inventory.add_item(item)
        bus.publish("log", f"\n Coffre trouvé ! Vous obtenez {desc}.")
        
        gold = random.randint(5, 20)
        bus.publish("log", f" + {gold} pièces d'or")
        return {"type": "chest", "item": item, "gold": gold}


class MerchantEvent(Event):
    """Marchand qui vend des objets"""
    def trigger(self, player, inventory, quest, bus):
        bus.publish("log", "\n Un marchand ambulant vous interpelle !")
        bus.publish("log", " 'Bonjour voyageur, j'ai des marchandises qui pourraient vous intéresser...'")
        return {"type": "merchant"}


class DialogueEvent(Event):
    """Interaction narrative avec un PNJ"""
    def __init__(self, npc_name, dialogue, quest_trigger=None):
        self.npc_name = npc_name
        self.dialogue = dialogue
        self.quest_trigger = quest_trigger
    
    def trigger(self, player, inventory, quest, bus):
        bus.publish("log", f"\n {self.npc_name} : \"{self.dialogue}\"")
        if self.quest_trigger:
            quest.advance(self.quest_trigger)
        return {"type": "dialogue", "npc": self.npc_name}


class EventFactory:
    """Genere des evenements aleatoires selon la zone"""
    
    @staticmethod
    def random_forest_event():
        roll = random.random()
        if roll < 0.5:
            return CombatEvent()
        elif roll < 0.75:
            return ChestEvent()
        elif roll < 0.90:
            # coffre special avec la clé (si pas encore trouvée)
            return ChestEvent(chest_id="key_chest", contains_key=True)
        else:
            return MerchantEvent()
    
    @staticmethod
    def random_dungeon_event():
        roll = random.random()
        if roll < 0.7:
            return CombatEvent(enemy_type=random.choice(["skelton", "bandit"]))
        else:
            return ChestEvent()
