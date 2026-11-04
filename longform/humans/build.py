"""Build video.json for "What if all humans disappeared tomorrow?" (~11 min, time-lapse documentary, no people on screen).

Compact (text, visual, extras) lists per chapter. Transitions, transition SFX, chapter openers and music cues are
added by rule (auto()); extras override. Shot texts are checked word for word against chapters/chN.txt.
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


def HF(n, st=0.0):
    return {"video": f"motion/{n}.mp4", "start": st, "zoom": 1.0, "drift": 0.0, "grade": False}


def RM(n, at=0.0, **kw):
    return {"mg": "clip", "dir": f"motion/{n}", "at": at, **kw}


def K(*lines, times=None, size=150, **kw):
    lines = [[l, "white"] if isinstance(l, str) else list(l) for l in lines]
    return {"mg": "kinetic", "lines": lines, "times": times or [0.0] * len(lines), "size": size, **kw}


def KO(*lines, times=None, size=130, dy=-60):   # kinetic words as an overlay on footage
    lines = [[l, "white"] if isinstance(l, str) else list(l) for l in lines]
    return {"mg": "kinetic", "lines": lines, "times": times or [0.0] * len(lines), "size": size, "dy": dy, "at": 0.0}


def TAG(text, at=0.0):
    return {"mg": "tag", "text": text, "at": at, "pos": [0.04, 0.08]}


# name: (file, first start, volume that levels it to ~ -15 LUFS)
TRACKS = {"intrigue": ("../../reels/audio/music/echoes.mp3", 162.865, 1.0),
          "tense": ("../../reels/audio/music/out-of-this-world.mp3", 117.26, 1.0),
          "sad": ("../../reels/audio/music/silent-descent.mp3", 0.0, 0.62),
          "confident": ("../../reels/audio/music/unforgiven.mp3", 13.63, 1.0),
          "warm": ("../../reels/audio/music/fifth-of-february.mp3", 1.6, 1.15)}

CH1 = [
    ("What if, tomorrow morning,", I("empty-times", (.5, .55), 1.0, tz=1.25), {"punch": True, "sfx": ["hook"]}),
    ("every human on Earth simply disappeared?", V("empty-aerial", 1.0, 1.15), {"captions": False, "overlays": [RM("title", 0.0)],
                                                                             "sfx": [{"name": "boom", "at": "@disappeared", "gain": 0.6}]}),
    ("No war.", V("empty-boulevard", 1.0, 1.15), {"in": "cut", "sfx": [{"name": "impact", "gain": 0.4}]}),
    ("No disease.", I("empty-office", (.5, .5), 1.1, tz=1.3), {"in": "cut", "sfx": [{"name": "impact", "gain": 0.4}]}),
    ("No warning.", I("traffic-light", (.5, .4), 1.0, tz=1.3), {"in": "cut", "sfx": [{"name": "impact", "gain": 0.5}]}),
    ("Eight billion people, gone in an instant.", HF("population"), {"captions": False, "sfx": [{"name": "bass", "at": 2.3}], "music_fx": "muffle"}),
    ("Every car, every office, every bed, suddenly empty.", I("empty-office", (.4, .55), 1.4, tz=1.7), {"overlays": [RM("nobody", "@empty-0.3")]}),
    ("The cities are still there.", V("city-lights", 1.0, 1.1), {}),
    ("The lights are still on.", V("city-grid", 1.0, 1.15), {}),
    ("Somewhere, a coffee machine is still dripping into a cup nobody will drink.", I("coffee", (.45, .5), 1.0, to=(.4, .55), tz=1.6), {}),
    ("So what happens next?", V("fog-towers", 1.0, 1.1), {"in": "glitch"}),
    ("How long would it take for the planet to erase us?", I("jungle-city", (.5, .5), 1.2, tz=1.0), {"sfx": [{"name": "whoosh2", "at": "@erase"}]}),
    ("In this video, we'll fast forward through time.", HF("tl0"), {"in": "flash", "sfx": [{"name": "rewind", "at": 0.1, "gain": 0.5}]}),
    ("One hour. One year. One century. Ten thousand years.", HF("tl8"),
     {"in": "cut", "captions": False, "sfx": [{"name": "tick", "at": "@hour"}, {"name": "tick", "at": "@year"}, {"name": "tick", "at": "@century"}, {"name": "bass", "at": "@Ten"}]}),
    ("And by the end, you'll find out which of our creations would survive the longest.", I("pyramids", (.5, .5), 1.0, tz=1.3), {}),
    ("The answer is not what most people expect.", I("moon-footprint", (.45, .65), 1.0, tz=1.5), {"sfx": [{"name": "reveal", "at": "@expect"}]}),
    ("Plus one hour.", HF("ch1"), {"chapter": True, "music": "tense"}),
    ("At first, almost nothing changes.", I("empty-times", (.5, .5), 1.2, tz=1.4), {"overlays": [RM("hour", 0.0, alpha=0.9)]}),
    ("Traffic lights keep switching from red to green", V("traffic-red", 1.0, 1.15), {}),
    ("for cars that will never move again.", I("traffic-light", (.5, .6), 1.3, tz=1.0), {}),
    ("Planes that were in the air are now flying on autopilot.", I("cockpit", (.5, .5), 1.0, tz=1.3), {}),
    ("Without pilots, they keep going until the fuel runs out,", I("cockpit", (.5, .3), 1.5, tz=1.8), {"sfx": [{"name": "tick", "at": "@fuel"}]}),
    ("and then they come down.", V("earth-planet", 1.0, 1.1), {"sfx": [{"name": "boom", "at": "@down", "gain": 0.5}]}),
    ("Inside power plants, nobody is watching the screens,", I("control-room", (.5, .5), 1.0, tz=1.25), {}),
    ("nobody is shovelling in coal, nobody is checking the gas.", V("factory-smoke", 1.0, 1.15), {}),
    ("Within hours, the first power stations start shutting themselves down.", V("plant-river", 1.0, 1.1), {"fx": [{"name": "light_off", "at": "@down"}],
                                                                                                      "sfx": [{"name": "switch", "at": "@down"}]}),
    ("All over the world, phones start ringing with nobody to answer.", I("phones", (.5, .55), 1.0, tz=1.35), {}),
    ("Messages pile up, unread.", I("phones", (.55, .6), 1.6, tz=1.9), {"sfx": [{"name": "pop", "at": 0.2}, {"name": "pop", "at": 0.5}, {"name": "pop", "at": 0.8}]}),
    ("Automatic emails keep sending reminders about meetings that will never happen.", I("empty-office", (.6, .4), 1.6, tz=2.0), {}),
    ("For a little while, the internet keeps talking to itself.", V("city-lights2", 1.0, 1.1), {}),
    ("Plus one day.", HF("tl1"), {"in": "dip", "captions": False, "sfx": [{"name": "tunnel"}, {"name": "tick", "at": 0.65}]}),
    ("One by one, the lights go out.", I("city-dark", (.5, .5), 1.0, tz=1.3), {"fx": [{"name": "light_off", "at": "@out"}], "sfx": [{"name": "switch", "at": "@out"}]}),
    ("Cities that glowed for a hundred years go dark.", V("city-grid", 4.0, 1.2), {"fx": [{"name": "light_off", "at": "@dark"}]}),
    ("Some places last a little longer.", I("solar-farm", (.5, .5), 1.0, tz=1.2), {}),
    ("Solar panels keep humming in the sun.", I("solar-farm", (.4, .6), 1.4, tz=1.7), {}),
    ("Hydroelectric dams can run on their own for weeks or even months,", I("dam", (.5, .5), 1.0, tz=1.3), {}),
    ("until something clogs or breaks.", I("dam", (.5, .6), 1.5, tz=1.8), {"shake": ["@breaks"], "sfx": [{"name": "impact", "at": "@breaks", "gain": 0.5}]}),
    ("But from space, the night side of Earth looks the way it did before Thomas Edison.", I("earth-dark", (.5, .5), 1.0, tz=1.3), {"voice_fx": {"at": "@Edison", "fx": "echo"}}),
    ("And deep under New York City, something is starting to happen.", V("subway-empty", 1.0, 1.15), {"music_fx": "muffle"}),
]

CH2 = [
    ("Every day, pumps under New York pull millions of litres of groundwater", V("subway-empty", 4.0, 1.2), {"overlays": [RM("nyc", 0.3)]}),
    ("out of the subway tunnels.", I("subway-flood", (.5, .5), 1.0, tz=1.3), {}),
    ("Without electricity, those pumps stop.", I("subway-flood", (.6, .5), 1.4, tz=1.6), {"fx": [{"name": "light_off", "at": "@stop"}], "sfx": [{"name": "switch", "at": "@stop"}]}),
    ("Some engineers estimate that within a day or two,", V("flood-marsh", 3.0, 1.15), {}),
    ("parts of the subway would start to flood.", I("subway-flood", (.55, .7), 1.6, tz=2.0), {}),
    ("The city's foundations are quietly filling with water,", I("flooded-street", (.5, .6), 1.2, tz=1.5), {}),
    ("and nobody is there to notice.", V("empty-boulevard", 4.0, 1.15), {}),
    ("Plus one week.", HF("ch2"), {"chapter": True, "music": "tense"}),
    ("Now the real danger begins.", I("nuclear", (.5, .5), 1.0, tz=1.25), {"in": "glitch", "sfx": [{"name": "bass", "at": "@danger"}]}),
    ("There are around four hundred nuclear reactors on Earth.", V("tower-top", 1.0, 1.15), {"overlays": [RM("reactors", "@four-0.2")]}),
    ("Most of them are built to shut down automatically.", I("control-room", (.5, .5), 1.3, tz=1.6), {}),
    ("But even a sleeping reactor needs cooling, and so does its used fuel.", I("spent-pool", (.5, .55), 1.0, tz=1.4), {}),
    ("Backup generators keep the water flowing for a while.", I("spent-pool", (.45, .6), 1.4, tz=1.7), {}),
    ("Then the diesel runs out.", I("control-room", (.5, .45), 1.6, tz=1.9), {"fx": [{"name": "light_off", "at": "@out"}], "sfx": [{"name": "switch", "at": "@out"}]}),
    ("Some experts warn that, without people, cooling pools could boil dry,", I("spent-pool", (.5, .5), 1.2, tz=1.6), {}),
    ("and some reactors could overheat, release radiation, or catch fire.", I("nuclear", (.5, .45), 1.3, tz=1.7), {"shake": ["@fire"], "sfx": [{"name": "boom", "at": "@fire", "gain": 0.6}]}),
    ("It sounds like the end of the world.", V("smoke-dark", 1.0, 1.15), {}),
    ("But we already know what happens next, because it already happened once.", V("tower-overgrown", 1.0, 1.1), {"music": "intrigue"}),
    ("In nineteen eighty six, the Chernobyl disaster forced people to abandon the land around the plant.",
     {"mg": "year", "from": 2026, "to": 1986, "roll": 0.9, "label": "CHERNOBYL"}, {"in": "dip"}),
    ("Decades later, the exclusion zone is full of wolves,", I("chernobyl-wolves", (.5, .6), 1.0, tz=1.3), {"overlays": [RM("chernobyl", 0.1)]}),
    ("elk, lynx, wild boar, and even wild horses.", I("przewalski", (.5, .55), 1.0, tz=1.3), {}),
    ("Radiation is bad for animals.", V("horses-wild", 1.0, 1.1), {}),
    ("But, it turns out, humans were worse.", K("HUMANS WERE", ("WORSE", "red"), times=[0.0, "@worse"]), {"sfx": [{"name": "bass", "at": "@worse"}]}),
    ("Plus one month.", HF("tl3"), {"in": "dip", "captions": False, "sfx": [{"name": "tunnel"}]}),
    ("Our pets are on their own now.", V("dog-grass", 1.0, 1.15), {}),
    ("There are hundreds of millions of pet dogs on Earth.", V("dog-run", 1.0, 1.15), {"overlays": [RM("dogs", "@hundreds-0.2")]}),
    ("Many small or very pampered breeds won't make it.", I("dog-pack", (.5, .6), 1.3, tz=1.0), {}),
    ("The tough ones form packs and go wild.", I("dog-pack", (.5, .6), 1.0, tz=1.35), {"sfx": [{"name": "whoosh", "at": "@wild"}]}),
    ("Cats are fine.", I("cat-throne", (.5, .5), 1.0, tz=1.3), {"in": "cut", "music": "warm"}),
    ("Cats were always fine.", V("cat-sit", 1.0, 1.15), {"in": "cut"}),
    ("They have been practising for this their whole lives.", I("cat-throne", (.5, .45), 1.6, tz=2.1), {"punch": {"at": "@whole", "zoom": 2.4}, "sfx": [{"name": "scratch", "at": "@practising", "gain": 0.4}]}),
    ("In zoos, it's a race against time.", V("zebras", 1.0, 1.15), {"music": "intrigue"}),
    ("Some animals escape through broken fences and wander into the empty streets.", V("zebra-herd", 1.0, 1.1), {}),
    ("Imagine a zebra trotting down a motorway,", I("zebra-highway", (.5, .55), 1.0, tz=1.35), {}),
    ("or a flock of parrots taking over a shopping mall.", I("parrots-mall", (.5, .4), 1.0, tz=1.3), {"sfx": [{"name": "sparkle", "at": "@parrots"}]}),
    ("On farms, it's harder.", I("farm-cows", (.5, .5), 1.0, tz=1.25), {}),
    ("There are around a billion cattle", V("cows-field", 1.0, 1.15), {"overlays": [RM("cows", "@billion-0.2")]}),
    ("and more than twenty billion chickens, and most of them were fed by us.", V("hens", 1.0, 1.15), {"overlays": [RM("chickens", "@twenty-0.2")]}),
    ("Some break out. Many don't.", I("chickens", (.5, .6), 1.0, tz=1.3), {}),
    ("And some creatures don't survive at all, because they only ever lived on us.", V("moss-forest", 1.0, 1.1), {}),
    ("Human head lice, for example. When we go, they go.", K("HUMAN HEAD LICE", ("EXTINCT", "red"), times=[0.0, "@go"], size=130), {"sfx": [{"name": "scratch", "at": "@go", "gain": 0.4}]}),
]

CH3 = [
    ("Plus one year.", HF("ch3"), {"chapter": True, "music": "intrigue"}),
    ("Look closely at any city.", V("empty-road", 1.0, 1.15), {}),
    ("Thin green lines are cracking through the pavement.", I("cracked-street", (.5, .5), 1.0, tz=1.4), {}),
    ("Every winter, water seeps into those cracks, freezes, and expands,", I("frost-crack", (.5, .5), 1.0, tz=1.4), {"sfx": [{"name": "glass", "at": "@freezes", "gain": 0.4}]}),
    ("prying the concrete apart a little more.", V("road-crack", 1.0, 1.15), {}),
    ("Every spring, plants move into the gaps.", I("cracked-street", (.55, .55), 1.6, tz=2.0), {}),
    ("With nobody mowing, lawns turn into meadows.", I("meadow-lawn", (.5, .5), 1.0, tz=1.3), {}),
    ("Leaves pile up in gutters, block the drains,", V("rain-leaves", 1.0, 1.15), {}),
    ("and the next heavy rain floods the streets.", I("flooded-street", (.5, .5), 1.0, tz=1.3), {"sfx": [{"name": "whoosh2", "at": "@floods"}]}),
    ("City rats, which lived on our rubbish, start to go hungry.", I("rats", (.5, .6), 1.0, tz=1.35), {}),
    ("Without restaurants and bins, there is a lot less to eat, and their numbers crash.", I("rats", (.45, .65), 1.6, tz=1.9), {"sfx": [{"name": "bass", "at": "@crash"}]}),
    ("Meanwhile, the sky is changing.", V("sky-dusk", 1.0, 1.1), {}),
    ("With no factories and no traffic, the air gets cleaner surprisingly fast.", V("fog-skyline", 1.0, 1.1), {}),
    ("And at night, without street lights, the stars come back.", V("milky-way", 1.0, 1.15), {"sfx": [{"name": "sparkle", "at": "@stars"}]}),
    ("For the first time in a century, you could see the Milky Way from the middle of a big city.", I("clear-sky-city", (.5, .35), 1.0, to=(.5, .25), tz=1.3), {}),
    ("Up above, our satellites are still circling the Earth.", I("satellite", (.5, .5), 1.0, tz=1.3), {}),
    ("Some will keep working for years.", V("iss", 1.0, 1.1), {}),
    ("Then, one by one, they will slowly fall and burn up in the atmosphere.", I("sat-reentry", (.5, .5), 1.0, tz=1.35), {"sfx": [{"name": "whoosh", "at": "@burn"}]}),
    ("Others are so high that they'll keep orbiting for a very long time.", V("satellite-earth", 1.0, 1.1), {}),
    ("Plus ten years.", HF("tl5"), {"in": "dip", "captions": False, "sfx": [{"name": "tunnel"}]}),
    ("Wooden houses are in trouble.", I("house-rot", (.5, .5), 1.0, tz=1.25), {}),
    ("Roofs start to leak, the water rots the beams, and the first ones collapse.", V("house-ruin", 1.0, 1.15), {"shake": ["@collapse"], "sfx": [{"name": "impact", "at": "@collapse", "gain": 0.6}]}),
    ("We know how this goes, too.", I("pripyat", (.5, .5), 1.2, tz=1.0), {}),
    ("The abandoned city of Pripyat, near Chernobyl,", I("pripyat", (.5, .4), 1.0, tz=1.35), {"overlays": [RM("pripyat", "@Pripyat")]}),
    ("was left empty in nineteen eighty six.", V("ruin-wall", 1.0, 1.15), {}),
    ("Today, trees grow out of its buildings, moss covers its floors,", V("ivy-wall", 1.0, 1.15), {}),
    ("and its famous fairground is being swallowed by forest.", I("ferris", (.5, .5), 1.0, tz=1.3), {}),
    ("Back in our empty cities, fires are a growing danger.", I("city-fire", (.5, .5), 1.0, tz=1.3), {"in": "glitch", "music": "tense"}),
    ("A single lightning strike can now burn through whole neighbourhoods,", V("lightning", 1.0, 1.15), {"shake": ["@lightning"], "sfx": [{"name": "boom", "at": "@lightning", "gain": 0.6}]}),
    ("because there are no firefighters left to stop it.", V("wildfire", 1.0, 1.15), {}),
    ("And the ash makes the soil richer.", V("ash", 1.0, 1.15), {}),
    ("The forest is coming.", I("jungle-city", (.5, .5), 1.0, tz=1.35), {"voice_fx": {"at": "@coming", "fx": "echo"}, "sfx": [{"name": "bass", "at": "@forest"}]}),
    ("And it isn't alone.", V("refinery-aerial", 1.0, 1.1), {"in": "glitch"}),
    ("Oil refineries and chemical plants, with nobody to maintain them,", I("refinery-rust", (.5, .5), 1.0, tz=1.3), {}),
    ("slowly leak and corrode.", V("rust-van", 1.0, 1.15), {}),
    ("Some of their tanks will rust through.", V("rust-ship", 1.0, 1.15), {}),
    ("For a while, the worst places will be toxic.", I("refinery-rust", (.4, .55), 1.5, tz=1.8), {}),
    ("But even there, life slowly finds a way.", V("fern-close", 1.0, 1.15), {"sfx": [{"name": "sparkle", "at": "@life"}]}),
]

CH4 = [
    ("Plus one hundred years.", HF("ch4"), {"chapter": True, "music": "confident"}),
    ("A century without people, and the city is now a jungle with skyscrapers in it.", I("jungle-city", (.5, .5), 1.0, to=(.55, .4), tz=1.35), {}),
    ("Steel is strong, but steel rusts.", I("bridge-rust", (.5, .5), 1.0, tz=1.3), {}),
    ("For a hundred years, nobody has painted a single bridge.", V("bridge-forest", 1.0, 1.1), {}),
    ("Some experts think many steel bridges would collapse within a few centuries.", I("bridge-rust", (.4, .6), 1.4, tz=1.8), {}),
    ("Big suspension bridges might fall even sooner, once their cables corrode.", V("bridge-river", 1.0, 1.15), {"shake": ["@fall"], "sfx": [{"name": "impact", "at": "@fall", "gain": 0.6}]}),
    ("Inside our tall buildings, the steel bars hidden in the concrete are rusting too.", I("concrete-rebar", (.5, .5), 1.0, tz=1.4), {}),
    ("Rust takes up more space than steel, so it pushes the concrete apart from the inside.", I("concrete-rebar", (.55, .45), 1.5, tz=1.9), {"sfx": [{"name": "glass", "at": "@pushes", "gain": 0.4}]}),
    ("Bit by bit, the towers start to crumble.", V("fog-spire", 1.0, 1.15), {}),
    ("Most wooden houses are gone.", V("house-window", 1.0, 1.15), {}),
    ("Our suburbs look like forests with a few brick chimneys poking out.", I("suburb-forest", (.5, .5), 1.0, tz=1.3), {}),
    ("Animals have moved in everywhere.", V("deer-forest", 1.0, 1.15), {"music": "warm"}),
    ("Deer graze where shopping centres used to be.", I("deer-mall", (.5, .55), 1.0, tz=1.3), {}),
    ("Bears and wolves return to places they haven't seen in centuries.", I("bear-street", (.5, .55), 1.0, tz=1.35), {}),
    ("Elephants in Africa, no longer hunted, slowly spread back across their old lands.", I("elephants", (.5, .55), 1.0, tz=1.3), {}),
    ("Fish return to rivers.", V("waterfall", 1.0, 1.15), {}),
    ("Coral reefs, without our pollution and fishing boats, begin to recover in many places.", I("reef-recover", (.5, .5), 1.0, tz=1.3), {"sfx": [{"name": "sparkle", "at": "@recover"}]}),
    ("But some of what we left behind won't go away so easily.", V("smoke-dark", 1.0, 1.15), {"in": "glitch", "music": "intrigue"}),
    ("Plastic doesn't really rot.", I("plastic-sea", (.5, .5), 1.0, tz=1.3), {"overlays": [RM("notrace", 0.2)], "sfx": [{"name": "impact", "at": 0.25, "gain": 0.6}]}),
    ("It breaks into smaller and smaller pieces that can last for centuries.", I("plastic-sea", (.6, .45), 1.6, tz=2.0), {}),
    ("Our bottles, bags and toys are now a permanent part of the ocean.", V("waves-aerial", 1.0, 1.1), {}),
    ("And the carbon dioxide we put into the air won't disappear quickly either.", V("factory-smoke", 4.0, 1.15), {}),
    ("Most of it will be absorbed by the oceans over centuries,", V("deep-rays", 1.0, 1.1), {}),
    ("but some of it will stay in the atmosphere for thousands of years.", I("earth-heal", (.5, .5), 1.3, tz=1.0), {}),
    ("Even without us, the planet is still feeling our fever.", V("sky-dusk", 3.0, 1.15), {"voice_fx": {"at": "@fever", "fx": "echo"}}),
    ("Still, by now, the air is clean, the night is dark, and the noise is gone.", I("quiet-city", (.5, .5), 1.0, tz=1.3), {"music": "warm", "music_fx": "muffle"}),
    ("No engines, no sirens, no music.", V("forest-mist", 1.0, 1.1),
     {"overlays": [KO("NO ENGINES.", "NO SIRENS.", ("NO MUSIC.", "yellow"), times=["@engines", "@sirens", "@music"], size=110)], "captions": False, "music_fx": "muffle"}),
    ("Only wind, rain, birdsong,", V("rain-puddle2", 1.0, 1.15), {}),
    ("and the occasional crash of a falling tower.", V("fog-spire", 3.0, 1.2), {"sfx": [{"name": "boom", "at": "@crash", "gain": 0.6}], "shake": ["@crash"]}),
]

CH5 = [
    ("Plus one thousand years.", HF("tl7"), {"in": "dip", "captions": False, "music": "intrigue", "sfx": [{"name": "tunnel"}, {"name": "tick", "at": 0.65}]}),
    ("Most of our cities are now forests and swamps.", V("forest-top", 1.0, 1.1), {}),
    ("If you walked through New York, you would see hills covered in trees,", I("nyc-forest", (.5, .5), 1.0, tz=1.3), {}),
    ("and every so often, a strange stone shape poking through the leaves.", I("nyc-forest", (.7, .3), 1.5, tz=1.9), {"sfx": [{"name": "reveal", "at": "@stone"}]}),
    ("That's because stone lasts far longer than steel or wood.", I("granite", (.5, .5), 1.0, tz=1.3), {}),
    ("Granite, marble, and the hardest concrete hold out the longest.", HF("lasts"), {}),
    ("Our roads are gone, buried under soil and roots.", V("jungle-path", 1.0, 1.15), {}),
    ("Our dams have cracked and given way, and rivers have found their old paths again.", I("dam-broken", (.5, .5), 1.0, tz=1.3), {}),
    ("Somewhere, a forgotten cellar still holds glass bottles, perfectly fine.", I("cellar-bottles", (.5, .5), 1.0, tz=1.35), {}),
    ("Glass can last for an incredibly long time.", I("cellar-bottles", (.6, .45), 1.6, tz=1.9), {"sfx": [{"name": "sparkle", "at": "@glass"}]}),
    ("Your phone? It's long gone.", I("phone-soil", (.5, .5), 1.0, tz=1.35), {"in": "glitch", "sfx": [{"name": "glitch-hit"}]}),
    ("Its battery leaked, its circuits corroded, and its screen cracked under the soil.", I("phone-soil", (.45, .55), 1.5, tz=1.9), {}),
    ("But its gold and copper are still down there, waiting.", V("stream", 1.0, 1.15), {}),
    ("Plus ten thousand years.", HF("ch5"), {"chapter": True, "music": "confident"}),
    ("Now we're talking about the age of the pyramids, doubled.", V("pyramids-v", 1.0, 1.1), {}),
    ("The Great Pyramid of Giza is already about four and a half thousand years old.", V("pyramid-v", 1.0, 1.15), {"overlays": [RM("pyramid", "@four-0.2")]}),
    ("In ten thousand more, it's worn and weathered, but very likely still there.", I("pyramids", (.5, .5), 1.0, tz=1.3), {}),
    ("Mount Rushmore is carved in granite,", I("granite", (.5, .45), 1.3, tz=1.6), {}),
    ("which erodes by only about an inch every ten thousand years.", I("granite", (.5, .5), 1.0, tz=1.2), {"overlays": [RM("granite", "@inch-0.3")]}),
    ("The four faces will still be staring out over a world with nobody left to look back.", I("granite", (.4, .4), 1.6, tz=2.0), {"voice_fx": {"at": "@back", "fx": "echo"}}),
    ("Parts of the Great Wall of China, especially the sections made of stone, may also still be standing.", I("great-wall", (.5, .5), 1.0, tz=1.3), {}),
    ("And our footprints on the Moon?", I("moon-footprint", (.45, .65), 1.0, tz=1.4), {"in": "glitch"}),
    ("There is no wind or rain up there.", I("moon-footprint", (.5, .3), 1.4, tz=1.6), {"overlays": [RM("apollo", 0.1)]}),
    ("The footprints of the Apollo astronauts could last for millions of years.", I("moon-footprint", (.45, .7), 1.8, tz=2.2), {"sfx": [{"name": "bass", "at": "@millions"}]}),
    ("Out in space, the Voyager probes keep flying,", I("voyager", (.5, .5), 1.0, tz=1.35), {"overlays": [RM("voyager", "@Voyager")]}),
    ("each carrying a golden record of human music and voices.", I("voyager", (.62, .55), 1.6, tz=2.0), {"sfx": [{"name": "sparkle", "at": "@golden"}]}),
    ("They could drift between the stars for billions of years.", V("sky-milky", 1.0, 1.1), {}),
]

CH6 = [
    ("So, millions of years from now, would anyone know we were here?", HF("ch6"), {"chapter": True, "music": "intrigue"}),
    ("Imagine a future scientist, maybe from a new species that evolved after us,", V("forest-mist", 3.0, 1.15), {}),
    ("digging into the rock.", I("rock-layers", (.5, .5), 1.0, tz=1.3), {}),
    ("They'd find a thin, strange layer.", I("rock-layers", (.45, .55), 1.5, tz=1.9), {"sfx": [{"name": "reveal", "at": "@layer"}]}),
    ("Bits of concrete and plastic.", K("CONCRETE.", ("PLASTIC.", "yellow"), times=["@concrete", "@plastic"]), {"sfx": [{"name": "pop", "at": "@concrete"}, {"name": "pop", "at": "@plastic"}]}),
    ("Traces of radioactive elements from the nuclear tests of the nineteen fifties and sixties.", V("tower-overgrown", 3.0, 1.15), {}),
    ("And an astonishing number of chicken bones.", V("rooster", 1.0, 1.15), {"in": "cut", "sfx": [{"name": "scratch", "at": "@chicken", "gain": 0.5}]}),
    ("Some geologists think that layer could be one of the clearest signs we ever existed.", I("rock-layers", (.5, .5), 1.2, tz=1.4), {}),
    ("They call this time the Anthropocene, the age of humans.", V("earth-night", 4.0, 1.1), {"overlays": [RM("anthro", "@Anthropocene")]}),
    ("Just one thin stripe in the rocks, that's it.", I("rock-layers", (.5, .6), 1.8, tz=2.2), {"voice_fx": {"at": "@it", "fx": "echo"}}),
    ("And there's one more sign we left, travelling outward at the speed of light.", V("radio-dish", 1.0, 1.15), {}),
    ("Our earliest radio and TV broadcasts are still racing through space.", I("radio-waves", (.5, .5), 1.0, tz=1.3), {}),
    ("Today, they're about a hundred light years from Earth, and they'll never stop.", HF("radio"), {"captions": False}),
    ("So, what if all humans disappeared tomorrow?", V("empty-aerial", 4.0, 1.15), {"in": "dip", "pause_before": 0.3, "captions": False, "music": "warm",
                                                                                     "overlays": [RM("title", 0.2)]}),
    ("The lights would go out in a day.", I("city-dark", (.5, .5), 1.2, tz=1.5), {}),
    ("The cities would turn green in a century.", I("jungle-city", (.5, .5), 1.0, tz=1.3), {}),
    ("Most of our buildings would be gone in a few thousand years.", I("nyc-forest", (.5, .5), 1.2, tz=1.0), {}),
    ("And the Earth would heal faster than you might think.", I("earth-heal", (.5, .5), 1.0, tz=1.3), {}),
    ("The wolves would return,", I("chernobyl-wolves", (.5, .6), 1.4, tz=1.7), {"in": "cut"}),
    ("the stars would come back,", I("clear-sky-city", (.5, .3), 1.2, tz=1.5), {"in": "cut"}),
    ("and the forests would take the cities.", I("final-forest", (.5, .5), 1.0, tz=1.3), {}),
    ("But here's the strange part.", K("THE STRANGE", ("PART", "yellow"), times=[0.0, "@part"]), {"in": "glitch"}),
    ("The planet doesn't need us to survive.", I("earth-heal", (.5, .5), 1.3, tz=1.6), {}),
    ("It did perfectly fine for billions of years before we arrived.", V("waterfall", 3.0, 1.15), {}),
    ("We are the ones who need it.", K("WE NEED", ("IT", "yellow"), times=[0.0, "@need"], size=190), {"sfx": [{"name": "bass", "at": "@need"}]}),
    ("So maybe the real question isn't what the world would do without us.", I("quiet-city", (.5, .5), 1.2, tz=1.0), {}),
    ("It's what we'll do with the world, while we're still here.", I("final-forest", (.5, .45), 1.0, tz=1.35), {"captions": False, "overlays": [RM("ending", "@while-0.2")],
                                                                                                              "sfx": [{"name": "bass", "at": "@still"}]}),
]

CHAPTERS = [CH1, CH2, CH3, CH4, CH5, CH6]
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
            if ov["mg"] == "tag":
                sh["sfx"] = sh.get("sfx", []) + [{"name": "click", "at": ov["at"], "gain": 0.6}]
        out.append(sh)
        prev = k
    return out


def words(s):
    return [re.sub(r"[^a-z0-9']", "", w.lower()) for w in s.split()]


def main():
    shots, cues, used = [], [{"shot": 0, "music": TRACKS["intrigue"][0], "start": TRACKS["intrigue"][1], "volume": 1.0}], {"intrigue"}
    for n, ch in enumerate(CHAPTERS, 1):
        want = words((HERE / "chapters" / f"ch{n}.txt").read_text())
        got = [w for text, _, _ in ch for w in words(text)]
        if want != got:
            i = next(i for i, (a, b) in enumerate(zip(want + ["<end>"], got + ["<end>"])) if a != b)
            raise SystemExit(f"ch{n}: shot text differs from the script at word {i}: script {want[i:i + 6]} vs shots {got[i:i + 6]}")
        for sh in auto([{"text": text, "v": v, **ex} for text, v, ex in ch]):
            if not shots:
                sh.pop("in", None)
            m = sh.pop("music", None)
            if m:
                cue = {"shot": len(shots), "music": TRACKS[m][0], "volume": TRACKS[m][2]}
                if m not in used:
                    cue["start"] = TRACKS[m][1]
                    used.add(m)
                cues.append(cue)
            shots.append(sh)
    spec = {"out": "../output/humans-full.mp4", "audio": [f"chapters/take{i}.wav" for i in range(1, 10)], "take_gap": 0.4, "speed": 0.95,
            "music_cues": cues, "music_volume": 0.38, "fade_out": 2.5, "progress": True, "shots": shots}
    (HERE / "video.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False))
    n_img = sum(1 for s in shots if kind(s["v"]) == "img")
    n_vid = sum(1 for s in shots if kind(s["v"]) == "video")
    n_ov = sum(1 for s in shots for o in s.get("overlays", []) if o["mg"] == "clip")
    print(f"{len(shots)} shots: {n_img} AI images, {n_vid} stock videos, {len(shots) - n_img - n_vid} motion-graphic shots, "
          f"{n_ov} Remotion overlays; {len(cues)} music cues")


if __name__ == "__main__":
    main()
