import pyxel

class Player:

    def __init__(self):
        self.speed = 2*pyxel.sqrt(2)
        self.width = 19
        self.height = 34
        self.direction = "down"
        self.run = False
        self.en_attaque = 0
        self.next_anim_attaque = 0
        
        self.base_damage = 10
        self.base_health = 100
        self.health = self.base_health
        self.base_defense = 0
        self.base_critical_chance = 0.1
        self.base_critical_multiplier = 1.5
        self.base_attack_speed = 1
        self.level = 1
        self.colkey = 5
        self.experience = 0
        self.experience_to_next_level = 40
        self.s_dmg = 0
        self.level = 1

    def deplace(self, app):
        #coordonnées du joueur relatif à l'écran
        temp_speed = int(self.speed + 1)
        xp_r = app.screen_center_x + (app.player_x_abs - app.x_center) - self.width//2
        yp_r = app.screen_center_y + (app.player_y_abs - app.y_center) - self.height//2
        self.run = False
        player_y_abs = player_x_abs = 0
        if (pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_Z)) and yp_r >= 0:
            self.direction = "up"
            self.run = True
            for i in range(temp_speed):
                # On teste uniquement l'axe Y pour permettre de glisser sur les murs verticaux
                if not self.next_dest_is_blocked(app, 0, player_y_abs - 1):
                    player_y_abs -= 1
                else:
                    self.open_colliding_chest(app, 0, player_y_abs - 1)
                    break
        if (pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S)) and yp_r <= app.height - self.height:
            self.direction = "down"
            self.run = True
            for i in range(temp_speed):
                if not self.next_dest_is_blocked(app, 0, player_y_abs + 1):
                    player_y_abs += 1
                else:
                    self.open_colliding_chest(app, 0, player_y_abs + 1)
                    break
        if (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_Q)) and xp_r >= 0:
            self.direction = "left"
            self.run = True
            for i in range(temp_speed):
                # On teste uniquement l'axe X pour glisser sur les murs horizontaux
                if not self.next_dest_is_blocked(app, player_x_abs - 1, 0):
                    player_x_abs -= 1
                else:
                    self.open_colliding_chest(app, player_x_abs - 1, 0)
                    break
        if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D)) and xp_r <= app.width - self.width:
            self.direction = "right"
            self.run = True
            for i in range(temp_speed):
                if not self.next_dest_is_blocked(app, player_x_abs + 1, 0):
                    player_x_abs += 1
                else:
                    self.open_colliding_chest(app, player_x_abs + 1, 0)
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
            if app.timestop:
                app.timestop = False
                app.recentrer = True
                app.timestop_cooldown = app.TIMESTOP_COOLDOWN
            elif app.timestop_cooldown == 0:
                app.timestop = True
                app.timestop_timer = app.TIMESTOP_DURATION
        if pyxel.btnp(pyxel.KEY_R):
            print(app.inventory.récuperer_case_souris())
        if pyxel.btnp(pyxel.KEY_I):
            app.inventory.open(app)
        if app.inventory.on_screen and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            app.inventory.drag_item(app)
        if pyxel.btnp(pyxel.KEY_DELETE):
            app.inventory.supprimer_item()

    def collision_rect(self, x1, y1, w1, h1, x2, y2, w2, h2):
        return (x1 < x2 + w2 and
                x1 + w1 > x2 and
                y1 < y2 + h2 and
                y1 + h1 > y2)
    
    def take_damage(self, app, n):
        if app.i_frames==0:
            print('AIE')
            defense = self.get_current_defense(app)
            actual_damage = max(1, n - defense)  # minimum 1 damage
            self.s_dmg=0.1
            self.health=max(0,self.health-actual_damage)
            app.i_frames = app.invincible_timer
        
    def regen(self, app, n):
        self.health=min(self.get_max_health(app), self.health+n)

    def get_max_health(self, app):
        bonus_health = 0
        if app.inventory.items["armure"] is not None:
            bonus_health = app.inventory.items["armure"].liste_attributs.get("bonus_health", 0)
        return self.base_health + bonus_health

    def update_health_to_max(self, app):
        self.health = min(self.health, self.get_max_health(app))

    def get_current_defense(self, app):
        defense = self.base_defense
        if app.inventory.items["armure"] is not None:
            defense += app.inventory.items["armure"].liste_attributs.get("defense", 0)
        return defense

    def is_dead(self):
        return self.health==0

    def next_dest_is_obstacle(self, app, dx, dy):
        next_x = app.player_x_abs - self.width//2 + dx
        next_y = app.player_y_abs  + dy
        for obs in app.obstacle:
            if self.collision_rect(next_x, next_y, self.width, self.height//2, obs[0]*8, obs[1]*8, 8, 8):
                return True
        return False

    def next_dest_is_blocked(self, app, dx, dy):
        return self.next_dest_is_obstacle(app, dx, dy) or self.next_dest_is_chest(app, dx, dy)

    def open_colliding_chest(self, app, dx, dy):
        next_x = app.player_x_abs - self.width//2 + dx
        next_y = app.player_y_abs + dy
        for c in app.coffres:
            if not c.ouvert and self.collision_rect(next_x, next_y, self.width, self.height//2, c.x, c.y, c.width, c.height):
                print(c.ouvrir())
                return
        
    def next_dest_is_chest(self, app, dx, dy):
        next_x = app.player_x_abs - self.width//2 + dx
        next_y = app.player_y_abs  + dy
        for c in app.coffres:
            if self.collision_rect(next_x, next_y, self.width, self.height//2, c.x, c.y, c.width, c.height):
                return True
        return False

    def level_up(self, app):
        if self.experience >= self.experience_to_next_level:
            self.level += 1
            self.experience -= self.experience_to_next_level
            self.experience_to_next_level = int(self.experience_to_next_level * 1.3)
            self.base_health += 20
            self.health = self.base_health
            self.base_damage += 5
            self.base_defense += 2
            self.base_critical_chance += 0.05
            self.base_critical_multiplier += 0.2
    def draw(self, app):
        #coordonnées du joueur relatif à l'écran
        self.player_screen_x = app.screen_center_x + (app.player_x_abs - app.x_center) - self.width//2
        self.player_screen_y = app.screen_center_y + (app.player_y_abs - app.y_center) - self.height//2
        idle_animation_frame = (pyxel.frame_count // 10) % 8
        run_animation_frame = (pyxel.frame_count // 5) % 8
        if self.en_attaque > 0:
            self.next_anim_attaque -= 1
            if self.next_anim_attaque <= 0:
                self.next_anim_attaque = 3
                self.en_attaque -= 1
        attack_animation_frame = 8 - self.en_attaque
        
        if self.run:
            pyxel.images[0].load(0, 0, "../Textures/Perso/run.png")
        elif self.en_attaque > 0 and self.direction in ["down", "left"]:
            pyxel.images[0].load(0, 0, "../Textures/Perso/attack 2 down and left.png")
        elif self.en_attaque > 0 and self.direction in ["right", "up"]:
            pyxel.images[0].load(0, 0, "../Textures/Perso/attack 2 right and up.png")
        else:
            pyxel.images[0].load(0, 0, "../Textures/Perso/idle.png")
        if self.direction == "up":
            if self.run:
                pyxel.blt(self.player_screen_x, self.player_screen_y, 0, 24 * run_animation_frame, 96, 23, 31, self.colkey)
            elif self.en_attaque > 0:
                pyxel.blt(self.player_screen_x - 17, self.player_screen_y - 4, 0, 56 * (attack_animation_frame % 4), 80 + (40 * (attack_animation_frame // 4)), 56, 40, self.colkey)
            else:
                pyxel.blt(self.player_screen_x, self.player_screen_y, 0, 24 * idle_animation_frame, 120, 23, 39, self.colkey)
        elif self.direction == "down":
            if self.run:
                pyxel.blt(self.player_screen_x, self.player_screen_y, 0, 24 * run_animation_frame, 0, 23, 31, self.colkey)
            elif self.en_attaque > 0:
                pyxel.blt(self.player_screen_x - 16, self.player_screen_y, 0, 56 * (attack_animation_frame % 4), 0 + (48 * (attack_animation_frame // 4)), 56, 48, self.colkey)
            else:
                pyxel.blt(self.player_screen_x, self.player_screen_y, 0, 24 * idle_animation_frame, 0, 23, 39, self.colkey)
        elif self.direction == "left":
            if self.run:
                pyxel.blt(self.player_screen_x, self.player_screen_y, 0, 24 * run_animation_frame, 32, 23, 31, self.colkey)
            elif self.en_attaque > 0:
                pyxel.blt(self.player_screen_x - 20, self.player_screen_y, 0, 64 * (attack_animation_frame % 4), 96 + (32 * (attack_animation_frame // 4)), 64, 32, self.colkey)
            else:
                pyxel.blt(self.player_screen_x, self.player_screen_y, 0, 24 * idle_animation_frame, 40, 23, 39, self.colkey)
        elif self.direction == "right":
            if self.run:
                pyxel.blt(self.player_screen_x, self.player_screen_y, 0, 24 * run_animation_frame, 64, 23, 31, self.colkey)
            elif self.en_attaque > 0:
                pyxel.blt(self.player_screen_x - 14, self.player_screen_y, 0, 56 * (attack_animation_frame % 4), 0 + (40 * (attack_animation_frame // 4)), 56, 40, self.colkey)
            else:
                pyxel.blt(self.player_screen_x, self.player_screen_y, 0, 24 * idle_animation_frame, 80, 23, 39, self.colkey)
    
    def show_dmg(self,app):
        if self.s_dmg>0:
            for i in range(int(25-self.health/5)):
                pyxel.rectb(i,i,app.width-i*2,app.height-i*2,8)
            if pyxel.frame_count%6==0:
                self.s_dmg = max(0,self.s_dmg-0.1)