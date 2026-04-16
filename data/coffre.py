class Coffre:
    def __init__(self, id, nom, description, contenu):
        self.id = id
        self.nom = nom
        self.description = description
        self.contenu = contenu

    def ouvrir(self):
        return f"Vous ouvrez le coffre '{self.nom}' et trouvez : {self.contenu}"