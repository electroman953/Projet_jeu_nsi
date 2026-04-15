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
        
        self.knockback_vx = 0
        self.knockback_vy = 0
        
        self.xp_drop_range = xp_drop_range
        self.loot_table = loot_table if loot_table is not None else []
        self.timer = 0
        self.detection_range = 200
    def draw(self, app):
        self.screen_x = app.screen_center_x + (self.x - app.x_center) - self.width // 2
        self.screen_y = app.screen_center_y + (self.y - app.y_center) - self.height // 2
        pyxel.rect(self.screen_x, self.screen_y, self.width, self.height, self.color)
        #pyxel.blt(self.x, self.y, 0, 0, 0, 16, 16)
    def move(self, app, player_x, player_y):
        if self.health <= 0:
            return
        if app.timestop:
            return
            
        if abs(self.knockback_vx) > 0.1 or abs(self.knockback_vy) > 0.1:
            move_x = int(self.knockback_vx)
            move_y = int(self.knockback_vy)
            
            if move_x != 0 and not self.next_dest_is_obstacle(app, move_x, 0):
                self.x += move_x
            if move_y != 0 and not self.next_dest_is_obstacle(app, 0, move_y):
                self.y += move_y
                
            self.x = max(self.width // 2, min(self.x, app.world.word_width - self.width // 2))
            self.y = max(self.height // 2, min(self.y, app.world.word_height - self.height // 2))

            self.knockback_vx *= 0.8
            self.knockback_vy *= 0.8
            if abs(self.knockback_vx) < 0.5: self.knockback_vx = 0
            if abs(self.knockback_vy) < 0.5: self.knockback_vy = 0
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
            next_x = next_cell[0] * 8 + 4
            next_y = next_cell[1] * 8 + 4
            dx = next_x - self.x
            dy = next_y - self.y
            if abs(dx) > self.vitesse:
                dx = self.vitesse if dx > 0 else -self.vitesse
            if abs(dy) > self.vitesse:
                dy = self.vitesse if dy > 0 else -self.vitesse

            if dx != 0 or dy != 0:
                hit_player = self.next_dest_is_player(app, dx, dy)
                if hit_player:
                    app.player.take_damage(app, self.damage)
                elif not self.next_dest_is_obstacle(app, dx, dy):
                    self.x += dx
                    self.y += dy
                else:
                    if dx != 0:
                        if self.next_dest_is_player(app, dx, 0):
                            hit_player = True
                        elif not self.next_dest_is_obstacle(app, dx, 0):
                            self.x += dx
                    if dy != 0:
                        if self.next_dest_is_player(app, 0, dy):
                            hit_player = True
                        elif not self.next_dest_is_obstacle(app, 0, dy):
                            self.y += dy
                    if hit_player:
                        app.player.take_damage(self.damage)

            if self.x == next_x and self.y == next_y:
                self.chemin.pop(0)
    def collision_rect(self, x1, y1, w1, h1, x2, y2, w2, h2):
        return (x1 < x2 + w2 and
                x1 + w1 > x2 and
                y1 < y2 + h2 and
                y1 + h1 > y2)
    def prendre_degats(self, damage):
        print(f"Mob took {damage} damage")
        self.health -= damage
        if self.health <= 0:
            self.health = 0

    def appliquer_knockback(self, app, source_x, source_y, force=20):
        if self.health <= 0 or force <= 0:
            return
        dx = self.x - source_x
        dy = self.y - source_y
        distance = pyxel.sqrt(dx**2 + dy**2)
        if distance == 0:
            dx, dy = 1, 0
            distance = 1
            
        # On définit une vélocité initiale en fonction de la force
        self.knockback_vx = (dx / distance) * (force / 3)
        self.knockback_vy = (dy / distance) * (force / 3)
        self.chemin = []

    def is_dead(self, app):
        if self.health == 0:
            xp_drop = pyxel.rndi(self.xp_drop_range[0], self.xp_drop_range[1])
            app.player.experience += xp_drop
            print(app.player.experience)
            for item in self.loot_table:
                if pyxel.rndf() < item["drop_chance"]:
                    app.inventory.add_item(item["item"])
            app.mobs.remove(self)

    def next_dest_is_player(self, app, dx, dy):
        next_x = self.x - self.width // 2 + dx
        next_y = self.y - self.height // 2 + dy
        player_x = app.player_x_abs - app.player.width // 2
        player_y = app.player_y_abs - app.player.height // 2
        if self.collision_rect(next_x, next_y, self.width, self.height,
                                player_x, player_y, app.player.width, app.player.height):
            return True
        return False

    def next_dest_is_obstacle(self, app, dx, dy):
        next_x = self.x - self.width//2 + dx
        next_y = self.y - self.height//2 + dy
        for obs in app.obstacle:
            if self.collision_rect(next_x, next_y, self.width, self.height, obs[0]*8, obs[1]*8, 8, 8):
                return True
        return False