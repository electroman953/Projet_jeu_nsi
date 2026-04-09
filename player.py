import pyxel
class Player:

    def __init__(self):
        self.speed = 5

    def deplace(self, app):
        if pyxel.btn(pyxel.KEY_UP):
            app.player_y -= self.speed
        if pyxel.btn(pyxel.KEY_DOWN):
            app.player_y += self.speed
        if pyxel.btn(pyxel.KEY_LEFT):
            app.player_x -= self.speed
        if pyxel.btn(pyxel.KEY_RIGHT):
            app.player_x += self.speed

    def check_key(self, app):
        if pyxel.btnp(pyxel.KEY_SPACE):
            if app.timestop == False:
                app.timestop = True
            else:
                app.timestop = False
                app.recentrer = True