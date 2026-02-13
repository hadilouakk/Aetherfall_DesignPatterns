"""
Gere les objets, l equipement (1 arme + 1 armure)
"""

MAX_SLOTS = 10


class Inventory:
    def __init__(self):
        self.items = []  # liste d objets (armes, armures, consommables)
        self.equipped_weapon = None
        self.equipped_armor = None
    
    def count(self):
        return len(self.items)
    
    def is_full(self):
        return self.count() >= MAX_SLOTS
    
    def add_item(self, item) -> bool:
        """Ajoute un objet. Retourne False si inventaire plein"""
        if self.is_full():
            return False
        self.items.append(item)
        return True
    
    def remove_item(self, item) -> bool:
        """Retire un objet de l inventaire"""
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    
    def equip_weapon(self, weapon, player):
        """Equipe une arme (la précédente retourne dans l inventaire)"""
        if weapon not in self.items:
            return False
        
        # desequiper l ancienne arme
        if self.equipped_weapon is not None:
            self.items.append(self.equipped_weapon)
        
        self.items.remove(weapon)
        self.equipped_weapon = weapon
        player.weapon = weapon
        return True
    
    def equip_armor(self, armor, player):
        """Equipe une armure"""
        if armor not in self.items:
            return False
        
        if self.equipped_armor is not None:
            self.items.append(self.equipped_armor)
        
        self.items.remove(armor)
        self.equipped_armor = armor
        player.armor = armor
        return True
    
    def use_consumable(self, consumable, player, target, ctx):
        """Utilise un consommable et le retire de l inventaire"""
        if consumable not in self.items:
            return False
        consumable.use(player, target, ctx)
        self.items.remove(consumable)
        return True
    
    def display(self):
        """Affiche le contenu de l inventaire"""
        print(f"\n=== Inventaire ({self.count()}/{MAX_SLOTS}) ===")
        if self.equipped_weapon:
            print(f"  [Arme] {self.equipped_weapon.name}")
        if self.equipped_armor:
            print(f"  [Armure] {self.equipped_armor.name}")
        if not self.items:
            print("  (vide)")
        for i, item in enumerate(self.items):
            print(f"  {i+1}. {item.name if hasattr(item, 'name') else item}")
        print()
    
    def to_dict(self):
        """Serialisation pour la sauvegarde"""
        data = {
            "items": [],
            "equipped_weapon": None,
            "equipped_armor": None
        }
        for item in self.items:
            data["items"].append({"name": item.name, "type": type(item).__name__})
        if self.equipped_weapon:
            data["equipped_weapon"] = {"name": self.equipped_weapon.name, "type": "Weapon"}
        if self.equipped_armor:
            data["equipped_armor"] = {"name": self.equipped_armor.name, "type": "Armor"}
        return data
