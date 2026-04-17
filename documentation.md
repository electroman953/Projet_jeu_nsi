# Documentation du Justin's Journey

## 0. Disclaimers
Dans le code de ce jeu, l'anglais et le français sont constamment utilisés. Cela est simplement notre manière de coder et n'est pas une erreur. Le code est aussi parfois mal organisé pour les créations de variable.

## 1. Présentation générale
Jeu d'action top-down réalisé avec Pyxel. Le joueur, qui s'appelle Justin, explore une carte tilemap, affronte des mobs, récupère des objets, gère un inventaire et peut activer un mode de timestop. La boucle principale passe par trois états : menu, jeu, mort. La progression se fait via l'XP et les niveaux, avec des armes (corps-à-corps ou distance) et des armures qui modifient les stats.

### Lancement
Prérequis : Python 3 et Pyxel 2.9.0 installé. Le point d'entrée est [main.py](main.py), qui instancie `App`. Les chargements de ressources dans [data/app.py](data/app.py) et [data/player.py](data/player.py) utilisent des chemins relatifs ; si les textures ne se chargent pas, ajuster le dossier de lancement.

### Sauvegarde
- Sauvegarde manuelle via le bouton Save du menu, ou automatique toutes les 1500 frames (~25s).
- Chargement automatique au démarrage si une sauvegarde existe.
- Le fichier de sauvegarde est [data/savegame.json](data/savegame.json) ; le jeu écrit dans le dossier de lancement.

### Commandes
- Déplacement : `ZQSD` ou flèches directionnelles.
- Attaque : clic gauche (arme équipée).
- Timestop : `SPACE`.
- Inventaire : `I`.
- Drag-and-drop inventaire : clic gauche.
- Utiliser un item (potion) : `E`.
- Supprimer un item : `DELETE`.
- Debug hitboxes : `H`.
- Retour menu : `M`.

## Fin du jeu
Le jeu prend fin après que le boss final soit vaincu. Celui-ci fait deux fois la taille d'une 'salamandre' et a des statistiques d'attaques largement supérieur.

---

## 2. Architecture du projet

**Racine**
- [main.py](main.py) — point d'entrée du jeu, instancie `App`.
- [accueil.py](accueil.py) — prototype de menu, rendu par primitives Pyxel.
- [dead.py](dead.py) — prototype d'écran de fin, rendu par primitives Pyxel.
- [conversion 2.0.py](conversion%202.0.py) — outil PIL qui convertit une image en appels Pyxel (rect/pset).
- [test.py](test.py) — script de test ponctuel (fonction `faire`).
- [README.md](README.md) — titre et présentation minimale.
- [documentation.md](documentation.md) — documentation du projet.
- [LICENSE](LICENSE) — licence du projet.

**data**
- [data/app.py](data/app.py) — cœur du jeu : états, boucle update/draw, timers, listes d'items, spawn, collisions, HUD, sauvegarde/chargement.
- [data/world.py](data/world.py) — caméra, déplacement global, rendu de la carte, pathfinding BFS.
- [data/player.py](data/player.py) — stats du joueur, inputs, déplacement, attaques, dégâts, rendu des sprites.
- [data/mob.py](data/mob.py) — IA ennemie, pathfinding, collisions, dégâts, knockback, drop d'XP.
- [data/items.py](data/items.py) — définitions des objets et classes `Item`, `Weapon`, `Armor`, `sword`, `bow`.
- [data/inventory.py](data/inventory.py) — UI inventaire, drag-and-drop, équipement et tooltips.
- [data/arrow.py](data/arrow.py) — projectiles à distance.
- [data/coffre.py](data/coffre.py) — coffres et interaction d'ouverture.
- [data/zone.py](data/zone.py) — définition des zones de spawn.
- [data/savegame.json](data/savegame.json) — fichier de sauvegarde écrit et lu par le jeu.

**Textures**
- [Textures/res.pyxres](Textures/res.pyxres) — ressources Pyxel (tilemap, images, sprites).
- [Textures/menu.py](Textures/menu.py) — rendu du menu et gestion des clics Start/Save.
- [Textures/conversion.py](Textures/conversion.py) — export de l'image bank 2 vers un PNG d'items.
- [Textures/map_hero_jeu.tmx](Textures/map_hero_jeu.tmx) — source de la carte (Tiled).
- [Textures/Pyxel.gpl](Textures/Pyxel.gpl) — palette Pyxel pour éditeur externe.
- [Textures/Perso/idle.png](Textures/Perso/idle.png) — sprite idle du joueur.
- [Textures/Perso/run.png](Textures/Perso/run.png) — sprite de course du joueur.
- [Textures/Perso/attack 2 down and left.png](Textures/Perso/attack%202%20down%20and%20left.png) — sprite d'attaque bas/gauche.
- [Textures/Perso/attack 2 right and up.png](Textures/Perso/attack%202%20right%20and%20up.png) — sprite d'attaque haut/droite.

---

## 3. Fonctionnement technique

### Classes et héritage

```
Item
├── Weapon
│   ├── sword
│   └── bow
├── Armor
└── Potion

App
Player
Mob
World
Zone
Coffre
Arrow
Inventory
```

---

### `App` — data/app.py
Classe centrale qui orchestre tout le jeu.

**Attributs principaux**

| Attribut | Type | Rôle |
|---|---|---|
| `width`, `height` | int | Dimensions de la fenêtre en pixels (512x256) |
| `player_x_abs`, `player_y_abs` | float | Position absolue du joueur dans le monde |
| `x_center`, `y_center` | float | Centre de la caméra dans le monde |
| `screen_center_x`, `screen_center_y` | int | Centre fixe de l'écran (256, 128) |
| `timestop` | bool | Vrai si le timestop est actif |
| `TIMESTOP_DURATION` | float | Durée maximale du timestop en secondes |
| `TIMESTOP_COOLDOWN` | float | Temps de recharge du timestop en secondes |
| `i_frames` | float | Compteur d'invincibilité du joueur après un coup |
| `obstacle` | list | Liste de tuples (col, row) des tuiles bloquantes visibles |
| `mobs` | list | Liste des instances `Mob` actives |
| `projectiles` | list | Liste des instances `Arrow` en vol |
| `coffres` | list | Liste des instances `Coffre` du monde |
| `items` | dict | Dictionnaire de tous les items du jeu, indexés par ID entier |
| `elt_col` | list | Coordonnées tilemap des tuiles considérées comme obstacles |
| `potion_active` | list | Effets de potions à durée en cours |
| `palette_normal` / `palette_timestop` / `palette_menu` | list | Palettes de 16 couleurs hex selon l'état du jeu |

**Méthodes**

| Méthode | Rôle |
|---|---|
| `__init__` | Initialise l'état, charge la sauvegarde, lance Pyxel |
| `start` | Réinitialise toutes les variables (appelé aussi à la mort) |
| `update` | Boucle logique principale (60 fps) |
| `draw` | Boucle de rendu principale (60 fps) |
| `create_mobs(monstre, zone)` | Crée un mob à une position libre dans la zone donnée |
| `create_coffres` | Place deux coffres par zone à des positions sans obstacle |
| `check_mobs` | Maintient le quota de mobs vivants par zone |
| `add_player_projectile(type, subtype)` | Crée une flèche dirigée vers la souris |
| `player_slash` | Déclenche l'attaque mêlée et vérifie les collisions |
| `get_melee_hitboxes` | Renvoie les rectangles de collision du joueur et de son slash |
| `calcul_degats(item, arrow)` | Calcule les dégâts finaux avec tirage critique |
| `orient_player_to_mouse` | Oriente le sprite du joueur vers la souris |
| `load_walls` | Reconstruit la liste des obstacles visibles à chaque frame |
| `draw_hud` | Affiche PV, timestop, XP, niveau et position |
| `draw_coffres` | Appelle le draw de chaque coffre |
| `draw_debug_hitboxes` | Affiche les hitboxes en mode debug (touche H) |
| `place_mobs` | Draw + move de tous les mobs |
| `place_projectiles` | Draw + move des projectiles, gestion des collisions |
| `build_item(item_id)` | Instancie un objet Item à partir de son ID |
| `save_game` | Sérialise l'état du jeu en JSON |
| `load_game` | Charge une sauvegarde JSON si elle existe |
| `start_game` | Passe du menu au jeu |

---

### `Player` — data/player.py
Représente le joueur (Justin) avec ses stats, ses inputs et ses animations.

**Attributs principaux**

| Attribut | Type | Rôle |
|---|---|---|
| `speed` | float | Vitesse de déplacement (multiple de sqrt(2) pour le diagonal) |
| `base_damage` | int | Dégâts de base sans arme |
| `health` | int | Points de vie actuels |
| `base_health` | int | Points de vie de base (augmente au level up) |
| `base_defense` | int | Réduction de dégâts de base |
| `base_critical_chance` | float | Probabilité de coup critique de base |
| `base_critical_multiplier` | float | Multiplicateur de dégâts critiques de base |
| `level` | int | Niveau actuel du joueur |
| `experience` | int | XP accumulée |
| `experience_to_next_level` | int | Seuil d'XP pour passer au niveau suivant |
| `en_attaque` | int | Compteur de frames d'animation d'attaque restantes |
| `direction` | str | Direction courante : "up", "down", "left", "right" |
| `run` | bool | Vrai si le joueur se déplace (pour l'animation) |
| `colkey` | int | Couleur de transparence du sprite (change pendant le timestop) |
| `s_dmg` | float | Timer de l'effet visuel de dégâts reçus |

**Méthodes**

| Méthode | Rôle |
|---|---|
| `deplace(app)` | Lit les inputs et déplace le joueur pixel par pixel avec vérification de collision |
| `check_key(app)` | Gère les actions : timestop, inventaire, retour menu |
| `next_dest_is_blocked(app, dx, dy)` | Renvoie True si la prochaine case est un obstacle ou un coffre |
| `next_dest_is_obstacle(app, dx, dy)` | Vérifie la collision avec les tuiles obstacles |
| `next_dest_is_chest(app, dx, dy)` | Vérifie la collision avec un coffre |
| `open_colliding_chest(app, dx, dy)` | Ouvre le coffre touché et ajoute l'item à l'inventaire |
| `take_damage(app, n)` | Inflige des dégâts en tenant compte de la défense et des i-frames |
| `regen(app, n)` | Soigne le joueur sans dépasser le maximum |
| `get_max_health(app)` | Renvoie les PV max (base + bonus armure) |
| `get_current_defense(app)` | Renvoie la défense totale (base + armure) |
| `is_dead` | Renvoie True si les PV sont à 0 |
| `level_up(app)` | Augmente le niveau et les stats si l'XP est suffisante |
| `collision_rect(...)` | Détection de collision entre deux rectangles |
| `draw(app)` | Affiche le bon sprite selon la direction et l'animation |
| `show_dmg(app)` | Affiche l'effet de bords rouges quand le joueur est blessé |

---

### `Mob` — data/mob.py
Représente un ennemi avec son IA de déplacement basée sur le pathfinding BFS.

**Attributs principaux**

| Attribut | Type | Rôle |
|---|---|---|
| `health` | int | Points de vie du mob |
| `damage` | int | Dégâts infligés au contact |
| `type` | str | Type du mob ("chien", "renard", "tortue", "lion", "salamandre") |
| `x`, `y` | int | Position absolue dans le monde |
| `width`, `height` | int | Dimensions de la hitbox |
| `vitesse` | int | Nombre de pixels parcourus par déplacement |
| `chemin` | list | Liste de cases (col, row) calculées par BFS |
| `timer` | int | Compteur de frames pour recalculer le chemin toutes les 30 frames |
| `knockback_vx`, `knockback_vy` | float | Vélocité de knockback en cours d'atténuation |
| `passive` | bool | Vrai si le mob ne détecte pas le joueur |
| `detection_range` | int | Distance en pixels au-delà de laquelle le mob redevient passif |
| `xp_drop_range` | tuple | (min, max) d'XP lâchée à la mort |
| `loot_table` | list | Liste de dicts `{drop_chance, item}` |
| `texture` | tuple | Coordonnées (u, v) du coin haut-gauche du sprite dans la spritesheet |
| `spawn_zone` | str | Nom de la zone d'appartenance pour le système de respawn |

**Méthodes**

| Méthode | Rôle |
|---|---|
| `draw(app)` | Affiche le sprite animé selon la direction, avec cas spécial pour la salamandre |
| `move(app, player_x, player_y)` | Gère knockback, détection, recalcul de chemin et déplacement |
| `prendre_degats(damage)` | Réduit les PV du mob |
| `appliquer_knockback(app, sx, sy, force)` | Calcule et applique une impulsion directionnelle |
| `is_dead(app)` | Si PV = 0, distribue XP + loot et supprime le mob |
| `next_dest_is_player(app, dx, dy)` | Vérifie si le déplacement amènerait en contact avec le joueur |
| `next_dest_is_obstacle(app, dx, dy)` | Vérifie la collision avec les tuiles obstacles |
| `next_dest_is_blocked(app, dx, dy)` | Combine obstacle + coffre |
| `next_dest_is_chest(app, dx, dy)` | Vérifie la collision avec un coffre |
| `collision_rect(x1,y1,w1,h1,x2,y2,w2,h2)` | Détection AABB entre deux rectangles |

---

### `World` — data/world.py
Gère la caméra, le rendu de la tilemap et le pathfinding BFS pour les mobs.

**Attributs principaux**

| Attribut | Type | Rôle |
|---|---|---|
| `width`, `height` | int | Dimensions de l'écran en pixels |
| `tm` | int | Index de la tilemap Pyxel utilisée |
| `word_width`, `word_height` | int | Dimensions du monde en pixels (2048x2048) |

**Méthodes**

| Méthode | Rôle |
|---|---|
| `place_map(x_player, y_player, app)` | Affiche la portion de tilemap visible autour de la caméra |
| `deplace(app, speed)` | Lit les inputs et déplace la caméra avec vérification de collision |
| `recentrer(app, speed)` | Rapproche progressivement la caméra du joueur après un timestop |
| `parcours_largeur(debut, fin, app, mob)` | BFS 8-directions qui renvoie le chemin en cases entre deux points du monde |

**Fonctionnement du BFS** : l'algorithme de parcours en largeur (Breadth-First Search) explore les cases voisines une par une, en partant du mob vers le joueur. Il garantit le chemin le plus court sans passer par les obstacles. Un ensemble d'obstacles "élargi" est calculé selon la taille du mob pour éviter qu'il coince dans les coins. L'exploration est limitée à 40 000 cases pour éviter les ralentissements.

---

### `Arrow` — data/arrow.py
Représente un projectile en vol tiré par le joueur.

**Attributs principaux**

| Attribut | Type | Rôle |
|---|---|---|
| `x`, `y` | float | Position absolue dans le monde |
| `direction` | tuple | Vecteur normalisé (dx, dy) indiquant la trajectoire |
| `speed` | int | Pixels parcourus par frame |
| `damage` | int | Dégâts de base de la flèche |
| `rotation` | float | Angle visuel en radians pour l'affichage |
| `damage_multiplier` | float | Multiplicateur appliqué aux dégâts de base |
| `crit_chance_bonus` | float | Bonus de chance critique apporté par la flèche |
| `crit_multiplier_bonus` | float | Bonus de multiplicateur critique |

**Méthodes**

| Méthode | Rôle |
|---|---|
| `draw(app)` | Affiche le sprite de la flèche à l'écran avec rotation |
| `move` | Déplace la flèche d'un pas selon sa direction et sa vitesse |
| `supprimer(app)` | Supprime la flèche si elle dépasse 512 pixels du centre caméra |
| `bout` | Renvoie les coordonnées de la pointe de la flèche |
| `collision_mob(mob)` | Renvoie True si la pointe touche la hitbox du mob |

---

### `Coffre` — data/coffre.py
Représente un coffre interactif posé dans le monde.

**Attributs principaux**

| Attribut | Type | Rôle |
|---|---|---|
| `id` | int | Identifiant unique pour la sauvegarde |
| `x`, `y` | int | Position absolue du coin haut-gauche |
| `width`, `height` | int | Dimensions (32x32) |
| `tier` | int | Tier de 1 à 4, détermine la qualité du loot |
| `contenu` | int | ID de l'item que le coffre contient |
| `ouvert` | bool | Vrai si le coffre a déjà été ouvert |

**Méthodes**

| Méthode | Rôle |
|---|---|
| `generer_contenu` | Tire aléatoirement un item_id selon le tier au moment de la création |
| `ouvrir` | Marque le coffre comme ouvert et renvoie l'item_id (None si déjà ouvert) |
| `draw(app)` | Affiche le sprite fermé ou ouvert selon l'état |

---

### `Inventory` — data/inventory.py
Gère l'interface et la logique de l'inventaire du joueur.

**Attributs principaux**

| Attribut | Type | Rôle |
|---|---|---|
| `items` | dict | Slots 0-23 + "arme" + "armure", chaque valeur est un Item ou None |
| `on_screen` | bool | Vrai si l'inventaire est ouvert |
| `dragging_item` | Item | Item actuellement glissé à la souris |
| `old_drag_case` | int/str | Slot d'origine de l'item en cours de drag |

**Méthodes**

| Méthode | Rôle |
|---|---|
| `open(app)` | Ouvre/ferme l'inventaire et active/désactive le curseur souris |
| `afficher(app)` | Dessine le panneau inventaire (grille, slots d'équipement, aperçu joueur) |
| `afficher_items` | Affiche les icônes des items dans leurs slots |
| `récuperer_case_souris` | Renvoie le slot sous le curseur ("arme", "armure" ou index entier) |
| `drag_item(app)` | Gère le début et la fin d'un déplacement d'item par clic |
| `show_drag_item` | Affiche l'item glissé sous le curseur |
| `over_item(app)` | Affiche le tooltip d'un item au survol |
| `add_item(item)` | Ajoute un item dans le premier slot libre (1-20) |
| `supprimer_item` | Supprime l'item sous le curseur |
| `use_item(app)` | Utilise une potion (instantanée ou à durée) |

---

### `Item` et sous-classes — data/items.py
Hiérarchie de classes représentant tous les objets du jeu.

**`Item`** — classe de base

| Attribut | Rôle |
|---|---|
| `name` | Nom affiché dans l'UI |
| `description` | Description affichée dans le tooltip |
| `image_x`, `image_y` | Coordonnées du sprite dans la spritesheet items |
| `colkey` | Couleur de transparence pour le rendu |
| `type` | Type de l'item (None, "sword", "bow", "armor", "potion") |
| `liste_attributs` | Dictionnaire des stats (damage, defense, etc.) |

**`Weapon(Item)`** — arme générique. Ajoute `damage`, `crit_chance_bonus`, `crit_multiplier_bonus`, `attack_speed_bonus`. Méthode `attack` vide, surchargée dans les sous-classes.

**`sword(Weapon)`** — épée. `attack` déclenche `player_slash` avec un cooldown.

**`bow(Weapon)`** — arc. `attack` crée un projectile `Arrow` vers la souris.

**`Armor(Item)`** — armure. Ajoute `defense` et `bonus_health`.

**`Potion(Item)`** — consommable. Ajoute `value` (quantité de soin) et `duration` (0 = instantané, >0 = durée en secondes).

La méthode `etat_arme(actif, app)` de `Item` active le curseur souris et déclenche `attack` au clic gauche.

---

### `Zone` — data/zone.py
Structure de données simple décrivant une zone de spawn.

| Attribut | Rôle |
|---|---|
| `name` | Nom de la zone ("Easy", "Medium", "Hard", "Boss") |
| `monstre` | Liste des types de mobs pouvant y spawner |
| `difficulty` | Tier des coffres générés dans cette zone |
| `max_mob` | Nombre maximum de mobs vivants dans la zone |
| `respawn_time` | Délai de respawn en secondes |
| `x`, `y`, `width`, `height` | Rectangle délimitant la zone dans le monde |

---

## 4. Systèmes clés

### Système de coordonnées et caméra
Le monde mesure 2048x2048 pixels. La caméra est définie par `(x_center, y_center)`, le point du monde affiché au centre de l'écran. Pour convertir une position absolue en position écran :
```
screen_x = screen_center_x + (world_x - x_center)
screen_y = screen_center_y + (world_y - y_center)
```
Pendant le timestop, la caméra se fige et c'est le joueur qui se déplace dans l'écran. Quand le timestop se termine, `recentrer` est activé et `world.recentrer` rapproche progressivement la caméra du joueur.

### Système de collision
Les obstacles sont des tuiles de 8x8 pixels. `load_walls` reconstruit la liste `obstacle` chaque frame en scannant les tuiles visibles et en filtrant celles présentes dans `elt_col`. Toutes les détections de collision utilisent la méthode AABB (Axis-Aligned Bounding Box) : `collision_rect(x1, y1, w1, h1, x2, y2, w2, h2)`.

### Pathfinding BFS
Toutes les 30 frames, chaque mob actif recalcule son chemin via `world.parcours_largeur`. Le monde est représenté en grille de cases de 8x8 pixels. Le BFS explore les 8 directions (4 cardinales + 4 diagonales), en bloquant les diagonales si un des deux axes est obstacle. Un ensemble d'obstacles élargi selon la taille du mob évite les situations de coincement dans les angles.

### Système de dégâts et critique
`calcul_degats` additionne les dégâts de base du joueur, les bonus de l'arme équipée et ceux de la flèche (si applicable). Un tirage aléatoire détermine si le coup est critique : si `random(0,100) < crit_chance * 100`, les dégâts sont multipliés par `crit_multiplier`.

### Système de timestop
Quand le joueur active le timestop (espace), `app.timestop` passe à True. La palette graphique bascule vers `palette_timestop` (tons gris). Les mobs et projectiles ne bougent plus. Le joueur se déplace librement dans l'écran figé. La durée est comptée via `timestop_timer` décrémenté toutes les 6 frames. À l'expiration, `recentrer` est activé pour resynchroniser la caméra.

### Système d'inventaire et d'équipement
L'inventaire contient 24 slots génériques (index 0-23) et 2 slots d'équipement ("arme", "armure"). Le drag-and-drop fonctionne en mémorisant l'item et son slot d'origine lors du clic, puis en le déposant sur le slot cible. Un item ne peut être équipé que dans le slot correspondant à son type. Équiper une armure recalcule immédiatement les PV max du joueur.

### Système de sauvegarde
La sauvegarde JSON stocke : position et stats du joueur, contenu de l'inventaire (IDs d'items), état des coffres. Au chargement, `build_item(item_id)` reconstruit chaque objet à partir du dictionnaire `self.items` d'`App`.
