import pyxel

class Coffre:
    def __init__(self, id, nom, description, contenu):
        self.id = id
        self.nom = nom
        self.description = description
        self.contenu = contenu

    def ouvrir(self):
        return f"Vous ouvrez le coffre '{self.nom}' et trouvez : {self.contenu}"
    
    def draw(self, x, y):
        pyxel.blt(x, y, 0, 0, 0, 16, 16, colkey=0)