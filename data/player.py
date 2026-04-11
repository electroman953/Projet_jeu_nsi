import pyxel

class Player:

    def __init__(self):
        self.speed = 5
        self.width = 19
        self.height = 34
        self.direction = "down"

    def deplace(self, app):
        #coordonnées du joueur relatif à l'écran
        xp_r = app.screen_center_x + (app.player_x_abs - app.x_center) - self.width//2
        yp_r = app.screen_center_y + (app.player_y_abs - app.y_center) - self.height//2
        if pyxel.btn(pyxel.KEY_UP) and yp_r >= 0:
            self.direction = "up"
            for i in range(self.speed):
                if not self.next_dest_is_obstacle(app, 0, -1):
                    app.player_y_abs -= 1
                else:
                    break
        if pyxel.btn(pyxel.KEY_DOWN) and yp_r<=app.height-self.height:
            self.direction = "down"
            for i in range(self.speed):
                if not self.next_dest_is_obstacle(app, 0, 1):
                    app.player_y_abs += 1
                else:
                    break
        if pyxel.btn(pyxel.KEY_LEFT) and xp_r>=0:
            self.direction = "left"
            for i in range(self.speed):
                if not self.next_dest_is_obstacle(app, -1, 0):
                    app.player_x_abs -= 1
                else:
                    break
        if pyxel.btn(pyxel.KEY_RIGHT) and xp_r<=app.width-self.width: 
            self.direction = "right"
            for i in range(self.speed):
                if not self.next_dest_is_obstacle(app, 1, 0):
                    app.player_x_abs += 1
                else:
                    break

    def check_key(self, app):
        if pyxel.btnp(pyxel.KEY_SPACE):
            if app.timestop == False:
                app.timestop = True
            else:
                app.timestop = False
                app.recentrer = True
        if pyxel.btnp(pyxel.KEY_R):
            print(app.obstacle)

    def collision_rect(self, x1, y1, w1, h1, x2, y2, w2, h2):
        return (x1 < x2 + w2 and
                x1 + w1 > x2 and
                y1 < y2 + h2 and
                y1 + h1 > y2)
    def next_dest_is_obstacle(self, app, dx, dy):
        next_x = app.player_x_abs - self.width//2 + dx
        next_y = app.player_y_abs - self.height//2 + dy
        for obs in app.obstacle:
            if self.collision_rect(next_x, next_y, self.width, self.height, obs[0]*8, obs[1]*8, 8, 8):
                return True
        return False
    
    def draw(self, app):
        #coordonnées du joueur relatif à l'écran
        pyxel.colors[:] = [
            0x0D0D0D, 0x1D2B53, 0x7E2553, 0x008751,
            0xAB5236, 0x5F574F, 0xC2C3C7, 0xFFF1E8,
            0xFF004D, 0xFFA300, 0xFFEC27, 0x00E436,
            0x29ADFF, 0x83769C, 0xFF77A8, 0xFFCCAA
        ]
        player_screen_x = app.screen_center_x + (app.player_x_abs - app.x_center) - self.width//2
        player_screen_y = app.screen_center_y + (app.player_y_abs - app.y_center) - self.height//2
        animation_frame = (pyxel.frame_count // 10) % 8
        if self.direction == "up":
            pyxel.blt(player_screen_x, player_screen_y, 0, 24 * animation_frame, 120, 23, 39, 11)
        elif self.direction == "down":
            pyxel.blt(player_screen_x, player_screen_y, 0, 24 * animation_frame, 0, 23, 39, 11)
        elif self.direction == "left":
            pyxel.blt(player_screen_x, player_screen_y, 0, 24 * animation_frame, 40, 23, 39, 11)
        elif self.direction == "right":
            pyxel.blt(player_screen_x, player_screen_y, 0, 24 * animation_frame, 80, 23, 39, 11)