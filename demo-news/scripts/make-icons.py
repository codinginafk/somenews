"""Draw the PTW mark (bars + check) as real PNG/ICO files.
RW lesson: /favicon.ico and /apple-touch-icon.png must be REAL files -
Google's fetcher probes bare paths and a SPA/static catchall soft-404
shows a generic globe in search results.
"""
from PIL import Image, ImageDraw

VERM = (194, 65, 12)
CREAM = (255, 247, 237)
INK = (22, 19, 14)


def tile(s, radius=True):
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    u = s / 64.0
    if radius:
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(12 * u), fill=VERM + (255,))
    else:
        d.rectangle([0, 0, s - 1, s - 1], fill=VERM + (255,))
    d.rectangle([14 * u, 36 * u, 22 * u, 50 * u], fill=CREAM + (255,))
    d.rectangle([26 * u, 28 * u, 34 * u, 50 * u], fill=CREAM + (255,))
    d.rectangle([38 * u, 20 * u, 46 * u, 50 * u], fill=INK + (255,))
    d.line([(34 * u, 14 * u), (42 * u, 22 * u), (54 * u, 8 * u)],
           fill=CREAM + (255,), width=max(2, int(5 * u)), joint="curve")
    return img


def solid(base_size, art_scale=0.72):
    bg = Image.new("RGBA", (base_size, base_size), VERM + (255,))
    art = tile(512).resize((int(base_size * art_scale),) * 2, Image.LANCZOS)
    off = (base_size - art.size[0]) // 2
    bg.alpha_composite(art, (off, off))
    return bg.convert("RGB")


if __name__ == "__main__":
    tile(512).resize((16, 16), Image.LANCZOS).save("public/favicon-16.png")
    tile(512).resize((32, 32), Image.LANCZOS).save("public/favicon-32.png")
    tile(512).save("public/icon-512-src.png")
    solid(512).save("public/icon-512.png")
    solid(192).save("public/icon-192.png")
    solid(180).save("public/apple-touch-icon.png")
    ico = [tile(512).resize((s, s), Image.LANCZOS) for s in (16, 32, 48)]
    ico[0].save("public/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)],
                append_images=ico[1:])
    print("icons written")
