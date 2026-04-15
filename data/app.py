import pyxel
import random
from data.world import World
from data.player import Player
from data.inventory import Inventory
from data.mob import Mob
from data.arrow import Arrow

class App:
    
    def __init__(self):
        self.start()
        pyxel.init(self.width, self.height, title = "Jeu du héros", fps=60)
        pyxel.load('../Textures/res.pyxres')
        print(pyxel.VERSION)
        pyxel.run(self.update, self.draw)

    def start(self):
        self.on_menu = True
        self.timestop = False
        self.TIMESTOP_DURATION = 5
        self.TIMESTOP_COOLDOWN = 10
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
        self.height = 256
        self.elt_col = [(21, 1), (21, 2), (21, 3), (21, 4), (21, 5), (21, 6), (21, 7), (21, 8), (21, 9), (21, 10), (22, 1), (22, 2), (22, 3), (22, 4), (22, 5), (22, 6), (22, 7), (22, 8), (22, 9), (22, 10), (21, 13), (21, 14), (22, 13), (22, 14), (1, 17), (1, 18), (2, 17), (2, 18), (3, 17), (3, 18), (4, 17), (4, 18), (5, 17), (5, 18), (6, 17), (6, 18), (7, 17), (7, 18), (8, 17), (8, 18), (9, 17), (9, 18), (10, 17), (10, 18), (12, 16), (12, 17), (12, 18), (12, 19), (13, 16), (13, 17), (13, 18), (13, 19), (14, 16), (14, 17), (14, 18), (14, 19), (15, 16), (15, 17), (15, 18), (15, 19), (16, 4), (16, 5), (16, 6), (16, 7), (16, 8), (16, 9), (17, 4), (17, 5), (17, 6), (17, 7), (17, 8), (17, 9), (18, 4), (18, 5), (18, 6), (18, 7), (18, 8), (18, 9), (19, 4), (19, 5), (19, 6), (19, 7), (19, 8), (19, 9)]
        self.screen_center_x = self.width // 2
        self.screen_center_y = self.height // 2
        self.correspondance_nom = {"damage" : "DMG", "crit_chance_bonus" : "CRIT CHANCE", "crit_multiplier_bonus" : "CRIT MULTIPLIER", "attack_speed_bonus" : "ATK SPEED", "defense" : "DEF", "bonus_health" : "HP"}
        self.palette_normal = [
            0x0D0D0D, 0x1D2B53, 0x7E2553, 0x609266,
            0xAB5236, 0x1E8C0A, 0xC2C3C7, 0xFFF1E8,  
            0xFF004D, 0xFFA300, 0xFFEC27, 0x00E436,
            0x4ba344, 0x83769C, 0xFF77A8, 0xFFCCAA   
        ]

        pyxel.colors[:] = self.palette_normal  
        self.palette_timestop = [
            0x0D0D0D, 0x1D2B53, 0x7E2553, 0x008751,
            0xAB5236, 0x555555, 0xC2C3C7, 0xFFF1E8,  
            0xFF004D, 0xFFA300, 0xFFEC27, 0x00E436,
            0xAAAAAA, 0x83769C, 0xFF77A8, 0xFFCCAA   
        ]
        self.items = {
            # === STAFFS ===
            # Starter : 5-6 coups normal
            1:  ("staff", "Bâton de novice",     "Un simple bâton en bois, gravé de runes pâles.",                        0,   0,  8,  {"crit_chance_bonus": 0.0,  "crit_multiplier_bonus": 0.0}),
            # Mid : ~3 coups normal, two-shot crit
            10: ("staff", "Sceptre de crâne",    "Un sceptre orné d'un crâne démoniaque qui pulse d'énergie sombre.",    32, 128, 22, {"crit_chance_bonus": 0.07, "crit_multiplier_bonus": 0.2}),

            # === SWORDS ===
            # Tier 1 starter : ~5 coups normal
            2:  ("sword", "Dague azurée",        "Une dague légère à lame bleue, idéale pour des attaques rapides.",      32,  0,  8, {"crit_chance_bonus": 0.0,  "crit_multiplier_bonus": 0.0,  "attack_speed_bonus": 0.3}),
            3:  ("sword", "Épée brisée",         "Une épée ancienne dont la lame a été reforgée à la hâte.",               0, 32,  8, {"crit_chance_bonus": 0.0,  "crit_multiplier_bonus": 0.0,  "attack_speed_bonus": 0.0}),
            # Tier 2 early-mid : ~3-4 coups normal
            4:  ("sword", "Épée de foudre",      "Une épée courte crépitante d'éclairs bleutés.",                         32, 32, 15, {"crit_chance_bonus": 0.05, "crit_multiplier_bonus": 0.1,  "attack_speed_bonus": 0.1}),
            7:  ("sword", "Poignard de l'ombre", "Un poignard fin et discret, parfait pour frapper dans le dos.",           0, 96, 13, {"crit_chance_bonus": 0.12, "crit_multiplier_bonus": 0.0,  "attack_speed_bonus": 0.3}),
            # Tier 3 mid : two-shot crit (~50 dégâts), ~3 coups normal
            5:  ("sword", "Lance du chaos",      "Une lance dont la tête diffuse une énergie corrompue.",                   0, 64, 23, {"crit_chance_bonus": 0.0,  "crit_multiplier_bonus": 0.2,  "attack_speed_bonus": 0.0}),
            6:  ("sword", "Épée de sang",        "Une lame écarlate gorgée de la force de ses victimes.",                  32, 64, 22, {"crit_chance_bonus": 0.1,  "crit_multiplier_bonus": 0.15, "attack_speed_bonus": 0.0}),
            9:  ("sword", "Bident maudit",       "Un double pic maudit dont les deux pointes empoisonnent les plaies.",     0,128, 21, {"crit_chance_bonus": 0.06, "crit_multiplier_bonus": 0.2,  "attack_speed_bonus": 0.0}),
            # Tier 4 endgame : one/two-shot fiable
            8:  ("sword", "Épée runique",        "Une grande lame gravée de runes conférant une puissance surnaturelle.",  32, 96, 35, {"crit_chance_bonus": 0.12, "crit_multiplier_bonus": 0.5,  "attack_speed_bonus": 0.0}),

            # === BOWS ===
            # Tier 1 starter
            17: ("bow",   "Arc simple",          "L'arc de tout aventurier qui débute sa quête.",                          64,   0,  6, {"crit_chance_bonus": 0.0,  "crit_multiplier_bonus": 0.0,  "attack_speed_bonus": 0.0}),
            16: ("bow",   "Arc de débutant",     "Un arc rudimentaire en bois brut, fiable mais sans éclat.",              32, 224,  9, {"crit_chance_bonus": 0.0,  "crit_multiplier_bonus": 0.0,  "attack_speed_bonus": 0.1}),
            15: ("bow",   "Arc court",           "Un arc léger et maniable, facile à utiliser en combat rapproché.",        0, 224,  9, {"crit_chance_bonus": 0.0,  "crit_multiplier_bonus": 0.0,  "attack_speed_bonus": 0.3}),
            # Tier 2 early-mid
            12: ("bow",   "Arc de racines",      "Un arc noueux façonné dans des racines entrelacées.",                    32, 160, 14, {"crit_chance_bonus": 0.05, "crit_multiplier_bonus": 0.0,  "attack_speed_bonus": 0.1}),
            11: ("bow",   "Arc long elfique",    "Un arc fin taillé dans un bois enchanté, précis sur longue portée.",     0, 160, 16, {"crit_chance_bonus": 0.08, "crit_multiplier_bonus": 0.1,  "attack_speed_bonus": 0.0}),
            # Tier 3 mid : two-shot crit
            14: ("bow",   "Arc de sang",         "Teint de sang séché, cet arc décuple la rage du tireur.",                32, 192, 22, {"crit_chance_bonus": 0.07, "crit_multiplier_bonus": 0.2,  "attack_speed_bonus": 0.0}),
            13: ("bow",   "Arc corrompu",        "Un arc tordu par la magie noire, dont les flèches percent les armures.", 0, 192, 24, {"crit_chance_bonus": 0.06, "crit_multiplier_bonus": 0.15, "attack_speed_bonus": 0.0}),
            # Tier 4 endgame
            19: ("bow",   "Arc de tempête",      "Cet arc massif déchaîne des flèches comme des éclairs.",                 64,  32, 28, {"crit_chance_bonus": 0.1,  "crit_multiplier_bonus": 0.3,  "attack_speed_bonus": 0.25}),
            23: ("bow",   "Arc draconique",      "Taillé dans l'os d'un dragon, il vibre d'une puissance colossale.",      64,  96, 32, {"crit_chance_bonus": 0.12, "crit_multiplier_bonus": 0.4,  "attack_speed_bonus": 0.0}),
            21: ("bow",   "Arc abyssal",         "Un arc forgé dans les profondeurs, ses flèches déchirent l'air.",        64,  64, 35, {"crit_chance_bonus": 0.12, "crit_multiplier_bonus": 0.5,  "attack_speed_bonus": 0.1}),

            # === ARMORS ===
            18: ("armor", "Tunique de cuir",     "Une protection légère en cuir tanné.",                                   96,   0,  3, {"bonus_health": 10}),
            20: ("armor", "Cotte de mailles",    "Une armure en mailles d'acier, bon équilibre protection/poids.",         96,  32,  6, {"bonus_health": 15}),
            22: ("armor", "Plastron solide",     "Un plastron en acier renforcé gravé aux armes d'une vieille guilde.",    96,  64,  9, {"bonus_health": 20}),
            24: ("armor", "Armure de plaques",   "Une lourde armure de plaques qui repousse les coups les plus violents.", 96,  96, 12, {"bonus_health": 25}),
            25: ("armor", "Armure d'os",         "Façonnée d'os monstrueux, elle dégage une aura intimidante.",            64, 128, 10, {"bonus_health": 20}),
            26: ("armor", "Armure démoniaque",   "Forgée aux enfers, elle brûle les attaquants qui la frôlent.",           96, 128, 14, {"bonus_health": 30}),
            27: ("armor", "Armure chitineuse",   "Taillée dans la carapace d'un colosse insectoïde.",                      64, 160, 12, {"bonus_health": 25}),
            28: ("armor", "Armure du seigneur",  "L'armure d'un seigneur de guerre, symbole de puissance absolue.",        96, 160, 16, {"bonus_health": 35}),
            29: ("armor", "Armure abyssale",     "Une armure noire profonde qui absorbe la lumière et les coups.",         64, 192, 18, {"bonus_health": 30}),
            30: ("armor", "Armure légendaire",   "Le summum de l'artisanat, portée par les héros des âges anciens.",       64, 224, 22, {"bonus_health": 40}),
        }

        # Coordonnées de spawn modifiables
        self.spawn_x = 8 * 38
        self.spawn_y = 9 * 41

        self.x_center, self.y_center = self.spawn_x, self.spawn_y

        self.projectiles = []
        self.mobs = [
            ('slime', random.randint(32, 1000), random.randint(32, 1000))
            for _ in range(12)
        ]
        self.create_mobs()
        self.inventory = Inventory(self)
        self.player = Player()
        self.player_x_abs, self.player_y_abs = self.spawn_x, self.spawn_y
        self.world = World(self.width, self.height,0)
        self.recentrer = False
        self.obstacle = []
        self.debug_hitbox = True

    def create_mobs(self):
        temp = []
        type={"slime": {"health": 100, "damage": 10, "height": 16, "width": 16, "color": 8, "xp_drop_range": (5, 15), "loot_table": []}}
        for mob_type, x, y in self.mobs:
            mob = Mob(type[mob_type]["health"], type[mob_type]["damage"], mob_type, x, y, type[mob_type]["width"], type[mob_type]["height"], type[mob_type]["color"], type[mob_type]["xp_drop_range"], type[mob_type]["loot_table"])
            temp.append(mob)
        self.mobs = temp

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

    def update(self):
        if self.timestop:
            self.player.colkey = 3
        else:
            self.player.colkey = 5
        if self.on_menu:
            if (224<pyxel.mouse_x<288 and 116<pyxel.mouse_y<148 and pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT)) or pyxel.btnr(pyxel.KEY_SPACE):
                self.on_menu=False
        elif self.player.is_dead():
            if (224<pyxel.mouse_x<288 and 116<pyxel.mouse_y<148 and pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT)) or pyxel.btnr(pyxel.KEY_SPACE):
                self.start()
        else:
            if pyxel.btnp(pyxel.KEY_H):
                self.debug_hitbox = not self.debug_hitbox
            self.player.check_key(self)
            if pyxel.frame_count % 6 == 0:
                for i in self.mobs:
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
            
            if self.timestop == False:
                self.world.deplace(self, self.player.speed)
            else:
                self.player.deplace(self)
                # Keep player on screen during timestop
                hw = self.player.width // 2
                hh = self.player.height // 2
                self.player_x_abs = max(self.x_center - self.width//2 + hw, min(self.player_x_abs, self.x_center + self.width//2 - hw))
                self.player_y_abs = max(self.y_center - self.height//2 + hh, min(self.player_y_abs, self.y_center + self.height//2 - hh))
                if self.timestop_timer == 0:
                    self.timestop = False
                    self.recentrer = True
            
    def draw(self):
        if self.on_menu:
            pyxel.cls(0)
            pyxel.mouse(True)
            pyxel.rect(224,116,64,32,7)
            pyxel.text(250, 132, 'Start', 0)
        elif self.player.is_dead():
            pyxel.cls(0)
            pyxel.text(224, 100, 'You Died', 7)
            pyxel.rect(224,116,64,32,7)
        else:
            pyxel.cls(0)
            if self.on_menu:
                return
            
            self.world.place_map(self.x_center, self.y_center, self)
            self.player.draw(self)
            self.place_mobs()
            self.place_projectiles()
            self.draw_hud()
            self.player.show_dmg(self)
            if self.timestop:
                pyxel.colors[:] = self.palette_timestop
            else:
                pyxel.colors[:] = self.palette_normal    
            if self.inventory.on_screen:
                self.inventory.afficher(self)
                self.inventory.over_item(self)
            if self.debug_hitbox:
                self.draw_debug_hitboxes()

    def place_mobs(self):
        for i in self.mobs:
            i.draw(self)
            i.move(self, self.player_x_abs, self.player_y_abs)
    
    def place_projectiles(self):
        for i in self.projectiles:
            i.draw(self)
            if not self.timestop:
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

    def orient_player_to_mouse(self):
        player_center_x = self.screen_center_x + (self.player_x_abs - self.x_center)
        player_center_y = self.screen_center_y + (self.player_y_abs - self.y_center)
        dx = pyxel.mouse_x - player_center_x
        dy = pyxel.mouse_y - player_center_y
        if abs(dx) >= abs(dy):
            self.player.direction = "right" if dx >= 0 else "left"
        else:
            self.player.direction = "down" if dy >= 0 else "up"

    def get_melee_hitboxes(self):
        slash_range = self.SLASH_RANGE
        player_box = (
            self.player_x_abs - self.player.width // 2,
            self.player_y_abs - self.player.height // 2,
            self.player.width,
            self.player.height,
        )
        if self.player.direction == 'up':
            slash_box = (player_box[0], player_box[1] - slash_range, player_box[2], slash_range)
        elif self.player.direction == 'down':
            slash_box = (player_box[0], player_box[1] + player_box[3], player_box[2], slash_range)
        elif self.player.direction == 'left':
            slash_box = (player_box[0] - slash_range, player_box[1], slash_range, player_box[3])
        else:  # right
            slash_box = (player_box[0] + player_box[2], player_box[1], slash_range, player_box[3])
        return player_box, slash_box

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

    def load_walls(self):
        self.obstacle = []
        
        for x in range(self.x_center - self.width//2, self.x_center + self.width//2, 8):
            for y in range(self.y_center - self.height//2, self.y_center + self.height//2, 8):                
                
                if pyxel.tilemaps[self.world.tm].pget(x // 8, y // 8) in self.elt_col:
                    self.obstacle.append((x//8, y//8))

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
    
    def draw_hud(self):
        pyxel.text(10,10,f"Health :{self.player.health}", 7)
        if self.timestop_cooldown>0:
            pyxel.text(10,20,f"Timestop ready in: {self.timestop_cooldown}s", 7)
        elif self.timestop:
            pyxel.text(10,20,f"Timestop left: {self.timestop_timer}s", 7)
        else:
            pyxel.text(10,20,f"Timestop is ready", 7)
        pyxel.text(10,30,f"XP: {self.player.experience}", 7)
