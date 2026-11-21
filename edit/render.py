"""Render Qivea Skin Class vlog.

usage: python3 render.py <src_dir> <work_dir> <fonts_dir> <music.mp3> <out_dir> [version ...]
"""
import os, sys, subprocess, math, json
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timeline import VERSIONS, CHAPTERS

SRC, WORK, FONTS, MUSIC, OUT = sys.argv[1:6]
WANT = sys.argv[6:] or list(VERSIONS)
W, H, FPS, SR = 1080, 1920, 30, 48000

MAROON = (122, 19, 53); CORAL = (232, 112, 72); PEACH = (253, 214, 186)
CREAM = (255, 247, 238); INK = (45, 22, 28); WHITE = (255, 255, 255); YEL = (255, 214, 120)

def F(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)

def serif(size, weight="Bold"):
    f = ImageFont.truetype(os.path.join(FONTS, "PlayfairDisplay.ttf"), size)
    try: f.set_variation_by_name(weight)
    except Exception: pass
    return f

PB = lambda s: F("Poppins-Bold.ttf", s)
PX = lambda s: F("Poppins-ExtraBold.ttf", s)
PS = lambda s: F("Poppins-SemiBold.ttf", s)
PM = lambda s: F("Poppins-Medium.ttf", s)

def ease(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3

# ---------------------------------------------------------------- drawing helpers
def canvas(w, h): return Image.new("RGBA", (w, h), (0, 0, 0, 0))

def shadowed(img, radius=14, alpha=110, off=6):
    """Add soft drop shadow around an RGBA element."""
    pad = radius * 2
    out = canvas(img.width + pad * 2, img.height + pad * 2)
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    a = img.split()[3].point(lambda v: v * alpha // 255)
    blk = Image.new("RGBA", img.size, (30, 5, 12, 255)); blk.putalpha(a)
    sh.paste(blk, (pad, pad + off), blk)
    sh = sh.filter(ImageFilter.GaussianBlur(radius))
    out.alpha_composite(sh); out.alpha_composite(img, (pad, pad))
    return out, pad

def text_w(font, s): return font.getlength(s)

def tick_icon(size, bg=CORAL, fg=WHITE):
    im = canvas(size, size); d = ImageDraw.Draw(im)
    d.ellipse((0, 0, size - 1, size - 1), fill=bg)
    s = size
    d.line([(s * .27, s * .52), (s * .44, s * .68), (s * .74, s * .34)], fill=fg, width=max(3, s // 9), joint="curve")
    return im

def parse_marked(text):
    out = []
    for i, part in enumerate(text.split("*")):
        for w in part.split():
            if out and w[0] in ".,!?;:" :
                out[-1] = (out[-1][0] + w, out[-1][1]); continue
            out.append((w, i % 2 == 1))
    return out

def wrap_words(words, font, maxw):
    lines, cur, cw = [], [], 0
    sp = text_w(font, " ")
    for w, hl in words:
        ww = text_w(font, w)
        if cur and cw + sp + ww > maxw:
            lines.append(cur); cur, cw = [], 0
        cw = cw + (sp if cur else 0) + ww; cur.append((w, hl))
    if cur: lines.append(cur)
    # balance 2-line splits
    if len(lines) == 2:
        allw = lines[0] + lines[1]; best = None
        for k in range(1, len(allw)):
            a = " ".join(x for x, _ in allw[:k]); b = " ".join(x for x, _ in allw[k:])
            la, lb = text_w(font, a), text_w(font, b)
            if la <= maxw and lb <= maxw:
                sc = abs(la - lb)
                if best is None or sc < best[0]: best = (sc, k)
        if best: lines = [allw[:best[1]], allw[best[1]:]]
    return lines

# ---------------------------------------------------------------- overlay elements
# Each returns (RGBA image, x, y) in frame coordinates.
def el_subtitle(text):
    font = PB(50); lh = 66
    lines = wrap_words(parse_marked(text), font, 900)
    widths = [text_w(font, " ".join(w for w, _ in ln)) for ln in lines]
    bw = int(max(widths)) + 64; bh = lh * len(lines) + 34
    im = canvas(bw, bh); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, bw - 1, bh - 1), 26, fill=(28, 10, 16, 190))
    y = 14
    for ln, lw in zip(lines, widths):
        x = (bw - lw) / 2
        for w, hl in ln:
            col = YEL if hl else WHITE
            d.text((x, y), w, font=font, fill=col, stroke_width=0)
            x += text_w(font, w + " ")
        y += lh
    img, pad = shadowed(im, 10, 90, 4)
    return img, (W - img.width) // 2, 1720 - bh - pad

def el_header(chap):
    title = CHAPTERS[chap][0]
    f1, f2 = PX(30), PS(32)
    t1 = "QIVEA SKIN CLASS"; t2 = (f"BAB {chap}  ·  " if chap <= 3 else "") + title
    w1 = int(text_w(f1, t1)) + 44; w2 = int(text_w(f2, t2)) + 44; h = 60
    im = canvas(w1 + w2, h); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w1 + w2 - 1, h - 1), 30, fill=(255, 247, 238, 235))
    d.rounded_rectangle((0, 0, w1 - 1, h - 1), 30, fill=CORAL)
    d.text((22, 12), t1, font=f1, fill=WHITE)
    d.text((w1 + 20, 10), t2, font=f2, fill=MAROON)
    img, pad = shadowed(im, 10, 80, 4)
    return img, (W - img.width) // 2, 74 - pad

def el_chip(i, text):
    f = PB(44); w, h = 400, 104
    im = canvas(w, h); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 52, fill=CREAM)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 52, outline=CORAL, width=5)
    tw = text_w(f, text); d.text(((w - tw) / 2, 22), text, font=f, fill=MAROON)
    img, pad = shadowed(im)
    x = 120 + (i % 2) * 440; y = 1170 + (i // 2) * 130
    return img, x - pad, y - pad

def el_badge(text, sub):
    f1, f2 = PX(56), PS(36)
    w1 = int(text_w(f1, text)) + 80; w2 = int(text_w(f2, sub)) + 60
    w = max(w1, w2); im = canvas(w, 190); d = ImageDraw.Draw(im)
    d.rounded_rectangle(((w - w1) // 2, 0, (w + w1) // 2, 104), 52, fill=CORAL)
    d.text(((w - text_w(f1, text)) / 2, 14), text, font=f1, fill=WHITE)
    d.rounded_rectangle(((w - w2) // 2, 118, (w + w2) // 2, 186), 34, fill=CREAM)
    d.text(((w - text_w(f2, sub)) / 2, 129), sub, font=f2, fill=MAROON)
    img, pad = shadowed(im)
    return img, (W - img.width) // 2, 1180 - pad

def panel(w, h):
    im = canvas(w, h); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 36, fill=(255, 247, 238, 245))
    return im, d

def el_steps(title, items):
    w, h = 900, 120 + 92 * len(items); im, d = panel(w, h)
    d.rounded_rectangle((0, 0, w - 1, 86), 36, fill=MAROON); d.rectangle((0, 50, w - 1, 86), fill=MAROON)
    f = PX(40); d.text(((w - text_w(f, title)) / 2, 18), title, font=f, fill=WHITE)
    for k, s in enumerate(items):
        y = 108 + k * 92
        d.ellipse((40, y, 110, y + 70), fill=CORAL)
        n = str(k + 1); fn = PX(40); d.text((75 - text_w(fn, n) / 2, y + 8), n, font=fn, fill=WHITE)
        d.text((136, y + 9), s, font=PB(42), fill=INK)
    img, pad = shadowed(im)
    return img, (W - img.width) // 2, 1080 - pad

def el_result(i, cond, res):
    w, h = 960, 118; im, d = panel(w, h)
    fr = PX(38); rw = int(text_w(fr, res)) + 56
    d.rounded_rectangle((w - rw - 16, 18, w - 16, h - 18), 41, fill=MAROON)
    d.text((w - rw - 16 + 28, 31), res, font=fr, fill=WHITE)
    fc = PS(34); maxw = w - rw - 70
    while text_w(fc, cond) > maxw: fc = PS(fc.size - 2)
    d.text((32, (h - fc.size * 1.25) / 2), cond, font=fc, fill=INK)
    # arrow
    ax = w - rw - 44; d.polygon([(ax, 48), (ax + 18, 59), (ax, 70)], fill=CORAL)
    img, pad = shadowed(im)
    return img, (W - img.width) // 2, 1040 + i * 136 - pad

def el_warn(text):
    f = PB(38); w = int(text_w(f, text)) + 130; h = 96
    im = canvas(w, h); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 48, fill=(196, 48, 48, 240))
    d.ellipse((18, 16, 82, 80), fill=WHITE); fx = PX(46); d.text((50 - text_w(fx, "!") / 2, 13), "!", font=fx, fill=(196, 48, 48))
    d.text((100, 22), text, font=f, fill=WHITE)
    img, pad = shadowed(im)
    return img, (W - img.width) // 2, 1250 - pad

def el_info(num, title, lines, noanim=False):
    w, h = 940, 280; im, d = panel(w, h)
    d.ellipse((34, 40, 174, 180), fill=CORAL)
    fn = PX(96); d.text((104 - text_w(fn, num) / 2, 40), num, font=fn, fill=WHITE)
    d.text((206, 34), title, font=PX(52), fill=MAROON)
    for k, s in enumerate(lines):
        y = 118 + k * 66
        d.ellipse((208, y + 16, 228, y + 36), fill=CORAL)
        d.text((246, y), s, font=PM(40), fill=INK)
    d.text((40, 206), "CARA", font=PB(26), fill=CORAL)
    d.text((44, 232), f"{num}/3", font=PB(26), fill=CORAL)
    img, pad = shadowed(im)
    return img, (W - img.width) // 2, 1110 - pad

def el_recap(title, items):
    w, h = 900, 110 + 96 * len(items); im, d = panel(w, h)
    d.rounded_rectangle((0, 0, w - 1, 86), 36, fill=CORAL); d.rectangle((0, 50, w - 1, 86), fill=CORAL)
    f = PX(42); d.text(((w - text_w(f, title)) / 2, 17), title, font=f, fill=WHITE)
    tk = tick_icon(66, MAROON)
    for k, s in enumerate(items):
        y = 104 + k * 96
        im.alpha_composite(tk, (40, y)); d.text((128, y + 8), s, font=PB(42), fill=INK)
    img, pad = shadowed(im)
    return img, (W - img.width) // 2, 1080 - pad

def el_tick(i, text, noanim=False):
    w, h = 900, 104; im, d = panel(w, h)
    im.alpha_composite(tick_icon(70), (22, 17))
    f = PB(42)
    while text_w(f, text) > w - 140: f = PB(f.size - 2)
    d.text((114, (h - f.size * 1.3) / 2), text, font=f, fill=INK)
    img, pad = shadowed(im)
    return img, (W - img.width) // 2, 1090 + i * 124 - pad

def el_big(top, bottom):
    f1 = PX(150); tw = int(text_w(f1, top))
    f2 = PB(44); bw = int(text_w(f2, bottom)) + 70
    w = max(tw + 40, bw); im = canvas(w, 300); d = ImageDraw.Draw(im)
    d.text(((w - tw) / 2, 0), top, font=f1, fill=CORAL, stroke_width=10, stroke_fill=WHITE)
    d.rounded_rectangle(((w - bw) // 2, 204, (w + bw) // 2, 290), 43, fill=MAROON)
    d.text(((w - text_w(f2, bottom)) / 2, 219), bottom, font=f2, fill=WHITE)
    img, pad = shadowed(im)
    return img, (W - img.width) // 2, 1100 - pad

def el_subscribe():
    f = PX(50); t = "SUBSCRIBE"; tw = int(text_w(f, t))
    w = tw + 220; h = 120; im = canvas(w + 20, h + 80); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 60, fill=(220, 30, 40))
    d.text((60, 26), t, font=f, fill=WHITE)
    # bell
    bx, by = w - 110, 20
    d.ellipse((bx, by, bx + 80, by + 80), fill=WHITE)
    d.pieslice((bx + 18, by + 14, bx + 62, by + 62), 180, 360, fill=(220, 30, 40))
    d.rectangle((bx + 18, by + 38, bx + 62, by + 56), fill=(220, 30, 40))
    d.rectangle((bx + 12, by + 54, bx + 68, by + 60), fill=(220, 30, 40))
    d.ellipse((bx + 33, by + 60, bx + 47, by + 72), fill=(220, 30, 40))
    f2 = PS(34); s = "+ hidupkan notifikasi"
    d.text(((w - text_w(f2, s)) / 2, h + 18), s, font=f2, fill=WHITE, stroke_width=3, stroke_fill=(40, 10, 15))
    img, pad = shadowed(im)
    return img, (W - img.width) // 2, 1200 - pad

def el_live(text):
    f = PX(48); tw = int(text_w(f, text)); w = tw + 170; h = 110
    im = canvas(w, h); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 55, fill=(220, 30, 40))
    d.ellipse((40, 37, 76, 73), fill=WHITE)
    d.text((104, 22), text, font=f, fill=WHITE)
    img, pad = shadowed(im)
    return img, (W - img.width) // 2, 1220 - pad

BUILDERS = dict(chip=el_chip, badge=el_badge, steps=el_steps, result=el_result, warn=el_warn,
                info=el_info, recap=el_recap, tick=el_tick, big=el_big, subscribe=el_subscribe, live=el_live)

# ---------------------------------------------------------------- compositing
def blend(frame, img_np, x, y, opacity=1.0):
    h, w = img_np.shape[:2]
    x0, y0 = max(0, x), max(0, y); x1, y1 = min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0: return
    src = img_np[y0 - y:y1 - y, x0 - x:x1 - x]
    a = src[..., 3:4].astype(np.float32) * (opacity / 255.0)
    reg = frame[y0:y1, x0:x1].astype(np.float32)
    frame[y0:y1, x0:x1] = (reg * (1 - a) + src[..., :3] * a).astype(np.uint8)

class Placed:
    def __init__(self, built, t0, t1, anim=True, slide=36):
        img, self.x, self.y = built
        self.np = np.asarray(img.convert("RGBA")); self.t0, self.t1 = t0, t1
        self.anim, self.slide = anim, slide
    def draw(self, frame, t):
        if t < self.t0 or (self.t1 is not None and t >= self.t1): return
        k = ease((t - self.t0) / 0.28) if self.anim else 1.0
        if self.t1 is not None and self.anim:
            k = min(k, ease((self.t1 - t) / 0.12) if self.t1 - t < 0.12 else 1.0)
        blend(frame, self.np, self.x, self.y + int((1 - k) * self.slide), k)

# ---------------------------------------------------------------- cards
_bg_cache = {}
def card_bg():
    if "bg" not in _bg_cache:
        p = os.path.join(WORK, "card_bg.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.4", "-i", os.path.join(SRC, "C2326.MP4"),
                        "-frames:v", "1", "-vf", f"scale={W}:{H}", p], check=True)
        im = Image.open(p).convert("RGB").filter(ImageFilter.GaussianBlur(28))
        ov = Image.new("RGB", im.size, CREAM)
        im = Image.blend(im, ov, 0.72)
        # soft coral glow blobs
        g = canvas(W, H); d = ImageDraw.Draw(g)
        d.ellipse((-300, -250, 600, 650), fill=(*CORAL, 70)); d.ellipse((560, 1350, 1500, 2250), fill=(*MAROON, 45))
        g = g.filter(ImageFilter.GaussianBlur(120))
        im = im.convert("RGBA"); im.alpha_composite(g)
        _bg_cache["bg"] = np.asarray(im.convert("RGB")).copy()
    return _bg_cache["bg"]

def center_text(text, font, fill, y, stroke=0, sfill=None):
    im = canvas(W, int(font.size * 1.5)); d = ImageDraw.Draw(im)
    d.text(((W - text_w(font, text)) / 2, 0), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=sfill)
    return (im, 0, y)

def wordmark(y, size=190):
    f = serif(size, "Bold"); t = "QIVEA"
    sp = size * 0.12; total = sum(text_w(f, c) for c in t) + sp * (len(t) - 1)
    im = canvas(W, int(size * 1.45)); d = ImageDraw.Draw(im); x = (W - total) / 2
    for c in t:
        d.text((x, 0), c, font=f, fill=MAROON); x += text_w(f, c) + sp
    return (im, 0, y)

def pill(text, font, bg, fg, y, padx=40, h=None):
    tw = int(text_w(font, text)); h = h or int(font.size * 1.75); w = tw + padx * 2
    im = canvas(w, h); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), h // 2, fill=bg)
    d.text((padx, (h - font.size * 1.32) / 2), text, font=font, fill=fg)
    return (im, (W - w) // 2, y)

def wrap_center(text, font, maxw):
    words = [(w, False) for w in text.split()]
    return [" ".join(w for w, _ in ln) for ln in wrap_words(words, font, maxw)]

def card_items(seg):
    t = seg["type"]; items = []
    if t == "intro":
        items += [(wordmark(470), 0.05, 26), (center_text("SKIN CLASS", PX(78), CORAL, 760), 0.25, 26)]
        items += [(center_text("Belajar jaga kulit bersama team Qivea", PM(40), INK, 880), 0.45, 20)]
        agenda = [("01", "Kenali jenis kulit"), ("02", "3 cara pilih sabun"), ("03", "Siapa sesuai sabun scrub")]
        for k, (n, s) in enumerate(agenda):
            w, h = 760, 104; im = canvas(w, h); d = ImageDraw.Draw(im)
            d.rounded_rectangle((0, 0, w - 1, h - 1), 52, fill=(255, 255, 255, 235))
            d.ellipse((14, 12, 94, 92), fill=MAROON); fn = PX(36); d.text((54 - text_w(fn, n) / 2, 26), n, font=fn, fill=WHITE)
            d.text((122, 24), s, font=PB(42), fill=INK)
            img, pad = shadowed(im)
            items.append(((img, (W - img.width) // 2, 1080 + k * 132 - pad), 0.9 + k * 0.28, 40))
    elif t == "chapter":
        c = seg["chap"]; title, sub = CHAPTERS[c]
        label = f"BAB {c}" if c <= 3 else "PROMO"
        items.append((pill(label, PX(48), CORAL, WHITE, 640), 0.05, 30))
        tf = PX(96); lines = wrap_center(title, tf, 940)
        y = 800
        for k, ln in enumerate(lines):
            items.append((center_text(ln, tf, MAROON, y), 0.18 + k * 0.08, 34)); y += 118
        items.append((center_text(sub, PM(42), INK, y + 30), 0.4, 24))
        # accent bar
        bar = canvas(160, 10); ImageDraw.Draw(bar).rounded_rectangle((0, 0, 159, 9), 5, fill=CORAL)
        items.append(((bar, (W - 160) // 2, y + 120), 0.5, 0))
    elif t == "end":
        items += [(wordmark(560), 0.05, 26), (center_text("Terima kasih kerana belajar", PB(54), INK, 900), 0.3, 24),
                  (center_text("bersama kami!", PB(54), INK, 975), 0.38, 24),
                  (pill("Jumpa di Skin Class seterusnya", PS(40), CORAL, WHITE, 1110), 0.6, 30),
                  (center_text("Music: \"Carefree\" Kevin MacLeod (incompetech.com)", PM(26), (110, 80, 85), 1690), 0.8, 0),
                  (center_text("Licensed under Creative Commons: By Attribution 4.0", PM(26), (110, 80, 85), 1728), 0.8, 0)]
    return items

# ---------------------------------------------------------------- per-version render
def frames_of(seg):
    return int(round((seg["b"] - seg["a"]) * FPS)) if seg["kind"] == "clip" else int(round(seg["dur"] * FPS))

def clip_reader(seg, n):
    z = seg["zoom"]; cw, ch = int(W / z) // 2 * 2, int(H / z) // 2 * 2
    cx, cy = (W - cw) // 2, int((H - ch) * 0.32)
    vf = (f"fps={FPS},scale={W}:{H},crop={cw}:{ch}:{cx}:{cy},scale={W}:{H}:flags=lanczos,"
          f"eq=contrast=1.04:saturation=1.08:brightness=0.01,unsharp=5:5:0.4")
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{seg['a']:.3f}", "-i", os.path.join(SRC, seg["clip"] + ".MP4"),
           "-t", f"{n / FPS + 0.2:.3f}", "-vf", vf, "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    last = None
    for _ in range(n):
        buf = p.stdout.read(W * H * 3)
        if len(buf) == W * H * 3:
            last = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        yield last.copy()
    p.stdout.close(); p.wait()

def build_audio(segs, path):
    parts = []
    for s in segs:
        n = frames_of(s); ns = int(round(n / FPS * SR))
        if s["kind"] == "card":
            parts.append(np.zeros(ns, np.float32)); continue
        tmp = os.path.join(WORK, "a_tmp.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s['a']:.3f}", "-i", os.path.join(SRC, s["clip"] + ".MP4"),
                        "-t", f"{n / FPS + 0.1:.3f}", "-vn", "-ac", "1", "-ar", str(SR), tmp], check=True)
        a, _ = sf.read(tmp, dtype="float32"); a = np.pad(a, (0, max(0, ns - len(a))))[:ns]
        f = int(0.025 * SR); r = np.linspace(0, 1, f, dtype=np.float32)
        a[:f] *= r; a[-f:] *= r[::-1]
        parts.append(a)
    sf.write(path, np.concatenate(parts), SR)

def render(version):
    segs = VERSIONS[version]
    total = sum(frames_of(s) for s in segs)
    print(f"[{version}] {len(segs)} segments, {total / FPS:.1f}s", flush=True)
    voice = os.path.join(WORK, f"{version}_voice.wav"); build_audio(segs, voice)

    # audio mix: cleaned voice + ducked music
    mix = os.path.join(WORK, f"{version}_mix.wav"); dur = total / FPS
    fc = (f"[0:a]highpass=f=90,lowpass=f=14000,acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=2,"
          f"aresample={SR},asplit=2[v][key];"
          f"[1:a]aresample={SR},aformat=channel_layouts=stereo,volume=0.30,atrim=0:{dur:.3f},"
          f"afade=t=in:d=0.6,afade=t=out:st={dur - 2.8:.3f}:d=2.8[m];"
          f"[m][key]sidechaincompress=threshold=0.015:ratio=10:attack=30:release=450:makeup=1[md];"
          f"[v]aformat=channel_layouts=stereo[vs];"
          f"[vs][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", voice, "-i", MUSIC, "-filter_complex", fc,
                    "-map", "[out]", "-ar", str(SR), mix], check=True)

    out = os.path.join(OUT, f"{version}.mp4")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-i", mix, "-map", "0:v", "-map", "1:a",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-maxrate", "4M", "-bufsize", "8M",
                            "-pix_fmt", "yuv420p", "-profile:v", "high", "-c:a", "aac", "-b:a", "192k",
                            "-movflags", "+faststart", "-shortest", out], stdin=subprocess.PIPE)
    header_cache = {}
    done = 0
    for si, s in enumerate(segs):
        n = frames_of(s)
        if s["kind"] == "card":
            items = [Placed(b, t0, None, True, sl) for b, t0, sl in card_items(s)]
            bg = card_bg()
            for f in range(n):
                t = f / FPS; fr = bg.copy()
                for it in items: it.draw(fr, t)
                # fade in from / out to previous a little
                k = min(1.0, (f + 1) / 6, (n - f) / 5)
                if k < 1: fr = (fr.astype(np.float32) * (0.6 + 0.4 * k) + 255 * (1 - k) * 0.4).astype(np.uint8)
                prog(fr, done + f, total); enc.stdin.write(fr.tobytes())
        else:
            a = s["a"]; dur = n / FPS
            subs = [Placed(el_subtitle(tx), t0 - a, min(t1 - a, dur), True, 14) for t0, t1, tx in s["subs"]]
            ovs = []
            for t0, t1, kind, kw in s["ov"]:
                kw = dict(kw); noanim = kw.pop("noanim", False)
                b = BUILDERS[kind](**kw) if kind not in ("info", "tick") else BUILDERS[kind](noanim=noanim, **kw)
                ovs.append(Placed(b, t0 - a, None if t1 is None else t1 - a, not noanim))
            if s["chap"] not in header_cache: header_cache[s["chap"]] = Placed(el_header(s["chap"]), 0, None, False)
            hdr = header_cache[s["chap"]]
            for f, fr in enumerate(clip_reader(s, n)):
                t = f / FPS
                hdr.draw(fr, t)
                for o in ovs: o.draw(fr, t)
                for o in subs: o.draw(fr, t)
                prog(fr, done + f, total); enc.stdin.write(fr.tobytes())
        done += n
        print(f"  seg {si + 1}/{len(segs)} done ({done / FPS:.1f}s)", flush=True)
    enc.stdin.close(); enc.wait()
    print("wrote", out, flush=True)

def prog(fr, i, total):
    w = int(W * (i + 1) / total)
    fr[0:10, :] = (fr[0:10, :].astype(np.uint16) * 2 // 5 + 150).astype(np.uint8)
    fr[0:10, :w] = CORAL

if __name__ == "__main__":
    os.makedirs(WORK, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    for v in WANT: render(v)
