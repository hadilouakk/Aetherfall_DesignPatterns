from strategy.enemy import Enemy, Stats
from strategy.enemyAI import Agressive
from strategy.status_effects import Poison


class BossAI:
    """IA du boss - change de comportement selon la phase"""
    def choose_action(self, ctx):
        from commande.commands import AttackCommand
        return AttackCommand(attacker=ctx.enemy, target=ctx.player)


class CorruptedChampion(Enemy):
    """Ennemi élite avec PV élevés et capacité spéciale"""
    def __init__(self):
        super().__init__(
            "Champion Corrompu", 4,
            Stats(120, 16, 5, 8, 6, 0.15),
            reward_gold=50,
            ai=Agressive()
        )
    
    def decide(self, ctx):
        # 30% de chance d appliquer poison au joueur
        import random
        if random.random() < 0.3 and not any(isinstance(s, Poison) for s in ctx.player.statuses):
            ctx.player.add_status(Poison(duration_turns=2, dmg_per_turn=3))
            ctx.bus.publish("log", f"{self.name} empoisonne {ctx.player.name} !")
        return self.ai.choose_action(ctx)


class DungeonGuardian(Enemy):
    """Boss final avec 2 phases de combat"""
    def __init__(self):
        super().__init__(
            "Gardien du Donjon", 5,
            Stats(200, 18, 10, 10, 5, 0.10),
            reward_gold=100,
            ai=BossAI()
        )
        self.phase = 1
        self.phase2_triggered = False
    
    def _enter_phase2(self, ctx):
        """Passe en phase 2 quand PV < 50%"""
        self.phase2_triggered = True
        self.phase = 2
        # boost des stats en phase 2
        self.stats.atk += 5
        self.stats.defense -= 3  # plus agressif, moins defensif
        self.stats.crit_chance = 0.25
        ctx.bus.publish("log", "")
        ctx.bus.publish("log", "=== LE GARDIEN ENTRE EN PHASE 2 ===")
        ctx.bus.publish("log", f"{self.name} devient enragé ! ATK augmentée, DEF réduite !")

    def decide(self, ctx):
        # check si on passe en phase 2
        if not self.phase2_triggered and self.hp_current <= self.stats.hp_max * 0.5:
            self._enter_phase2(ctx)
        
        from commande.commands import AttackCommand
        import random
        
        if self.phase == 2:
            # en phase 2 il peut attaquer 2 fois (25% de chance)
            if random.random() < 0.25:
                ctx.bus.publish("log", f"{self.name} déchaîne une attaque double !")
                cmd = AttackCommand(attacker=self, target=ctx.player)
                cmd.execute(ctx)
            # poison en phase 2
            if random.random() < 0.4 and not any(isinstance(s, Poison) for s in ctx.player.statuses):
                ctx.player.add_status(Poison(duration_turns=3, dmg_per_turn=4))
                ctx.bus.publish("log", f"{self.name} empoisonne {ctx.player.name} !")
        
        return AttackCommand(attacker=self, target=ctx.player)
