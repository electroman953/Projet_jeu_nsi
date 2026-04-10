import pyxel

class World:
    
    def __init__(self, width, height, tm):
        self.width = width
        self.height = height
        self.tm = tm


    def place_map(self, x_player, y_player):
        u = x_player - self.width // 2
        v = y_player - self.height // 2
        x, y = 0, 0
        pyxel.bltm(x, y, self.tm, u, v, self.width, self.height)
        
    def deplace(self, app, speed = 1):
        dx, dy = 0, 0

        if pyxel.btn(pyxel.KEY_RIGHT):
            dx += speed
        if pyxel.btn(pyxel.KEY_LEFT):
            dx -= speed
        if pyxel.btn(pyxel.KEY_UP):
            dy -= speed
        if pyxel.btn(pyxel.KEY_DOWN):
            dy += speed

        app.player_x_abs += dx
        app.player_y_abs += dy
        app.x_center += dx
        app.y_center += dy

    def recentrer(self, app, speed = 5):
        if not app.recentrer:
            return

        diff_x = app.player_x_abs - app.x_center
        diff_y = app.player_y_abs - app.y_center

        if abs(diff_x) <= speed:
            app.x_center = app.player_x_abs
        else:
            app.x_center += speed if diff_x > 0 else -speed

        if abs(diff_y) <= speed:
            app.y_center = app.player_y_abs
        else:
            app.y_center += speed if diff_y > 0 else -speed

        if app.x_center == app.player_x_abs and app.y_center == app.player_y_abs:
            app.recentrer = False