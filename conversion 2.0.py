"""
img_to_pyxel.py
Convertit une image (512x256 ou autre) en un fichier .py Pyxel
avec des appels pset/rect optimisés et conversion vers la palette Pyxel 16 couleurs.

Usage :
    python img_to_pyxel.py mon_image.png -o output.py
"""

import argparse
from pathlib import Path
from PIL import Image

# ── Palette Pyxel 16 couleurs (index → RGB) ──────────────────────────────────
PYXEL_PALETTE = [
    (0,   0,   0),    # 0  black
    (43,  51,  95),   # 1  dark navy
    (126, 32,  114),  # 2  purple
    (25,  149, 156),  # 3  teal
    (139, 72,  82),   # 4  dark red
    (57,  92,  110),  # 5  dark blue-grey
    (169, 193, 255),  # 6  light lavender
    (238, 238, 238),  # 7  white
    (212, 24,  108),  # 8  pink/red
    (211, 132, 65),   # 9  orange
    (233, 195, 91),   # 10 yellow
    (112, 198, 169),  # 11 light green
    (118, 150, 222),  # 12 light blue
    (163, 163, 163),  # 13 light grey
    (255, 151, 152),  # 14 light pink
    (254, 207, 158),  # 15 peach
]


def nearest_pyxel_color(r: int, g: int, b: int) -> int:
    """Retourne l'index Pyxel le plus proche (distance euclidienne en RGB)."""
    best_idx, best_dist = 0, float("inf")
    for idx, (pr, pg, pb) in enumerate(PYXEL_PALETTE):
        d = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2
        if d < best_dist:
            best_dist, best_idx = d, idx
    return best_idx


def image_to_pyxel_indices(img: Image.Image) -> list[list[int]]:
    """Convertit chaque pixel en index palette Pyxel."""
    rgb = img.convert("RGB")
    w, h = rgb.size
    pixels = list(rgb.getdata())
    grid = []
    for y in range(h):
        row = []
        for x in range(w):
            r, g, b = pixels[y * w + x]
            row.append(nearest_pyxel_color(r, g, b))
        grid.append(row)
    return grid


# ── Algorithme de compression par rectangles ─────────────────────────────────

def find_max_rect(grid: list[list[int]], used: list[list[bool]],
                  x0: int, y0: int, color: int) -> tuple[int, int, int, int]:
    """
    Trouve le plus grand rectangle de couleur `color` à partir de (x0, y0)
    sans chevauchement avec les pixels déjà traités.
    Retourne (x0, y0, w, h).
    """
    h_img = len(grid)
    w_img = len(grid[0])

    # Largeur maximale sur la ligne y0
    max_w = 0
    for x in range(x0, w_img):
        if grid[y0][x] == color and not used[y0][x]:
            max_w += 1
        else:
            break

    if max_w == 0:
        return (x0, y0, 0, 0)

    best_area = 0
    best = (x0, y0, max_w, 1)
    cur_w = max_w

    for y in range(y0, h_img):
        # Réduire cur_w à la largeur disponible sur cette ligne
        w = 0
        for x in range(x0, x0 + cur_w):
            if grid[y][x] == color and not used[y][x]:
                w += 1
            else:
                break
        cur_w = w
        if cur_w == 0:
            break
        height = y - y0 + 1
        area = cur_w * height
        if area > best_area:
            best_area = area
            best = (x0, y0, cur_w, height)

    return best


def mark_used(used: list[list[bool]], x: int, y: int, w: int, h: int):
    for dy in range(h):
        for dx in range(w):
            used[y + dy][x + dx] = True


def compress_to_rects(grid: list[list[int]]) -> list[tuple]:
    """
    Parcourt l'image et produit une liste de (x, y, w, h, color).
    Utilise une heuristique gloutonne : pour chaque pixel non traité,
    on cherche le plus grand rectangle possible.
    """
    h_img = len(grid)
    w_img = len(grid[0])
    used = [[False] * w_img for _ in range(h_img)]
    ops = []

    for y in range(h_img):
        for x in range(w_img):
            if used[y][x]:
                continue
            color = grid[y][x]
            rx, ry, rw, rh = find_max_rect(grid, used, x, y, color)
            if rw > 0 and rh > 0:
                mark_used(used, rx, ry, rw, rh)
                ops.append((rx, ry, rw, rh, color))

    return ops


# ── Génération du fichier .py ─────────────────────────────────────────────────

def generate_py(ops: list[tuple], width: int, height: int, out_path: Path):
    lines = [
        "import pyxel",
        "",
        "",
        "class App:",
        "    def __init__(self):",
        f"        pyxel.init({width}, {height}, title=\"Image\")",
        "        pyxel.run(self.update, self.draw)",
        "",
        "    def update(self):",
        "        if pyxel.btnp(pyxel.KEY_Q):",
        "            pyxel.quit()",
        "",
        "    def draw(self):",
        f"        pyxel.cls(0)",
    ]

    for (x, y, w, h, c) in ops:
        if w == 1 and h == 1:
            lines.append(f"        pyxel.pset({x}, {y}, {c})")
        else:
            lines.append(f"        pyxel.rect({x}, {y}, {w}, {h}, {c})")

    lines += [
        "",
        "",
        "App()",
        "",
    ]

    out_path.write_text("\n".join(lines), encoding="utf-8")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Convertit une image en fichier .py Pyxel optimisé."
    )
    parser.add_argument("image", help="Chemin vers l'image source")
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Fichier .py de sortie (défaut : <image>.py)"
    )
    args = parser.parse_args()

    src = Path(args.image)
    if not src.exists():
        print(f"Erreur : fichier introuvable : {src}")
        return

    out = Path(args.output) if args.output else src.with_suffix(".py")

    print(f"Chargement de {src} …")
    img = Image.open(src)
    w, h = img.size
    print(f"  Taille : {w}×{h}")

    print("Conversion vers la palette Pyxel …")
    grid = image_to_pyxel_indices(img)

    print("Compression en rectangles …")
    ops = compress_to_rects(grid)
    n_rect  = sum(1 for o in ops if o[2] > 1 or o[3] > 1)
    n_pset  = sum(1 for o in ops if o[2] == 1 and o[3] == 1)
    print(f"  {len(ops)} opérations ({n_rect} rect, {n_pset} pset)")
    print(f"  (au lieu de {w * h} pset bruts)")

    print(f"Écriture dans {out} …")
    generate_py(ops, w, h, out)
    print("Terminé ✓")


if __name__ == "__main__":
    main()