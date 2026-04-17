import pyxel

class Player:
    # Initialise toutes les stats de base du joueur : vitesse, dimensions, PV, dégâts, critique, niveau, XP.
    def __init__(self):
        self.speed = 2*pyxel.sqrt(2)
        self.base_speed = self.speed
        self.speed_bonus = 0
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

    # Gère le déplacement du joueur en mode timestop (caméra fixe, joueur bouge librement).
    # Pour chaque direction, on avance pixel par pixel jusqu'à la vitesse max ou jusqu'à un obstacle.
    # La vitesse diagonale est divisée par √2 pour rester cohérente avec le déplacement normal.
    def deplace(self, app):
        temp_speed = int(self.speed + 1)
        xp_r = app.screen_center_x + (app.player_x_abs - app.x_center) - self.width//2
        yp_r = app.screen_center_y + (app.player_y_abs - app.y_center) - self.height//2
        self.run = False
        player_y_abs = player_x_abs = 0
        if (pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_Z)) and yp_r >= 0:
            self.direction = "up"
            self.run = True
            for i in range(temp_speed):
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

        # Correction de la vitesse entière vers la vraie vitesse (flottante) après les boucles.
        if player_x_abs == temp_speed:
            player_x_abs = self.speed
        if player_x_abs == -temp_speed:
            player_x_abs = -self.speed
        if player_y_abs == temp_speed:
            player_y_abs = self.speed
        if player_y_abs == -temp_speed:
            player_y_abs = -self.speed

        # Normalisation diagonale : évite que la vitesse diagonale soit √2 fois plus rapide.
        if player_x_abs != 0 and player_y_abs != 0:
            player_x_abs/=pyxel.sqrt(2)
            player_y_abs/=pyxel.sqrt(2)
        
        app.player_x_abs += player_x_abs
        app.player_y_abs += player_y_abs

        # Clamp (limitation) pour que le joueur ne sorte pas des limites du monde.
        hw = self.width // 2
        hh = self.height // 2
        app.player_x_abs = max(hw, min(app.player_x_abs, app.world.word_width - hw))
        app.player_y_abs = max(hh, min(app.player_y_abs, app.world.word_height - hh))

    # Gère les touches clavier qui déclenchent des actions ponctuelles (pas de mouvement).
    # Timestop, ouverture inventaire, usage d'item, suppression, retour au menu…
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
        if app.inventory.on_screen and pyxel.btnp(pyxel.KEY_E):
            app.inventory.use_item(app)
        if pyxel.btnp(pyxel.KEY_DELETE):
            app.inventory.supprimer_item()
        if pyxel.btnp(pyxel.KEY_M):
            app.on_menu = True

    # Vérifie si deux rectangles se chevauchent. Même logique que dans Mob — dupliquée ici pour l'indépendance des classes.
    def collision_rect(self, x1, y1, w1, h1, x2, y2, w2, h2):
        return (x1 < x2 + w2 and
                x1 + w1 > x2 and
                y1 < y2 + h2 and
                y1 + h1 > y2)
    
    # Inflige des dégâts au joueur en tenant compte de sa défense, si les i_frames (frames d'invincibilité) sont épuisées.
    # Les i_frames empêchent de subir plusieurs hits à la suite immédiatement.
    def take_damage(self, app, n):
        if app.i_frames==0:
            print('AIE')
            defense = self.get_current_defense(app)
            actual_damage = max(1, n - defense)
            self.s_dmg=0.1
            self.health=max(0,self.health-actual_damage)
            app.i_frames = app.invincible_timer

    # Soigne le joueur du montant indiqué, sans dépasser ses PV maximum.
    def regen(self, app, n):
        self.health=min(self.get_max_health(app), self.health+n)

    # Renvoie les PV maximum du joueur, en ajoutant le bonus de PV de l'armure équipée si elle existe.
    def get_max_health(self, app):
        bonus_health = 0
        if app.inventory.items["armure"] is not None:
            bonus_health = app.inventory.items["armure"].liste_attributs.get("bonus_health", 0)
        return self.base_health + bonus_health

    # Met à jour les PV actuels pour qu'ils ne dépassent pas le nouveau maximum (utile après déséquipement d'armure).
    def update_health_to_max(self, app):
        self.health = min(self.health, self.get_max_health(app))

    # Renvoie la défense totale du joueur (base + bonus armure équipée).
    def get_current_defense(self, app):
        defense = self.base_defense
        if app.inventory.items["armure"] is not None:
            defense += app.inventory.items["armure"].liste_attributs.get("defense", 0)
        return defense

    # Renvoie True si le joueur n'a plus de PV. Déclenche l'écran de mort dans la boucle principale.
    def is_dead(self):
        return self.health==0

    # Vérifie si la prochaine position du joueur chevauche un obstacle de la tilemap.
    # Utilise seulement la moitié basse du sprite comme hitbox (plus naturel visuellement pour un perso vu de haut).
    def next_dest_is_obstacle(self, app, dx, dy):
        next_x = app.player_x_abs - self.width//2 + dx
        next_y = app.player_y_abs  + dy
        for obs in app.obstacle:
            if self.collision_rect(next_x, next_y, self.width, self.height//2, obs[0]*8, obs[1]*8, 8, 8):
                return True
        return False

    # Renvoie True si la destination est bloquée par un obstacle ou un coffre.
    def next_dest_is_blocked(self, app, dx, dy):
        return self.next_dest_is_obstacle(app, dx, dy) or self.next_dest_is_chest(app, dx, dy)

    # Si le joueur marche contre un coffre fermé, l'ouvre et ajoute l'item à l'inventaire.
    # Convertit l'item_id retourné par le coffre en vrai objet Item via app.build_item().
    def open_colliding_chest(self, app, dx, dy):
        next_x = app.player_x_abs - self.width//2 + dx
        next_y = app.player_y_abs + dy
        for c in app.coffres:
            if not c.ouvert and self.collision_rect(next_x, next_y, self.width, self.height//2, c.x, c.y, c.width, c.height):
                item_id = c.ouvrir()
                if item_id is not None:
                    item_obj = app.build_item(item_id)
                    if item_obj is not None:
                        app.inventory.add_item(item_obj)
                return
        
    # Vérifie si la prochaine position du joueur chevauche un coffre (ouvert ou fermé).
    def next_dest_is_chest(self, app, dx, dy):
        next_x = app.player_x_abs - self.width//2 + dx
        next_y = app.player_y_abs  + dy
        for c in app.coffres:
            if self.collision_rect(next_x, next_y, self.width, self.height//2, c.x, c.y, c.width, c.height):
                return True
        return False

    # Gère la montée de niveau : augmente les stats de base et réinitialise les PV au nouveau maximum.
    # Le seuil d'XP pour le prochain niveau augmente de 30% à chaque level.
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

    # Affiche le sprite du joueur à l'écran selon sa direction et son état (idle, course, attaque).
    # Charge dynamiquement la bonne feuille de sprites selon l'état pour économiser la mémoire vidéo.
    def draw(self, app):
        self.player_screen_x = app.screen_center_x + (app.player_x_abs - app.x_center) - self.width//2
        self.player_screen_y = app.screen_center_y + (app.player_y_abs - app.y_center) - self.height//2
        idle_animation_frame = (pyxel.frame_count // 10) % 8
        run_animation_frame = (pyxel.frame_count // 5) % 8

        # Décompte de l'animation d'attaque : en_attaque représente le nombre de frames restantes,
        # next_anim_attaque est un sous-compteur qui cadence le changement de frame.
        if self.en_attaque > 0:
            self.next_anim_attaque -= 1
            if self.next_anim_attaque <= 0:
                self.next_anim_attaque = 3
                self.en_attaque -= 1
        attack_animation_frame = 8 - self.en_attaque
        
        # Chargement de la bonne spritesheet selon l'état du joueur.
        if self.run:
            pyxel.images[0].load(0, 0, "../Textures/Perso/run.png")
        elif self.en_attaque > 0 and self.direction in ["down", "left"]:
            pyxel.images[0].load(0, 0, "../Textures/Perso/attack 2 down and left.png")
        elif self.en_attaque > 0 and self.direction in ["right", "up"]:
            pyxel.images[0].load(0, 0, "../Textures/Perso/attack 2 right and up.png")
        else:
            pyxel.images[0].load(0, 0, "../Textures/Perso/idle.png")

        # Sélection du bon sprite selon la direction, en découpant la spritesheet aux bonnes coordonnées.
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

    # Affiche un effet de bord rouge (vignette) quand le joueur vient de subir des dégâts.
    # Plus les PV sont bas, plus les bordures rouges sont épaisses. L'effet s'estompe progressivement.
    def show_dmg(self,app):
        if self.s_dmg>0:
            for i in range(int(25-self.health/5)):
                pyxel.rectb(i,i,app.width-i*2,app.height-i*2,8)
            if pyxel.frame_count%6==0:
                self.s_dmg = max(0,self.s_dmg-0.1)