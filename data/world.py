import pyxel

class World:
    
    def __init__(self, width, height, tm):
        self.width = width
        self.height = height
        self.tm = tm
        self.word_width = 2048
        self.word_height = 2048
    def place_map(self, x_player, y_player, app):

        u = x_player - self.width // 2
        v = y_player - self.height // 2
        pyxel.bltm(0, 0, self.tm, u, v, self.width, self.height)

    def deplace(self, app, speed=1):
        dx, dy = 0, 0
        real_speed = speed
        speed = int(speed+1)
        app.player.run = False
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            app.player.direction = "right"
            app.player.run = True
            for _ in range(speed):
                if not app.player.next_dest_is_blocked(app, dx + 1, dy):
                    dx += 1
                else:
                    app.player.open_colliding_chest(app, dx + 1, dy)
                    break
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_Q):
            app.player.direction = "left"
            app.player.run = True
            for _ in range(speed):
                if not app.player.next_dest_is_blocked(app, dx - 1, dy):
                    dx -= 1
                else:
                    app.player.open_colliding_chest(app, dx - 1, dy)
                    break
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_Z):
            app.player.direction = "up"
            app.player.run = True
            for _ in range(speed):
                if not app.player.next_dest_is_blocked(app, dx, dy - 1):
                    dy -= 1
                else:
                    app.player.open_colliding_chest(app, dx, dy - 1)
                    break
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            app.player.direction = "down"
            app.player.run = True
            for _ in range(speed):
                if not app.player.next_dest_is_blocked(app, dx, dy + 1):
                    dy += 1
                else:
                    app.player.open_colliding_chest(app, dx, dy + 1)
                    break
        if dx == speed:
            dx = real_speed
        if dx == -speed:
            dx = -real_speed
        if dy == speed:
            dy = real_speed
        if dy == -speed:
            dy = -real_speed
        if dx != 0 and dy != 0:
            dx/=pyxel.sqrt(2)
            dy/=pyxel.sqrt(2)
        
            

        app.player_x_abs = max(app.player.width // 2, min(app.player_x_abs + dx, self.word_width - app.player.width // 2))
        app.player_y_abs = max(app.player.height // 2, min(app.player_y_abs + dy, self.word_height - app.player.height // 2))
        app.x_center = int(max(app.width // 2, min(app.player_x_abs, self.word_width - app.width // 2)))
        app.y_center = int(max(app.height // 2, min(app.player_y_abs, self.word_height - app.height // 2)))

    def recentrer(self, app, speed = 5):
        if not app.recentrer:
            return

        target_x = int(max(app.width // 2, min(app.player_x_abs, self.word_width - app.width // 2)))
        target_y = int(max(app.height // 2, min(app.player_y_abs, self.word_height - app.height // 2)))

        diff_x = target_x - app.x_center
        diff_y = target_y - app.y_center

        if abs(diff_x) <= speed:
            app.x_center = target_x
        else:
            app.x_center += speed if diff_x > 0 else -speed

        if abs(diff_y) <= speed:
            app.y_center = target_y
        else:
            app.y_center += speed if diff_y > 0 else -speed

        if app.x_center == target_x and app.y_center == target_y:
            app.recentrer = False
    def parcours_largeur(self, debut, fin, app, mob=None):
        obstacles = [(i, j) for i, j in app.obstacle]
        # Ajouter une zone de sécurité dynamique si un mob est fourni, sinon on utilise les obstacles normaux
        expanded_obstacles = set(obstacles)
        if mob:
            largeur_cases = (mob.width // 8) // 2
            hauteur_cases = (mob.height // 8) // 2
            if largeur_cases > 0 or hauteur_cases > 0:
                for obs in obstacles:
                    for dx in range(-largeur_cases, largeur_cases + 1):
                        for dy in range(-hauteur_cases, hauteur_cases + 1):
                            expanded_obstacles.add((obs[0]+dx, obs[1]+dy))
        else:
            expanded_obstacles = set(obstacles)

        queue = [debut]
        viens_de = {debut: None}
        while queue:
            actuel = queue.pop(0)
            
            # Limiter le nombre de cases explorées pour éviter les crashs / boucles infinies
            if len(viens_de) > 40000:
                return []
                
            if actuel == fin:
                chemin = []
                while actuel is not None:
                    chemin.append(actuel)
                    actuel = viens_de[actuel]
                chemin = chemin[::-1]
                return chemin[1:]
            for dx, dy in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]:
                voisin = (actuel[0] + dx, actuel[1] + dy)
                # Corriger les limites de la carte pour qu'elles soient en cases (divisées par 8)
                if not (0 <= voisin[0] < self.word_width // 8 and 0 <= voisin[1] < self.word_height // 8):
                    continue
                if dx != 0 and dy != 0:
                    if (actuel[0] + dx, actuel[1]) in expanded_obstacles or (actuel[0], actuel[1] + dy) in expanded_obstacles:
                        continue
                # Autoriser la fin même si elle est dans un obstacle "étendu" pour éviter de ne pas trouver de chemin
                if voisin != fin and (voisin in expanded_obstacles or voisin in viens_de):  
                    continue
                if voisin == fin and voisin in viens_de:
                    continue
                viens_de[voisin] = actuel
                queue.append(voisin)

        return []
