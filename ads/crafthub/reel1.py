"""The Craft Hub reel 1 - "Berlin, you need a new hobby": six real workshops as a scrapbook countdown.
python3 reel1.py [--plan | --stills | --frame t1,t2]"""
import math

import numpy as np

import craftkit as C
from craftkit import CREAM, GREEN, MUSTARD, SAGE, TERRA, BLUSH, PAPER, K, W, H, put, st

WORKSHOPS = [   # (photo, label, sub, paper colour, extra)
    ("img/o-mug.jpg", "First Spin", "pottery wheel · €85", (250, 233, 222), "stamp"),
    ("img/o-lino.jpg", "Lino carving", "make your own Christmas cards", (232, 238, 226), "carve"),
    ("img/o-wine-clay.jpg", "Sip & Clay", "pottery, wine & good company", BLUSH, "hearts"),
    ("img/o-hoop.jpg", "The Stitch Circle", "embroidery club", (246, 236, 210), "stitch"),
    ("img/o-wallet.jpg", "Leather craft", "your own card wallet", (238, 228, 214), "stars"),
    ("img/o-tea.jpg", "Craft & Connect", "community craft night", (226, 236, 228), "price"),
]


def s_hook(t, d, a, ctx):
    fr = C.paper(CREAM, t, 1)
    put(fr, C.sprite("p-tower"), W * 0.8, H * 0.9, 0.85, rot=4, t=t, i=1, pop=(0.0, 0.35), anchor="b")
    for j, (x, y, s) in enumerate([(200, 330, 30), (880, 420, 22), (150, 1120, 18)]):
        if C.st(t) > 0.15 + j * 0.1:
            C.star(fr, x, y, s, C.MUSTARD, t, j)
    put(fr, C.text("Berlin,", 280, GREEN), W * 0.34, 1050, rot=-4, t=t, i=2, pop=(0.02, 0.3))
    return fr


def s_hobby(t, d, a, ctx):
    fr = C.paper(CREAM, t, 1)
    put(fr, C.sprite("p-tower"), W * 0.82, H * 0.97, 0.55, rot=4, t=t, i=1, anchor="b")
    put(fr, C.text("you need a", 150, GREEN), W / 2, 420, t=t, i=2, pop=(0.0, 0.25))
    put(fr, C.text("new hobby.", 230, TERRA), W / 2, 620, t=t, i=3, pop=(0.25, 0.3))
    C.underline(fr, 180, 900, 760, (C.st(t) - 0.5) / 0.4, GREEN, t)
    return fr


def grid_pos(i, n=6):
    col, row = i % 2, i // 2
    return 310 + col * 460, 380 + row * 400


def s_six(t, d, a, ctx):
    fr = C.paper(PAPER, t, 2)
    put(fr, C.text("6", 520, TERRA), W / 2, 820, t=t, i=0, pop=(0.0, 0.3), alpha=0.18, jitter=0.3)
    for i, w in enumerate(WORKSHOPS):
        x, y = grid_pos(i)
        put(fr, C.torn_card(w[0], 340, 14, seed=i), x, y, rot=(-1) ** i * (5 + i), t=t, i=10 + i, pop=(0.1 + 0.13 * i, 0.3))
    put(fr, C.label("to try this month", 72, GREEN, CREAM), W / 2, 1420, rot=-2, t=t, i=30, pop=(0.6, 0.3))
    return fr


def s_noexp(t, d, a, ctx):
    fr = C.paper(TERRA, t, 3)
    put(fr, C.sprite("p-person2"), W * 0.5, H * 0.92, 1.0, t=t, i=1, pop=(0.0, 0.35), anchor="b")
    put(fr, C.label("      no experience needed", 76, GREEN, CREAM), W / 2, 520, rot=0, t=t, i=2, pop=(0.05, 0.3), jitter=0.4)
    if C.st(t) > 0.2:
        C.tick(fr, 150, 512, 64, (C.st(t) - 0.3) / 0.3, MUSTARD, t)
    return fr


def s_card(t, d, a, ctx):
    i = a["i"]
    photo, name, sub, bg, extra = WORKSHOPS[i]
    fr = C.paper(bg, t, 10 + i)
    cx, cy = W / 2, 700
    put(fr, C.torn_card(photo, 780, 26, seed=20 + i), cx, cy, rot=(-1) ** i * 3, t=t, i=1, pop=(0.0, 0.3))
    put(fr, C.washi(300, 72, [MUSTARD, SAGE, TERRA][i % 3], ["dots", "stripes"][i % 2], i), cx - 220, cy - 400,
        rot=-18, t=t, i=2, pop=(0.12, 0.2))
    put(fr, C.washi(260, 72, [SAGE, TERRA, MUSTARD][i % 3], ["stripes", "dots"][i % 2], i + 5), cx + 260, cy - 380,
        rot=24, t=t, i=3, pop=(0.18, 0.2))
    # number badge
    b = C.text(f"{i + 1}/6", 120, TERRA)
    put(fr, b, 150, 210, rot=-8, t=t, i=4, pop=(0.05, 0.25))
    put(fr, C.label(name, 96, GREEN, CREAM, C.HAND), W / 2, 1210, rot=-2, t=t, i=5, pop=(0.25, 0.3))
    put(fr, C.text(sub, 58, GREEN, C.HAND2), W / 2, 1345, t=t, i=6, pop=(0.4, 0.3))
    ts = C.st(t)
    if extra == "stamp" and ts > 0.55:
        put(fr, C.stamp("SELLS OUT FAST"), 860, 1020, 0.9, t=t, i=7, pop=(0.55, 0.15), jitter=0.3)
    elif extra == "stitch":
        C.stitches(fr, 120, 270, 960, 1130, (ts - 0.2) / 0.8, TERRA, t)
    elif extra == "hearts" and ts > 0.4:
        for j, (x, y) in enumerate([(170, 330), (930, 520), (880, 1080)]):
            if ts > 0.4 + 0.12 * j:
                C.heart(fr, x, y, 2.4, TERRA, t, j)
    elif extra == "stars":
        for j, (x, y) in enumerate([(150, 400), (950, 330), (930, 1050)]):
            if ts > 0.35 + 0.12 * j:
                C.star(fr, x, y, 28, MUSTARD, t, j)
    elif extra == "carve":
        for j in range(4):
            y = 360 + j * 50
            C.hand_line(fr, [(110, y), (190, y - 30)], (ts - 0.3 - j * 0.08) / 0.15, GREEN, 6, j, t)
    elif extra == "price":
        tag = C.label("from €10", 110, CREAM, TERRA, C.HAND)
        swing = 8 * math.sin(ts * 7) * math.exp(-ts * 1.5)
        put(fr, tag, 820, 1020, rot=-10 + swing, t=t, i=8, pop=(0.45, 0.3), jitter=0.2)
    return fr


def s_groups(t, d, a, ctx):
    fr = C.paper((232, 238, 226), t, 30)
    put(fr, C.torn_card("img/o-tea.jpg", 520, 20, seed=40), W / 2, 520, rot=-3, t=t, i=1)
    for j, (nm, x, y) in enumerate([("p-person1", 220, 1120), ("p-person2", 540, 1160), ("p-person3", 860, 1120)]):
        put(fr, C.sprite(nm), x, y, 0.42, t=t, i=2 + j, pop=(0.05 + 0.12 * j, 0.3), anchor="b")
    put(fr, C.label("small groups", 76, GREEN, CREAM), 330, 1230, rot=-4, t=t, i=6, pop=(0.1, 0.25))
    put(fr, C.label("mostly in English", 76, CREAM, TERRA), 730, 1340, rot=3, t=t, i=7, pop=(0.55, 0.25))
    return fr


def s_which(t, d, a, ctx):
    fr = C.paper(CREAM, t, 40)
    for i, w in enumerate(WORKSHOPS):
        x, y = grid_pos(i)
        put(fr, C.torn_card(w[0], 330, 14, seed=i), x, y, rot=(-1) ** i * (4 + i), t=t, i=10 + i)
        put(fr, C.text(str(i + 1), 110, TERRA), x - 140, y - 130, t=t, i=20 + i, pop=(0.05 + 0.08 * i, 0.25))
    put(fr, C.label("comment your number", 76, CREAM, GREEN), W / 2, 1380, rot=-2, t=t, i=30, pop=(0.4, 0.3))
    return fr


shots = [
    dict(w=0, scene=s_hook, cap=False, sfx=["hook", {"name": "paper", "at": 0.0}]),
    dict(w=1, scene=s_hobby, tr="tear", cap=False, sfx=[{"name": "scribble", "at": 0.5}]),
    dict(w=6, scene=s_six, tr="page", cap_y=1600, sfx=[{"name": "page", "at": 0.1 + 0.13 * i, "gain": 0.7} for i in range(6)]),
    dict(w=14, scene=s_noexp, tr="whip", cap=False, sfx=[{"name": "scribble", "at": 0.3}, {"name": "pop", "at": 0.05}]),
] + [
    dict(w=w, scene=s_card, a={"i": i}, tr=["slide", "page", "tear", "slide", "page", "tear"][i],
         sfx=[{"name": "tape", "at": 0.12, "gain": 0.5}, {"name": "pop", "at": 0.27}]
         + ([{"name": "bass", "at": 0.55, "gain": 0.5}] if i == 0 else [])
         + ([{"name": "pencil", "at": 0.2, "gain": 0.6}] if i in (1, 3) else [])
         + ([{"name": "ding", "at": 0.45, "gain": 0.6}] if i == 5 else []))
    for i, w in enumerate([17, 24, 29, 35, 39, 44])
] + [
    dict(w=53, scene=s_groups, tr="whip", cap=False, sfx=[{"name": "pop", "at": 0.05 + 0.12 * j} for j in range(3)]),
    dict(w=58, scene=s_which, tr="page", cap_y=1560, sfx=[{"name": "pop", "at": 0.05 + 0.08 * j, "gain": 0.6} for j in range(6)]),
    dict(w=None, scene=C.end_card, tr="page", cap=False, dur=2.6, a={},
         sfx=[{"name": "paper", "at": 0.1}, {"name": "wink", "at": 0.6}]),
]

if __name__ == "__main__":
    spec = dict(name="crafthub-reel-1", voice="reel1/voice-1.wav", max_gap=0.32, shots=shots, caption=C.cap, post=C.post,
                fixes={"€10.": "€10."}, music=[{"t": 0.0, "file": "music/okay.mp3", "start": 15.28, "vol": 1.0}],
                music_volume=0.3, duck=0.38, tail_gain=0.6)
    voice, words = K.prepare_voice(spec["voice"], K.HERE / "work" / spec["name"], spec["max_gap"], 1.0, spec["fixes"])
    shots[-1].pop("w")
    shots[-1]["after"] = 0.35
    shots[-1]["dur"] = 2.6
    K.render(spec)
