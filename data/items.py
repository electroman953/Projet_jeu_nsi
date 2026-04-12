class Item:
    def __init__(self, name, description, image_x, image_y):
        self.name = name
        self.description = description
        self.image_x = image_x
        self.image_y = image_y
        self.durability = 100
class Weapon(Item):
    def __init__(self, name, description, image_x, image_y, damage):
        super().__init__(name, description, image_x, image_y)
        self.damage = damage
class Armor(Item):
    def __init__(self, name, description, image_x, image_y, defense):
        super().__init__(name, description, image_x, image_y)
        self.defense = defense
        self.type = "armor"
class sword(Weapon):
    def __init__(self, name, description, image_x, image_y, damage):
        super().__init__(name, description, image_x, image_y, damage)
        self.type = "sword"
class range_weapon(Weapon):
    def __init__(self, name, description, image_x, image_y, damage, range):
        super().__init__(name, description, image_x, image_y, damage)
        self.range = range
class bow(range_weapon):
    def __init__(self, name, description, image_x, image_y, damage, range):
        super().__init__(name, description, image_x, image_y, damage, range)
        self.type = "bow"
class staff(range_weapon):
    def __init__(self, name, description, image_x, image_y, damage, range):
        super().__init__(name, description, image_x, image_y, damage, range)
        self.type = "staff"

preset_sword = sword("Épée de base", "Une épée simple mais efficace.", 0, 0, 10)
preset_bow = bow("Arc de base", "Un arc simple pour attaquer à distance.", 0, 0, 8, 3)
preset_staff = staff("Bâton de base", "Un bâton magique pour les attaques à distance.", 0, 0, 6, 4)
preset_armor = Armor("Armure de base", "Une armure simple pour se protéger.", 0, 0, 5)