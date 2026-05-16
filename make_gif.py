from PIL import Image, ImageDraw, ImageFont

frame1 = """\
                     █▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
█▀▀▀▀▀█▀▀▀▀▀█▀▀▀▀▀█  █     ▄  ▄     █  █▀▀▀▀▀█▀▀▀▀▀█▀▀▀▀▀█
█░░░░░█░░░░░█░░░░░█  █    ██▄▄██    █  █░░░░░█░░░░░█░░░░░█
█▄▄▄▄▄█▄▄▄▄▄█▄▄▄▄▄█▄▄█   ██ ██ ██   █▄▄█▄▄▄▄▄█▄▄▄▄▄█▄▄▄▄▄█
█▀▀▀▀▀█▀▀▀▀▀█▀▀▀▀▀█▀▀█   ████████   █▀▀█▀▀▀▀▀█▀▀▀▀▀█▀▀▀▀▀█
█░░░░░█░░░░░█░░░░░█  █   ▄ ████     █  █░░░░░█░░░░░█░░░░░█
█▄▄▄▄▄█▄▄▄▄▄█▄▄▄▄▄█  █   ▐▄████     █  █▄▄▄▄▄█▄▄▄▄▄█▄▄▄▄▄█
                     █▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
                          ▄████▄
                         ▀▀▀▀▀▀▀▀
                          ▀▄▄▄▄▀

                        ▀▀▄▄▄▄▄▄▀▀

                      ▀▀▀▄▄▄▄▄▄▄▄▀▀▀                      """

frame2 = """\
                     █▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
█▀▀▀▀▀█▀▀▀▀▀█▀▀▀▀▀█  █     ▄  ▄     █  █▀▀▀▀▀█▀▀▀▀▀█▀▀▀▀▀█
█░░░░░█░░░░░█░░░░░█  █    ██▄▄██    █  █░░░░░█░░░░░█░░░░░█
█▄▄▄▄▄█▄▄▄▄▄█▄▄▄▄▄█▄▄█   ██ ██ ██   █▄▄█▄▄▄▄▄█▄▄▄▄▄█▄▄▄▄▄█
█▀▀▀▀▀█▀▀▀▀▀█▀▀▀▀▀█▀▀█   ████████   █▀▀█▀▀▀▀▀█▀▀▀▀▀█▀▀▀▀▀█
█░░░░░█░░░░░█░░░░░█  █   ▄ ████     █  █░░░░░█░░░░░█░░░░░█
█▄▄▄▄▄█▄▄▄▄▄█▄▄▄▄▄█  █   ▐▄████     █  █▄▄▄▄▄█▄▄▄▄▄█▄▄▄▄▄█
                     █▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
                          ▄████▄
                         ▀▀▀▀▀▀▀▀

                         ▀▄▄▄▄▄▄▀


                       ▀▀▄▄▄▄▄▄▄▄▀▀
                       

                     ▀▀▀▄▄▄▄▄▄▄▄▄▄▀▀▀                      """

FONT_PATH = "/System/Library/Fonts/SFNSMono.ttf"
FONT_SIZE = 9
BG = (13, 17, 23)       # GitHub dark background
FG = (201, 209, 217)    # GitHub dark text
PAD = 12


def render_frame(text):
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    lines = text.split("\n")
    bbox = font.getbbox("W")
    ch = bbox[3] - bbox[1]
    cw = bbox[2] - bbox[0]
    width = max(len(l) for l in lines) * cw + PAD * 2
    height = len(lines) * ch + PAD * 2
    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)
    for i, line in enumerate(lines):
        draw.text((PAD, PAD + i * ch), line, font=font, fill=FG)
    return img


f1 = render_frame(frame1)
f2 = render_frame(frame2)

# Match sizes (pad smaller to match larger)
w = max(f1.width, f2.width)
h = max(f1.height, f2.height)


def pad_img(img, w, h):
    out = Image.new("RGB", (w, h), BG)
    out.paste(img, (0, 0))
    return out


f1 = pad_img(f1, w, h)
f2 = pad_img(f2, w, h)

f1.save(
    "ascii.gif",
    save_all=True,
    append_images=[f2],
    loop=0,
    duration=600,
    optimize=False,
)
print(f"Saved ascii.gif ({w}x{h})")
