import pyxel
from data.items import sword, bow, staff, Armor

class Inventory:
    def __init__(self, app):
        self.items = {i : None for i in range(24)}
        self.items["arme"] = None
        self.items["armure"] = None
        for i in range(1, 21):
            self.items[i] = make_item(app.items[i])
        self.on_screen = False
        self.dragging_item = None
        self.old_drag_case = None

    def open(self, app):
        self.on_screen = not self.on_screen
        app.timestop = self.on_screen
        pyxel.mouse(self.on_screen)
        if self.on_screen:
            self.items[self.old_drag_case] = self.dragging_item
            self.dragging_item = None
    def afficher(self, app):
        if self.on_screen:
            px, py = 80, 40
            pyxel.rect(px, py, 320, 175, 1)
            pyxel.rectb(px, py, 320, 175, 6)

            # Preview joueur
            pyxel.rect(px+16, py+12, 48, 64, 5)
            pyxel.rectb(px+16, py+12, 48, 64, 6)
            pyxel.blt(px+28, py+20, 0, 0, 0, 23, 39, colkey=3) 

            # Slots armure et arme
            for i in range(2):
                sx = px + 10 + i * 40
                pyxel.rect(sx, py+88, 32, 32, 5)
                pyxel.rectb(sx, py+88, 32, 32, 6)

            # Séparateur
            pyxel.line(px+92, py+4, px+92, py+171, 13)

            # Grille inventaire
            pyxel.text(px+148, py+6, "INVENTAIRE", 7)
            for row in range(4):
                for col in range(6):
                    sx, sy = px+100 + col*36, py+16 + row*36
                    pyxel.rect(sx, sy, 32, 32, 5)
                    pyxel.rectb(sx, sy, 32, 32, 6)
            self.afficher_items()
    def afficher_items(self):
        if self.on_screen:
            for idx, item in self.items.items():
                if item is None or (self.dragging_item is not None and idx == self.old_drag_case):
                    continue
                if idx is None:
                    continue
                if type(idx) == str:
                    sx = 90 if idx == "arme" else 130
                    sy = 128
                else:
                    sx = 180 + (idx % 6) * 36
                    sy = 56 + (idx // 6) * 36
                pyxel.blt(sx, sy, 2, item.image_x, item.image_y, 32, 32, colkey=item.colkey)
            self.show_drag_item()
    def récuperer_case_souris(self):
        if not self.on_screen:
            return None
        mx, my = pyxel.mouse_x, pyxel.mouse_y
        #vérifie pour les cases d'equipement actif armure et arme
        if 90 <= mx < 90 + 32 and 128 <= my < 128 + 32:
            return "arme"
        if 130 <= mx < 130 + 32 and 128 <= my < 128 + 32:
            return "armure"
        return int(f"{(my - 56) // 36}{(mx - 180) // 36}", 6) if 180 <= mx < 180 + 6*36 and 56 <= my < 56 + 4*36 else None
    def drag_item(self, app):
        case = self.récuperer_case_souris()
        if self.dragging_item is not None:
            if case is not None :
                if self.items[case] is None:
                    self.items[case] = self.dragging_item
                    self.dragging_item = None
                    self.old_drag_case = None
                else:
                    temp = self.dragging_item
                    self.items[case], self.dragging_item = temp, self.items[case]
                    self.items[self.old_drag_case] = None
                    self.old_drag_case = None

            else:
                self.items[self.old_drag_case] = self.dragging_item
                self.dragging_item = None
                self.old_drag_case = None
            return
        
        if case is None:
            return
        self.old_drag_case = case
        self.dragging_item = self.items[case]
        self.items[case] = None
    def show_drag_item(self):
        if self.dragging_item is not None:
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            pyxel.blt(mx - 16, my - 16, 2, self.dragging_item.image_x, self.dragging_item.image_y, 32, 32, colkey=self.dragging_item.colkey)
    def over_item(self, app):
        case = self.récuperer_case_souris()
        if case is None:
            return
        item = self.items[case]
        if item is None:
            return

        mx, my = pyxel.mouse_x, pyxel.mouse_y
        lines = [item.name, item.description] + item.get_stats(app)

        w = max(len(l) * 4 + 8 for l in lines)
        h = len(lines) * 9 + 6
        tx = mx + 10 if mx + 10 + w < 512 else mx - w - 4
        ty = my - h - 4 if my - h - 4 > 0 else my + 10

        pyxel.rect (tx, ty, w, h, 1)
        pyxel.rectb(tx, ty, w, h, 6)
        for i in range(len(lines)):
            color = 7 if i == 0 else (6 if i == 1 else 10)
            pyxel.text(tx + 4, ty + 4 + i * 9, lines[i], color)
def make_item(data):
    type_, name, desc, x, y, stat, *extra = data
    bonus = extra[0] if extra else {}
    constructors = {"sword": sword, "bow": bow, "staff": staff, "armor": Armor}
    item = constructors[type_](name, desc, x, y, stat, **bonus)
    return item
