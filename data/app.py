import pyxel
import random
import json
import os
from data.world import World
from data.player import Player
from data.inventory import Inventory
from data.mob import Mob
from data.items import Item
from data.arrow import Arrow
from data.coffre import Coffre
from data.zone import Zone
from Textures.menu import Menu

class App:
    
    # Point d'entrée du jeu : initialise l'état, charge la sauvegarde, crée la fenêtre Pyxel
    # et lance la boucle principale (update + draw à 60 fps).
    def __init__(self):
        self.start()
        self.load_game()
        pyxel.init(self.width, self.height, title = "Jeu du heros", fps=60)
        pyxel.load('../Textures/res.pyxres')
        print(pyxel.VERSION)
        pyxel.run(self.update, self.draw)

    # Initialise ou réinitialise toutes les variables du jeu (appelé au démarrage et à la mort du joueur).
    # Crée les zones, la palette de couleurs, l'inventaire de départ et les coffres.
    def start(self):
        self.on_menu = True
        self.game_won = False
        self.palette_menu = [
            0x000000, 0xFCDED7, 0xE87C3C, 0xFF9656, 0x49D35C,
            0x29204A, 0x563271, 0xDC576C, 0x417B1C, 0xF3A2AF, 
            0xB8E416, 0xA7D10C, 0xCF1818, 0x9B1919, 0xCFCFCF, 
            0xFFFFFF
        ]
        self.menu = Menu()
        self.timestop = False
        self.TIMESTOP_DURATION = 5
        self.TIMESTOP_COOLDOWN = 10
        self.game_started = True
        self.BOW_COOLDOWN = .9
        self.bow_cooldown = 0
        self.SWORD_COOLDOWN = .5
        self.SLASH_RANGE = 50
        self.MELEE_KNOCKBACK_FORCE = 50
        self.RANGED_KNOCKBACK_FORCE = 4
        self.sword_cooldown = 0
        self.timestop_timer = 0
        self.timestop_cooldown = 0
        self.invincible_timer = .5
        self.i_frames = 0
        self.width = 512
        self.potion_active = []
        self.height = 256
        # Liste des coordonnées de tuiles (col, row) considérées comme obstacles (murs, arbres, eau...).
        self.elt_col = [ (21, 1), (21, 2), (21, 3), (21, 4), (21, 5), (21, 6), (21, 7), (21, 8), (21, 9), (21, 10), (22, 1), (22, 2), (22, 3), (22, 4), (22, 5), (22, 6), (22, 7), (22, 8), (22, 9), (22, 10), (21, 13), (21, 14), (22, 13), (22, 14), (1, 17), (1, 18), (2, 17), (2, 18), (3, 17), (3, 18), (4, 17), (4, 18), (5, 17), (5, 18), (6, 17), (6, 18), (7, 17), (7, 18), (8, 17), (8, 18), (9, 17), (9, 18), (10, 17), (10, 18), (12, 16), (12, 17), (12, 18), (12, 19), (13, 16), (13, 17), (13, 18), (13, 19), (14, 16), (14, 17), (14, 18), (14, 19), (15, 16), (15, 17), (15, 18), (15, 19), (16, 4), (16, 5), (16, 6), (16, 7), (16, 8), (16, 9), (17, 4), (17, 5), (17, 6), (17, 7), (17, 8), (17, 9), (18, 4), (18, 5), (18, 6), (18, 7), (18, 8), (18, 9), (19, 4), (19, 5), (19, 6), (19, 7), (19, 8), (19, 9)]
        self.screen_center_x = self.width // 2
        self.screen_center_y = self.height // 2
        # Correspondance entre les clés internes des attributs et leurs noms affichés dans l'UI.
        self.correspondance_nom = {"damage" : "DMG", "crit_chance_bonus" : "CRIT CHANCE", "crit_multiplier_bonus" : "CRIT MULTIPLIER", "attack_speed_bonus" : "ATK SPEED", "defense" : "DEF", "bonus_health" : "HP"}
        self.zones = [
            Zone("Easy", ["tortue", "renard"], 1, 20, 0, 0, 1024, 1024),
            Zone("Medium", ["renard", "chien"], 2, 30, 1024, 0, 1024, 1024),
            Zone("Hard", [ "chien", "lion"], 3, 0, 40, 1024, 1024, 1024),
            Zone("Boss", ["salamandre"], 4, 40, 1024, 1024,1024, 1024)
        ]
        self.palette_normal = [
            0x0D0D0D, 0x1D2B53, 0x7E2553, 0x1e5925,
            0xAB5236, 0x1E8C0A, 0xC2C3C7, 0xFFF1E8,  
            0xFF004D, 0xFFA300, 0xFFEC27, 0x64b0e6,
            0x4ba344, 0x83769C, 0xFF77A8, 0xFFCCAA   
        ]

        pyxel.colors[:] = self.palette_menu
        # Palette alternative au look désaturé/gris, activée pendant le timestop.
        self.palette_timestop = [
            0x0D0D0D, 0x1D2B53, 0x7E2553, 0x008751,
            0xAB5236, 0x555555, 0xC2C3C7, 0xFFF1E8,  
            0xFF004D, 0xFFA300, 0xFFEC27, 0x00E436,
            0xAAAAAA, 0x83769C, 0xFF77A8, 0xFFCCAA   
        ]
        # Dictionnaire central de tous les items du jeu, indexé par ID entier.
        # Format : (type, nom, description, image_x, image_y, damage/defense, dict_attributs)
        self.items = {
            # === SWORDS ===
            # Tier 1 starter : ~5 coups normal
            2:  ("sword", "Dague azuree",        "Une dague legère à lame bleue, ideale pour des attaques rapides.",      32,  0,  8, {"crit_chance_bonus": 0.0,  "crit_multiplier_bonus": 0.0,  "attack_speed_bonus": 0.3}),
            3:  ("sword", "epee brisee",         "Une epee ancienne dont la lame a ete reforgee à la hate.",               0, 32,  8, {"crit_chance_bonus": 0.0,  "crit_multiplier_bonus": 0.0,  "attack_speed_bonus": 0.0}),
            # Tier 2 early-mid : ~3-4 coups normal
            4:  ("sword", "epee de foudre",      "Une epee courte crepitante d'eclairs bleutes.",                         32, 32, 15, {"crit_chance_bonus": 0.05, "crit_multiplier_bonus": 0.1,  "attack_speed_bonus": 0.1}),
            7:  ("sword", "Poignard de l'ombre", "Un poignard fin et discret, parfait pour frapper dans le dos.",           0, 96, 13, {"crit_chance_bonus": 0.12, "crit_multiplier_bonus": 0.0,  "attack_speed_bonus": 0.3}),
            # Tier 3 mid : two-shot crit (~50 degats), ~3 coups normal
            5:  ("sword", "Lance du chaos",      "Une lance dont la tête diffuse une energie corrompue.",                   0, 64, 23, {"crit_chance_bonus": 0.0,  "crit_multiplier_bonus": 0.2,  "attack_speed_bonus": 0.0}),
            6:  ("sword", "epee de sang",        "Une lame ecarlate gorgee de la force de ses victimes.",                  32, 64, 22, {"crit_chance_bonus": 0.1,  "crit_multiplier_bonus": 0.15, "attack_speed_bonus": 0.0}),
            9:  ("sword", "Bident maudit",       "Un double pic maudit dont les deux pointes empoisonnent les plaies.",     0,128, 21, {"crit_chance_bonus": 0.06, "crit_multiplier_bonus": 0.2,  "attack_speed_bonus": 0.0}),
            # Tier 4 endgame : one/two-shot fiable
            8:  ("sword", "epee runique",        "Une grande lame gravee de runes conferant une puissance surnaturelle.",  32, 96, 35, {"crit_chance_bonus": 0.12, "crit_multiplier_bonus": 0.5,  "attack_speed_bonus": 0.0}),

            # === BOWS ===
            # Tier 1 starter
            17: ("bow",   "Arc simple",          "L'arc de tout aventurier qui debute sa quête.",                          64,   0,  6, {"crit_chance_bonus": 0.0,  "crit_multiplier_bonus": 0.0,  "attack_speed_bonus": 0.0}),
            16: ("bow",   "Arc de debutant",     "Un arc rudimentaire en bois brut, fiable mais sans eclat.",              32, 224,  9, {"crit_chance_bonus": 0.0,  "crit_multiplier_bonus": 0.0,  "attack_speed_bonus": 0.1}),
            15: ("bow",   "Arc court",           "Un arc leger et maniable, facile à utiliser en combat rapproche.",        0, 224,  9, {"crit_chance_bonus": 0.0,  "crit_multiplier_bonus": 0.0,  "attack_speed_bonus": 0.3}),
            # Tier 2 early-mid
            12: ("bow",   "Arc de racines",      "Un arc noueux façonne dans des racines entrelacees.",                    32, 160, 14, {"crit_chance_bonus": 0.05, "crit_multiplier_bonus": 0.0,  "attack_speed_bonus": 0.1}),
            11: ("bow",   "Arc long elfique",    "Un arc fin taille dans un bois enchante, precis sur longue portee.",     0, 160, 16, {"crit_chance_bonus": 0.08, "crit_multiplier_bonus": 0.1,  "attack_speed_bonus": 0.0}),
            # Tier 3 mid : two-shot crit
            14: ("bow",   "Arc de sang",         "Teint de sang seche, cet arc decuple la rage du tireur.",                32, 192, 22, {"crit_chance_bonus": 0.07, "crit_multiplier_bonus": 0.2,  "attack_speed_bonus": 0.0}),
            13: ("bow",   "Arc corrompu",        "Un arc tordu par la magie noire, dont les flèches percent les armures.", 0, 192, 24, {"crit_chance_bonus": 0.06, "crit_multiplier_bonus": 0.15, "attack_speed_bonus": 0.0}),
            # Tier 4 endgame
            19: ("bow",   "Arc de tempête",      "Cet arc massif dechaîne des flèches comme des eclairs.",                 64,  32, 28, {"crit_chance_bonus": 0.1,  "crit_multiplier_bonus": 0.3,  "attack_speed_bonus": 0.25}),
            23: ("bow",   "Arc draconique",      "Taille dans l'os d'un dragon, il vibre d'une puissance colossale.",      64,  96, 32, {"crit_chance_bonus": 0.12, "crit_multiplier_bonus": 0.4,  "attack_speed_bonus": 0.0}),
            21: ("bow",   "Arc abyssal",         "Un arc forge dans les profondeurs, ses flèches dechirent l'air.",        64,  64, 35, {"crit_chance_bonus": 0.12, "crit_multiplier_bonus": 0.5,  "attack_speed_bonus": 0.1}),

            # === ARMORS ===
            # Tier 1 starter
            18: ("armor", "Tunique de cuir",     "Une protection legère en cuir tanne.",                                   96,   0,  3, {"bonus_health": 10}),
            20: ("armor", "Cotte de mailles",    "Une armure en mailles d'acier, bon equilibre protection/poids.",         96,  32,  6, {"bonus_health": 15}),
            # Tier 2 early-mid
            22: ("armor", "Plastron solide",     "Un plastron en acier renforce grave aux armes d'une vieille guilde.",    96,  64,  9, {"bonus_health": 20}),
            24: ("armor", "Armure de plaques",   "Une lourde armure de plaques qui repousse les coups les plus violents.", 96,  96, 12, {"bonus_health": 25}),
            25: ("armor", "Armure d'os",         "Façonnee d'os monstrueux, elle degage une aura intimidante.",            64, 128, 10, {"bonus_health": 20}),
            # Tier 3 mid
            26: ("armor", "Armure demoniaque",   "Forgee aux enfers, elle brûle les attaquants qui la frôlent.",           96, 128, 14, {"bonus_health": 30}),
            27: ("armor", "Armure chitineuse",   "Taillee dans la carapace d'un colosse insectoïde.",                      64, 160, 12, {"bonus_health": 25}),
            28: ("armor", "Armure du seigneur",  "L'armure d'un seigneur de guerre, symbole de puissance absolue.",        96, 160, 16, {"bonus_health": 35}),
            # Tier 4 endgame
            29: ("armor", "Armure abyssale",     "Une armure noire profonde qui absorbe la lumière et les coups.",         64, 192, 18, {"bonus_health": 30}),
            30: ("armor", "Armure legendaire",   "Le summum de l'artisanat, portee par les heros des ages anciens.",       64, 224, 22, {"bonus_health": 40}),

            # === POTIONS DE SOIN (4 tiers) ===
            # Format: ("potion", name, description, image_x, image_y, attributs, value, duration)
            # Tier 1 : petite potion, +20 PV instantané
            31: ("potion", "Petite potion de soin",   "Restaure 20 PV instantanement.", 224,  224, {"heal": True}, 20,  0),
            # Tier 2 : potion normale, +50 PV instantané
            32: ("potion", "Potion de soin",          "Restaure 50 PV instantanement.", 224, 174, {"heal": True}, 50,  0),
            # Tier 3 : grande potion, +100 PV instantané
            33: ("potion", "Grande potion de soin",   "Restaure 100 PV instantanement.", 224, 114, {"heal": True}, 100, 0),
            # Tier 4 : potion supreme, soin progressif 20 PV/s pendant 10s (200 PV total)
            34: ("potion", "Potion de soin supreme",  "Regenere 20 PV par seconde pendant 10 secondes.", 224, 51, {"heal": True}, 20, 10),        
    }

        
        # Coordonnees de spawn modifiables
        self.spawn_x = 8 * 38
        self.spawn_y = 9 * 41

        self.x_center, self.y_center = self.spawn_x, self.spawn_y

        self.projectiles = []
        self.mobs = []
        self.coffres = []
        self.inventory = Inventory(self)
        # Items de départ
        self.inventory.add_item(self.build_item(2))   # Dague azurée (sword tier 1)
        self.inventory.add_item(self.build_item(31))  # Petite potion de soin
        self.player = Player()
        self.player_x_abs, self.player_y_abs = self.spawn_x, self.spawn_y
        self.world = World(self.width, self.height,0)
        self.recentrer = False
        self.obstacle = []
        self.debug_hitbox = False
        self.boss_spawned = False
        self.create_coffres()

    # Crée un mob du type demandé dans la zone donnée, à une position aléatoire sans obstacle.
    # La double boucle de vérification teste plusieurs points autour du centre pour éviter
    # de spawner un mob à cheval sur un mur.
    def create_mobs(self, monstre, zone=None):
        temp = []
        loot_tables = {
            "tortue": [
                {"drop_chance": 0.08, "item": self.build_item(31)},
                {"drop_chance": 0.03, "item": self.build_item(18)},
                {"drop_chance": 0.02, "item": self.build_item(17)},
            ],
            "renard": [
                {"drop_chance": 0.07, "item": self.build_item(31)},
                {"drop_chance": 0.04, "item": self.build_item(32)},
                {"drop_chance": 0.03, "item": self.build_item(2)},
                {"drop_chance": 0.02, "item": self.build_item(15)},
                {"drop_chance": 0.01, "item": self.build_item(20)},
            ],
            "chien": [
                {"drop_chance": 0.06, "item": self.build_item(32)},
                {"drop_chance": 0.04, "item": self.build_item(4)},
                {"drop_chance": 0.04, "item": self.build_item(12)},
                {"drop_chance": 0.02, "item": self.build_item(22)},
                {"drop_chance": 0.01, "item": self.build_item(5)},
            ],
            "lion": [
                {"drop_chance": 0.08, "item": self.build_item(33)},
                {"drop_chance": 0.04, "item": self.build_item(6)},
                {"drop_chance": 0.04, "item": self.build_item(14)},
                {"drop_chance": 0.03, "item": self.build_item(26)},
                {"drop_chance": 0.02, "item": self.build_item(8)},
                {"drop_chance": 0.01, "item": self.build_item(19)},
            ],
            "salamandre": [
                {"drop_chance": 0.10, "item": self.build_item(34)},
                {"drop_chance": 0.05, "item": self.build_item(8)},
                {"drop_chance": 0.05, "item": self.build_item(21)},
                {"drop_chance": 0.03, "item": self.build_item(30)},
                {"drop_chance": 0.03, "item": self.build_item(29)},
                {"drop_chance": 0.02, "item": self.build_item(23)},
            ],
        }

        type={
            "chien": {"health": 50, "damage": 20, "height": 32, "width": 32, "color": 8, "xp_drop_range": (5, 15), "loot_table":loot_tables["chien"], 'texture':(0,0)},
            "lion":{"health": 200, "damage": 100, "height": 32, "width": 32, "color": 7, "xp_drop_range": (50,60), "loot_table": loot_tables["lion"],'texture':(0,125)},
            "renard":{"health": 100, "damage": 50, "height": 32, "width": 32, "color": 9, "xp_drop_range": (10, 20), "loot_table": loot_tables["renard"],'texture':(96,0)},
            "salamandre":{"health": 550, "damage": 150, "height": 32, "width": 32, "color": 10, "xp_drop_range": (100,150), "loot_table": loot_tables["salamandre"],'texture':(192,0)},
            "tortue":{"health": 80, "damage": 40, "height": 32, "width": 32, "color": 11, "xp_drop_range": (25,35), "loot_table": loot_tables["tortue"],'texture':(96,128)},
            "boss":{"health": 1500, "damage": 250, "height": 32, "width": 32, "color": 10, "xp_drop_range": (100,150), "loot_table": loot_tables["salamandre"],'texture':(192,0)}
            }
        if zone is not None:
            # Cherche en boucle une position libre dans la zone : on tire des coordonnées aléatoires,
            # puis on vérifie un échantillon de points autour du centre du mob (pas de 4 pixels)
            # pour s'assurer qu'aucun ne tombe sur une tuile obstacle.
            while True:
                x = random.randint(zone.x, zone.x + zone.width)
                y = random.randint(zone.y, zone.y + zone.height)
                collision = False
                for i in range(-type[monstre]["width"]//2, type[monstre]["width"]//2 + 1, 4):
                    for j in range(-type[monstre]["height"]//2, type[monstre]["height"]//2 + 1, 4):
                        # On lit directement la carte complète en divisant par 8 pour avoir la tuile
                        if pyxel.tilemaps[self.world.tm].pget((x + i) // 8, (y + j) // 8) in self.elt_col:
                            collision = True
                            break
                    if collision:
                        break
                if not collision:
                    break
        else:
            x, y = pyxel.rndi(0, self.width), pyxel.rndi(0, self.height)
        self.mobs.append(Mob(type[monstre]["health"], type[monstre]["damage"], monstre, x, y, type[monstre]["width"], type[monstre]["height"], type[monstre]["color"], type[monstre]["xp_drop_range"], type[monstre]["loot_table"], type[monstre]["texture"], None if zone is None else zone.name))

    # Place un coffre à une position aléatoire valide dans chaque zone, en vérifiant
    # qu'aucun point de sa hitbox ne tombe sur un obstacle. Même logique que create_mobs.
    def create_coffres(self):
        for zone in self.zones:
            for c in range(2):
                while True:
                    x = random.randint(zone.x, zone.x + zone.width)
                    y = random.randint(zone.y, zone.y + zone.height)
                    collision = False
                    for i in range(-16, 17, 4):
                        for j in range(-16, 17, 4):
                            if pyxel.tilemaps[self.world.tm].pget((x + i) // 8, (y + j) // 8) in self.elt_col:
                                collision = True
                                break
                        if collision:
                            break
                    if not collision:
                        break
                self.coffres.append(Coffre(len(self.coffres)+1, f"Coffre {len(self.coffres)+1}", x, y, 32, 32, zone.difficulty))

    # Vérifie que chaque zone a bien son quota de mobs vivants. Si ce n'est pas le cas,
    # en crée de nouveaux jusqu'à atteindre max_mob.
    def check_mobs(self):
        for zone in self.zones:
            while len([mob for mob in self.mobs if mob.spawn_zone == zone.name]) < zone.max_mob:
                monstre = random.choice(zone.monstre)
                self.create_mobs(monstre, zone)
                zone.timer_respawn = zone.respawn_time

    # Crée un projectile tiré par le joueur en direction de la souris.
    # Calcule la direction normalisée (vecteur de longueur 1) et la rotation visuelle de la flèche.
    def add_player_projectile(self, type, subtype):
        a={"arrow":{"basic":(8,5)}}
        self.orient_player_to_mouse()
        xr = pyxel.mouse_x - (self.player.player_screen_x + self.player.width // 2)
        yr = pyxel.mouse_y - (self.player.player_screen_y + self.player.width // 2)
        hr = pyxel.sqrt(xr**2 + yr**2)
        if hr == 0:
            hr=1
        rotation = pyxel.atan2(yr, xr) - pyxel.atan2(-1, 1)
        self.projectiles.append(Arrow(self.player_x_abs, self.player_y_abs - self.player.height//4, a[type][subtype][1], rotation, (xr/hr, yr/hr), a[type][subtype][0], subtype))

    # Boucle de logique principale appelée à chaque frame par Pyxel.
    # Gère les trois états du jeu (menu, mort, jeu), les timers, les cooldowns
    # et les appels aux systèmes de déplacement et d'armes.
    def update(self):
        self.player.level_up(self)
        if self.player.level >= 20 and not self.boss_spawned:
            self.create_mobs("boss", None)
            self.mobs[-1].x = self.player_x_abs + 100
            self.mobs[-1].y = self.player_y_abs + 100
            self.boss_spawned = True
            
        if self.timestop:
            self.player.colkey = 3
        else:
            self.player.colkey = 5
        if self.on_menu:
            self.menu.check_menu_click(self)
        elif self.player.is_dead():
            pyxel.colors[:] = self.palette_menu
            if (224<pyxel.mouse_x<288 and 116<pyxel.mouse_y<148 and pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT)) or pyxel.btnr(pyxel.KEY_SPACE):
                self.start()
        else:
            if pyxel.frame_count % 1500 == 0:
                print("Autosaving game...")
                self.save_game()
                
            if pyxel.btnp(pyxel.KEY_H):
                self.debug_hitbox = not self.debug_hitbox
            self.player.check_key(self)

            # Bloc exécuté toutes les 6 frames : vérification des mobs, timers flottants
            # (timestop, cooldowns, i_frames) décrémentés par pas de 0.1s.
            if pyxel.frame_count % 6 == 0:
                self.check_mobs()
                for zone in self.zones:
                    if zone.timer_respawn > 0:
                        zone.timer_respawn = max(0, round(zone.timer_respawn - 0.1, 1))
                for i in self.mobs[:]:
                    i.is_dead(self)
                if self.timestop_timer > 0:
                    self.timestop_timer = max(0, round(self.timestop_timer - 0.1, 1))
                if self.timestop_cooldown > 0:
                    self.timestop_cooldown = max(0, round(self.timestop_cooldown - 0.1, 1))
                if self.bow_cooldown > 0:
                    self.bow_cooldown = max(0, round(self.bow_cooldown - 0.1, 1))
                if self.sword_cooldown > 0:
                    self.sword_cooldown = max(0, round(self.sword_cooldown - 0.1, 1))
                if self.i_frames > 0:
                    self.i_frames = max(0, round(self.i_frames - 0.1, 1))

            if pyxel.frame_count % 30 == 0:
                for i in self.projectiles:
                    i.supprimer(self)
            if self.timestop and self.timestop_timer == 0:
                self.timestop = False
                self.recentrer = True
                self.timestop_cooldown = self.TIMESTOP_COOLDOWN
            self.world.recentrer(self, 10)
            
            if self.recentrer:
                return
            if self.on_menu:
                return
            if self.inventory.on_screen:
                return
            self.load_walls()
            if self.inventory.items["arme"]:
                self.inventory.items["arme"].etat_arme(True, self)
            
            # En timestop, le joueur se déplace librement sur l'écran figé.
            # Hors timestop, c'est la caméra (world.deplace) qui suit le joueur normalement.
            if self.timestop == False:
                self.world.deplace(self, self.player.speed)
            else:
                self.player.deplace(self)
                # Limite la position du joueur à l'intérieur de l'écran visible pendant le timestop.
                hw = self.player.width // 2
                hh = self.player.height // 2
                self.player_x_abs = max(self.x_center - self.width//2 + hw, min(self.player_x_abs, self.x_center + self.width//2 - hw))
                self.player_y_abs = max(self.y_center - self.height//2 + hh, min(self.player_y_abs, self.y_center + self.height//2 - hh))
                if self.timestop_timer == 0:
                    self.timestop = False
                    self.recentrer = True

        if getattr(self, "game_won", False):
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.game_won = False
            return
            
    # Boucle de rendu appelée à chaque frame. Gère les trois états visuels :
    # menu d'accueil, écran de mort, et jeu en cours (carte, entités, HUD, inventaire).
    def draw(self):
        if self.on_menu:
            pyxel.cls(0)
            pyxel.mouse(True)
            self.menu.draw_menu_accueil()
        elif self.player.is_dead():
            pyxel.cls(0)
            pyxel.mouse(True)
            self.menu.draw_menu_dead()
        elif getattr(self, "game_won", False):
            pyxel.cls(0)
            pyxel.text(self.width // 2 - 40, self.height // 2 - 10, "BRAVO VOUS AVEZ GAGNE !", 7)
            pyxel.text(self.width // 2 - 50, self.height // 2 + 10, "Appuyez sur ESPACE pour continuer", 7)
        else:
            pyxel.cls(0)

            if self.on_menu:
                return
            
            self.world.place_map(self.x_center, self.y_center, self)
            self.draw_coffres()
            self.player.draw(self)
            self.place_mobs()
            self.place_projectiles()
            self.draw_hud()
            self.player.show_dmg(self)
            # On change la palette après le dessin du joueur pour que l'effet timestop
            # s'applique à partir de la prochaine frame sans décalage visuel.
            if self.timestop:
                pyxel.colors[:] = self.palette_timestop
            else:
                pyxel.colors[:] = self.palette_normal    
            if self.inventory.on_screen:
                pyxel.images[0].load(0, 0, '../Textures/items.png')
                self.inventory.afficher(self)
                self.inventory.over_item(self)
            if self.debug_hitbox:
                self.draw_debug_hitboxes()

    # Dessine et déplace tous les mobs de la liste à chaque frame.
    def place_mobs(self):
        for i in self.mobs:
            i.draw(self)
            i.move(self, self.player_x_abs, self.player_y_abs)
    
    # Dessine et déplace tous les projectiles. Vérifie également la collision avec chaque mob :
    # si touché, applique dégâts + knockback et supprime le projectile.
    def place_projectiles(self):
        for i in self.projectiles:
            i.draw(self)
            if not self.timestop and not self.inventory.on_screen:
                i.move()
            for j in self.mobs:
                if i.collision_mob(j):
                    damage = self.calcul_degats(self.inventory.items["arme"], i)
                    j.prendre_degats(damage)
                    j.appliquer_knockback(self, i.x, i.y, force=self.RANGED_KNOCKBACK_FORCE)
                    j.is_dead(self)
                    if i in self.projectiles:
                        self.projectiles.remove(i)
                    break

    # Oriente le sprite du joueur vers la souris selon l'axe dominant (horizontal ou vertical).
    def orient_player_to_mouse(self):
        player_center_x = self.screen_center_x + (self.player_x_abs - self.x_center)
        player_center_y = self.screen_center_y + (self.player_y_abs - self.y_center)
        dx = pyxel.mouse_x - player_center_x
        dy = pyxel.mouse_y - player_center_y
        if abs(dx) >= abs(dy):
            self.player.direction = "right" if dx >= 0 else "left"
        else:
            self.player.direction = "down" if dy >= 0 else "up"

    # Calcule et renvoie les deux rectangles de collision de l'attaque mêlée :
    # la hitbox du joueur lui-même, et la zone de slash projetée devant lui selon sa direction.
    def get_melee_hitboxes(self):
        slash_range = self.SLASH_RANGE//1.5
        player_box = (
            self.player_x_abs - (self.player.width // 2),
            self.player_y_abs - (self.player.height // 2),
            self.player.width,
            self.player.height,
        )
        # Même rectangle carré pour toutes directions, centré devant le joueur
        if self.player.direction == 'up':
            slash_box = (player_box[0] + (player_box[2] - slash_range) // 2, player_box[1] - slash_range, slash_range, slash_range)
        elif self.player.direction == 'down':
            slash_box = (player_box[0] + (player_box[2] - slash_range) // 2, player_box[1] + player_box[3], slash_range, slash_range)
        elif self.player.direction == 'left':
            slash_box = (player_box[0] - slash_range, player_box[1] + (player_box[3] - slash_range) // 2, slash_range, slash_range)
        else:  # right
            slash_box = (player_box[0] + player_box[2], player_box[1] + (player_box[3] - slash_range) // 2, slash_range, slash_range)
        return player_box, slash_box

    # Déclenche l'attaque mêlée : vérifie pour chaque mob s'il est touché par la zone de slash
    # ou par contact direct avec le joueur, puis applique dégâts et knockback.
    def player_slash(self):
        player_box, slash_box = self.get_melee_hitboxes()
        for j in self.mobs:
            mob_box = (j.x - j.width // 2, j.y - j.height // 2, j.width, j.height)
            hit_by_slash = j.collision_rect(
                slash_box[0], slash_box[1], slash_box[2], slash_box[3],
                mob_box[0], mob_box[1], mob_box[2], mob_box[3]
            )
            hit_by_contact = j.collision_rect(
                player_box[0], player_box[1], player_box[2], player_box[3],
                mob_box[0], mob_box[1], mob_box[2], mob_box[3]
            )
            if hit_by_slash or hit_by_contact:
                damage = self.calcul_degats(self.inventory.items["arme"])
                j.prendre_degats(damage)
                j.appliquer_knockback(self, self.player_x_abs, self.player_y_abs, force=self.MELEE_KNOCKBACK_FORCE)
                j.is_dead(self) 

    # Affiche les hitboxes de debug en mode H : contours rouges pour les mobs,
    # vert pour le joueur, jaune pour la zone de slash.
    def draw_debug_hitboxes(self):
        for mob in self.mobs:
            mx = int(self.screen_center_x + (mob.x - self.x_center) - mob.width // 2)
            my = int(self.screen_center_y + (mob.y - self.y_center) - mob.height // 2)
            pyxel.rectb(mx, my, mob.width, mob.height, 8)

        player_box, slash_box = self.get_melee_hitboxes()
        px = int(self.screen_center_x + (player_box[0] - self.x_center))
        py = int(self.screen_center_y + (player_box[1] - self.y_center))
        pyxel.rectb(px, py, int(player_box[2]), int(player_box[3]), 11)

        sx = int(self.screen_center_x + (slash_box[0] - self.x_center))
        sy = int(self.screen_center_y + (slash_box[1] - self.y_center))
        pyxel.rectb(sx, sy, int(slash_box[2]), int(slash_box[3]), 10)

    # Parcourt les tuiles visibles à l'écran et reconstruit la liste des obstacles
    # (tuiles collisionnables) à chaque frame. Indispensable car la caméra se déplace.
    def load_walls(self):
        self.obstacle = []
        
        for x in range(int(self.x_center) - self.width//2, int(self.x_center) + self.width//2, 8):
            for y in range(int(self.y_center) - self.height//2, int(self.y_center) + self.height//2, 8):                
                
                if pyxel.tilemaps[self.world.tm].pget(x // 8, y // 8) in self.elt_col:
                    self.obstacle.append((x//8, y//8))

    # Calcule les dégâts d'une attaque en tenant compte de l'arme équipée et,
    # optionnellement, des bonus de la flèche. Tire aléatoirement un coup critique.
    # Renvoie les dégâts finaux (float).
    def calcul_degats(self, item, arrow = None):
        base_damage = self.player.base_damage + item.liste_attributs.get("damage", 0)
        crit_chance_bonus = item.liste_attributs.get("crit_chance_bonus", 0)
        crit_multiplier_bonus = item.liste_attributs.get("crit_multiplier_bonus", 0)
        if arrow:
            base_damage += arrow.damage * arrow.damage_multiplier
            crit_chance_bonus += arrow.crit_chance_bonus
            crit_multiplier_bonus += arrow.crit_multiplier_bonus
        crit_chance = self.player.base_critical_chance + crit_chance_bonus
        crit_multiplier = self.player.base_critical_multiplier + crit_multiplier_bonus
        if pyxel.rndi(0, 100) < crit_chance * 100:
            return base_damage * crit_multiplier
        else:
            return base_damage
    
    # Affiche le HUD en haut à gauche : PV, état du timestop, XP, niveau et position absolue.
    def draw_hud(self):
        pyxel.text(10,10,f"Health :{self.player.health}", 7)
        if self.timestop_cooldown>0:
            pyxel.text(10,20,f"Timestop ready in: {self.timestop_cooldown}s", 7)
        elif self.timestop:
            pyxel.text(10,20,f"Timestop left: {self.timestop_timer}s", 7)
        else:
            pyxel.text(10,20,f"Timestop is ready", 7)
        pyxel.text(10,30,f"XP: {self.player.experience}", 7)
        pyxel.text(10,40,f"Level: {self.player.level}", 7)
        pyxel.text(10, 50, f"x : {self.player_x_abs} y: {self.player_y_abs}", 7)
    
    # Appelle la méthode draw de chaque coffre présent dans le monde.
    def draw_coffres(self):
        for i in self.coffres:
            i.draw(self)

    # Passe l'état du jeu de "menu" à "en jeu" et applique la palette normale.
    def start_game(self):
        self.on_menu = False
        if not self.game_started:
            self.game_started = False
        pyxel.colors[:] = self.palette_normal

    # Sérialise l'état du jeu (joueur, inventaire, mobs, coffres) dans un fichier JSON.
    # La correspondance item -> ID se fait en cherchant le nom dans self.items.
    def save_game(self):
        print("Saving game...")
        data = {
            "player": {
                "x": self.player_x_abs,
                "y": self.player_y_abs,
                "health": self.player.health,
                "experience": self.player.experience,
                "level": self.player.level,
                "base_damage": self.player.base_damage,
                "base_critical_chance": self.player.base_critical_chance,
                "base_critical_multiplier": self.player.base_critical_multiplier
            },
            "inventory": {
                "items": {
                    slot: next((k for k, v in self.items.items() if item and v[1] == item.name), None)
                    for slot, item in self.inventory.items.items()
                }
            },
            "mobs": [
                {"x": mob.x, "y": mob.y, "health": mob.health}
                for mob in self.mobs if mob.health > 0
            ],
            "boss_spawned": self.boss_spawned
        }
        save_path = os.path.join(os.path.dirname(__file__), 'savegame.json')
        with open(save_path, 'w') as f:
            json.dump(data, f)

    # Construit et renvoie un objet Item à partir de son ID dans self.items.
    # Instancie la bonne sous-classe (sword, bow, Armor, Potion) selon le type stocké.
    def build_item(self, item_id):
        if item_id not in self.items:
            return None
        from data.items import sword, bow, Armor, Potion
        item_data = self.items[item_id]
        item_type_str = item_data[0]
        if item_type_str == "sword":
            return sword(*item_data[1:5], item_data[5], **item_data[6])
        elif item_type_str == "bow":
            return bow(*item_data[1:5], item_data[5], **item_data[6])
        elif item_type_str == "armor":
            return Armor(*item_data[1:5], item_data[5], **item_data[6])
        elif item_type_str == "potion":
            # Format: ("potion", name, description, image_x, image_y, attributs, value, duration)
            return Potion(item_data[1], item_data[2], item_data[3], item_data[4], item_data[5], item_data[6], item_data[7])
        return None

    # Charge une sauvegarde JSON si elle existe. Restaure la position, les stats du joueur,
    # l'inventaire (par ID d'item) et l'état des coffres. En cas d'erreur, démarre normalement.
    def load_game(self):
        try:
            save_path = os.path.join(os.path.dirname(__file__), 'savegame.json')
            with open(save_path, 'r') as f:
                data = json.load(f)
            
            self.player_x_abs = data["player"]["x"]
            self.player_y_abs = data["player"]["y"]
            self.x_center = self.player_x_abs
            self.y_center = self.player_y_abs
            self.player.health = data["player"]["health"]
            self.player.experience = data["player"]["experience"]
            self.player.level = data["player"]["level"]
            self.player.base_damage = data["player"]["base_damage"]
            self.player.base_critical_chance = data["player"]["base_critical_chance"]
            self.player.base_critical_multiplier = data["player"]["base_critical_multiplier"]
            self.boss_spawned = data.get("boss_spawned", False)
            
            for slot, item_id in data["inventory"]["items"].items():
                if str(slot).isdigit():
                    slot = int(slot)
                if item_id is not None:
                    try:
                        item_obj = self.build_item(int(item_id))
                        self.inventory.items[slot] = item_obj
                    except (ValueError, TypeError):
                        self.inventory.items[slot] = None
                else:
                    self.inventory.items[slot] = None
            if "coffres" in data:
                for saved in data["coffres"]:
                    for c in self.coffres:
                        if c.id == saved["id"]:
                            c.ouvert = saved["ouvert"]
                            c.contenu = saved["contenu"]
                            break
        except (FileNotFoundError, KeyError, json.JSONDecodeError):
            pass
