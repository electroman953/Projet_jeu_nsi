import pyxel
from data.world import World
from data.player import Player

class App:
    
    def __init__(self):

        self.timestop = False
        self.width = 512
        self.height = 256
        self.elt_col = [(2,0),(3,0),(2,1),(3,1)]
        self.screen_center_x = self.width // 2
        self.screen_center_y = self.height // 2


        self.x_center, self.y_center = self.screen_center_x, self.screen_center_y


        
        self.player = Player()
        self.player_x_abs,self.player_y_abs = self.x_center, self.y_center
        self.world = World(self.width, self.height,0)
        self.recentrer = False
        pyxel.init(self.width, self.height, title = "Jeu du héros", fps=60)
        pyxel.load('../Textures/res.pyxres')
        
        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.check_key(self)
        self.world.recentrer(self, 10)
        if self.recentrer:
            return
        
        self.load_walls()
        if self.timestop == False:
            self.world.deplace(self, self.player.speed)
        else:
            self.player.deplace(self)
            
    def draw(self):
        pyxel.cls(0)
        self.world.place_map(self.x_center, self.y_center)
        player_screen_x = self.screen_center_x + (self.player_x_abs - self.x_center) - 16
        player_screen_y = self.screen_center_y + (self.player_y_abs - self.y_center) - 16
        pyxel.rect(player_screen_x, player_screen_y, 32, 32, 9)
    
    def load_walls(self):
        self.obstacle = []
        
        for x in range(self.x_center - self.width//2, self.x_center + self.width//2, 8):
            for y in range(self.y_center - self.height//2, self.y_center + self.height//2, 8):                
                
                if pyxel.tilemap(self.world.tm).pget(x // 8, y // 8) in self.elt_col: #verifie si c'est un obstacle
                    self.obstacle.append((x//8, y//8))
