from strategy.skills import Skill
from strategy.shield_effect import Shield
from strategy.stun_effect import Stun


# === GUERRIER ===

class CoupPuissant(Skill):
    """Attaque lourde qui inflige 2x les degats normaux"""
    def name(self) -> str:
        return "Coup puissant"
    
    def use(self, caster, target, ctx) -> None:
        dmg = max(1, (caster.stats.atk * 2) - target.stats.defense)
        target.take_damage(dmg)
        ctx.bus.publish("log", f"{caster.name} assène un Coup puissant à {target.name} ! ({dmg} dégâts)")


class ChargeHeroique(Skill):
    """Charge qui inflige des degats et peut etourdir"""
    def name(self) -> str:
        return "Charge héroïque"
    
    def use(self, caster, target, ctx) -> None:
        import random
        dmg = max(1, int(caster.stats.atk * 1.5) - target.stats.defense)
        target.take_damage(dmg)
        ctx.bus.publish("log", f"{caster.name} charge {target.name} ! ({dmg} dégâts)")
        # 40% de chance d etourdir
        if random.random() < 0.4:
            target.add_status(Stun())
            ctx.bus.publish("log", f"{target.name} est étourdi !")


# === MAGE ===

class BouclierArcanique(Skill):
    """Cree un bouclier qui absorbe des degats"""
    def name(self) -> str:
        return "Bouclier arcanique"
    
    def use(self, caster, target, ctx) -> None:
        shield_amount = 15 + caster.stats.intelligence
        caster.add_status(Shield(duration_turns=3, shield_amount=shield_amount))
        ctx.bus.publish("log", f"{caster.name} invoque un Bouclier arcanique ! ({shield_amount} pts d'absorption)")


# === VOLEUR ===

class AttaqueSournoise(Skill):
    """Attaque basee sur l agilite avec bonus de critique"""
    def name(self) -> str:
        return "Attaque sournoise"
    
    def use(self, caster, target, ctx) -> None:
        import random
        # utilise l agilite au lieu de l attaque
        base_dmg = max(1, caster.stats.agility * 2 - target.stats.defense)
        # chance de critique augmentée
        if random.random() < (caster.stats.crit_chance + 0.3):
            base_dmg *= 2
            ctx.bus.publish("log", "Coup critique sournois !")
        target.take_damage(base_dmg)
        ctx.bus.publish("log", f"{caster.name} frappe sournoisement {target.name} ! ({base_dmg} dégâts)")


class EsquiveParfaite(Skill):
    """Le voleur esquive la prochaine attaque + contre-attaque"""
    def name(self) -> str:
        return "Esquive parfaite"
    
    def use(self, caster, target, ctx) -> None:
        # met en defense + petite contre attaque
        caster.is_defending = True
        counter_dmg = max(1, caster.stats.agility - target.stats.defense)
        target.take_damage(counter_dmg)
        ctx.bus.publish("log", f"{caster.name} esquive et contre-attaque ! ({counter_dmg} dégâts)")
