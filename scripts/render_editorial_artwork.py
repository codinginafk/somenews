"""
Render stark, high-resolution editorial vector illustrations for:
1. ArtCraft (Creative engine / Adobe alternative)
2. WordCraft (Word alternative)

Renders at 2x resolution (2752x1536) and downsamples with Lanczos to 1376x768
for pristine vector-sharp edges, smooth geometric silhouettes, and exact brand palette:
- Warm cream paper background: #F7F2E9
- Solid deep charcoal black ink: #16130E
- Bold vermilion red-orange accent: #C2410C
- Subtle wireframe grid: #E5DDD0
"""
from PIL import Image, ImageDraw
import math

W_FINAL, H_FINAL = 1376, 768
SCALE = 2
W, H = W_FINAL * SCALE, H_FINAL * SCALE

CREAM = (247, 242, 233)
GRID = (229, 221, 208)
GRID_ACCENT = (218, 208, 192)
INK = (22, 19, 14)
VERM = (194, 65, 12)

def draw_perspective_grid(d, vp_x, vp_y, horizon_y):
    # Base background
    d.rectangle([0, 0, W, H], fill=CREAM)
    
    # Wall background grid (vertical and horizontal lines)
    wall_step = 64 * SCALE
    for x in range(0, W, wall_step):
        d.line([(x, 0), (x, horizon_y)], fill=GRID, width=SCALE)
    for y in range(0, horizon_y, wall_step):
        d.line([(0, y), (W, y)], fill=GRID, width=SCALE)
        
    # Horizon line
    d.line([(0, horizon_y), (W, horizon_y)], fill=GRID_ACCENT, width=2 * SCALE)
    
    # Floor perspective rays from horizon toward bottom edge
    for x in range(-W // 2, W * 2, 80 * SCALE):
        d.line([(vp_x, vp_y), (x, H)], fill=GRID, width=SCALE)
        
    # Floor horizontal perspective rungs
    for t in [0.05, 0.12, 0.22, 0.35, 0.52, 0.72, 0.95]:
        fy = int(horizon_y + (H - horizon_y) * t)
        d.line([(0, fy), (W, fy)], fill=GRID, width=SCALE)

def draw_person_silhouette(d, x, y, facing_left=True, sitting=True):
    """Draw a natural, human-proportioned silhouette."""
    s = SCALE
    # Head
    head_r = 44 * s
    head_cx = x
    head_cy = y
    d.ellipse([head_cx - head_r, head_cy - head_r, head_cx + head_r, head_cy + head_r], fill=INK)
    
    # Neck & collar
    d.polygon([
        (head_cx - 16 * s, head_cy + 36 * s),
        (head_cx + 16 * s, head_cy + 36 * s),
        (head_cx + 26 * s, head_cy + 74 * s),
        (head_cx - 26 * s, head_cy + 74 * s)
    ], fill=INK)
    
    # Torso
    torso_top = head_cy + 70 * s
    torso_bottom = torso_top + 160 * s
    if sitting:
        # Leaning slightly forward
        d.polygon([
            (head_cx - 40 * s, torso_top),
            (head_cx + 38 * s, torso_top),
            (head_cx + (20 if facing_left else 55) * s, torso_bottom),
            (head_cx - (55 if facing_left else 20) * s, torso_bottom)
        ], fill=INK)
        # Shoulders curved
        d.ellipse([head_cx - 52 * s, torso_top - 10 * s, head_cx + 50 * s, torso_top + 50 * s], fill=INK)
        
        # Thighs / seated lap
        lap_x1 = head_cx - 55 * s if facing_left else head_cx - 20 * s
        lap_x2 = lap_x1 - 120 * s if facing_left else lap_x1 + 140 * s
        lap_y = torso_bottom + 10 * s
        d.polygon([
            (lap_x1, torso_bottom - 20 * s),
            (lap_x1 + (40 * s if facing_left else -40 * s), torso_bottom - 20 * s),
            (lap_x2, lap_y + 40 * s),
            (lap_x2 + (20 * s if facing_left else -20 * s), lap_y + 70 * s),
            (lap_x1, torso_bottom + 50 * s)
        ], fill=INK)
        
        # Arms reaching toward desk/keyboard
        arm_start_x = head_cx - 30 * s if facing_left else head_cx + 30 * s
        arm_end_x = arm_start_x - 130 * s if facing_left else arm_start_x + 130 * s
        arm_elbow_x = arm_start_x - 70 * s if facing_left else arm_start_x + 70 * s
        d.polygon([
            (arm_start_x, torso_top + 20 * s),
            (arm_elbow_x, torso_top + 90 * s),
            (arm_end_x, torso_top + 110 * s),
            (arm_end_x + 10 * s, torso_top + 130 * s),
            (arm_elbow_x + 20 * s, torso_top + 110 * s),
            (arm_start_x + 20 * s, torso_top + 30 * s)
        ], fill=INK)
    else:
        # Standing director silhouette
        d.polygon([
            (head_cx - 42 * s, torso_top),
            (head_cx + 42 * s, torso_top),
            (head_cx + 36 * s, torso_bottom),
            (head_cx - 36 * s, torso_bottom)
        ], fill=INK)
        # Legs standing firm
        d.rectangle([head_cx - 36 * s, torso_bottom, head_cx - 6 * s, torso_bottom + 200 * s], fill=INK)
        d.rectangle([head_cx + 6 * s, torso_bottom, head_cx + 36 * s, torso_bottom + 200 * s], fill=INK)
        # Pointing arm
        d.polygon([
            (head_cx - 30 * s, torso_top + 15 * s),
            (head_cx - 150 * s, torso_top - 40 * s),
            (head_cx - 150 * s, torso_top - 15 * s),
            (head_cx - 20 * s, torso_top + 45 * s)
        ], fill=INK)

def render_artcraft():
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    s = SCALE
    
    # Single unified vanishing point for natural spatial depth
    vp_x, vp_y = int(W * 0.42), int(H * 0.38)
    horizon_y = int(H * 0.65)
    draw_perspective_grid(d, vp_x, vp_y, horizon_y)
    
    # Architectural studio trusses / framework in background
    for tx in [int(W * 0.15), int(W * 0.85)]:
        d.rectangle([tx, 0, tx + 14 * s, horizon_y], fill=INK)
    d.line([(int(W * 0.15), int(H * 0.15)), (int(W * 0.85), int(H * 0.15))], fill=INK, width=4 * s)
    d.line([(int(W * 0.15), int(H * 0.28)), (int(W * 0.85), int(H * 0.28))], fill=INK, width=2 * s)
    
    # Studio lighting rig silhouettes hanging from trusses
    for lx in [int(W * 0.28), int(W * 0.72)]:
        d.line([(lx, int(H * 0.15)), (lx, int(H * 0.22))], fill=INK, width=3 * s)
        d.polygon([(lx - 25 * s, int(H * 0.22)), (lx + 25 * s, int(H * 0.22)), (lx + 40 * s, int(H * 0.28)), (lx - 40 * s, int(H * 0.28))], fill=INK)
    
    # Central Studio Production Console (Desks in perspective)
    desk_left, desk_right = int(W * 0.10), int(W * 0.78)
    desk_top, desk_bottom = int(H * 0.52), int(H * 0.78)
    d.polygon([
        (desk_left + 80 * s, desk_top),
        (desk_right - 40 * s, desk_top),
        (desk_right, desk_bottom),
        (desk_left, desk_bottom)
    ], fill=INK)
    # Heavy desk legs
    d.rectangle([desk_left + 40 * s, desk_bottom, desk_left + 80 * s, H], fill=INK)
    d.rectangle([desk_right - 80 * s, desk_bottom, desk_right - 40 * s, H], fill=INK)
    
    # Dual studio production monitors
    # Left Monitor: 3D Scene Viewport / Camera Staging
    m1_x1, m1_y1, m1_x2, m1_y2 = desk_left + 100 * s, int(H * 0.18), desk_left + 460 * s, desk_top - 10 * s
    d.polygon([(m1_x1, m1_y1), (m1_x2, m1_y1), (m1_x2 - 30 * s, m1_y2), (m1_x1 + 30 * s, m1_y2)], fill=INK)
    # Screen bezel cutout (cream window)
    d.polygon([(m1_x1 + 16 * s, m1_y1 + 16 * s), (m1_x2 - 16 * s, m1_y1 + 16 * s), (m1_x2 - 42 * s, m1_y2 - 16 * s), (m1_x1 + 42 * s, m1_y2 - 16 * s)], fill=CREAM)
    
    # 3D Wireframe Scene within left monitor (Inks on Cream)
    cx, cy = (m1_x1 + m1_x2) // 2, (m1_y1 + m1_y2) // 2
    # Perspective stage cube
    cube_s = 60 * s
    d.polygon([(cx, cy - cube_s), (cx + cube_s, cy - cube_s // 2), (cx, cy), (cx - cube_s, cy - cube_s // 2)], outline=INK, width=2 * s)
    d.line([(cx, cy), (cx, cy + cube_s)], fill=INK, width=2 * s)
    d.line([(cx - cube_s, cy - cube_s // 2), (cx - cube_s, cy + cube_s // 2)], fill=INK, width=2 * s)
    d.line([(cx + cube_s, cy - cube_s // 2), (cx + cube_s, cy + cube_s // 2)], fill=INK, width=2 * s)
    d.polygon([(cx, cy + cube_s), (cx + cube_s, cy + cube_s // 2), (cx, cy), (cx - cube_s, cy + cube_s // 2)], outline=INK, width=2 * s)
    
    # Vermilion Focal Accent 1: Camera frustum target ring on 3D stage
    d.ellipse([cx - 24 * s, cy - 24 * s, cx + 24 * s, cy + 24 * s], outline=VERM, width=4 * s)
    d.ellipse([cx - 8 * s, cy - 8 * s, cx + 8 * s, cy + 8 * s], fill=VERM)
    d.line([(cx - 36 * s, cy), (cx + 36 * s, cy)], fill=VERM, width=2 * s)
    d.line([(cx, cy - 36 * s), (cx, cy + 36 * s)], fill=VERM, width=2 * s)
    
    # Right Monitor: Multi-Track Timeline Sequencing
    m2_x1, m2_y1, m2_x2, m2_y2 = desk_left + 480 * s, int(H * 0.18), desk_right - 60 * s, desk_top - 10 * s
    d.polygon([(m2_x1, m2_y1), (m2_x2, m2_y1), (m2_x2 - 30 * s, m2_y2), (m2_x1 + 30 * s, m2_y2)], fill=INK)
    # Screen bezel cutout
    d.polygon([(m2_x1 + 16 * s, m2_y1 + 16 * s), (m2_x2 - 16 * s, m2_y1 + 16 * s), (m2_x2 - 42 * s, m2_y2 - 16 * s), (m2_x1 + 42 * s, m2_y2 - 16 * s)], fill=CREAM)
    
    # Media timeline tracks (Ink on Cream)
    tl_x1, tl_x2 = m2_x1 + 30 * s, m2_x2 - 30 * s
    for i, ty in enumerate(range(m2_y1 + 45 * s, m2_y2 - 40 * s, 26 * s)):
        d.line([(tl_x1, ty), (tl_x2, ty)], fill=INK, width=s)
        # Track clips
        d.rectangle([tl_x1 + (20 + i * 40) * s, ty - 18 * s, tl_x1 + (120 + i * 40) * s, ty - 4 * s], fill=INK)
        d.rectangle([tl_x1 + (160 + i * 30) * s, ty - 18 * s, tl_x1 + (240 + i * 30) * s, ty - 4 * s], fill=INK)
        
    # Vermilion Focal Accent 2: Active Timeline Playhead Bar & Marker
    playhead_x = tl_x1 + 140 * s
    d.line([(playhead_x, m2_y1 + 25 * s), (playhead_x, m2_y2 - 25 * s)], fill=VERM, width=4 * s)
    d.polygon([
        (playhead_x - 12 * s, m2_y1 + 25 * s),
        (playhead_x + 12 * s, m2_y1 + 25 * s),
        (playhead_x, m2_y1 + 42 * s)
    ], fill=VERM)
    
    # Foreground Standing Creative Director Silhouette (Right side, natural perspective)
    director_x = int(W * 0.84)
    director_y = int(H * 0.38)
    draw_person_silhouette(d, director_x, director_y, facing_left=True, sitting=False)
    
    # Monitor stands and cables
    d.rectangle([(m1_x1 + m1_x2) // 2 - 16 * s, desk_top - 12 * s, (m1_x1 + m1_x2) // 2 + 16 * s, desk_top + 10 * s], fill=INK)
    d.rectangle([(m2_x1 + m2_x2) // 2 - 16 * s, desk_top - 12 * s, (m2_x1 + m2_x2) // 2 + 16 * s, desk_top + 10 * s], fill=INK)
    
    # Resize with Lanczos to final resolution
    im_final = im.resize((W_FINAL, H_FINAL), Image.LANCZOS)
    im_final.save("demo-news/public/images/artcraft-rust-creative-engine.jpg", quality=95)
    print("ArtCraft illustration rendered successfully.")

def render_wordcraft():
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    s = SCALE
    
    # Vanishing point
    vp_x, vp_y = int(W * 0.38), int(H * 0.36)
    horizon_y = int(H * 0.65)
    draw_perspective_grid(d, vp_x, vp_y, horizon_y)
    
    # Library bookshelf architecture in background (deep silhouettes on wall)
    for bx in range(int(W * 0.05), int(W * 0.32), 60 * s):
        d.rectangle([bx, int(H * 0.12), bx + 48 * s, int(H * 0.50)], fill=INK)
        # Horizontal book rungs
        d.line([(bx, int(H * 0.24)), (bx + 48 * s, int(H * 0.24))], fill=CREAM, width=s)
        d.line([(bx, int(H * 0.36)), (bx + 48 * s, int(H * 0.36))], fill=CREAM, width=s)
    
    # Main Writing Desk (perspective)
    desk_left, desk_right = int(W * 0.15), int(W * 0.88)
    desk_top, desk_bottom = int(H * 0.54), int(H * 0.80)
    d.polygon([
        (desk_left + 60 * s, desk_top),
        (desk_right - 40 * s, desk_top),
        (desk_right, desk_bottom),
        (desk_left, desk_bottom)
    ], fill=INK)
    # Desk legs
    d.rectangle([desk_left + 40 * s, desk_bottom, desk_left + 80 * s, H], fill=INK)
    d.rectangle([desk_right - 80 * s, desk_bottom, desk_right - 40 * s, H], fill=INK)
    
    # Architectural desk drafting lamp
    lamp_base_x = desk_left + 120 * s
    d.rectangle([lamp_base_x - 20 * s, desk_top - 8 * s, lamp_base_x + 20 * s, desk_top], fill=INK)
    d.line([(lamp_base_x, desk_top), (lamp_base_x - 30 * s, int(H * 0.34))], fill=INK, width=4 * s)
    d.line([(lamp_base_x - 30 * s, int(H * 0.34)), (lamp_base_x + 40 * s, int(H * 0.22))], fill=INK, width=4 * s)
    d.polygon([
        (lamp_base_x + 30 * s, int(H * 0.20)),
        (lamp_base_x + 80 * s, int(H * 0.18)),
        (lamp_base_x + 65 * s, int(H * 0.26)),
        (lamp_base_x + 20 * s, int(H * 0.25))
    ], fill=INK)
    
    # Tall Portrait Document Display (Center stage)
    mon_x1, mon_y1 = int(W * 0.34), int(H * 0.12)
    mon_x2, mon_y2 = int(W * 0.68), int(H * 0.54)
    d.polygon([(mon_x1, mon_y1), (mon_x2, mon_y1), (mon_x2 - 20 * s, mon_y2), (mon_x1 + 20 * s, mon_y2)], fill=INK)
    # Screen bezel cutout (Cream paper document on display)
    doc_x1, doc_y1 = mon_x1 + 18 * s, mon_y1 + 16 * s
    doc_x2, doc_y2 = mon_x2 - 18 * s, mon_y2 - 14 * s
    d.polygon([(doc_x1, doc_y1), (doc_x2, doc_y1), (doc_x2 - 15 * s, doc_y2), (doc_x1 + 15 * s, doc_y2)], fill=CREAM)
    
    # Word processor UI & Manuscript layout (Ink on Cream)
    # Ribbon header bar
    d.rectangle([doc_x1 + 10 * s, doc_y1 + 8 * s, doc_x2 - 10 * s, doc_y1 + 22 * s], fill=INK)
    # Horizontal page ruler
    d.line([(doc_x1 + 10 * s, doc_y1 + 30 * s), (doc_x2 - 10 * s, doc_y1 + 30 * s)], fill=INK, width=s)
    for rx in range(doc_x1 + 20 * s, doc_x2 - 20 * s, 20 * s):
        d.line([(rx, doc_y1 + 26 * s), (rx, doc_y1 + 30 * s)], fill=INK, width=s)
        
    # Multi-column manuscript text block lines
    col_w = (doc_x2 - doc_x1 - 60 * s) // 2
    for c in range(2):
        col_start_x = doc_x1 + 20 * s + c * (col_w + 20 * s)
        for ly in range(doc_y1 + 45 * s, doc_y2 - 40 * s, 16 * s):
            d.rectangle([col_start_x, ly, col_start_x + col_w, ly + 4 * s], fill=INK)
            
    # Bold Vermilion Red-Orange Accent 1: Active Cursor & Highlighted Text Revision Block
    rev_col_x = doc_x1 + 20 * s
    rev_y = doc_y1 + 45 * s + 16 * s * 3
    # Track-changes revision highlight in Vermilion
    d.rectangle([rev_col_x + 40 * s, rev_y - 3 * s, rev_col_x + col_w - 20 * s, rev_y + 7 * s], fill=VERM)
    # Tall active cursor in Vermilion
    d.rectangle([rev_col_x + col_w - 18 * s, rev_y - 8 * s, rev_col_x + col_w - 13 * s, rev_y + 12 * s], fill=VERM)
    
    # Bold Vermilion Red-Orange Accent 2: Proofreader margin annotation flag
    flag_x = doc_x2 - 38 * s
    d.polygon([
        (flag_x, rev_y - 6 * s),
        (flag_x + 28 * s, rev_y - 6 * s),
        (flag_x + 28 * s, rev_y + 10 * s),
        (flag_x, rev_y + 10 * s)
    ], fill=VERM)
    d.line([(rev_col_x + col_w - 13 * s, rev_y + 2 * s), (flag_x, rev_y + 2 * s)], fill=VERM, width=2 * s)
    
    # Stand for monitor
    d.rectangle([(mon_x1 + mon_x2) // 2 - 14 * s, mon_y2, (mon_x1 + mon_x2) // 2 + 14 * s, desk_top + 10 * s], fill=INK)
    
    # Ergonomic seated author silhouette on right side facing left
    author_x = int(W * 0.82)
    author_y = int(H * 0.38)
    # Chair backrest
    d.polygon([(author_x + 30 * s, int(H * 0.30)), (author_x + 60 * s, int(H * 0.30)), (author_x + 50 * s, int(H * 0.70)), (author_x + 20 * s, int(H * 0.70))], fill=INK)
    d.rectangle([author_x + 35 * s, int(H * 0.70), author_x + 45 * s, H], fill=INK)
    # Author
    draw_person_silhouette(d, author_x, author_y, facing_left=True, sitting=True)
    
    # Stack of manuscripts on desk corner
    stack_x = desk_right - 140 * s
    for sy in range(desk_top - 6 * s, desk_top - 36 * s, -8 * s):
        d.rectangle([stack_x, sy, stack_x + 80 * s, sy + 6 * s], fill=INK)
        
    # Resize with Lanczos to final resolution
    im_final = im.resize((W_FINAL, H_FINAL), Image.LANCZOS)
    im_final.save("demo-news/public/images/wordcraft-rust-word.jpg", quality=95)
    print("WordCraft illustration rendered successfully.")

if __name__ == "__main__":
    render_artcraft()
    render_wordcraft()
