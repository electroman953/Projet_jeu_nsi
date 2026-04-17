import pyxel
import random
from data.items import sword, bow, Armor, Weapon, Potion

class Coffre:
    def __init__(self, id, nom, x, y, width, height, tier):
        self.id = id
        self.nom = nom
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tier = tier
        self.contenu = self.generer_contenu()
        self.ouvert = False

    def ouvrir(self):
        if not self.ouvert:
            self.ouvert = True
            return self.contenu  # retourne l'objet Item directement
        else:
            return None

    def generer_contenu(self):
        # Mapping tier -> item IDs possibles (correspondant à self.items dans app.py)
        a = {
            1: [2, 3, 15, 16, 17, 18, 20, 31],
            2: [4, 7, 11, 12, 22, 24, 25, 32],
            3: [5, 6, 9, 13, 14, 26, 27, 28, 33],
            4: [8, 19, 21, 23, 29, 30, 34]
        }
        tier_key = self.tier if self.tier in a else 1
        return random.choice(a[tier_key])  # retourne un item_id

    def draw(self, app):
        screen_x = app.screen_center_x + (self.x - app.x_center)
        screen_y = app.screen_center_y + (self.y - app.y_center)
        if not self.ouvert:
            pyxel.blt(screen_x, screen_y, 1, 0, 224, self.width, self.height, colkey=12)
        else:
            pyxel.blt(screen_x, screen_y-4, 1, 32, 192, self.width, self.height+4, colkey=12)