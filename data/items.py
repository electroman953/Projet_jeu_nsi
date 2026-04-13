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
class Weapon(Item):
    def __init__(self, name, description, image_x, image_y, damage):
        super().__init__(name, description, image_x, image_y)
        self.damage = damage
        self.parent_type = "weapon"
    
    def etat_arme(self, actif):
        pass

            
class Armor(Item):
    def __init__(self, name, description, image_x, image_y, defense):
        super().__init__(name, description, image_x, image_y)
        self.defense = defense
        self.type = "armor"
        self.parent_type = "armor"    
class sword(Weapon):
    def __init__(self, name, description, image_x, image_y, damage):
        super().__init__(name, description, image_x, image_y, damage)
        self.type = "sword"
class range_weapon(Weapon):
    def __init__(self, name, description, image_x, image_y, damage, range):
        super().__init__(name, description, image_x, image_y, damage)
        self.range = range
    def etat_arme(self, actif, app):
        pyxel.mouse(actif)
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and actif:
            self.attack(app)
        

class bow(range_weapon):
    def __init__(self, name, description, image_x, image_y, damage, range):
        super().__init__(name, description, image_x, image_y, damage, range)
        self.type = "bow"
        self.colkey = 7

    def attack(self, app):
        app.add_player_projectile("arrow", "basic")

class staff(range_weapon):
    def __init__(self, name, description, image_x, image_y, damage, range):
        super().__init__(name, description, image_x, image_y, damage, range)
        self.type = "staff"

preset_sword = sword("Épée de base", "Une épée simple mais efficace.", 32, 0, 10)
preset_bow = bow("Arc de base", "Un arc simple pour attaquer à distance.", 64, 0, 8, 3)
preset_staff = staff("Bâton de base", "Un bâton magique pour les attaques à distance.", 0, 0, 6, 4)
preset_armor = Armor("Armure de base", "Une armure simple pour se protéger.", 64, 224, 5)