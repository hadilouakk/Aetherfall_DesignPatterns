from abc import ABC, abstractmethod
from exploration.events import (
    CombatEvent, ChestEvent, MerchantEvent, 
    DialogueEvent, EventFactory
)


class Zone(ABC):
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    @abstractmethod
    def get_actions(self, quest):
        """Retourne les actions possibles dans cette zone"""
        ...
    
    @abstractmethod
    def explore(self, player, inventory, quest, bus):
        """Genere un evenement dans la zone"""
        ...


class Village(Zone):
    def __init__(self):
        super().__init__("Village", "Le hub central. Un endroit paisible avec un marchand et des PNJ.")
    
    def get_actions(self, quest):
        actions = ["Parler au villageois", "Visiter le marchand", "Partir vers la Forêt"]
        if quest.can_enter_dungeon():
            actions.append("Partir vers le Donjon")
        return actions
    
    def explore(self, player, inventory, quest, bus):
        # le village est une zone safe, pas de combat aleatoire
        npc = DialogueEvent(
            "Ancien du village",
            "Des ombres étranges rôdent dans la Forêt... "
            "On dit qu'une clé ancienne s'y trouve, ouvrant les portes du Donjon maudit.",
            quest_trigger=None
        )
        return npc.trigger(player, inventory, quest, bus)


class Forest(Zone):
    def __init__(self):
        super().__init__("Forêt", "Zone dangereuse avec des ennemis et des coffres cachés.")
        self.key_chest_opened = False
    
    def get_actions(self, quest):
        actions = ["Explorer (événement aléatoire)", "Retourner au Village"]
        if quest.can_enter_dungeon():
            actions.append("Aller au Donjon")
        return actions
    
    def explore(self, player, inventory, quest, bus):
        import random
        
        # si la clé n a pas encore été trouvée, chance de tomber sur le coffre de la clé
        if not quest.has_dungeon_key and not self.key_chest_opened:
            if random.random() < 0.25:
                self.key_chest_opened = True
                event = ChestEvent(chest_id="key_chest", contains_key=True)
                return event.trigger(player, inventory, quest, bus)
        
        event = EventFactory.random_forest_event()
        # eviter de redonner la clé si deja trouvée
        if isinstance(event, ChestEvent) and event.contains_key and quest.has_dungeon_key:
            event = CombatEvent()
        
        return event.trigger(player, inventory, quest, bus)


class Dungeon(Zone):
    def __init__(self):
        super().__init__("Donjon", "Le donjon maudit. Le Gardien vous attend au fond.")
        self.rooms_cleared = 0
        self.total_rooms = 2  # 2 salles avant le boss
    
    def get_actions(self, quest):
        if self.rooms_cleared < self.total_rooms:
            return ["Avancer dans le donjon", "Retourner au Village"]
        else:
            return ["Affronter le Gardien du Donjon", "Retourner au Village"]
    
    def explore(self, player, inventory, quest, bus):
        if self.rooms_cleared < self.total_rooms:
            self.rooms_cleared += 1
            bus.publish("log", f"\n--- Salle {self.rooms_cleared}/{self.total_rooms} ---")
            event = EventFactory.random_dungeon_event()
            return event.trigger(player, inventory, quest, bus)
        else:
            # boss fight
            bus.publish("log", "\n=== SALLE DU BOSS ===")
            bus.publish("log", "Le Gardien du Donjon se dresse devant vous !")
            from strategy.boss import DungeonGuardian
            boss = DungeonGuardian()
            return {"type": "combat", "enemy": boss, "is_boss": True}
