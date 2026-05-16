from PIL import Image, ImageDraw, ImageFont

frame1 = """\
                  █▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
█▀▀▀▀█▀▀▀▀█▀▀▀▀█  █     ▄  ▄     █  █▀▀▀▀█▀▀▀▀█▀▀▀▀█
█░░░░█░░░░█░░░░█  █    ██▄▄██    █  █░░░░█░░░░█░░░░█
█▄▄▄▄█▄▄▄▄█▄▄▄▄█▄▄█   ██ ██ ██   █▄▄█▄▄▄▄█▄▄▄▄█▄▄▄▄█
█▀▀▀▀█▀▀▀▀█▀▀▀▀█▀▀█   ████████   █▀▀█▀▀▀▀█▀▀▀▀█▀▀▀▀█
█░░░░█░░░░█░░░░█  █   ▄ ████     █  █░░░░█░░░░█░░░░█
█▄▄▄▄█▄▄▄▄█▄▄▄▄█  █   ▐▄████     █  █▄▄▄▄█▄▄▄▄█▄▄▄▄█
                  █▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
                       ▄████▄
                      ▀▀▀▀▀▀▀▀
                       ▀▄▄▄▄▀

                     ▀▀▄▄▄▄▄▄▀▀

                   ▀▀▀▄▄▄▄▄▄▄▄▀▀▀"""

frame2 = """\
                  █▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
█▀▀▀▀█▀▀▀▀█▀▀▀▀█  █     ▄  ▄     █  █▀▀▀▀█▀▀▀▀█▀▀▀▀█
█░░░░█░░░░█░░░░█  █    ██▄▄██    █  █░░░░█░░░░█░░░░█
█▄▄▄▄█▄▄▄▄█▄▄▄▄█▄▄█   ██ ██ ██   █▄▄█▄▄▄▄█▄▄▄▄█▄▄▄▄█
█▀▀▀▀█▀▀▀▀█▀▀▀▀█▀▀█   ████████   █▀▀█▀▀▀▀█▀▀▀▀█▀▀▀▀█
█░░░░█░░░░█░░░░█  █   ▄ ████     █  █░░░░█░░░░█░░░░█
█▄▄▄▄█▄▄▄▄█▄▄▄▄█  █   ▐▄████     █  █▄▄▄▄█▄▄▄▄█▄▄▄▄█
                  █▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
                       ▄████▄
                      ▀▀▀▀▀▀▀▀

                      ▀▄▄▄▄▄▄▀

                    ▀▀▄▄▄▄▄▄▄▄▀▀

                  ▀▀▀▄▄▄▄▄▄▄▄▄▄▀▀▀"""

FONT_PATH = "/System/Library/Fonts/SFNSMono.ttf"
FONT_SIZE = 9
BG = (13, 17, 23)
FG = (201, 209, 217)
PAD = 8
GAP = 1000        # padding between panels in the ribbon
DURATION_MS = round(1000 / 24)   # 42ms = 24 fps
SCROLL_SPEED = 141  # px/s
FRAMES_PER_SWITCH = 24  # alternate f1/f2 every 1 second
GROUND_COLOR = (58, 110, 48)  # earthy green

font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
_bbox = font.getbbox("W")
CH = _bbox[3] - _bbox[1]
CW = _bbox[2] - _bbox[0]


def render_panel(text):
    lines = [l.rstrip() for l in text.split("\n")]
    width = max(len(l) for l in lines) * CW + PAD * 2
    height = len(lines) * CH + PAD * 2
    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)
    for i, line in enumerate(lines):
        draw.text((PAD, PAD + i * CH), line, font=font, fill=FG)
    return img


def make_ground(width):
    row = "▄" * (width // CW + 2)
    ground = Image.new("RGB", (width, CH), BG)
    ImageDraw.Draw(ground).text((0, 0), row, font=font, fill=GROUND_COLOR)
    return ground


p1 = render_panel(frame1)
p2 = render_panel(frame2)

panel_w = max(p1.width, p2.width)
panel_h = max(p1.height, p2.height)


def pad_panel(img):
    out = Image.new("RGB", (panel_w, panel_h), BG)
    out.paste(img, (0, 0))
    return out


p1 = pad_panel(p1)
p2 = pad_panel(p2)

# Two ribbons — one per ASCII frame — doubled for seamless loop
panel_step = panel_w + GAP
cycle_w = panel_step * 2
ribbon_a = Image.new("RGB", (cycle_w * 2, panel_h), BG)
ribbon_b = Image.new("RGB", (cycle_w * 2, panel_h), BG)
for i in range(4):
    ribbon_a.paste(p1, (i * panel_step, 0))
    ribbon_b.paste(p2, (i * panel_step, 0))

# Compute frames needed to maintain SCROLL_SPEED at 24fps
n_frames = round(cycle_w / (SCROLL_SPEED * DURATION_MS / 1000))

# Viewport scrolls right-to-left; content alternates between f1/f2 every second
viewport_w = 1000
ground = make_ground(viewport_w)
frames = []
for i in range(n_frames):
    ribbon = ribbon_a if (i // FRAMES_PER_SWITCH) % 2 == 0 else ribbon_b
    x = cycle_w - int(i * cycle_w / n_frames)
    crop = ribbon.crop((x, 0, x + viewport_w, panel_h))
    crop.paste(ground, (0, panel_h - CH))  # static ground at bottom
    frames.append(crop)

frames[0].save(
    "ascii.gif",
    save_all=True,
    append_images=frames[1:],
    loop=0,
    duration=DURATION_MS,
    optimize=False,
)
print(f"Saved ascii.gif  viewport={viewport_w}x{panel_h}  cycle={cycle_w}px  frames={n_frames}  fps=24")
