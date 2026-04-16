class Zone:
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
