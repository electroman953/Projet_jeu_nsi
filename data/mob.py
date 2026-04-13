
import pyxel

class Mob:
    def __init__(self, health, damage, type, x, y, w, h, c, xp_drop_range, loot_table=None):
        self.health = health
        self.damage = damage
        self.type = type
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.color = c
        self.vitesse = 1
        self.chemin  = []
        self.xp_drop_range = xp_drop_range
        self.loot_table = loot_table if loot_table is not None else []
        self.timer = 0
        self.detection_range = 200
    def draw(self, app):
        self.screen_x = app.screen_center_x + (self.x - app.x_center)
        self.screen_y = app.screen_center_y + (self.y - app.y_center)
        pyxel.rect(self.screen_x, self.screen_y, self.width, self.height, self.color)
        #pyxel.blt(self.x, self.y, 0, 0, 0, 16, 16)
    def move(self, app, player_x, player_y):
        if self.health <= 0:
            return
        if app.timestop:
            return
        if abs(self.x - player_x) + abs(self.y - player_y) > self.detection_range:
            return
        self.timer += 1
        if self.timer % 30 == 0:
            self.timer = 0
            debut = (self.x//8, self.y//8)
            fin = (player_x//8, player_y//8)
            self.chemin = app.world.parcours_largeur(debut, fin, app)
        if self.chemin:
            next_cell = self.chemin[0]
            next_x = next_cell[0]*8 + 4
            next_y = next_cell[1]*8 + 4
            dx = next_x - self.x
            dy = next_y - self.y
            if abs(dx) > self.vitesse:
                dx = self.vitesse if dx > 0 else -self.vitesse
            elif abs(dx) > 0:
                dx = dx
            if abs(dy) > self.vitesse:
                dy = self.vitesse if dy > 0 else -self.vitesse
            elif abs(dy) > 0:
                dy = dy
            self.x += dx
            self.y += dy
            if self.x == next_x and self.y == next_y:
                self.chemin.pop(0)
            
    def collision_rect(self, x1, y1, w1, h1, x2, y2, w2, h2):
        return (x1 < x2 + w2 and
                x1 + w1 > x2 and
                y1 < y2 + h2 and
                y1 + h1 > y2)
    def prendre_degats(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
    def is_dead(self, app):
        if self.health == 0:
            xp_drop = pyxel.rndi(self.xp_drop_range[0], self.xp_drop_range[1])
            app.player.experience += xp_drop
            print(app.player.experience)
            for item in self.loot_table:
                if pyxel.rndf() < item["drop_chance"]:
                    app.inventory.add_item(item["item"])
            app.mobs.remove(self)
            

    def next_dest_is_obstacle(self, app, dx, dy):
        next_x = self.x - self.width//2 + dx
        next_y = self.y - self.height//2 + dy
        for obs in app.obstacle:
            if self.collision_rect(next_x, next_y, self.width, self.height, obs[0]*8, obs[1]*8, 8, 8):
                return True
        return False