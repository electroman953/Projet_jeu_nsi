import pyxel

class Arrow:
    def __init__(self, x, y, damage, rotation, direction = (1, 1), speed=3, type="basic"):
        self.x = x
        self.y = y
        self.damage = damage
        self.rotation = rotation
        self.direction = direction
        self.speed = speed
        self.type = type
        self.scale = 1
    def draw(self, app):
        screen_x = app.screen_center_x + (self.x - app.x_center)
        screen_y = app.screen_center_y + (self.y - app.y_center)
        pyxel.blt(screen_x - 16, screen_y - 16, 2, 96, 192, 32, 32, 3, self.rotation, self.scale)
    def move(self):
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
    def supprimer(self, app):
        if self.x < app.x_center - 512 or self.x > app.x_center + 512 or self.y < app.y_center - 512 or self.y > app.y_center + 512:
            app.projectiles.remove(self)