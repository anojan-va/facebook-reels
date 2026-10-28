"""Build video.json for "What if the Moon disappeared?" (~11 min, same editing style as ../asteroid-full).

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
    ("What if, tonight,", V("moon-glow", 1.0, 1.25, drift=0.12), {"punch": True, "sfx": ["hook"]}),
    ("the Moon simply disappeared?", I("moon-city", (.47, .3), 1.3, tz=1.6), {"captions": False, "overlays": [RM("title", 0.0)],
                                                                           "sfx": [{"name": "boom", "at": "@disappeared", "gain": 0.6}]}),
    ("No explosion.", I("moon-vanish", (.45, .3), 1.4, tz=1.7), {"in": "glitch", "sfx": [{"name": "glitch-hit"}]}),
    ("No warning.", V("moon-cloud", 1.0, 1.2), {"in": "glitch", "sfx": [{"name": "glitch"}]}),
    ("One moment it's there,", I("moon-city", (.47, .4), 1.0, tz=1.15), {}),
    ("and the next, the sky is empty.", I("moon-vanish", (.5, .45), 1.0, tz=1.2), {"in": "flash", "fx": [{"name": "light_off", "at": "@empty"}],
                                                                               "sfx": [{"name": "switch", "at": "@empty"}]}),
    ("It sounds harmless.", V("sky-trees", 1.0, 1.1), {}),
    ("The Moon is just a light in the sky, right?", V("moon-trees", 1.0, 1.15), {"sfx": [{"name": "tick", "at": "@right"}]}),
    ("But that rock has been quietly holding our world together", I("earth-moon", (.4, .55), 1.0, tz=1.3), {"in": "glitch", "music_fx": "muffle"}),
    ("for billions of years.", V("earth-night", 3.0, 1.1), {"music_fx": "muffle"}),
    ("It moves our oceans,", V("waves-aerial", 1.0, 1.1), {"in": "flash", "sfx": [{"name": "bass", "at": 0.0}]}),
    ("steadies our planet,", I("earth-tilt", (.5, .5), 1.0, tz=1.25), {}),
    ("sets the clock for countless animals,", I("coral-spawn", (.5, .5), 1.0, tz=1.3), {}),
    ("and it even shaped the length of your day.", V("clock", 1.0, 1.15), {"sfx": [{"name": "tick", "at": "@length"}, {"name": "tick", "at": "@day"}]}),
    ("In this video, we'll follow what happens step by step,", V("sky-milky", 1.0, 1.1, drift=0.1), {}),
    ("from the first night without it,", I("dark-land", (.5, .5), 1.0, tz=1.25), {}),
    ("to the strange, wobbling world it would leave behind.", HF("tilt", 3.2), {"in": "zoom"}),
    ("And by the end, you'll see why some scientists think", I("young-earth", (.5, .45), 1.0, tz=1.3), {}),
    ("we might not even be here without it.", I("tide-pools-life", (.5, .5), 1.0, tz=1.35), {"sfx": [{"name": "boom", "at": "@here", "gain": 0.5}]}),
    ("Chapter one. The first night.", HF("ch1"), {"chapter": True, "music": "tense"}),
    ("It's a clear night, and the Moon is full.", V("moon-glow", 4.0, 1.15), {}),
    ("Then, in an instant, it's gone.", I("moon-vanish", (.45, .3), 1.0, tz=1.5), {"in": "flash", "shake": ["@gone"],
                                                                               "fx": [{"name": "light_off", "at": "@gone"}], "sfx": [{"name": "impact", "at": "@gone"}]}),
    ("The first thing you notice is the dark.", I("dark-land", (.5, .55), 1.3, tz=1.0), {"voice_fx": {"at": "@dark", "fx": "echo"}}),
    ("A full Moon lights the ground", V("moon-forest", 1.0, 1.1), {}),
    ("around a hundred times brighter than starlight alone.", V("moon-trees", 2.0, 1.15), {"overlays": [RM("x100", "@hundred-0.2")], "sfx": [{"name": "pop", "at": "@hundred"}]}),
    ("Now every night is as dark as a new Moon night, forever.", V("sky-dusk", 1.0, 1.1), {"fx": [{"name": "light_off", "at": "@forever"}]}),
    ("Astronomers would actually love it.", V("observatory", 2.0, 1.1), {}),
    ("With no moonlight washing out the sky,", V("stars", 1.0, 1.15), {}),
    ("the Milky Way would shine on every clear night of the year.", I("milky-way-desert", (.55, .35), 1.0, to=(.6, .25), tz=1.3),
     {"sfx": [{"name": "sparkle", "at": "@Milky"}]}),
    ("But something else changes right away, and you can't see it.", V("earth-planet", 1.0, 1.1, drift=0.12), {"in": "glitch"}),
    ("The Moon's gravity is gone.", K("THE MOON'S GRAVITY", ("IS GONE", "red"), times=[0.0, "@gone"]), {"sfx": [{"name": "bass", "at": "@gone"}]}),
    ("Earth and the Moon don't simply travel around the Sun side by side.", I("earth-moon", (.45, .5), 1.2, tz=1.0), {}),
    ("They swing around a shared balance point,", HF("bary"), {"sfx": [{"name": "pop", "at": 1.0}]}),
    ("about four thousand seven hundred kilometres from Earth's centre.", HF("bary", 1.7), {"in": "cut", "captions": False, "sfx": [{"name": "impact", "at": 0.1, "gain": 0.5}]}),
    ("Without the Moon, that dance stops,", I("earth-alone", (.55, .5), 1.0, tz=1.3), {}),
    ("and Earth settles into a slightly different path around the Sun.", V("earth-turn", 1.0, 1.05, drift=0.15), {}),
    ("The change is tiny, and you wouldn't feel a thing.", I("earth-alone", (.55, .5), 1.4, tz=1.6), {}),
    ("There's no earthquake, no flood, no sudden end of the world.", V("sea-sunset", 1.0, 1.1),
     {"overlays": [KO(("NO EARTHQUAKE", "white"), ("NO FLOOD", "white"), ("NO END", "yellow"), times=["@earthquake", "@flood", "@sudden"], size=110)],
      "captions": False, "sfx": [{"name": "pop", "at": "@earthquake"}, {"name": "pop", "at": "@flood"}, {"name": "pop", "at": "@sudden"}]}),
    ("But at the next high tide,", I("night-beach", (.5, .6), 1.0, tz=1.2), {"in": "glitch"}),
    ("the ocean doesn't come as far up the beach as it should.", V("tide-beach", 1.0, 1.1), {}),
    ("And that's where the trouble begins.", V("tide-flat", 1.0, 1.15), {"music_fx": "muffle", "sfx": [{"name": "boom", "at": "@trouble", "gain": 0.6}]}),
]

CH2 = [
    ("Chapter two. The tides fall.", HF("ch2"), {"chapter": True, "music": "intrigue"}),
    ("Twice a day, all around the world, the oceans rise and fall.", V("tide-rocks", 1.0, 1.1), {}),
    ("Most of that is the Moon.", V("moon-big", 2.0, 1.15), {"sfx": [{"name": "bass", "at": "@Moon"}]}),
    ("Its gravity pulls on the side of Earth facing it a little harder than on the far side,", I("tidal-bulge", (.5, .5), 1.0, tz=1.25), {}),
    ("stretching our oceans into two bulges.", HF("bulge"), {"sfx": [{"name": "sweep", "at": 0.3}]}),
    ("As Earth spins through them, we get high tide and low tide.", I("fundy-high", (.5, .5), 1.0, tz=1.2), {}),
    ("The Sun makes tides too, but they're less than half as strong.",
     {"mg": "bars", "headline": "TIDAL PULL", "bars": [["MOON", 100, "yellow"], ["SUN", 46, "grey"]]}, {"sfx": [{"name": "sweep", "at": 0.2}]}),
    ("So without the Moon, only the Sun's tides are left.", HF("bulge", 3.0), {}),
    ("They'd be less than half the size we're used to,", V("tide-town", 1.0, 1.1), {}),
    ("and they'd look almost the same every day of the month.", I("phases", (.5, .5), 1.0, tz=1.3), {}),
    ("No more spring tides. No more king tides.", V("swell", 1.0, 1.15), {"overlays": [RM("nospring", "@spring")], "sfx": [{"name": "impact", "at": "@spring", "gain": 0.7}]}),
    ("In Canada's Bay of Fundy, home of the highest tides on Earth,", I("fundy-low", (.5, .5), 1.0, tz=1.25), {"overlays": [RM("fundy", "@Bay")]}),
    ("the water can rise and fall by about sixteen metres.", I("fundy-high", (.4, .6), 1.2, tz=1.5), {"overlays": [RM("m16", "@sixteen-0.2")]}),
    ("That show would shrink to a fraction of its size.", I("fundy-low", (.4, .65), 1.4, tz=1.8), {}),
    ("Tidal power plants, like La Rance in France,", I("tidal-dam", (.55, .55), 1.0, tz=1.3), {"overlays": [RM("rance", "@Rance")]}),
    ("which has been making electricity from the tides since nineteen sixty six,", I("tidal-dam", (.65, .6), 1.4, tz=1.7), {}),
    ("would lose most of their energy.", I("tidal-dam", (.5, .5), 1.1, tz=1.0), {"sfx": [{"name": "switch", "at": "@lose"}]}),
    ("The bigger change happens underwater.", V("deep-rays", 1.0, 1.15), {"in": "glitch"}),
    ("Tides don't just move water up and down a beach.", V("foam", 1.0, 1.1), {}),
    ("As they slosh across the ocean floor, they help stir the deep sea,", I("deep-ocean", (.5, .5), 1.0, tz=1.35), {}),
    ("mixing heat and nutrients through the oceans.", V("fish-blue", 1.0, 1.1), {}),
    ("Weaker tides mean a calmer, more layered ocean,", V("sun-path", 1.0, 1.1), {}),
    ("and over time, that could shift ocean currents and the climates that depend on them.", V("hurricane-space", 1.0, 1.05, drift=0.12), {}),
    ("And along every coastline, a whole world is about to shrink.", V("cliffs", 1.0, 1.1), {}),
    ("The intertidal zone, the strip of shore that floods and drains every day,", I("rock-pool", (.5, .5), 1.0, tz=1.3),
     {"overlays": [TAG("THE INTERTIDAL ZONE")]}),
    ("is home to crabs,", V("crab", 1.0, 1.15), {"in": "cut", "sfx": [{"name": "pop"}]}),
    ("mussels, sea stars,", V("starfish", 1.0, 1.15), {"in": "cut", "sfx": [{"name": "pop"}]}),
    ("barnacles and countless birds that feed there at low tide.", I("mudflat-birds", (.5, .5), 1.0, tz=1.25), {}),
    ("With smaller tides, that strip gets narrower,", V("tide-birds", 1.0, 1.1), {}),
    ("and much of the life squeezed into it loses its home.", I("rock-pool", (.45, .55), 1.5, tz=1.9), {}),
    ("But for some animals, losing the Moon means losing something even more important.", V("moon-cloud2", 1.0, 1.1), {"music_fx": "muffle"}),
    ("Their calendar.", K(("THEIR CALENDAR", "yellow"), size=170), {"in": "flash", "voice_fx": {"at": "@calendar", "fx": "echo"},
                                                                  "sfx": [{"name": "bass", "at": "@calendar"}]}),
]

CH3 = [
    ("Chapter three. The animals that lose their clock.", HF("ch3"), {"chapter": True, "music": "sad"}),
    ("Every year, a few nights after a full Moon in late spring,", I("reef-moon", (.5, .4), 1.0, tz=1.3), {}),
    ("the Great Barrier Reef does something incredible.", V("coral", 1.0, 1.1), {"overlays": [RM("reef", "@Great")]}),
    ("More than a hundred kinds of coral", V("coral", 4.0, 1.15), {"overlays": [RM("coral100", "@hundred-0.2")]}),
    ("release their eggs and sperm at almost the same moment,", I("coral-spawn", (.5, .6), 1.0, to=(.5, .35), tz=1.35), {}),
    ("filling the water like an underwater snowstorm.", I("coral-spawn", (.5, .4), 1.5, tz=2.0), {"sfx": [{"name": "sparkle", "at": "@snowstorm"}]}),
    ("Corals have no eyes, but they can sense moonlight.", V("coral2", 1.0, 1.15), {}),
    ("Scientists think the changing light of the Moon helps them pick the right night.", I("reef-moon", (.5, .3), 1.4, tz=1.0), {}),
    ("Without the Moon, that signal disappears.", I("reef-moon", (.5, .3), 1.0, tz=1.2), {"fx": [{"name": "light_off", "at": "@disappears"}],
                                                                                         "sfx": [{"name": "switch", "at": "@disappears"}]}),
    ("Spawning could drift out of sync,", V("reef-fish", 1.0, 1.1), {"in": "glitch"}),
    ("and when corals spawn at different times, far fewer eggs meet.", K("FAR FEWER", ("EGGS MEET", "red"), times=[0.0, "@eggs"]), {}),
    ("On the beaches of California, little silver fish called grunion", I("grunion", (.5, .6), 1.0, tz=1.3), {"overlays": [RM("grunion", "@grunion")]}),
    ("wait for the highest tides after a full or new Moon.", V("moon-glow", 2.0, 1.2), {}),
    ("Then they ride the waves up onto the sand to lay their eggs.", I("grunion", (.4, .7), 1.4, tz=1.8), {"sfx": [{"name": "swoosh-fast", "at": "@ride"}]}),
    ("About ten days later, the next big tides wash the hatchlings out to sea.", V("waves-aerial", 4.0, 1.1), {"overlays": [TAG("+ 10 DAYS")]}),
    ("With tiny tides that barely change, that perfect timing is gone.", V("tide-sunset", 1.0, 1.1), {}),
    ("In Delaware Bay, horseshoe crabs,", I("horseshoe-crabs", (.5, .6), 1.0, tz=1.3), {"overlays": [RM("delaware", "@Delaware")]}),
    ("animals older than the dinosaurs,", I("horseshoe-crabs", (.45, .65), 1.5, tz=1.9), {}),
    ("crawl ashore by the hundreds of thousands to spawn on the high tides of late spring,", V("hermit", 1.0, 1.15), {}),
    ("with the biggest crowds around new and full Moons.", I("phases", (.5, .5), 1.3, tz=1.0), {}),
    ("Their eggs feed migrating birds like the red knot,", I("red-knot", (.5, .55), 1.0, tz=1.3), {}),
    ("which flies thousands of kilometres and stops here to refuel.", V("birds-sky", 1.0, 1.1), {}),
    ("Break the crabs' timing, and you break the birds' journey too.", I("red-knot", (.45, .5), 1.5, tz=1.8), {"in": "glitch", "sfx": [{"name": "glass", "at": "@Break"}]}),
    ("And it's not just the ocean.", K("NOT JUST", ("THE OCEAN", "yellow"), times=[0.0, "@ocean"]), {}),
    ("Dung beetles in Africa use polarised moonlight", I("dung-beetle", (.5, .55), 1.0, tz=1.35), {"overlays": [RM("beetle", "@Dung")]}),
    ("to roll their dung balls in a straight line at night.", V("beetles", 1.0, 1.15), {}),
    ("Predators follow the Moon, too.", I("owl-night", (.55, .45), 1.0, tz=1.3), {"in": "glitch"}),
    ("Lions in Tanzania catch more prey on the darkest nights, when there's little moonlight.", I("lions-night", (.5, .55), 1.0, tz=1.3),
     {"overlays": [RM("lions", "@Lions")]}),
    ("So for lions, a moonless world might be a better world.", V("lion-face", 1.0, 1.15), {}),
    ("For the animals they hunt, it's a nightmare.", I("zebra-night", (.5, .5), 1.0, tz=1.3), {"sfx": [{"name": "boom", "at": "@nightmare", "gain": 0.5}]}),
    ("Even tiny animals in the Arctic Ocean,", V("jellyfish", 1.0, 1.15), {}),
    ("during the months-long polar night, move up and down through the water following the Moon.", I("arctic-plankton", (.5, .5), 1.0, tz=1.35),
     {"overlays": [RM("arctic", "@polar")]}),
    ("Take the Moon away, and one of the oldest clocks on Earth stops ticking.", V("clock", 3.0, 1.2), {"sfx": [{"name": "tick", "at": 0.2}, {"name": "tick", "at": 0.7},
                                                                                                     {"name": "bass", "at": "@stops"}]}),
    ("But the biggest change of all would take much longer to arrive.", I("earth-tilt", (.5, .5), 1.0, tz=1.3), {"music_fx": "muffle"}),
    ("Our seasons.", K(("OUR SEASONS", "yellow"), size=170), {"in": "flash", "sfx": [{"name": "bass", "at": "@seasons"}]}),
]

CH4 = [
    ("Chapter four. Wobbling seasons.", HF("ch4"), {"chapter": True, "music": "tense"}),
    ("Earth is tilted.", I("earth-tilt", (.5, .5), 1.2, tz=1.5), {}),
    ("Right now, its axis leans by about twenty three and a half degrees,", HF("tilt"), {"captions": False}),
    ("and that tilt is the reason we have seasons.", I("summer-winter", (.5, .5), 1.0, tz=1.2), {}),
    ("When your half of the planet leans toward the Sun, it's summer.", V("meadow", 1.0, 1.1), {}),
    ("When it leans away, it's winter.", V("snow-trees", 1.0, 1.1), {"in": "flash"}),
    ("That tilt isn't perfectly fixed.", I("earth-tilt", (.45, .5), 1.4, tz=1.7), {"in": "glitch"}),
    ("Today it rocks gently between about twenty two and twenty four and a half degrees,", HF("tilt", 0.3), {"captions": False}),
    ("over a cycle of about forty one thousand years.", V("sky-milky", 3.0, 1.1), {"overlays": [RM("yr41k", "@forty-0.2")]}),
    ("Part of the reason it stays so steady is the Moon.", V("moon-glow", 3.0, 1.2), {}),
    ("Its gravity tugs on Earth's bulging middle", I("earth-tilt", (.5, .5), 1.0, tz=1.3), {}),
    ("and keeps our planet spinning like a steady top.", V("globe", 1.0, 1.1), {}),
    ("Without the Moon, the pulls from the other planets", I("earth-alone", (.5, .5), 1.0, tz=1.3), {}),
    ("would have far more say over our tilt.", V("sky-milky", 6.0, 1.15), {}),
    ("In the nineteen nineties, scientists ran simulations", {"mg": "year", "from": 2026, "to": 1993, "roll": 0.8, "label": "THE SIMULATIONS"}, {"in": "dip"}),
    ("suggesting that a Moonless Earth could tip chaotically,", HF("tilt", 3.2), {"overlays": [RM("laskar", 0.3)]}),
    ("anywhere from almost upright to more than eighty degrees.", I("earth-tilt", (.5, .5), 1.2, tz=1.6),
     {"overlays": [KO(("0° → 80°+", "red"), times=["@eighty"], size=170)], "captions": False, "shake": ["@eighty"]}),
    ("Newer studies found the swings would probably be smaller and slower than feared,", I("earth-tilt", (.55, .5), 1.0, tz=1.25),
     {"overlays": [RM("lissauer", "@Newer")]}),
    ("perhaps ten to twenty degrees, playing out over hundreds of millions of years.", V("sky-dusk", 3.0, 1.1),
     {"overlays": [KO(("10–20°", "yellow"), times=["@ten"], size=170)], "captions": False}),
    ("But even that is enough to change everything.", K("ENOUGH TO", ("CHANGE EVERYTHING", "red"), times=[0.0, "@change"]), {"in": "glitch"}),
    ("Imagine Earth tilted at just ten degrees.", I("earth-tilt", (.5, .5), 1.0, tz=1.2), {"overlays": [KO(("10°", "yellow"), size=200, dy=-120)], "captions": False}),
    ("Seasons would almost vanish.", V("grass", 1.0, 1.1), {}),
    ("Summer and winter would feel nearly the same.", I("summer-winter", (.5, .5), 1.3, tz=1.0), {}),
    ("Now tilt it to forty five degrees.", I("earth-tilt", (.5, .5), 1.2, tz=1.5), {"in": "flash", "overlays": [KO(("45°", "red"), size=200, dy=-120)],
                                                                                   "captions": False, "shake": ["@forty"]}),
    ("Summers would be scorching,", I("endless-summer", (.5, .4), 1.0, tz=1.3), {}),
    ("winters brutal,", V("snow", 1.0, 1.15), {"in": "cut"}),
    ("and huge parts of the planet would spend months in darkness", I("polar-night", (.5, .5), 1.0, tz=1.3), {}),
    ("or in constant daylight.", V("sun-blaze", 1.0, 1.15), {"in": "flash"}),
    ("Ice ages could come and go in new patterns,", I("ice-age", (.5, .5), 1.0, tz=1.3), {}),
    ("and whole ecosystems would have to move, adapt, or die out.", V("forest-top", 1.0, 1.1), {"overlays": [KO("MOVE.", ("ADAPT.", "yellow"), ("OR DIE OUT.", "red"),
                                                                                                          times=["@move", "@adapt", "@die"], size=110)],
                                                                                         "captions": False, "sfx": [{"name": "pop", "at": "@move"}, {"name": "pop", "at": "@adapt"},
                                                                                                                    {"name": "bass", "at": "@die"}]}),
    ("Mars is a warning.", I("mars-tilt", (.5, .5), 1.0, tz=1.3), {"in": "glitch", "sfx": [{"name": "boom", "at": "@warning", "gain": 0.5}]}),
    ("Its two tiny moons are far too small to steady it,", I("mars-tilt", (.3, .3), 1.5, tz=1.8), {}),
    ("and over millions of years its tilt has swung wildly,", I("mars-tilt", (.6, .55), 1.0, tz=1.3), {"shake": ["@wildly"]}),
    ("possibly beyond sixty degrees.", I("mars-ice", (.5, .5), 1.0, tz=1.3), {"overlays": [KO(("60°+", "red"), times=["@sixty"], size=190)], "captions": False}),
    ("That's one reason Mars has gone through climate swings unlike anything we know.", I("mars-ice", (.6, .55), 1.4, tz=1.8), {}),
    ("But the Moon doesn't just steady how Earth leans.", V("moon-cloud", 1.0, 1.15), {"music_fx": "muffle"}),
    ("It also controls how fast it spins.", V("earth-turn", 2.0, 1.1, drift=0.2), {"in": "flash", "sfx": [{"name": "bass", "at": "@spins"}]}),
]

CH5 = [
    ("Chapter five. The length of a day.", HF("ch5"), {"chapter": True, "music": "intrigue"}),
    ("Here's something strange.", K("SOMETHING", ("STRANGE", "yellow"), times=[0.0, "@strange"]), {}),
    ("A day on Earth hasn't always been twenty four hours long.", V("sunrise", 1.0, 1.1), {"overlays": [KO(("24 H?", "yellow"), times=["@twenty"], size=180)],
                                                                                         "captions": False}),
    ("As the tides drag against the ocean floor,", V("foam", 3.0, 1.15), {}),
    ("they act like a very slow brake on Earth's spin.", V("globe", 3.0, 1.1), {}),
    ("Every century, our day gets about two thousandths of a second longer.", V("hourglass", 1.0, 1.15), {"overlays": [RM("ms2", "@two-0.2")]}),
    ("It doesn't sound like much.", V("clock", 5.0, 1.25), {}),
    ("But over hundreds of millions of years, it adds up.", V("sky-milky", 5.0, 1.1), {}),
    ("When the dinosaurs lived, a day was about twenty three and a half hours,", HF("daylength", 1.2), {"captions": False}),
    ("and a year had around three hundred and seventy days.", I("young-earth", (.5, .5), 1.2, tz=1.0), {"overlays": [RM("d370", "@three-0.2")]}),
    ("One study of ancient rocks found that one point four billion years ago,", I("giant-tide", (.5, .5), 1.0, tz=1.3), {"overlays": [RM("meyers", 0.3)]}),
    ("a day lasted only about eighteen and a half hours.", HF("daylength"), {"captions": False}),
    ("And that energy doesn't just disappear.", V("waves-aerial", 6.0, 1.1), {"in": "glitch"}),
    ("As Earth slows down, the Moon gets pushed farther away.", I("moon-drift", (.6, .5), 1.0, tz=1.35), {"sfx": [{"name": "whoosh2", "at": "@pushed"}]}),
    ("Every year, it drifts about three point eight centimetres further from us.", I("earth-moon", (.4, .5), 1.0, tz=1.2), {"overlays": [RM("cm38", "@three-0.2")]}),
    ("We know this precisely because Apollo astronauts left mirrors on the Moon,", I("retroreflector", (.4, .55), 1.0, tz=1.35), {"overlays": [RM("apollo", "@Apollo")]}),
    ("and scientists still bounce lasers off them today.", I("laser-moon", (.5, .45), 1.0, tz=1.3), {"sfx": [{"name": "zap", "at": "@lasers", "gain": 0.6}]}),
    ("So what happens when the Moon is gone?", I("moon-vanish", (.45, .35), 1.0, tz=1.4), {"in": "glitch", "sfx": [{"name": "glitch-hit"}]}),
    ("The biggest brake on Earth's spin disappears.", V("earth-planet", 4.0, 1.1, drift=0.15), {"sfx": [{"name": "bass", "at": "@disappears"}]}),
    ("The Sun's tides would still slow us down, but far more gently.", V("sun-blaze", 1.0, 1.1), {}),
    ("Our days would almost stop getting longer,", V("sky-trees", 4.0, 1.1), {}),
    ("and twenty four hours would stay twenty four hours for a very, very long time.", K(("24 HOURS", "yellow"), "FOR A VERY, VERY", "LONG TIME",
                                                                                     times=[0.0, "@very", "@long"], size=140), {}),
    ("That sounds like good news.", V("meadow", 3.0, 1.1), {}),
    ("But it makes you wonder what kind of world we'd have", I("earth-alone", (.55, .5), 1.0, tz=1.35), {"in": "glitch"}),
    ("if the Moon had never been there at all.", V("moon-cloud", 4.0, 1.15), {}),
    ("Some scientists think that without the Moon slowing it down,", V("globe", 5.0, 1.2), {}),
    ("Earth could be spinning much faster today, with days far shorter than ours.", V("earth-turn", 4.0, 1.1, rate=1.6), {"sfx": [{"name": "swoosh", "at": "@faster"}]}),
    ("A faster spin could mean stronger winds,", V("reeds", 1.0, 1.15), {}),
    ("wilder storms,", V("storm", 1.0, 1.15), {"in": "cut", "shake": [0.1]}),
    ("and a very different climate.", I("spin-storms", (.5, .5), 1.0, tz=1.3), {"sfx": [{"name": "boom", "at": "@different", "gain": 0.5}]}),
    ("Which brings us to the biggest question of all.", V("moon-cloud2", 4.0, 1.15), {"music_fx": "muffle"}),
]

CH6 = [
    ("Chapter six. A world without a Moon.", HF("ch6"), {"chapter": True, "music": "confident"}),
    ("Think about all the things that would quietly disappear.", V("sky-dusk", 5.0, 1.1), {}),
    ("No more solar eclipses.", I("eclipse", (.5, .4), 1.0, tz=1.3), {"overlays": [RM("noeclipse", 0.2)], "sfx": [{"name": "impact", "at": 0.25, "gain": 0.7}]}),
    ("The Moon is about four hundred times smaller than the Sun,", HF("eclipse400"), {}),
    ("but also about four hundred times closer,", HF("eclipse400", 1.4), {"in": "cut", "captions": False}),
    ("so it fits almost perfectly over it.", I("eclipse", (.5, .4), 1.4, tz=1.8), {}),
    ("Without it, the sky's greatest show is gone forever.", I("eclipse", (.5, .4), 1.1, tz=1.0), {"fx": [{"name": "light_off", "at": "@gone"}]}),
    ("No more lunar eclipses. No more blood Moons.", I("blood-moon", (.5, .3), 1.0, tz=1.3), {"sfx": [{"name": "bass", "at": "@blood"}]}),
    ("Our calendars would lose their anchor too.", I("calendar-moon", (.55, .5), 1.0, tz=1.3), {}),
    ("The word month comes from Moon,", K("MONTH", ("← MOON", "yellow"), times=[0.0, "@Moon"]), {"sfx": [{"name": "pop", "at": "@Moon"}]}),
    ("and Ramadan, Easter, Passover,", V("red-lanterns", 1.0, 1.1), {}),
    ("Diwali and Lunar New Year are all timed by its phases.", I("lanterns", (.5, .4), 1.0, tz=1.3), {}),
    ("But some scientists think the Moon's biggest gift came long before any of that.", I("young-earth", (.5, .45), 1.0, tz=1.3), {"in": "glitch"}),
    ("About four and a half billion years ago,", K(("4.5 BILLION", "yellow"), "YEARS AGO", times=[0.0, "@billion"], size=170), {"in": "dip", "sfx": [{"name": "rewind", "at": 0.0, "gain": 0.6}]}),
    ("a planet roughly the size of Mars is thought to have smashed into the young Earth.", I("theia", (.5, .5), 1.0, tz=1.35),
     {"overlays": [RM("theia", "@planet")], "shake": ["@smashed"], "sfx": [{"name": "boom", "at": "@smashed"}]}),
    ("The debris came together to form the Moon.", I("debris-ring", (.5, .5), 1.0, tz=1.3), {}),
    ("Back then, the Moon was much closer, and its tides were enormous.", I("giant-tide", (.5, .5), 1.0, tz=1.3), {"shake": ["@enormous"]}),
    ("Some researchers think those tides,", I("giant-tide", (.5, .5), 1.2, tz=1.5), {}),
    ("flooding and drying coastal pools again and again,", I("tide-pools-life", (.5, .6), 1.0, tz=1.3), {}),
    ("could have helped the first building blocks of life come together.", I("tide-pools-life", (.5, .7), 1.5, tz=1.9), {"sfx": [{"name": "sparkle", "at": "@life"}]}),
    ("Others think the Moon's steadying pull", I("earth-moon", (.4, .5), 1.0, tz=1.3), {}),
    ("gave life billions of years of fairly stable seasons to evolve.", V("blossom", 1.0, 1.1), {}),
    ("Nobody knows for sure.", K("NOBODY", ("KNOWS FOR SURE", "yellow"), times=[0.0, "@knows"]), {}),
    ("But it's possible that without the Moon, we wouldn't be here to miss it.", V("sky-milky", 8.0, 1.1), {"voice_fx": {"at": "@miss", "fx": "echo"}}),
    ("And here's a myth worth busting.", K("MYTH", ("BUSTED", "red"), times=[0.0, "@busting"]), {"in": "glitch", "sfx": [{"name": "glitch-hit"}]}),
    ("Many people believe the Moon shields us from asteroids.", I("asteroid-moon", (.5, .5), 1.0, tz=1.3), {}),
    ("It doesn't.", I("asteroid-moon", (.4, .5), 1.4, tz=1.6), {"overlays": [RM("myth", 0.0)], "sfx": [{"name": "impact", "at": 0.05}]}),
    ("It's far too small and too far away to block more than a tiny fraction of them.", V("earth-night", 6.0, 1.1), {}),
    ("So, what if the Moon disappeared?", I("moon-city", (.47, .3), 1.3, tz=1.6), {"in": "dip", "pause_before": 0.3, "captions": False, "overlays": [RM("title", 0.2)]}),
    ("The first night would be strangely beautiful, full of stars.", I("milky-way-desert", (.5, .4), 1.0, tz=1.25), {}),
    ("But slowly, the tides would shrink,", V("tide-sunset", 3.0, 1.1), {}),
    ("the animals would lose their clock,", I("coral-spawn", (.5, .5), 1.0, tz=1.3), {}),
    ("and over millions of years, our seasons could start to wobble.", HF("tilt", 3.2), {}),
    ("The good news?", K("THE GOOD", ("NEWS?", "yellow"), times=[0.0, "@news"]), {"music": "warm", "sfx": [{"name": "correct", "at": "@news", "gain": 0.5}]}),
    ("The Moon isn't going anywhere.", V("moon-glow", 6.0, 1.1), {}),
    ("It's drifting away by just a few centimetres a year.", I("moon-drift", (.6, .5), 1.0, tz=1.3), {}),
    ("In about six hundred million years, it will look too small to cover the Sun,", I("moon-small-eclipse", (.5, .4), 1.0, tz=1.3),
     {"overlays": [RM("myr600", "@six-0.2")]}),
    ("and the last total solar eclipse on Earth will happen.", I("eclipse", (.5, .4), 1.0, tz=1.4), {}),
    ("So next time you see the Moon, take a second look.", I("moonrise-ocean", (.5, .45), 1.0, tz=1.3), {}),
    ("It's been holding our world together all along.", I("earth-moon", (.4, .55), 1.3, tz=1.0), {"captions": False, "overlays": [RM("together", 0.2, hold=True)],
                                                                                              "sfx": [{"name": "bass", "at": "@together"}]}),
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
    spec = {"out": "../output/moon-full.mp4", "audio": [f"chapters/take{i}.wav" for i in range(1, 10)], "take_gap": 0.4, "speed": 0.94,
            "music_cues": cues, "music_volume": 0.38, "fade_out": 2.5, "progress": True, "shots": shots}
    (HERE / "video.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False))
    n_img = sum(1 for s in shots if kind(s["v"]) == "img")
    n_vid = sum(1 for s in shots if kind(s["v"]) == "video")
    n_ov = sum(1 for s in shots for o in s.get("overlays", []) if o["mg"] == "clip")
    print(f"{len(shots)} shots: {n_img} AI images, {n_vid} stock videos, {len(shots) - n_img - n_vid} motion-graphic shots, "
          f"{n_ov} Remotion overlays; {len(cues)} music cues")


if __name__ == "__main__":
    main()
