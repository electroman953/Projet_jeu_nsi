class Zone:
    # Représente une zone de la carte avec ses propres ennemis, sa difficulté et ses limites spatiales.
    # Utilisée pour contrôler le spawn (apparition) des mobs par secteur.
    def __init__(self, name, monstre, difficulty, max_mob, x, y, width, height):
        self.name = name
        self.monstre = monstre
        self.difficulty = difficulty
        self.max_mob = max_mob
        self.respawn_time = 10
        self.timer_respawn = 0
        self.x = x
        self.y = y
        self.width = width
        self.height = height