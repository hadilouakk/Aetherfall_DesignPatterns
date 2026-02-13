"""
Tests unitaires - Aetherfall
Couvre : combat, statuts, inventaire, evenements, sauvegarde, quete
"""
import unittest
import sys
import os

# ajouter le dossier parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strategy.enemy import Enemy, Stats
from strategy.status_effects import Poison
from strategy.shield_effect import Shield
from strategy.stun_effect import Stun
from strategy.inventory import Inventory
from strategy.consumables import HealthPotion, Bomb, Antidote
from strategy.items import Weapon
from strategy.armors import Armor
from strategy.boss import DungeonGuardian, CorruptedChampion
from exploration.quest import MainQuest, QuestState
from persistence.save_manager import SaveManager
from observer.event_bus import EventBus
from observer.console_logger import ConsoleLogger
from commande.context import Battle
from commande.damage_system import DamageSystem
from commande.commands import AttackCommand, DefendCommand
from factory.player_factory import PlayerFactory
from factory.enemy_factory import EnemyFactory


def make_bus():
    """Helper pour creer un bus silencieux (pas de print dans les tests)"""
    bus = EventBus()
    # on subscribe rien pour pas polluer la sortie
    return bus


def make_ctx(player, enemy, bus=None):
    if bus is None:
        bus = make_bus()
    return Battle(player=player, enemy=enemy, bus=bus, damage_system=DamageSystem())


class TestCombat(unittest.TestCase):
    """Test 1 : systeme de combat de base"""
    
    def test_attack_reduces_hp(self):
        player = Enemy("Hero", 1, Stats(100, 15, 0, 8, 5, 0.0), 0)
        enemy = EnemyFactory.create("wolf")
        ctx = make_ctx(player, enemy)
        
        hp_before = enemy.hp_current
        cmd = AttackCommand(player, enemy)
        cmd.execute(ctx)
        
        self.assertLess(enemy.hp_current, hp_before, "L'attaque doit reduire les PV")
    
    def test_defend_reduces_damage(self):
        player = Enemy("Hero", 1, Stats(100, 15, 0, 8, 5, 0.0), 0)
        enemy = Enemy("TestMob", 1, Stats(50, 20, 0, 0, 5, 0.0), 0)
        ctx = make_ctx(player, enemy)
        
        # sans defense
        cmd = AttackCommand(enemy, player)
        cmd.execute(ctx)
        hp_after_no_def = player.hp_current
        dmg_no_def = 100 - hp_after_no_def
        
        # reset
        player.hp_current = 100
        player.is_defending = True
        cmd.execute(ctx)
        hp_after_def = player.hp_current
        dmg_with_def = 100 - hp_after_def
        
        self.assertLessEqual(dmg_with_def, dmg_no_def, "La defense doit reduire les degats")


class TestStatuts(unittest.TestCase):
    """Test 2 : application des effets de statut"""
    
    def test_poison_deals_damage(self):
        enemy = Enemy("Mob", 1, Stats(50, 5, 0, 2, 3, 0.0), 0)
        bus = make_bus()
        # on subscribe un logger muet
        bus.subscribe("log", lambda msg: None)
        ctx = make_ctx(enemy, enemy, bus)
        
        poison = Poison(duration_turns=3, dmg_per_turn=5)
        enemy.add_status(poison)
        
        hp_before = enemy.hp_current
        enemy.apply_end_turn_statuses(ctx)
        
        self.assertEqual(enemy.hp_current, hp_before - 5, "Le poison doit infliger 5 degats")
    
    def test_poison_expires(self):
        enemy = Enemy("Mob", 1, Stats(50, 5, 0, 2, 3, 0.0), 0)
        bus = make_bus()
        bus.subscribe("log", lambda msg: None)
        ctx = make_ctx(enemy, enemy, bus)
        
        poison = Poison(duration_turns=2, dmg_per_turn=3)
        enemy.add_status(poison)
        
        # tour 1
        enemy.apply_end_turn_statuses(ctx)
        # tour 2
        enemy.apply_end_turn_statuses(ctx)
        
        self.assertEqual(len(enemy.statuses), 0, "Le poison doit expirer apres 2 tours")
    
    def test_stun_skip_turn(self):
        stun = Stun()
        self.assertTrue(stun.should_skip_turn(), "L'etourdissement doit faire passer le tour")
    
    def test_shield_absorbs(self):
        shield = Shield(duration_turns=3, shield_amount=20)
        remaining = shield.absorb(15)
        self.assertEqual(remaining, 0, "Le bouclier doit absorber 15 degats")
        self.assertEqual(shield.shield_amount, 5, "Il doit rester 5 pts de bouclier")


class TestInventaire(unittest.TestCase):
    """Test 3 : gestion de l inventaire"""
    
    def test_add_item(self):
        inv = Inventory()
        potion = HealthPotion()
        result = inv.add_item(potion)
        self.assertTrue(result)
        self.assertEqual(inv.count(), 1)
    
    def test_inventory_limit(self):
        inv = Inventory()
        for i in range(10):
            inv.add_item(HealthPotion())
        
        # le 11eme doit echouer
        result = inv.add_item(Bomb())
        self.assertFalse(result, "L'inventaire ne doit pas depasser 10 slots")
        self.assertEqual(inv.count(), 10)
    
    def test_equip_weapon(self):
        inv = Inventory()
        player = Enemy("Hero", 1, Stats(100, 10, 0, 5, 5, 0.1), 0)
        sword = Weapon("Epee", atk_bonus=5)
        inv.add_item(sword)
        
        inv.equip_weapon(sword, player)
        self.assertEqual(inv.equipped_weapon, sword)
        self.assertEqual(player.weapon, sword)
        self.assertEqual(inv.count(), 0, "L'arme equipee ne doit plus etre dans l inventaire")
    
    def test_equip_armor(self):
        inv = Inventory()
        player = Enemy("Hero", 1, Stats(100, 10, 0, 5, 5, 0.1), 0)
        armor = Armor("Cuir", def_bonus=3)
        inv.add_item(armor)
        
        inv.equip_armor(armor, player)
        self.assertEqual(inv.equipped_armor, armor)
    
    def test_use_consumable(self):
        inv = Inventory()
        player = Enemy("Hero", 1, Stats(100, 10, 0, 5, 5, 0.1), 0)
        player.hp_current = 50
        enemy = Enemy("Mob", 1, Stats(30, 5, 0, 2, 3, 0.0), 0)
        
        potion = HealthPotion()
        inv.add_item(potion)
        
        bus = make_bus()
        bus.subscribe("log", lambda msg: None)
        ctx = make_ctx(player, enemy, bus)
        
        inv.use_consumable(potion, player, enemy, ctx)
        self.assertGreater(player.hp_current, 50, "La potion doit soigner")
        self.assertEqual(inv.count(), 0, "La potion doit etre consommée")


class TestQuete(unittest.TestCase):
    """Test 4 : progression de la quete"""
    
    def test_initial_state(self):
        q = MainQuest()
        self.assertEqual(q.state, QuestState.NOT_STARTED)
        self.assertFalse(q.can_enter_dungeon())
    
    def test_find_key(self):
        q = MainQuest()
        q.advance("key_found")
        self.assertEqual(q.state, QuestState.KEY_FOUND)
        self.assertTrue(q.can_enter_dungeon())
    
    def test_boss_defeated(self):
        q = MainQuest()
        q.advance("key_found")
        q.advance("boss_defeated")
        self.assertTrue(q.is_completed())
    
    def test_cant_skip_steps(self):
        q = MainQuest()
        # essayer de vaincre le boss sans avoir la clé
        q.advance("boss_defeated")
        self.assertEqual(q.state, QuestState.NOT_STARTED, "On ne peut pas skip des etapes")


class TestSauvegarde(unittest.TestCase):
    """Test 5 : sauvegarde et chargement JSON"""
    
    def setUp(self):
        # nettoyer la sauvegarde avant chaque test
        if os.path.exists("savegame.json"):
            os.remove("savegame.json")
    
    def tearDown(self):
        if os.path.exists("savegame.json"):
            os.remove("savegame.json")
    
    def test_save_and_load(self):
        player = Enemy("TestHero", 1, Stats(100, 15, 8, 7, 6, 0.1), 0)
        inv = Inventory()
        inv.add_item(HealthPotion())
        quest = MainQuest()
        quest.advance("key_found")
        
        # sauvegarder
        result = SaveManager.save(player, inv, quest, "forest")
        self.assertTrue(result)
        
        # charger
        data = SaveManager.load()
        self.assertIsNotNone(data)
        self.assertEqual(data["player"]["name"], "TestHero")
        self.assertEqual(data["quest"]["state"], QuestState.KEY_FOUND)
        self.assertEqual(data["current_zone"], "forest")
    
    def test_load_nonexistent(self):
        data = SaveManager.load()
        self.assertIsNone(data)


class TestBoss(unittest.TestCase):
    """Test 6 : boss avec 2 phases"""
    
    def test_boss_phase2_trigger(self):
        boss = DungeonGuardian()
        player = Enemy("Hero", 1, Stats(100, 15, 0, 8, 5, 0.0), 0)
        bus = make_bus()
        bus.subscribe("log", lambda msg: None)
        ctx = make_ctx(player, boss, bus)
        
        # reduire les PV en dessous de 50%
        boss.hp_current = 90  # en dessous de 100 (50% de 200)
        boss.decide(ctx)
        
        self.assertEqual(boss.phase, 2, "Le boss doit passer en phase 2")
        self.assertTrue(boss.phase2_triggered)


class TestPlayerFactory(unittest.TestCase):
    """Test 7 : creation des classes de personnage"""
    
    def test_create_guerrier(self):
        p = PlayerFactory.create("Test", "guerrier")
        self.assertEqual(p.stats.hp_max, 120)
        self.assertEqual(len(p.skills), 2)
        self.assertEqual(p.player_class, "Guerrier")
    
    def test_create_mage(self):
        p = PlayerFactory.create("Test", "mage")
        self.assertEqual(p.stats.intelligence, 18)
        self.assertEqual(len(p.skills), 2)
    
    def test_create_voleur(self):
        p = PlayerFactory.create("Test", "voleur")
        self.assertEqual(p.stats.agility, 16)
        self.assertEqual(p.stats.crit_chance, 0.25)


if __name__ == "__main__":
    unittest.main()
