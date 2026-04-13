import pyxel
import sys

# CONFIGURATION
INPUT_FILE = "res.pyxres"   # fichier .pyxres en entrée
OUTPUT_FILE = "attack 2 right and up.png"     # fichier PNG de sortie

pyxel.init(256, 256)
pyxel.load(INPUT_FILE)

def update():
    # Exporter l'image bank 0 en PNG
    img = pyxel.image(0)
    img.save(OUTPUT_FILE, 1)
    print(f"Image 0 exportée dans '{OUTPUT_FILE}'")
    pyxel.quit()

def draw():
    pyxel.cls(0)

pyxel.run(update, draw)