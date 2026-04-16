import pyxel

class Coffre:
    def __init__(self, id, nom, x, y, contenu):
        self.id = id
        self.nom = nom
        self.x = x
        self.y = y
        self.contenu = contenu
        self.ouvert = False

    def ouvrir(self):
        if not self.ouvert:
            self.ouvert = True
            return f"Vous ouvrez le coffre '{self.nom}' et trouvez : {self.contenu}"
        else:
            return "Le coffre est déjà ouvert."

    def draw(self, app):
        screen_x = app.screen_center_x + (self.x - app.x_center)
        screen_y = app.screen_center_y + (self.y - app.y_center)
        if not self.ouvert:
            pyxel.rect(screen_x, screen_y, 16, 16, 8)  # Dessine un coffre simple (un carré)
        else:
            pyxel.rect(screen_x, screen_y, 16, 16, 7)  # Dessine un coffre fermé (un carré d'une autre couleur)
        #pyxel.blt(screen_x, screen_y, 0, 0, 0, 16, 16, colkey=0)