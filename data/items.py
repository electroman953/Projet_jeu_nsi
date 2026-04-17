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
class Potion(Item):
    def __init__(self, name, description, image_x, image_y, attributs, value, duration=0):
        super().__init__(name, description, image_x, image_y)
        self.type = "potion"
        self.liste_attributs = attributs
        self.value = value
        self.duration = duration
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

