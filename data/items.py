import pyxel

class Item:
    def __init__(self, name, description, image_x, image_y):
        self.name = name
        self.description = description
        self.image_x = image_x
        self.image_y = image_y
        self.durability = 100
        self.colkey = 0
        self.type = None
        self.liste_attributs = {}
    def get_stats(self, app):
        stats = []
        for i, j in self.liste_attributs.items():
            if j != 0:
                stats.append(f"{i if i not in app.correspondance_nom else app.correspondance_nom[i]} : {j}")
        return stats
    def etat_arme(self, actif, app):
        pyxel.mouse(actif)
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and actif:
            app.orient_player_to_mouse()
            self.attack(app)

class Weapon(Item):
    def __init__(self, name, description, image_x, image_y, damage, crit_chance_bonus=0, crit_multiplier_bonus=0, attack_speed_bonus=0):
        super().__init__(name, description, image_x, image_y)
        self.parent_type = "weapon"
        self.liste_attributs["damage"] = damage
        self.liste_attributs["crit_chance_bonus"] = crit_chance_bonus
        self.liste_attributs["crit_multiplier_bonus"] = crit_multiplier_bonus
        self.liste_attributs["attack_speed_bonus"] = attack_speed_bonus

    def attack(self, app):
        pass

            
class Armor(Item):
    def __init__(self, name, description, image_x, image_y, defense, bonus_health=0):
        super().__init__(name, description, image_x, image_y)
        self.type = "armor"
        self.parent_type = "armor"

        self.liste_attributs["defense"] = defense
        self.liste_attributs["bonus_health"] = bonus_health

class sword(Weapon):
    def __init__(self, name, description, image_x, image_y, damage, crit_chance_bonus=0.05, crit_multiplier_bonus=0.5, attack_speed_bonus=0.2):
        super().__init__(name, description, image_x, image_y, damage, crit_chance_bonus=0.05, crit_multiplier_bonus=0.5, attack_speed_bonus=0.2)
        self.type = "sword"
    def attack(self, app):
        if app.sword_cooldown <= 0:
            app.player_slash()
            app.sword_cooldown = app.SWORD_COOLDOWN - self.liste_attributs.get("attack_speed_bonus", 0)
            app.player.en_attaque = 8
            app.player.next_anim_attaque = 3

class bow(Weapon):
    def __init__(self, name, description, image_x, image_y, damage, crit_chance_bonus=0.05, crit_multiplier_bonus=0.5, attack_speed_bonus=0.2):
        super().__init__(name, description, image_x, image_y, damage, crit_chance_bonus=crit_chance_bonus, crit_multiplier_bonus=crit_multiplier_bonus, attack_speed_bonus=attack_speed_bonus)
        self.type = "bow"
        self.colkey = 7

    def attack(self, app):
        if app.bow_cooldown <= 0:
            app.add_player_projectile("arrow", "basic")
            app.bow_cooldown = app.BOW_COOLDOWN - self.liste_attributs["attack_speed_bonus"]
            app.player.en_attaque = 8
            app.player.next_anim_attaque = 3

class staff(Weapon):
    def __init__(self, name, description, image_x, image_y, damage, crit_chance_bonus=0.05, crit_multiplier_bonus=0.5, attack_speed_bonus=0.2):
        super().__init__(name, description, image_x, image_y, damage, crit_chance_bonus=crit_chance_bonus, crit_multiplier_bonus=crit_multiplier_bonus, attack_speed_bonus=attack_speed_bonus)
        self.type = "staff"

items = {
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

def make_item(data):
    type_, name, desc, x, y, stat, *extra = data
    bonus = extra[0] if extra else {}
    constructors = {"sword": sword, "bow": bow, "staff": staff, "armor": Armor}
    return constructors[type_](name, desc, x, y, stat, **bonus)