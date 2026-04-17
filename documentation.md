# Documentation du Justin's Journey

## 0. Disclaimers
Dans le code de ce jeu, l'anglais et le français sont constamment utilisés. Cela est simplement notre manière de coder et n'est pas une erreur. Le code est aussi parfois mal organisé pour les créations de variable.
*truc a modifier sur l'ia*

## 1. Presentation generale
Jeu d'action top-down realise avec Pyxel. Le joueur, qui s'appelle justin, explore une carte tilemap, affronte des mobs, recupere des objets, gere un inventaire et peut activer un mode de timestop. La boucle principale passe par trois etats: menu, jeu, mort. La progression se fait via l'XP et les niveaux, avec des armes (corps-a-corps ou distance) et des armures qui modifient les stats.

### Lancement
Prerequis: Python 3 et Pyxel 2.9.0 installe. Le point d'entree est [main.py](main.py), qui instancie `App`. Les chargements de ressources dans [data/app.py](data/app.py) et [data/player.py](data/player.py) utilisent des chemins relatifs; si les textures ne se chargent pas, ajuster le dossier de lancement.

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

## 3. Fonctionnement technique

**Classes**
1. App - classe pour le jeu principal
2. Coffres - classe pour les coffres
3. Player - classe pour le joueur (Justin)
4. Arrow - classe pour les flèches
5. Inventory - classe pour l'inventaire
6. Items - classe pour les items
7. Potions - classe pour les potions héréditaire de items
8. Weapons - classe pour les armes héréditaire de items
9. Armor - classe pour les armures héréditaire de items
10. sword - classe pour les épées héréditaire de weapons
11. bow - classe pour les arcs héréditaire de weapons
12. Mob - classe pour les monstres
13. World - classe pour le monde
14. Zone - classe pour les zones

---

### Méthodes

#### 1. App

1.1 `__init__` — méthode constructeur
1.2 `start` — méthode pour initier les variables du monde
1.3 `create_mobs` — initie les monstres, avec leurs position notamment
1.4 `create_coffres` — fait de même que le 1.3 mais pour les coffres
1.6 `check_mobs` — *à compléter*
1.7 `add_player_projectile` — *à compléter*
1.8 `update` — *à compléter*
1.9 `draw` — *à compléter*
1.10 `place_mobs` — *à compléter*
1.11 `place_projectiles` — *à compléter*
1.12 `orient_player_to_mouse` — *à compléter*
1.13 `get_melee_hitboxes` — *à compléter*
1.14 `player_slash` — *à compléter*
1.15 `draw_debug_hitboxes` — *à compléter*
1.16 `load_walls` — *à compléter*
1.17 `calcul_degats` — *à compléter*
1.18 `draw_hud` — *à compléter*
1.19 `draw_coffres` — *à compléter*
1.20 `start_game` — *à compléter*
1.21 `save_game` — *à compléter*
1.22 `build_item` — *à compléter*
1.23 `load_game` — *à compléter*

#### 2. Coffre

2.1 `__init__` — *à compléter*
2.2 `ouvrir` — *à compléter*
2.3 `generer_contenu` — *à compléter*
2.4 `draw` — *à compléter*

#### 3. Player

3.1 `__init__` — *à compléter*
3.2 `deplace` — *à compléter*
3.3 `check_key` — *à compléter*
3.4 `collision_rect` — *à compléter*
3.5 `take_damage` — *à compléter*
3.6 `regen` — *à compléter*
3.7 `get_max_health` — *à compléter*
3.8 `update_health_to_max` — *à compléter*
3.9 `get_current_defense` — *à compléter*
3.10 `is_dead` — *à compléter*
3.11 `next_dest_is_obstacle` — *à compléter*
3.12 `next_dest_is_blocked` — *à compléter*
3.13 `open_colliding_chest` — *à compléter*
3.14 `next_dest_is_chest` — *à compléter*
3.15 `level_up` — *à compléter*
3.16 `draw` — *à compléter*
3.17 `show_dmg` — *à compléter*

#### 4. Arrow

4.1 `__init__` — *à compléter*
4.2 `draw` — *à compléter*
4.3 `move` — *à compléter*
4.4 `supprimer` — *à compléter*
4.5 `bout` — *à compléter*
4.6 `collision_mob` — *à compléter*

#### 5. Inventory

5.1 `__init__` — *à compléter*
5.2 `open` — *à compléter*
5.3 `afficher` — *à compléter*
5.4 `afficher_items` — *à compléter*
5.5 `récuperer_case_souris` — *à compléter*
5.6 `drag_item` — *à compléter*
5.7 `show_drag_item` — *à compléter*
5.8 `over_item` — *à compléter*
5.9 `add_item` — *à compléter*
5.10 `supprimer_item` — *à compléter*
5.11 `use_item` — *à compléter*

#### 6. Item

6.1 `__init__` — *à compléter*
6.2 `get_stats` — *à compléter*
6.3 `etat_arme` — *à compléter*

#### 7. Potion (hérite de Item)

7.1 `__init__` — *à compléter*

#### 8. Weapon (hérite de Item)

8.1 `__init__` — *à compléter*
8.2 `attack` — *à compléter*

#### 9. Armor (hérite de Item)

9.1 `__init__` — *à compléter*

#### 10. sword (hérite de Weapon)

10.1 `__init__` — *à compléter*
10.2 `attack` — *à compléter*

#### 11. bow (hérite de Weapon)

11.1 `__init__` — *à compléter*
11.2 `attack` — *à compléter*

#### 12. Mob

12.1 `__init__` — *à compléter*
12.2 `draw` — *à compléter*
12.3 `move` — *à compléter*
12.4 `collision_rect` — *à compléter*
12.5 `prendre_degats` — *à compléter*
12.6 `appliquer_knockback` — *à compléter*
12.7 `is_dead` — *à compléter*
12.8 `next_dest_is_player` — *à compléter*
12.9 `next_dest_is_obstacle` — *à compléter*
12.10 `next_dest_is_blocked` — *à compléter*
12.11 `next_dest_is_chest` — *à compléter*

#### 13. World

13.1 `__init__` — *à compléter*
13.2 `place_map` — *à compléter*
13.3 `deplace` — *à compléter*
13.4 `recentrer` — *à compléter*
13.5 `parcours_largeur` — *à compléter*

#### 14. Zone

14.1 `__init__` — *à compléter*

---

### Attributs

#### 1. App

- `on_menu` — *à compléter*
- `palette_menu` — *à compléter*
- `menu` — *à compléter*
- `timestop` — *à compléter*
- `TIMESTOP_DURATION` — *à compléter*
- `TIMESTOP_COOLDOWN` — *à compléter*
- `game_started` — *à compléter*
- `BOW_COOLDOWN` — *à compléter*
- `bow_cooldown` — *à compléter*
- `SWORD_COOLDOWN` — *à compléter*
- `SLASH_RANGE` — *à compléter*
- `MELEE_KNOCKBACK_FORCE` — *à compléter*
- `RANGED_KNOCKBACK_FORCE` — *à compléter*
- `sword_cooldown` — *à compléter*
- `timestop_timer` — *à compléter*
- `timestop_cooldown` — *à compléter*
- `invincible_timer` — *à compléter*
- `i_frames` — *à compléter*
- `width` — *à compléter*
- `height` — *à compléter*
- `potion_active` — *à compléter*
- `elt_col` — *à compléter*
- `screen_center_x` — *à compléter*
- `screen_center_y` — *à compléter*
- `correspondance_nom` — *à compléter*
- `zones` — *à compléter*
- `palette_normal` — *à compléter*
- `palette_timestop` — *à compléter*
- `items` — *à compléter*
- `spawn_x` — *à compléter*
- `spawn_y` — *à compléter*
- `x_center` — *à compléter*
- `y_center` — *à compléter*
- `projectiles` — *à compléter*
- `mobs` — *à compléter*
- `coffres` — *à compléter*
- `inventory` — *à compléter*
- `player` — *à compléter*
- `player_x_abs` — *à compléter*
- `player_y_abs` — *à compléter*
- `world` — *à compléter*
- `recentrer` — *à compléter*
- `obstacle` — *à compléter*
- `debug_hitbox` — *à compléter*

#### 2. Coffre

- `id` — *à compléter*
- `nom` — *à compléter*
- `x` — *à compléter*
- `y` — *à compléter*
- `width` — *à compléter*
- `height` — *à compléter*
- `tier` — *à compléter*
- `contenu` — *à compléter*
- `ouvert` — *à compléter*

#### 3. Player

- `speed` — *à compléter*
- `base_speed` — *à compléter*
- `speed_bonus` — *à compléter*
- `width` — *à compléter*
- `height` — *à compléter*
- `direction` — *à compléter*
- `run` — *à compléter*
- `en_attaque` — *à compléter*
- `next_anim_attaque` — *à compléter*
- `base_damage` — *à compléter*
- `base_health` — *à compléter*
- `health` — *à compléter*
- `base_defense` — *à compléter*
- `base_critical_chance` — *à compléter*
- `base_critical_multiplier` — *à compléter*
- `base_attack_speed` — *à compléter*
- `level` — *à compléter*
- `colkey` — *à compléter*
- `experience` — *à compléter*
- `experience_to_next_level` — *à compléter*
- `s_dmg` — *à compléter*
- `player_screen_x` — *à compléter*
- `player_screen_y` — *à compléter*

#### 4. Arrow

- `x` — *à compléter*
- `y` — *à compléter*
- `damage` — *à compléter*
- `rotation` — *à compléter*
- `direction` — *à compléter*
- `speed` — *à compléter*
- `type` — *à compléter*
- `damage_multiplier` — *à compléter*
- `crit_chance_bonus` — *à compléter*
- `crit_multiplier_bonus` — *à compléter*
- `scale` — *à compléter*

#### 5. Inventory

- `items` — *à compléter*
- `on_screen` — *à compléter*
- `dragging_item` — *à compléter*
- `old_drag_case` — *à compléter*

#### 6. Item

- `name` — *à compléter*
- `description` — *à compléter*
- `image_x` — *à compléter*
- `image_y` — *à compléter*
- `durability` — *à compléter*
- `colkey` — *à compléter*
- `type` — *à compléter*
- `liste_attributs` — *à compléter*

#### 7. Potion (hérite de Item)

- `type` — *à compléter*
- `liste_attributs` — *à compléter*
- `value` — *à compléter*
- `duration` — *à compléter*

#### 8. Weapon (hérite de Item)

- `parent_type` — *à compléter*
- `liste_attributs["damage"]` — *à compléter*
- `liste_attributs["crit_chance_bonus"]` — *à compléter*
- `liste_attributs["crit_multiplier_bonus"]` — *à compléter*
- `liste_attributs["attack_speed_bonus"]` — *à compléter*

#### 9. Armor (hérite de Item)

- `type` — *à compléter*
- `parent_type` — *à compléter*
- `liste_attributs["defense"]` — *à compléter*
- `liste_attributs["bonus_health"]` — *à compléter*

#### 10. sword (hérite de Weapon)

- `type` — *à compléter*

#### 11. bow (hérite de Weapon)

- `type` — *à compléter*
- `colkey` — *à compléter*

#### 12. Mob

- `health` — *à compléter*
- `damage` — *à compléter*
- `type` — *à compléter*
- `x` — *à compléter*
- `y` — *à compléter*
- `width` — *à compléter*
- `height` — *à compléter*
- `color` — *à compléter*
- `vitesse` — *à compléter*
- `chemin` — *à compléter*
- `timer` — *à compléter*
- `knockback_vx` — *à compléter*
- `knockback_vy` — *à compléter*
- `direction` — *à compléter*
- `texture` — *à compléter*
- `passive` — *à compléter*
- `xp_drop_range` — *à compléter*
- `loot_table` — *à compléter*
- `detection_range` — *à compléter*
- `spawn_zone` — *à compléter*
- `screen_x` — *à compléter*
- `screen_y` — *à compléter*

#### 13. World

- `width` — *à compléter*
- `height` — *à compléter*
- `tm` — *à compléter*
- `word_width` — *à compléter*
- `word_height` — *à compléter*

#### 14. Zone

- `name` — *à compléter*
- `monstre` — *à compléter*
- `difficulty` — *à compléter*
- `max_mob` — *à compléter*
- `respawn_time` — *à compléter*
- `timer_respawn` — *à compléter*
- `x` — *à compléter*
- `y` — *à compléter*
- `width` — *à compléter*
- `height` — *à compléter*