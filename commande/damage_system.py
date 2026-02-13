import random

class DamageSystem:
    def compute_basic_attack(self, attacker, defender, ctx) -> int:
        base = max(1, attacker.stats.atk - defender.stats.defense)

        if random.random() < attacker.stats.crit_chance:
            base *= 2
            ctx.bus.publish("log", "Coup critique !")

        return base
        if defender.is_defending:
            base= base //2
            ctx.bus.publish("log",f"{defender.name} reduit les degats")