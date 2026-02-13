from abc import ABC,abstractmethod
class Command (ABC):
    @abstractmethod
    def execute (self,ctx) ->None:
        ...

class AttackCommand (Command):
    def __init__ (self,attacker,target):
        self.attacker = attacker
        self.target = target   

    def execute(self,ctx) -> None: 
        dmg = ctx.damage_system.compute_basic_attack (self.attacker, self.target, ctx)
        self.target.take_damage(dmg)
        ctx.bus.publish ("log", f"{self.attacker.name} attaque {self.target.name} et inflige {dmg} degats."
                        f"(HP {self.target.name}: {self.target.hp_current})" 

                        )   


class DefendCommand(Command):
    def reset_defense(self):    
        self.is_defending = False

    def __init__(self,defender):
        self.defender = defender
    def execute (self,ctx) -> None:
        self.defender.is_defending = True
        ctx.bus.publish("log",f"{self.defender.name} est en defense")



