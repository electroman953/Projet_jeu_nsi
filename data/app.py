import pyxel
from data.world import World
from data.player import Player

class App:
    
    def __init__(self):

        self.timestop = False
        self.width = 512
        self.height = 256
        self.elt_col = [(16, 21), (16, 22), (16, 23), (16, 24), (16, 25), (16, 26), (16, 27), (17, 21), (17, 22), (17, 23), (17, 24), (17, 25), (17, 26), (17, 27), (18, 21), (18, 22), (18, 23), (18, 24), (18, 25), (18, 26), (18, 27), (19, 21), (19, 22), (19, 23), (19, 24), (19, 25), (19, 26), (19, 27), (20, 21), (20, 22), (20, 23), (20, 24), (20, 25), (20, 26), (20, 27), (21, 21), (21, 22), (21, 23), (21, 24), (21, 25), (21, 26), (21, 27)]
        self.screen_center_x = self.width // 2
        self.screen_center_y = self.height // 2


        self.x_center, self.y_center = self.screen_center_x, self.screen_center_y


        
        self.player = Player()
        self.player_x_abs,self.player_y_abs = self.x_center, self.y_center
        self.world = World(self.width, self.height,1)
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
        player_screen_x = self.screen_center_x + (self.player_x_abs - self.x_center) - self.player.width//2
        player_screen_y = self.screen_center_y + (self.player_y_abs - self.y_center) - self.player.height//2
        pyxel.rect(player_screen_x, player_screen_y, self.player.width, self.player.height, 9)

    def load_walls(self):
        self.obstacle = []
        
        for x in range(self.x_center - self.width//2, self.x_center + self.width//2, 8):
            for y in range(self.y_center - self.height//2, self.y_center + self.height//2, 8):                
                
                if pyxel.tilemap(self.world.tm).pget(x // 8, y // 8) in self.elt_col: #verifie si c'est un obstacle
                    self.obstacle.append((x//8, y//8))
    