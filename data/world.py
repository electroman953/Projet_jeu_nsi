import pyxel

class World:
    # Gère la carte du monde : dimensions, tilemap et déplacements de la caméra.
    # "tm" est l'index de la tilemap Pyxel à utiliser pour le rendu.
    def __init__(self, width, height, tm):
        self.width = width
        self.height = height
        self.tm = tm
        self.word_width = 2048
        self.word_height = 2048

    # Affiche la portion de la carte visible à l'écran, centrée sur la position du joueur.
    # u et v sont les coordonnées dans la tilemap à partir desquelles on commence à lire.
    def place_map(self, x_player, y_player, app):
        u = x_player - self.width // 2
        v = y_player - self.height // 2
        pyxel.bltm(0, 0, self.tm, u, v, self.width, self.height)

    # Déplace le joueur et recalcule le centre de la caméra (x_center, y_center).
    # En mode normal (pas timestop), c'est cette méthode qui gère le mouvement — la caméra suit le joueur en temps réel.
    # La vitesse diagonale est divisée par √2 pour éviter que le joueur aille plus vite en diagonale.
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

        # Correction de la vitesse : si on a atteint la vitesse max entière, on repasse à la vraie vitesse (flottante).
        if dx == speed:
            dx = real_speed
        if dx == -speed:
            dx = -real_speed
        if dy == speed:
            dy = real_speed
        if dy == -speed:
            dy = -real_speed

        # Normalisation diagonale : diviser par √2 pour garder une vitesse constante dans toutes les directions.
        if dx != 0 and dy != 0:
            dx/=pyxel.sqrt(2)
            dy/=pyxel.sqrt(2)

        # Mise à jour de la position absolue du joueur, clampée dans les limites du monde.
        # x_center et y_center suivent le joueur mais sont aussi clampés pour ne pas dépasser les bords de la carte.
        app.player_x_abs = max(app.player.width // 2, min(app.player_x_abs + dx, self.word_width - app.player.width // 2))
        app.player_y_abs = max(app.player.height // 2, min(app.player_y_abs + dy, self.word_height - app.player.height // 2))
        app.x_center = int(max(app.width // 2, min(app.player_x_abs, self.word_width - app.width // 2)))
        app.y_center = int(max(app.height // 2, min(app.player_y_abs, self.word_height - app.height // 2)))

    # Anime le recentrage de la caméra sur le joueur après la fin du timestop.
    # La caméra se déplace progressivement vers sa cible plutôt que de sauter instantanément.
    def recentrer(self, app, speed = 5):
        if not app.recentrer:
            return

        target_x = int(max(app.width // 2, min(app.player_x_abs, self.word_width - app.width // 2)))
        target_y = int(max(app.height // 2, min(app.player_y_abs, self.word_height - app.height // 2)))

        diff_x = target_x - app.x_center
        diff_y = target_y - app.y_center

        # Avance d'un pas vers la cible, ou se cale exactement dessus si on est assez proche.
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

    # Algorithme de pathfinding (BFS = recherche en largeur) : trouve le chemin le plus court
    # entre deux cases de la grille, en évitant les obstacles.
    # Reçoit les coordonnées de départ et d'arrivée en cases (divisées par 8), renvoie une liste de cases à parcourir.
    def parcours_largeur(self, debut, fin, app, mob=None):
        obstacles = [(i, j) for i, j in app.obstacle]

        # Si un mob est fourni, on élargit la zone d'obstacle autour de chaque tuile bloquée
        # pour que le mob évite les murs même avec sa taille (hitbox plus grande qu'une case).
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

            # Sécurité : si trop de cases explorées, on arrête pour ne pas bloquer le jeu.
            if len(viens_de) > 40000:
                return []

            # On a atteint la destination : on reconstruit le chemin en remontant les parents.
            if actuel == fin:
                chemin = []
                while actuel is not None:
                    chemin.append(actuel)
                    actuel = viens_de[actuel]
                chemin = chemin[::-1]
                return chemin[1:]

            # On explore les 8 voisins (4 directions + 4 diagonales).
            for dx, dy in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]:
                voisin = (actuel[0] + dx, actuel[1] + dy)

                # Ignorer les cases hors des limites de la carte.
                if not (0 <= voisin[0] < self.word_width // 8 and 0 <= voisin[1] < self.word_height // 8):
                    continue

                # En diagonale, vérifier que les deux cases adjacentes ne sont pas des murs
                # pour éviter de "couper les coins" à travers un obstacle.
                if dx != 0 and dy != 0:
                    if (actuel[0] + dx, actuel[1]) in expanded_obstacles or (actuel[0], actuel[1] + dy) in expanded_obstacles:
                        continue

                # Ignorer les cases déjà visitées ou bloquées, sauf si c'est la destination.
                if voisin != fin and (voisin in expanded_obstacles or voisin in viens_de):
                    continue
                if voisin == fin and voisin in viens_de:
                    continue

                viens_de[voisin] = actuel
                queue.append(voisin)

        return []