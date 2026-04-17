import pyxel
from data.items import sword, bow, Armor, Weapon, Potion

class Inventory:
    # Initialise l'inventaire avec 24 cases numérotées et 2 slots d'équipement ("arme" et "armure").
    # Toutes les cases sont vides au départ (None).
    def __init__(self, app):
        self.items = {i : None for i in range(24)}
        self.items["arme"] = None
        self.items["armure"] = None
        self.on_screen = False
        self.dragging_item = None
        self.old_drag_case = None

    # Bascule l'affichage de l'inventaire. Active le curseur souris quand il est ouvert.
    # Si on ferme avec un item en cours de déplacement, il est replacé dans sa case d'origine.
    def open(self, app):
        self.on_screen = not self.on_screen
        pyxel.mouse(self.on_screen)
        if self.on_screen:
            self.items[self.old_drag_case] = self.dragging_item
            self.dragging_item = None

    # Dessine le panneau d'inventaire complet : fond, preview du personnage, slots d'équipement et grille.
    def afficher(self, app):
        if self.on_screen:
            px, py = 80, 40
            pyxel.rect(px, py, 320, 175, 1)
            pyxel.rectb(px, py, 320, 175, 6)

            # Aperçu du personnage à gauche du panneau.
            pyxel.rect(px+16, py+12, 48, 64, 5)
            pyxel.rectb(px+16, py+12, 48, 64, 6)
            pyxel.blt(px+28, py+20, 1, 70, 222, 23, 39, colkey=3) 

            # Deux slots d'équipement (arme et armure) sous l'aperçu.
            for i in range(2):
                sx = px + 10 + i * 40
                pyxel.rect(sx, py+88, 32, 32, 5)
                pyxel.rectb(sx, py+88, 32, 32, 6)

            pyxel.line(px+92, py+4, px+92, py+171, 13)

            # Grille de 4 lignes x 6 colonnes pour les items.
            pyxel.text(px+148, py+6, "INVENTAIRE", 7)
            for row in range(4):
                for col in range(6):
                    sx, sy = px+100 + col*36, py+16 + row*36
                    pyxel.rect(sx, sy, 32, 32, 5)
                    pyxel.rectb(sx, sy, 32, 32, 6)
            self.afficher_items()

    # Parcourt tous les items de l'inventaire et dessine leur sprite dans leur case respective.
    # Saute l'item actuellement en cours de déplacement (il sera dessiné séparément sous la souris).
    def afficher_items(self):
        if self.on_screen:
            px, py = 80, 40
            for idx, item in self.items.items():
                if item is None or (self.dragging_item is not None and idx == self.old_drag_case):
                    continue
                if idx is None:
                    continue
                if type(idx) == str:
                    sx = px + 10 if idx == "arme" else px + 50
                    sy = py + 88
                else:
                    sx = px + 100 + (idx % 6) * 36
                    sy = py + 16 + (idx // 6) * 36
                img_bank = getattr(item, 'image_bank', 0)
                pyxel.blt(sx, sy, img_bank, item.image_x, item.image_y, 32, 32, colkey=item.colkey)
            self.show_drag_item()

    # Renvoie l'identifiant de la case de l'inventaire sous le curseur souris, ou None si aucune.
    # Utilise un calcul de position pour retrouver la case de la grille à partir des coordonnées pixel de la souris.
    def récuperer_case_souris(self):
        if not self.on_screen:
            return None
        mx, my = pyxel.mouse_x, pyxel.mouse_y
        if 90 <= mx < 90 + 32 and 128 <= my < 128 + 32:
            return "arme"
        if 130 <= mx < 130 + 32 and 128 <= my < 128 + 32:
            return "armure"
        # Conversion pixel → indice de case en base 6 (6 colonnes dans la grille).
        return int(f"{(my - 56) // 36}{(mx - 180) // 36}", 6) if 180 <= mx < 180 + 6*36 and 56 <= my < 56 + 4*36 else None

    # Gère le déplacement d'un item par glisser-déposer (drag & drop).
    # Au premier clic : saisit l'item. Au second clic sur une case valide : le dépose.
    # Vérifie que le type d'item correspond au slot cible (arme → slot arme, armure → slot armure).
    def drag_item(self, app):
        case = self.récuperer_case_souris()
        if self.dragging_item is not None:
            if case is not None :
                # Vérification de compatibilité : on ne peut pas mettre une armure dans le slot arme, et vice versa.
                if case == "arme" and not isinstance(self.dragging_item, Weapon):
                    return
                if case == "armure" and not isinstance(self.dragging_item, Armor):
                    return
                if self.items[case] is None:
                    self.items[case] = self.dragging_item
                    self.dragging_item = None
                    self.old_drag_case = None
                    if case == "armure":
                        bonus = self.items[case].liste_attributs.get("bonus_health", 0)
                        app.player.health = min(app.player.get_max_health(app), app.player.health + bonus)
                else:
                    # Échange entre l'item tenu et celui présent dans la case cible.
                    old_item = self.items[case]
                    temp = self.dragging_item
                    self.items[case], self.dragging_item = temp, self.items[case]
                    self.items[self.old_drag_case] = None
                    self.old_drag_case = None
                    if case == "armure":
                        # Recalcul des PV en tenant compte du changement d'armure (ancienne vs nouvelle).
                        old_bonus = old_item.liste_attributs.get("bonus_health", 0) if old_item else 0
                        new_bonus = self.items[case].liste_attributs.get("bonus_health", 0)
                        app.player.health = min(app.player.get_max_health(app), app.player.health - old_bonus + new_bonus)
            else:
                # Si on dépose en dehors de l'inventaire, l'item retourne dans sa case d'origine.
                self.items[self.old_drag_case] = self.dragging_item
                self.dragging_item = None
                self.old_drag_case = None
            return
        
        if case is None:
            return
        self.old_drag_case = case
        self.dragging_item = self.items[case]
        self.items[case] = None

    # Affiche le sprite de l'item actuellement tenu sous le curseur de la souris.
    def show_drag_item(self):
        if self.dragging_item is not None:
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            img_bank = getattr(self.dragging_item, 'image_bank', 0)
            pyxel.blt(mx - 16, my - 16, img_bank, self.dragging_item.image_x, self.dragging_item.image_y, 32, 32, colkey=self.dragging_item.colkey)

    # Affiche un tooltip (bulle d'info) avec le nom, la description et les stats de l'item survolé.
    # La position du tooltip s'adapte pour rester dans les limites de l'écran.
    def over_item(self, app):
        case = self.récuperer_case_souris()
        if case is None:
            return
        item = self.items[case]
        if item is None:
            return

        mx, my = pyxel.mouse_x, pyxel.mouse_y
        lines = [item.name, item.description] + item.get_stats(app)

        # Calcul de la taille du tooltip en fonction du texte le plus long.
        w = max(len(l) * 4 + 8 for l in lines)
        h = len(lines) * 9 + 6

        # Placement intelligent : à droite et en haut de la souris si possible, sinon de l'autre côté.
        tx = mx + 10 if mx + 10 + w < 512 else mx - w - 4
        ty = my - h - 4 if my - h - 4 > 0 else my + 10

        pyxel.rect (tx, ty, w, h, 1)
        pyxel.rectb(tx, ty, w, h, 6)
        for i in range(len(lines)):
            color = 7 if i == 0 else (6 if i == 1 else 10)
            pyxel.text(tx + 4, ty + 4 + i * 9, lines[i], color)

    # Ajoute un item dans la première case vide de l'inventaire (cases 1 à 20).
    # Renvoie True si l'ajout a réussi, False si l'inventaire est plein.
    def add_item(self, item):
        for idx in range(1, 21):
            if self.items[idx] is None:
                self.items[idx] = item
                return True
        return False

    # Supprime l'item dans la case pointée par la souris. Renvoie True si un item a été supprimé.
    def supprimer_item(self):
        case = self.récuperer_case_souris()
        if case is not None and self.items[case] is not None:
            self.items[case] = None
            return True
        return False

    # Utilise la potion dans la case pointée par la souris.
    # Si la durée est 0, l'effet est immédiat (soin instantané). Sinon, l'effet est ajouté à la liste des effets actifs.
    def use_item(self, app):
        case = self.récuperer_case_souris()
        if case is not None and self.items[case] is not None and self.items[case].type == "potion":
            potion = self.items[case]
            self.items[case] = None
            if potion.duration == 0:
                if "heal" in potion.liste_attributs:
                    app.player.regen(app, potion.value)
            else:
                app.potion_active.append({"effect": potion.liste_attributs, "value": potion.value, "duration": potion.duration})