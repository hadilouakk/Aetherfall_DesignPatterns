# Aetherfall – Mini RPG (Design Patterns)

## Description

Aetherfall est un mini RPG en console développé en Python dans le cadre du module Design Patterns (Master 2).
Le joueur choisit une classe (Guerrier, Mage ou Voleur), explore trois zones, combat des ennemis en tour par tour,
gère son inventaire et progresse dans une quête principale jusqu'au boss final.

Le projet met en œuvre plusieurs patterns d'architecture logicielle pour garder le code extensible et maintenable.

## Lancer le projet

```bash
git clone https://github.com/hadilouakk/Aetherfall_DesignPatterns.git
cd Aetherfall_DesignPatterns
python main.py
```

## Lancer les tests

```bash
python -m unittest tests.test_aetherfall -v
```

## Architecture du projet

```
Aetherfall_DesignPatterns/
├── main.py                  # Point d'entrée
├── commande/
│   ├── commands.py          # Command ABC, AttackCommand, DefendCommand
│   ├── combat_engine.py     # Boucle de combat tour par tour
│   ├── context.py           # Contexte de bataille (Battle)
│   ├── damage_system.py     # Calcul des dégâts, critiques, défense
│   ├── equipe.py            # EquipWeaponCommand
│   ├── skill_command.py     # SkillCommand
│   └── use_item_command.py  # UseItemCommand (consommables)
├── factory/
│   ├── enemy_factory.py     # Création des ennemis
│   ├── weapon_factory.py    # Création des armes
│   └── player_factory.py    # Création Guerrier / Mage / Voleur
├── observer/
│   ├── event_bus.py         # Pub/sub pour les événements
│   └── console_logger.py    # Affichage découplé
├── strategy/
│   ├── enemy.py             # Classe Enemy + Wolf, Skeleton, Bandit
│   ├── boss.py              # CorruptedChampion, DungeonGuardian (2 phases)
│   ├── enemyAI.py           # IA ennemis (Agressive, defensive)
│   ├── skills.py            # Skill ABC + Fireball
│   ├── class_skills.py      # Compétences des 3 classes
│   ├── items.py             # Weapon (dataclass)
│   ├── armors.py            # Armor (dataclass)
│   ├── consumables.py       # Potion, Antidote, Bombe
│   ├── inventory.py         # Inventaire (10 slots, équipement)
│   ├── status_effects.py    # StatusEffect ABC + Poison
│   ├── shield_effect.py     # Bouclier (absorbe les dégâts)
│   ├── stun_effect.py       # Étourdissement (skip le tour)
│   └── player.py            # Classes joueur (non utilisé dans main)
├── exploration/
│   ├── zones.py             # Village, Forêt, Donjon
│   ├── events.py            # Combat, Coffre, Marchand, Dialogue
│   └── quest.py             # Quête principale (3 états)
├── persistence/
│   └── save_manager.py      # Sauvegarde / chargement JSON
├── tests/
│   └── test_aetherfall.py   # 21 tests unitaires
├── savegame_example.json    # Exemple de sauvegarde
└── UML.png                  # Diagramme UML
```

## Design Patterns utilisés

**Observer** – `EventBus` + `ConsoleLogger`. Le moteur de combat publie des événements sans dépendre de `print`. Les loggers s'abonnent et affichent. Découplage logique métier / affichage.

**Factory** – `EnemyFactory`, `WeaponFactory`, `PlayerFactory`. Centralise la création des objets. Ajouter un ennemi ou une arme = ajouter une entrée dans le mapping, c'est tout.

**Command** – Chaque action est un objet : `AttackCommand`, `DefendCommand`, `SkillCommand`, `UseItemCommand`, `EquipWeaponCommand`. Le moteur exécute des commandes sans connaître leur implémentation.

**Strategy** – IA des ennemis (`Agressive`, `defensive`, `BossAI`) et compétences (`Fireball`, `CoupPuissant`, etc.). Comportements interchangeables sans modifier les classes existantes.

## Classes jouables

| Classe | PV | ATK | INT | DEF | AGI | Crit | Compétences |
|---|---|---|---|---|---|---|---|
| Guerrier | 120 | 15 | 4 | 10 | 6 | 10% | Coup puissant, Charge héroïque |
| Mage | 80 | 5 | 18 | 5 | 8 | 5% | Boule de feu, Bouclier arcanique |
| Voleur | 95 | 12 | 6 | 6 | 16 | 25% | Attaque sournoise, Esquive parfaite |

## Bestiaire

| Ennemi | Type | PV | Particularité |
|---|---|---|---|
| Loup sauvage | Standard | 50 | Rapide, attaques multiples |
| Squelette | Standard | 60 | Résistant aux physiques |
| Bandit | Standard | 55 | Critique élevé |
| Champion corrompu | Élite | 120 | Peut empoisonner |
| Gardien du donjon | Boss | 200 | 2 phases (enragé sous 50% PV) |

## Effets de statut

- **Poison** – dégâts fixes chaque tour, durée limitée
- **Bouclier** – absorbe un montant de dégâts avant de disparaître
- **Étourdissement** – la cible saute son prochain tour

Chaque statut gère sa propre logique via polymorphisme (pas de if/else dans le moteur de combat).

## Inventaire

- 10 slots maximum
- 1 arme + 1 armure équipables simultanément
- Consommables : Potion de soin, Antidote, Bombe
- L'équipement applique ses bonus directement aux stats

## Exploration

3 zones avec événements aléatoires ou scriptés :
- **Village** – zone safe, marchand, PNJ de quête
- **Forêt** – combats aléatoires, coffres, clé du donjon
- **Donjon** – 2 salles + boss final (nécessite la clé)

## Quête principale

1. Trouver la Clé du Donjon (explorer la Forêt)
2. Entrer dans le Donjon
3. Vaincre le Gardien du Donjon

## Sauvegarde

Format JSON, structure plate. Sauvegarde les stats du joueur, l'inventaire, la progression de quête et la zone actuelle. Voir `savegame_example.json` pour un exemple.

## Tests

21 tests couvrant : combat, statuts (poison/bouclier/stun), inventaire, quête, sauvegarde/chargement, boss 2 phases, création des classes.

```bash
python -m unittest tests.test_aetherfall -v
```