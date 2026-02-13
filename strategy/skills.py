from abc import ABC,abstractmethod
class Skill(ABC):
    @abstractmethod
    def name (self) -> str:
        ...

    @abstractmethod 
    def  use (self, caster, target, ctx) -> None:
        ...

class Fireball (Skill):
    def name(self) -> str:
        return "Fireball"
    def use (self, caster, target, ctx) -> None:
        dmg = max(1, caster.stats.intelligence *2 - target.stats.defense)
        target.take_damage(dmg)
        ctx.bus.publish("log", f"{caster.name} lance Fireball sur {target.name} ({dmg} dégats)")



