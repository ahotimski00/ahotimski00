import math
import random
from PIL import Image, ImageChops, ImageDraw, ImageFont

frame1 = """\
               █▀▀▀▀▀▀▀▀▀▀▀▀█
█▀▀▀█▀▀▀█▀▀▀█  █    ▄  ▄    █  █▀▀▀█▀▀▀█▀▀▀█
█░░░█░░░█░░░█  █   ██▄▄██   █  █░░░█░░░█░░░█
█▄▄▄█▄▄▄█▄▄▄█▄▄█  ██ ██ ██  █▄▄█▄▄▄█▄▄▄█▄▄▄█
█▀▀▀█▀▀▀█▀▀▀█▀▀█  ████████  █▀▀█▀▀▀█▀▀▀█▀▀▀█
█░░░█░░░█░░░█  █  ▄ ████    █  █░░░█░░░█░░░█
█▄▄▄█▄▄▄█▄▄▄█  █  ▐▄████    █  █▄▄▄█▄▄▄█▄▄▄█
               █▄▄▄▄▄▄▄▄▄▄▄▄█
                   ▄████▄
                  ▀▀▀▀▀▀▀▀
                    ▀▄▄▀

                  ▀▀▄▄▄▄▀▀

                ▀▀▀▄▄▄▄▄▄▀▀▀

                   """

frame2 = """\
               █▀▀▀▀▀▀▀▀▀▀▀▀█
█▀▀▀█▀▀▀█▀▀▀█  █    ▄  ▄    █  █▀▀▀█▀▀▀█▀▀▀█
█░░░█░░░█░░░█  █   ██▄▄██   █  █░░░█░░░█░░░█
█▄▄▄█▄▄▄█▄▄▄█▄▄█  ██ ██ ██  █▄▄█▄▄▄█▄▄▄█▄▄▄█
█▀▀▀█▀▀▀█▀▀▀█▀▀█  ████████  █▀▀█▀▀▀█▀▀▀█▀▀▀█
█░░░█░░░█░░░█  █  ▄ ████    █  █░░░█░░░█░░░█
█▄▄▄█▄▄▄█▄▄▄█  █  ▐▄████    █  █▄▄▄█▄▄▄█▄▄▄█
               █▄▄▄▄▄▄▄▄▄▄▄▄█
                   ▄████▄
                  ▀▀▀▀▀▀▀▀

                   ▀▄▄▄▄▀

                 ▀▀▄▄▄▄▄▄▀▀

               ▀▀▀▄▄▄▄▄▄▄▄▀▀▀

                  """

FONT_PATH = "/System/Library/Fonts/SFNSMono.ttf"
FONT_SIZE = 5    # small enough that the full QR art fits above the ground strip
BG = (13, 17, 23)
FG = (201, 209, 217)
PAD = 3 
PANEL_H = 106   # fixed ribbon height — keeps total GIF height stable
GAP = 1000
DURATION_MS = round(1000 / 24)
SCROLL_SPEED = 50
FRAMES_PER_SWITCH = 24
BOAT_PERIOD = 48          # frames per full left-right oscillation

GROUND_H    = 72
SOIL_H      = 4
GRASS_H     = 5
SOIL_COLOR  = (72, 44, 18)
GRASS_COLOR = (72, 140, 52)
MTN_COLOR   = (95, 108, 122)
SNOW_COLOR  = (225, 230, 238)
TREE_BG     = (18, 48, 18)   # back layer — darker
TREE_BG2    = (12, 36, 12)
TREE_COLOR  = (34, 80, 34)   # front layer
TREE_DARK   = (22, 56, 22)
LAKE_COLOR  = (35, 80, 130)
LAKE_HI     = (65, 120, 175)
BOAT_COLOR  = (190, 30, 30)
SAIL_COLOR  = (220, 45, 45)
SAIL_COLOR2 = (240, 200, 180)
DUCK_COLOR  = (230, 220, 185)
DEER_COLOR  = (110, 65, 22)

font  = ImageFont.truetype(FONT_PATH, FONT_SIZE)
_bbox = font.getbbox("W")
CH = _bbox[3] - _bbox[1]
CW = _bbox[2] - _bbox[0]


def render_panel(text):
    lines  = [l.rstrip() for l in text.split("\n")]
    width  = max(len(l) for l in lines) * CW + PAD * 2
    height = len(lines) * CH + PAD * 2
    img    = Image.new("RGB", (width, height), BG)
    draw   = ImageDraw.Draw(img)
    for i, line in enumerate(lines):
        draw.text((PAD, PAD + i * CH), line, font=font, fill=FG)
    return img


def draw_duck(draw, x, y, facing="right"):
    dc = DUCK_COLOR
    if facing == "right":
        draw.ellipse([(x, y - 3), (x + 10, y + 1)], fill=dc)
        draw.ellipse([(x + 7, y - 6), (x + 11, y - 2)], fill=dc)
        draw.line([(x + 11, y - 4), (x + 14, y - 4)], fill=(220, 110, 10), width=1)
    else:
        draw.ellipse([(x, y - 3), (x + 10, y + 1)], fill=dc)
        draw.ellipse([(x - 1, y - 6), (x + 3, y - 2)], fill=dc)
        draw.line([(x - 1, y - 4), (x - 4, y - 4)], fill=(220, 110, 10), width=1)


def draw_deer(draw, cx, ground_y):
    dc = DEER_COLOR
    bt = ground_y - 14   # body top
    bb = ground_y - 8    # body bottom
    draw.ellipse([(cx - 8, bt), (cx + 8, bb)], fill=dc)
    for lx in [cx - 5, cx - 2, cx + 2, cx + 5]:
        draw.line([(lx, bb), (lx, ground_y - 1)], fill=dc, width=1)
    draw.line([(cx + 6, bt + 1), (cx + 10, bt - 4)], fill=dc, width=2)
    draw.ellipse([(cx + 8, bt - 7), (cx + 14, bt - 3)], fill=dc)
    ax, ay = cx + 10, bt - 7
    draw.line([(ax, ay), (ax - 2, ay - 5)], fill=dc, width=1)
    draw.line([(ax - 2, ay - 5), (ax - 4, ay - 7)], fill=dc, width=1)
    draw.line([(ax - 2, ay - 5), (ax, ay - 8)], fill=dc, width=1)
    draw.line([(ax + 1, ay), (ax + 3, ay - 4)], fill=dc, width=1)
    draw.line([(ax + 3, ay - 4), (ax + 2, ay - 7)], fill=dc, width=1)
    draw.line([(ax + 3, ay - 4), (ax + 5, ay - 6)], fill=dc, width=1)


def make_ground(width, frame_idx=0):
    img      = Image.new("RGB", (width, GROUND_H), BG)
    draw     = ImageDraw.Draw(img)
    ground_y = GROUND_H - SOIL_H - GRASS_H

    draw.rectangle([(0, GROUND_H - SOIL_H), (width, GROUND_H)], fill=SOIL_COLOR)
    draw.rectangle([(0, ground_y), (width, GROUND_H - SOIL_H)], fill=GRASS_COLOR)

    rng = random.Random(7)

    # Connected mountain ridge — taller than the trees
    STEP = 16
    h = rng.randint(20, 36)
    samples = []
    x = -STEP
    while x <= width + STEP:
        samples.append((x, ground_y - h))
        h = max(14, min(42, h + rng.randint(-7, 7)))
        x += STEP
    pts = [(samples[0][0], ground_y)] + samples + [(samples[-1][0], ground_y)]
    draw.polygon(pts, fill=MTN_COLOR)

    # Snow caps interpolated along actual ridge slope
    for i in range(1, len(samples) - 1):
        px, py = samples[i]
        lx, ly = samples[i - 1]
        rx, ry = samples[i + 1]
        if py < ly and py < ry:
            peak_h = ground_y - py
            snow_y = py + max(3, peak_h // 3)
            t_l    = (snow_y - py) / (ly - py) if ly != py else 0
            t_r    = (snow_y - py) / (ry - py) if ry != py else 0
            sx_l   = int(px + t_l * (lx - px))
            sx_r   = int(px + t_r * (rx - px))
            if sx_r > sx_l:
                draw.polygon([(sx_l, snow_y), (px, py), (sx_r, snow_y)], fill=SNOW_COLOR)

    # Lake
    lk_x1, lk_x2 = width // 3 + 60, width // 3 + 260
    draw.rectangle([(lk_x1, ground_y), (lk_x2, GROUND_H)], fill=LAKE_COLOR)
    for j in range(3):
        yo = ground_y + 2 + j * 4
        draw.line([(lk_x1 + 12 + j * 8, yo), (lk_x2 - 12 - j * 8, yo)], fill=LAKE_HI, width=1)

    # Animated sailboat — rocks left/right
    boat_off = int(7 * math.sin(2 * math.pi * frame_idx / BOAT_PERIOD))
    bx       = (lk_x1 + lk_x2) // 2 + boat_off
    hull_y   = GROUND_H - SOIL_H - 2
    hull_top = hull_y - 5
    mast_top = hull_top - 18
    draw.polygon([(bx-14, hull_top), (bx+14, hull_top), (bx+10, hull_y), (bx-10, hull_y)], fill=BOAT_COLOR)
    draw.line([(bx, hull_top), (bx, mast_top)], fill=(210, 210, 210), width=1)
    draw.polygon([(bx, mast_top), (bx, hull_top), (bx+18, hull_top-6)], fill=SAIL_COLOR)
    draw.polygon([(bx, mast_top-2), (bx, hull_top), (bx-10, hull_top-4)], fill=SAIL_COLOR2)

    # Ducks near lake shore
    draw_duck(draw, lk_x1 + 6,  ground_y + 6, "right")
    draw_duck(draw, lk_x1 + 22, ground_y + 4, "right")
    draw_duck(draw, lk_x2 - 24, ground_y + 5, "left")

    # Background tree layer — smaller than mountains, very dark, dense
    rng_bg = random.Random(21)
    x = -8
    while x < width + 8:
        tw = rng_bg.randint(6, 11)
        th = rng_bg.randint(6, 11)
        cx = x + tw // 2
        if not (lk_x1 - 4 < cx < lk_x2 + 4):
            for layer in range(3):
                lh      = th * (3 - layer) // 4
                lw      = tw * (layer + 2) // 3
                ly_base = ground_y - th // 5 + layer * (th // 7)
                ly_tip  = ly_base - lh
                color   = TREE_BG if layer % 2 == 0 else TREE_BG2
                draw.polygon([(cx - lw//2, ly_base), (cx, ly_tip), (cx + lw//2, ly_base)], fill=color)
        x += rng_bg.randint(2, 5)

    # Foreground tree layer — slightly larger, brighter, overlapping
    rng2 = random.Random(13)
    x = -5
    while x < width + 10:
        tw = rng2.randint(8, 14)
        th = rng2.randint(10, 18)
        cx = x + tw // 2
        if not (lk_x1 - 6 < cx < lk_x2 + 6):
            for layer in range(3):
                lh      = th * (3 - layer) // 4
                lw      = tw * (layer + 2) // 3
                ly_base = ground_y - th // 4 + layer * (th // 6)
                ly_tip  = ly_base - lh
                color   = TREE_COLOR if layer % 2 == 0 else TREE_DARK
                draw.polygon([(cx - lw//2, ly_base), (cx, ly_tip), (cx + lw//2, ly_base)], fill=color)
        x += rng2.randint(1, 5)

    # Deer drawn last so it appears in front of all trees
    deer_cx = lk_x1 - 70
    if deer_cx > 20:
        draw_deer(draw, deer_cx, ground_y)

    return img


p1 = render_panel(frame1)
p2 = render_panel(frame2)

panel_w = max(p1.width, p2.width)


def pad_panel(img):
    # Always pad to PANEL_H so the ribbon height never changes
    out = Image.new("RGB", (panel_w, PANEL_H), BG)
    out.paste(img, (0, 0))
    return out


p1 = pad_panel(p1)
p2 = pad_panel(p2)

# Two ribbons — one per ASCII frame — doubled for seamless loop
panel_step = panel_w + GAP
cycle_w    = panel_step * 2
ribbon_a   = Image.new("RGB", (cycle_w * 2, PANEL_H), BG)
ribbon_b   = Image.new("RGB", (cycle_w * 2, PANEL_H), BG)
for i in range(4):
    ribbon_a.paste(p1, (i * panel_step, 0))
    ribbon_b.paste(p2, (i * panel_step, 0))

n_frames   = round(cycle_w / (SCROLL_SPEED * DURATION_MS / 1000))
viewport_w = 1000

# Static star field — RGBA overlay, composited over the sky area each frame
sky_h      = PANEL_H - GROUND_H
star_overlay = Image.new("RGBA", (viewport_w, PANEL_H), (0, 0, 0, 0))
star_draw    = ImageDraw.Draw(star_overlay)
star_font    = ImageFont.truetype(FONT_PATH, 6)
star_rng     = random.Random(42)
for _ in range(90):
    sx = star_rng.randint(0, viewport_w - 6)
    sy = star_rng.randint(0, sky_h - 6)
    br = star_rng.randint(130, 230)
    al = star_rng.randint(120, 200)
    star_draw.text((sx, sy), "*", font=star_font, fill=(br, br, br + 25, al))

# Precompute one oscillation cycle of ground frames
print(f"Rendering {BOAT_PERIOD} ground frames…")
ground_cache = [make_ground(viewport_w, i) for i in range(BOAT_PERIOD)]

_bg_solid = Image.new("RGB", (viewport_w, PANEL_H), BG)  # for mask generation

print(f"Compositing {n_frames} GIF frames…")
frames = []
for i in range(n_frames):
    # 1. Build landscape base (full height)
    base = Image.new("RGB", (viewport_w, PANEL_H), BG)
    base.paste(ground_cache[i % BOAT_PERIOD], (0, PANEL_H - GROUND_H))
    # 2. Composite static stars onto sky
    base = Image.alpha_composite(base.convert("RGBA"), star_overlay).convert("RGB")
    # 3. Crop QR panels from scrolling ribbon
    ribbon = ribbon_a if (i // FRAMES_PER_SWITCH) % 2 == 0 else ribbon_b
    x      = cycle_w - int(i * cycle_w / n_frames)
    crop   = ribbon.crop((x, 0, x + viewport_w, PANEL_H))
    # 4. Mask out BG pixels so only QR characters show; paste on top of landscape
    mask   = ImageChops.difference(crop, _bg_solid).convert("L")
    base.paste(crop, (0, 0), mask=mask)
    frames.append(base)

frames[0].save(
    "ascii.gif",
    save_all=True,
    append_images=frames[1:],
    loop=0,
    duration=DURATION_MS,
    optimize=False,
)
print(f"Saved ascii.gif  viewport={viewport_w}x{PANEL_H}  cycle={cycle_w}px  frames={n_frames}  fps=24")
