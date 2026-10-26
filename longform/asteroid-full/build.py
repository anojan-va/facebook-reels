"""Build video.json for the full "What if a giant asteroid was about to hit Earth?" video (~11 min).

Intro + chapter one are the approved 1-minute sample (../asteroid-sample/video.json, same assets copied here).
Chapters 2-6: compact (text, visual, extras) lists. Transitions, transition SFX, graphic SFX, chapter openers and
music cues are added by rule (auto()); extras override. Shot texts are checked word for word against chapters/chN.txt.
Visual sources: I() cinematic AI still, V() Mixkit stock, HF() HyperFrames card (motion/*.mp4), RM() Remotion alpha
overlay (motion/<name>/ PNG sequence), K() kinetic text and the renderer's own motion graphics.
Usage: python3 build.py  ->  video.json
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent


def I(n, f=(.5, .5), z=1.05, to=None, tz=None, **kw):
    v = {"img": f"img/{n}.jpg", "focus": list(f), "zoom": z, "drift": kw.pop("drift", 0.06), **kw}
    if to or tz:
        v.update({"to": list(to or f), "to_zoom": tz or z, "drift": 0})
    return v


def V(n, st=1.0, z=1.08, **kw):
    return {"video": f"stock/{n}.mp4", "start": st, "zoom": z, "drift": kw.pop("drift", 0.06), **kw}


def HF(n):
    return {"video": f"motion/{n}.mp4", "start": 0.0, "zoom": 1.0, "drift": 0.0, "grade": False}


def RM(n, at=0.0, **kw):
    return {"mg": "clip", "dir": f"motion/{n}", "at": at, **kw}


def K(*lines, times=None, size=150, **kw):
    lines = [[l, "white"] if isinstance(l, str) else list(l) for l in lines]
    return {"mg": "kinetic", "lines": lines, "times": times or [0.0] * len(lines), "size": size, **kw}


def KO(*lines, times=None, size=130, dy=-60):   # kinetic words as an overlay on footage
    lines = [[l, "white"] if isinstance(l, str) else list(l) for l in lines]
    return {"mg": "kinetic", "lines": lines, "times": times or [0.0] * len(lines), "size": size, "dy": dy, "at": 0.0}


def LT(title, sub, at=0.1, y=0.66):
    return {"mg": "lower_third", "title": title, "sub": sub, "at": at, "y": y}


def TAG(text, at=0.0):
    return {"mg": "tag", "text": text, "at": at, "pos": [0.04, 0.08]}


# name: (file, first start, volume that levels it to ~ -15 LUFS like echoes / out-of-this-world)
TRACKS = {"intrigue": ("../../reels/audio/music/echoes.mp3", 162.865, 1.0),
          "tense": ("../../reels/audio/music/out-of-this-world.mp3", 117.26, 1.0),
          "punchy": ("../../reels/audio/music/trapanomics.mp3", 0.0, 0.56),
          "sad": ("../../reels/audio/music/silent-descent.mp3", 0.0, 0.62),
          "confident": ("../../reels/audio/music/unforgiven.mp3", 13.63, 1.0),
          "warm": ("../../reels/audio/music/fifth-of-february.mp3", 1.6, 1.15)}

CH2 = [
    ("Chapter two. Impact.", HF("ch2"), {"chapter": True, "music": "punchy"}),
    ("The asteroid reaches the top of the atmosphere,", I("atmo-entry", (.45, .45), 1.0, tz=1.3), {"sfx": [{"name": "trailer", "at": 0.3}]}),
    ("a hundred kilometres up.", V("earth-spin", 2.0, 1.05, drift=0.2), {"overlays": [RM("alt100", 0.0)]}),
    ("At twenty kilometres every second,", V("meteor-earth", 4.0, 1.15, drift=0.12), {}),
    ("it punches through all of that air in about five seconds.", I("plasma-trail", (.5, .35), 1.0, to=(.5, .55), tz=1.25),
     {"overlays": [RM("sec5", "@five-0.2")], "sfx": [{"name": "tick", "at": "@five"}], "shake": ["@punches"]}),
    ("The air in front of it can't get out of the way.", I("shock-front", (.5, .5), 1.0, tz=1.4), {"sfx": [{"name": "zap", "at": 0.2, "gain": 0.5}]}),
    ("It gets squeezed so hard", I("shock-front", (.5, .5), 1.6, tz=2.0), {"shake": ["@squeezed"]}),
    ("that it glows hotter than the surface of the Sun.",
     {"mg": "versus", "left": ["SUN'S SURFACE", "5,500 °C"], "right": ["THE AIR IN FRONT", "HOTTER"], "at": "@hotter"},
     {"sfx": [{"name": "pop", "at": 0.05}, {"name": "bass", "at": "@hotter"}]}),
    ("For anyone looking up,", I("sky-split", (.5, .6), 1.0, tz=1.15), {}),
    ("the sky splits open with a blinding white light.", I("sky-split", (.62, .3), 1.5, tz=1.9),
     {"in": "flash", "sfx": [{"name": "glass", "at": "@splits"}, {"name": "reveal", "at": "@blinding"}]}),
    ("Let's say it comes down exactly where the dinosaur killer did,", I("earth-target", (.5, .5), 1.0, tz=1.3),
     {"overlays": [RM("chicx", "@exactly")], "sfx": [{"name": "zap", "at": 0.1, "gain": 0.4}]}),
    ("in a shallow sea off the coast of Mexico.", V("turquoise", 1.0, 1.1, drift=0.1), {}),
    ("This rock is so big that when its front edge touches the seabed,", HF("jet"), {"sfx": [{"name": "impact", "at": 0.75, "gain": 0.6}]}),
    ("its back end is still about as high as a passenger jet flies.", V("plane-clouds", 2.0, 1.1), {"sfx": [{"name": "whoosh2", "at": "@passenger"}]}),
    ("To an object this size, the ocean is barely a puddle.", I("asteroid-sea", (.5, .5), 1.0, to=(.47, .72), tz=1.6), {}),
    ("In less than a second,", V("hourglass", 1.0, 1.15), {"sfx": [{"name": "tick", "at": 0.2}, {"name": "tick", "at": 0.6}]}),
    ("it releases about a hundred million megatons of energy.", V("flames", 2.0, 1.1, drift=0.1),
     {"overlays": [RM("megatons", "@hundred-0.2")], "sfx": [{"name": "boom", "at": "@megatons", "gain": 0.7}], "shake": ["@megatons"]}),
    ("That's billions of times the bomb that destroyed Hiroshima,", I("nuke-cloud", (.5, .5), 1.0, tz=1.3), {"sfx": [{"name": "boom", "at": "@bomb", "gain": 0.5}]}),
    ("and more than ten thousand times", K("MORE THAN", ("10,000 ×", "yellow"), times=[0.0, "@ten"], size=170),
     {"sfx": [{"name": "pop", "at": 0.05}, {"name": "bass", "at": "@ten"}]}),
    ("every nuclear weapon on Earth put together.", I("nuke-cloud", (.5, .4), 1.3, tz=1.7),
     {"overlays": [KO("EVERY NUCLEAR", ("WEAPON ON EARTH", "yellow"), times=[0.0, "@weapon"], size=120)], "captions": False, "sfx": [{"name": "impact", "at": "@weapon", "gain": 0.6}]}),
    ("The asteroid doesn't just make a hole.", I("impact-flash", (.5, .5), 1.0, tz=1.25), {"in": "flash", "sfx": [{"name": "boom", "at": 0.0}], "shake": [0.0]}),
    ("It vaporises.", V("fire", 3.0, 1.2), {"in": "glitch", "shake": [0.05]}),
    ("So does the rock underneath it.", I("crater-rebound", (.5, .55), 1.3, tz=1.0), {"sfx": [{"name": "impact", "at": "@rock", "gain": 0.7}]}),
    ("For a moment, the hole is around thirty kilometres deep,", HF("crater"), {}),
    ("more than three times the height of Mount Everest.", I("everest", (.5, .45), 1.0, to=(.5, .3), tz=1.4), {"sfx": [{"name": "whoosh"}]}),
    ("Then the walls collapse,", I("crater-rebound", (.5, .5), 1.0, tz=1.3), {"shake": ["@collapse"], "sfx": [{"name": "impact", "at": "@collapse", "gain": 0.6}]}),
    ("and the floor rebounds upward,", I("crater-rebound", (.5, .45), 1.4, to=(.5, .35), tz=1.9), {}),
    ("like a drop of water splashing back out of a pond.", V("water-drop", 0.5, 1.1, rate=0.6), {"sfx": [{"name": "pop", "at": "@splashing"}]}),
    ("Within minutes, the crater settles into a scar", I("crater-orbit", (.5, .5), 1.4, tz=1.0), {}),
    ("about a hundred and eighty kilometres wide.", I("crater-orbit", (.5, .5), 1.0, tz=1.1), {"overlays": [RM("km180", "@hundred-0.2")], "sfx": [{"name": "sweep", "at": "@hundred"}]}),
    ("A column of molten rock and vapour blasts upward,", I("plume-space", (.5, .7), 1.2, to=(.5, .35), tz=1.3), {"sfx": [{"name": "boom", "at": "@blasts", "gain": 0.7}]}),
    ("right out of the atmosphere.", I("plume-space", (.5, .4), 1.0, tz=1.15), {}),
    ("Some of it reaches space.", V("earth-planet", 1.0, 1.1, drift=0.15), {"sfx": [{"name": "whoosh2"}]}),
    ("The ground shakes with an earthquake", V("cracked-road", 1.0, 1.15), {"shake": [0.1, "@earthquake"], "sfx": [{"name": "boom", "at": "@earthquake", "gain": 0.6}]}),
    ("far stronger than anything ever recorded.", I("quake", (.5, .55), 1.0, tz=1.3),
     {"overlays": [LT("STRONGEST EVER RECORDED", "MAGNITUDE 9.5 · CHILE 1960", at="@stronger")], "shake": ["@stronger"]}),
    ("A blast wave races outward", V("tree-car", 1.0, 1.15), {"sfx": [{"name": "tunnel", "at": 0.0}]}),
    ("with winds faster than any hurricane.", V("hurricane", 2.0, 1.1, drift=0.12), {}),
    ("Everything within hundreds of kilometres", V("burnt", 2.0, 1.15), {}),
    ("is flattened, burned, or buried.", I("flattened-forest", (.5, .5), 1.0, tz=1.3),
     {"overlays": [KO("FLATTENED.", ("BURNED.", "yellow"), ("BURIED.", "red"), times=["@flattened", "@burned", "@buried"], size=120)],
      "captions": False, "sfx": [{"name": "impact", "at": "@flattened", "gain": 0.5}, {"name": "impact", "at": "@burned", "gain": 0.5}, {"name": "impact", "at": "@buried", "gain": 0.6}]}),
    ("Further away, the ground jumps first.", V("city-aerial", 4.0, 1.1), {"shake": ["@jumps"], "sfx": [{"name": "bass", "at": "@jumps"}]}),
    ("The sound of the impact arrives much later,", V("lightning", 1.0, 1.15), {}),
    ("as a roar louder than any thunder.", V("storm-tree", 1.0, 1.2), {"sfx": [{"name": "boom", "at": "@roar"}], "shake": ["@roar"]}),
    ("That's the first few minutes.", I("crater-orbit", (.5, .5), 1.2, tz=1.0), {"overlays": [TAG("+ 00:05:00  AFTER IMPACT")]}),
    ("But the crater isn't the real danger.", I("crater-orbit", (.55, .45), 1.8, tz=2.2), {"in": "glitch", "music_fx": "muffle"}),
    ("What comes back down is.", I("debris-reentry", (.5, .45), 1.0, tz=1.3), {"in": "flash", "sfx": [{"name": "bass", "at": 0.0}], "voice_fx": {"at": "@down", "fx": "echo"}}),
]

CH3 = [
    ("Chapter three. The sky catches fire.", HF("ch3"), {"chapter": True, "music": "tense"}),
    ("Remember the debris that was blasted into space?", I("plume-space", (.5, .45), 1.3, tz=1.0), {"overlays": [TAG("◀◀ REPLAY  T + 00:01:00")], "fx": ["vhs"], "sfx": [{"name": "rewind"}]}),
    ("Gravity pulls it back.", I("debris-reentry", (.5, .3), 1.0, to=(.5, .6), tz=1.3), {"sfx": [{"name": "whoosh2"}]}),
    ("Billions of tonnes of it.", I("debris-reentry", (.5, .55), 1.5, tz=1.9),
     {"overlays": [KO(("BILLIONS", "yellow"), "OF TONNES", times=["@Billions", "@tonnes"])], "captions": False, "sfx": [{"name": "bass", "at": "@Billions"}]}),
    ("Over the next few hours,", V("star-trails", 1.0, 1.1), {"overlays": [TAG("T + 1 HOUR")]}),
    ("it rains down all over the planet", V("meteor-storm", 4.0, 1.1, drift=0.12), {}),
    ("as tiny glassy beads and burning rock.", I("spherules", (.5, .5), 1.0, tz=1.5), {"sfx": [{"name": "sparkle", "at": "@glassy"}]}),
    ("Every grain is a little shooting star.", V("milky-way", 1.0, 1.15, drift=0.1), {"sfx": [{"name": "sparkle", "at": "@shooting"}]}),
    ("Even on the far side of the planet,", V("earth-night", 12.0, 1.1, drift=0.1), {}),
    ("people look up and see the sky fill with meteors,", I("meteor-crowd", (.5, .65), 1.0, to=(.5, .3), tz=1.3), {"amb": {"name": "crowd-murmur", "gain": 0.1}}),
    ("as if every star is falling at once.", I("meteor-crowd", (.5, .25), 1.6, tz=2.0), {}),
    ("Trillions of them heat the upper atmosphere at the same time.", I("glowing-atmosphere", (.55, .5), 1.0, tz=1.35), {"sfx": [{"name": "riser", "at": "@same"}]}),
    ("Some scientists think the whole sky glowed", I("oven-sky", (.5, .3), 1.0, tz=1.25), {}),
    ("like the inside of an oven,", I("oven-sky", (.5, .4), 1.4, tz=1.8), {}),
    ("hot enough to set fire to forests on the ground below.", V("flames", 6.0, 1.1), {"sfx": [{"name": "whoosh", "at": "@fire"}]}),
    ("And we have evidence.", K("WE HAVE", ("EVIDENCE", "yellow"), times=[0.0, "@evidence"]), {"sfx": [{"name": "shutter", "at": "@evidence"}]}),
    ("Geologists have found soot and those same tiny glass beads", I("kpg-layer", (.45, .5), 1.0, to=(.65, .45), tz=1.4), {}),
    ("in a thin layer of rock all around the world,", I("kpg-closeup", (.5, .45), 1.0, tz=1.5), {"overlays": [LT("THE K–Pg BOUNDARY", "A WORLDWIDE LAYER, 66 MILLION YEARS OLD", at="@thin")]}),
    ("laid down at the exact moment the dinosaurs disappeared.", V("fossil", 1.0, 1.1), {}),
    ("Meanwhile, the ocean strikes back.", V("swell", 1.0, 1.15), {"in": "glitch", "sfx": [{"name": "boom", "at": "@strikes", "gain": 0.6}]}),
    ("The impact shoves trillions of tonnes of water aside,", I("water-pushed", (.5, .5), 1.0, tz=1.35), {"sfx": [{"name": "tunnel"}]}),
    ("and it comes rushing back in as a tsunami.", I("mega-wave", (.5, .5), 1.0, to=(.5, .35), tz=1.3), {"shake": ["@tsunami"], "sfx": [{"name": "impact", "at": "@tsunami"}]}),
    ("In twenty twenty two, scientists simulated the dinosaur impact", I("sim-screen", (.6, .45), 1.0, tz=1.3), {"overlays": [LT("RANGE ET AL. · 2022", "AGU ADVANCES · CHICXULUB TSUNAMI MODEL", at=0.2)]}),
    ("and found the first wave may have been around one and a half kilometres tall.", HF("wave"), {"sfx": [{"name": "whoosh", "at": 0.5}, {"name": "impact", "at": 1.5, "gain": 0.6}]}),
    ("In the open ocean, a tsunami can travel as fast as a jet airliner.", V("plane-landing", 1.0, 1.1), {"overlays": [RM("kmh800", "@fast-0.2")]}),
    ("Within two days, the waves had spread across most of the world's oceans,", I("tsunami-rings", (.5, .5), 1.0, tz=1.3), {"overlays": [TAG("T + 48 HOURS")]}),
    ("some still many metres high", V("lighthouse", 1.0, 1.1), {}),
    ("when they reached coastlines on the other side of the planet.", V("big-wave", 1.0, 1.1), {"sfx": [{"name": "whoosh2"}]}),
    ("Now imagine that today.", K("NOW IMAGINE", ("THAT TODAY", "red"), times=[0.0, "@today"]), {"in": "glitch"}),
    ("Coastal cities around the Gulf of Mexico disappear under water within hours.", I("city-tsunami", (.5, .5), 1.0, to=(.4, .45), tz=1.35), {"shake": ["@disappear"], "sfx": [{"name": "boom", "at": "@disappear", "gain": 0.6}]}),
    ("Planes are grounded.", V("plane-gate", 1.0, 1.15), {}),
    ("Power grids fail.", I("blackout", (.5, .5), 1.0, tz=1.2), {"fx": [{"name": "light_off", "at": "@fail"}], "sfx": [{"name": "switch", "at": "@fail"}]}),
    ("Satellites are hit by falling debris.", I("sat-hit", (.55, .45), 1.0, tz=1.35), {"sfx": [{"name": "glass", "at": "@hit"}], "shake": ["@hit"]}),
    ("For most of the world, the news arrives in fragments,", V("tv-static", 1.0, 1.1), {"fx": ["vhs"], "sfx": [{"name": "glitch", "at": 0.1}]}),
    ("if it arrives at all.", V("tv-static", 3.0, 1.3), {"in": "glitch", "fx": ["vhs"]}),
    ("And yet, the fire and the water are not what wiped out the dinosaurs.", I("dino-ash", (.5, .5), 1.0, tz=1.3), {}),
    ("The real killer is quieter.", I("veiled-earth", (.5, .5), 1.0, tz=1.2), {"music_fx": "muffle"}),
    ("It's the dark.", K(("IT'S THE DARK", "white"), size=170), {"in": "dip", "voice_fx": {"at": "@dark", "fx": "echo"}, "sfx": [{"name": "boom", "at": "@dark", "gain": 0.7}]}),
]

CH4 = [
    ("Chapter four. The long night.", HF("ch4"), {"chapter": True, "music": "sad"}),
    ("The impact threw something else into the sky.", I("ash-planet", (.5, .5), 1.0, tz=1.3), {}),
    ("Dust, soot from the fires,", V("burnt", 1.0, 1.15), {}),
    ("and hundreds of billions of tonnes of sulfur", K("HUNDREDS OF BILLIONS", "OF TONNES", ("OF SULFUR", "yellow"), times=[0.0, "@tonnes", "@sulfur"], size=120),
     {"sfx": [{"name": "pop", "at": 0.05}, {"name": "pop", "at": "@tonnes"}, {"name": "bass", "at": "@sulfur"}]}),
    ("from the rocks it vaporised.", I("crater-orbit", (.5, .5), 1.0, tz=1.3), {}),
    ("High in the atmosphere, that sulfur turns into tiny droplets", I("haze-orbit", (.5, .5), 1.0, tz=1.3), {}),
    ("that reflect sunlight back into space.", V("sun-darkclouds", 1.0, 1.1), {}),
    ("Within weeks, a veil wraps around the entire planet.", I("veiled-earth", (.5, .55), 1.3, tz=1.0), {"overlays": [TAG("T + 3 WEEKS")], "sfx": [{"name": "sweep", "at": "@veil"}]}),
    ("Midday starts to look like dusk.", I("dim-sun", (.5, .45), 1.0, tz=1.2), {}),
    ("In some places, like night.", I("dim-sun", (.55, .35), 1.4, tz=1.7), {"fx": [{"name": "light_off", "at": "@night"}]}),
    ("Imagine stepping outside at noon and needing a torch to see.", I("torch-street", (.5, .5), 1.0, to=(.5, .55), tz=1.4), {"sfx": [{"name": "click", "at": "@torch"}]}),
    ("The air smells of smoke.", V("smoke-dark", 4.0, 1.2), {}),
    ("Snow starts falling in places that have never seen it,", I("ash-snow", (.5, .5), 1.0, tz=1.25), {}),
    ("and it's grey with ash.", I("ash-snow", (.6, .4), 1.5, tz=1.9), {}),
    ("Without sunlight, plants can't make food.", I("dead-plants", (.5, .5), 1.0, tz=1.3), {}),
    ("Studies suggest photosynthesis almost stopped for a year or more.", V("fern-close", 1.0, 1.15, grade=True),
     {"overlays": [LT("PHOTOSYNTHESIS: NEARLY ZERO", "FOR A YEAR OR MORE · BARDEEN ET AL. 2017", at="@photosynthesis")], }),
    ("Then the cold arrives.", V("frost", 1.0, 1.15), {"in": "glitch", "sfx": [{"name": "glass", "at": "@cold"}]}),
    ("Some climate models suggest the planet's average temperature dropped by more than twenty degrees Celsius,", HF("temp"),
     {"sfx": [{"name": "sweep", "at": 0.4}, {"name": "bass", "at": "@twenty"}]}),
    ("and stayed below freezing for years.", V("ice-lake", 1.0, 1.1), {}),
    ("Tropical forests freeze.", I("frozen-jungle", (.5, .5), 1.0, tz=1.3), {"sfx": [{"name": "glass", "at": "@freeze", "gain": 0.6}]}),
    ("Rain turns acidic.", V("rain-window", 1.0, 1.15), {}),
    ("In the oceans, the plankton die first,", V("deep-rays", 1.0, 1.1), {}),
    ("then the fish that eat them,", V("fish-school", 1.0, 1.1), {}),
    ("then everything that eats the fish.", V("shark", 1.0, 1.1), {}),
    ("The whole food chain collapses from the bottom up.", HF("pyramid"), {"sfx": [{"name": "wrong", "at": 1.2, "gain": 0.4}, {"name": "impact", "at": 1.9, "gain": 0.6}]}),
    ("Now think about us.", K("NOW THINK", ("ABOUT US", "yellow"), times=[0.0, "@about"]), {"in": "glitch"}),
    ("Our farms need sunlight just like the forests do.", V("wheat", 1.0, 1.1), {}),
    ("One cold, dark year means no harvest almost anywhere on Earth.", I("dead-crops", (.5, .5), 1.0, tz=1.3),
     {"overlays": [RM("noharvest", "@harvest-0.1")], "sfx": [{"name": "impact", "at": "@harvest", "gain": 0.7}]}),
    ("And most countries only keep a few months of food in storage.", V("shelves", 1.0, 1.15), {"overlays": [KO(("A FEW MONTHS", "yellow"), "OF FOOD", times=["@few", "@food"], size=120)], "captions": False}),
    ("So the people who make it through the first day", I("survivors-fire", (.5, .5), 1.0, tz=1.3), {}),
    ("face a much harder question.", I("survivors-fire", (.5, .45), 1.5, tz=1.8), {}),
    ("What do eight billion people eat when the Sun disappears?", {"mg": "grid", "label": "8,000,000,000 PEOPLE", "lit": [0, 20, 0.0, "@billion"], "question": False},
     {"sfx": [{"name": "pop", "at": "@eight"}, {"name": "bass", "at": "@disappears"}]}),
    ("Researchers who study global catastrophes have looked at this exact problem.", V("lab", 1.0, 1.1), {}),
    ("Their answers sound strange, but they work.", I("mission-control", (.5, .5), 1.0, tz=1.2), {}),
    ("Mushrooms grown on dead wood.", V("mushrooms", 1.0, 1.15), {}),
    ("Greenhouses heated by power plants.", V("greenhouses", 1.0, 1.1), {}),
    ("Even sugar made from leaves and sawdust.", V("sawdust", 1.0, 1.15), {}),
    ("Survival would depend on how fast we could switch the whole world", V("earth-spin", 8.0, 1.05, drift=0.15), {}),
    ("to food that doesn't need the Sun.", V("mushrooms", 5.0, 1.3), {}),
    ("But if you could fast forward a few years,", I("sun-return", (.5, .5), 1.0, tz=1.2), {"in": "glitch", "overlays": [TAG("▶▶ FAST FORWARD  + 5 YEARS")], "fx": ["vhs"], "sfx": [{"name": "rewind"}]}),
    ("you'd see something unexpected.", I("mammal-dawn", (.5, .6), 1.0, tz=1.3), {"sfx": [{"name": "sparkle", "at": "@unexpected"}]}),
    ("Life doesn't end.", I("mammal-dawn", (.45, .6), 1.5, tz=1.9), {}),
    ("It changes hands.", K("IT CHANGES", ("HANDS", "yellow"), times=[0.0, "@hands"]), {"sfx": [{"name": "bass", "at": "@hands"}]}),
]

CH5 = [
    ("Chapter five. The world it leaves behind.", HF("ch5"), {"chapter": True, "music": "intrigue"}),
    ("Slowly, the sky clears.", V("sun-darkclouds", 5.0, 1.1), {}),
    ("The sulfur rains out within a few years.", V("rain-puddle", 1.0, 1.15), {}),
    ("The dust settles. Sunlight returns.", I("sun-return", (.5, .4), 1.0, tz=1.3), {"sfx": [{"name": "reveal", "at": "@Sunlight"}]}),
    ("But the climate swings the other way.", V("dune", 1.0, 1.1), {"in": "glitch"}),
    ("All the carbon dioxide released by the impact and the fires traps heat.", V("smokestacks", 1.0, 1.1), {}),
    ("One study found that after the cold, temperatures rose by about five degrees,", I("hot-earth", (.5, .5), 1.0, tz=1.3),
     {"overlays": [LT("MACLEOD ET AL. · 2018", "SCIENCE · FISH-TOOTH OXYGEN RECORD", at=0.2), KO(("+5 °C", "yellow"), times=["@five"], size=170)]}),
    ("and stayed high for around a hundred thousand years.", V("sun-orange", 1.0, 1.1), {"overlays": [KO(("100,000 YEARS", "yellow"), times=["@hundred"], size=140)], "captions": False}),
    ("Sixty six million years ago,", I("dino-herd", (.5, .5), 1.0, tz=1.25), {"overlays": [KO(("66,000,000", "yellow"), "YEARS AGO", times=[0.0, "@years"], size=140)], "captions": False, "sfx": [{"name": "rewind", "at": 0.0, "gain": 0.6}]}),
    ("when this really happened,", I("dino-fireball", (.5, .45), 1.1, tz=1.4), {}),
    ("about three quarters of all species on Earth disappeared.", {"mg": "grid", "label": "SPECIES THAT DISAPPEARED", "lit": [0, 15, "@three", "@species"], "pct": [0, 75, "@three", "@species"]},
     {"sfx": [{"name": "pop", "at": "@three"}, {"name": "bass", "at": "@disappeared"}]}),
    ("Not just the dinosaurs.", I("trex", (.5, .5), 1.0, tz=1.3), {"sfx": [{"name": "impact", "at": 0.1, "gain": 0.5}]}),
    ("The giant sea reptiles.", I("mosasaur", (.5, .5), 1.0, tz=1.3), {}),
    ("The flying pterosaurs.", I("pterosaur", (.5, .5), 1.0, tz=1.25), {}),
    ("The ammonites,", I("ammonite", (.55, .5), 1.0, tz=1.3), {}),
    ("whose shells had filled the oceans for hundreds of millions of years.", V("fossil", 3.0, 1.15), {}),
    ("So who survived?", K("WHO", ("SURVIVED?", "yellow"), times=[0.0, "@survived"]), {"in": "glitch"}),
    ("The small ones.", I("mammal-burrow", (.45, .45), 1.0, tz=1.4), {}),
    ("Animals that could burrow, hide,", V("beetles", 1.0, 1.15), {}),
    ("eat seeds, or live on dead things.", I("mammal-dawn", (.5, .6), 1.1, tz=1.4), {}),
    ("Turtles.", V("turtle", 1.0, 1.1), {"in": "cut", "sfx": [{"name": "pop"}]}),
    ("Crocodiles.", V("croc", 1.0, 1.1), {"in": "cut", "sfx": [{"name": "pop"}]}),
    ("Frogs.", V("frog", 1.0, 1.15), {"in": "cut", "sfx": [{"name": "pop"}]}),
    ("Birds, the only dinosaurs that made it.", V("gulls", 1.0, 1.1), {"overlays": [LT("BIRDS = LIVING DINOSAURS", "THE ONLY BRANCH THAT SURVIVED", at="@only")]}),
    ("And small, furry mammals,", I("mammal-burrow", (.45, .45), 1.4, tz=1.8), {}),
    ("most of them tiny enough to hide in a hole in the ground.", I("mammal-burrow", (.4, .5), 1.0, tz=1.2), {}),
    ("With the giants gone, those mammals got their chance.", I("fern-land", (.5, .5), 1.0, tz=1.3), {"music": "warm"}),
    ("Over the next ten million years", V("forest-top", 1.0, 1.1), {"overlays": [TAG("▶▶ + 10,000,000 YEARS")]}),
    ("they spread into every empty corner of the planet,", V("jungle-falls", 1.0, 1.1), {}),
    ("and grew into whales,", I("whale", (.5, .5), 1.0, tz=1.25), {}),
    ("horses,", V("horses", 1.0, 1.1), {"in": "cut"}),
    ("elephants,", V("elephants", 1.0, 1.1), {"in": "cut"}),
    ("and eventually, primates.", V("monkey", 1.0, 1.15), {}),
    ("The plants came back too.", V("fern-close", 3.0, 1.1), {}),
    ("In rock layers just above the impact,", I("kpg-closeup", (.5, .4), 1.2, tz=1.6), {}),
    ("fossil pollen suddenly gives way to fern spores.", I("spores", (.5, .5), 1.0, tz=1.4), {"overlays": [LT("THE FERN SPIKE", "FERN SPORES ABOVE THE IMPACT LAYER", at="@fern")]}),
    ("Ferns were the first plants to cover the burned land.", I("fern-land", (.5, .55), 1.3, tz=1.0), {}),
    ("In a strange way, we're only here", V("crowd-bridge", 12.0, 1.1), {"amb": {"name": "crowd-murmur", "gain": 0.1}}),
    ("because an asteroid cleared the stage.", I("dino-fireball", (.6, .35), 1.4, tz=1.8), {"sfx": [{"name": "whoosh"}]}),
    ("But this time, the giants are us.", V("city-aerial", 10.0, 1.1), {"in": "glitch", "overlays": [KO("THE GIANTS", ("ARE US", "yellow"), times=["@giants", "@us"], size=150)], "captions": False,
                                                                        "sfx": [{"name": "bass", "at": "@us"}]}),
    ("We're big, we need a lot of food,", V("traffic-lights", 2.0, 1.1), {}),
    ("and our whole civilisation depends on a stable climate.", V("earth-night", 18.0, 1.1), {}),
    ("A world after impact would have no global trade,", V("port", 1.0, 1.1), {"overlays": [KO(("NO TRADE", "red"), times=["@trade"], size=150)], "captions": False, "sfx": [{"name": "wrong", "at": "@trade", "gain": 0.4}]}),
    ("no internet,", V("servers", 1.0, 1.15), {"in": "cut", "overlays": [KO(("NO INTERNET", "red"), size=150)], "captions": False, "fx": [{"name": "light_off", "at": 0.3}], "sfx": [{"name": "wrong", "at": 0.05, "gain": 0.4}]}),
    ("and no supermarkets.", V("shelves", 4.0, 1.15), {"in": "cut", "overlays": [KO(("NO SUPERMARKETS", "red"), times=["@supermarkets"], size=140)], "captions": False, "sfx": [{"name": "wrong", "at": "@supermarkets", "gain": 0.4}]}),
    ("What it would have is what we've saved.", V("seeds", 1.0, 1.15), {}),
    ("Libraries.", V("library", 1.0, 1.15), {"in": "cut"}),
    ("Survivors with skills.", V("carpenter", 1.0, 1.15), {"in": "cut"}),
    ("And places like the Global Seed Vault in Norway,", I("seed-vault", (.55, .5), 1.0, tz=1.3), {"overlays": [RM("vault", "@Global")]}),
    ("buried inside a frozen mountain,", I("seed-vault", (.5, .35), 1.3, to=(.45, .2), tz=1.6), {}),
    ("holding more than a million samples of the world's crops.", V("seeds", 4.0, 1.2), {"overlays": [KO(("1,000,000+", "yellow"), "SEED SAMPLES", times=["@million", "@samples"], size=140)], "captions": False}),
    ("The world it leaves behind", I("wasteland", (.5, .55), 1.0, tz=1.25), {}),
    ("is colder, darker and emptier,", V("ice-lake", 3.0, 1.15), {}),
    ("and then, over thousands of years, green again.", V("forest-autumn", 1.0, 1.1), {"sfx": [{"name": "sparkle", "at": "@green"}]}),
    ("Which brings us back to the question from the very beginning.", I("asteroid-earth", (.5, .5), 1.2, tz=1.0), {"fx": ["vhs"], "overlays": [TAG("◀◀ REWIND  00:00:01")], "sfx": [{"name": "rewind"}]}),
    ("If this could happen,", I("impact-flash", (.5, .5), 1.2, tz=1.5), {}),
    ("why are space agencies so calm?", I("mission-control", (.5, .45), 1.0, tz=1.35), {"music": "confident", "sfx": [{"name": "tick", "at": "@calm"}]}),
]

CH6 = [
    ("Chapter six. How we stop it.", HF("ch6"), {"chapter": True}),
    ("First, the good news.", K("THE GOOD", ("NEWS", "yellow"), times=[0.0, "@news"]), {"sfx": [{"name": "correct", "at": "@news", "gain": 0.5}]}),
    ("Asteroids this big are incredibly rare.", I("asteroid-belt", (.5, .5), 1.0, tz=1.3), {}),
    ("A rock ten kilometres wide hits Earth", I("asteroid-earth", (.4, .5), 1.0, to=(.6, .5), tz=1.3), {}),
    ("roughly once every hundred million years.", V("milky-way", 3.0, 1.1, drift=0.1), {"overlays": [RM("myr100", 0.0)]}),
    ("They're also the easiest to find.", V("telescope-man", 2.0, 1.1), {}),
    ("NASA says it has already found more than ninety percent", I("mission-control", (.6, .4), 1.1, tz=1.4), {}),
    ("of the near Earth asteroids bigger than one kilometre,",
     {"mg": "bars", "headline": "NEAR-EARTH ASTEROIDS OVER 1 KM", "bars": [["FOUND", 90, "yellow"], ["STILL HIDDEN", 10, "grey"]]},
     {"sfx": [{"name": "sweep", "at": 0.2}, {"name": "pop", "at": 0.9}]}),
    ("and none of them are on course to hit us for at least the next century.", V("earth-spin", 12.0, 1.05, drift=0.15),
     {"overlays": [RM("nothreat", "@none")], "sfx": [{"name": "impact", "at": "@none", "gain": 0.6}]}),
    ("The real danger is the smaller ones.", I("small-asteroid", (.45, .55), 1.0, tz=1.35), {"in": "glitch"}),
    ("A rock a few hundred metres wide wouldn't end the world,", I("small-asteroid", (.4, .6), 1.5, tz=1.8), {}),
    ("but it could wipe out a city, or an entire region.", I("city-impact", (.5, .5), 1.0, tz=1.3), {"overlays": [RM("city", "@city-0.2")], "sfx": [{"name": "zap", "at": "@city", "gain": 0.5}]}),
    ("And fewer than half of those have been found.", K("FEWER THAN", ("HALF FOUND", "red"), times=[0.0, "@half"]), {"sfx": [{"name": "bass", "at": "@half"}]}),
    ("That's why the real weapon isn't a missile.", V("rocket", 6.0, 1.1), {}),
    ("It's time.", V("hourglass", 3.0, 1.25), {"overlays": [KO(("IT'S TIME", "yellow"), size=170)], "captions": False, "sfx": [{"name": "tick", "at": 0.1}, {"name": "bass", "at": "@time"}]}),
    ("If we spot an asteroid years or decades ahead,", V("observatory", 3.0, 1.1), {}),
    ("we don't need to blow it up.", I("nuke-asteroid", (.4, .5), 1.0, tz=1.3), {"sfx": [{"name": "wrong", "at": "@blow", "gain": 0.4}]}),
    ("We just need to nudge it.", I("miss", (.4, .5), 1.0, tz=1.25), {"sfx": [{"name": "pop", "at": "@nudge"}]}),
    ("A push of just one centimetre per second, given ten years early,", HF("nudge"), {"sfx": [{"name": "swoosh", "at": 0.6}]}),
    ("adds up to thousands of kilometres by the time it reaches us.", dict(HF("nudge"), start=2.4), {"in": "cut", "sfx": [{"name": "impact", "at": "@thousands", "gain": 0.5}]}),
    ("Enough to make it miss.", I("miss", (.5, .5), 1.2, tz=1.0), {"sfx": [{"name": "whoosh2"}]}),
    ("There are a few ways to give that push.", K("3 WAYS", ("TO PUSH IT", "yellow"), times=[0.0, "@push"]), {}),
    ("Crash a spacecraft into it.", I("dart-impact", (.5, .5), 1.0, tz=1.4), {"overlays": [TAG("01  KINETIC IMPACTOR")], "sfx": [{"name": "impact", "at": "@Crash", "gain": 0.6}]}),
    ("Park a heavy spacecraft beside it", I("gravity-tractor", (.55, .45), 1.0, tz=1.25), {"overlays": [TAG("02  GRAVITY TRACTOR")]}),
    ("and let gravity tug it off course, very slowly.", I("gravity-tractor", (.45, .5), 1.3, tz=1.5, drift=0.02), {}),
    ("Or, for a big one with little time, set off a nuclear device nearby,", I("nuke-asteroid", (.5, .5), 1.0, tz=1.3), {"overlays": [TAG("03  NUCLEAR DEFLECTION")], "sfx": [{"name": "boom", "at": "@nuclear", "gain": 0.6}]}),
    ("to blast vapour off one side and shove it away.", I("nuke-asteroid", (.62, .5), 1.4, tz=1.8), {"shake": ["@blast"]}),
    ("In twenty twenty two, NASA tested exactly that.", {"mg": "year", "from": 2026, "to": 2022, "roll": 0.8, "label": "NASA · DART MISSION"}, {"in": "dip"}),
    ("A spacecraft called DART flew eleven million kilometres", I("dart", (.4, .5), 1.0, to=(.55, .45), tz=1.3), {"overlays": [RM("dart", "@DART")]}),
    ("and slammed into a small asteroid moon called Dimorphos", I("dart-impact", (.5, .5), 1.0, tz=1.4), {"sfx": [{"name": "impact", "at": "@slammed"}], "shake": ["@slammed"]}),
    ("at about six kilometres per second.", I("dimorphos-ejecta", (.4, .5), 1.0, tz=1.3), {"overlays": [RM("kms6", 0.0)]}),
    ("It worked.", K(("IT WORKED.", "yellow"), size=170), {"sfx": [{"name": "correct", "at": 0.1, "gain": 0.6}]}),
    ("The impact changed the moon's orbit by thirty two minutes.", HF("dart"), {"sfx": [{"name": "impact", "at": 1.2, "gain": 0.6}, {"name": "pop", "at": 1.9}]}),
    ("For the first time ever,", K("FIRST TIME", ("EVER", "yellow"), times=[0.0, "@ever"]), {"sfx": [{"name": "sparkle", "at": "@ever"}]}),
    ("humans changed the path of a natural object in space.", I("dimorphos-ejecta", (.5, .5), 1.3, tz=1.0), {}),
    ("And Europe's Hera spacecraft is on its way there right now,", I("hera", (.45, .5), 1.0, tz=1.3), {"overlays": [RM("hera", "@Hera")]}),
    ("to study the crash site up close.", I("hera", (.6, .5), 1.4, tz=1.8), {}),
    ("Meanwhile, the hunt is getting faster.", V("milky-way", 6.0, 1.15), {}),
    ("The new Vera Rubin Observatory in Chile", I("rubin", (.5, .55), 1.0, tz=1.25), {"overlays": [RM("rubin", "@Vera")]}),
    ("is scanning the whole southern sky every few nights.", V("stars", 2.0, 1.1, drift=0.1), {"overlays": [{"mg": "scan", "box": [0.2, 0.15, 0.8, 0.7], "label": "SCANNING SOUTHERN SKY...", "at": 0.1}],
                                                                                          "sfx": [{"name": "typing", "at": 0.3, "gain": 0.5}]}),
    ("And NASA is building a space telescope called NEO Surveyor,", I("neo-surveyor", (.5, .5), 1.0, tz=1.3), {"overlays": [RM("neos", "@NEO")]}),
    ("made for one job:", I("neo-surveyor", (.5, .45), 1.5, tz=1.8), {}),
    ("finding dangerous asteroids before they find us.", I("small-asteroid", (.45, .5), 1.0, tz=1.3), {"overlays": [{"mg": "scan", "box": [0.3, 0.3, 0.62, 0.8], "label": "TARGET ACQUIRED", "at": 0.1}],
                                                                                                     "sfx": [{"name": "zap", "at": 0.1, "gain": 0.5}]}),
    ("The system is already being tested for real.", I("mission-control", (.5, .5), 1.2, tz=1.0), {}),
    ("In early twenty twenty five,", {"mg": "year", "from": 2026, "to": 2025, "roll": 0.5, "label": "EARLY 2025"}, {"in": "dip"}),
    ("a newly found asteroid called twenty twenty four Y R four", I("small-asteroid", (.5, .5), 1.0, tz=1.3), {"overlays": [RM("yr4", "@asteroid")]}),
    ("briefly had about a three percent chance", V("earth-spin", 15.0, 1.05, drift=0.1),
     {"overlays": [RM("pct3", "@three-0.2")], "sfx": [{"name": "heartbeat", "at": 0.1}, {"name": "heartbeat", "at": 0.5}]}),
    ("of hitting Earth in twenty thirty two.", I("earth-target", (.5, .5), 1.1, tz=1.5), {"sfx": [{"name": "zap", "at": 0.1, "gain": 0.4}]}),
    ("Telescopes around the world tracked it,", V("telescope-man", 10.0, 1.1), {}),
    ("and within weeks, the threat was ruled out.", I("miss", (.5, .5), 1.0, tz=1.2), {"overlays": [RM("ruledout", "@ruled-0.1")], "sfx": [{"name": "impact", "at": "@ruled", "gain": 0.6}]}),
    ("And on the thirteenth of April, twenty twenty nine,", {"mg": "year", "from": 2026, "to": 2029, "roll": 0.8, "label": "13 APRIL"}, {"in": "dip"}),
    ("an asteroid called Apophis, longer than three football fields,", I("apophis", (.4, .5), 1.0, tz=1.3), {"overlays": [RM("apophis", "@Apophis")]}),
    ("will pass closer to Earth than many of our satellites.", V("iss", 1.0, 1.1), {}),
    ("An impact has already been ruled out,", I("apophis", (.55, .45), 1.4, tz=1.7), {}),
    ("so instead of a threat, it's a free science lesson,", V("lab", 4.0, 1.15), {}),
    ("and NASA is sending a spacecraft to meet it.", I("hera", (.5, .5), 1.0, tz=1.3), {"overlays": [RM("osiris", "@NASA")]}),
    ("And every couple of years, space agencies and emergency planners sit down together", V("meeting", 1.0, 1.1), {"overlays": [RM("drill", 0.4)]}),
    ("and run drills for a fake asteroid, step by step,", V("control-room", 10.0, 1.15), {}),
    ("from the first warning to the evacuation.", I("mountain-road", (.5, .5), 1.0, tz=1.3), {}),
    ("So, what if a giant asteroid was about to hit Earth?", I("asteroid-earth", (.3, .5), 1.0, to=(.6, .5), tz=1.35), {"in": "dip", "pause_before": 0.3, "captions": False, "overlays": [RM("title", 0.3)]}),
    ("With only one day of warning,", I("astronomer", (.6, .4), 1.1, tz=1.5), {"overlays": [RM("t24", 0.0, alpha=0.95)], "sfx": [{"name": "heartbeat", "at": 0.2}]}),
    ("there would be nothing we could do.", V("rocket", 3.0, 1.1), {"overlays": [RM("notime", "@nothing")], "sfx": [{"name": "impact", "at": "@nothing", "gain": 0.7}]}),
    ("But that's exactly why people are watching the sky every single night.", I("night-watch", (.5, .5), 1.0, tz=1.3), {"music": "warm"}),
    ("So that if that day ever comes,", V("observatory", 4.0, 1.1), {}),
    ("we'll see it decades early,", I("rubin", (.5, .4), 1.0, tz=1.25), {}),
    ("and give it a gentle push.", I("dart", (.45, .5), 1.0, tz=1.3), {"sfx": [{"name": "sparkle", "at": "@push"}]}),
    ("The dinosaurs never saw it coming.", I("dino-fireball", (.45, .6), 1.0, to=(.6, .35), tz=1.3), {"sfx": [{"name": "boom", "at": "@coming", "gain": 0.5}]}),
    ("We will.", I("night-watch", (.5, .45), 1.3, tz=1.0), {"captions": False, "overlays": [RM("wewill", 0.0, hold=True)], "sfx": [{"name": "bass", "at": "@will"}],
                                                          "voice_fx": {"at": "@will", "fx": "echo"}}),
]

CHAPTERS = [CH2, CH3, CH4, CH5, CH6]
TRANS_SFX = {"whip": "swoosh", "zoom": "sweep", "flash": "whoosh", "glitch": "glitch", "dip": "tunnel"}


def kind(v):
    return "img" if "img" in v else "video" if "video" in v and not v["video"].startswith("motion/") else "mg"


def auto(shots):
    out, prev, n = [], None, 0
    for sh in shots:
        sh = dict(sh)
        k = kind(sh["v"])
        if sh.pop("chapter", False):
            sh.setdefault("in", "dip")
            sh.setdefault("pause_before", 0.35)
            sh["captions"] = False
            sh["sfx"] = [{"name": "reveal", "at": 0.0}, {"name": "impact", "at": 1.75, "gain": 0.8},
                         {"name": "bass", "at": 1.8, "gain": 0.7}] + sh.get("sfx", [])
        if "in" not in sh and prev:
            n += 1
            sh["in"] = ("flash" if prev != "mg" else "cut") if k == "mg" else \
                ["whip", "zoom", "whip", "flash"][n % 4] if prev == "mg" else \
                ["whip", "zoom", "whip", "glitch", "whip", "zoom"][n % 6]
        t = sh.get("in")
        if t in TRANS_SFX:
            sh["sfx"] = [{"name": TRANS_SFX[t], "gain": 0.7}] + sh.get("sfx", [])
        if k == "mg" and sh["v"].get("mg") in ("kinetic", "year", "versus", "bars", "grid"):
            sh.setdefault("captions", False)
        for ov in sh.get("overlays", []):
            if ov["mg"] == "lower_third":
                sh["sfx"] = sh.get("sfx", []) + [{"name": "swoosh-fast", "at": ov["at"], "gain": 0.5}]
            if ov["mg"] == "tag":
                sh["sfx"] = sh.get("sfx", []) + [{"name": "click", "at": ov["at"], "gain": 0.6}]
        out.append(sh)
        prev = k
    return out


def words(s):
    return [re.sub(r"[^a-z0-9']", "", w.lower()) for w in s.split()]


def main():
    intro = json.loads((HERE.parent / "asteroid-sample" / "video.json").read_text())
    shots = []
    for s in intro["shots"]:
        s = json.loads(json.dumps(s))
        if s["v"].get("video") == "motion/chapter.mp4":
            s["v"]["video"] = "motion/ch1.mp4"
        shots.append(s)
    assert words(" ".join(s["text"] for s in shots)) == words((HERE / "chapters" / "ch1.txt").read_text())
    cues = [{"shot": 0, "music": TRACKS["intrigue"][0], "start": TRACKS["intrigue"][1]},
            {"shot": 10, "music": TRACKS["tense"][0], "start": TRACKS["tense"][1]}]
    used = {"intrigue", "tense"}
    for n, ch in enumerate(CHAPTERS, 2):
        want = words((HERE / "chapters" / f"ch{n}.txt").read_text())
        got = [w for text, _, _ in ch for w in words(text)]
        if want != got:
            i = next(i for i, (a, b) in enumerate(zip(want + ["<end>"], got + ["<end>"])) if a != b)
            raise SystemExit(f"ch{n}: shot text differs from the script at word {i}: script {want[i:i + 6]} vs shots {got[i:i + 6]}")
        for sh in auto([{"text": text, "v": v, **ex} for text, v, ex in ch]):
            m = sh.pop("music", None)
            if m:
                cue = {"shot": len(shots), "music": TRACKS[m][0], "volume": TRACKS[m][2]}
                if m not in used:
                    cue["start"] = TRACKS[m][1]
                    used.add(m)
                cues.append(cue)
            shots.append(sh)
    takes = ["chapters/ch1.wav"] + [f"chapters/ch{n}{p}.wav" for n in range(2, 6) for p in "ab"] + [f"chapters/ch6{p}.wav" for p in "abc"]
    spec = {"out": "../output/asteroid-full.mp4", "audio": takes, "take_gap": 0.5, "speed": 1.0, "music_cues": cues,
            "music_volume": 0.38, "fade_out": 2.5, "progress": True, "shots": shots}
    (HERE / "video.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False))
    n_img = sum(1 for s in shots if kind(s["v"]) == "img")
    n_vid = sum(1 for s in shots if kind(s["v"]) == "video")
    n_ov = sum(1 for s in shots for o in s.get("overlays", []) if o["mg"] == "clip")
    print(f"{len(shots)} shots: {n_img} AI images, {n_vid} stock videos, {len(shots) - n_img - n_vid} motion-graphic shots, "
          f"{n_ov} Remotion overlays; {len(cues)} music cues")


if __name__ == "__main__":
    main()
