import pyxel

class World:
    
    def __init__(self, width, height, tm):
        self.width = width
        self.height = height
        self.tm = tm
        self.word_width = 2048
        self.word_height = 2048


    def place_map(self, x_player, y_player):
        u = x_player - self.width // 2
        v = y_player - self.height // 2
        x, y = 0, 0
        pyxel.bltm(x, y, self.tm, u, v, self.width, self.height)
        
    def deplace(self, app, speed=1):
        dx, dy = 0, 0

        if pyxel.btn(pyxel.KEY_RIGHT):
            app.player.direction = "right"
            for _ in range(speed):
                if not app.player.next_dest_is_obstacle(app, dx + 1, dy):
                    dx += 1
                else:
                    break
        if pyxel.btn(pyxel.KEY_LEFT):
            app.player.direction = "left"
            for _ in range(speed):
                if not app.player.next_dest_is_obstacle(app, dx - 1, dy):
                    dx -= 1
                else:
                    break
        if pyxel.btn(pyxel.KEY_UP):
            app.player.direction = "up"
            for _ in range(speed):
                if not app.player.next_dest_is_obstacle(app, dx, dy - 1):
                    dy -= 1
                else:
                    break
        if pyxel.btn(pyxel.KEY_DOWN):
            app.player.direction = "down"
            for _ in range(speed):
                if not app.player.next_dest_is_obstacle(app, dx, dy + 1):
                    dy += 1
                else:
                    break

        app.player_x_abs = max(app.player.width // 2, min(app.player_x_abs + dx, self.word_width - app.player.width // 2))
        app.player_y_abs = max(app.player.height // 2, min(app.player_y_abs + dy, self.word_height - app.player.height // 2))
        app.x_center = max(app.width // 2, min(app.player_x_abs, self.word_width - app.width // 2))
        app.y_center = max(app.height // 2, min(app.player_y_abs, self.word_height - app.height // 2))

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
