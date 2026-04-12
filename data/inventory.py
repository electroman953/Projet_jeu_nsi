import pyxel


class Inventory:
    def __init__(self):
        self.items = []
        self.on_screen = False
    def open(self):
        self.on_screen = not self.on_screen
    def afficher(self, app):
        if self.on_screen:
            px, py = 80, 40
            pyxel.rect(px, py, 320, 175, 1)
            pyxel.rectb(px, py, 320, 175, 6)

            # Preview joueur
            pyxel.rect(px+16, py+12, 48, 64, 5)
            pyxel.rectb(px+16, py+12, 48, 64, 6)
            pyxel.blt(px+28, py+20, 0, 0, 0, 23, 39, colkey=3)  # 11 = couleur transparente

            # Slots armure et arme
            for i in range(2):
                sx = px + 10 + i * 40
                pyxel.rect(sx, py+88, 32, 32, 5)
                pyxel.rectb(sx, py+88, 32, 32, 6)

            # Séparateur
            pyxel.line(px+92, py+4, px+92, py+171, 13)

            # Grille inventaire
            pyxel.text(px+148, py+6, "INVENTAIRE", 7)
            for row in range(4):
                for col in range(6):
                    sx, sy = px+100 + col*36, py+16 + row*36
                    pyxel.rect(sx, sy, 32, 32, 5)
                    pyxel.rectb(sx, sy, 32, 32, 6)