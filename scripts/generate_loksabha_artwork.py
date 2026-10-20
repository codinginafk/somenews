"""Generate editorial artwork for Lok Sabha 850 Seats Delimitation News.
Adheres strictly to Rent Free News editorial art specifications:
- Two-tone style with warm cream paper background (#F7F2E9)
- Solid deep charcoal black ink silhouettes (#16130E)
- Bold splash of vermilion red-orange accent (#C2410C)
- Subtle wireframe grid
- Strict 16:10 aspect ratio (1280x800)
- Single unified composition, flat vector art, zero shading/transparency
"""
from PIL import Image, ImageDraw, ImageFont
import math
import os

W_FINAL, H_FINAL = 1280, 800
SCALE = 2
W, H = W_FINAL * SCALE, H_FINAL * SCALE

CREAM = (247, 242, 233)
GRID = (229, 221, 208)
GRID_DARK = (218, 208, 192)
INK = (22, 19, 14)
VERM = (194, 65, 12)

def generate():
    im = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(im)

    # 1. Subtle wireframe background grid
    grid_step = 64 * SCALE
    for x in range(0, W, grid_step):
        draw.line([(x, 0), (x, H)], fill=GRID, width=SCALE)
    for y in range(0, H, grid_step):
        draw.line([(0, y), (W, y)], fill=GRID, width=SCALE)

    # Perspective chamber lines converging towards center dais
    vp_x = W // 2
    vp_y = int(H * 0.38)

    # Chamber wall lines
    draw.line([(0, int(H * 0.48)), (W, int(H * 0.48))], fill=GRID_DARK, width=2 * SCALE)
    for px in range(0, W + 1, 160 * SCALE):
        draw.line([(px, H), (vp_x, vp_y)], fill=GRID, width=SCALE)

    # 2. Chamber architectural structure (parliamentary acoustic ribs and central arch)
    # Background parliamentary hall acoustic wall panels
    draw.polygon([
        (vp_x - 360 * SCALE, int(H * 0.12)),
        (vp_x + 360 * SCALE, int(H * 0.12)),
        (vp_x + 440 * SCALE, int(H * 0.48)),
        (vp_x - 440 * SCALE, int(H * 0.48))
    ], fill=GRID)

    # Central Speaker's dais backdrop
    draw.polygon([
        (vp_x - 180 * SCALE, int(H * 0.15)),
        (vp_x + 180 * SCALE, int(H * 0.15)),
        (vp_x + 220 * SCALE, int(H * 0.52)),
        (vp_x - 220 * SCALE, int(H * 0.52))
    ], fill=INK)

    # 3. VERMILION ACCENT: The Voting Division Display / 850 Seats Board
    board_w = 260 * SCALE
    board_h = 75 * SCALE
    board_x = vp_x - board_w // 2
    board_y = int(H * 0.20)
    draw.rectangle([board_x, board_y, board_x + board_w, board_y + board_h], fill=VERM)

    # Cutout text "850 SEATS // DIVISION" on the vermilion board in cream
    # Using clean vector geometry for numerals and text if system font unavailable
    # Draw simple bold glyphs for "850"
    num_y = board_y + 12 * SCALE
    num_h = 50 * SCALE
    num_w = 28 * SCALE
    stroke_w = 6 * SCALE

    # 8
    x8 = vp_x - 55 * SCALE
    draw.rectangle([x8, num_y, x8 + num_w, num_y + num_h], outline=CREAM, width=stroke_w)
    draw.line([(x8, num_y + num_h // 2), (x8 + num_w, num_y + num_h // 2)], fill=CREAM, width=stroke_w)

    # 5
    x5 = vp_x - 14 * SCALE
    draw.line([(x5, num_y), (x5 + num_w, num_y)], fill=CREAM, width=stroke_w)
    draw.line([(x5, num_y), (x5, num_y + num_h // 2)], fill=CREAM, width=stroke_w)
    draw.line([(x5, num_y + num_h // 2), (x5 + num_w, num_y + num_h // 2)], fill=CREAM, width=stroke_w)
    draw.line([(x5 + num_w, num_y + num_h // 2), (x5 + num_w, num_y + num_h)], fill=CREAM, width=stroke_w)
    draw.line([(x5, num_y + num_h), (x5 + num_w, num_y + num_h)], fill=CREAM, width=stroke_w)

    # 0
    x0 = vp_x + 28 * SCALE
    draw.rectangle([x0, num_y, x0 + num_w, num_y + num_h], outline=CREAM, width=stroke_w)

    # 4. Central Speaker's Podium & Table of the House
    podium_top = int(H * 0.38)
    podium_w = 140 * SCALE
    podium_h = 80 * SCALE
    draw.polygon([
        (vp_x - podium_w // 2, podium_top),
        (vp_x + podium_w // 2, podium_top),
        (vp_x + (podium_w // 2 + 30 * SCALE), podium_top + podium_h),
        (vp_x - (podium_w // 2 + 30 * SCALE), podium_top + podium_h)
    ], fill=INK)

    # Speaker silhouette seated at dais
    sp_head_r = 16 * SCALE
    sp_cx = vp_x
    sp_cy = podium_top - 24 * SCALE
    draw.ellipse([sp_cx - sp_head_r, sp_cy - sp_head_r, sp_cx + sp_head_r, sp_cy + sp_head_r], fill=INK)
    draw.polygon([
        (sp_cx - 24 * SCALE, podium_top),
        (sp_cx + 24 * SCALE, podium_top),
        (sp_cx + 18 * SCALE, podium_top - 12 * SCALE),
        (sp_cx - 18 * SCALE, podium_top - 12 * SCALE)
    ], fill=INK)

    # Vermilion accent strip on Speaker's desk rim
    draw.line([(vp_x - podium_w // 2, podium_top + 2 * SCALE), (vp_x + podium_w // 2, podium_top + 2 * SCALE)], fill=VERM, width=3 * SCALE)

    # 5. Tiered Semi-Circular Parliamentary Benches (Horseshoe Rows)
    # Tier 1 (Middle distance)
    t1_y = int(H * 0.54)
    # Left bank
    draw.polygon([
        (vp_x - 80 * SCALE, t1_y),
        (vp_x - 420 * SCALE, t1_y + 40 * SCALE),
        (vp_x - 440 * SCALE, t1_y + 85 * SCALE),
        (vp_x - 70 * SCALE, t1_y + 35 * SCALE)
    ], fill=INK)
    # Right bank
    draw.polygon([
        (vp_x + 80 * SCALE, t1_y),
        (vp_x + 420 * SCALE, t1_y + 40 * SCALE),
        (vp_x + 440 * SCALE, t1_y + 85 * SCALE),
        (vp_x + 70 * SCALE, t1_y + 35 * SCALE)
    ], fill=INK)

    # Seated MP silhouettes along Tier 1
    for i, offset in enumerate([-380, -320, -260, -200, -140, 140, 200, 260, 320, 380]):
        cx = vp_x + offset * SCALE
        cy = t1_y + int(abs(offset) * 0.08) * SCALE - 14 * SCALE
        r = 13 * SCALE
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=INK)
        draw.rectangle([cx - 16 * SCALE, cy + 6 * SCALE, cx + 16 * SCALE, cy + 28 * SCALE], fill=INK)

    # Tier 2 (Foreground / Lower tier)
    t2_y = int(H * 0.68)
    # Left bank
    draw.polygon([
        (vp_x - 120 * SCALE, t2_y),
        (vp_x - 580 * SCALE, t2_y + 70 * SCALE),
        (vp_x - 610 * SCALE, t2_y + 140 * SCALE),
        (vp_x - 100 * SCALE, t2_y + 55 * SCALE)
    ], fill=INK)
    # Right bank
    draw.polygon([
        (vp_x + 120 * SCALE, t2_y),
        (vp_x + 580 * SCALE, t2_y + 70 * SCALE),
        (vp_x + 610 * SCALE, t2_y + 140 * SCALE),
        (vp_x + 100 * SCALE, t2_y + 55 * SCALE)
    ], fill=INK)

    # Seated / standing MP silhouettes along Tier 2
    for i, offset in enumerate([-540, -460, -380, -300, -220, 220, 300, 380, 460, 540]):
        cx = vp_x + offset * SCALE
        cy = t2_y + int(abs(offset) * 0.10) * SCALE - 22 * SCALE
        r = 18 * SCALE
        # One MP raising an opposition document / order paper on left
        if offset == -380:
            draw.ellipse([cx - r, cy - r - 15 * SCALE, cx + r, cy + r - 15 * SCALE], fill=INK)
            draw.rectangle([cx - 22 * SCALE, cy - 2 * SCALE, cx + 22 * SCALE, cy + 35 * SCALE], fill=INK)
            # Arm raised holding rectangular document paper
            draw.polygon([
                (cx - 10 * SCALE, cy - 5 * SCALE),
                (cx - 30 * SCALE, cy - 45 * SCALE),
                (cx - 20 * SCALE, cy - 50 * SCALE),
                (cx, cy - 10 * SCALE)
            ], fill=INK)
            draw.polygon([
                (cx - 45 * SCALE, cy - 65 * SCALE),
                (cx - 15 * SCALE, cy - 55 * SCALE),
                (cx - 25 * SCALE, cy - 40 * SCALE),
                (cx - 55 * SCALE, cy - 50 * SCALE)
            ], fill=VERM) # Vermilion accent on the held bill document
        elif offset == 300:
            # MP standing to address the house
            draw.ellipse([cx - r, cy - r - 20 * SCALE, cx + r, cy + r - 20 * SCALE], fill=INK)
            draw.rectangle([cx - 24 * SCALE, cy - 5 * SCALE, cx + 24 * SCALE, cy + 45 * SCALE], fill=INK)
        else:
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=INK)
            draw.rectangle([cx - 22 * SCALE, cy + 10 * SCALE, cx + 22 * SCALE, cy + 40 * SCALE], fill=INK)

    # Tier 3 (Immediate foreground silhouette framing)
    draw.polygon([
        (0, H),
        (0, int(H * 0.86)),
        (int(W * 0.35), H),
    ], fill=INK)
    draw.polygon([
        (W, H),
        (W, int(H * 0.86)),
        (int(W * 0.65), H),
    ], fill=INK)

    # Downsample with Lanczos to final resolution (1280x800)
    final_im = im.resize((W_FINAL, H_FINAL), Image.Resampling.LANCZOS)
    
    out_dir = r"C:\Users\DELL\OneDrive\Desktop\somenews\demo-news\public\images"
    out_path = os.path.join(out_dir, "lok-sabha-850-seats-delimitation.jpg")
    final_im.save(out_path, "JPEG", quality=95)
    print(f"Generated artwork saved to: {out_path}")

if __name__ == "__main__":
    generate()
