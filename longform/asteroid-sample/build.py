"""Shot list for the 1-minute "What if a giant asteroid was about to hit Earth?" sample -> video.json.
Visual grammar: stock (V) for real-world statements, cinematic AI stills (I) with camera moves for the story beats,
HyperFrames cards (HF, full-screen MP4s in motion/) for numbers/maps/chapter, Remotion alpha layers (RM, PNG
sequences in motion/) on top for kinetic numbers, HUD countdowns, stamps and the target reticle.
Checks that the shot texts reproduce script.txt word for word."""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent


def I(img, focus=(0.5, 0.5), zoom=1.05, to=None, to_zoom=None, drift=0.05):
    v = {"img": f"img/{img}.jpg", "focus": list(focus), "zoom": zoom, "drift": drift}
    if to or to_zoom:
        v.update({"to": list(to or focus), "to_zoom": to_zoom or zoom, "drift": 0})
    return v


def V(name, start=0.0, zoom=1.08, drift=0.05, focus=(0.5, 0.5), rate=1.0):
    return {"video": f"stock/{name}.mp4", "start": start, "zoom": zoom, "drift": drift, "focus": list(focus), "rate": rate}


def HF(name):   # HyperFrames card, already in the channel look: no stock grade
    return {"video": f"motion/{name}.mp4", "start": 0.0, "zoom": 1.0, "drift": 0.0, "grade": False}


def RM(name, at=0.0, **kw):   # Remotion alpha layer
    return {"mg": "clip", "dir": f"motion/{name}", "at": at, **kw}


S = [
    # ---- hook
    dict(text="What if a giant asteroid", v=V("meteor-earth", 0.5, zoom=1.2, drift=0.12), punch=True, sfx=["hook"]),
    dict(text="was about to hit Earth?", in_="zoom", v=I("asteroid-earth", (0.3, 0.5), 1.0, to=(0.6, 0.5), to_zoom=1.35),
         captions=False, overlays=[RM("title", 0.0)],
         sfx=[{"name": "boom", "at": "@Earth", "gain": 0.6}], shake=["@Earth"]),
    dict(text="Not a small one.", in_="glitch", v=I("rock-surface", (0.5, 0.5), 1.1, to_zoom=1.5),
         sfx=["glitch-hit", {"name": "bass", "at": "@small", "gain": 0.7}]),
    dict(text="A rock ten kilometres wide,", in_="flash", v=HF("size"),
         sfx=[{"name": "impact", "at": 0.95, "gain": 0.7}, {"name": "sweep", "at": 1.0, "gain": 0.6},
              {"name": "pop", "at": 1.25, "gain": 0.7}]),
    dict(text="the same size as the one that wiped out the dinosaurs.", in_="whip",
         v=I("dino-fireball", (0.45, 0.6), 1.0, to=(0.6, 0.35), to_zoom=1.3),
         sfx=["whoosh", {"name": "boom", "at": "@wiped", "gain": 0.7}], shake=["@wiped"]),
    dict(text="In this video, we'll follow it step by step,", in_="whip", v=V("meteor-storm", 1.0, zoom=1.1, drift=0.1),
         sfx=["swoosh"]),
    dict(text="from the first warning", in_="glitch", v=V("control-room", 8.0, zoom=1.15, drift=0.08),
         sfx=["glitch", {"name": "zap", "at": 0.1, "gain": 0.5}]),
    dict(text="to the world it leaves behind.", in_="dip", v=I("wasteland", (0.5, 0.6), 1.25, to=(0.5, 0.55), to_zoom=1.0),
         sfx=["tunnel"]),
    dict(text="And by the end, you'll see why", in_="whip", v=V("earth-night", 6.0, zoom=1.1, drift=0.08), sfx=["swoosh-fast"]),
    dict(text="space agencies are already practising for this exact day.", in_="zoom",
         v=I("dart", (0.35, 0.5), 1.0, to=(0.6, 0.45), to_zoom=1.3),
         overlays=[RM("dart", "@agencies")], sfx=["sweep", {"name": "typing", "at": "@agencies+0.35", "gain": 0.5}]),
    # ---- chapter one
    dict(text="Chapter one. Twenty four hours to impact.", in_="dip", pause_before=0.25, captions=False, v=HF("chapter"),
         sfx=[{"name": "reveal", "at": 0.0}, {"name": "impact", "at": "@Twenty", "gain": 0.8},
              {"name": "bass", "at": "@impact", "gain": 0.8}]),
    dict(text="Telescopes spot it", in_="whip", v=V("observatory", 1.5, zoom=1.1, drift=0.1), sfx=["swoosh", {"name": "shutter", "at": "@spot"}]),
    dict(text="far beyond the Moon,", in_="zoom", v=I("past-moon", (0.5, 0.5), 1.0, to=(0.55, 0.5), to_zoom=1.4), sfx=["whoosh2"]),
    dict(text="racing toward us at about twenty kilometres every second.", in_="flash",
         v=V("meteor-3", 1.0, zoom=1.1, drift=0.15), overlays=[RM("speed", "@twenty-0.25")],
         sfx=[{"name": "trailer", "at": "@twenty"}, {"name": "tick", "at": "@kilometres"}]),
    dict(text="That's fast enough", in_="whip", v=V("map-point", 3.0, zoom=1.15, drift=0.1), sfx=["swoosh-fast"]),
    dict(text="to cross the entire United States in under four minutes.", in_="flash", v=HF("crossing"),
         sfx=[{"name": "sweep", "at": 0.4}, {"name": "whoosh", "at": 1.2, "gain": 0.6}, {"name": "impact", "at": "@under", "gain": 0.6}]),
    dict(text="With only one day left,", in_="glitch", v=I("astronomer", (0.6, 0.4), 1.1, to=(0.68, 0.32), to_zoom=1.5),
         overlays=[RM("t24", 0.0, alpha=0.95)], sfx=["glitch", {"name": "heartbeat", "at": 0.2, "gain": 0.8}]),
    dict(text="there's no time to launch a spacecraft and push it away.", in_="whip", v=V("rocket", 3.0, zoom=1.1, drift=0.08),
         overlays=[RM("notime", "@spacecraft")], music_fx="muffle",
         sfx=["whoosh", {"name": "impact", "at": "@spacecraft", "gain": 0.8}], shake=["@spacecraft"]),
    dict(text="So the only question left", in_="whip", v=V("telescope-man", 6.0, zoom=1.1, drift=0.06), sfx=["swoosh"]),
    dict(text="is where it will land.", in_="zoom", v=V("earth-spin", 4.0, zoom=1.0, drift=0.25, focus=(0.42, 0.5)),
         overlays=[RM("target", 0.0)], voice_fx={"at": "@land", "fx": "echo"},
         sfx=[{"name": "zap", "at": 0.05, "gain": 0.5}, {"name": "bass", "at": "@land", "gain": 0.8}]),
    dict(text="Cities empty overnight.", in_="dip", v=I("empty-city", (0.5, 0.55), 1.0, to_zoom=1.25),
         sfx=[{"name": "tunnel", "gain": 0.7}]),
    dict(text="Highways jam.", in_="flash", v=V("traffic-jam", 2.0, zoom=1.15, drift=0.1), punch={"at": "@jam", "zoom": 1.4},
         sfx=[{"name": "impact", "at": "@jam", "gain": 0.6}]),
    dict(text="People head for high ground,", in_="whip", v=I("mountain-road", (0.5, 0.6), 1.0, to=(0.5, 0.35), to_zoom=1.3), sfx=["swoosh"]),
    dict(text="and deep underground.", in_="zoom", v=I("bunker", (0.5, 0.5), 1.0, to=(0.47, 0.45), to_zoom=1.6),
         sfx=[{"name": "boom", "at": "@underground", "gain": 0.5}]),
    # ---- final hour
    dict(text="And then, in the final hour,", in_="glitch", v=V("city-skyline", 8.0, zoom=1.15, drift=0.08),
         overlays=[RM("t1", 0.0)], sfx=["glitch-hit", {"name": "heartbeat", "at": "@final", "gain": 0.9}]),
    dict(text="a new star appears in the sky,", in_="whip", v=I("new-star", (0.5, 0.6), 1.0, to=(0.53, 0.35), to_zoom=1.25),
         sfx=["whoosh2", {"name": "sparkle", "at": "@star", "gain": 0.8}]),
    dict(text="and it's getting brighter.", in_="flash", v=I("new-star", (0.53, 0.3), 1.6, to=(0.53, 0.18), to_zoom=2.6),
         sfx=[{"name": "riser", "at": "@brighter+1.0"}]),
    dict(text="Everyone on Earth is about to find out", in_="whip", v=V("crowd-bridge", 8.0, zoom=1.1, drift=0.08),
         amb={"name": "crowd-murmur", "gain": 0.12}, sfx=["swoosh"]),
    dict(text="what ten kilometres of rock can do.", in_="flash", v=I("fireball-city", (0.55, 0.45), 1.0, to=(0.55, 0.42), to_zoom=1.35),
         punch={"at": "@do", "zoom": 1.5, "focus": [0.55, 0.42]}, shake=["@rock", "@do"],
         sfx=[{"name": "boom", "at": "@rock", "gain": 0.8}, {"name": "impact", "at": "@do"}, {"name": "bass", "at": "@do"}]),
]

shots = []
for s in S:
    s = dict(s)
    if "in_" in s:
        s["in"] = s.pop("in_")
    shots.append(s)

script = re.sub(r"\s+", " ", (HERE / "script.txt").read_text()).strip()
said = " ".join(s["text"] for s in shots)
assert said == script, f"shot texts drift from script:\n{said}\n---\n{script}"

spec = {
    "out": "../output/asteroid-sample.mp4",
    "audio": "voice-b.wav",
    "speed": 1.0,
    "music_cues": [{"shot": 0, "music": "../../reels/audio/music/echoes.mp3", "start": 162.865},
                   {"shot": 10, "music": "../../reels/audio/music/out-of-this-world.mp3", "start": 117.26}],
    "music_volume": 0.4,
    "fade_out": 1.2,
    "progress": True,
    "shots": shots,
}
(HERE / "video.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False))
print(f"{len(shots)} shots -> video.json")
