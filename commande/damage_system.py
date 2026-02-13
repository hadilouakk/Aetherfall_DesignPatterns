import random

class DamageSystem:
    def compute_basic_attack(self, attacker, defender, ctx) -> int:
        atk = attacker.get_atk_total() if hasattr(attacker, "get_atk_total") else attacker.stats.atk
        crit = attacker.get_crit_total() if hasattr(attacker, "get_crit_total") else attacker.stats.crit_chance
        base = max(1, attacker.stats.atk - defender.stats.defense)

        if random.random() < attacker.stats.crit_chance:
            base *= 2
            ctx.bus.publish("log", "Coup critique !")

        if defender.is_defending:
            base= base //2
            ctx.bus.publish("log",f"{defender.name} reduit les degats")

        if getattr(defender, "is_defending", False):
            base //= 2
            ctx.bus.publish("log", f"{defender.name} réduit les dégâts !")

        return max(1, base)
        