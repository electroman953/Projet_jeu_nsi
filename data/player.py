import pyxel

class Player:

    def __init__(self):
        self.speed = 3
        self.width = 32
        self.height = 32

    def deplace(self, app):
        #coordonnées du joueur relatif à l'écran
        xp_r = app.screen_center_x + (app.player_x_abs - app.x_center) - 16
        yp_r = app.screen_center_y + (app.player_y_abs - app.y_center) - 16
        if pyxel.btn(pyxel.KEY_UP) and yp_r>=0:
            app.player_y_abs -= self.speed
        if pyxel.btn(pyxel.KEY_DOWN) and yp_r<=app.height-self.height:
            app.player_y_abs += self.speed
        if pyxel.btn(pyxel.KEY_LEFT) and xp_r>=0:
            app.player_x_abs -= self.speed
        if pyxel.btn(pyxel.KEY_RIGHT) and xp_r<=app.width-self.width: 
            app.player_x_abs += self.speed

    def check_key(self, app):
        if pyxel.btnp(pyxel.KEY_SPACE):
            if app.timestop == False:
                app.timestop = True
            else:
                app.timestop = False
                app.recentrer = True
        if pyxel.btnp(pyxel.KEY_R):
            print(app.obstacle)