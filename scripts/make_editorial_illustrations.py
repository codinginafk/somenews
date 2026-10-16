"""Generate stark, minimalist editorial illustrations for CADCraft, GridCraft, WordCraft, ArtCraft.
Two-tone style with warm cream paper background (hex #F7F2E9),
deep charcoal black ink silhouettes (hex #16130E),
and a bold splash of vermilion red-orange accent color (hex #C2410C).
Wireframe grid subtle background. Strictly no translucent or faded elements.
"""
from PIL import Image, ImageDraw
import math

W, H = 1376, 768
CREAM = (247, 242, 233)
GRID = (232, 224, 210)
INK = (22, 19, 14)
VERM = (194, 65, 12)

def draw_base_grid(draw):
    # Background
    draw.rectangle([0, 0, W, H], fill=CREAM)
    # Subtle wireframe grid
    step = 48
    for x in range(0, W, step):
        draw.line([(x, 0), (x, H)], fill=GRID, width=1)
    for y in range(0, H, step):
        draw.line([(0, y), (W, y)], fill=GRID, width=1)
    # Isometric/perspective horizon guide lines
    draw.line([(0, int(H * 0.7)), (W, int(H * 0.7))], fill=GRID, width=2)
    # Floor perspective rays converging to center-left
    vp_x, vp_y = int(W * 0.45), int(H * 0.4)
    for px in range(-200, W + 400, 120):
        draw.line([(px, H), (vp_x, vp_y)], fill=GRID, width=1)

def create_cadcraft():
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    draw_base_grid(d)
    
    # Floor plane
    d.polygon([(0, int(H * 0.72)), (W, int(H * 0.72)), (W, H), (0, H)], fill=(238, 230, 218))
    
    # Workstation / drafting table silhouette
    d.polygon([(180, int(H * 0.52)), (880, int(H * 0.52)), (920, int(H * 0.78)), (140, int(H * 0.78))], fill=INK)
    d.rectangle([200, int(H * 0.78), 240, H], fill=INK)
    d.rectangle([820, int(H * 0.78), 860, H], fill=INK)
    
    # Large angled drafting monitor
    d.polygon([(260, int(H * 0.22)), (800, int(H * 0.22)), (780, int(H * 0.52)), (280, int(H * 0.52))], fill=INK)
    # Stand
    d.rectangle([510, int(H * 0.52), 550, int(H * 0.62)], fill=INK)
    
    # Blueprint vector lines on screen (Charcoal / Cream cutout)
    # Circular mechanical gear outline
    d.ellipse([380, int(H * 0.26), 540, int(H * 0.48)], outline=CREAM, width=3)
    d.ellipse([420, int(H * 0.31), 500, int(H * 0.43)], outline=CREAM, width=2)
    d.line([(340, int(H * 0.37)), (580, int(H * 0.37))], fill=CREAM, width=2)
    d.line([(460, int(H * 0.24)), (460, int(H * 0.50))], fill=CREAM, width=2)
    
    # Architectural dimension layout lines
    d.line([(580, int(H * 0.28)), (740, int(H * 0.28))], fill=CREAM, width=2)
    d.line([(580, int(H * 0.28)), (580, int(H * 0.46))], fill=CREAM, width=2)
    d.line([(740, int(H * 0.28)), (740, int(H * 0.46))], fill=CREAM, width=2)
    d.line([(580, int(H * 0.46)), (740, int(H * 0.46))], fill=CREAM, width=2)
    
    # Bold Vermilion Red-Orange Accent: CAD drafting crosshairs & dimension arc
    cx, cy = 660, int(H * 0.36)
    d.line([(cx - 40, cy), (cx + 40, cy)], fill=VERM, width=4)
    d.line([(cx, cy - 40), (cx, cy + 40)], fill=VERM, width=4)
    d.arc([cx - 25, cy - 25, cx + 25, cy + 25], 0, 360, fill=VERM, width=3)
    # Dimension leader line and arrow in Vermilion
    d.line([(cx + 25, cy - 25), (710, int(H * 0.25))], fill=VERM, width=3)
    d.line([(710, int(H * 0.25)), (750, int(H * 0.25))], fill=VERM, width=3)
    d.polygon([(cx + 25, cy - 25), (cx + 33, cy - 20), (cx + 20, cy - 33)], fill=VERM)
    
    # Draftsman / Architect silhouette leaning over workstation
    # Head
    d.ellipse([920, int(H * 0.32), 990, int(H * 0.41)], fill=INK)
    # Torso leaning forward
    d.polygon([(920, int(H * 0.41)), (1000, int(H * 0.41)), (1040, int(H * 0.72)), (880, int(H * 0.72))], fill=INK)
    # Arm reaching toward desk
    d.polygon([(890, int(H * 0.46)), (810, int(H * 0.58)), (840, int(H * 0.60)), (920, int(H * 0.50))], fill=INK)
    # Stool / legs
    d.rectangle([940, int(H * 0.72), 970, H], fill=INK)
    d.rectangle([1000, int(H * 0.72), 1030, H], fill=INK)
    
    im.save("demo-news/public/images/cadcraft-rust-autocad.jpg", quality=95)

def create_gridcraft():
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    draw_base_grid(d)
    
    # Floor plane
    d.polygon([(0, int(H * 0.72)), (W, int(H * 0.72)), (W, H), (0, H)], fill=(238, 230, 218))
    
    # Desk silhouette
    d.polygon([(160, int(H * 0.54)), (960, int(H * 0.54)), (1000, int(H * 0.78)), (120, int(H * 0.78))], fill=INK)
    d.rectangle([180, int(H * 0.78), 220, H], fill=INK)
    d.rectangle([900, int(H * 0.78), 940, H], fill=INK)
    
    # Ultrawide dual spreadsheet monitor
    d.polygon([(240, int(H * 0.18)), (880, int(H * 0.18)), (860, int(H * 0.54)), (260, int(H * 0.54))], fill=INK)
    d.rectangle([540, int(H * 0.54), 580, int(H * 0.64)], fill=INK)
    
    # Spreadsheet matrix grid lines on screen (Cream on Ink)
    sx1, sy1, sx2, sy2 = 280, int(H * 0.22), 840, int(H * 0.50)
    col_w = 70
    row_h = 24
    for gx in range(sx1, sx2, col_w):
        d.line([(gx, sy1), (gx, sy2)], fill=CREAM, width=1)
    for gy in range(sy1, sy2, row_h):
        d.line([(sx1, gy), (sx2, gy)], fill=CREAM, width=1)
    
    # Bold Vermilion Red-Orange Accent: Formula calculation bar & highlighted dynamic array cell
    fx1, fy1, fx2, fy2 = sx1 + col_w * 3, sy1 + row_h * 2, sx1 + col_w * 6, sy1 + row_h * 6
    # Active formula cell highlight block
    d.rectangle([fx1, fy1, fx2, fy2], outline=VERM, width=4)
    d.rectangle([fx1, fy1, fx1 + col_w, fy1 + row_h], fill=VERM)
    # Small drag handle on corner of dynamic array
    d.rectangle([fx2 - 4, fy2 - 4, fx2 + 4, fy2 + 4], fill=VERM)
    
    # Formula bar highlight above grid
    d.rectangle([sx1, sy1 - 16, sx2, sy1 - 6], fill=INK)
    d.rectangle([sx1 + 80, sy1 - 14, sx1 + 320, sy1 - 8], fill=VERM)
    
    # Data Analyst silhouette sitting in ergonomic chair
    # Chair silhouette
    d.polygon([(980, int(H * 0.36)), (1060, int(H * 0.36)), (1040, int(H * 0.74)), (970, int(H * 0.74))], fill=INK)
    d.rectangle([1000, int(H * 0.74), 1020, H], fill=INK)
    # Analyst Head
    d.ellipse([930, int(H * 0.28), 990, int(H * 0.37)], fill=INK)
    # Analyst Torso
    d.polygon([(930, int(H * 0.37)), (1010, int(H * 0.37)), (1020, int(H * 0.68)), (920, int(H * 0.68))], fill=INK)
    # Analyst Arms typing on keyboard
    d.polygon([(930, int(H * 0.44)), (850, int(H * 0.55)), (880, int(H * 0.58)), (950, int(H * 0.48))], fill=INK)
    
    im.save("demo-news/public/images/gridcraft-rust-excel.jpg", quality=95)

def create_wordcraft():
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    draw_base_grid(d)
    
    # Floor plane
    d.polygon([(0, int(H * 0.72)), (W, int(H * 0.72)), (W, H), (0, H)], fill=(238, 230, 218))
    
    # Author Desk silhouette
    d.polygon([(200, int(H * 0.54)), (980, int(H * 0.54)), (1020, int(H * 0.78)), (160, int(H * 0.78))], fill=INK)
    d.rectangle([220, int(H * 0.78), 260, H], fill=INK)
    d.rectangle([920, int(H * 0.78), 960, H], fill=INK)
    
    # Vertical portrait document monitor
    d.polygon([(340, int(H * 0.14)), (760, int(H * 0.14)), (740, int(H * 0.54)), (360, int(H * 0.54))], fill=INK)
    d.rectangle([530, int(H * 0.54), 570, int(H * 0.64)], fill=INK)
    
    # Document manuscript margins and text block bars (Cream on Ink)
    doc_x1, doc_y1, doc_x2, doc_y2 = 400, int(H * 0.18), 700, int(H * 0.50)
    d.rectangle([doc_x1, doc_y1, doc_x2, doc_y2], outline=CREAM, width=2)
    # Ruler on top
    d.line([(doc_x1, doc_y1 + 14), (doc_x2, doc_y1 + 14)], fill=CREAM, width=1)
    
    # Simulated paragraphs of text lines
    line_y = doc_y1 + 26
    while line_y < doc_y2 - 20:
        d.rectangle([doc_x1 + 16, line_y, doc_x2 - 16, line_y + 4], fill=CREAM)
        line_y += 14
        
    # Bold Vermilion Red-Orange Accent: Active paragraph revision mark & typing cursor
    rev_y = doc_y1 + 26 + 14 * 4
    # Vermilion track-changes insertion highlight block
    d.rectangle([doc_x1 + 60, rev_y - 2, doc_x1 + 220, rev_y + 6], fill=VERM)
    # Tall pulsing text cursor
    d.rectangle([doc_x1 + 224, rev_y - 6, doc_x1 + 228, rev_y + 10], fill=VERM)
    # Margin revision bubble in vermilion
    d.polygon([(doc_x2 + 8, rev_y - 4), (doc_x2 + 36, rev_y - 4), (doc_x2 + 36, rev_y + 12), (doc_x2 + 8, rev_y + 12)], fill=VERM)
    
    # Writer silhouette at desk
    # Head
    d.ellipse([1010, int(H * 0.30), 1070, int(H * 0.39)], fill=INK)
    # Torso
    d.polygon([(1010, int(H * 0.39)), (1080, int(H * 0.39)), (1070, int(H * 0.70)), (990, int(H * 0.70))], fill=INK)
    # Hand on keyboard
    d.polygon([(1000, int(H * 0.46)), (910, int(H * 0.55)), (930, int(H * 0.58)), (1010, int(H * 0.50))], fill=INK)
    # Books stacked on right edge of desk
    d.rectangle([980, int(H * 0.48), 1080, int(H * 0.54)], fill=INK)
    d.rectangle([990, int(H * 0.43), 1070, int(H * 0.48)], fill=INK)
    
    im.save("demo-news/public/images/wordcraft-rust-word.jpg", quality=95)

def create_artcraft():
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    draw_base_grid(d)
    
    # Floor plane
    d.polygon([(0, int(H * 0.70)), (W, int(H * 0.70)), (W, H), (0, H)], fill=(238, 230, 218))
    
    # Studio Console / production desk silhouette
    d.polygon([(120, int(H * 0.50)), (920, int(H * 0.50)), (960, int(H * 0.76)), (80, int(H * 0.76))], fill=INK)
    d.rectangle([140, int(H * 0.76), 180, H], fill=INK)
    d.rectangle([860, int(H * 0.76), 900, H], fill=INK)
    
    # Dual studio production monitors
    # Left monitor (3D viewport & camera staging)
    d.polygon([(180, int(H * 0.16)), (520, int(H * 0.16)), (500, int(H * 0.50)), (200, int(H * 0.50))], fill=INK)
    # Right monitor (Multi-track timeline)
    d.polygon([(540, int(H * 0.16)), (880, int(H * 0.16)), (860, int(H * 0.50)), (560, int(H * 0.50))], fill=INK)
    
    # 3D viewport spatial grid on left screen
    vx1, vy1, vx2, vy2 = 220, int(H * 0.20), 480, int(H * 0.46)
    d.rectangle([vx1, vy1, vx2, vy2], outline=CREAM, width=2)
    # Isometric cube / staging mannequin outline
    d.polygon([(340, int(H * 0.24)), (400, int(H * 0.28)), (340, int(H * 0.32)), (280, int(H * 0.28))], outline=CREAM, width=2)
    d.line([(280, int(H * 0.28)), (280, int(H * 0.40))], fill=CREAM, width=2)
    d.line([(400, int(H * 0.28)), (400, int(H * 0.40))], fill=CREAM, width=2)
    d.line([(340, int(H * 0.32)), (340, int(H * 0.44))], fill=CREAM, width=2)
    
    # Timeline tracks on right screen
    tx1, ty1, tx2, ty2 = 580, int(H * 0.20), 840, int(H * 0.46)
    d.rectangle([tx1, ty1, tx2, ty2], outline=CREAM, width=2)
    for track_y in range(ty1 + 20, ty2, 22):
        d.line([(tx1, track_y), (tx2, track_y)], fill=CREAM, width=1)
        # Media clip blocks on tracks
        d.rectangle([tx1 + 20, track_y - 16, tx1 + 100, track_y - 4], fill=CREAM)
        d.rectangle([tx1 + 140, track_y - 16, tx1 + 220, track_y - 4], fill=CREAM)
        
    # Bold Vermilion Red-Orange Accent: Director timeline playhead & keyframe camera node
    playhead_x = tx1 + 120
    d.line([(playhead_x, ty1), (playhead_x, ty2)], fill=VERM, width=4)
    d.polygon([(playhead_x - 8, ty1), (playhead_x + 8, ty1), (playhead_x, ty1 + 14)], fill=VERM)
    # 3D staging camera focal target on left screen in Vermilion
    d.ellipse([332, int(H * 0.32) - 8, 348, int(H * 0.32) + 8], fill=VERM)
    
    # Creative Director silhouette
    # Head
    d.ellipse([980, int(H * 0.28), 1040, int(H * 0.37)], fill=INK)
    # Torso
    d.polygon([(980, int(H * 0.37)), (1050, int(H * 0.37)), (1030, int(H * 0.68)), (960, int(H * 0.68))], fill=INK)
    # Arms directing / staging
    d.polygon([(970, int(H * 0.42)), (890, int(H * 0.52)), (910, int(H * 0.55)), (990, int(H * 0.46))], fill=INK)
    
    im.save("demo-news/public/images/artcraft-rust-creative-engine.jpg", quality=95)

if __name__ == "__main__":
    create_cadcraft()
    create_gridcraft()
    create_wordcraft()
    create_artcraft()
    print("All 4 editorial illustrations generated.")
