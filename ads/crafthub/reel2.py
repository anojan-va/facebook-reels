"""The Craft Hub reel 2 - "Making friends in Berlin is hard. Making a mug isn't." Paper-cut group portrait behind a
craft table: alone -> strangers -> friends, then the membership perks as a notebook checklist.
python3 reel2.py [--plan | --stills | --frame t1,t2]"""
import math
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import craftkit as C
from craftkit import CREAM, GREEN, MUSTARD, SAGE, TERRA, BLUSH, PAPER, K, W, H, put

TABLE_Y = 1080   # top edge of the table (front view)
SEATS = [("p-person1", 175), ("p-person2", 420), ("p-person3", 665), ("p-person4", 905)]


@lru_cache(maxsize=1)
def table_layer():
    """Front view of the wooden craft table: a band cut from the oak texture, with a darker front edge."""
    im = Image.open(C.HERE / "img/p-table.jpg").convert("RGB")
    wood = im.crop((int(im.width * 0.2), int(im.height * 0.2), int(im.width * 0.8), int(im.height * 0.8)))
    wood = wood.rotate(90, expand=True).resize((W + 80, 300))
    a = np.asarray(wood).astype(np.float32)
    a[230:] *= 0.72   # front edge
    a[:12] *= 1.08
    rgba = np.dstack([np.clip(a, 0, 255).astype(np.uint8), np.full(a.shape[:2], 255, np.uint8)])
    return C._with_shadow(rgba, 10, 18, 0.35)


def scene_base(t, color=(247, 239, 228), seed=60):
    return C.paper(color, t, seed)


def draw_table(fr, t):
    put(fr, table_layer(), W / 2, TABLE_Y + 150, t=t, i=99, jitter=0.2)


def person(fr, name, x, t, i, pop=None, s=0.4, slide=None):
    """Paper-cut person sitting behind the table (waist-up visible above it)."""
    xx = x
    if slide is not None:   # slide in from a side
        p = K.ease_out((C.st(t) - slide[0]) / 0.35)
        if p <= 0:
            return
        xx = x + (1 - p) * slide[1]
    put(fr, C.sprite(name), xx, TABLE_Y + 30, s, t=t, i=i, pop=pop, anchor="b")


@lru_cache(maxsize=16)
def bubble(txt, size=58, flip=False):
    f = ImageFont.truetype(C.HAND2, size)
    w = int(f.getlength(txt)) + 60
    h = int(size * 1.7)
    im = Image.new("RGBA", (w + 10, h + 50), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((4, 4, w, h), 34, fill=(255, 255, 255, 255), outline=(*GREEN, 255), width=5)
    tx = w * (0.75 if flip else 0.25)
    d.polygon([(tx - 18, h - 2), (tx + 18, h - 2), (tx + (20 if flip else -20), h + 40)], fill=(255, 255, 255, 255), outline=(*GREEN, 255))
    d.line((tx - 15, h - 3, tx + 15, h - 3), fill=(255, 255, 255, 255), width=8)
    d.text((32, h / 2 - size * 0.66), txt, font=f, fill=(*GREEN, 255))
    return np.asarray(im)


@lru_cache(maxsize=1)
def notebook():
    """Lined notebook page with a red margin, torn top edge and binder holes."""
    w, h = 880, 1000
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(4)
    top = [(x, 18 + rng.uniform(-8, 8)) for x in range(0, w + 1, 20)]
    d.polygon([(0, h), *top, (w, h)], fill=(253, 251, 244, 255))
    for y in range(170, h - 20, 74):
        d.line((0, y, w, y), fill=(160, 190, 215, 255), width=3)
    d.line((110, 30, 110, h), fill=(225, 120, 110, 255), width=4)
    for y in (200, 500, 800):
        d.ellipse((34, y - 20, 74, y + 20), fill=(230, 222, 208, 255))
    return C._with_shadow(np.asarray(im), 10, 16, 0.3)


PERKS = ["Craft & Connect nights: free", "monthly workshop credit", "book 3 days early"]


# ------------------------------------------------------------------ scenes
def s_alone(t, d, a, ctx):
    fr = scene_base(t, (236, 232, 226), 61)
    put(fr, C.text("Making friends", 150, GREEN), W / 2, 330, t=t, i=1, pop=(0.0, 0.3))
    put(fr, C.text("in Berlin is hard.", 150, GREEN), W / 2, 500, t=t, i=2, pop=(0.25, 0.3))
    person(fr, "p-person1-sad", 300, t, 3, pop=(0.05, 0.3), s=0.46)
    # little rain cloud doodle
    if C.st(t) > 0.5:
        cx, cy = 300, 760
        for j, (dx, r) in enumerate([(-60, 45), (0, 62), (60, 45)]):
            C.hand_line(fr, [(cx + dx + r * math.cos(u), cy + r * 0.7 * math.sin(u)) for u in np.linspace(math.pi, 2 * math.pi, 14)],
                        1, (120, 130, 140), 7, j, t)
        for j in range(4):
            y0 = cy + 40 + ((C.st(t) * 300 + j * 37) % 90)
            C.hand_line(fr, [(cx - 60 + j * 40, y0), (cx - 66 + j * 40, y0 + 26)], 1, (120, 150, 190), 6, j + 5, t)
    draw_table(fr, t)
    for x in (560, 800):   # empty seats (chair backs)
        C.hand_line(fr, [(x - 70, TABLE_Y), (x - 70, TABLE_Y - 200), (x + 70, TABLE_Y - 200), (x + 70, TABLE_Y)], 1, (150, 120, 90), 10, int(x), t)
    return fr


def s_mug(t, d, a, ctx):
    fr = scene_base(t, BLUSH, 62)
    put(fr, C.text("Making a mug?", 150, GREEN), W / 2, 300, t=t, i=1, pop=(0.0, 0.3))
    put(fr, C.torn_card("img/o-mug.jpg", 700, 24, seed=70), W / 2, 860, rot=-4, t=t, i=2, pop=(0.1, 0.3))
    put(fr, C.label("      surprisingly easy", 84, GREEN, CREAM), W / 2, 1400, rot=-2, t=t, i=3, pop=(0.55, 0.3), jitter=0.4)
    if C.st(t) > 0.7:
        C.tick(fr, 230, 1392, 64, (C.st(t) - 0.75) / 0.25, MUSTARD, t)
    for j, (x, y) in enumerate([(170, 560), (930, 700), (900, 1150)]):
        if C.st(t) > 0.3 + 0.1 * j:
            C.star(fr, x, y, 26, MUSTARD, t, j)
    return fr


def table_scene(t, a, ctx, color=(247, 239, 228)):
    fr = scene_base(t, color, 63)
    sl = a.get("slide", False)
    for j, (nm, x) in enumerate(SEATS):
        if a.get("laugh") and nm == "p-person1":
            nm = "p-person1-laugh"
        person(fr, nm, x, t, 10 + j, s=0.44, slide=(0.05 + 0.22 * j, (-1 if x < W / 2 else 1) * 700) if sl else None)
    draw_table(fr, t)
    return fr


def s_strangers(t, d, a, ctx):
    fr = table_scene(t, {"slide": True}, ctx)
    put(fr, C.label("strangers", 110, CREAM, GREEN, C.HAND), W / 2, 300, rot=-3, t=t, i=1, pop=(0.0, 0.3))
    return fr


def items_on_table(fr, t, start=0.0):
    for j, (nm, x, r) in enumerate([("img/o-yarn.jpg", 230, -9), ("img/o-palette.jpg", 540, 5), ("img/o-hoop.jpg", 850, -4)]):
        p = K.ease_out((C.st(t) - start - 0.14 * j) / 0.3)
        if p > 0:
            put(fr, C.torn_card(nm, 300, 12, seed=80 + j), x, TABLE_Y + 120 + (1 - p) * 500, rot=r, t=t, i=40 + j)


def s_materials(t, d, a, ctx):
    fr = table_scene(t, {}, ctx)
    items_on_table(fr, t, 0.05)
    put(fr, C.label("share the materials", 84, GREEN, CREAM), W / 2, 300, rot=2, t=t, i=1, pop=(0.0, 0.3))
    return fr


def s_hands(t, d, a, ctx):
    fr = scene_base(t, (232, 238, 226), 64)
    for j, (nm, x, y, r) in enumerate([("img/o-lino.jpg", 330, 620, -7), ("img/o-mug.jpg", 760, 760, 6), ("img/o-hoop.jpg", 380, 1130, 4)]):
        put(fr, C.torn_card(nm, 480, 18, seed=90 + j), x, y, rot=r, t=t, i=1 + j, pop=(0.05 + 0.15 * j, 0.3))
    put(fr, C.label("made by hand", 86, CREAM, TERRA, C.HAND), 760, 1240, rot=-4, t=t, i=6, pop=(0.5, 0.3))
    return fr


def s_giggles(t, d, a, ctx):
    fr = table_scene(t, {}, ctx)
    items_on_table(fr, 9, 0.0)
    for j, (txt, x, y, fl, at) in enumerate([("hi!", 200, 520, False, 0.05), ("first time?", 470, 380, False, 0.3),
                                             ("me too!", 700, 540, True, 0.6), ("haha", 900, 380, True, 0.9)]):
        put(fr, bubble(txt, 60, fl), x, y, t=t, i=50 + j, pop=(at, 0.22))
    return fr


def s_friends(t, d, a, ctx):
    fr = table_scene(t, {"laugh": True}, ctx, (250, 233, 222))
    items_on_table(fr, 9, 0.0)
    heads = [(x, TABLE_Y - 400) for _, x in SEATS]
    k = (C.st(t) - 0.05) / 0.6
    for j in range(3):   # stitched lines join the group
        (x0, y0), (x1, y1) = heads[j], heads[j + 1]
        C.hand_line(fr, [(x0 + 60, y0 - 160), ((x0 + x1) / 2, y0 - 230), (x1 - 60, y1 - 160)], k * 3 - j, TERRA, 6, j, t)
    for j, (x, y) in enumerate([(300, 420), (545, 380), (790, 420)]):
        if C.st(t) > 0.3 + 0.12 * j:
            C.heart(fr, x, y, 2.4, TERRA, t, j)
    put(fr, C.label("friends", 120, CREAM, TERRA, C.HAND), W / 2, 260, rot=-3, t=t, i=1, pop=(0.1, 0.3))
    return fr


def s_perks(t, d, a, ctx):
    fr = scene_base(t, (232, 238, 226), 65)
    put(fr, notebook(), W / 2, 900, rot=-2, t=t, i=1, jitter=0.4)
    put(fr, C.washi(320, 76, MUSTARD, "dots", 7), W / 2, 420, rot=-6, t=t, i=2, jitter=0.4)
    put(fr, C.text("Members get:", 120, TERRA), W / 2, 560, t=t, i=3, jitter=0.4)
    n = a["n"]
    for j in range(n):
        y = 770 + j * 190
        lay = C.text(PERKS[j], 52, GREEN, C.HAND2)
        put(fr, lay, 280 + lay.shape[1] / 2, y, t=t, i=10 + j, pop=((0.0 if j == n - 1 else -9), 0.25), jitter=0.4)
        cv_k = (C.st(t) - 0.15) / 0.25 if j == n - 1 else 1.0
        C.tick(fr, 225, y - 4, 64, cv_k, TERRA, t)
    if n == 3 and C.st(t) > 0.45:   # tiny calendar doodle
        C.hand_line(fr, [(820, 1240), (960, 1240), (960, 1360), (820, 1360), (820, 1240)], 1, GREEN, 6, 9, t)
        put(fr, C.text("3", 90, TERRA), 890, 1310, t=t, i=30)
    return fr


def s_come_alone(t, d, a, ctx):
    fr = scene_base(t, (236, 232, 226), 66)
    p = K.ease_out((C.st(t)) / 0.35)
    put(fr, C.sprite("p-person1"), 200 + p * 340, 1320, 0.55, t=t, i=1, anchor="b")
    put(fr, C.text("Come alone.", 170, GREEN), W / 2, 420, t=t, i=2, pop=(0.0, 0.3))
    return fr


def s_leave_friends(t, d, a, ctx):
    fr = scene_base(t, (250, 233, 222), 67)
    for j, (nm, x, s) in enumerate([("p-person2", 260, 0.45), ("p-person4", 820, 0.45), ("p-person3", 640, 0.48),
                                    ("p-person1-laugh", 420, 0.52)]):
        put(fr, C.sprite(nm), x, 1400, s, t=t, i=1 + j, pop=(0.03 * j, 0.3), anchor="b")
    put(fr, C.text("Leave with friends.", 140, TERRA), W / 2, 400, t=t, i=6, pop=(0.0, 0.3))
    for j, (x, y) in enumerate([(160, 650), (930, 700)]):
        C.heart(fr, x, y, 3.2, TERRA, t, j)
    return fr


def s_wonky(t, d, a, ctx):
    fr = scene_base(t, (232, 238, 226), 68)
    put(fr, C.torn_card("img/o-wonky.jpg", 720, 24, seed=99), W / 2, 760, rot=6, t=t, i=1, pop=(0.0, 0.3))
    put(fr, C.label("(slightly wonky)", 90, CREAM, TERRA, C.HAND), 690, 1260, rot=-5, t=t, i=2, pop=(0.4, 0.3))
    C.hand_line(fr, [(560, 1190), (470, 1120), (430, 1040)], (C.st(t) - 0.55) / 0.3, GREEN, 8, 4, t)
    put(fr, C.sprite("p-person1-laugh"), 190, 1500, 0.3, t=t, i=3, pop=(0.6, 0.3), anchor="b")
    return fr


shots = [
    dict(w=0, scene=s_alone, cap=False, sfx=["hook", {"name": "paper", "at": 0.0}, {"name": "scribble", "at": 0.55}]),
    dict(w=6, scene=s_mug, tr="page", cap=False, sfx=[{"name": "pop", "at": 0.12}, {"name": "scribble", "at": 0.75}]),
    dict(w=11, scene=s_strangers, tr="slide", sfx=[{"name": "paper", "at": 0.05 + 0.22 * j, "gain": 0.7} for j in range(4)]),
    dict(w=16, scene=s_materials, sfx=[{"name": "paperq", "at": 0.05}, {"name": "page", "at": 0.2}, {"name": "page", "at": 0.34}]),
    dict(w=19, scene=s_hands, tr="tear", sfx=[{"name": "pop", "at": 0.05 + 0.15 * j} for j in range(3)]),
    dict(w=25, scene=s_giggles, tr="page", sfx=[{"name": "ui-pop", "at": at} for at in (0.05, 0.3, 0.6, 0.9)]),
    dict(w=33, scene=s_friends, tr="whip", cap=False, sfx=[{"name": "bubble", "at": 0.1}, {"name": "pencil", "at": 0.05, "gain": 0.5}]),
    dict(w=36, scene=s_perks, a={"n": 1}, tr="page", cap=False, sfx=[{"name": "scribble", "at": 0.2}]),
    dict(w=43, scene=s_perks, a={"n": 2}, cap=False, sfx=[{"name": "scribble", "at": 0.2}]),
    dict(w=47, scene=s_perks, a={"n": 3}, cap=False, sfx=[{"name": "scribble", "at": 0.2}, {"name": "pop", "at": 0.5}]),
    dict(w=52, scene=s_come_alone, tr="slide", cap=False, sfx=[{"name": "paper", "at": 0.0}]),
    dict(w=54, scene=s_leave_friends, tr="tear", cap=False, sfx=[{"name": "pop", "at": 0.03 * j} for j in range(4)]),
    dict(w=57, scene=s_wonky, tr="page", cap_y=1640, sfx=[{"name": "bloop", "at": 0.1}, {"name": "scribble", "at": 0.6}]),
    dict(scene=C.end_card, tr="page", cap=False, after=0.35, dur=2.6, a={"line": "Craft & Connect nights from €10"},
         sfx=[{"name": "paper", "at": 0.1}, {"name": "wink", "at": 0.6}]),
]

if __name__ == "__main__":
    spec = dict(name="crafthub-reel-2", voice="reel2/voice-1.wav", max_gap=0.34, shots=shots, caption=C.cap, post=C.post,
                music=[{"t": 0.0, "file": "music/happy-home.mp3", "start": 11.28, "vol": 1.0}],
                music_volume=0.3, duck=0.38, tail_gain=0.6)
    K.render(spec)
