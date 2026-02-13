from observer.event_bus import EventBus
from observer.console_logger import ConsoleLogger
from factory.enemy_factory import EnemyFactory
from commande.commands import AttackCommand
from commande.context import Battle
from commande.damage_system import DamageSystem
from commande.combat_engine import CombatEngine
from strategy.enemy import Enemy, Stats

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

    player = Enemy("Hero", 1, Stats(100, 14, 0, 6, 7, 0.2), reward_gold=0)

    ctx = Battle(player=player, enemy=enemy, bus=bus, damage_system=DamageSystem())
    engine = CombatEngine()

    
    def player_provider(ctx):
        if ctx.turn ==1:
            from commande.commands import DefendCommand
            return DefendCommand (ctx.player)
        return AttackCommand(attacker=ctx.player, target=ctx.enemy)

    engine.run(ctx, player_provider)


if __name__ == "__main__":
    test_observer()
    test_factory ()
    test_command ()
    test_combat_engine()