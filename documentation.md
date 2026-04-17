# Documentation du jeu

## 1. Presentation generale
Jeu d'action top-down realise avec Pyxel. Le joueur explore une carte tilemap, affronte des mobs, recupere des objets, gere un inventaire et peut activer un mode de timestop. La boucle principale passe par trois etats: menu, jeu, mort. La progression se fait via l'XP et les niveaux, avec des armes (corps-a-corps ou distance) et des armures qui modifient les stats.

### Lancement
Prerequis: Python 3 et Pyxel installe. Le point d'entree est [main.py](main.py), qui instancie `App`. Les chargements de ressources dans [data/app.py](data/app.py) et [data/player.py](data/player.py) utilisent des chemins relatifs; si les textures ne se chargent pas, ajuster le dossier de lancement.

### Sauvegarde
- Sauvegarde manuelle via le bouton Save du menu.
- Chargement automatique au demarrage si une sauvegarde existe.
- Exemple de sauvegarde dans [data/savegame.json](data/savegame.json) ; le jeu ecrit dans le dossier de lancement.

### Commandes
- Deplacement: `ZQSD` ou fleches directionnelles.
- Attaque: clic gauche (arme equipee).
- Timestop: `SPACE`.
- Inventaire: `I`.
- Drag-and-drop inventaire: clic gauche.
- Supprimer un item: `DELETE`.
- Debug hitboxes: `H`.
- Retour menu: `M`.

## 2. Architecture du projet

**Racine**
- [main.py](main.py) — point d'entree du jeu, instancie `App`.
- [accueil.py](accueil.py) — prototype de menu, rendu par primitives Pyxel.
- [dead.py](dead.py) — prototype d'ecran de fin, rendu par primitives Pyxel.
- [conversion 2.0.py](conversion%202.0.py) — outil PIL qui convertit une image en appels Pyxel (rect/pset).
- [test.py](test.py) — script de test ponctuel (fonction `faire`).
- [zone.py](zone.py) — fichier vide (placeholder).
- [README.md](README.md) — titre et presentation minimale.
- [documentation.md](documentation.md) — documentation du projet.
- [LICENSE](LICENSE) — licence du projet.

**data**
- [data/app.py](data/app.py) — coeur du jeu: etats, boucle update/draw, timers, listes d'items, spawn, collisions, HUD, sauvegarde/chargement.
- [data/world.py](data/world.py) — camera, deplacement global, rendu de la carte, pathfinding BFS.
- [data/player.py](data/player.py) — stats du joueur, inputs, deplacement, attaques, degats, rendu des sprites.
- [data/mob.py](data/mob.py) — IA ennemie, pathfinding, collisions, degats, knockback, drop d'XP.
- [data/items.py](data/items.py) — definitions des objets et classes `Item`, `Weapon`, `Armor`, `sword`, `bow`, `staff`.
- [data/inventory.py](data/inventory.py) — UI inventaire, drag-and-drop, equipement et tooltips.
- [data/arrow.py](data/arrow.py) — projectiles a distance.
- [data/coffre.py](data/coffre.py) — coffres et interaction d'ouverture.
- [data/zone.py](data/zone.py) — definition des zones de spawn.
- [data/savegame.json](data/savegame.json) — exemple de sauvegarde chargee par le jeu.

**Textures**
- [Textures/res.pyxres](Textures/res.pyxres) — ressources Pyxel (tilemap, images, sprites).
- [Textures/menu.py](Textures/menu.py) — rendu du menu et gestion des clics Start/Save.
- [Textures/conversion.py](Textures/conversion.py) — export de l'image bank 2 vers un PNG d'items.
- [Textures/map_hero_jeu.tmx](Textures/map_hero_jeu.tmx) — source de la carte (Tiled).
- [Textures/Pyxel.gpl](Textures/Pyxel.gpl) — palette Pyxel pour editeur externe.
- [Textures/Perso/idle.png](Textures/Perso/idle.png) — sprite idle du joueur.
- [Textures/Perso/run.png](Textures/Perso/run.png) — sprite de course du joueur.
- [Textures/Perso/attack 2 down and left.png](Textures/Perso/attack%202%20down%20and%20left.png) — sprite d'attaque bas/gauche.
- [Textures/Perso/attack 2 right and up.png](Textures/Perso/attack%202%20right%20and%20up.png) — sprite d'attaque haut/droite.
