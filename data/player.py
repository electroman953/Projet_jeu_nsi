import pyxel

class Player:

    def __init__(self):
        self.speed = 2*pyxel.sqrt(2)
        self.width = 19
        self.height = 34
        self.direction = "down"
        self.run = False

    def deplace(self, app):
        #coordonnées du joueur relatif à l'écran
        temp_speed = int(self.speed + 1)
        xp_r = app.screen_center_x + (app.player_x_abs - app.x_center) - self.width//2
        yp_r = app.screen_center_y + (app.player_y_abs - app.y_center) - self.height//2
        self.run = False
        player_y_abs = player_x_abs = 0
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_Z) and yp_r >= 0:
            self.direction = "up"
            self.run = True
            for i in range(temp_speed):
                if not self.next_dest_is_obstacle(app, 0, -1):
                    player_y_abs -= 1
                else:
                    break
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S) and yp_r<=app.height-self.height:
            self.direction = "down"
            self.run = True
            for i in range(temp_speed):
                if not self.next_dest_is_obstacle(app, 0, 1):
                    player_y_abs += 1
                else:
                    break
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_Q) and xp_r>=0:
            self.direction = "left"
            self.run = True
            for i in range(temp_speed):
                if not self.next_dest_is_obstacle(app, -1, 0):
                    player_x_abs -= 1
                else:
                    break
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D) and xp_r<=app.width-self.width:
            self.direction = "right"
            self.run = True
            for i in range(temp_speed):
                if not self.next_dest_is_obstacle(app, 1, 0):
                    player_x_abs += 1
                else:
                    break
        if player_x_abs == temp_speed:
            player_x_abs = self.speed
        if player_x_abs == -temp_speed:
            player_x_abs = -self.speed
        if player_y_abs == temp_speed:
            player_y_abs = self.speed
        if player_y_abs == -temp_speed:
            player_y_abs = -self.speed
        if player_x_abs != 0 and player_y_abs != 0:
            player_x_abs/=pyxel.sqrt(2)
            player_y_abs/=pyxel.sqrt(2)
        
        app.player_x_abs += player_x_abs
        app.player_y_abs += player_y_abs
        hw = self.width // 2
        hh = self.height // 2
        app.player_x_abs = max(hw, min(app.player_x_abs, app.world.word_width - hw))
        app.player_y_abs = max(hh, min(app.player_y_abs, app.world.word_height - hh))

    def check_key(self, app):
        if pyxel.btnp(pyxel.KEY_SPACE):
            if app.timestop == False:
                app.timestop = True
            else:
                app.timestop = False
                app.recentrer = True
        if pyxel.btnp(pyxel.KEY_R):
            print(app.inventory.récuperer_case_souris())
        if pyxel.btnp(pyxel.KEY_I):
            app.inventory.open()
        if app.inventory.on_screen and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            app.inventory.drag_item(app)

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
        player_screen_x = app.screen_center_x + (app.player_x_abs - app.x_center) - self.width//2
        player_screen_y = app.screen_center_y + (app.player_y_abs - app.y_center) - self.height//2
        idle_animation_frame = (pyxel.frame_count // 10) % 8
        run_animation_frame = (pyxel.frame_count // 5) % 8
        if self.run:
            pyxel.images[0].load(0, 0, "../Textures/Perso/run.png")
        else:
            pyxel.images[0].load(0, 0, "../Textures/Perso/idle.png")
        if self.direction == "up":
            if self.run:
                pyxel.blt(player_screen_x, player_screen_y, 0, 24 * run_animation_frame, 96, 23, 31, 3)
            else:
                pyxel.blt(player_screen_x, player_screen_y, 0, 24 * idle_animation_frame, 120, 23, 39, 3)
        elif self.direction == "down":
            if self.run:
                pyxel.blt(player_screen_x, player_screen_y, 0, 24 * run_animation_frame, 0, 23, 31, 3)
            else:
                pyxel.blt(player_screen_x, player_screen_y, 0, 24 * idle_animation_frame, 0, 23, 39, 3)
        elif self.direction == "left":
            if self.run:
                pyxel.blt(player_screen_x, player_screen_y, 0, 24 * run_animation_frame, 32, 23, 31, 3)
            else:
                pyxel.blt(player_screen_x, player_screen_y, 0, 24 * idle_animation_frame, 40, 23, 39, 3)
        elif self.direction == "right":
            if self.run:
                pyxel.blt(player_screen_x, player_screen_y, 0, 24 * run_animation_frame, 64, 23, 31, 3)
            else:
                pyxel.blt(player_screen_x, player_screen_y, 0, 24 * idle_animation_frame, 80, 23, 39, 3)