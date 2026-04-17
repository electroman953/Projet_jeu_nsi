import pyxel

class Mob:
    # Initialise un ennemi avec ses stats, sa position et sa table de loot.
    # spawn_zone permet de savoir à quelle zone appartient ce mob pour le respawn.
    def __init__(self, health, damage, type, x, y, w, h, c, xp_drop_range, loot_table=None, texture=(0,0), spawn_zone=None):
        self.health = health
        self.damage = damage
        self.type = type
        self.x = x
        self.y = y
        self.width = w
        self.spawn_zone = spawn_zone
        self.height = h
        self.color = c
        self.vitesse = 1
        self.chemin  = []
        self.timer = pyxel.rndi(0, 29)
        self.knockback_vx = 0
        self.knockback_vy = 0
        self.direction='down'
        self.texture=texture
        self.passive = True
        self.xp_drop_range = xp_drop_range
        self.loot_table = loot_table if loot_table is not None else []
        self.timer = 0
        self.detection_range = 200

    # Affiche le mob à l'écran. La salamandre a une gestion de frames spéciale
    # car ses animations sont organisées différemment dans la spritesheet.
    def draw(self, app):
        self.screen_x = app.screen_center_x + (self.x - app.x_center) - self.width // 2
        self.screen_y = app.screen_center_y + (self.y - app.y_center) - self.height // 2
        #scale sert à modifier la taille pour le boss de sorte à ce qu'il soit deux fois plus grand que les autres mobs.
        scale=1
        if self.type == "salamandre":
            # Chaque direction a ses propres coordonnées de frames dans la spritesheet
            s={'down':[(192,0),(192,127),(224,126)],'left':[(192,30),(192,159),(224,158)],'right':[(192,64),(192,189),(224,191)], 'up':[(192,96),(192,224),(224,223)]}[self.direction]
            frame = pyxel.frame_count // 10 % 3 if not app.timestop and not self.passive else 0
            u,v=s[frame][0],s[frame][1]
        elif self.type == "boss":
            s={'down':[(192,0),(192,127),(224,126)],'left':[(192,30),(192,159),(224,158)],'right':[(192,64),(192,189),(224,191)], 'up':[(192,96),(192,224),(224,223)]}[self.direction]
            frame = pyxel.frame_count // 10 % 3 if not app.timestop and not self.passive else 0
            u,v=s[frame][0],s[frame][1]
            scale=3
        else:
            dir_index = {'down': 0, 'left': 1, 'right': 2, 'up': 3}[self.direction]
            frame = pyxel.frame_count // 10 % 3 if not app.timestop and not self.passive else 0
            u = self.texture[0] + 32 * frame
            v = self.texture[1] + 32 * dir_index

        pyxel.blt(self.screen_x, self.screen_y, 2, u, v, self.width, self.height, colkey=8, scale=scale)

    # Gère tous les déplacements du mob à chaque frame : knockback, détection du joueur,
    # recalcul du chemin BFS et suivi case par case.
    def move(self, app, player_x, player_y):
        if self.health <= 0:
            return
        if app.timestop:
            return
        if app.inventory.on_screen:
            return
            
        # Si le mob est en knockback, on le déplace selon sa vélocité résiduelle
        # puis on atténue progressivement cette vélocité (facteur 0.8 à chaque frame).
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

        # Si le joueur est trop loin, le mob repasse en mode passif et arrête de bouger.
        if abs(self.x - player_x) + abs(self.y - player_y) > self.detection_range:
            self.passive = True
            self.direction = "down"
            return

        # Toutes les 30 frames, on recalcule le chemin BFS vers le joueur.
        # Ce délai évite de recalculer à chaque frame, ce qui serait trop coûteux.
        self.timer += 1
        if self.timer % 30 == 0:
            self.timer = 0
            debut = (self.x//8, self.y//8)
            fin = (player_x//8, player_y//8)
            self.chemin = app.world.parcours_largeur(debut, fin, app, self)

        if self.chemin:
            self.passive = False
            next_cell = self.chemin[0]
            next_x = next_cell[0] * 8 + 4
            next_y = next_cell[1] * 8 + 4
            dx = next_x - self.x
            dy = next_y - self.y
            # On plafonne le déplacement à la vitesse du mob pour éviter les sauts brusques.
            if abs(dx) > self.vitesse:
                dx = self.vitesse if dx > 0 else -self.vitesse
            if abs(dy) > self.vitesse:
                dy = self.vitesse if dy > 0 else -self.vitesse
            if abs(dx) >= abs(dy):
                self.direction = "right" if dx > 0 else "left"
            else:
                self.direction = "down" if dy > 0 else "up"
                        
            if dx != 0 or dy != 0:
                hit_player = self.next_dest_is_player(app, dx, dy)
                if hit_player:
                    app.player.take_damage(app, self.damage)
                elif not self.next_dest_is_blocked(app, dx, dy):
                    self.x += dx
                    self.y += dy
                else:
                    # Si le déplacement diagonal est bloqué, on essaie chaque axe séparément.
                    # Cela permet au mob de longer les murs sans se bloquer.
                    if dx != 0:
                        if self.next_dest_is_player(app, dx, 0):
                            hit_player = True
                        elif not self.next_dest_is_blocked(app, dx, 0):
                            self.x += dx
                    if dy != 0:
                        if self.next_dest_is_player(app, 0, dy):
                            hit_player = True
                        elif not self.next_dest_is_blocked(app, 0, dy):
                            self.y += dy
                    if hit_player:
                        app.player.take_damage(app, self.damage)

            # On retire la cellule courante du chemin quand le mob est assez proche d'elle.
            if abs(self.x - next_x) <= self.vitesse and abs(self.y - next_y) <= self.vitesse:
                self.chemin.pop(0)
        else:
            self.passive = True
            self.direction = "down"

    # Détecte si deux rectangles (définis par position + dimensions) se chevauchent.
    # Utilisé pour toutes les collisions du mob : joueur, obstacles, coffres.
    def collision_rect(self, x1, y1, w1, h1, x2, y2, w2, h2):
        return (x1 < x2 + w2 and
                x1 + w1 > x2 and
                y1 < y2 + h2 and
                y1 + h1 > y2)

    # Inflige des dégâts au mob et bloque ses PV à 0 minimum.
    def prendre_degats(self, damage):
        print(f"Mob took {damage} damage")
        self.health -= damage
        if self.health <= 0:
            self.health = 0

    # Calcule et applique une impulsion de knockback depuis une source (ex: projectile ou slash).
    # La direction est normalisée, la force détermine la vélocité initiale.
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

    # Vérifie si le mob est mort (0 PV). Si oui, distribue l'XP et le loot,
    # puis supprime le mob de la liste. Renvoie implicitement None.
    def is_dead(self, app):
        if self.health == 0:
            if self.type == "boss":
                app.game_won = True
                
            xp_drop = pyxel.rndi(self.xp_drop_range[0], self.xp_drop_range[1])
            app.player.experience += xp_drop
            print(app.player.experience)
            # Pour chaque item possible dans la table de loot, on tire un nombre aléatoire
            # entre 0 et 1 ; si c'est inférieur à drop_chance, l'item est ajouté à l'inventaire.
            for item in self.loot_table:
                if pyxel.rndf(0, 1) < item["drop_chance"]:
                    app.inventory.add_item(item["item"])
            app.mobs.remove(self)

    # Vérifie si la prochaine position du mob (après déplacement dx, dy) chevauche le joueur.
    # Reçoit les deltas de déplacement, renvoie True si collision avec le joueur.
    def next_dest_is_player(self, app, dx, dy):
        next_x = self.x - self.width // 2 + dx
        next_y = self.y - self.height // 2 + dy
        player_x = app.player_x_abs - app.player.width // 2
        player_y = app.player_y_abs - app.player.height // 2
        if self.collision_rect(next_x, next_y, self.width, self.height,
                                player_x, player_y, app.player.width, app.player.height):
            return True
        return False

    # Vérifie si la prochaine position du mob heurte une tuile obstacle.
    # Les obstacles sont stockés en coordonnées de cases (col, row), multipliées par 8 pour pixel.
    def next_dest_is_obstacle(self, app, dx, dy):
        next_x = self.x - self.width//2 + dx
        next_y = self.y - self.height//2 + dy
        for obs in app.obstacle:
            if self.collision_rect(next_x, next_y, self.width, self.height, obs[0]*8, obs[1]*8, 8, 8):
                return True
        return False

    # Renvoie True si la prochaine destination est bloquée, que ce soit par un obstacle ou un coffre.
    def next_dest_is_blocked(self, app, dx, dy):
        return self.next_dest_is_obstacle(app, dx, dy) or self.next_dest_is_chest(app, dx, dy)
    
    # Vérifie si la prochaine position du mob entre en collision avec un coffre.
    def next_dest_is_chest(self, app, dx, dy):
        next_x = self.x - self.width // 2 + dx
        next_y = self.y - self.height // 2 + dy
        for c in app.coffres:
            if self.collision_rect(next_x, next_y, self.width, self.height, c.x, c.y, c.width, c.height):
                return True
        return False
