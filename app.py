import pyxel
from world import World
from player import Player

class App:
    
    def __init__(self):

        self.timestop = False
        self.width = 512
        self.heigth = 256
        self.x_center, self.y_center = self.width / 2, self.heigth / 2
        self.x = self.x_center - 16
        self.y = self.y_center - 16
        self.player = Player()
        self.world = World(self.width, self.heigth,0)
    
        pyxel.init(self.width, self.heigth, title = "Jeu du héros")
        pyxel.load('Textures/res.pyxres')
        
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.timestop == False:
            self.world.deplace(self, self.player.speed)
        else:
            #self.player.deplace(self.player, self.player.speed)
            pass
    def draw(self):
        pyxel.cls(0)
        self.world.place_map(self.x_center, self.y_center)
        pyxel.rect(self.x, self.y, 32, 32, 9)