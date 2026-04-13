import pyxel
from data.world import World
from data.player import Player
from data.inventory import Inventory
from data.mob import Mob
from data.arrow import Arrow

class App:
    
    def __init__(self):
        self.on_menu = False
        self.timestop = False
        self.TIMESTOP_DURATION = 5
        self.TIMESTOP_COOLDOWN = 10
        self.timestop_timer = 0
        self.timestop_cooldown = 0
        self.width = 512
        self.height = 256
        self.elt_col = [(16, 21), (16, 22), (16, 23), (16, 24), (16, 25), (16, 26), (16, 27), (17, 21), (17, 22), (17, 23), (17, 24), (17, 25), (17, 26), (17, 27), (18, 21), (18, 22), (18, 23), (18, 24), (18, 25), (18, 26), (18, 27), (19, 21), (19, 22), (19, 23), (19, 24), (19, 25), (19, 26), (19, 27), (20, 21), (20, 22), (20, 23), (20, 24), (20, 25), (20, 26), (20, 27), (21, 21), (21, 22), (21, 23), (21, 24), (21, 25), (21, 26), (21, 27)]
        self.screen_center_x = self.width // 2
        self.screen_center_y = self.height // 2

        self.palette_normal = [
            0x0D0D0D, 0x1D2B53, 0x7E2553, 0x008751,
            0xAB5236, 0x1E8C0A, 0xC2C3C7, 0xFFF1E8,  
            0xFF004D, 0xFFA300, 0xFFEC27, 0x00E436,
            0x3DDB1A, 0x83769C, 0xFF77A8, 0xFFCCAA   
        ]


        self.palette_timestop = [
            0x0D0D0D, 0x1D2B53, 0x7E2553, 0x008751,
            0xAB5236, 0x555555, 0xC2C3C7, 0xFFF1E8,  
            0xFF004D, 0xFFA300, 0xFFEC27, 0x00E436,
            0xAAAAAA, 0x83769C, 0xFF77A8, 0xFFCCAA   
        ]      
        self.x_center, self.y_center = self.screen_center_x, self.screen_center_y

        self.projectiles = []

        self.mobs = [('slime', 50, 50), ('slime', 75, 75), ('slime', 100, 100)]
        self.create_mobs()

        self.inventory = Inventory()
        self.player = Player()
        self.player_x_abs,self.player_y_abs = self.x_center, self.y_center
        self.world = World(self.width, self.height,2)
        self.recentrer = False
        pyxel.init(self.width, self.height, title = "Jeu du héros", fps=60)
        pyxel.load('../Textures/res.pyxres')
        print(pyxel.VERSION)
        pyxel.run(self.update, self.draw)

    def create_mobs(self):
        temp = []
        type={"slime": {"health": 100, "damage": 10, "height": 16, "width": 16, "color": 8}}
        for mob_type, x, y in self.mobs:
            mob = Mob(type[mob_type]["health"], type[mob_type]["damage"], mob_type, x, y, type[mob_type]["width"], type[mob_type]["height"], type[mob_type]["color"])
            temp.append(mob)
        self.mobs = temp

    def add_player_projectile(self, type, subtype):
        a={"arrow":{"basic":(3,5)}}
        xr = pyxel.mouse_x - (self.player.player_screen_x + self.player.width // 2)
        yr = pyxel.mouse_y - (self.player.player_screen_y + self.player.width // 2)
        hr = pyxel.sqrt(xr**2 + yr**2)
        if hr == 0:
            hr=1
        rotation = pyxel.atan2(yr, xr) - pyxel.atan2(-1, 1)
        self.projectiles.append(Arrow(self.player_x_abs, self.player_y_abs - self.player.height//4, a[type][subtype][1], rotation, (xr/hr, yr/hr), a[type][subtype][0], subtype))

    def update(self):
        self.player.check_key(self)
        if pyxel.frame_count % 6 == 0:
            if self.timestop_timer > 0:
                self.timestop_timer = max(0, self.timestop_timer - 0.1)
            if self.timestop_cooldown > 0:
                self.timestop_cooldown = max(0, self.timestop_cooldown - 0.1)
        if pyxel.frame_count % 30 == 0:
            for i in self.projectiles:
                i.supprimer(self)
        if self.timestop and self.timestop_timer == 0:
            self.timestop = False
            self.recentrer = True
            self.timestop_cooldown = self.TIMESTOP_COOLDOWN
        self.world.recentrer(self, 10)
        
        if self.recentrer:
            return
        if self.on_menu:
            return
        if self.inventory.on_screen:
            return
        if self.inventory.items["arme"]:
            self.inventory.items["arme"].etat_arme(True, self)
        self.load_walls()
        
        if self.timestop == False:
            self.world.deplace(self, self.player.speed)
        else:
            self.player.deplace(self)
            if self.timestop_timer == 0:
                self.timestop = False
                self.recentrer = True
            
    def draw(self):
        pyxel.cls(0)
        if self.on_menu:
            return
        
        
        self.world.place_map(self.x_center, self.y_center, self)
        self.player.draw(self)
        self.place_mobs()
        self.place_projectiles()

        if self.timestop:
            pyxel.colors[:] = self.palette_timestop
        else:
            pyxel.colors[:] = self.palette_normal    
        if self.inventory.on_screen:
            self.inventory.afficher(self)

    def place_mobs(self):
        for i in self.mobs:
            i.draw(self)
            i.move(self, self.player_x_abs, self.player_y_abs)
    
    def place_projectiles(self):
        for i in self.projectiles:
            i.draw(self)
            i.move()

    def load_walls(self):
        self.obstacle = []
        
        for x in range(self.x_center - self.width//2, self.x_center + self.width//2, 8):
            for y in range(self.y_center - self.height//2, self.y_center + self.height//2, 8):                
                
                if pyxel.tilemaps[self.world.tm].pget(x // 8, y // 8) in self.elt_col:
                    self.obstacle.append((x//8, y//8))
