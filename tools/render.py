import sys, os, math, subprocess, wave, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from episodes import EPISODES

SCR = sys.argv[1]            # scratchpad dir
KEY = sys.argv[2]            # episode key
PREVIEW = len(sys.argv) > 3 and sys.argv[3] == "preview"
EP = EPISODES[KEY]
RAW = f"{SCR}/raw/A"
WORK = f"{SCR}/work/{KEY}"; os.makedirs(WORK, exist_ok=True)
OUTDIR = f"{SCR}/out"; os.makedirs(OUTDIR, exist_ok=True)
MUSIC = f"{SCR}/music/Easy_Lemon.mp3"
W, H, FPS = 1080, 1920, 30
RECAP = 4.2

# ---------- palette & fonts (Qivea papaya theme) ----------
PAPAYA = (242, 106, 61); CORAL = (244, 154, 126); CREAM = (255, 246, 236)
SAGE = (63, 94, 75); DARK = (42, 35, 32); MAROON = (140, 28, 58); YELLOW = (255, 196, 75)
FD = "/usr/share/fonts/opentype/inter/"
@functools.lru_cache(None)
def F(name, size): return ImageFont.truetype(FD + name + ".otf", size)
SERIF = "/usr/share/fonts/truetype/crosextra/Caladea-Bold.ttf"

def ease_out(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def ease_back(x):
    x = min(max(x, 0), 1); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

def rrect(w, h, r, fill):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=fill)
    return im

def shadowed(im, blur=18, off=8, alpha=90):
    pad = blur * 2
    sh = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    a = im.split()[3].point(lambda v: v * alpha // 255)
    blk = Image.new("RGBA", im.size, (0, 0, 0, 255)); blk.putalpha(a)
    sh.paste(blk, (pad, pad + off), blk)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    sh.alpha_composite(im, (pad, pad))
    return sh, pad

def put(canvas, im, cx, cy, alpha=1.0, scale=1.0, anchor="c"):
    if alpha <= 0.01: return
    if abs(scale - 1) > 0.005:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BICUBIC)
    if alpha < 0.999:
        im = im.copy(); a = im.split()[3].point(lambda v: int(v * alpha)); im.putalpha(a)
    x = int(cx - im.width / 2) if anchor == "c" else int(cx)
    y = int(cy - im.height / 2)
    canvas.alpha_composite(im, (max(x, 0), max(y, 0)), (max(-x, 0), max(-y, 0)))

def check_icon(d, cx, cy, s, col):
    d.line([(cx - s * .45, cy), (cx - s * .12, cy + s * .32), (cx + s * .48, cy - s * .34)], fill=col, width=max(3, int(s * .18)), joint="curve")

# ---------- timeline ----------
segs = EP["segments"]; G = []; t = 0
for s in segs: G.append(t); t += s["out"] - s["in"]
SPEECH_END = t; TOTAL = t + RECAP
def g(i, src_t): s = segs[i]; return G[i] + (min(max(src_t, s["in"]), s["out"]) - s["in"])

subs = []; ev = {"rows": {}, "panel": None, "done": None, "badges": [], "cta": None, "timer": None, "tzone": None, "poll": None}
sfx = [(0.05, "whoosh")]
for i, s in enumerate(segs):
    for (txt, a, b) in s["subs"]: subs.append((g(i, a), g(i, b), txt))
    for e in s.get("events", []):
        k = e[0]
        if k == "panel": ev["panel"] = g(i, e[1]); sfx.append((ev["panel"], "whoosh"))
        elif k == "row": ev["rows"][e[2]] = g(i, e[1]); sfx.append((g(i, e[1]), "pop"))
        elif k == "done": ev["done"] = g(i, e[1]); sfx.append((ev["done"], "ding"))
        elif k in ("badge", "warn"):
            ev["badges"].append((k, g(i, e[1]), g(i, e[2]), e[3:])); sfx.append((g(i, e[1]), "pop"))
        elif k == "cta": ev["cta"] = (g(i, e[1]), e[2]); sfx.append((g(i, e[1]), "ding"))
        elif k == "timer": ev["timer"] = (g(i, e[1]), g(i, e[2])); sfx.append((g(i, e[1]), "pop"))
        elif k == "tzone": ev["tzone"] = (g(i, e[1]), g(i, e[2])); sfx.append((g(i, e[1]), "pop"))
        elif k == "poll":
            ev["poll"] = (g(i, e[1]), g(i, e[2]), [g(i, x) for x in e[3]])
            for x in e[3]: sfx.append((g(i, x), "pop"))
for k in range(3): sfx.append((SPEECH_END + 0.75 + k * 0.32, "tick"))
sfx.append((SPEECH_END + 0.05, "whoosh"))

# ---------- sprites ----------
@functools.lru_cache(None)
def header_sprites():
    f = F("Inter-Bold", 30); lab = EP["label"]
    tw = int(f.getlength(lab)); pill = rrect(tw + 56, 56, 28, SAGE + (255,))
    ImageDraw.Draw(pill).text((28, 28), lab, font=f, fill=CREAM, anchor="lm")
    f1 = F("InterDisplay-ExtraBold", 60); f2 = F("InterDisplay-ExtraBold", 50)
    l1, l2 = EP["title"]; w = int(max(f1.getlength(l1), f2.getlength(l2))) + 90
    card = rrect(w, 172, 32, CREAM + (248,)); d = ImageDraw.Draw(card)
    d.text((w // 2, 56), l1, font=f1, fill=DARK, anchor="mm"); d.text((w // 2, 122), l2, font=f2, fill=PAPAYA, anchor="mm")
    card, _ = shadowed(card)
    return pill, card

PW, PX, PY0, RH, PH0 = 940, 70, 170, 80, 74
@functools.lru_cache(None)
def row_sprite(idx, state):  # state: active / done / idle
    im = Image.new("RGBA", (PW - 28, RH - 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if state == "active": d.rounded_rectangle((0, 0, im.width - 1, im.height - 1), 20, fill=PAPAYA + (46,))
    cx, cy, r = 44, im.height // 2, 26
    col = SAGE if state == "done" else PAPAYA
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col)
    if state == "done": check_icon(d, cx, cy, 30, CREAM)
    else: d.text((cx, cy), str(idx + 1), font=F("Inter-Bold", 30), fill="white", anchor="mm")
    txt = EP["rows"][idx]; f = F("Inter-Bold" if state == "active" else "Inter-SemiBold", 33)
    while f.getlength(txt) > im.width - 100 and f.size > 24: f = F(f.path.split("/")[-1][:-4], f.size - 1)
    d.text((88, cy), txt, font=f, fill=DARK if state != "done" else (88, 80, 74), anchor="lm")
    return im

@functools.lru_cache(None)
def panel_bg(h):
    bg = rrect(PW, h, 30, CREAM + (244,)); d = ImageDraw.Draw(bg)
    d.rounded_rectangle((0, 0, 12, h - 1), 6, fill=PAPAYA)
    d.text((40, 40), EP["panel_title"], font=F("Inter-ExtraBold", 31), fill=PAPAYA, anchor="lm")
    sh, pad = shadowed(bg, blur=16, off=6, alpha=70)
    return sh, pad

def wrap_tokens(text, font, maxw):
    # words between *...* are highlighted (closing * may be followed by punctuation)
    words, hl, on = [], [], False
    for raw in text.split(" "):
        st = raw.startswith("*"); en = raw.rstrip(",.!?:;").endswith("*")
        if st: on = True
        words.append(raw.replace("*", "")); hl.append(on)
        if en: on = False
    lines, cur, curw = [], [], 0; sp = font.getlength(" ")
    for w, h in zip(words, hl):
        lw = font.getlength(w)
        if cur and curw + sp + lw > maxw: lines.append(cur); cur, curw = [], 0
        cur.append((w, h)); curw += (sp if len(cur) > 1 else 0) + lw
    if cur: lines.append(cur)
    return lines

@functools.lru_cache(None)
def sub_sprite(text):
    f = F("InterDisplay-ExtraBold", 66); lines = wrap_tokens(text, f, 900); sp = f.getlength(" ")
    lh = 84; h = lh * len(lines) + 30
    im = Image.new("RGBA", (W, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for li, line in enumerate(lines):
        lw = sum(f.getlength(w) for w, _ in line) + sp * (len(line) - 1); x = (W - lw) / 2; y = 15 + li * lh + lh / 2
        for w, hlt in line:
            d.text((x, y), w, font=f, fill=YELLOW if hlt else "white", anchor="lm", stroke_width=8, stroke_fill=(20, 16, 14))
            x += f.getlength(w) + sp
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); a = im.split()[3].filter(ImageFilter.GaussianBlur(10)).point(lambda v: v * 0.5)
    sh.putalpha(a); out = Image.new("RGBA", im.size, (0, 0, 0, 0)); out.alpha_composite(sh, (0, 6)); out.alpha_composite(im)
    return out

@functools.lru_cache(None)
def badge_sprite(kind, args):
    if kind == "warn":
        txt = args[0]; f = F("Inter-Bold", 36); tw = int(f.getlength(txt))
        im = rrect(tw + 140, 96, 48, MAROON + (250,)); d = ImageDraw.Draw(im)
        d.ellipse((22, 20, 78, 76), fill=YELLOW); d.text((50, 49), "!", font=F("Inter-Black", 40), fill=MAROON, anchor="mm")
        d.text((100, 48), txt, font=f, fill="white", anchor="lm")
    else:
        tag, txt = args; ft = F("Inter-Black", 34); f = F("Inter-Bold", 36)
        tgw = int(ft.getlength(tag)) + 40; tw = int(f.getlength(txt))
        im = rrect(tgw + tw + 70, 100, 50, PAPAYA + (252,)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((14, 14, 14 + tgw, 86), 36, fill=CREAM)
        d.text((14 + tgw / 2, 50), tag, font=ft, fill=PAPAYA, anchor="mm")
        d.text((tgw + 40, 50), txt, font=f, fill="white", anchor="lm")
    return shadowed(im)[0]

@functools.lru_cache(None)
def cta_sprite(txt):
    f = F("Inter-ExtraBold", 38); tw = int(f.getlength(txt))
    im = rrect(tw + 150, 100, 50, (255, 255, 255, 252)); d = ImageDraw.Draw(im)
    d.ellipse((22, 18, 86, 82), fill=PAPAYA)
    d.rounded_rectangle((36, 34, 72, 60), 8, fill="white"); d.polygon([(44, 58), (44, 70), (56, 58)], fill="white")
    d.text((110, 50), txt, font=f, fill=DARK, anchor="lm")
    d.polygon([(tw + 118, 42), (tw + 138, 42), (tw + 128, 58)], fill=PAPAYA)
    return shadowed(im)[0]

def timer_sprite(p):
    S = 240; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((10, 10, S - 10, S - 10), fill=CREAM + (250,))
    d.arc((26, 26, S - 26, S - 26), 0, 360, fill=(235, 215, 200), width=16)
    if p > 0.001: d.arc((26, 26, S - 26, S - 26), -90, -90 + 360 * p, fill=PAPAYA, width=16)
    d.text((S / 2, S / 2 - 14), "30", font=F("InterDisplay-Black", 76), fill=DARK, anchor="mm")
    d.text((S / 2, S / 2 + 44), "MINIT", font=F("Inter-Bold", 26), fill=PAPAYA, anchor="mm")
    return shadowed(im, blur=14)[0]

@functools.lru_cache(None)
def tzone_sprite():
    im = rrect(760, 200, 40, CREAM + (250,)); d = ImageDraw.Draw(im)
    cx, cy = 110, 100
    d.ellipse((cx - 62, cy - 82, cx + 62, cy + 82), outline=(120, 100, 90), width=5)
    d.rounded_rectangle((cx - 48, cy - 64, cx + 48, cy - 34), 12, fill=PAPAYA + (230,))
    d.rounded_rectangle((cx - 14, cy - 40, cx + 14, cy + 66), 12, fill=PAPAYA + (230,))
    d.text((210, 70), "T-ZONE", font=F("InterDisplay-Black", 52), fill=PAPAYA, anchor="lm")
    d.text((210, 132), "= dahi + hidung + dagu", font=F("Inter-SemiBold", 34), fill=DARK, anchor="lm")
    return shadowed(im)[0]

POLL = ["KERING", "BERMINYAK", "KOMBINASI", "SENSITIF"]
@functools.lru_cache(None)
def chip(i, on):
    im = rrect(400, 84, 42, (PAPAYA + (252,)) if on else (255, 255, 255, 235)); d = ImageDraw.Draw(im)
    d.text((200, 42), POLL[i], font=F("Inter-ExtraBold", 36), fill="white" if on else (120, 110, 104), anchor="mm")
    return shadowed(im, blur=10, off=4, alpha=60)[0]

@functools.lru_cache(None)
def recap_parts():
    card = rrect(940, 620, 40, CREAM + (252,)); d = ImageDraw.Draw(card)
    d.text((470, 70), EP["recap_title"], font=F("Inter-ExtraBold", 40), fill=PAPAYA, anchor="mm")
    d.line((350, 112, 590, 112), fill=CORAL, width=4)
    d.text((470, 530), "QIVEA", font=ImageFont.truetype(SERIF, 66), fill=SAGE, anchor="mm")
    d.text((470, 580), "Kelas Kulit · follow untuk tips seterusnya", font=F("Inter-Medium", 26), fill=(110, 100, 94), anchor="mm")
    rows = []
    for i, txt in enumerate(EP["rows"]):
        r = Image.new("RGBA", (860, 96), (0, 0, 0, 0)); rd = ImageDraw.Draw(r)
        rd.ellipse((10, 20, 66, 76), fill=SAGE); check_icon(rd, 38, 48, 32, CREAM)
        f = F("Inter-Bold", 34)
        while f.getlength(txt) > 760: f = F("Inter-Bold", f.size - 1)
        rd.text((90, 48), txt, font=f, fill=DARK, anchor="lm"); rows.append(r)
    credit = Image.new("RGBA", (W, 40), (0, 0, 0, 0))
    ImageDraw.Draw(credit).text((W / 2, 20), "Muzik: \"Easy Lemon\" – Kevin MacLeod (incompetech.com) · CC BY 4.0",
                                font=F("Inter-Medium", 22), fill=(255, 255, 255, 190), anchor="mm")
    return shadowed(card, blur=24, off=10, alpha=110)[0], rows, credit

# ---------- per-frame compositor ----------
def frame(t):
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    if t >= SPEECH_END:   # recap screen
        rt = t - SPEECH_END
        c.paste((20, 12, 10, int(120 * ease_out(rt / 0.4))), (0, 0, W, H))
        card, rows, credit = recap_parts()
        k = ease_out(rt / 0.45); put(c, card, W / 2, 960 + 80 * (1 - k), alpha=k)
        for i, r in enumerate(rows):
            kk = ease_out((rt - 0.75 - i * 0.32) / 0.3)
            put(c, r, W / 2 + 20 - 40 * (1 - kk), 960 - 310 + 190 + i * 110 + 80 * (1 - k), alpha=kk * k)
        put(c, credit, W / 2, 1850, alpha=ease_out((rt - 0.5) / 0.5))
        d.rectangle((0, 0, W, 10), fill=PAPAYA)
        return c
    # progress bar
    d.rectangle((0, 0, int(W * t / SPEECH_END), 10), fill=PAPAYA)
    # header: label + title until panel appears
    pill, card = header_sprites(); pa = ev["panel"] if ev["panel"] is not None else 1e9
    out = ease_out((t - pa) / 0.3); k = ease_out(t / 0.45)
    if out < 1:
        put(c, pill, W / 2, 196 - 30 * (1 - k), alpha=k * (1 - out))
        put(c, card, W / 2, 340 - 30 * (1 - k), alpha=k * (1 - out), scale=0.94 + 0.06 * ease_back(t / 0.45))
    # panel
    if t >= pa:
        pk = ease_out((t - pa) / 0.35)
        rows_p = [ease_out((t - ev["rows"][i]) / 0.3) if i in ev["rows"] and t >= ev["rows"][i] else 0 for i in range(3)]
        h = int(PH0 + sum(rows_p) * RH + 10)
        bg, pad = panel_bg(h); put(c, bg, PX - pad, PY0 + h / 2 - 22 * (1 - pk), alpha=pk, anchor="l")
        active = max([i for i in range(3) if rows_p[i] > 0], default=None)
        done = ev["done"] is not None and t >= ev["done"]
        for i in range(3):
            if rows_p[i] <= 0: continue
            st = "done" if done or (active is not None and i < active) else ("active" if i == active else "idle")
            rs = row_sprite(i, st)
            put(c, rs, PX + 14 - 40 * (1 - rows_p[i]), PY0 + PH0 + i * RH + RH / 2 - 4 - 22 * (1 - pk), alpha=rows_p[i] * pk, anchor="l")
    # subtitles
    for (a, b, txt) in subs:
        if a <= t < b:
            sp = sub_sprite(txt); x = (t - a)
            put(c, sp, W / 2, 1335, alpha=min(1, x / 0.07), scale=0.86 + 0.14 * ease_back(x / 0.16))
            break
    # lower-third callouts
    LY = 1555
    for kind, a, b, args in ev["badges"]:
        if a <= t < b + 0.25:
            x = t - a; o = 1 - ease_out((t - b) / 0.25) if t > b else 1
            put(c, badge_sprite(kind, tuple(args)), W / 2, LY, alpha=o * min(1, x / 0.1), scale=0.7 + 0.3 * ease_back(x / 0.3))
    if ev["timer"]:
        a, b = ev["timer"]
        if a <= t < b + 0.25:
            x = t - a; o = 1 - ease_out((t - b) / 0.25) if t > b else 1
            put(c, timer_sprite(ease_out(x / (b - a - 0.3))), W / 2, LY + 20, alpha=o * min(1, x / 0.1), scale=0.6 + 0.4 * ease_back(x / 0.35))
    if ev["tzone"]:
        a, b = ev["tzone"]
        if a <= t < b + 0.25:
            x = t - a; o = 1 - ease_out((t - b) / 0.25) if t > b else 1
            put(c, tzone_sprite(), W / 2, LY + 10, alpha=o * min(1, x / 0.1), scale=0.7 + 0.3 * ease_back(x / 0.3))
    if ev["poll"]:
        a, b, starts = ev["poll"]
        if a - 0.2 <= t < b:
            o = ease_out((t - a + 0.2) / 0.25) * (1 - ease_out((t - b + 0.25) / 0.25))
            for i in range(4):
                on = t >= starts[i]; bump = 1 + 0.12 * math.sin(math.pi * min(1, max(0, (t - starts[i]) / 0.3))) if on else 1
                put(c, chip(i, on), W / 2 + (-210 if i % 2 == 0 else 210), LY - 30 + (i // 2) * 104, alpha=o, scale=bump)
    if ev["cta"] and t >= ev["cta"][0]:
        x = t - ev["cta"][0]
        put(c, cta_sprite(ev["cta"][1]), W / 2, LY + 6 * math.sin(x * 5) - 0, alpha=min(1, x / 0.12), scale=0.6 + 0.4 * ease_back(x / 0.35))
    return c

# ---------- SFX ----------
def make_sfx(path):
    sr = 48000; n = int(TOTAL * sr) + sr; buf = np.zeros(n, np.float32); rng = np.random.default_rng(1)
    def env(L, dec): tt = np.arange(L) / sr; return np.exp(-tt / dec)
    tt = lambda L: np.arange(L) / sr
    L = int(.09 * sr); f = np.linspace(950, 420, L); pop = np.sin(2 * np.pi * np.cumsum(f) / sr) * env(L, .025) * .32
    L2 = int(.5 * sr); ding = (np.sin(2 * np.pi * 1318 * tt(L2)) + .5 * np.sin(2 * np.pi * 1976 * tt(L2))) * env(L2, .12) * .16
    L3 = int(.12 * sr); tick = np.sin(2 * np.pi * 1760 * tt(L3)) * env(L3, .02) * .18
    L4 = int(.45 * sr); nz = rng.standard_normal(L4); spec = np.fft.rfft(nz); fr = np.fft.rfftfreq(L4, 1 / sr)
    spec *= np.exp(-((fr - 2200) / 1600) ** 2); wh = np.fft.irfft(spec, L4); wh /= np.abs(wh).max()
    wh *= np.sin(np.pi * tt(L4) / tt(L4)[-1]) ** 2 * .16
    S = {"pop": pop, "ding": ding, "tick": tick, "whoosh": wh}
    for (tm, k) in sfx:
        i = int(tm * sr); s = S[k]; buf[i:i + len(s)] += s[:max(0, n - i)]
    pcm = (np.clip(buf, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "w") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())

def run(cmd): subprocess.run(cmd, check=True)

if PREVIEW:
    for tm in [float(x) for x in sys.argv[4].split(",")]:
        fr = frame(tm); src = None
        # find source frame for background
        if tm < SPEECH_END:
            i = max(j for j in range(len(segs)) if G[j] <= tm); s = segs[i]; st = s["in"] + tm - G[i]
        else:
            i = len(segs) - 1; s = segs[i]; st = s["out"] - 0.05
        bgp = f"{WORK}/bg.png"
        z = s["zoom"]; vf = f"scale=trunc(1080*{z}/2)*2:trunc(1920*{z}/2)*2,crop=1080:1920:{540*z-540}:{800*z-800}"
        if tm >= SPEECH_END: vf += ",boxblur=20:2"
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{st}", "-i", f"{RAW}/{s['src']}.mp4", "-frames:v", "1", "-vf", vf, bgp])
        bg = Image.open(bgp).convert("RGBA"); bg.alpha_composite(fr)
        bg.convert("RGB").resize((540, 960)).save(f"{WORK}/prev_{tm:05.2f}.jpg", quality=85)
    sys.exit()

# ---------- 1. base segments ----------
lst = []
for i, s in enumerate(segs):
    dur = s["out"] - s["in"]; z = s["zoom"]; o = f"{WORK}/seg{i:02d}.mkv"; lst.append(o)
    vf = f"fps=30,scale=trunc(1080*{z}/2)*2:trunc(1920*{z}/2)*2,crop=1080:1920:{540*z-540}:{800*z-800},setsar=1"
    af = f"aresample=48000,afade=t=in:d=0.025,afade=t=out:st={dur-0.05:.3f}:d=0.05"
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s['in']}", "-i", f"{RAW}/{s['src']}.mp4", "-t", f"{dur:.3f}",
         "-vf", vf, "-af", af, "-c:v", "libx264", "-crf", "12", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", o])
with open(f"{WORK}/list.txt", "w") as fh:
    for o in lst: fh.write(f"file '{o}'\n")
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{WORK}/list.txt", "-c", "copy", f"{WORK}/base.mkv"])
make_sfx(f"{WORK}/sfx.wav")

# ---------- 2. composite ----------
NF = int(round(TOTAL * FPS))
fc = (f"[0:v]tpad=stop_mode=clone:stop_duration={RECAP},boxblur=24:2:enable='gte(t,{SPEECH_END:.3f})'[bv];"
      f"[bv][1:v]overlay=0:0:format=auto:eof_action=pass,format=yuv420p[v];"
      f"[0:a]apad=pad_dur={RECAP},highpass=f=80,afftdn=nf=-28,acompressor=threshold=-22dB:ratio=3:attack=5:release=90:makeup=2,"
      f"loudnorm=I=-15:TP=-2:LRA=9,aresample=48000,aformat=channel_layouts=stereo,asplit=2[voice][sc];"
      f"[2:a]atrim=0:{TOTAL:.3f},asetpts=N/SR/TB,loudnorm=I=-27:TP=-4,aresample=48000,aformat=channel_layouts=stereo,"
      f"afade=t=in:d=0.8,afade=t=out:st={TOTAL-2.2:.3f}:d=2.2[mus];"
      f"[mus][sc]sidechaincompress=threshold=0.05:ratio=4:attack=40:release=400[duck];"
      f"[3:a]aformat=channel_layouts=stereo[fx];"
      f"[voice][duck][fx]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.93[a]")
cmd = ["ffmpeg", "-v", "error", "-y", "-i", f"{WORK}/base.mkv",
       "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
       "-i", MUSIC, "-i", f"{WORK}/sfx.wav", "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
       "-t", f"{TOTAL:.3f}", "-r", str(FPS), "-c:v", "libx264", "-crf", "19", "-preset", "medium", "-profile:v", "high",
       "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", f"{OUTDIR}/{KEY}.mp4"]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for n in range(NF):
    p.stdin.write(frame(n / FPS).tobytes())
    if n % 150 == 0: print(f"{KEY} frame {n}/{NF}", flush=True)
p.stdin.close(); p.wait()
print("DONE", KEY, f"{TOTAL:.2f}s", "rc", p.returncode)
