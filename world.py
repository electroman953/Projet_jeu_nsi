import pyxel

class World:
    
    def __init__(self, width, height, tm):
        self.width = width
        self.height = height
        self.tm = tm


    def place_map(self, x_player, y_player):
        u = x_player - self.width / 2
        v = y_player - self.height / 2
        x, y = 0, 0
        pyxel.bltm(x, y, self.tm, u, v, self.width, self.height)
        
    def deplace(self, player, speed = 1):
        if pyxel.btn(pyxel.KEY_RIGHT):
            player.x_center += speed
        if pyxel.btn(pyxel.KEY_LEFT):
            player.x_center -= speed
        if pyxel.btn(pyxel.KEY_UP):
            player.y_center -= speed
        if pyxel.btn(pyxel.KEY_DOWN):
            player.y_center += speed