from abc import ABC , abstractmethod
from commande.commands import AttackCommand

class EnemyAi(ABC):
    
    @abstractmethod
    def choose_action (self, ctx) :
        ...

class Agressive (EnemyAi):
    def choose_action(self, ctx) :
        from commande.commands import AttackCommand
        return AttackCommand (attacker=ctx.enemy, target=ctx.player)
    
class defensive (EnemyAi):
    def choose_action(self, ctx) :
        if ctx.enemy.hp_current <= ctx.enemy.stats.hp_max * 0.3:
            return AttackCommand (attacker =ctx.enemy, target=ctx.player)
        return AttackCommand (attacker= ctx.enemy, target= ctx.player)