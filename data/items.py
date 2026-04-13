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
class Weapon(Item):
    def __init__(self, name, description, image_x, image_y, damage, crit_chance_bonus=0, crit_multiplier_bonus=0, attack_speed_bonus=0):
        super().__init__(name, description, image_x, image_y)
        self.parent_type = "weapon"
        self.liste_attributs["damage"] = damage
        self.liste_attributs["crit_chance_bonus"] = crit_chance_bonus
        self.liste_attributs["crit_multiplier_bonus"] = crit_multiplier_bonus
        self.liste_attributs["attack_speed_bonus"] = attack_speed_bonus

    def etat_arme(self, actif):
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
class range_weapon(Weapon):
    def __init__(self, name, description, image_x, image_y, damage, range, crit_chance_bonus=0.05, crit_multiplier_bonus=0.5, attack_speed_bonus=0.2):
        super().__init__(name, description, image_x, image_y, damage, crit_chance_bonus=0.05, crit_multiplier_bonus=0.5, attack_speed_bonus=0.2)
        self.liste_attributs["range"] = range
    def etat_arme(self, actif, app):
        pyxel.mouse(actif)
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and actif:
            self.attack(app)
        

class bow(range_weapon):
    def __init__(self, name, description, image_x, image_y, damage, range, crit_chance_bonus=0.05, crit_multiplier_bonus=0.5, attack_speed_bonus=0.2):
        super().__init__(name, description, image_x, image_y, damage, range, crit_chance_bonus, crit_multiplier_bonus, attack_speed_bonus)
        self.type = "bow"
        self.colkey = 7

    def attack(self, app):
        app.add_player_projectile("arrow", "basic")

class staff(range_weapon):
    def __init__(self, name, description, image_x, image_y, damage, range, crit_chance_bonus=0.05, crit_multiplier_bonus=0.5, attack_speed_bonus=0.2):
        super().__init__(name, description, image_x, image_y, damage, range, crit_chance_bonus, crit_multiplier_bonus, attack_speed_bonus)
        self.type = "staff"

preset_sword = sword("Épée de base", "Une épée simple mais efficace.", 32, 0, 10)
preset_bow = bow("Arc de base", "Un arc simple pour attaquer à distance.", 64, 0, 8, 3)
preset_staff = staff("Bâton de base", "Un bâton magique pour les attaques à distance.", 0, 0, 6, 4)
preset_armor = Armor("Armure de base", "Une armure simple pour se protéger.", 64, 224, 5)