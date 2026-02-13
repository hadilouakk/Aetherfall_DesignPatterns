from abc import ABC, abstractmethod


class Consumable(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def use(self, user, target, ctx):
        """Appliquer l effet de l objet"""
        ...

    def __repr__(self):
        return f"{self.name}"


class HealthPotion(Consumable):
    def __init__(self):
        super().__init__("Potion de soin", "Restaure 30 PV")
        self.heal_amount = 30
    
    def use(self, user, target, ctx):
        old_hp = user.hp_current
        user.hp_current = min(user.stats.hp_max, user.hp_current + self.heal_amount)
        healed = user.hp_current - old_hp
        ctx.bus.publish("log", f"{user.name} utilise {self.name} et récupère {healed} PV !")


class Antidote(Consumable):
    def __init__(self):
        super().__init__("Antidote", "Retire le poison")
    
    def use(self, user, target, ctx):
        from strategy.status_effects import Poison
        before = len(user.statuses)
        user.statuses = [s for s in user.statuses if not isinstance(s, Poison)]
        if len(user.statuses) < before:
            ctx.bus.publish("log", f"{user.name} utilise un Antidote. Poison retiré !")
        else:
            ctx.bus.publish("log", f"{user.name} utilise un Antidote... mais n'était pas empoisonné.")


class Bomb(Consumable):
    """Inflige des degats fixes a l ennemi"""
    def __init__(self):
        super().__init__("Bombe", "Inflige 25 dégâts")
        self.damage = 25
    
    def use(self, user, target, ctx):
        target.take_damage(self.damage)
        ctx.bus.publish("log", f"{user.name} lance une Bombe sur {target.name} ! ({self.damage} dégâts)")
