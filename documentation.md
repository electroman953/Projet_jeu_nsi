# Documentation du projet

## Vue d'ensemble
Ce projet est un jeu d'action top-down realise avec Pyxel. Le coeur du jeu est la classe `App`, qui orchestre l'initialisation, la boucle de jeu (update/draw), le rendu, les collisions, le combat, l'inventaire et la generation des mobs.

## Lancer le jeu
Prerequis : Python 3 et Pyxel installe.

Le point d'entree est [main.py](main.py), qui instancie `App`.

Important : des ressources sont chargees avec des chemins relatifs du type `../Textures/...` depuis [data/app.py](data/app.py) et [data/player.py](data/player.py). Si les assets ne se chargent pas, verifier le working directory (il doit correspondre au dossier data pour que `../Textures` pointe vers les ressources du projet).

## Repartition du code
- [main.py](main.py) : point d'entree. Lance `App`.
- [data/app.py](data/app.py) : boucle de jeu, etats (menu, gameplay, mort), palettes, timers, definitions d'items, spawn, collisions, HUD.
- [data/world.py](data/world.py) : camera, deplacement global, rendu de la carte (tilemap) et pathfinding BFS.
- [data/player.py](data/player.py) : stats du joueur, deplacement, gestion des inputs, attaques, degats, niveau, rendu des sprites.
- [data/mob.py](data/mob.py) : logique des ennemis (IA simple, pathfinding, knockback, collisions, degats et XP).
- [data/items.py](data/items.py) : modeles d'objets et armes (`sword`, `bow`, `staff`), armures et potions.
- [data/inventory.py](data/inventory.py) : UI de l'inventaire, drag-and-drop, equipement, tooltips.
- [data/arrow.py](data/arrow.py) : projectiles a distance.
- [data/coffre.py](data/coffre.py) : coffres et interaction d'ouverture.
- [data/zone.py](data/zone.py) : definition des zones de spawn (nom, monstres, limites).
- [Textures/menu.py](Textures/menu.py) : rendu du menu (pixel art par primitives Pyxel).
- [Textures/res.pyxres](Textures/res.pyxres) : ressources Pyxel (tilemap, images, etc).
- [Textures/Perso/run.png](Textures/Perso/run.png), [Textures/Perso/idle.png](Textures/Perso/idle.png), [Textures/Perso/attack 2 down and left.png](Textures/Perso/attack%202%20down%20and%20left.png), [Textures/Perso/attack 2 right and up.png](Textures/Perso/attack%202%20right%20and%20up.png) : sprites du joueur.
- [conversion 2.0.py](conversion%202.0.py) : outil de conversion d'image vers des appels Pyxel (rect/pset).
- [accueil.py](accueil.py) : ancienne page de menu/test de rendu.
- [test.py](test.py) : script de test ponctuel.
- [zone.py](zone.py) : fichier vide (placeholder).

## Fonctionnement global
### 1) Initialisation
- `App.__init__` appelle `start()`, initialise Pyxel, charge les ressources et demarre la boucle `pyxel.run`.
- `start()` installe les palettes, cree l'inventaire, le joueur, le monde et les zones, et initialise les timers (timestop, cooldowns, i-frames).

### 2) Update (logique)
`App.update()` gere trois etats : menu, jeu, mort.

En jeu :
- Inputs : deplacement, ouverture inventaire, attaques, activation du timestop.
- Cooldowns : decompte des timers pour le tir, le corps-a-corps, l'invincibilite, et le timestop.
- Spawn : `check_mobs()` maintient un nombre de mobs par zone.
- Map : `load_walls()` extrait les tuiles bloquantes depuis la tilemap.
- Deplacement : `World.deplace()` bouge le monde et la camera, sauf en timestop ou c'est `Player.deplace()` qui bouge le joueur a l'ecran.

### 3) Draw (rendu)
`App.draw()` dessine selon l'etat :
- Menu : `Menu.draw_menu()`.
- Mort : ecran de fin.
- Jeu : carte, coffres, joueur, mobs, projectiles, HUD, inventaire et debug hitboxes.

## Systemes de jeu
### Monde et collisions
- La carte est rendue par `World.place_map()` via une tilemap.
- Les obstacles proviennent de la liste `elt_col` dans [data/app.py](data/app.py) et alimentent `App.obstacle`.
- Les collisions sont gerees par le joueur et les mobs avec `collision_rect()`.

### Joueur
- `Player.check_key()` lit les inputs (timestop, inventaire, drag-and-drop).
- `Player.take_damage()` applique les degats et les i-frames.
- Le level-up est gere par `Player.level_up()` avec augmentation de stats.
- Le rendu du sprite depend de l'etat (idle/run/attaque) et de la direction.

### Combat
- Corps-a-corps : `sword.attack()` declenche `App.player_slash()` qui calcule une hitbox devant le joueur.
- Distance : `bow.attack()` cree un `Arrow` via `App.add_player_projectile()`.
- `App.calcul_degats()` calcule les degats et les critiques.
- Les mobs subissent du knockback avec `Mob.appliquer_knockback()`.

### Mobs et IA
- `Mob.move()` suit le joueur si proche, sinon reste passif.
- Le chemin est calcule par BFS (`World.parcours_largeur()`), avec prise en compte des obstacles et d'une marge dynamique pour la hitbox du mob.
- A la mort, un mob donne de l'XP et peut dropper des objets.

### Inventaire et equipement
- `Inventory.afficher()` dessine la grille (4x6) et les slots d'equipement (arme, armure).
- `Inventory.drag_item()` gere le drag-and-drop et les restrictions de type.
- `Item.get_stats()` fournit le texte de stats pour les tooltips.

### Zones et spawn
- Les zones sont definies dans `App.zones` via `Zone` (nom, difficulte, limites, monstres).
- `App.create_mobs()` place un mob aleatoirement dans la zone en evitant les obstacles.

### Timestop
- Active par `SPACE`. Pendant le timestop, les mobs et projectiles sont freezes, la palette change, et le joueur se deplace a l'ecran.
- Un cooldown empile un delai avant la reactivation.

## Controles
- Deplacement : `ZQSD` ou fleches directionnelles.
- Attaque : clic gauche (arme equipee).
- Timestop : `SPACE`.
- Inventaire : `I`.
- Debug hitboxes : `H`.

## Outils et generation d'assets
- [conversion 2.0.py](conversion%202.0.py) convertit une image en code Pyxel (rect/pset). Utile pour generer un rendu comme le menu.
- [Textures/menu.py](Textures/menu.py) contient un menu deja converti.
- [accueil.py](accueil.py) sert de preview/ancienne version pour le menu.
