Aetherfall – Mini RPG (Design Patterns)
Description

Aetherfall est un mini RPG en console développé en Python dans le cadre du module Design Patterns (Master 2). Le projet met en œuvre plusieurs patterns d’architecture logicielle afin de structurer un moteur de combat tour par tour extensible, maintenable et évolutif. Le joueur peut choisir son nom, sélectionner une arme, décider de son action à chaque tour (attaque ou défense, éventuellement compétence), et combattre des ennemis générés via une factory. Le système inclut également des effets de statut comme le poison.

Architecture du projet

Le projet est organisé en plusieurs modules correspondant aux responsabilités principales :

main.py : point d’entrée et orchestration des tests et du combat interactif

observer/ : gestion des événements et des logs

factory/ : création des ennemis et des armes

commande/ : commandes, moteur de combat, contexte et système de dégâts

strategy/ : ennemis, IA, compétences et effets de statut

Cette séparation permet de respecter le principe de responsabilité unique et de faciliter l’évolution du projet.

Design Patterns utilisés

Observer Pattern
Implémenté via EventBus et ConsoleLogger. Le moteur de combat publie des événements de type "log" sans dépendre directement de print. Les loggers s’abonnent aux événements et affichent les messages. Cela permet un découplage entre la logique métier et l’affichage.

Factory Pattern
EnemyFactory et WeaponFactory centralisent la création des objets (Wolf, Skeleton, Bandit, armes). Cela évite de disperser la logique d’instanciation dans le code et facilite l’ajout de nouveaux types d’ennemis ou d’armes.

Command Pattern
Chaque action est encapsulée dans un objet commande : AttackCommand, DefendCommand, SkillCommand, EquipWeaponCommand. Le moteur de combat exécute des commandes sans connaître leur implémentation interne. Ce pattern permet d’ajouter de nouvelles actions sans modifier la boucle principale.

Strategy Pattern
Utilisé pour l’intelligence artificielle des ennemis (par exemple Agressive) et pour les compétences (comme Fireball). Les comportements sont interchangeables et extensibles sans modifier les classes existantes.

Gestion des états temporaires
Le système de défense et les effets de statut (Poison) reposent sur des états internes modifiés temporairement. Les effets sont appliqués en fin de tour, leur durée est décrémentée, puis ils sont supprimés lorsqu’ils expirent.

Moteur de combat

Le CombatEngine gère la boucle principale du combat. Tant que le joueur et l’ennemi sont vivants, le moteur exécute les étapes suivantes :

Affichage du numéro du tour

Récupération et exécution de la commande du joueur

Vérification de l’état de l’ennemi

Récupération et exécution de la commande de l’ennemi

Application des effets de fin de tour (poison, etc.)

Réinitialisation des états temporaires comme la défense

Incrémentation du compteur de tour

Cette structure sépare clairement la logique de contrôle du combat des actions concrètes effectuées.

Système de dégâts

Le DamageSystem calcule les dégâts en tenant compte :

de l’attaque totale (statistiques de base + bonus d’arme)

de la défense de la cible

du taux de critique

de l’état de défense

des éventuels effets actifs

La formule simplifiée est : dégâts = max(1, attaque_totale - défense). En cas de critique, les dégâts sont doublés. Si la cible est en défense, les dégâts sont réduits.

Fonctionnalités actuelles

Le projet permet actuellement :

le choix du nom du joueur

le choix d’une arme (épée, bâton, dague)

l’application des bonus d’arme dans le calcul des dégâts

le choix de l’action à chaque tour (attaque ou défense)

l’utilisation d’une compétence (Fireball)

la gestion des coups critiques

l’application d’un effet Poison sur plusieurs tours

une intelligence artificielle simple pour les ennemis

un affichage découplé via Observer

Conclusion

Ce projet démontre l’utilisation combinée de plusieurs Design Patterns dans un contexte concret de jeu tour par tour. L’architecture est modulaire, extensible et respecte les principes de séparation des responsabilités. De nouvelles fonctionnalités comme des boss à phases multiples, un inventaire, des objets consommables ou une interface graphique peuvent être ajoutées sans remettre en cause la structure existante.



////////////////////////////////////////////////////////////////
////Pour lancer le projet : ///////////////////////////////////:
//// git clone https://github.com/hadilouakk/Aetherfall_DesignPatterns.git /////////////////////////////////:
////sur le terminal d'un editeur de code "VS-code" par exemple lancer la commande //////////////////////////////:
//// python main.py////////////////////////////////////////////////////////////////////////
/// Choisir un nom /////////////////////////////////////////////////////////////////////////
//// choisir une arme de 1 à 3 //////////////////////////////////////////////////////////////////
/// à chaque tour on choisi si on est en defense ou en attaque  ////////////////////://
//// 1 attaque  2 defense //////////////////////////////////////////////////////////////:
