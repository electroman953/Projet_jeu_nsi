import pyxel

class Arrow:
    def __init__(self, x, y, damage, rotation, direction = (1, 1), speed=8, type="basic", damage_multiplier=1, crit_chance_bonus=0, crit_multiplier_bonus=0):
        self.x = x
        self.y = y
        self.damage = damage
        self.rotation = rotation
        self.direction = direction
        self.speed = speed
        self.type = type
        self.damage_multiplier = damage_multiplier
        self.crit_chance_bonus = crit_chance_bonus
        self.crit_multiplier_bonus = crit_multiplier_bonus
        self.scale = 1
    def draw(self, app):
        screen_x = app.screen_center_x + (self.x - app.x_center)
        screen_y = app.screen_center_y + (self.y - app.y_center)
        pyxel.blt(screen_x - 16, screen_y - 16, 1, 0, 192, 32, 32, 3, self.rotation, self.scale)
    def move(self):
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
    def supprimer(self, app):
        if self.x < app.x_center - 512 or self.x > app.x_center + 512 or self.y < app.y_center - 512 or self.y > app.y_center + 512:
            app.projectiles.remove(self)
    def bout(self):
        return (self.x + self.direction[0] * 16, self.y + self.direction[1] * 16)
    def collision_mob(self, mob):
        tx, ty = self.bout()
        return mob.collision_rect(mob.x - mob.width//2, mob.y - mob.height//2, mob.width, mob.height, tx - 4, ty - 4, 8, 8)