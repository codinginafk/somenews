"""
Generate rich, high-fidelity editorial illustrations matching the exact clarity, depth,
and architectural storytelling of Rent Free News signature thumbnails.

Canvas: 1376x768 (rendered at 2x 2752x1536 with Lanczos downsampling)
Palette:
- Cream Paper Background: #F7F2E9  (247, 242, 233)
- Wireframe Grid:          #E2DAC9  (226, 218, 201)
- Grid Horizon/Accent:     #D4C9B5  (212, 201, 181)
- Solid Charcoal Ink:      #16130E  (22, 19, 14)
- Vermilion Red-Orange:    #C2410C  (194, 65, 12)
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

W_FINAL, H_FINAL = 1376, 768
SCALE = 2
W, H = W_FINAL * SCALE, H_FINAL * SCALE

CREAM = (247, 242, 233)
GRID = (226, 218, 201)
GRID_ACCENT = (212, 201, 181)
INK = (22, 19, 14)
VERM = (194, 65, 12)

def load_font(filename, pt_size):
    try:
        return ImageFont.truetype(f"C:/Windows/Fonts/{filename}", int(pt_size * SCALE))
    except Exception:
        try:
            return ImageFont.truetype("arial.ttf", int(pt_size * SCALE))
        except Exception:
            return ImageFont.load_default()

FONT_BANNER = load_font("segoeuib.ttf", 22)
FONT_TITLE = load_font("segoeuib.ttf", 16)
FONT_SUBTITLE = load_font("segoeuib.ttf", 13)
FONT_BODY = load_font("segoeui.ttf", 12)
FONT_CODE_BOLD = load_font("consolab.ttf", 13)
FONT_CODE = load_font("consola.ttf", 11)
FONT_TINY = load_font("consola.ttf", 9)
FONT_BADGE = load_font("segoeuib.ttf", 11)

def draw_perspective_grid(d, vp_x, vp_y, horizon_y, ray_spacing=90, floor_fill=None):
    s = SCALE
    d.rectangle([0, 0, W, H], fill=CREAM)
    
    # Wall background grid
    w_step = 60 * s
    for x in range(0, W, w_step):
        d.line([(x, 0), (x, horizon_y)], fill=GRID, width=s)
    for y in range(0, horizon_y, w_step):
        d.line([(0, y), (W, y)], fill=GRID, width=s)
        
    # Optional floor plane tone
    if floor_fill:
        d.polygon([(0, horizon_y), (W, horizon_y), (W, H), (0, H)], fill=floor_fill)
        
    # Horizon line
    d.line([(0, horizon_y), (W, horizon_y)], fill=GRID_ACCENT, width=2 * s)
    
    # Floor perspective rays converging to (vp_x, vp_y)
    for px in range(-W // 2, W * 2, ray_spacing * s):
        d.line([(vp_x, vp_y), (px, H)], fill=GRID, width=s)
        
    # Floor horizontal perspective rungs
    for t in [0.04, 0.09, 0.16, 0.25, 0.36, 0.50, 0.67, 0.86]:
        fy = int(horizon_y + (H - horizon_y) * t)
        d.line([(0, fy), (W, fy)], fill=GRID, width=s)

def draw_silhouette_standing(d, cx, cy, total_h=620, facing_left=True, arms_crossed=False, pointing=False):
    """Draw a realistic, anatomically proportioned human silhouette standing firm."""
    s = SCALE
    h = total_h
    w = int(h * 0.26)
    
    # Head & hair
    head_r = int(h * 0.075)
    head_cy = cy - int(h * 0.88)
    d.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r], fill=INK)
    # Facial profile
    p_dir = -1 if facing_left else 1
    d.polygon([
        (cx, head_cy - int(head_r * 0.4)),
        (cx + p_dir * (head_r + int(10 * s)), head_cy + int(2 * s)),
        (cx + p_dir * (head_r + int(4 * s)), head_cy + int(12 * s)),
        (cx, head_cy + int(head_r * 0.6))
    ], fill=INK)
    
    # Neck & collar
    neck_w = int(head_r * 0.5)
    neck_top = head_cy + head_r - int(4 * s)
    neck_bottom = neck_top + int(22 * s)
    d.polygon([
        (cx - neck_w, neck_top),
        (cx + neck_w, neck_top),
        (cx + neck_w + int(8 * s), neck_bottom),
        (cx - neck_w - int(8 * s), neck_bottom)
    ], fill=INK)
    
    # Torso (Suit jacket / coat)
    torso_top = neck_bottom
    torso_bottom = cy - int(h * 0.46)
    sh_w = int(w * 0.58)
    waist_w = int(w * 0.44)
    d.polygon([
        (cx - sh_w, torso_top + int(14 * s)),
        (cx + sh_w, torso_top + int(14 * s)),
        (cx + waist_w, torso_bottom),
        (cx - waist_w, torso_bottom)
    ], fill=INK)
    # Shoulder curves
    d.ellipse([cx - sh_w - int(6 * s), torso_top, cx - sh_w + int(20 * s), torso_top + int(36 * s)], fill=INK)
    d.ellipse([cx + sh_w - int(20 * s), torso_top, cx + sh_w + int(6 * s), torso_top + int(36 * s)], fill=INK)
    
    # Legs (Pants & shoes)
    leg_w = int(w * 0.20)
    leg_gap = int(w * 0.05)
    # Left leg
    d.polygon([
        (cx - waist_w + int(4 * s), torso_bottom),
        (cx - leg_gap, torso_bottom),
        (cx - leg_gap - int(6 * s), cy - int(12 * s)),
        (cx - waist_w - int(4 * s), cy - int(12 * s))
    ], fill=INK)
    # Right leg
    d.polygon([
        (cx + leg_gap, torso_bottom),
        (cx + waist_w - int(4 * s), torso_bottom),
        (cx + waist_w + int(4 * s), cy - int(12 * s)),
        (cx + leg_gap + int(6 * s), cy - int(12 * s))
    ], fill=INK)
    # Shoes
    shoe_len = int(w * 0.32)
    s_dir = -shoe_len if facing_left else shoe_len
    d.polygon([(cx - waist_w - int(4 * s), cy - int(12 * s)), (cx - waist_w + s_dir, cy), (cx - leg_gap, cy)], fill=INK)
    d.polygon([(cx + leg_gap, cy - int(12 * s)), (cx + waist_w + s_dir, cy), (cx + waist_w + int(4 * s), cy)], fill=INK)
    
    # Arms
    if arms_crossed:
        d.ellipse([cx - sh_w + int(6 * s), torso_top + int(30 * s), cx + sh_w - int(6 * s), torso_top + int(100 * s)], fill=INK)
    elif pointing:
        arm_end_x = cx - int(w * 1.4) if facing_left else cx + int(w * 1.4)
        d.polygon([
            (cx - sh_w + int(10 * s), torso_top + int(18 * s)),
            (arm_end_x, torso_top - int(30 * s)),
            (arm_end_x, torso_top + int(2 * s)),
            (cx - sh_w + int(10 * s), torso_top + int(50 * s))
        ], fill=INK)
    else:
        # Arms resting along sides
        d.polygon([
            (cx - sh_w, torso_top + int(18 * s)),
            (cx - sh_w + int(20 * s), torso_top + int(18 * s)),
            (cx - waist_w + int(8 * s), torso_bottom + int(30 * s)),
            (cx - waist_w - int(12 * s), torso_bottom + int(30 * s))
        ], fill=INK)
        d.polygon([
            (cx + sh_w - int(20 * s), torso_top + int(18 * s)),
            (cx + sh_w, torso_top + int(18 * s)),
            (cx + waist_w + int(12 * s), torso_bottom + int(30 * s)),
            (cx + waist_w - int(8 * s), torso_bottom + int(30 * s))
        ], fill=INK)

def draw_silhouette_walking(d, cx, cy, total_h=620, facing_left=True):
    """Draw a realistic walking human silhouette with natural dynamic stride."""
    s = SCALE
    h = total_h
    w = int(h * 0.28)
    p_dir = -1 if facing_left else 1
    
    # Head & hair
    head_r = int(h * 0.075)
    head_cy = cy - int(h * 0.89)
    d.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r], fill=INK)
    # Nose & chin profile
    d.polygon([
        (cx, head_cy - int(head_r * 0.4)),
        (cx + p_dir * (head_r + int(10 * s)), head_cy + int(2 * s)),
        (cx + p_dir * (head_r + int(4 * s)), head_cy + int(12 * s)),
        (cx, head_cy + int(head_r * 0.6))
    ], fill=INK)
    
    # Neck
    neck_top = head_cy + head_r - int(4 * s)
    neck_bottom = neck_top + int(20 * s)
    d.polygon([
        (cx - int(head_r * 0.4), neck_top),
        (cx + int(head_r * 0.4), neck_top),
        (cx + int(head_r * 0.6), neck_bottom),
        (cx - int(head_r * 0.6), neck_bottom)
    ], fill=INK)
    
    # Torso (Leaning slightly into the stride)
    torso_top = neck_bottom
    torso_bottom = cy - int(h * 0.46)
    sh_w = int(w * 0.54)
    waist_w = int(w * 0.40)
    lean = p_dir * int(14 * s)
    d.polygon([
        (cx - sh_w + lean, torso_top),
        (cx + sh_w + lean, torso_top),
        (cx + waist_w, torso_bottom),
        (cx - waist_w, torso_bottom)
    ], fill=INK)
    
    # Dynamic Striding Legs
    stride_f = p_dir * int(w * 0.45)
    stride_b = -p_dir * int(w * 0.40)
    
    # Front leg
    d.polygon([
        (cx + lean, torso_bottom),
        (cx + lean + int(18 * s), torso_bottom),
        (cx + stride_f + int(20 * s), cy - int(10 * s)),
        (cx + stride_f - int(10 * s), cy - int(10 * s))
    ], fill=INK)
    # Front shoe planted
    d.polygon([
        (cx + stride_f - int(10 * s), cy - int(14 * s)),
        (cx + stride_f + p_dir * int(40 * s), cy),
        (cx + stride_f + int(20 * s), cy)
    ], fill=INK)
    
    # Back leg
    d.polygon([
        (cx - lean, torso_bottom),
        (cx - lean - int(18 * s), torso_bottom),
        (cx + stride_b + int(16 * s), cy - int(24 * s)),
        (cx + stride_b - int(10 * s), cy - int(24 * s))
    ], fill=INK)
    # Back shoe angled off the ground
    d.polygon([
        (cx + stride_b - int(10 * s), cy - int(26 * s)),
        (cx + stride_b + p_dir * int(34 * s), cy - int(12 * s)),
        (cx + stride_b + int(16 * s), cy - int(24 * s))
    ], fill=INK)
    
    # Swinging Arms
    # Forward arm
    arm_f = p_dir * int(w * 0.35)
    d.polygon([
        (cx + lean, torso_top + int(15 * s)),
        (cx + lean + int(16 * s), torso_top + int(15 * s)),
        (cx + arm_f + int(14 * s), torso_bottom + int(20 * s)),
        (cx + arm_f, torso_bottom + int(20 * s))
    ], fill=INK)
    # Back arm
    arm_b = -p_dir * int(w * 0.30)
    d.polygon([
        (cx - lean, torso_top + int(15 * s)),
        (cx - lean - int(16 * s), torso_top + int(15 * s)),
        (cx + arm_b - int(12 * s), torso_bottom + int(10 * s)),
        (cx + arm_b, torso_bottom + int(10 * s))
    ], fill=INK)

def draw_silhouette_seated(d, cx, cy, total_h=580, facing_left=True):
    """Draw a developer/writer seated at a desk typing."""
    s = SCALE
    h = total_h
    w = int(h * 0.32)
    p_dir = -1 if facing_left else 1
    
    # Head & hair
    head_r = int(h * 0.08)
    head_cy = cy - int(h * 0.65)
    d.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r], fill=INK)
    # Profile
    d.polygon([
        (cx, head_cy - int(head_r * 0.4)),
        (cx + p_dir * (head_r + int(10 * s)), head_cy + int(2 * s)),
        (cx + p_dir * (head_r + int(4 * s)), head_cy + int(12 * s)),
        (cx, head_cy + int(head_r * 0.6))
    ], fill=INK)
    
    # Torso leaning forward toward desk
    torso_top = head_cy + head_r + int(6 * s)
    torso_bottom = cy - int(h * 0.18)
    sh_w = int(w * 0.50)
    lean = p_dir * int(22 * s)
    d.polygon([
        (cx - sh_w + lean, torso_top),
        (cx + sh_w + lean, torso_top),
        (cx + int(sh_w * 0.7), torso_bottom),
        (cx - int(sh_w * 0.7), torso_bottom)
    ], fill=INK)
    
    # Seated thighs
    thigh_start_x = cx + p_dir * int(15 * s)
    thigh_end_x = thigh_start_x + p_dir * int(w * 0.75)
    thigh_y = torso_bottom + int(10 * s)
    d.polygon([
        (thigh_start_x, torso_bottom - int(15 * s)),
        (thigh_start_x - p_dir * int(40 * s), torso_bottom - int(15 * s)),
        (thigh_end_x, thigh_y + int(30 * s)),
        (thigh_end_x + p_dir * int(20 * s), thigh_y + int(50 * s)),
        (thigh_start_x, torso_bottom + int(40 * s))
    ], fill=INK)
    
    # Lower legs
    shin_x = thigh_end_x + p_dir * int(10 * s)
    shin_bottom = cy + int(h * 0.28)
    d.rectangle([shin_x - int(14 * s), thigh_y + int(40 * s), shin_x + int(14 * s), shin_bottom], fill=INK)
    # Shoe
    d.polygon([(shin_x - int(14 * s), shin_bottom - int(10 * s)), (shin_x + p_dir * int(45 * s), shin_bottom), (shin_x + int(14 * s), shin_bottom)], fill=INK)
    
    # Reaching arms
    arm_start_x = cx + lean
    arm_end_x = arm_start_x + p_dir * int(w * 0.85)
    elbow_x = arm_start_x + p_dir * int(w * 0.45)
    d.polygon([
        (arm_start_x, torso_top + int(15 * s)),
        (elbow_x, torso_top + int(70 * s)),
        (arm_end_x, torso_top + int(90 * s)),
        (arm_end_x, torso_top + int(110 * s)),
        (elbow_x + p_dir * int(15 * s), torso_top + int(90 * s)),
        (arm_start_x + p_dir * int(20 * s), torso_top + int(25 * s))
    ], fill=INK)


# ==============================================================================
# 1. RUVIEW: WI-FI SPATIAL INTELLIGENCE & CAMERA-FREE VITAL SIGNS
# ==============================================================================
def generate_ruview():
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    s = SCALE
    
    vp_x, vp_y = int(W * 0.48), int(H * 0.38)
    horizon_y = int(H * 0.60)
    draw_perspective_grid(d, vp_x, vp_y, horizon_y, ray_spacing=80)
    
    # Central Partition Wall: Structural cross-section dividing the 2 rooms
    wall_x1 = int(W * 0.44)
    wall_x2 = int(W * 0.50)
    d.rectangle([wall_x1, 0, wall_x2, H], fill=INK)
    
    # Detailed wall stud cutaways with insulation bracing
    for sy in range(int(50 * s), int(H * 0.90), int(140 * s)):
        d.rectangle([wall_x1 + 10 * s, sy, wall_x2 - 10 * s, sy + 100 * s], fill=CREAM)
        d.line([(wall_x1 + 10 * s, sy), (wall_x2 - 10 * s, sy + 100 * s)], fill=GRID_ACCENT, width=2 * s)
        d.line([(wall_x1 + 10 * s, sy + 100 * s), (wall_x2 - 10 * s, sy)], fill=GRID_ACCENT, width=2 * s)
        d.rectangle([wall_x1 + 8 * s, sy, wall_x2 - 8 * s, sy + 100 * s], outline=INK, width=2 * s)
        
    # LEFT ROOM: SENSING STATION
    # Window with exterior city grid
    win_x1, win_y1, win_x2, win_y2 = int(W * 0.03), int(H * 0.10), int(W * 0.16), int(H * 0.52)
    d.polygon([(win_x1, win_y1), (win_x2, win_y1 + 25 * s), (win_x2, win_y2 - 25 * s), (win_x1, win_y2)], fill=INK)
    d.polygon([(win_x1 + 6 * s, win_y1 + 6 * s), (win_x2 - 6 * s, win_y1 + 30 * s), (win_x2 - 6 * s, win_y2 - 30 * s), (win_x1 + 6 * s, win_y2 - 6 * s)], fill=CREAM)
    d.line([(win_x1 + 6 * s, (win_y1 + win_y2) // 2), (win_x2 - 6 * s, (win_y1 + win_y2) // 2)], fill=INK, width=3 * s)
    d.line([((win_x1 + win_x2) // 2, win_y1 + 20 * s), ((win_x1 + win_x2) // 2, win_y2 - 20 * s)], fill=INK, width=3 * s)
    
    # Credenza / Console Table in Left Room
    c_x1, c_y1 = int(W * 0.12), int(H * 0.50)
    c_x2, c_y2 = int(W * 0.40), int(H * 0.74)
    d.polygon([(c_x1, c_y1), (c_x2, c_y1 + 15 * s), (c_x2, c_y2), (c_x1, c_y2 - 15 * s)], fill=INK)
    d.rectangle([c_x1 + 20 * s, c_y2 - 15 * s, c_x1 + 35 * s, int(H * 0.92)], fill=INK)
    d.rectangle([c_x2 - 35 * s, c_y2, c_x2 - 20 * s, int(H * 0.94)], fill=INK)
    
    # Wi-Fi Router Hardware
    r_cx, r_cy = int(W * 0.28), c_y1 - 10 * s
    r_w, r_h = 70 * s, 22 * s
    d.rectangle([r_cx - r_w, r_cy - r_h, r_cx + r_w, r_cy], fill=INK)
    # Dual Dipole Antennas
    d.line([(r_cx - 45 * s, r_cy - r_h), (r_cx - 65 * s, r_cy - 90 * s)], fill=INK, width=5 * s)
    d.line([(r_cx + 45 * s, r_cy - r_h), (r_cx + 65 * s, r_cy - 90 * s)], fill=INK, width=5 * s)
    for lx in range(r_cx - 40 * s, r_cx + 40 * s, 16 * s):
        d.rectangle([lx, r_cy - 14 * s, lx + 6 * s, r_cy - 8 * s], fill=CREAM)
        
    # Bookshelf / Hardware Rack above credenza
    d.rectangle([int(W * 0.20), int(H * 0.16), int(W * 0.38), int(H * 0.34)], fill=INK)
    d.rectangle([int(W * 0.21), int(H * 0.18), int(W * 0.37), int(H * 0.32)], fill=CREAM)
    # Books and hardware slots
    for bx in range(int(W * 0.22), int(W * 0.36), int(18 * s)):
        d.rectangle([bx, int(H * 0.20), bx + 12 * s, int(H * 0.31)], fill=INK)
        
    # Concentric CSI Phase Waves Radiating Across Wall
    orig_x, orig_y = r_cx + 60 * s, r_cy - 70 * s
    for r in range(int(120 * s), int(760 * s), int(70 * s)):
        bbox = [orig_x - r, orig_y - r, orig_x + r, orig_y + r]
        d.arc(bbox, start=-38, end=38, fill=INK, width=2 * s)
        
    # Bold Vermilion Red-Orange CSI Wavefront passing through the wall
    active_r = int(480 * s)
    d.arc([orig_x - active_r, orig_y - active_r, orig_x + active_r, orig_y + active_r], start=-34, end=34, fill=VERM, width=5 * s)
    # Router transmission pulse
    d.ellipse([r_cx + 42 * s, r_cy - 16 * s, r_cx + 52 * s, r_cy - 6 * s], fill=VERM)
    d.line([(r_cx + 58 * s, r_cy - 88 * s), (r_cx + 72 * s, r_cy - 94 * s)], fill=VERM, width=4 * s)
    
    # RIGHT ROOM: CONCEALED SUBJECT (Zero cameras)
    # Interior props: Floor reading lamp
    lamp_x = int(W * 0.92)
    d.line([(lamp_x, int(H * 0.22)), (lamp_x, int(H * 0.76))], fill=INK, width=4 * s)
    d.polygon([(lamp_x - 35 * s, int(H * 0.22)), (lamp_x + 35 * s, int(H * 0.22)), (lamp_x + 50 * s, int(H * 0.32)), (lamp_x - 50 * s, int(H * 0.32))], fill=INK)
    d.ellipse([lamp_x - 40 * s, int(H * 0.74), lamp_x + 40 * s, int(H * 0.78)], fill=INK)
    
    # Modern armchair on far right
    chair_x = int(W * 0.78)
    chair_y = int(H * 0.62)
    d.polygon([(chair_x, chair_y), (chair_x + 130 * s, chair_y - 30 * s), (chair_x + 180 * s, chair_y + 60 * s), (chair_x + 40 * s, chair_y + 90 * s)], fill=INK)
    d.rectangle([chair_x + 40 * s, chair_y - 70 * s, chair_x + 150 * s, chair_y], fill=INK)
    
    # FULL-SIZE WALKING HUMAN SILHOUETTE (Mid-stride, concealed behind wall)
    walker_cx = int(W * 0.66)
    walker_cy = int(H * 0.86)
    draw_silhouette_walking(d, walker_cx, walker_cy, total_h=int(330 * s), facing_left=True)
    
    # Bold Vermilion Red-Orange Vital Sign Targeting Reticle & ECG Respiration Banner
    chest_x = walker_cx - int(24 * s)
    chest_y = walker_cy - int(210 * s)
    ret_r = int(48 * s)
    
    # Reticle outer ticks
    d.line([(chest_x - ret_r - 25 * s, chest_y), (chest_x + ret_r + 25 * s, chest_y)], fill=VERM, width=3 * s)
    d.line([(chest_x, chest_y - ret_r - 25 * s), (chest_x, chest_y + ret_r + 25 * s)], fill=VERM, width=3 * s)
    # Circular corner brackets
    d.arc([chest_x - ret_r, chest_y - ret_r, chest_x + ret_r, chest_y + ret_r], start=25, end=65, fill=VERM, width=4 * s)
    d.arc([chest_x - ret_r, chest_y - ret_r, chest_x + ret_r, chest_y + ret_r], start=115, end=155, fill=VERM, width=4 * s)
    d.arc([chest_x - ret_r, chest_y - ret_r, chest_x + ret_r, chest_y + ret_r], start=205, end=245, fill=VERM, width=4 * s)
    d.arc([chest_x - ret_r, chest_y - ret_r, chest_x + ret_r, chest_y + ret_r], start=295, end=335, fill=VERM, width=4 * s)
    
    # Micro-Doppler Cardiac Waveform Display Card
    card_x1 = chest_x + int(60 * s)
    card_y1 = chest_y - int(45 * s)
    card_w, card_h = int(210 * s), int(85 * s)
    d.rectangle([card_x1, card_y1, card_x1 + card_w, card_y1 + card_h], fill=CREAM, outline=VERM, width=3 * s)
    d.rectangle([card_x1, card_y1, card_x1 + card_w, card_y1 + 22 * s], fill=VERM)
    d.text((card_x1 + 10 * s, card_y1 + 3 * s), "MICRO-DOPPLER RADAR // RUST", fill=CREAM, font=FONT_TINY)
    
    # Heartbeat & respiration ECG wave line in Vermilion
    pts = [
        (card_x1 + 10 * s, card_y1 + 54 * s),
        (card_x1 + 45 * s, card_y1 + 54 * s),
        (card_x1 + 55 * s, card_y1 + 38 * s),
        (card_x1 + 65 * s, card_y1 + 72 * s),
        (card_x1 + 75 * s, card_y1 + 24 * s),
        (card_x1 + 85 * s, card_y1 + 76 * s),
        (card_x1 + 95 * s, card_y1 + 54 * s),
        (card_x1 + 135 * s, card_y1 + 54 * s),
        (card_x1 + 145 * s, card_y1 + 40 * s),
        (card_x1 + 155 * s, card_y1 + 70 * s),
        (card_x1 + 165 * s, card_y1 + 26 * s),
        (card_x1 + 175 * s, card_y1 + 74 * s),
        (card_x1 + 185 * s, card_y1 + 54 * s),
        (card_x1 + card_w - 10 * s, card_y1 + 54 * s)
    ]
    d.line(pts, fill=VERM, width=3 * s)
    d.text((card_x1 + 10 * s, card_y1 + card_h - 18 * s), "PULSE: 72 BPM // RESP: 16 BRPM", fill=INK, font=FONT_TINY)
    
    # Top Headline Banner
    d.rectangle([int(W * 0.05), int(H * 0.04), int(W * 0.42), int(H * 0.09)], fill=INK)
    d.text((int(W * 0.06), int(H * 0.05)), "SPATIAL INTELLIGENCE WITHOUT CAMERAS // RUVIEW", fill=CREAM, font=FONT_BADGE)
    
    im_final = im.resize((W_FINAL, H_FINAL), Image.LANCZOS)
    im_final.save("demo-news/public/images/ruview-rust-wifi-spatial-intelligence.jpg", quality=95)
    print("RuView rich thumbnail generated.")


# ==============================================================================
# 2. XIAOLAI: THE CRAFT OF SELF-TEACHING (PROOF-OF-WORK JUPYTER & GIT DAG)
# ==============================================================================
def generate_xiaolai():
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    s = SCALE
    
    vp_x, vp_y = int(W * 0.36), int(H * 0.40)
    horizon_y = int(H * 0.58)
    draw_perspective_grid(d, vp_x, vp_y, horizon_y, ray_spacing=80)
    
    # Massive Main Workstation Desk (Perspective wood slab)
    desk_left, desk_right = int(W * 0.06), int(W * 0.56)
    desk_top, desk_bottom = int(H * 0.52), int(H * 0.76)
    d.polygon([(desk_left + 50 * s, desk_top), (desk_right - 30 * s, desk_top), (desk_right, desk_bottom), (desk_left, desk_bottom)], fill=INK)
    # Sturdy desk legs
    d.rectangle([desk_left + 40 * s, desk_bottom, desk_left + 65 * s, H], fill=INK)
    d.rectangle([desk_right - 65 * s, desk_bottom, desk_right - 40 * s, H], fill=INK)
    
    # Articulated Desk Lamp
    lamp_x = desk_left + 100 * s
    d.rectangle([lamp_x - 15 * s, desk_top - 10 * s, lamp_x + 15 * s, desk_top], fill=INK)
    d.line([(lamp_x, desk_top), (lamp_x - 30 * s, int(H * 0.34))], fill=INK, width=5 * s)
    d.line([(lamp_x - 30 * s, int(H * 0.34)), (lamp_x + 40 * s, int(H * 0.22))], fill=INK, width=5 * s)
    d.polygon([(lamp_x + 30 * s, int(H * 0.20)), (lamp_x + 80 * s, int(H * 0.18)), (lamp_x + 70 * s, int(H * 0.26)), (lamp_x + 20 * s, int(H * 0.24))], fill=INK)
    
    # Stacked Textbooks on Desk Corner
    stack_x = desk_left + 150 * s
    for by in range(int(desk_top - 8 * s), int(desk_top - 48 * s), -int(12 * s)):
        d.rectangle([stack_x, by, stack_x + 90 * s, by + 10 * s], fill=INK)
        d.rectangle([stack_x + 8 * s, by + 2 * s, stack_x + 82 * s, by + 8 * s], fill=CREAM)
        
    # Ultrawide Curved Curved Display on Articulated Arm
    mon_x1, mon_y1 = int(W * 0.12), int(H * 0.14)
    mon_x2, mon_y2 = int(W * 0.50), int(H * 0.52)
    d.polygon([(mon_x1, mon_y1), (mon_x2, mon_y1), (mon_x2 - 18 * s, mon_y2), (mon_x1 + 18 * s, mon_y2)], fill=INK)
    # Screen inner cutout
    sc_x1, sc_y1 = mon_x1 + 14 * s, mon_y1 + 12 * s
    sc_x2, sc_y2 = mon_x2 - 14 * s, mon_y2 - 12 * s
    d.polygon([(sc_x1, sc_y1), (sc_x2, sc_y1), (sc_x2 - 14 * s, sc_y2), (sc_x1 + 14 * s, sc_y2)], fill=CREAM)
    
    # Jupyter Notebook Layout on screen
    d.rectangle([sc_x1 + 8 * s, sc_y1 + 6 * s, sc_x2 - 8 * s, sc_y1 + 26 * s], fill=INK)
    d.text((sc_x1 + 16 * s, sc_y1 + 9 * s), "JupyterLab - the-craft-of-selfteaching.ipynb [Python 3.12]", fill=CREAM, font=FONT_TINY)
    
    # Code Cell 1
    c1_y = sc_y1 + 35 * s
    d.rectangle([sc_x1 + 12 * s, c1_y, sc_x2 - 12 * s, c1_y + 45 * s], outline=INK, width=s)
    d.text((sc_x1 + 18 * s, c1_y + 5 * s), "[In 1]:", fill=GRID_ACCENT, font=FONT_TINY)
    d.text((sc_x1 + 65 * s, c1_y + 5 * s), "def proof_of_work(commit_hash, nonce=0):", fill=INK, font=FONT_CODE_BOLD)
    d.text((sc_x1 + 65 * s, c1_y + 22 * s), "    return sha256(f'{commit_hash}:{nonce}').hexdigest()", fill=INK, font=FONT_CODE)
    
    # Code Cell 2 (Active execution)
    c2_y = c1_y + 55 * s
    d.rectangle([sc_x1 + 12 * s, c2_y, sc_x2 - 12 * s, c2_y + 65 * s], outline=INK, width=s)
    d.text((sc_x1 + 18 * s, c2_y + 5 * s), "[In 2]:", fill=GRID_ACCENT, font=FONT_TINY)
    d.text((sc_x1 + 65 * s, c2_y + 5 * s), "# Verifying local git progress against curriculum", fill=GRID_ACCENT, font=FONT_CODE)
    d.text((sc_x1 + 65 * s, c2_y + 22 * s), "verify_learner_commits(repo='xiaolai/craft')", fill=INK, font=FONT_CODE_BOLD)
    d.text((sc_x1 + 65 * s, c2_y + 40 * s), ">> 42 Chapters Completed. Proof-of-Work: Valid.", fill=INK, font=FONT_CODE)
    
    # Bold Vermilion Red-Orange Running Indicator on Notebook
    d.rectangle([sc_x1 + 12 * s, c2_y, sc_x1 + 18 * s, c2_y + 65 * s], fill=VERM)
    d.text((sc_x2 - 100 * s, c2_y + 5 * s), "[EXEC *]", fill=VERM, font=FONT_CODE_BOLD)
    
    # Monitor heavy aluminum stand
    d.rectangle([(mon_x1 + mon_x2) // 2 - 15 * s, mon_y2, (mon_x1 + mon_x2) // 2 + 15 * s, desk_top + 10 * s], fill=INK)
    d.polygon([
        ((mon_x1 + mon_x2) // 2 - 45 * s, desk_top + 10 * s),
        ((mon_x1 + mon_x2) // 2 + 45 * s, desk_top + 10 * s),
        ((mon_x1 + mon_x2) // 2 + 55 * s, desk_top + 18 * s),
        ((mon_x1 + mon_x2) // 2 - 55 * s, desk_top + 18 * s)
    ], fill=INK)
    
    # FULL SEATED DEVELOPER SILHOUETTE
    dev_cx = int(W * 0.44)
    dev_cy = int(H * 0.52)
    # Ergonomic office chair
    d.polygon([(dev_cx + 40 * s, int(H * 0.38)), (dev_cx + 75 * s, int(H * 0.38)), (dev_cx + 60 * s, int(H * 0.74)), (dev_cx + 25 * s, int(H * 0.74))], fill=INK)
    d.rectangle([dev_cx + 45 * s, int(H * 0.74), dev_cx + 55 * s, int(H * 0.90)], fill=INK)
    d.line([(dev_cx + 15 * s, int(H * 0.90)), (dev_cx + 85 * s, int(H * 0.90))], fill=INK, width=6 * s)
    draw_silhouette_seated(d, dev_cx, dev_cy, total_h=int(280 * s), facing_left=True)
    
    # RIGHT BACKGROUND: MASSIVE WALL-MOUNTED PROOF-OF-WORK GIT DAG DISPLAY
    dag_x1, dag_y1 = int(W * 0.58), int(H * 0.08)
    dag_x2, dag_y2 = int(W * 0.96), int(H * 0.78)
    d.rectangle([dag_x1, dag_y1, dag_x2, dag_y2], fill=CREAM, outline=INK, width=3 * s)
    d.rectangle([dag_x1, dag_y1, dag_x2, dag_y1 + 32 * s], fill=INK)
    d.text((dag_x1 + 18 * s, dag_y1 + 8 * s), "GIT COMMIT PROOF-OF-WORK GRAPH // 18.5k STARS // 17.9k FORKS", fill=CREAM, font=FONT_TITLE)
    
    # Trunk nodes
    trunk = [
        (dag_x1 + 70 * s, dag_y2 - 70 * s, "init: 0.1"),
        (dag_x1 + 140 * s, dag_y2 - 140 * s, "ch01: f82a"),
        (dag_x1 + 210 * s, dag_y2 - 210 * s, "ch02: c31b"),
        (dag_x1 + 280 * s, dag_y2 - 280 * s, "ch03: 7a9e"),
        (dag_x1 + 350 * s, dag_y2 - 350 * s, "ch04: d401"),
        (dag_x1 + 420 * s, dag_y2 - 420 * s, "HEAD: v2.0")
    ]
    for i in range(len(trunk) - 1):
        d.line([(trunk[i][0], trunk[i][1]), (trunk[i+1][0], trunk[i+1][1])], fill=INK, width=4 * s)
        
    # Feature Branches
    fork1 = [(trunk[1][0], trunk[1][1]), (trunk[1][0] + 70 * s, trunk[1][1] - 50 * s), (trunk[3][0], trunk[3][1])]
    d.line([fork1[0], fork1[1], fork1[2]], fill=INK, width=3 * s)
    
    fork2 = [(trunk[2][0], trunk[2][1]), (trunk[2][0] + 90 * s, trunk[2][1] - 40 * s), (trunk[4][0], trunk[4][1])]
    d.line([fork2[0], fork2[1], fork2[2]], fill=INK, width=3 * s)
    
    # Draw trunk nodes
    for x, y, lbl in trunk[:-1]:
        d.ellipse([x - 12 * s, y - 12 * s, x + 12 * s, y + 12 * s], fill=INK)
        d.text((x + 18 * s, y - 10 * s), lbl, fill=INK, font=FONT_TINY)
    d.ellipse([fork1[1][0] - 10 * s, fork1[1][1] - 10 * s, fork1[1][0] + 10 * s, fork1[1][1] + 10 * s], fill=INK)
    d.ellipse([fork2[1][0] - 10 * s, fork2[1][0] - 10 * s, fork2[1][0] + 10 * s, fork2[1][1] + 10 * s], fill=INK)
    
    # Bold Vermilion Red-Orange Summit HEAD Commit Node & PoW Verified Badge
    head_x, head_y, _ = trunk[-1]
    d.ellipse([head_x - 20 * s, head_y - 20 * s, head_x + 20 * s, head_y + 20 * s], fill=VERM)
    d.ellipse([head_x - 10 * s, head_y - 10 * s, head_x + 10 * s, head_y + 10 * s], fill=CREAM)
    
    # Summit PoW Badge in Vermilion
    flag_x = head_x + 28 * s
    d.polygon([(flag_x, head_y - 18 * s), (flag_x + 130 * s, head_y - 18 * s), (flag_x + 130 * s, head_y + 18 * s), (flag_x, head_y + 18 * s)], fill=VERM)
    d.text((flag_x + 10 * s, head_y - 10 * s), "HEAD -> v2.0 [POW]", fill=CREAM, font=FONT_CODE_BOLD)
    
    # Git terminal log below DAG on board
    log_y = dag_y2 - 60 * s
    d.rectangle([dag_x1 + 20 * s, log_y, dag_x2 - 20 * s, dag_y2 - 15 * s], fill=INK)
    d.text((dag_x1 + 30 * s, log_y + 10 * s), "$ git commit -am 'Proof of Work: Verified executable notebook'", fill=CREAM, font=FONT_TINY)
    d.text((dag_x1 + 30 * s, log_y + 25 * s), "[main a8f2d] 17,900 forks synced. Curriculum complete.", fill=GRID_ACCENT, font=FONT_TINY)
    
    im_final = im.resize((W_FINAL, H_FINAL), Image.LANCZOS)
    im_final.save("demo-news/public/images/xiaolai-craft-of-selfteaching.jpg", quality=95)
    print("Xiaolai rich thumbnail generated.")


# ==============================================================================
# 3. EXPO SKILLS: AI AGENT NATIVE UI (4-STATE ARCHITECTURE & ROBOTIC ASSEMBLY)
# ==============================================================================
def generate_expo_skills():
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    s = SCALE
    
    vp_x, vp_y = int(W * 0.50), int(H * 0.36)
    horizon_y = int(H * 0.60)
    draw_perspective_grid(d, vp_x, vp_y, horizon_y, ray_spacing=80)
    
    # Background Wall: Large Blueprint Board "4-STATE NATIVE ARCHITECTURE"
    bp_x1, bp_y1 = int(W * 0.06), int(H * 0.08)
    bp_x2, bp_y2 = int(W * 0.94), int(H * 0.44)
    d.rectangle([bp_x1, bp_y1, bp_x2, bp_y2], fill=CREAM, outline=INK, width=3 * s)
    d.rectangle([bp_x1, bp_y1, bp_x2, bp_y1 + 30 * s], fill=INK)
    d.text((bp_x1 + 18 * s, bp_y1 + 7 * s), "EXPO/SKILLS SPECIFICATION: NATIVE UI 4-STATE ARCHITECTURE", fill=CREAM, font=FONT_TITLE)
    
    # 4 Architecture Cards
    card_w = (bp_x2 - bp_x1 - 50 * s) // 4
    for idx, title in enumerate(["01. LOADING", "02. EMPTY", "03. ERROR", "04. CONTENT"]):
        cx1 = bp_x1 + 10 * s + idx * (card_w + 10 * s)
        cy1 = bp_y1 + 42 * s
        cx2 = cx1 + card_w
        cy2 = bp_y2 - 16 * s
        d.rectangle([cx1, cy1, cx2, cy2], fill=CREAM, outline=GRID_ACCENT, width=s)
        if idx == 3:
            # Active state
            d.rectangle([cx1, cy1, cx2, cy1 + 22 * s], fill=VERM)
            d.text((cx1 + 8 * s, cy1 + 4 * s), title, fill=CREAM, font=FONT_BADGE)
            d.rectangle([cx1 + 10 * s, cy1 + 32 * s, cx2 - 10 * s, cy1 + 54 * s], fill=INK)
            d.rectangle([cx1 + 10 * s, cy1 + 60 * s, cx2 - 10 * s, cy1 + 82 * s], fill=INK)
        else:
            d.rectangle([cx1, cy1, cx2, cy1 + 22 * s], fill=INK)
            d.text((cx1 + 8 * s, cy1 + 4 * s), title, fill=CREAM, font=FONT_TINY)
            if idx == 0:
                d.rectangle([cx1 + 12 * s, cy1 + 35 * s, cx2 - 12 * s, cy1 + 48 * s], fill=GRID_ACCENT)
                d.rectangle([cx1 + 12 * s, cy1 + 56 * s, cx2 - 30 * s, cy1 + 68 * s], fill=GRID_ACCENT)
            elif idx == 1:
                d.rectangle([cx1 + 15 * s, cy1 + 35 * s, cx2 - 15 * s, cy2 - 20 * s], outline=GRID_ACCENT, width=s)
            elif idx == 2:
                tx = (cx1 + cx2) // 2
                d.polygon([(tx, cy1 + 35 * s), (tx + 22 * s, cy2 - 20 * s), (tx - 22 * s, cy2 - 20 * s)], outline=INK, width=2 * s)
                
    # Center Stage: Precision Smartphone Plinth & Hardware
    phone_cx = int(W * 0.45)
    phone_w, phone_h = 140 * s, 280 * s
    phone_top = int(H * 0.40)
    phone_bottom = phone_top + phone_h
    
    # Plinth base
    d.polygon([
        (phone_cx - 120 * s, phone_bottom + 45 * s),
        (phone_cx + 120 * s, phone_bottom + 45 * s),
        (phone_cx + 160 * s, int(H * 0.92)),
        (phone_cx - 160 * s, int(H * 0.92))
    ], fill=INK)
    d.rectangle([phone_cx - 35 * s, phone_bottom, phone_cx + 35 * s, phone_bottom + 50 * s], fill=INK)
    
    # Phone Body
    d.rectangle([phone_cx - phone_w, phone_top, phone_cx + phone_w, phone_bottom], fill=INK)
    sc_w, sc_h = phone_w - 14 * s, phone_h - 16 * s
    sc_x1, sc_y1 = phone_cx - sc_w, phone_top + 12 * s
    sc_x2, sc_y2 = phone_cx + sc_w, phone_bottom - 12 * s
    d.rectangle([sc_x1, sc_y1, sc_x2, sc_y2], fill=CREAM)
    
    # Native Mobile UI layout on phone
    d.ellipse([phone_cx - 16 * s, sc_y1 + 4 * s, phone_cx + 16 * s, sc_y1 + 16 * s], fill=INK)
    # Header bar
    d.rectangle([sc_x1 + 12 * s, sc_y1 + 26 * s, sc_x2 - 12 * s, sc_y1 + 52 * s], fill=INK)
    d.text((sc_x1 + 20 * s, sc_y1 + 32 * s), "Expo Router // Native UI", fill=CREAM, font=FONT_TINY)
    
    # Search bar
    d.rectangle([sc_x1 + 12 * s, sc_y1 + 60 * s, sc_x2 - 12 * s, sc_y1 + 82 * s], outline=INK, width=s)
    d.text((sc_x1 + 20 * s, sc_y1 + 65 * s), "Search native primitives...", fill=GRID_ACCENT, font=FONT_TINY)
    
    # Feed cards
    for fy in range(int(sc_y1 + 92 * s), int(sc_y2 - 65 * s), int(56 * s)):
        d.rectangle([sc_x1 + 12 * s, fy, sc_x2 - 12 * s, fy + 48 * s], fill=CREAM, outline=INK, width=s)
        d.rectangle([sc_x1 + 18 * s, fy + 8 * s, sc_x1 + 54 * s, fy + 40 * s], fill=INK)
        d.rectangle([sc_x1 + 62 * s, fy + 12 * s, sc_x2 - 25 * s, fy + 22 * s], fill=INK)
        d.rectangle([sc_x1 + 62 * s, fy + 26 * s, sc_x2 - 60 * s, fy + 36 * s], fill=GRID_ACCENT)
        
    # Tab navigation bar
    d.rectangle([sc_x1 + 12 * s, sc_y2 - 36 * s, sc_x2 - 12 * s, sc_y2 - 8 * s], fill=INK)
    for tx in range(sc_x1 + 30 * s, sc_x2 - 15 * s, (sc_w * 2 - 40 * s) // 4):
        d.ellipse([tx - 8 * s, sc_y2 - 26 * s, tx + 8 * s, sc_y2 - 14 * s], fill=CREAM)
        
    # Bold Vermilion Red-Orange Accent 1: Content State Tag on Phone
    pill_y = sc_y1 + 92 * s + 8 * s
    d.polygon([(sc_x2 - 76 * s, pill_y), (sc_x2 - 18 * s, pill_y), (sc_x2 - 18 * s, pill_y + 18 * s), (sc_x2 - 76 * s, pill_y + 18 * s)], fill=VERM)
    d.text((sc_x2 - 72 * s, pill_y + 3 * s), "CONTENT", fill=CREAM, font=FONT_TINY)
    
    # Right Flank: High-Precision Articulated AI Robotic Arm
    arm_base_x = int(W * 0.86)
    arm_base_y = int(H * 0.86)
    d.polygon([(arm_base_x - 80 * s, arm_base_y), (arm_base_x + 80 * s, arm_base_y), (arm_base_x + 100 * s, H), (arm_base_x - 100 * s, H)], fill=INK)
    shoulder_x, shoulder_y = arm_base_x, arm_base_y - 50 * s
    d.ellipse([shoulder_x - 35 * s, shoulder_y - 35 * s, shoulder_x + 35 * s, shoulder_y + 35 * s], fill=INK)
    elbow_x, elbow_y = int(W * 0.68), int(H * 0.44)
    d.line([(shoulder_x, shoulder_y), (elbow_x, elbow_y)], fill=INK, width=18 * s)
    d.ellipse([elbow_x - 26 * s, elbow_y - 26 * s, elbow_x + 26 * s, elbow_y + 26 * s], fill=INK)
    wrist_x, wrist_y = phone_cx + phone_w + 15 * s, phone_top + 110 * s
    d.line([(elbow_x, elbow_y), (wrist_x, wrist_y)], fill=INK, width=14 * s)
    d.ellipse([wrist_x - 18 * s, wrist_y - 18 * s, wrist_x + 18 * s, wrist_y + 18 * s], fill=INK)
    
    # Gripper
    d.polygon([(wrist_x, wrist_y - 12 * s), (wrist_x - 30 * s, wrist_y - 22 * s), (wrist_x - 35 * s, wrist_y - 14 * s), (wrist_x - 12 * s, wrist_y - 6 * s)], fill=INK)
    d.polygon([(wrist_x, wrist_y + 12 * s), (wrist_x - 30 * s, wrist_y + 22 * s), (wrist_x - 35 * s, wrist_y + 14 * s), (wrist_x - 12 * s, wrist_y + 6 * s)], fill=INK)
    
    # Bold Vermilion Red-Orange Accent 2: Alignment Laser Crosshairs
    laser_tx = phone_cx + 45 * s
    laser_ty = phone_top + 110 * s
    d.line([(wrist_x - 30 * s, wrist_y), (laser_tx, laser_ty)], fill=VERM, width=3 * s)
    d.ellipse([laser_tx - 12 * s, laser_ty - 12 * s, laser_tx + 12 * s, laser_ty + 12 * s], outline=VERM, width=2 * s)
    d.line([(laser_tx - 18 * s, laser_ty), (laser_tx + 18 * s, laser_ty)], fill=VERM, width=2 * s)
    d.line([(laser_tx, laser_ty - 18 * s), (laser_tx, laser_ty + 18 * s)], fill=VERM, width=2 * s)
    
    # Left Foreground: FULL STANDING AI ENGINEER SILHOUETTE
    draw_silhouette_standing(d, int(W * 0.16), int(H * 0.90), total_h=int(320 * s), facing_left=False, arms_crossed=True)
    
    im_final = im.resize((W_FINAL, H_FINAL), Image.LANCZOS)
    im_final.save("demo-news/public/images/expo-skills-shell-ai-agent-native-ui.jpg", quality=95)
    print("Expo Skills rich thumbnail generated.")


# ==============================================================================
# 4. MACRO: AGPL RUST WORKSPACE & MODEL CONTEXT PROTOCOL (MCP)
# ==============================================================================
def generate_macro():
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    s = SCALE
    
    vp_x, vp_y = int(W * 0.50), int(H * 0.44)
    horizon_y = int(H * 0.58)
    draw_perspective_grid(d, vp_x, vp_y, horizon_y, ray_spacing=75)
    
    # Left and Right Monolithic Blade Server Racks (Perspective columns)
    l_racks = [
        (int(W * 0.02), int(W * 0.16), int(H * 0.08), int(H * 0.88)),
        (int(W * 0.18), int(W * 0.28), int(H * 0.18), int(H * 0.78)),
        (int(W * 0.30), int(W * 0.36), int(H * 0.28), int(H * 0.68))
    ]
    for rx1, rx2, ry1, ry2 in l_racks:
        d.polygon([(rx1, ry1), (rx2, ry1 + 25 * s), (rx2, ry2 - 25 * s), (rx1, ry2)], fill=INK)
        h_total = ry2 - ry1 - 50 * s
        num_blades = 14
        b_h = h_total // num_blades
        for b in range(num_blades):
            by = ry1 + 25 * s + b * b_h
            d.line([(rx1 + 10 * s, by), (rx2 - 8 * s, by + 4 * s)], fill=CREAM, width=s)
            d.ellipse([rx2 - 16 * s, by + 2 * s, rx2 - 12 * s, by + 6 * s], fill=CREAM)
            
    r_racks = [
        (int(W * 0.98), int(W * 0.84), int(H * 0.08), int(H * 0.88)),
        (int(W * 0.82), int(W * 0.72), int(H * 0.18), int(H * 0.78)),
        (int(W * 0.70), int(W * 0.64), int(H * 0.28), int(H * 0.68))
    ]
    for rx1, rx2, ry1, ry2 in r_racks:
        d.polygon([(rx1, ry1), (rx2, ry1 + 25 * s), (rx2, ry2 - 25 * s), (rx1, ry2)], fill=INK)
        h_total = ry2 - ry1 - 50 * s
        num_blades = 14
        b_h = h_total // num_blades
        for b in range(num_blades):
            by = ry1 + 25 * s + b * b_h
            d.line([(rx1 - 10 * s, by), (rx2 + 8 * s, by + 4 * s)], fill=CREAM, width=s)
            d.ellipse([rx2 + 12 * s, by + 2 * s, rx2 + 16 * s, by + 6 * s], fill=CREAM)
            
    # Overhead cable trusses
    for gy in [int(H * 0.12), int(H * 0.22)]:
        d.line([(0, gy), (W, gy)], fill=INK, width=5 * s)
        for gx in range(int(W * 0.10), int(W * 0.90), 80 * s):
            d.line([(gx, gy), (gx + 18 * s, gy + 18 * s)], fill=INK, width=2 * s)
            
    # Center Elevated Walkway & FULL STANDING SYSTEM ARCHITECT SILHOUETTE
    plat_w = int(W * 0.28)
    plat_x1, plat_x2 = vp_x - plat_w // 2, vp_x + plat_w // 2
    plat_y = int(H * 0.76)
    d.polygon([(plat_x1, plat_y), (plat_x2, plat_y), (plat_x2 + 45 * s, H), (plat_x1 - 45 * s, H)], fill=INK)
    d.line([(plat_x1 - 45 * s, plat_y), (plat_x2 + 45 * s, plat_y)], fill=CREAM, width=3 * s)
    
    draw_silhouette_standing(d, vp_x, plat_y + int(60 * s), total_h=int(260 * s), facing_left=False, arms_crossed=True)
    
    # Center Upper Space: Model Context Protocol (MCP) Nexus & Unified Tool Graph
    mcp_cx, mcp_cy = vp_x, int(H * 0.28)
    
    nodes = [
        (mcp_cx - 180 * s, mcp_cy - 85 * s, "EMAIL [IMAP/SMTP]"),
        (mcp_cx + 180 * s, mcp_cy - 85 * s, "CHAT [MATRIX/WEBSOCKET]"),
        (mcp_cx - 180 * s, mcp_cy + 85 * s, "TASKS [GRAPH DB]"),
        (mcp_cx + 180 * s, mcp_cy + 85 * s, "CRM [SHARED MEMORY]")
    ]
    for nx, ny, label in nodes:
        d.line([(nx, ny), (mcp_cx, mcp_cy)], fill=INK, width=4 * s)
        nw, nh = 70 * s, 38 * s
        d.rectangle([nx - nw, ny - nh, nx + nw, ny + nh], fill=CREAM, outline=INK, width=2 * s)
        d.rectangle([nx - nw, ny - nh, nx + nw, ny - nh + 16 * s], fill=INK)
        d.text((nx - nw + 8 * s, ny - nh + 3 * s), label.split()[0], fill=CREAM, font=FONT_TINY)
        
        # Internal icons
        if "EMAIL" in label:
            d.rectangle([nx - 26 * s, ny + 2 * s, nx + 26 * s, ny + 22 * s], outline=INK, width=s)
            d.line([(nx - 26 * s, ny + 2 * s), (nx, ny + 14 * s), (nx + 26 * s, ny + 2 * s)], fill=INK, width=s)
        elif "CHAT" in label:
            d.rectangle([nx - 26 * s, ny, nx + 12 * s, ny + 16 * s], fill=INK)
            d.rectangle([nx - 10 * s, ny + 8 * s, nx + 26 * s, ny + 24 * s], outline=INK, width=s)
        elif "TASKS" in label:
            d.rectangle([nx - 22 * s, ny, nx - 12 * s, ny + 8 * s], fill=INK)
            d.line([(nx - 8 * s, ny + 4 * s), (nx + 22 * s, ny + 4 * s)], fill=INK, width=s)
            d.rectangle([nx - 22 * s, ny + 12 * s, nx - 12 * s, ny + 20 * s], fill=INK)
            d.line([(nx - 8 * s, ny + 16 * s), (nx + 22 * s, ny + 16 * s)], fill=INK, width=s)
        elif "CRM" in label:
            d.ellipse([nx - 20 * s, ny, nx + 20 * s, ny + 8 * s], outline=INK, width=s)
            d.line([(nx - 20 * s, ny + 4 * s), (nx - 20 * s, ny + 22 * s)], fill=INK, width=s)
            d.line([(nx + 20 * s, ny + 4 * s), (nx + 20 * s, ny + 22 * s)], fill=INK, width=s)
            d.ellipse([nx - 20 * s, ny + 18 * s, nx + 20 * s, ny + 26 * s], outline=INK, width=s)
            
    # Bold Vermilion Red-Orange Hexagonal MCP Nexus Core
    hex_r = 60 * s
    hex_pts = []
    for angle in range(30, 390, 60):
        rad = math.radians(angle)
        hex_pts.append((mcp_cx + hex_r * math.cos(rad), mcp_cy + hex_r * math.sin(rad)))
    d.polygon(hex_pts, fill=VERM)
    
    inner_pts = []
    for angle in range(30, 390, 60):
        rad = math.radians(angle)
        inner_pts.append((mcp_cx + (hex_r - 12 * s) * math.cos(rad), mcp_cy + (hex_r - 12 * s) * math.sin(rad)))
    d.polygon(inner_pts, fill=CREAM)
    d.text((mcp_cx - 28 * s, mcp_cy - 14 * s), "MCP", fill=INK, font=FONT_TITLE)
    
    # Vermilion high-speed data pulses
    for nx, ny, _ in nodes:
        px = int(nx * 0.4 + mcp_cx * 0.6)
        py = int(ny * 0.4 + mcp_cy * 0.6)
        d.ellipse([px - 7 * s, py - 7 * s, px + 7 * s, py + 7 * s], fill=VERM)
        
    # Top banner
    d.rectangle([vp_x - 160 * s, int(H * 0.04), vp_x + 160 * s, int(H * 0.09)], fill=INK)
    d.text((vp_x - 145 * s, int(H * 0.05)), "42 RUST SERVICES // AGPL-3.0 WORKSPACE", fill=CREAM, font=FONT_BADGE)
    
    im_final = im.resize((W_FINAL, H_FINAL), Image.LANCZOS)
    im_final.save("demo-news/public/images/macro-rust-agpl-workspace-mcp.jpg", quality=95)
    print("Macro rich thumbnail generated.")


# ==============================================================================
# 5. LINKSWIFT: DIRECT CLOUD STORAGE DOWNLOAD BYPASS
# ==============================================================================
def generate_linkswift():
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    s = SCALE
    
    vp_x, vp_y = int(W * 0.50), int(H * 0.42)
    horizon_y = int(H * 0.60)
    draw_perspective_grid(d, vp_x, vp_y, horizon_y, ray_spacing=75)
    
    # Central Bank Vault Door
    vault_cx, vault_cy = vp_x, int(H * 0.38)
    vault_r = 185 * s
    d.ellipse([vault_cx - vault_r - 22 * s, vault_cy - vault_r - 22 * s, vault_cx + vault_r + 22 * s, vault_cy + vault_r + 22 * s], fill=INK)
    for angle in range(0, 360, 20):
        rad = math.radians(angle)
        rx = vault_cx + (vault_r + 11 * s) * math.cos(rad)
        ry = vault_cy + (vault_r + 11 * s) * math.sin(rad)
        d.ellipse([rx - 4 * s, ry - 4 * s, rx + 4 * s, ry + 4 * s], fill=CREAM)
        
    d.ellipse([vault_cx - vault_r, vault_cy - vault_r, vault_cx + vault_r, vault_cy + vault_r], fill=CREAM, outline=INK, width=4 * s)
    d.ellipse([vault_cx - 50 * s, vault_cy - 50 * s, vault_cx + 50 * s, vault_cy + 50 * s], fill=INK)
    for angle in range(0, 360, 60):
        rad = math.radians(angle)
        sx = vault_cx + 100 * s * math.cos(rad)
        sy = vault_cy + 100 * s * math.sin(rad)
        d.line([(vault_cx, vault_cy), (sx, sy)], fill=INK, width=7 * s)
        d.ellipse([sx - 14 * s, sy - 14 * s, sx + 14 * s, sy + 14 * s], fill=INK)
        
    # Heavy Crossed Steel Security Chains
    chain_w = 18 * s
    d.line([(vault_cx - vault_r, vault_cy - vault_r), (vault_cx + vault_r, vault_cy + vault_r)], fill=INK, width=chain_w)
    d.line([(vault_cx - vault_r, vault_cy + vault_r), (vault_cx + vault_r, vault_cy - vault_r)], fill=INK, width=chain_w)
    for t in [-0.7, -0.4, -0.1, 0.2, 0.5, 0.8]:
        lx = vault_cx + int(vault_r * t)
        ly = vault_cy + int(vault_r * t)
        d.ellipse([lx - 6 * s, ly - 4 * s, lx + 6 * s, ly + 4 * s], fill=CREAM)
        lx2 = vault_cx + int(vault_r * t)
        ly2 = vault_cy - int(vault_r * t)
        d.ellipse([lx2 - 6 * s, ly2 - 4 * s, lx2 + 6 * s, ly2 + 4 * s], fill=CREAM)
        
    # Snapped Central Padlock
    lock_cx, lock_cy = vault_cx, vault_cy
    lock_w, lock_h = 68 * s, 56 * s
    d.rectangle([lock_cx - lock_w // 2, lock_cy - lock_h // 2, lock_cx + lock_w // 2, lock_cy + lock_h // 2], fill=INK)
    d.ellipse([lock_cx - 7 * s, lock_cy - 14 * s, lock_cx + 7 * s, lock_cy], fill=CREAM)
    d.polygon([(lock_cx - 5 * s, lock_cy - 5 * s), (lock_cx + 5 * s, lock_cy - 5 * s), (lock_cx + 2 * s, lock_cy + 12 * s), (lock_cx - 2 * s, lock_cy + 12 * s)], fill=CREAM)
    
    # Left Foreground: Browser Developer Console Window
    con_x1, con_y1 = int(W * 0.08), int(H * 0.46)
    con_x2, con_y2 = int(W * 0.45), int(H * 0.88)
    d.polygon([(con_x1, con_y1), (con_x2, con_y1 + 22 * s), (con_x2 - 22 * s, con_y2), (con_x1 - 22 * s, con_y2 - 22 * s)], fill=CREAM)
    d.polygon([(con_x1, con_y1), (con_x2, con_y1 + 22 * s), (con_x2 - 22 * s, con_y2), (con_x1 - 22 * s, con_y2 - 22 * s)], outline=INK, width=3 * s)
    d.polygon([(con_x1, con_y1), (con_x2, con_y1 + 22 * s), (con_x2 - 3 * s, con_y1 + 48 * s), (con_x1 - 3 * s, con_y1 + 26 * s)], fill=INK)
    d.text((con_x1 + 12 * s, con_y1 + 7 * s), "LinkSwift.js // Userscript Console [33.9k Stars]", fill=CREAM, font=FONT_TINY)
    
    lines = [
        "> LinkSwift.intercept(downloadRequest);",
        "  [Provider]: Baidu / Aliyun / 123Drive / Quark",
        "  [Action]: Stripping desktop client payload...",
        "  [Status]: Direct CDN stream token extracted.",
        "> streamDownload(url, threads=16);"
    ]
    for idx, l in enumerate(lines):
        d.text((con_x1 + 12 * s, con_y1 + 38 * s + idx * 20 * s), l, fill=INK, font=FONT_TINY)
        
    # Bold Vermilion Red-Orange Piercing Direct Download Lightning Vector
    arrow_tip_x = int(W * 0.74)
    arrow_tip_y = int(H * 0.72)
    arrow_pts = [
        (vault_cx - 12 * s, vault_cy - 12 * s),
        (vault_cx + 45 * s, vault_cy + 18 * s),
        (vault_cx + 28 * s, vault_cy + 40 * s),
        (arrow_tip_x, arrow_tip_y),
        (arrow_tip_x - 50 * s, arrow_tip_y - 12 * s),
        (arrow_tip_x - 34 * s, arrow_tip_y - 28 * s),
        (vault_cx + 12 * s, vault_cy + 12 * s)
    ]
    d.polygon(arrow_pts, fill=VERM)
    
    # Vermilion speed callout badge
    d.polygon([(arrow_tip_x + 12 * s, arrow_tip_y - 35 * s), (arrow_tip_x + 170 * s, arrow_tip_y - 35 * s), (arrow_tip_x + 170 * s, arrow_tip_y + 12 * s), (arrow_tip_x + 12 * s, arrow_tip_y + 12 * s)], fill=VERM)
    d.text((arrow_tip_x + 20 * s, arrow_tip_y - 28 * s), "DIRECT LINK: 100 MB/s", fill=CREAM, font=FONT_CODE_BOLD)
    d.text((arrow_tip_x + 20 * s, arrow_tip_y - 10 * s), "CLIENT BYPASSED: 100%", fill=CREAM, font=FONT_TINY)
    
    # Snapped shackle sparks
    d.line([(lock_cx + 22 * s, lock_cy - 28 * s), (lock_cx + 50 * s, lock_cy - 50 * s)], fill=VERM, width=5 * s)
    d.line([(lock_cx + 12 * s, lock_cy - 34 * s), (lock_cx + 28 * s, lock_cy - 60 * s)], fill=VERM, width=4 * s)
    
    im_final = im.resize((W_FINAL, H_FINAL), Image.LANCZOS)
    im_final.save("demo-news/public/images/linkswift-javascript-cloud-storage.jpg", quality=95)
    print("LinkSwift rich thumbnail generated.")


# ==============================================================================
# 6. ELAYADESIGN: AI DESIGN SYSTEM SKILLS & ACCESSIBILITY CALIBRATION
# ==============================================================================
def generate_elayadesign():
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    s = SCALE
    
    vp_x, vp_y = int(W * 0.40), int(H * 0.38)
    horizon_y = int(H * 0.58)
    draw_perspective_grid(d, vp_x, vp_y, horizon_y, ray_spacing=75)
    
    # Background Wall Board: Typography & Spatial Scale
    b_x1, b_y1 = int(W * 0.06), int(H * 0.08)
    b_x2, b_y2 = int(W * 0.94), int(H * 0.42)
    d.rectangle([b_x1, b_y1, b_x2, b_y2], fill=CREAM, outline=INK, width=3 * s)
    d.rectangle([b_x1, b_y1, b_x2, b_y1 + 28 * s], fill=INK)
    d.text((b_x1 + 18 * s, b_y1 + 6 * s), "ELAYADESIGN / DESIGN-SYSTEM // AGENT DESIGN SKILLS SPECIFICATION", fill=CREAM, font=FONT_TITLE)
    
    type_x = b_x1 + 35 * s
    d.text((type_x, b_y1 + 42 * s), "DISPLAY TITLE 48px / Line Height 56px", fill=INK, font=FONT_SUBTITLE)
    d.text((type_x, b_y1 + 68 * s), "SECTION HEADING 24px / Bold 700 / Letter Spacing -0.5px", fill=INK, font=FONT_BODY)
    d.text((type_x, b_y1 + 92 * s), "BODY REGULAR 16px / Regular 400 / Line Height 24px", fill=GRID_ACCENT, font=FONT_BODY)
    d.text((type_x, b_y1 + 114 * s), "CAPTION 12px / Medium 500 / Uppercase Monospace", fill=GRID_ACCENT, font=FONT_TINY)
    
    # 8px Base Scale Swatches
    sw_x = b_x2 - 300 * s
    sw_y = b_y1 + 44 * s
    d.text((sw_x, sw_y), "SPATIAL GRID: 8px BASE SYSTEM", fill=INK, font=FONT_TINY)
    for idx, step in enumerate([8, 16, 24, 32, 48, 64]):
        bx = sw_x + idx * 46 * s
        by = sw_y + 20 * s
        d.rectangle([bx, by, bx + step // 2 * s, by + 34 * s], fill=INK)
        d.text((bx, by + 38 * s), f"{step}px", fill=INK, font=FONT_TINY)
        
    # Foreground Drafting Table
    desk_left, desk_right = int(W * 0.12), int(W * 0.88)
    desk_top, desk_bottom = int(H * 0.46), int(H * 0.84)
    d.polygon([(desk_left + 70 * s, desk_top), (desk_right - 50 * s, desk_top), (desk_right, desk_bottom), (desk_left, desk_bottom)], fill=INK)
    d.rectangle([desk_left + 60 * s, desk_bottom, desk_left + 90 * s, H], fill=INK)
    d.rectangle([desk_right - 90 * s, desk_bottom, desk_right - 60 * s, H], fill=INK)
    d.line([(desk_left + 70 * s, int(H * 0.92)), (desk_right - 70 * s, int(H * 0.92))], fill=INK, width=7 * s)
    
    # Pinned Blueprint Sheet on Desk
    sheet_x1, sheet_y1 = desk_left + 100 * s, desk_top + 18 * s
    sheet_x2, sheet_y2 = desk_right - 80 * s, desk_bottom - 18 * s
    d.polygon([(sheet_x1 + 35 * s, sheet_y1), (sheet_x2 - 25 * s, sheet_y1), (sheet_x2, sheet_y2), (sheet_x1, sheet_y2)], fill=CREAM)
    
    # Button Primitives Row on Blueprint
    btn_y = sheet_y1 + 35 * s
    d.rectangle([sheet_x1 + 45 * s, btn_y, sheet_x1 + 145 * s, btn_y + 32 * s], fill=INK)
    d.text((sheet_x1 + 62 * s, btn_y + 8 * s), "Primary", fill=CREAM, font=FONT_TINY)
    d.rectangle([sheet_x1 + 160 * s, btn_y, sheet_x1 + 260 * s, btn_y + 32 * s], outline=INK, width=2 * s)
    d.text((sheet_x1 + 172 * s, btn_y + 8 * s), "Secondary", fill=INK, font=FONT_TINY)
    
    # UI Card Prototype
    card_x1 = sheet_x1 + 45 * s
    card_y1 = btn_y + 50 * s
    card_x2 = sheet_x1 + 300 * s
    card_y2 = sheet_y2 - 28 * s
    d.rectangle([card_x1, card_y1, card_x2, card_y2], fill=CREAM, outline=INK, width=2 * s)
    d.rectangle([card_x1 + 12 * s, card_y1 + 12 * s, card_x2 - 12 * s, card_y1 + 38 * s], fill=INK)
    d.text((card_x1 + 20 * s, card_y1 + 16 * s), "Component Card [AI Generated]", fill=CREAM, font=FONT_TINY)
    d.rectangle([card_x1 + 12 * s, card_y1 + 46 * s, card_x1 + 80 * s, card_y1 + 105 * s], fill=GRID_ACCENT)
    d.rectangle([card_x1 + 92 * s, card_y1 + 52 * s, card_x2 - 18 * s, card_y1 + 62 * s], fill=INK)
    d.rectangle([card_x1 + 92 * s, card_y1 + 68 * s, card_x2 - 38 * s, card_y1 + 78 * s], fill=INK)
    d.rectangle([card_x1 + 92 * s, card_y1 + 84 * s, card_x2 - 65 * s, card_y1 + 94 * s], fill=GRID_ACCENT)
    
    # Bold Vermilion Red-Orange Dimension Lines
    dim_x = card_x1 + 80 * s
    d.line([(dim_x, card_y1 + 46 * s), (dim_x + 12 * s, card_y1 + 46 * s)], fill=VERM, width=2 * s)
    d.line([(dim_x, card_y1 + 105 * s), (dim_x + 12 * s, card_y1 + 105 * s)], fill=VERM, width=2 * s)
    d.line([(dim_x + 6 * s, card_y1 + 46 * s), (dim_x + 6 * s, card_y1 + 105 * s)], fill=VERM, width=2 * s)
    d.text((dim_x + 14 * s, card_y1 + 70 * s), "8px PAD", fill=VERM, font=FONT_TINY)
    
    # Precision Metal Caliper Tool
    cal_cx, cal_cy = sheet_x1 + 360 * s, sheet_y1 + 65 * s
    d.line([(cal_cx, cal_cy), (cal_cx - 35 * s, cal_cy + 90 * s)], fill=INK, width=5 * s)
    d.line([(cal_cx, cal_cy), (cal_cx + 35 * s, cal_cy + 90 * s)], fill=INK, width=5 * s)
    d.ellipse([cal_cx - 10 * s, cal_cy - 10 * s, cal_cx + 10 * s, cal_cy + 10 * s], fill=INK)
    
    # Bold Vermilion Red-Orange WCAG AA Contrast Compliance Gauge
    gauge_cx = sheet_x2 - 120 * s
    gauge_cy = sheet_y1 + 95 * s
    gauge_r = 60 * s
    d.ellipse([gauge_cx - gauge_r, gauge_cy - gauge_r, gauge_cx + gauge_r, gauge_cy + gauge_r], outline=VERM, width=5 * s)
    d.line([(gauge_cx, gauge_cy), (gauge_cx + 36 * s, gauge_cy - 36 * s)], fill=VERM, width=5 * s)
    d.ellipse([gauge_cx - 8 * s, gauge_cy - 8 * s, gauge_cx + 8 * s, gauge_cy + 8 * s], fill=VERM)
    for angle in range(140, 400, 30):
        rad = math.radians(angle)
        gx1 = gauge_cx + (gauge_r - 10 * s) * math.cos(rad)
        gy1 = gauge_cy + (gauge_r - 10 * s) * math.sin(rad)
        gx2 = gauge_cx + gauge_r * math.cos(rad)
        gy2 = gauge_cy + gauge_r * math.sin(rad)
        d.line([(gx1, gy1), (gx2, gy2)], fill=VERM, width=3 * s)
    d.text((gauge_cx - 40 * s, gauge_cy + 14 * s), "4.5:1 PASSED", fill=VERM, font=FONT_CODE_BOLD)
    d.text((gauge_cx - 35 * s, gauge_cy + 30 * s), "WCAG AA OK", fill=INK, font=FONT_TINY)
    
    # FULL STANDING LEAD DESIGNER SILHOUETTE
    draw_silhouette_standing(d, int(W * 0.88), int(H * 0.74), total_h=int(330 * s), facing_left=True, pointing=True)
    
    im_final = im.resize((W_FINAL, H_FINAL), Image.LANCZOS)
    im_final.save("demo-news/public/images/elayadesign-ai-design-skills.jpg", quality=95)
    print("ElayaDesign rich thumbnail generated.")


if __name__ == "__main__":
    generate_ruview()
    generate_xiaolai()
    generate_expo_skills()
    generate_macro()
    generate_linkswift()
    generate_elayadesign()
    print("All 6 rich editorial thumbnails generated successfully.")

