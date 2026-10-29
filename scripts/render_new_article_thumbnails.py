"""
Render high-fidelity, intricately detailed editorial illustrations for the 6 new articles:
1. RuView: Wi-Fi Spatial Intelligence (ruview-rust-wifi-spatial-intelligence.jpg)
2. Xiaolai: The Craft of Self-Teaching (xiaolai-craft-of-selfteaching.jpg)
3. Expo Skills: AI Agent Native UI (expo-skills-shell-ai-agent-native-ui.jpg)
4. Macro: AGPL Rust Workspace & MCP (macro-rust-agpl-workspace-mcp.jpg)
5. LinkSwift: Direct Cloud Download Bypass (linkswift-javascript-cloud-storage.jpg)
6. ElayaDesign: AI Design System Skills (elayadesign-ai-design-skills.jpg)

Renders at 2x resolution (2752x1536) and downsamples with Lanczos to 1376x768
for pristine vector-sharp edges, smooth geometric silhouettes, and exact brand palette:
- Warm cream paper background: #F7F2E9
- Solid deep charcoal black ink: #16130E
- Bold vermilion red-orange accent: #C2410C
- Subtle wireframe grid: #E5DDD0
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

W_FINAL, H_FINAL = 1376, 768
SCALE = 2
W, H = W_FINAL * SCALE, H_FINAL * SCALE

CREAM = (247, 242, 233)
GRID = (229, 221, 208)
GRID_ACCENT = (218, 208, 192)
INK = (22, 19, 14)
VERM = (194, 65, 12)

# Load system TrueType fonts scaled appropriately
def get_font(name, size):
    size_scaled = int(size * SCALE)
    path = f"C:/Windows/Fonts/{name}"
    try:
        return ImageFont.truetype(path, size_scaled)
    except Exception:
        try:
            return ImageFont.truetype("arial.ttf", size_scaled)
        except Exception:
            return ImageFont.load_default()

FONT_TITLE = get_font("segoeuib.ttf", 20)
FONT_SUBTITLE = get_font("segoeuib.ttf", 14)
FONT_BODY = get_font("segoeui.ttf", 12)
FONT_CODE = get_font("consola.ttf", 11)
FONT_CODE_BOLD = get_font("consolab.ttf", 12)
FONT_SMALL = get_font("segoeui.ttf", 10)
FONT_TINY = get_font("consola.ttf", 9)
FONT_LARGE_NUM = get_font("segoeuib.ttf", 36)

def draw_perspective_room(d, vp_x, vp_y, horizon_y, wall_step=64):
    """Draw an architectural interior perspective grid."""
    s = SCALE
    # Base background
    d.rectangle([0, 0, W, H], fill=CREAM)
    
    # Wall background grid
    w_step = wall_step * s
    for x in range(0, W, w_step):
        d.line([(x, 0), (x, horizon_y)], fill=GRID, width=s)
    for y in range(0, horizon_y, w_step):
        d.line([(0, y), (W, y)], fill=GRID, width=s)
        
    # Horizon line
    d.line([(0, horizon_y), (W, horizon_y)], fill=GRID_ACCENT, width=2 * s)
    
    # Floor perspective rays from horizon toward bottom edge
    for x in range(-W // 2, W * 2, 70 * s):
        d.line([(vp_x, vp_y), (x, H)], fill=GRID, width=s)
        
    # Floor horizontal perspective rungs
    for t in [0.04, 0.10, 0.18, 0.28, 0.40, 0.55, 0.73, 0.95]:
        fy = int(horizon_y + (H - horizon_y) * t)
        d.line([(0, fy), (W, fy)], fill=GRID, width=s)

def draw_person_standing(d, cx, cy, height=360, facing_left=True, arms_crossed=False, pointing=False):
    """Draw a crisp, anatomically proportioned standing human silhouette."""
    s = SCALE
    h = height * s // 200
    w = h // 4
    
    # Head & hair
    head_r = int(h * 0.13)
    head_cy = cy - int(h * 0.85)
    d.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r], fill=INK)
    # Nose / profile bump
    profile_x = cx - head_r - int(4 * s) if facing_left else cx + head_r + int(4 * s)
    d.polygon([(cx, head_cy - 4 * s), (profile_x, head_cy + 2 * s), (cx, head_cy + 8 * s)], fill=INK)
    
    # Neck & collar
    d.polygon([
        (cx - int(head_r * 0.4), head_cy + head_r - int(2 * s)),
        (cx + int(head_r * 0.4), head_cy + head_r - int(2 * s)),
        (cx + int(head_r * 0.6), head_cy + head_r + int(12 * s)),
        (cx - int(head_r * 0.6), head_cy + head_r + int(12 * s))
    ], fill=INK)
    
    # Torso (Suit / jacket)
    torso_top = head_cy + head_r + int(10 * s)
    torso_bottom = cy - int(h * 0.45)
    shoulder_w = int(w * 1.2)
    waist_w = int(w * 0.9)
    d.polygon([
        (cx - shoulder_w, torso_top + int(6 * s)),
        (cx + shoulder_w, torso_top + int(6 * s)),
        (cx + waist_w, torso_bottom),
        (cx - waist_w, torso_bottom)
    ], fill=INK)
    # Shoulder curves
    d.ellipse([cx - shoulder_w - int(4 * s), torso_top, cx - shoulder_w + int(12 * s), torso_top + int(24 * s)], fill=INK)
    d.ellipse([cx + shoulder_w - int(12 * s), torso_top, cx + shoulder_w + int(4 * s), torso_top + int(24 * s)], fill=INK)
    
    # Legs / trousers
    leg_w = int(w * 0.38)
    leg_gap = int(w * 0.14)
    # Left leg
    d.polygon([
        (cx - waist_w + int(2 * s), torso_bottom),
        (cx - leg_gap, torso_bottom),
        (cx - leg_gap - int(4 * s), cy),
        (cx - waist_w - int(2 * s), cy)
    ], fill=INK)
    # Right leg
    d.polygon([
        (cx + leg_gap, torso_bottom),
        (cx + waist_w - int(2 * s), torso_bottom),
        (cx + waist_w + int(2 * s), cy),
        (cx + leg_gap + int(4 * s), cy)
    ], fill=INK)
    # Shoes
    shoe_len = int(w * 0.6)
    shoe_dir = -shoe_len if facing_left else shoe_len
    d.polygon([(cx - waist_w - int(2 * s), cy - int(6 * s)), (cx - waist_w + shoe_dir, cy), (cx - leg_gap, cy)], fill=INK)
    d.polygon([(cx + leg_gap, cy - int(6 * s)), (cx + waist_w + shoe_dir, cy), (cx + waist_w + int(2 * s), cy)], fill=INK)
    
    # Arms
    if arms_crossed:
        d.ellipse([cx - shoulder_w, torso_top + int(14 * s), cx + shoulder_w, torso_top + int(50 * s)], fill=INK)
    elif pointing:
        arm_end_x = cx - int(w * 2.2) if facing_left else cx + int(w * 2.2)
        d.polygon([
            (cx - shoulder_w + int(6 * s), torso_top + int(8 * s)),
            (arm_end_x, torso_top - int(10 * s)),
            (arm_end_x, torso_top + int(8 * s)),
            (cx - shoulder_w + int(6 * s), torso_top + int(26 * s))
        ], fill=INK)
    else:
        # Hanging naturally
        d.rectangle([cx - shoulder_w - int(2 * s), torso_top + int(8 * s), cx - shoulder_w + int(10 * s), torso_bottom + int(15 * s)], fill=INK)
        d.rectangle([cx + shoulder_w - int(10 * s), torso_top + int(8 * s), cx + shoulder_w + int(2 * s), torso_bottom + int(15 * s)], fill=INK)

def draw_person_walking(d, cx, cy, height=360, facing_left=True):
    """Draw a walking human silhouette with natural stride."""
    s = SCALE
    h = height * s // 200
    w = h // 4
    
    # Head & hair
    head_r = int(h * 0.13)
    head_cy = cy - int(h * 0.86)
    d.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r], fill=INK)
    # Profile
    profile_x = cx - head_r - int(4 * s) if facing_left else cx + head_r + int(4 * s)
    d.polygon([(cx, head_cy - 4 * s), (profile_x, head_cy + 2 * s), (cx, head_cy + 8 * s)], fill=INK)
    
    # Torso leaning slightly forward
    torso_top = head_cy + head_r + int(8 * s)
    torso_bottom = cy - int(h * 0.44)
    shoulder_w = int(w * 1.1)
    waist_w = int(w * 0.85)
    lean = -int(8 * s) if facing_left else int(8 * s)
    d.polygon([
        (cx - shoulder_w + lean, torso_top),
        (cx + shoulder_w + lean, torso_top),
        (cx + waist_w, torso_bottom),
        (cx - waist_w, torso_bottom)
    ], fill=INK)
    
    # Walking legs: Stride forward and back
    stride_f = -int(w * 0.9) if facing_left else int(w * 0.9)
    stride_b = int(w * 0.8) if facing_left else -int(w * 0.8)
    # Forward leg
    d.polygon([
        (cx + lean, torso_bottom),
        (cx + lean + int(8 * s), torso_bottom),
        (cx + stride_f + int(10 * s), cy),
        (cx + stride_f - int(6 * s), cy)
    ], fill=INK)
    # Forward shoe
    d.polygon([(cx + stride_f - int(6 * s), cy - int(8 * s)), (cx + stride_f + stride_f // 2, cy), (cx + stride_f + int(10 * s), cy)], fill=INK)
    
    # Back leg
    d.polygon([
        (cx - lean, torso_bottom),
        (cx - lean - int(8 * s), torso_bottom),
        (cx + stride_b + int(8 * s), cy - int(10 * s)),
        (cx + stride_b - int(6 * s), cy - int(10 * s))
    ], fill=INK)
    # Back shoe lifted
    d.polygon([(cx + stride_b - int(6 * s), cy - int(12 * s)), (cx + stride_b + stride_b // 2, cy - int(4 * s)), (cx + stride_b + int(8 * s), cy - int(10 * s))], fill=INK)
    
    # Swinging arms
    # Front arm swinging forward
    arm_f = -int(w * 0.7) if facing_left else int(w * 0.7)
    d.polygon([
        (cx + lean, torso_top + int(10 * s)),
        (cx + lean + int(10 * s), torso_top + int(10 * s)),
        (cx + arm_f + int(8 * s), torso_bottom + int(5 * s)),
        (cx + arm_f, torso_bottom + int(5 * s))
    ], fill=INK)
    # Back arm swinging backward
    arm_b = int(w * 0.6) if facing_left else -int(w * 0.6)
    d.polygon([
        (cx - lean, torso_top + int(10 * s)),
        (cx - lean - int(10 * s), torso_top + int(10 * s)),
        (cx + arm_b - int(6 * s), torso_bottom),
        (cx + arm_b, torso_bottom)
    ], fill=INK)

def draw_person_seated(d, cx, cy, facing_left=True):
    """Draw an author/engineer seated at a desk."""
    s = SCALE
    head_r = 38 * s
    head_cy = cy - 140 * s
    d.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r], fill=INK)
    # Profile
    px = cx - head_r - 4 * s if facing_left else cx + head_r + 4 * s
    d.polygon([(cx, head_cy - 4 * s), (px, head_cy + 2 * s), (cx, head_cy + 8 * s)], fill=INK)
    
    # Torso leaning forward
    torso_top = head_cy + head_r + 6 * s
    torso_bottom = cy + 20 * s
    d.polygon([
        (cx - 36 * s, torso_top),
        (cx + 36 * s, torso_top),
        (cx + (18 if facing_left else 48) * s, torso_bottom),
        (cx - (48 if facing_left else 18) * s, torso_bottom)
    ], fill=INK)
    
    # Seated thighs
    thigh_start_x = cx - 48 * s if facing_left else cx - 18 * s
    thigh_end_x = thigh_start_x - 110 * s if facing_left else thigh_start_x + 130 * s
    thigh_y = torso_bottom + 15 * s
    d.polygon([
        (thigh_start_x, torso_bottom - 15 * s),
        (thigh_start_x + (35 * s if facing_left else -35 * s), torso_bottom - 15 * s),
        (thigh_end_x, thigh_y + 35 * s),
        (thigh_end_x + (15 * s if facing_left else -15 * s), thigh_y + 60 * s),
        (thigh_start_x, torso_bottom + 45 * s)
    ], fill=INK)
    
    # Lower legs
    shin_x = thigh_end_x + (10 * s if facing_left else -10 * s)
    shin_bottom = cy + 180 * s
    d.rectangle([shin_x - 16 * s, thigh_y + 45 * s, shin_x + 16 * s, shin_bottom], fill=INK)
    # Shoe
    shoe_front = shin_x - 40 * s if facing_left else shin_x + 40 * s
    d.polygon([(shin_x - 16 * s, shin_bottom - 8 * s), (shoe_front, shin_bottom), (shin_x + 16 * s, shin_bottom)], fill=INK)
    
    # Arms reaching toward keyboard / controls
    arm_start_x = cx - 25 * s if facing_left else cx + 25 * s
    arm_end_x = arm_start_x - 120 * s if facing_left else arm_start_x + 120 * s
    elbow_x = arm_start_x - 65 * s if facing_left else arm_start_x + 65 * s
    d.polygon([
        (arm_start_x, torso_top + 15 * s),
        (elbow_x, torso_top + 75 * s),
        (arm_end_x, torso_top + 95 * s),
        (arm_end_x + 8 * s, torso_top + 115 * s),
        (elbow_x + 18 * s, torso_top + 95 * s),
        (arm_start_x + 18 * s, torso_top + 25 * s)
    ], fill=INK)


# ==============================================================================
# 1. RUVIEW: WI-FI SPATIAL INTELLIGENCE & VITAL SIGN MONITORING
# ==============================================================================
def render_ruview():
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    s = SCALE
    
    # Deep architectural cutaway room with vanishing point
    vp_x, vp_y = int(W * 0.46), int(H * 0.38)
    horizon_y = int(H * 0.62)
    draw_perspective_room(d, vp_x, vp_y, horizon_y, wall_step=56)
    
    # Structural Partition Wall (Center architectural cross-section dividing rooms)
    wall_x1 = int(W * 0.44)
    wall_x2 = int(W * 0.50)
    
    # Studs & wall cross-section hatching
    d.rectangle([wall_x1, 0, wall_x2, H], fill=INK)
    # Stud cavity cutaways (Cream paper slots with wood studs)
    stud_w = 12 * s
    for sy in range(int(60 * s), int(H * 0.85), int(120 * s)):
        d.rectangle([wall_x1 + 10 * s, sy, wall_x2 - 10 * s, sy + 80 * s], fill=CREAM)
        # Diagonal architectural cross-hatch inside stud
        d.line([(wall_x1 + 10 * s, sy), (wall_x2 - 10 * s, sy + 80 * s)], fill=GRID_ACCENT, width=2 * s)
        d.line([(wall_x1 + 10 * s, sy + 80 * s), (wall_x2 - 10 * s, sy)], fill=GRID_ACCENT, width=2 * s)
    
    # Left Room: Public Living / Router Room
    # Window on far left wall in perspective
    win_x1, win_y1, win_x2, win_y2 = int(W * 0.04), int(H * 0.12), int(W * 0.16), int(H * 0.52)
    d.polygon([(win_x1, win_y1), (win_x2, win_y1 + int(20 * s)), (win_x2, win_y2 - int(20 * s)), (win_x1, win_y2)], fill=INK)
    # Window panes
    d.polygon([(win_x1 + 6 * s, win_y1 + 6 * s), (win_x2 - 6 * s, win_y1 + 24 * s), (win_x2 - 6 * s, win_y2 - 24 * s), (win_x1 + 6 * s, win_y2 - 6 * s)], fill=CREAM)
    d.line([(win_x1 + 6 * s, (win_y1 + win_y2) // 2), (win_x2 - 6 * s, (win_y1 + win_y2) // 2)], fill=INK, width=2 * s)
    d.line([((win_x1 + win_x2) // 2, win_y1 + 15 * s), ((win_x1 + win_x2) // 2, win_y2 - 15 * s)], fill=INK, width=2 * s)
    
    # Router credenza / shelf
    desk_x1, desk_y1 = int(W * 0.14), int(H * 0.48)
    desk_x2, desk_y2 = int(W * 0.38), int(H * 0.70)
    d.polygon([(desk_x1, desk_y1), (desk_x2, desk_y1 + int(10 * s)), (desk_x2, desk_y2), (desk_x1, desk_y2 - int(10 * s))], fill=INK)
    # Desk legs
    d.rectangle([desk_x1 + 15 * s, desk_y2 - 10 * s, desk_x1 + 25 * s, int(H * 0.88)], fill=INK)
    d.rectangle([desk_x2 - 25 * s, desk_y2, desk_x2 - 15 * s, int(H * 0.90)], fill=INK)
    
    # Commodity Wi-Fi Router (Detailed hardware)
    r_cx, r_cy = int(W * 0.26), desk_y1 - int(12 * s)
    r_w, r_h = 56 * s, 16 * s
    d.rectangle([r_cx - r_w, r_cy - r_h, r_cx + r_w, r_cy], fill=INK)
    # Dual adjustable dipole antennas
    d.line([(r_cx - 36 * s, r_cy - r_h), (r_cx - 52 * s, r_cy - 70 * s)], fill=INK, width=4 * s)
    d.line([(r_cx + 36 * s, r_cy - r_h), (r_cx + 52 * s, r_cy - 70 * s)], fill=INK, width=4 * s)
    # Router status LEDs
    for lx in range(r_cx - 30 * s, r_cx + 30 * s, 12 * s):
        d.rectangle([lx, r_cy - 10 * s, lx + 4 * s, r_cy - 6 * s], fill=CREAM)
        
    # Concentric CSI (Channel State Information) Radio Waves passing through the wall
    # Drawn as precision radio wave contours
    origin_x, origin_y = r_cx + 40 * s, r_cy - 50 * s
    for radius in range(int(100 * s), int(700 * s), int(60 * s)):
        # Wave arc in subtle ink/grid penetrating into adjacent room
        bbox = [origin_x - radius, origin_y - radius, origin_x + radius, origin_y + radius]
        d.arc(bbox, start=-40, end=40, fill=INK, width=2 * s)
        
    # Bold Vermilion Red-Orange Accent 1: Active penetrating CSI Wavefront
    active_rad = int(380 * s)
    d.arc([origin_x - active_rad, origin_y - active_rad, origin_x + active_rad, origin_y + active_rad], start=-35, end=35, fill=VERM, width=4 * s)
    
    # Router active transmission pulse in Vermilion
    d.ellipse([r_cx + 34 * s, r_cy - 12 * s, r_cx + 42 * s, r_cy - 4 * s], fill=VERM)
    d.line([(r_cx + 46 * s, r_cy - 68 * s), (r_cx + 58 * s, r_cy - 72 * s)], fill=VERM, width=3 * s)
    
    # Right Room: Hidden Subject (Private room behind opaque wall)
    # Furniture silhouettes in right room
    # Modern armchair
    chair_x = int(W * 0.82)
    chair_y = int(H * 0.64)
    d.polygon([(chair_x, chair_y), (chair_x + 90 * s, chair_y - 20 * s), (chair_x + 130 * s, chair_y + 40 * s), (chair_x + 30 * s, chair_y + 60 * s)], fill=INK)
    d.rectangle([chair_x + 30 * s, chair_y - 50 * s, chair_x + 110 * s, chair_y], fill=INK)
    # Floor reading lamp
    lamp_x = int(W * 0.94)
    d.line([(lamp_x, int(H * 0.28)), (lamp_x, int(H * 0.74))], fill=INK, width=3 * s)
    d.polygon([(lamp_x - 20 * s, int(H * 0.28)), (lamp_x + 20 * s, int(H * 0.28)), (lamp_x + 30 * s, int(H * 0.35)), (lamp_x - 30 * s, int(H * 0.35))], fill=INK)
    d.ellipse([lamp_x - 25 * s, int(H * 0.73), lamp_x + 25 * s, int(H * 0.76)], fill=INK)
    
    # Human Silhouette walking in right room (Completely occluded by wall)
    walker_x = int(W * 0.68)
    walker_y = int(H * 0.76)
    draw_person_walking(d, walker_x, walker_y, height=390, facing_left=True)
    
    # Bold Vermilion Red-Orange Accent 2: Micro-Doppler Vital Sign Reticle & Cardiac Waveform
    # Targeting chest coordinates
    chest_x = walker_x - 14 * s
    chest_y = walker_y - 210 * s
    reticle_r = 44 * s
    # Outer crosshairs
    d.line([(chest_x - reticle_r - 20 * s, chest_y), (chest_x + reticle_r + 20 * s, chest_y)], fill=VERM, width=2 * s)
    d.line([(chest_x, chest_y - reticle_r - 20 * s), (chest_x, chest_y + reticle_r + 20 * s)], fill=VERM, width=2 * s)
    # Reticle brackets
    d.arc([chest_x - reticle_r, chest_y - reticle_r, chest_x + reticle_r, chest_y + reticle_r], start=25, end=65, fill=VERM, width=3 * s)
    d.arc([chest_x - reticle_r, chest_y - reticle_r, chest_x + reticle_r, chest_y + reticle_r], start=115, end=155, fill=VERM, width=3 * s)
    d.arc([chest_x - reticle_r, chest_y - reticle_r, chest_x + reticle_r, chest_y + reticle_r], start=205, end=245, fill=VERM, width=3 * s)
    d.arc([chest_x - reticle_r, chest_y - reticle_r, chest_x + reticle_r, chest_y + reticle_r], start=295, end=335, fill=VERM, width=3 * s)
    
    # Micro-Doppler ECG Respiration Waveform Banner in Vermilion
    wave_x1 = chest_x + 55 * s
    wave_y1 = chest_y - 30 * s
    wave_w, wave_h = 160 * s, 60 * s
    d.rectangle([wave_x1, wave_y1, wave_x1 + wave_w, wave_y1 + wave_h], fill=CREAM, outline=VERM, width=2 * s)
    # ECG trace line in Vermilion
    pts = [
        (wave_x1 + 10 * s, wave_y1 + 30 * s),
        (wave_x1 + 35 * s, wave_y1 + 30 * s),
        (wave_x1 + 45 * s, wave_y1 + 20 * s),
        (wave_x1 + 52 * s, wave_y1 + 45 * s),
        (wave_x1 + 60 * s, wave_y1 + 8 * s),
        (wave_x1 + 68 * s, wave_y1 + 48 * s),
        (wave_x1 + 75 * s, wave_y1 + 30 * s),
        (wave_x1 + 105 * s, wave_y1 + 30 * s),
        (wave_x1 + 115 * s, wave_y1 + 22 * s),
        (wave_x1 + 122 * s, wave_y1 + 44 * s),
        (wave_x1 + 130 * s, wave_y1 + 10 * s),
        (wave_x1 + 138 * s, wave_y1 + 46 * s),
        (wave_x1 + 145 * s, wave_y1 + 30 * s),
        (wave_x1 + wave_w - 10 * s, wave_y1 + 30 * s)
    ]
    d.line(pts, fill=VERM, width=3 * s)
    # Data label
    d.text((wave_x1 + 12 * s, wave_y1 + 6 * s), "VITAL SIGN: 72 BPM // CSI PHASE", fill=INK, font=FONT_TINY)
    
    # Save final Lanczos downsampled image
    im_final = im.resize((W_FINAL, H_FINAL), Image.LANCZOS)
    out_path = "demo-news/public/images/ruview-rust-wifi-spatial-intelligence.jpg"
    im_final.save(out_path, quality=95)
    print("RuView illustration saved to:", out_path)


# ==============================================================================
# 2. XIAOLAI: THE CRAFT OF SELF-TEACHING (PROOF-OF-WORK JUPYTER & GIT DAG)
# ==============================================================================
def render_xiaolai():
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    s = SCALE
    
    vp_x, vp_y = int(W * 0.38), int(H * 0.42)
    horizon_y = int(H * 0.58)
    draw_perspective_room(d, vp_x, vp_y, horizon_y, wall_step=60)
    
    # Left Studio Workspace: Main Desk
    desk_left, desk_right = int(W * 0.08), int(W * 0.56)
    desk_top, desk_bottom = int(H * 0.52), int(H * 0.76)
    d.polygon([(desk_left + 40 * s, desk_top), (desk_right - 20 * s, desk_top), (desk_right, desk_bottom), (desk_left, desk_bottom)], fill=INK)
    d.rectangle([desk_left + 30 * s, desk_bottom, desk_left + 50 * s, H], fill=INK)
    d.rectangle([desk_right - 50 * s, desk_bottom, desk_right - 30 * s, H], fill=INK)
    
    # Ultra-wide curved developer monitor
    mon_x1, mon_y1 = int(W * 0.12), int(H * 0.16)
    mon_x2, mon_y2 = int(W * 0.48), int(H * 0.52)
    d.polygon([(mon_x1, mon_y1), (mon_x2, mon_y1), (mon_x2 - 15 * s, mon_y2), (mon_x1 + 15 * s, mon_y2)], fill=INK)
    # Screen bezel cutout
    scr_x1, scr_y1 = mon_x1 + 12 * s, mon_y1 + 10 * s
    scr_x2, scr_y2 = mon_x2 - 12 * s, mon_y2 - 10 * s
    d.polygon([(scr_x1, scr_y1), (scr_x2, scr_y1), (scr_x2 - 12 * s, scr_y2), (scr_x1 + 12 * s, scr_y2)], fill=CREAM)
    
    # Jupyter Notebook UI layout on screen
    # Toolbar
    d.rectangle([scr_x1 + 6 * s, scr_y1 + 4 * s, scr_x2 - 6 * s, scr_y1 + 22 * s], fill=INK)
    d.text((scr_x1 + 12 * s, scr_y1 + 6 * s), "JupyterLab - the-craft-of-selfteaching.ipynb [Python 3.12]", fill=CREAM, font=FONT_TINY)
    
    # Code Cell 1
    c1_y = scr_y1 + 30 * s
    d.rectangle([scr_x1 + 10 * s, c1_y, scr_x2 - 10 * s, c1_y + 40 * s], outline=INK, width=s)
    d.text((scr_x1 + 15 * s, c1_y + 4 * s), "[In 1]:", fill=GRID_ACCENT, font=FONT_TINY)
    d.text((scr_x1 + 55 * s, c1_y + 4 * s), "def proof_of_work(commit_hash, nonce=0):", fill=INK, font=FONT_CODE_BOLD)
    d.text((scr_x1 + 55 * s, c1_y + 18 * s), "    return hashlib.sha256(f'{commit_hash}:{nonce}').hexdigest()", fill=INK, font=FONT_CODE)
    
    # Code Cell 2 (Active execution)
    c2_y = c1_y + 50 * s
    d.rectangle([scr_x1 + 10 * s, c2_y, scr_x2 - 10 * s, c2_y + 55 * s], outline=INK, width=s)
    d.text((scr_x1 + 15 * s, c2_y + 4 * s), "[In 2]:", fill=GRID_ACCENT, font=FONT_TINY)
    d.text((scr_x1 + 55 * s, c2_y + 4 * s), "# Verifying local git progress against curriculum", fill=GRID_ACCENT, font=FONT_CODE)
    d.text((scr_x1 + 55 * s, c2_y + 18 * s), "validate_learner_commits(repo='xiaolai/craft')", fill=INK, font=FONT_CODE_BOLD)
    
    # Bold Vermilion Red-Orange Accent 1: Active Cell Execution Button & Cursor
    d.rectangle([scr_x1 + 10 * s, c2_y, scr_x1 + 14 * s, c2_y + 55 * s], fill=VERM)
    d.text((scr_x2 - 80 * s, c2_y + 4 * s), "[RUNNING *]", fill=VERM, font=FONT_CODE_BOLD)
    
    # Monitor stand
    d.rectangle([(mon_x1 + mon_x2) // 2 - 12 * s, mon_y2, (mon_x1 + mon_x2) // 2 + 12 * s, desk_top + 10 * s], fill=INK)
    d.polygon([((mon_x1 + mon_x2) // 2 - 35 * s, desk_top + 10 * s), ((mon_x1 + mon_x2) // 2 + 35 * s, desk_top + 10 * s), ((mon_x1 + mon_x2) // 2 + 45 * s, desk_top + 18 * s), ((mon_x1 + mon_x2) // 2 - 45 * s, desk_top + 18 * s)], fill=INK)
    
    # Seated Programmer Silhouette
    dev_x = int(W * 0.44)
    dev_y = int(H * 0.46)
    # Mesh office chair
    d.polygon([(dev_x + 35 * s, int(H * 0.35)), (dev_x + 65 * s, int(H * 0.35)), (dev_x + 50 * s, int(H * 0.70)), (dev_x + 20 * s, int(H * 0.70))], fill=INK)
    d.rectangle([dev_x + 35 * s, int(H * 0.70), dev_x + 45 * s, int(H * 0.88)], fill=INK)
    d.line([(dev_x + 10 * s, int(H * 0.88)), (dev_x + 70 * s, int(H * 0.88))], fill=INK, width=6 * s)
    # Person
    draw_person_seated(d, dev_x, dev_y, facing_left=True)
    
    # Right Background: Massive Wall-Mounted Git Commit DAG (Proof-of-Work Visualization)
    dag_x1, dag_y1 = int(W * 0.60), int(H * 0.10)
    dag_x2, dag_y2 = int(W * 0.96), int(H * 0.75)
    
    # Board backing
    d.rectangle([dag_x1, dag_y1, dag_x2, dag_y2], fill=CREAM, outline=INK, width=2 * s)
    # Title banner on board
    d.rectangle([dag_x1, dag_y1, dag_x2, dag_y1 + 28 * s], fill=INK)
    d.text((dag_x1 + 15 * s, dag_y1 + 6 * s), "PROOF OF WORK: GIT COMMIT VERIFICATION GRAPH [18.5k STARS]", fill=CREAM, font=FONT_SUBTITLE)
    
    # Commit DAG Nodes and Branches
    # Main trunk nodes
    trunk_nodes = [
        (dag_x1 + 60 * s, dag_y2 - 60 * s, "init: 0.1"),
        (dag_x1 + 120 * s, dag_y2 - 120 * s, "ch01: f82a"),
        (dag_x1 + 180 * s, dag_y2 - 180 * s, "ch02: c31b"),
        (dag_x1 + 240 * s, dag_y2 - 240 * s, "ch03: 7a9e"),
        (dag_x1 + 300 * s, dag_y2 - 300 * s, "ch04: d401"),
        (dag_x1 + 360 * s, dag_y2 - 360 * s, "HEAD: v2.0")
    ]
    # Connect trunk line
    for i in range(len(trunk_nodes) - 1):
        x1, y1, _ = trunk_nodes[i]
        x2, y2, _ = trunk_nodes[i+1]
        d.line([(x1, y1), (x2, y2)], fill=INK, width=3 * s)
        
    # Feature branches / fork branches
    fork1 = [
        (trunk_nodes[1][0], trunk_nodes[1][1]),
        (trunk_nodes[1][0] + 60 * s, trunk_nodes[1][1] - 40 * s),
        (trunk_nodes[3][0], trunk_nodes[3][1])
    ]
    d.line([fork1[0], fork1[1], fork1[2]], fill=INK, width=2 * s)
    
    fork2 = [
        (trunk_nodes[2][0], trunk_nodes[2][1]),
        (trunk_nodes[2][0] + 80 * s, trunk_nodes[2][1] - 30 * s),
        (trunk_nodes[4][0], trunk_nodes[4][1])
    ]
    d.line([fork2[0], fork2[1], fork2[2]], fill=INK, width=2 * s)
    
    # Draw standard nodes
    for x, y, label in trunk_nodes[:-1]:
        d.ellipse([x - 10 * s, y - 10 * s, x + 10 * s, y + 10 * s], fill=INK)
        d.text((x + 14 * s, y - 8 * s), label, fill=INK, font=FONT_TINY)
    d.ellipse([fork1[1][0] - 8 * s, fork1[1][1] - 8 * s, fork1[1][0] + 8 * s, fork1[1][1] + 8 * s], fill=INK)
    d.ellipse([fork2[1][0] - 8 * s, fork2[1][1] - 8 * s, fork2[1][0] + 8 * s, fork2[1][1] + 8 * s], fill=INK)
    
    # Bold Vermilion Red-Orange Accent 2: Summit HEAD Commit Node & PoW Verified Badge
    head_x, head_y, head_lbl = trunk_nodes[-1]
    d.ellipse([head_x - 16 * s, head_y - 16 * s, head_x + 16 * s, head_y + 16 * s], fill=VERM)
    d.ellipse([head_x - 8 * s, head_y - 8 * s, head_x + 8 * s, head_y + 8 * s], fill=CREAM)
    
    # Summit tag flag in Vermilion
    flag_x = head_x + 22 * s
    d.polygon([(flag_x, head_y - 14 * s), (flag_x + 110 * s, head_y - 14 * s), (flag_x + 110 * s, head_y + 14 * s), (flag_x, head_y + 14 * s)], fill=VERM)
    d.text((flag_x + 8 * s, head_y - 8 * s), "HEAD -> v2.0 [POW]", fill=CREAM, font=FONT_CODE_BOLD)
    
    im_final = im.resize((W_FINAL, H_FINAL), Image.LANCZOS)
    out_path = "demo-news/public/images/xiaolai-craft-of-selfteaching.jpg"
    im_final.save(out_path, quality=95)
    print("Xiaolai illustration saved to:", out_path)


# ==============================================================================
# 3. EXPO SKILLS: AI AGENT NATIVE UI (4-STATE ARCHITECTURE & ROBOTIC ASSEMBLY)
# ==============================================================================
def render_expo_skills():
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    s = SCALE
    
    vp_x, vp_y = int(W * 0.50), int(H * 0.35)
    horizon_y = int(H * 0.60)
    draw_perspective_room(d, vp_x, vp_y, horizon_y, wall_step=64)
    
    # Background Wall: Blueprint Board "4-STATE NATIVE ARCHITECTURE"
    bp_x1, bp_y1 = int(W * 0.08), int(H * 0.08)
    bp_x2, bp_y2 = int(W * 0.92), int(H * 0.44)
    d.rectangle([bp_x1, bp_y1, bp_x2, bp_y2], fill=CREAM, outline=INK, width=2 * s)
    d.rectangle([bp_x1, bp_y1, bp_x2, bp_y1 + 24 * s], fill=INK)
    d.text((bp_x1 + 15 * s, bp_y1 + 5 * s), "EXPO/SKILLS SPECIFICATION: NATIVE COMPONENT 4-STATE ARCHITECTURE", fill=CREAM, font=FONT_SUBTITLE)
    
    # 4 Architecture State Cards on blueprint board
    card_w = (bp_x2 - bp_x1 - 50 * s) // 4
    states = [
        ("STATE 01: LOADING", "Skeleton layout & shimmer primitives"),
        ("STATE 02: EMPTY", "Ghost state with action trigger"),
        ("STATE 03: ERROR", "Retry boundary & alert feedback"),
        ("STATE 04: CONTENT", "Active viewport layout primitives")
    ]
    for idx, (title, desc) in enumerate(states):
        cx1 = bp_x1 + 10 * s + idx * (card_w + 10 * s)
        cy1 = bp_y1 + 35 * s
        cx2 = cx1 + card_w
        cy2 = bp_y2 - 15 * s
        d.rectangle([cx1, cy1, cx2, cy2], fill=CREAM, outline=GRID_ACCENT, width=s)
        d.rectangle([cx1, cy1, cx2, cy1 + 18 * s], fill=INK)
        d.text((cx1 + 6 * s, cy1 + 3 * s), title, fill=CREAM, font=FONT_TINY)
        # Diagram lines inside state card
        if idx == 0:
            # Loading bars
            d.rectangle([cx1 + 10 * s, cy1 + 30 * s, cx2 - 10 * s, cy1 + 42 * s], fill=GRID_ACCENT)
            d.rectangle([cx1 + 10 * s, cy1 + 50 * s, cx2 - 25 * s, cy1 + 60 * s], fill=GRID_ACCENT)
        elif idx == 1:
            # Empty dashed box
            d.rectangle([cx1 + 15 * s, cy1 + 30 * s, cx2 - 15 * s, cy2 - 15 * s], outline=GRID_ACCENT, width=s)
        elif idx == 2:
            # Error triangle
            tx = (cx1 + cx2) // 2
            d.polygon([(tx, cy1 + 30 * s), (tx + 20 * s, cy2 - 20 * s), (tx - 20 * s, cy2 - 20 * s)], outline=INK, width=2 * s)
        elif idx == 3:
            # Content state (Highlighted)
            d.rectangle([cx1 + 8 * s, cy1 + 26 * s, cx2 - 8 * s, cy1 + 46 * s], fill=INK)
            d.rectangle([cx1 + 8 * s, cy1 + 52 * s, cx2 - 8 * s, cy1 + 72 * s], fill=INK)
            d.rectangle([cx1, cy1, cx2, cy1 + 18 * s], fill=VERM)
            d.text((cx1 + 6 * s, cy1 + 3 * s), title, fill=CREAM, font=FONT_TINY)
            
    # Center Stage: Precision Smartphone Plinth & Hardware
    phone_cx = int(W * 0.45)
    phone_w, phone_h = 130 * s, 260 * s
    phone_top = int(H * 0.40)
    phone_bottom = phone_top + phone_h
    
    # Plinth base
    d.polygon([
        (phone_cx - 100 * s, phone_bottom + 40 * s),
        (phone_cx + 100 * s, phone_bottom + 40 * s),
        (phone_cx + 140 * s, int(H * 0.90)),
        (phone_cx - 140 * s, int(H * 0.90))
    ], fill=INK)
    d.rectangle([phone_cx - 30 * s, phone_bottom, phone_cx + 30 * s, phone_bottom + 45 * s], fill=INK)
    
    # Phone Body (Monolithic silhouette)
    d.rectangle([phone_cx - phone_w, phone_top, phone_cx + phone_w, phone_bottom], fill=INK)
    # Bezel screen cutout (Cream paper surface)
    sc_w, sc_h = phone_w - 12 * s, phone_h - 14 * s
    sc_x1, sc_y1 = phone_cx - sc_w, phone_top + 10 * s
    sc_x2, sc_y2 = phone_cx + sc_w, phone_bottom - 10 * s
    d.rectangle([sc_x1, sc_y1, sc_x2, sc_y2], fill=CREAM)
    
    # Phone Screen UI: React Native / Expo Native UI Layout
    # Dynamic island / camera notch
    d.ellipse([phone_cx - 14 * s, sc_y1 + 4 * s, phone_cx + 14 * s, sc_y1 + 14 * s], fill=INK)
    
    # App header bar
    d.rectangle([sc_x1 + 10 * s, sc_y1 + 24 * s, sc_x2 - 10 * s, sc_y1 + 48 * s], fill=INK)
    d.text((sc_x1 + 18 * s, sc_y1 + 28 * s), "Expo Router // Native UI", fill=CREAM, font=FONT_TINY)
    
    # Search / Filter Bar
    d.rectangle([sc_x1 + 10 * s, sc_y1 + 56 * s, sc_x2 - 10 * s, sc_y1 + 76 * s], outline=INK, width=s)
    d.text((sc_x1 + 18 * s, sc_y1 + 60 * s), "Search components...", fill=GRID_ACCENT, font=FONT_TINY)
    
    # Feed items (Native card primitives)
    for fy in range(int(sc_y1 + 86 * s), int(sc_y2 - 60 * s), int(52 * s)):
        d.rectangle([sc_x1 + 10 * s, fy, sc_x2 - 10 * s, fy + 44 * s], fill=CREAM, outline=INK, width=s)
        # Thumbnail box
        d.rectangle([sc_x1 + 16 * s, fy + 6 * s, sc_x1 + 48 * s, fy + 38 * s], fill=INK)
        # Content bars
        d.rectangle([sc_x1 + 56 * s, fy + 10 * s, sc_x2 - 20 * s, fy + 18 * s], fill=INK)
        d.rectangle([sc_x1 + 56 * s, fy + 24 * s, sc_x2 - 50 * s, fy + 32 * s], fill=GRID_ACCENT)
        
    # Bottom Tab Navigation Bar
    d.rectangle([sc_x1 + 10 * s, sc_y2 - 32 * s, sc_x2 - 10 * s, sc_y2 - 6 * s], fill=INK)
    for tx in range(sc_x1 + 25 * s, sc_x2 - 15 * s, (sc_w * 2 - 40 * s) // 4):
        d.ellipse([tx - 6 * s, sc_y2 - 22 * s, tx + 6 * s, sc_y2 - 10 * s], fill=CREAM)
        
    # Bold Vermilion Red-Orange Accent 1: Active Component State Pill on Screen
    pill_y = sc_y1 + 86 * s + 6 * s
    d.polygon([(sc_x2 - 68 * s, pill_y), (sc_x2 - 16 * s, pill_y), (sc_x2 - 16 * s, pill_y + 16 * s), (sc_x2 - 68 * s, pill_y + 16 * s)], fill=VERM)
    d.text((sc_x2 - 64 * s, pill_y + 2 * s), "CONTENT", fill=CREAM, font=FONT_TINY)
    
    # Right Flank: High-Precision Articulated AI Robotic Arm
    arm_base_x = int(W * 0.85)
    arm_base_y = int(H * 0.85)
    # Robot turntable base
    d.polygon([
        (arm_base_x - 70 * s, arm_base_y),
        (arm_base_x + 70 * s, arm_base_y),
        (arm_base_x + 90 * s, H),
        (arm_base_x - 90 * s, H)
    ], fill=INK)
    # Shoulder joint
    shoulder_x, shoulder_y = arm_base_x, arm_base_y - 40 * s
    d.ellipse([shoulder_x - 30 * s, shoulder_y - 30 * s, shoulder_x + 30 * s, shoulder_y + 30 * s], fill=INK)
    # Upper arm boom reaching left toward phone
    elbow_x, elbow_y = int(W * 0.68), int(H * 0.46)
    d.line([(shoulder_x, shoulder_y), (elbow_x, elbow_y)], fill=INK, width=16 * s)
    d.ellipse([elbow_x - 22 * s, elbow_y - 22 * s, elbow_x + 22 * s, elbow_y + 22 * s], fill=INK)
    # Forearm
    wrist_x, wrist_y = phone_cx + phone_w + 10 * s, phone_top + 100 * s
    d.line([(elbow_x, elbow_y), (wrist_x, wrist_y)], fill=INK, width=12 * s)
    d.ellipse([wrist_x - 16 * s, wrist_y - 16 * s, wrist_x + 16 * s, wrist_y + 16 * s], fill=INK)
    
    # Dual precision gripper end-effector
    d.polygon([(wrist_x, wrist_y - 10 * s), (wrist_x - 25 * s, wrist_y - 18 * s), (wrist_x - 30 * s, wrist_y - 12 * s), (wrist_x - 10 * s, wrist_y - 6 * s)], fill=INK)
    d.polygon([(wrist_x, wrist_y + 10 * s), (wrist_x - 25 * s, wrist_y + 18 * s), (wrist_x - 30 * s, wrist_y + 12 * s), (wrist_x - 10 * s, wrist_y + 6 * s)], fill=INK)
    
    # Bold Vermilion Red-Orange Accent 2: Alignment Laser Crosshairs from Gripper
    laser_target_x = phone_cx + 40 * s
    laser_target_y = phone_top + 100 * s
    d.line([(wrist_x - 28 * s, wrist_y), (laser_target_x, laser_target_y)], fill=VERM, width=2 * s)
    # Reticle at target
    d.ellipse([laser_target_x - 10 * s, laser_target_y - 10 * s, laser_target_x + 10 * s, laser_target_y + 10 * s], outline=VERM, width=2 * s)
    d.line([(laser_target_x - 16 * s, laser_target_y), (laser_target_x + 16 * s, laser_target_y)], fill=VERM, width=2 * s)
    d.line([(laser_target_x, laser_target_y - 16 * s), (laser_target_x, laser_target_y + 16 * s)], fill=VERM, width=2 * s)
    
    # Left Foreground: AI Developer / Inspector silhouette
    draw_person_standing(d, int(W * 0.16), int(H * 0.88), height=380, facing_left=False, arms_crossed=True)
    
    im_final = im.resize((W_FINAL, H_FINAL), Image.LANCZOS)
    out_path = "demo-news/public/images/expo-skills-shell-ai-agent-native-ui.jpg"
    im_final.save(out_path, quality=95)
    print("Expo Skills illustration saved to:", out_path)


# ==============================================================================
# 4. MACRO: AGPL RUST WORKSPACE & MODEL CONTEXT PROTOCOL (MCP)
# ==============================================================================
def render_macro():
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    s = SCALE
    
    # Cathedral enterprise data center in dramatic central 1-point perspective
    vp_x, vp_y = int(W * 0.50), int(H * 0.44)
    horizon_y = int(H * 0.58)
    draw_perspective_room(d, vp_x, vp_y, horizon_y, wall_step=50)
    
    # Left and Right Monolithic Blade Server Racks (Perspective columns)
    # Left racks
    l_racks = [
        (int(W * 0.02), int(W * 0.16), int(H * 0.08), int(H * 0.88)),
        (int(W * 0.18), int(W * 0.28), int(H * 0.18), int(H * 0.78)),
        (int(W * 0.30), int(W * 0.36), int(H * 0.28), int(H * 0.68))
    ]
    for rx1, rx2, ry1, ry2 in l_racks:
        d.polygon([(rx1, ry1), (rx2, ry1 + 25 * s), (rx2, ry2 - 25 * s), (rx1, ry2)], fill=INK)
        # Server blade slots & vents
        h_total = ry2 - ry1 - 50 * s
        num_blades = 14
        b_h = h_total // num_blades
        for b in range(num_blades):
            by = ry1 + 25 * s + b * b_h
            d.line([(rx1 + 10 * s, by), (rx2 - 8 * s, by + 4 * s)], fill=CREAM, width=s)
            # Status LED dots
            d.ellipse([rx2 - 16 * s, by + 2 * s, rx2 - 12 * s, by + 6 * s], fill=CREAM)
            
    # Right racks
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
            
    # Overhead cable raceways / gantries connecting racks across ceiling
    for gy in [int(H * 0.12), int(H * 0.22)]:
        d.line([(0, gy), (W, gy)], fill=INK, width=4 * s)
        for gx in range(int(W * 0.10), int(W * 0.90), 80 * s):
            d.line([(gx, gy), (gx + 15 * s, gy + 15 * s)], fill=INK, width=2 * s)
            
    # Center Elevated Walkway & Architect Silhouette
    plat_w = int(W * 0.28)
    plat_x1, plat_x2 = vp_x - plat_w // 2, vp_x + plat_w // 2
    plat_y = int(H * 0.76)
    d.polygon([(plat_x1, plat_y), (plat_x2, plat_y), (plat_x2 + 40 * s, H), (plat_x1 - 40 * s, H)], fill=INK)
    d.line([(plat_x1 - 40 * s, plat_y), (plat_x2 + 40 * s, plat_y)], fill=CREAM, width=2 * s)
    
    # Systems Architect standing firm in center observing
    draw_person_standing(d, vp_x, plat_y + int(45 * s), height=340, facing_left=False, arms_crossed=True)
    
    # Center Upper Space: Model Context Protocol (MCP) Nexus & Unified Tool Graph
    mcp_cx, mcp_cy = vp_x, int(H * 0.28)
    
    # Four satellite service nodes converging into MCP:
    # 1. Email (Top-left)
    # 2. Chat (Top-right)
    # 3. Tasks / Kanban (Bottom-left)
    # 4. CRM / Memory (Bottom-right)
    nodes = [
        (mcp_cx - 160 * s, mcp_cy - 80 * s, "EMAIL [IMAP/SMTP]"),
        (mcp_cx + 160 * s, mcp_cy - 80 * s, "CHAT [MATRIX/WEBSOCKET]"),
        (mcp_cx - 160 * s, mcp_cy + 80 * s, "TASKS [GRAPH DB]"),
        (mcp_cx + 160 * s, mcp_cy + 80 * s, "CRM [SHARED AI MEMORY]")
    ]
    # Data bus lines converging to center
    for nx, ny, label in nodes:
        d.line([(nx, ny), (mcp_cx, mcp_cy)], fill=INK, width=3 * s)
        # Node box
        nw, nh = 64 * s, 36 * s
        d.rectangle([nx - nw, ny - nh, nx + nw, ny + nh], fill=CREAM, outline=INK, width=2 * s)
        d.rectangle([nx - nw, ny - nh, nx + nw, ny - nh + 14 * s], fill=INK)
        d.text((nx - nw + 8 * s, ny - nh + 2 * s), label.split()[0], fill=CREAM, font=FONT_TINY)
        # Icon representation inside
        if "EMAIL" in label:
            # Envelope
            d.rectangle([nx - 24 * s, ny, nx + 24 * s, ny + 20 * s], outline=INK, width=s)
            d.line([(nx - 24 * s, ny), (nx, ny + 12 * s), (nx + 24 * s, ny)], fill=INK, width=s)
        elif "CHAT" in label:
            # Chat bubbles
            d.rectangle([nx - 24 * s, ny, nx + 12 * s, ny + 16 * s], fill=INK)
            d.rectangle([nx - 10 * s, ny + 8 * s, nx + 24 * s, ny + 24 * s], outline=INK, width=s)
        elif "TASKS" in label:
            # Checklist
            d.rectangle([nx - 20 * s, ny, nx - 12 * s, ny + 8 * s], fill=INK)
            d.line([(nx - 8 * s, ny + 4 * s), (nx + 20 * s, ny + 4 * s)], fill=INK, width=s)
            d.rectangle([nx - 20 * s, ny + 12 * s, nx - 12 * s, ny + 20 * s], fill=INK)
            d.line([(nx - 8 * s, ny + 16 * s), (nx + 20 * s, ny + 16 * s)], fill=INK, width=s)
        elif "CRM" in label:
            # Database cylinder
            d.ellipse([nx - 18 * s, ny, nx + 18 * s, ny + 8 * s], outline=INK, width=s)
            d.line([(nx - 18 * s, ny + 4 * s), (nx - 18 * s, ny + 20 * s)], fill=INK, width=s)
            d.line([(nx + 18 * s, ny + 4 * s), (nx + 18 * s, ny + 20 * s)], fill=INK, width=s)
            d.ellipse([nx - 18 * s, ny + 16 * s, nx + 18 * s, ny + 24 * s], outline=INK, width=s)
            
    # Bold Vermilion Red-Orange Accent: Hexagonal Model Context Protocol (MCP) Core Nexus
    hex_r = 52 * s
    hex_pts = []
    for angle in range(30, 390, 60):
        rad = math.radians(angle)
        hex_pts.append((mcp_cx + hex_r * math.cos(rad), mcp_cy + hex_r * math.sin(rad)))
    d.polygon(hex_pts, fill=VERM)
    # Inner hexagon cutout
    inner_pts = []
    for angle in range(30, 390, 60):
        rad = math.radians(angle)
        inner_pts.append((mcp_cx + (hex_r - 10 * s) * math.cos(rad), mcp_cy + (hex_r - 10 * s) * math.sin(rad)))
    d.polygon(inner_pts, fill=CREAM)
    # MCP text in center
    d.text((mcp_cx - 24 * s, mcp_cy - 12 * s), "MCP", fill=INK, font=FONT_CODE_BOLD)
    
    # Vermilion high-speed data pulses on the bus lines
    for nx, ny, _ in nodes:
        px = int(nx * 0.4 + mcp_cx * 0.6)
        py = int(ny * 0.4 + mcp_cy * 0.6)
        d.ellipse([px - 6 * s, py - 6 * s, px + 6 * s, py + 6 * s], fill=VERM)
        
    # Top banner
    d.rectangle([vp_x - 140 * s, int(H * 0.04), vp_x + 140 * s, int(H * 0.09)], fill=INK)
    d.text((vp_x - 128 * s, int(H * 0.05)), "42 RUST SERVICES // AGPL-3.0 WORKSPACE", fill=CREAM, font=FONT_TINY)
    
    im_final = im.resize((W_FINAL, H_FINAL), Image.LANCZOS)
    out_path = "demo-news/public/images/macro-rust-agpl-workspace-mcp.jpg"
    im_final.save(out_path, quality=95)
    print("Macro illustration saved to:", out_path)


# ==============================================================================
# 5. LINKSWIFT: DIRECT CLOUD STORAGE DOWNLOAD BYPASS
# ==============================================================================
def render_linkswift():
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    s = SCALE
    
    vp_x, vp_y = int(W * 0.50), int(H * 0.42)
    horizon_y = int(H * 0.60)
    draw_perspective_room(d, vp_x, vp_y, horizon_y, wall_step=56)
    
    # Central High-Security Cloud Storage Vault Door
    vault_cx, vault_cy = vp_x, int(H * 0.38)
    vault_r = 170 * s
    
    # Vault outer steel frame
    d.ellipse([vault_cx - vault_r - 20 * s, vault_cy - vault_r - 20 * s, vault_cx + vault_r + 20 * s, vault_cy + vault_r + 20 * s], fill=INK)
    # Rivets around outer frame
    for angle in range(0, 360, 20):
        rad = math.radians(angle)
        rx = vault_cx + (vault_r + 10 * s) * math.cos(rad)
        ry = vault_cy + (vault_r + 10 * s) * math.sin(rad)
        d.ellipse([rx - 3 * s, ry - 3 * s, rx + 3 * s, ry + 3 * s], fill=CREAM)
        
    # Inner vault door surface (Cream paper texture with steel locking spokes)
    d.ellipse([vault_cx - vault_r, vault_cy - vault_r, vault_cx + vault_r, vault_cy + vault_r], fill=CREAM, outline=INK, width=3 * s)
    # Central locking wheel hub
    d.ellipse([vault_cx - 45 * s, vault_cy - 45 * s, vault_cx + 45 * s, vault_cy + 45 * s], fill=INK)
    # 6 Vault Spokes
    for angle in range(0, 360, 60):
        rad = math.radians(angle)
        sx = vault_cx + 90 * s * math.cos(rad)
        sy = vault_cy + 90 * s * math.sin(rad)
        d.line([(vault_cx, vault_cy), (sx, sy)], fill=INK, width=6 * s)
        d.ellipse([sx - 12 * s, sy - 12 * s, sx + 12 * s, sy + 12 * s], fill=INK)
        
    # Heavy Crossed Steel Security Chains Padlocking the Cloud Storage Door
    chain_w = 16 * s
    d.line([(vault_cx - vault_r, vault_cy - vault_r), (vault_cx + vault_r, vault_cy + vault_r)], fill=INK, width=chain_w)
    d.line([(vault_cx - vault_r, vault_cy + vault_r), (vault_cx + vault_r, vault_cy - vault_r)], fill=INK, width=chain_w)
    # Chain links definition (Cream oval cutouts)
    for t in [-0.7, -0.4, -0.1, 0.2, 0.5, 0.8]:
        lx = vault_cx + int(vault_r * t)
        ly = vault_cy + int(vault_r * t)
        d.ellipse([lx - 5 * s, ly - 3 * s, lx + 5 * s, ly + 3 * s], fill=CREAM)
        lx2 = vault_cx + int(vault_r * t)
        ly2 = vault_cy - int(vault_r * t)
        d.ellipse([lx2 - 5 * s, ly2 - 3 * s, lx2 + 5 * s, ly2 + 3 * s], fill=CREAM)
        
    # Massive Central Padlock (Snapped open by LinkSwift)
    lock_cx, lock_cy = vault_cx, vault_cy
    lock_w, lock_h = 60 * s, 50 * s
    d.rectangle([lock_cx - lock_w // 2, lock_cy - lock_h // 2, lock_cx + lock_w // 2, lock_cy + lock_h // 2], fill=INK)
    # Keyhole
    d.ellipse([lock_cx - 6 * s, lock_cy - 12 * s, lock_cx + 6 * s, lock_cy], fill=CREAM)
    d.polygon([(lock_cx - 4 * s, lock_cy - 4 * s), (lock_cx + 4 * s, lock_cy - 4 * s), (lock_cx + 2 * s, lock_cy + 10 * s), (lock_cx - 2 * s, lock_cy + 10 * s)], fill=CREAM)
    
    # Left Foreground: Floating Browser / Developer Console Window
    con_x1, con_y1 = int(W * 0.08), int(H * 0.48)
    con_x2, con_y2 = int(W * 0.44), int(H * 0.88)
    d.polygon([
        (con_x1, con_y1),
        (con_x2, con_y1 + 20 * s),
        (con_x2 - 20 * s, con_y2),
        (con_x1 - 20 * s, con_y2 - 20 * s)
    ], fill=CREAM)
    d.polygon([
        (con_x1, con_y1),
        (con_x2, con_y1 + 20 * s),
        (con_x2 - 20 * s, con_y2),
        (con_x1 - 20 * s, con_y2 - 20 * s)
    ], outline=INK, width=2 * s)
    
    # Console Header
    d.polygon([(con_x1, con_y1), (con_x2, con_y1 + 20 * s), (con_x2 - 3 * s, con_y1 + 45 * s), (con_x1 - 3 * s, con_y1 + 25 * s)], fill=INK)
    d.text((con_x1 + 10 * s, con_y1 + 6 * s), "LinkSwift.js // Userscript Console [33.9k Stars]", fill=CREAM, font=FONT_TINY)
    
    # JavaScript code lines in console
    lines = [
        "> LinkSwift.intercept(downloadRequest);",
        "  [Provider]: Baidu / Aliyun / 123Drive / Quark",
        "  [Action]: Stripping desktop client payload...",
        "  [Status]: Direct CDN stream token extracted.",
        "> streamDownload(url, threads=16);"
    ]
    for idx, l in enumerate(lines):
        d.text((con_x1 + 10 * s, con_y1 + 35 * s + idx * 18 * s), l, fill=INK, font=FONT_TINY)
        
    # Bold Vermilion Red-Orange Accent: Piercing Direct Download Lightning Vector
    # Punching straight through the broken padlock and vault door out toward the viewer
    arrow_tip_x = int(W * 0.72)
    arrow_tip_y = int(H * 0.72)
    
    # Razor lightning arrow in Vermilion
    arrow_pts = [
        (vault_cx - 10 * s, vault_cy - 10 * s),
        (vault_cx + 40 * s, vault_cy + 15 * s),
        (vault_cx + 25 * s, vault_cy + 35 * s),
        (arrow_tip_x, arrow_tip_y),
        (arrow_tip_x - 45 * s, arrow_tip_y - 10 * s),
        (arrow_tip_x - 30 * s, arrow_tip_y - 25 * s),
        (vault_cx + 10 * s, vault_cy + 10 * s)
    ]
    d.polygon(arrow_pts, fill=VERM)
    
    # Download speed callout badge in Vermilion
    d.polygon([
        (arrow_tip_x + 10 * s, arrow_tip_y - 30 * s),
        (arrow_tip_x + 150 * s, arrow_tip_y - 30 * s),
        (arrow_tip_x + 150 * s, arrow_tip_y + 10 * s),
        (arrow_tip_x + 10 * s, arrow_tip_y + 10 * s)
    ], fill=VERM)
    d.text((arrow_tip_x + 18 * s, arrow_tip_y - 24 * s), "DIRECT LINK: 100 MB/s", fill=CREAM, font=FONT_CODE_BOLD)
    d.text((arrow_tip_x + 18 * s, arrow_tip_y - 8 * s), "CLIENT BYPASSED: 100%", fill=CREAM, font=FONT_TINY)
    
    # Shackle snapped vector sparks in Vermilion
    d.line([(lock_cx + 20 * s, lock_cy - 25 * s), (lock_cx + 45 * s, lock_cy - 45 * s)], fill=VERM, width=4 * s)
    d.line([(lock_cx + 10 * s, lock_cy - 30 * s), (lock_cx + 25 * s, lock_cy - 55 * s)], fill=VERM, width=3 * s)
    
    im_final = im.resize((W_FINAL, H_FINAL), Image.LANCZOS)
    out_path = "demo-news/public/images/linkswift-javascript-cloud-storage.jpg"
    im_final.save(out_path, quality=95)
    print("LinkSwift illustration saved to:", out_path)


# ==============================================================================
# 6. ELAYADESIGN: AI DESIGN SYSTEM SKILLS & ACCESSIBILITY CALIBRATION
# ==============================================================================
def render_elayadesign():
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    s = SCALE
    
    vp_x, vp_y = int(W * 0.40), int(H * 0.38)
    horizon_y = int(H * 0.58)
    draw_perspective_room(d, vp_x, vp_y, horizon_y, wall_step=56)
    
    # Background Wall: Design System Grid Board & Typography Scales
    b_x1, b_y1 = int(W * 0.06), int(H * 0.08)
    b_x2, b_y2 = int(W * 0.94), int(H * 0.42)
    d.rectangle([b_x1, b_y1, b_x2, b_y2], fill=CREAM, outline=INK, width=2 * s)
    d.rectangle([b_x1, b_y1, b_x2, b_y1 + 24 * s], fill=INK)
    d.text((b_x1 + 15 * s, b_y1 + 5 * s), "ELAYADESIGN / DESIGN-SYSTEM // AGENT DESIGN SKILLS SPECIFICATION", fill=CREAM, font=FONT_SUBTITLE)
    
    # Typography hierarchy bars on wall board
    type_x = b_x1 + 30 * s
    d.text((type_x, b_y1 + 36 * s), "DISPLAY TITLE 48px / Line Height 56px", fill=INK, font=FONT_SUBTITLE)
    d.text((type_x, b_y1 + 60 * s), "SECTION HEADING 24px / Bold 700 / Letter Spacing -0.5px", fill=INK, font=FONT_BODY)
    d.text((type_x, b_y1 + 80 * s), "BODY REGULAR 16px / Regular 400 / Line Height 24px", fill=GRID_ACCENT, font=FONT_BODY)
    d.text((type_x, b_y1 + 98 * s), "CAPTION 12px / Medium 500 / Uppercase Monospace", fill=GRID_ACCENT, font=FONT_TINY)
    
    # 8px Spacing Scale Swatches on right of board
    sw_x = b_x2 - 280 * s
    sw_y = b_y1 + 38 * s
    d.text((sw_x, sw_y), "SPATIAL GRID: 8px BASE SYSTEM", fill=INK, font=FONT_TINY)
    steps = [8, 16, 24, 32, 48, 64]
    for idx, step in enumerate(steps):
        bx = sw_x + idx * 42 * s
        by = sw_y + 18 * s
        d.rectangle([bx, by, bx + step // 2 * s, by + 30 * s], fill=INK)
        d.text((bx, by + 34 * s), f"{step}px", fill=INK, font=FONT_TINY)
        
    # Foreground / Center: Massive Tilted Architectural Drafting Table in Perspective
    desk_left, desk_right = int(W * 0.12), int(W * 0.88)
    desk_top, desk_bottom = int(H * 0.46), int(H * 0.84)
    # Tilted drafting board top
    d.polygon([
        (desk_left + 60 * s, desk_top),
        (desk_right - 40 * s, desk_top),
        (desk_right, desk_bottom),
        (desk_left, desk_bottom)
    ], fill=INK)
    # Trestle heavy wooden legs
    d.rectangle([desk_left + 50 * s, desk_bottom, desk_left + 75 * s, H], fill=INK)
    d.rectangle([desk_right - 75 * s, desk_bottom, desk_right - 50 * s, H], fill=INK)
    # Cross-brace between legs
    d.line([(desk_left + 60 * s, int(H * 0.92)), (desk_right - 60 * s, int(H * 0.92))], fill=INK, width=6 * s)
    
    # Large UI Blueprint Sheet Pinned to Drafting Board
    sheet_x1, sheet_y1 = desk_left + 90 * s, desk_top + 16 * s
    sheet_x2, sheet_y2 = desk_right - 70 * s, desk_bottom - 16 * s
    d.polygon([
        (sheet_x1 + 30 * s, sheet_y1),
        (sheet_x2 - 20 * s, sheet_y1),
        (sheet_x2, sheet_y2),
        (sheet_x1, sheet_y2)
    ], fill=CREAM)
    
    # Design System Layout Components on the sheet
    # Button Primitives Row
    btn_y = sheet_y1 + 30 * s
    # Button 1: Solid Primary
    d.rectangle([sheet_x1 + 40 * s, btn_y, sheet_x1 + 130 * s, btn_y + 28 * s], fill=INK)
    d.text((sheet_x1 + 55 * s, btn_y + 6 * s), "Primary", fill=CREAM, font=FONT_TINY)
    # Button 2: Secondary Outline
    d.rectangle([sheet_x1 + 145 * s, btn_y, sheet_x1 + 235 * s, btn_y + 28 * s], outline=INK, width=2 * s)
    d.text((sheet_x1 + 155 * s, btn_y + 6 * s), "Secondary", fill=INK, font=FONT_TINY)
    
    # Complex UI Card Prototype on sheet
    card_x1 = sheet_x1 + 40 * s
    card_y1 = btn_y + 45 * s
    card_x2 = sheet_x1 + 280 * s
    card_y2 = sheet_y2 - 25 * s
    d.rectangle([card_x1, card_y1, card_x2, card_y2], fill=CREAM, outline=INK, width=2 * s)
    # Card Header
    d.rectangle([card_x1 + 10 * s, card_y1 + 10 * s, card_x2 - 10 * s, card_y1 + 35 * s], fill=INK)
    d.text((card_x1 + 18 * s, card_y1 + 14 * s), "Component Card [AI Generated]", fill=CREAM, font=FONT_TINY)
    # Card image placeholder
    d.rectangle([card_x1 + 10 * s, card_y1 + 42 * s, card_x1 + 75 * s, card_y1 + 95 * s], fill=GRID_ACCENT)
    # Card body lines
    d.rectangle([card_x1 + 85 * s, card_y1 + 48 * s, card_x2 - 15 * s, card_y1 + 56 * s], fill=INK)
    d.rectangle([card_x1 + 85 * s, card_y1 + 62 * s, card_x2 - 35 * s, card_y1 + 70 * s], fill=INK)
    d.rectangle([card_x1 + 85 * s, card_y1 + 76 * s, card_x2 - 60 * s, card_y1 + 84 * s], fill=GRID_ACCENT)
    
    # Bold Vermilion Red-Orange Accent 1: 8px Caliper Measurement Dimension Lines
    dim_x = card_x1 + 75 * s
    d.line([(dim_x, card_y1 + 42 * s), (dim_x + 10 * s, card_y1 + 42 * s)], fill=VERM, width=2 * s)
    d.line([(dim_x, card_y1 + 95 * s), (dim_x + 10 * s, card_y1 + 95 * s)], fill=VERM, width=2 * s)
    d.line([(dim_x + 5 * s, card_y1 + 42 * s), (dim_x + 5 * s, card_y1 + 95 * s)], fill=VERM, width=2 * s)
    d.text((dim_x + 12 * s, card_y1 + 62 * s), "8px PAD", fill=VERM, font=FONT_TINY)
    
    # Precision Metal Caliper / Divider Tool Resting on Desk
    cal_cx, cal_cy = sheet_x1 + 330 * s, sheet_y1 + 60 * s
    d.line([(cal_cx, cal_cy), (cal_cx - 30 * s, cal_cy + 80 * s)], fill=INK, width=4 * s)
    d.line([(cal_cx, cal_cy), (cal_cx + 30 * s, cal_cy + 80 * s)], fill=INK, width=4 * s)
    d.ellipse([cal_cx - 8 * s, cal_cy - 8 * s, cal_cx + 8 * s, cal_cy + 8 * s], fill=INK)
    
    # Bold Vermilion Red-Orange Accent 2: WCAG AA Contrast Compliance Ratio Gauge
    gauge_cx = sheet_x2 - 110 * s
    gauge_cy = sheet_y1 + 90 * s
    gauge_r = 55 * s
    # Outer circle in Vermilion
    d.ellipse([gauge_cx - gauge_r, gauge_cy - gauge_r, gauge_cx + gauge_r, gauge_cy + gauge_r], outline=VERM, width=4 * s)
    # Dial needle in Vermilion
    d.line([(gauge_cx, gauge_cy), (gauge_cx + 32 * s, gauge_cy - 32 * s)], fill=VERM, width=4 * s)
    d.ellipse([gauge_cx - 6 * s, gauge_cy - 6 * s, gauge_cx + 6 * s, gauge_cy + 6 * s], fill=VERM)
    # Dial markings
    for angle in range(140, 400, 30):
        rad = math.radians(angle)
        gx1 = gauge_cx + (gauge_r - 8 * s) * math.cos(rad)
        gy1 = gauge_cy + (gauge_r - 8 * s) * math.sin(rad)
        gx2 = gauge_cx + gauge_r * math.cos(rad)
        gy2 = gauge_cy + gauge_r * math.sin(rad)
        d.line([(gx1, gy1), (gx2, gy2)], fill=VERM, width=2 * s)
    # Label inside gauge
    d.text((gauge_cx - 34 * s, gauge_cy + 12 * s), "4.5:1 PASSED", fill=VERM, font=FONT_CODE_BOLD)
    d.text((gauge_cx - 30 * s, gauge_cy + 26 * s), "WCAG AA OK", fill=INK, font=FONT_TINY)
    
    # Lead Designer Silhouette on Right
    draw_person_standing(d, int(W * 0.88), int(H * 0.72), height=380, facing_left=True, pointing=True)
    
    im_final = im.resize((W_FINAL, H_FINAL), Image.LANCZOS)
    out_path = "demo-news/public/images/elayadesign-ai-design-skills.jpg"
    im_final.save(out_path, quality=95)
    print("ElayaDesign illustration saved to:", out_path)


if __name__ == "__main__":
    render_ruview()
    render_xiaolai()
    render_expo_skills()
    render_macro()
    render_linkswift()
    render_elayadesign()
    print("All 6 high-detail editorial illustrations rendered successfully.")
