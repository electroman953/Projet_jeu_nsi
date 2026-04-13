
import pyxel

class Mob:
    def __init__(self, health, damage, type, x, y, w, h, c):
        self.health = health
        self.damage = damage
        self.type = type
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.color = c
    def draw(self, app):
        self.screen_x = app.screen_center_x + (self.x - app.x_center)
        self.screen_y = app.screen_center_y + (self.y - app.y_center)
        pyxel.rect(self.screen_x, self.screen_y, self.width, self.height, self.color)
        #pyxel.blt(self.x, self.y, 0, 0, 0, 16, 16)
    def move(self, app, player_x, player_y):
        if self.health <= 0:
            return
        dx = player_x - self.x
        dy = player_y - self.y
        if abs(dx) > abs(dy):
            step_x = 1 if dx > 0 else -1
            if not self.next_dest_is_obstacle(app, step_x, 0):
                self.x += step_x
        else:
            step_y = 1 if dy > 0 else -1
            if not self.next_dest_is_obstacle(app, 0, step_y):
                self.y += step_y

    def collision_rect(self, x1, y1, w1, h1, x2, y2, w2, h2):
        return (x1 < x2 + w2 and
                x1 + w1 > x2 and
                y1 < y2 + h2 and
                y1 + h1 > y2)
    
    def next_dest_is_obstacle(self, app, dx, dy):
        next_x = self.x - self.width//2 + dx
        next_y = self.y - self.height//2 + dy
        for obs in app.obstacle:
            if self.collision_rect(next_x, next_y, self.width, self.height, obs[0]*8, obs[1]*8, 8, 8):
                return True
        return False