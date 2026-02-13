from observer.event_bus import EventBus
from observer.console_logger import ConsoleLogger
from factory.enemy_factory import EnemyFactory
from commande.commands import AttackCommand
from commande.context import Battle
from commande.damage_system import DamageSystem
from commande.combat_engine import CombatEngine
from strategy.enemy import Enemy, Stats
from commande.commands import AttackCommand
from strategy.skills import Fireball
from commande.skill_command import SkillCommand
from strategy.status_effects import Poison
from factory.weapon_factory import WeaponFactory
from commande.equipe import EquipWeaponCommand
from commande.commands import DefendCommand

def test_observer():
    bus = EventBus()
    bus.subscribe("log", ConsoleLogger())

    bus.publish("log", "Observer OK : j'affiche un message")
    bus.publish("log", "Deuxième message")
    bus.publish("other", "Ce message ne s'affiche pas car pas d'abonné")


def test_factory ():
    enemy = EnemyFactory.create("wolf")
    print(enemy.name, enemy.stats.hp_max)
    
  

def test_command ():
    bus = EventBus ()
    bus.subscribe("log", ConsoleLogger())
    enemy = EnemyFactory.create("wolf")

    from strategy.enemy import Enemy, Stats
    player = Enemy("Hero", 1, Stats(100, 14, 0, 6, 7, 0.2), reward_gold=0)
    
    ctx = Battle(player=player, enemy=enemy, bus=bus, damage_system=DamageSystem())

    AttackCommand(player, enemy).execute(ctx)

def test_combat_engine():
    bus = EventBus()
    bus.subscribe("log", ConsoleLogger())

    enemy = EnemyFactory.create("wolf")
    enemy.add_status(Poison(duration_turns=3, dmg_per_turn=2))
    name = input("Nom du joueur : ").strip()
    if not name:
        name = "Hero"
    
  

    player = Enemy(name, 1, Stats(100, 14, 0, 6, 7, 0.2), reward_gold=0)

    ctx = Battle(player=player, enemy=enemy, bus=bus, damage_system=DamageSystem())
    print("\nChoisis ton arme :")
    print("1) Épée (+5 ATK, +5% crit)")
    print("2) Bâton (+6 INT, +2% crit)")
    print("3) Dague (+3 ATK, +10% crit)")

    choice = input("> ").strip()
    weapon_type = {"1": "sword", "2": "staff", "3": "dagger"}.get(choice, "sword")

    weapon = WeaponFactory.create(weapon_type)
    EquipWeaponCommand(player, weapon).execute(ctx)
    engine = CombatEngine()

    
    def player_provider(ctx):
        action = input ("> ").strip()
        if action == "2":
            return DefendCommand (ctx.player)
        else : 
            
            ##return  SkillCommand(Fireball(), ctx.player, ctx.enemy)
         return AttackCommand(attacker=ctx.player, target=ctx.enemy)

    engine.run(ctx, player_provider)

if __name__ == "__main__":
    test_observer()
    test_factory ()
    test_command ()
    test_combat_engine()
    
