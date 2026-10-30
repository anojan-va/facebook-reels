"""Build video.json for "What if you lived on Mars for a year?" (~11 min, comedic second-person story, same editing style).

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
          "punchy": ("../../reels/audio/music/trapanomics.mp3", 0.0, 0.56),
          "tense": ("../../reels/audio/music/out-of-this-world.mp3", 117.26, 1.0),
          "sad": ("../../reels/audio/music/silent-descent.mp3", 0.0, 0.62),
          "confident": ("../../reels/audio/music/unforgiven.mp3", 13.63, 1.0),
          "warm": ("../../reels/audio/music/fifth-of-february.mp3", 1.6, 1.15)}

CH1 = [
    ("Congratulations.", V("balloons", 1.0, 1.2), {"punch": True, "sfx": ["hook", {"name": "sparkle", "at": 0.2}]}),
    ("You just signed up to live on Mars for one whole year.", V("mars-globe", 1.0, 1.1, drift=0.12),
     {"captions": False, "overlays": [RM("title", 0.0)], "sfx": [{"name": "boom", "at": "@Mars", "gain": 0.5}]}),
    ("You clicked \"I agree\" without reading the terms and conditions.", I("contract", (.45, .55), 1.0, to=(.5, .65), tz=1.5),
     {"sfx": [{"name": "click", "at": "@agree"}]}),
    ("Classic you.", I("contract", (.5, .65), 1.6, tz=1.9), {"in": "cut", "captions": False, "overlays": [RM("classic", 0.0)],
                                                             "sfx": [{"name": "scratch", "at": 0.0, "gain": 0.6}]}),
    ("Don't worry. I read them.", V("suitcase-pack", 1.0, 1.15), {}),
    ("And I'm going to walk you through every single day of it,", V("mars-astros", 1.0, 1.1), {}),
    ("the beautiful parts,", I("blue-sunset", (.5, .5), 1.0, tz=1.25), {"in": "cut", "sfx": [{"name": "sparkle"}]}),
    ("the terrifying parts,", I("storm-coming", (.5, .5), 1.0, tz=1.3), {"in": "glitch", "shake": [0.1]}),
    ("and the part where you find out what a \"year\" on Mars actually means.", HF("year"), {}),
    ("Spoiler: it's not what you think.", K("SPOILER:", ("IT'S NOT WHAT YOU THINK", "yellow"), times=[0.0, "@not"], size=120),
     {"sfx": [{"name": "glitch-hit", "at": 0.0}]}),
    ("Oh, and a few house rules before we leave.", I("hab-inside", (.5, .5), 1.0, tz=1.2), {"music": "warm"}),
    ("No pets.", I("space-dog", (.5, .45), 1.2, tz=1.5), {"in": "cut", "overlays": [KO(("NO PETS", "red"), size=150)], "captions": False,
                                                          "sfx": [{"name": "wrong", "at": 0.05, "gain": 0.4}]}),
    ("No pizza delivery.", V("mars-base", 1.0, 1.15), {"in": "cut", "overlays": [KO(("NO PIZZA DELIVERY", "red"), size=130)],
                                                                                  "captions": False, "sfx": [{"name": "wrong", "at": 0.05, "gain": 0.4}]}),
    ("And no complaining.", I("hab-outside", (.5, .5), 1.1, tz=1.3), {"in": "cut", "overlays": [KO(("NO COMPLAINING", "red"), size=130)], "captions": False,
                                                                     "sfx": [{"name": "wrong", "at": 0.05, "gain": 0.4}]}),
    ("Okay, complaining is allowed.", I("mars-plain", (.5, .5), 1.0, tz=1.15), {}),
    ("Nobody can hear you anyway.", I("mars-plain", (.5, .5), 1.4, tz=1.8), {"voice_fx": {"at": "@anyway", "fx": "echo"}}),
    ("Day zero. Launch day.", HF("ch1"), {"chapter": True, "music": "punchy"}),
    ("You're strapped into a seat on top of a rocket", I("g-force", (.5, .5), 1.0, tz=1.25), {}),
    ("that is basically a skyscraper full of fuel.", I("launch", (.5, .6), 1.0, to=(.5, .35), tz=1.4), {"sfx": [{"name": "boom", "at": "@fuel", "gain": 0.5}]}),
    ("Someone counts down from ten.", V("shuttle-launch2", 0.5, 1.1), {"sfx": [{"name": "tick", "at": 0.2}, {"name": "tick", "at": 0.7}, {"name": "tick", "at": 1.2}]}),
    ("Your heart counts down faster.", I("g-force", (.55, .35), 1.6, tz=2.0), {"sfx": [{"name": "heartbeat", "at": 0.1}, {"name": "heartbeat", "at": 0.5}, {"name": "heartbeat", "at": 0.9}]}),
    ("Then it feels like an elephant sits on your chest.", V("shuttle-launch", 2.0, 1.15), {"shake": [0.1, "@elephant"], "sfx": [{"name": "boom", "at": "@elephant"}]}),
    ("A friendly elephant.", I("g-force", (.5, .45), 1.3, tz=1.6), {"in": "cut", "sfx": [{"name": "pop", "at": "@friendly"}]}),
    ("But still an elephant.", I("g-force", (.5, .4), 1.8, tz=2.2), {"in": "cut", "shake": [0.05]}),
    ("Eight minutes later, you're in space.", V("iss", 1.0, 1.1), {"overlays": [TAG("+ 00:08:00")]}),
    ("Congratulations again.", V("balloons", 4.0, 1.2), {"in": "cut", "sfx": [{"name": "sparkle"}]}),
    ("Now the boring part starts.", I("cramped", (.5, .5), 1.0, tz=1.2), {"sfx": [{"name": "scratch", "at": "@boring", "gain": 0.5}]}),
    ("Because Mars is not next door.", V("mars-globe2", 1.0, 1.1), {}),
    ("Depending on where the planets are, the trip takes around seven months.", I("orbits", (.5, .5), 1.0, tz=1.25),
     {"overlays": [RM("months7", "@seven-0.2")]}),
    ("Seven months in a spaceship the size of a small apartment,", I("cramped", (.5, .5), 1.3, tz=1.0), {}),
    ("with the same few people, the same food, and the same smell.", V("iss2", 1.0, 1.15),
     {"overlays": [KO("SAME PEOPLE.", "SAME FOOD.", ("SAME SMELL.", "yellow"), times=["@people", "@food", "@smell"], size=110)], "captions": False,
      "sfx": [{"name": "pop", "at": "@people"}, {"name": "pop", "at": "@food"}, {"name": "wrong", "at": "@smell", "gain": 0.4}]}),
    ("Your water? Recycled.", I("recycler", (.5, .5), 1.0, tz=1.3), {"sfx": [{"name": "tick", "at": "@Recycled"}]}),
    ("On the space station, almost all of the water, including sweat and urine,", V("iss", 6.0, 1.1), {}),
    ("gets cleaned and turned back into drinking water.", I("recycler", (.55, .55), 1.5, tz=1.9), {}),
    ("So yes.", I("coffee", (.5, .5), 1.0, tz=1.2), {"in": "cut"}),
    ("Today's coffee is yesterday's coffee.", I("coffee", (.5, .45), 1.4, tz=1.9), {"punch": {"at": "@yesterday", "zoom": 2.0}, "sfx": [{"name": "scratch", "at": "@yesterday", "gain": 0.5}]}),
    ("Don't think about it too much.", V("coffee-pour", 1.0, 1.15), {}),
    ("You float.", V("spacewalk", 1.0, 1.15), {"in": "cut"}),
    ("You exercise for two hours a day so your muscles don't melt.", I("space-treadmill", (.5, .5), 1.0, tz=1.3), {}),
    ("You watch every movie you downloaded.", I("laptop", (.5, .5), 1.0, tz=1.2), {}),
    ("Twice.", I("laptop", (.55, .45), 1.7, tz=2.0), {"in": "cut", "sfx": [{"name": "pop"}]}),
    ("And Earth slowly shrinks behind you,", I("earth-window", (.5, .5), 1.0, tz=1.3), {"music": "intrigue"}),
    ("from a big blue marble, to a bright blue dot, to just another star.", V("earth-planet", 1.0, 1.1, drift=0.25), {}),
    ("Then one morning, a red dot outside the window starts getting bigger.", I("mars-window", (.5, .5), 1.0, tz=1.3), {}),
    ("And bigger.", I("mars-window", (.4, .5), 1.6, tz=2.0), {"in": "cut", "sfx": [{"name": "riser", "at": 0.6}]}),
    ("It's time to land.", V("mars-globe", 6.0, 1.3), {"sfx": [{"name": "bass", "at": "@land"}]}),
]

CH2 = [
    ("Day one. Welcome to Mars.", HF("ch2"), {"chapter": True, "music": "tense"}),
    ("Landing on Mars has been called seven minutes of terror.", I("entry", (.5, .5), 1.0, tz=1.3), {"overlays": [TAG("7 MINUTES OF TERROR")]}),
    ("You hit the atmosphere at thousands of kilometres an hour,", I("entry", (.5, .45), 1.4, tz=1.8), {"shake": ["@atmosphere"]}),
    ("and you have to stop completely before you hit the ground.", V("mars-canyon", 1.0, 1.15, drift=0.15), {}),
    ("Heat shield.", I("entry", (.5, .4), 1.6, tz=1.9), {"in": "cut", "sfx": [{"name": "impact", "gain": 0.5}]}),
    ("Parachute.", I("parachute", (.5, .4), 1.0, tz=1.3), {"in": "cut", "sfx": [{"name": "whoosh2"}]}),
    ("Rockets.", I("touchdown", (.5, .5), 1.0, tz=1.3), {"in": "cut", "sfx": [{"name": "boom", "gain": 0.6}]}),
    ("Thud.", I("touchdown", (.5, .6), 1.5, tz=1.5, drift=0), {"in": "cut", "shake": [0.0], "sfx": [{"name": "impact"}]}),
    ("You made it.", V("mars-haze", 1.0, 1.15), {"music": "warm", "sfx": [{"name": "correct", "at": 0.2, "gain": 0.5}]}),
    ("And the first thing you notice is that you feel amazing.", I("jump", (.5, .5), 1.0, tz=1.2), {}),
    ("Mars has only about thirty eight percent of Earth's gravity.", V("mars-astros", 3.0, 1.1), {"overlays": [RM("g38", "@thirty-0.2")]}),
    ("If you weigh seventy kilos at home, here you feel like you weigh about twenty seven.", HF("weight"), {"captions": False}),
    ("You could jump almost three times higher.", I("jump", (.5, .4), 1.2, to=(.5, .25), tz=1.5), {"sfx": [{"name": "swoosh", "at": "@jump"}]}),
    ("You could carry your friend like a backpack.", I("piggyback", (.5, .5), 1.0, tz=1.3), {}),
    ("You will absolutely try both on day one.", I("piggyback", (.5, .4), 1.5, tz=1.8), {"sfx": [{"name": "pop", "at": "@both"}]}),
    ("Your first walk outside won't look like a brave astronaut.", V("moonwalk", 1.0, 1.1), {}),
    ("It will look like a toddler on a trampoline.", I("faceplant", (.5, .55), 1.0, tz=1.35), {"punch": {"at": "@trampoline", "zoom": 1.7, "focus": [.45, .6]},
                                                                                           "sfx": [{"name": "scratch", "at": "@trampoline", "gain": 0.5}]}),
    ("That's normal.", I("faceplant", (.45, .6), 1.7, tz=1.9), {"in": "cut"}),
    ("The Apollo astronauts on the Moon fell over all the time too.", V("moonwalk", 6.0, 1.15), {}),
    ("Then you look outside, and you remember why you can't just open the door.", I("airlock", (.5, .5), 1.0, tz=1.3), {"music": "tense"}),
    ("The air on Mars is about ninety five percent carbon dioxide,", V("mars-haze", 4.0, 1.1), {"overlays": [RM("co2", "@ninety-0.2")]}),
    ("and it's incredibly thin.", I("mars-plain", (.5, .5), 1.2, tz=1.0), {}),
    ("Less than one percent of the air pressure we have on Earth.", V("red-rocks", 1.0, 1.1), {"overlays": [RM("pressure", "@one-0.2")]}),
    ("So here's your first rule of Mars.", K("RULE", ("NUMBER ONE", "yellow"), times=[0.0, "@first"]), {"sfx": [{"name": "bass", "at": "@rule"}]}),
    ("Never, ever take your helmet off.", I("frost-helmet", (.5, .5), 1.0, tz=1.4), {"overlays": [RM("helmet", "@helmet-0.2")], "sfx": [{"name": "impact", "at": "@helmet"}]}),
    ("If you did, you'd have about fifteen seconds before you passed out.", I("frost-helmet", (.5, .45), 1.4, tz=1.8),
     {"overlays": [RM("sec15", "@fifteen-0.2")], "sfx": [{"name": "heartbeat", "at": 0.2}]}),
    ("The saliva on your tongue would start to boil.", V("red-dust", 1.0, 1.2), {"in": "glitch"}),
    ("Not because it's hot, but because the pressure is so low.", I("mars-plain", (.6, .5), 1.4, tz=1.7), {}),
    ("And it is not hot.", K("IT IS", ("NOT HOT", "yellow"), times=[0.0, "@not"]), {}),
    ("The average temperature on Mars is around minus sixty degrees Celsius.", V("mars-canyon", 4.0, 1.1), {"overlays": [RM("minus60", "@minus-0.2")]}),
    ("On a nice summer afternoon near the equator, it can reach twenty degrees.", I("sol-sunrise", (.5, .5), 1.0, tz=1.25),
     {"overlays": [KO(("+20 °C", "yellow"), times=["@twenty"], size=170)], "captions": False}),
    ("That same night, it drops to minus seventy.", I("frost-helmet", (.5, .55), 1.2, tz=1.5), {"in": "flash",
                                                                                                "overlays": [KO(("−70 °C", "white"), times=["@minus"], size=170)], "captions": False}),
    ("So the forecast for your first day:", K("TODAY'S", ("FORECAST", "yellow"), times=[0.0, "@forecast"]), {"music": "warm"}),
    ("sunny, with a chance of instant death.", I("mars-plain", (.5, .4), 1.0, tz=1.3),
     {"overlays": [KO("SUNNY ☀", ("CHANCE OF INSTANT DEATH", "red"), times=[0.0, "@chance"], size=110)], "captions": False,
      "sfx": [{"name": "scratch", "at": "@death", "gain": 0.5}]}),
    ("But then you look up, and you forget all of that for a second.", V("dune-crest", 1.0, 1.1), {}),
    ("The sky is not blue.", I("mars-plain", (.5, .2), 1.4, tz=1.6), {}),
    ("It's a dusty, butterscotch kind of orange.", V("mars-haze", 7.0, 1.15), {}),
    ("And when the sun sets, the sky around it turns blue.", I("blue-sunset", (.5, .45), 1.0, tz=1.35), {"overlays": [RM("sunset", 0.2)], "sfx": [{"name": "reveal", "at": "@blue"}]}),
    ("Mars has blue sunsets.", I("blue-sunset", (.5, .4), 1.5, tz=1.9), {"voice_fx": {"at": "@sunsets", "fx": "echo"}}),
    ("You're the first person in your family to see one.", I("final-sunset", (.5, .5), 1.0, tz=1.25), {}),
    ("Take a picture.", I("selfie", (.55, .45), 1.0, tz=1.3), {"in": "cut", "sfx": [{"name": "shutter", "at": "@picture"}]}),
    ("Nobody back home will believe you.", I("selfie", (.45, .4), 1.5, tz=1.8), {"in": "flash"}),
]

CH3 = [
    ("Week one. Your new home.", HF("ch3"), {"chapter": True, "music": "warm"}),
    ("Your house is called a habitat.", I("hab-outside", (.5, .5), 1.0, tz=1.3), {"overlays": [TAG("YOUR HOUSE")]}),
    ("Think of a tiny, very expensive tent that is trying very hard to keep you alive.", I("hab-inside", (.5, .5), 1.0, tz=1.3), {}),
    ("It holds the air you breathe, the water you drink,", I("hab-inside", (.6, .4), 1.5, tz=1.8), {}),
    ("and the warmth that stops you from becoming a popsicle.", I("frost-helmet", (.5, .5), 1.2, tz=1.5), {"sfx": [{"name": "glass", "at": "@popsicle", "gain": 0.5}]}),
    ("So where does the oxygen come from?", K("WHERE DOES THE", ("OXYGEN", "yellow"), "COME FROM?", times=[0.0, "@oxygen", "@come"], size=130), {}),
    ("Mars has plenty of oxygen.", V("mars-globe2", 3.0, 1.1), {}),
    ("It's just stuck inside carbon dioxide.", V("red-dust", 3.0, 1.15), {}),
    ("So you split it.", K(("CO₂", "white"), ("→  C + O₂", "yellow"), times=[0.0, "@split"], size=170), {"sfx": [{"name": "zap", "at": "@split", "gain": 0.6}]}),
    ("NASA already tested this.", V("mars-base", 3.0, 1.1), {}),
    ("A machine called MOXIE, about the size of a lunchbox,", I("moxie", (.5, .5), 1.0, tz=1.35), {"overlays": [RM("moxie", "@MOXIE")]}),
    ("rode to Mars on the Perseverance rover and pulled oxygen out of the Martian air.", I("rover-dust", (.5, .55), 1.0, tz=1.25), {}),
    ("In total, it made about a hundred and twenty two grams.", I("moxie", (.55, .45), 1.4, tz=1.7), {"overlays": [RM("g122", "@hundred-0.2")]}),
    ("NASA said that's roughly what a small dog breathes in ten hours.", I("space-dog", (.5, .45), 1.0, tz=1.4), {"sfx": [{"name": "pop", "at": "@dog"}]}),
    ("So the technology works.", V("mars-base", 6.0, 1.15), {"sfx": [{"name": "correct", "at": "@works", "gain": 0.5}]}),
    ("You just need a much bigger machine.", I("moxie", (.5, .5), 1.0, tz=1.2), {}),
    ("Or a much smaller dog.", I("space-dog", (.5, .4), 1.7, tz=2.1), {"in": "cut", "punch": {"at": "@smaller", "zoom": 2.4}, "sfx": [{"name": "scratch", "at": "@dog", "gain": 0.5}]}),
    ("Next problem. Food.", K("NEXT PROBLEM:", ("FOOD", "yellow"), times=[0.0, "@Food"]), {"sfx": [{"name": "bass", "at": "@Food"}]}),
    ("You'll be growing some of it yourself, in a greenhouse with special lights.", I("greenhouse", (.5, .5), 1.0, tz=1.3), {}),
    ("Lettuce, radishes, and yes, potatoes.", I("potatoes", (.5, .5), 1.0, tz=1.4), {"sfx": [{"name": "pop", "at": "@potatoes"}]}),
    ("But you can't just plant them in Martian dirt.", V("red-rocks", 4.0, 1.15), {"in": "glitch"}),
    ("The soil contains chemicals called perchlorates, which are toxic to humans.", I("soil-lab", (.5, .5), 1.0, tz=1.3), {"overlays": [RM("toxic", "@toxic-0.2")]}),
    ("You'd have to wash the soil first, or grow everything in water.", I("potatoes", (.6, .6), 1.4, tz=1.8), {}),
    ("Farming on Mars is less \"peaceful countryside\"", V("lettuce-wash", 1.0, 1.15), {}),
    ("and more \"chemistry exam you can eat.\"", I("soil-lab", (.45, .55), 1.6, tz=2.0), {"in": "cut", "sfx": [{"name": "scratch", "at": "@chemistry", "gain": 0.5}]}),
    ("And then there's the dust.", V("red-dust", 6.0, 1.2), {"in": "glitch", "sfx": [{"name": "bass", "at": "@dust"}]}),
    ("Martian dust is finer than flour, it's a little bit toxic, and it sticks to everything.", V("dust-gold", 1.0, 1.15), {}),
    ("Your suit.", I("dusty-suit", (.5, .55), 1.0, tz=1.2), {"in": "cut", "sfx": [{"name": "pop"}]}),
    ("Your boots.", I("dusty-suit", (.5, .85), 1.8, tz=2.0), {"in": "cut", "sfx": [{"name": "pop"}]}),
    ("Your hair.", I("dusty-suit", (.5, .25), 2.0, tz=2.2), {"in": "cut", "sfx": [{"name": "pop"}]}),
    ("Your soul.", I("dusty-suit", (.5, .4), 2.6, tz=3.0), {"in": "cut", "voice_fx": {"at": "@soul", "fx": "echo"}, "sfx": [{"name": "bass"}]}),
    ("You will clean the airlock every single day,", I("dust-airlock", (.5, .5), 1.0, tz=1.3), {}),
    ("and you will still find red dust in places you didn't know you had.", I("dust-airlock", (.35, .6), 1.6, tz=2.0), {}),
    ("And showers? Water is far too precious.", V("lettuce-wash", 5.0, 1.15), {}),
    ("You get a quick wipe with a wet cloth.", I("hab-inside", (.4, .6), 1.4, tz=1.7), {}),
    ("Your crew will smell you before they see you.", I("cards", (.5, .5), 1.0, tz=1.3), {"sfx": [{"name": "wrong", "at": "@smell", "gain": 0.4}]}),
    ("And you will smell them.", I("cards", (.4, .5), 1.6, tz=1.9), {"in": "cut"}),
    ("Teamwork.", K(("TEAMWORK.", "yellow"), size=180), {"in": "cut", "sfx": [{"name": "correct", "gain": 0.5}]}),
    ("By the end of week one, you've learned three things.", I("hab-outside", (.5, .5), 1.2, tz=1.0), {}),
    ("Breathing is a team effort.", K("1.", ("BREATHING = TEAM EFFORT", "yellow"), times=[0.0, 0.1], size=120), {"sfx": [{"name": "pop"}]}),
    ("Potatoes are precious.", K("2.", ("POTATOES = PRECIOUS", "yellow"), times=[0.0, 0.1], size=120), {"in": "cut", "sfx": [{"name": "pop"}]}),
    ("And the dust always wins.", K("3.", ("THE DUST ALWAYS WINS", "red"), times=[0.0, 0.1], size=120), {"in": "cut", "sfx": [{"name": "bass", "at": "@wins"}]}),
]

CH4 = [
    ("Month three. The weird new normal.", HF("ch4"), {"chapter": True, "music": "intrigue"}),
    ("By now you've noticed your days are a little longer.", I("sol-sunrise", (.5, .5), 1.0, tz=1.3), {}),
    ("A day on Mars is called a sol, and it lasts twenty four hours and thirty nine minutes.", HF("sol"), {"captions": False}),
    ("That doesn't sound like much.", V("clock2", 1.0, 1.15), {}),
    ("But every single day, you get almost forty extra minutes.", HF("sol", 2.4), {"in": "cut"}),
    ("On Mars, you can finally hit snooze without feeling guilty.", I("hab-inside", (.35, .55), 1.5, tz=1.8), {"sfx": [{"name": "click", "at": "@snooze"}]}),
    ("At night, you look up and see not one moon, but two.", I("two-moons", (.5, .4), 1.0, tz=1.3), {"sfx": [{"name": "pop", "at": "@one"}, {"name": "pop", "at": "@two"}]}),
    ("Phobos and Deimos.", I("two-moons", (.55, .35), 1.6, tz=1.9), {"in": "cut", "overlays": [RM("moons", 0.1)]}),
    ("They're tiny, potato shaped rocks.", I("phobos", (.55, .5), 1.0, tz=1.4), {"sfx": [{"name": "pop", "at": "@potato"}]}),
    ("And Phobos is so fast that it rises in the west,", V("star-trails", 1.0, 1.1), {}),
    ("races across the sky, and sets in the east, about twice every sol.", V("milkyway2", 1.0, 1.1, drift=0.15), {"sfx": [{"name": "swoosh-fast", "at": "@races"}]}),
    ("Even the moon here is in a hurry.", I("phobos", (.6, .5), 1.6, tz=2.0), {"in": "cut"}),
    ("And it won't last forever.", I("phobos", (.5, .5), 1.2, tz=1.0), {"in": "glitch"}),
    ("Phobos is slowly spiralling down toward Mars.", V("mars-globe", 3.0, 1.2, drift=0.15), {}),
    ("In tens of millions of years, it will be ripped apart,", I("phobos-ring", (.5, .5), 1.0, tz=1.3), {"sfx": [{"name": "glass", "at": "@ripped", "gain": 0.5}]}),
    ("and it may turn into a ring around the planet.", I("phobos-ring", (.4, .45), 1.5, tz=1.8), {}),
    ("You try to call your mom.", I("laptop", (.5, .5), 1.0, tz=1.3), {"music": "warm"}),
    ("Bad idea.", K(("BAD IDEA.", "red"), size=180), {"in": "cut", "sfx": [{"name": "wrong", "gain": 0.4}]}),
    ("Radio signals between Earth and Mars take anywhere from about three to twenty two minutes, one way.", HF("delay"), {"captions": False}),
    ("So you say, \"Hi mom!\" and then you wait.", I("laptop", (.55, .45), 1.4, tz=1.7), {}),
    ("And wait.", I("laptop", (.6, .4), 2.0, tz=2.2), {"in": "cut", "sfx": [{"name": "tick", "at": 0.1}, {"name": "tick", "at": 0.6}]}),
    ("Twenty minutes later, you hear, \"Hi sweetie, can you hear me?\"", I("dish", (.5, .5), 1.0, tz=1.3), {"overlays": [TAG("+ 00:20:00")]}),
    ("Video calls are impossible.", V("dish-vla", 1.0, 1.15), {"overlays": [KO(("VIDEO CALLS", "white"), ("IMPOSSIBLE", "red"), times=[0.0, "@impossible"], size=120)],
                                                              "captions": False}),
    ("Texting is the only way.", I("laptop", (.5, .55), 1.2, tz=1.5), {}),
    ("You are now basically sending letters, but faster.", V("star-trails", 5.0, 1.15), {}),
    ("And then there's something you can't see at all. Radiation.", I("radiation", (.5, .5), 1.0, tz=1.3), {"music": "tense", "in": "glitch",
                                                                                                           "sfx": [{"name": "zap", "at": "@Radiation", "gain": 0.6}]}),
    ("Mars has no global magnetic field and a very thin atmosphere,", V("mars-globe2", 6.0, 1.15), {}),
    ("so far more radiation reaches the ground than on Earth.", I("radiation", (.5, .6), 1.4, tz=1.8), {}),
    ("NASA's Curiosity rover measured it.", I("rover-dust", (.5, .5), 1.0, tz=1.3), {"overlays": [RM("curiosity", 0.1)]}),
    ("Every day on the surface, you get roughly as much radiation as dozens of chest X rays.", V("xray-lungs", 1.0, 1.1), {}),
    ("That's why the smart move is to live underground,", I("underground", (.5, .5), 1.0, tz=1.3), {}),
    ("or to cover your habitat with a thick blanket of Martian soil.", I("hab-outside", (.5, .55), 1.4, tz=1.7), {}),
    ("Then one day, the sky turns brown.", I("storm-coming", (.5, .4), 1.0, tz=1.2), {"in": "glitch", "sfx": [{"name": "boom", "at": "@brown", "gain": 0.5}]}),
    ("A dust storm is coming.", I("storm-coming", (.6, .5), 1.4, tz=1.8), {"shake": ["@storm"]}),
    ("Some of them grow so big they cover the entire planet for weeks.", V("mars-globe", 9.0, 1.1), {}),
    ("In twenty eighteen, one of those storms blocked out so much sunlight", I("dark-panels", (.5, .5), 1.0, tz=1.3), {"overlays": [RM("opportunity", 0.2)]}),
    ("that NASA's Opportunity rover ran out of power, and it never woke up again.", I("rover-dust", (.45, .55), 1.4, tz=1.8),
     {"fx": [{"name": "light_off", "at": "@never"}], "sfx": [{"name": "switch", "at": "@never"}], "voice_fx": {"at": "@again", "fx": "echo"}}),
]

CH5 = [
    ("But here's a myth worth busting.", K("MYTH", ("BUSTED", "red"), times=[0.0, "@busting"]), {"in": "glitch", "music": "warm", "sfx": [{"name": "glitch-hit"}]}),
    ("In movies, Mars storms blow astronauts off their feet.", I("storm-coming", (.4, .5), 1.0, tz=1.3), {}),
    ("In real life, the air is so thin that even a fast wind would feel like a gentle breeze.", I("breeze", (.5, .5), 1.0, tz=1.35),
     {"overlays": [RM("myth", "@gentle-0.3")], "sfx": [{"name": "impact", "at": "@gentle", "gain": 0.6}]}),
    ("The real danger isn't the wind. It's the darkness.", I("dark-panels", (.5, .5), 1.2, tz=1.5), {"fx": [{"name": "light_off", "at": "@darkness"}]}),
    ("Your solar panels go dark, and your power starts to drop.", I("dark-panels", (.55, .6), 1.6, tz=1.9), {"sfx": [{"name": "switch", "at": "@dark"}]}),
    ("So you turn off everything you don't need, you wrap yourself in a blanket,", I("hab-inside", (.5, .5), 1.1, tz=1.4), {}),
    ("and you wait it out with your crew, playing the same card game for the hundredth time.", I("cards", (.5, .5), 1.0, tz=1.3), {}),
    ("Month seven. The loneliness hits.", HF("ch5"), {"chapter": True, "music": "sad"}),
    ("Scientists actually tested this.", V("control-room2", 1.0, 1.15), {}),
    ("In a project called Mars five hundred,", I("mars500", (.5, .5), 1.0, tz=1.3), {"overlays": [RM("mars500", 0.1)]}),
    ("six men lived sealed inside a fake spaceship in Moscow for five hundred and twenty days.", I("mars500", (.6, .5), 1.4, tz=1.8),
     {"overlays": [RM("days520", "@five-0.2")]}),
    ("Some of them started sleeping more, moving less, and drifting onto their own schedules.", V("clock2", 4.0, 1.2), {}),
    ("So you make rules.", K("SO YOU MAKE", ("RULES", "yellow"), times=[0.0, "@rules"]), {"music": "warm"}),
    ("Exercise every day.", I("mars-treadmill", (.5, .5), 1.0, tz=1.25), {"in": "cut", "sfx": [{"name": "pop"}]}),
    ("Eat together.", I("cards", (.5, .5), 1.2, tz=1.4), {"in": "cut", "sfx": [{"name": "pop"}]}),
    ("Celebrate everything.", V("balloons", 6.0, 1.15), {"in": "cut", "sfx": [{"name": "sparkle"}]}),
    ("Somebody's birthday? Party.", V("candles", 1.0, 1.15), {"in": "cut", "overlays": [KO(("PARTY!", "yellow"), times=["@Party"], size=170)], "captions": False}),
    ("Tuesday? Party.", V("cake", 1.0, 1.15), {"in": "cut", "overlays": [KO(("PARTY!", "yellow"), times=["@Party"], size=170)], "captions": False}),
    ("Found a nice rock? Party.", I("party", (.5, .55), 1.0, tz=1.4), {"in": "cut", "overlays": [KO(("PARTY!", "yellow"), times=["@Party"], size=170)], "captions": False,
                                                                       "punch": {"at": "@rock", "zoom": 1.8, "focus": [.53, .6]}}),
    ("Someone always cheats at cards.", V("cards-deal", 1.0, 1.15), {}),
    ("And on Mars, there's nowhere to storm off to.", I("mars-plain", (.5, .5), 1.0, tz=1.4), {"sfx": [{"name": "scratch", "at": "@storm", "gain": 0.5}]}),
    ("Your body is changing too.", I("mars-treadmill", (.5, .4), 1.4, tz=1.6), {"music": "sad"}),
    ("In lower gravity, your muscles and bones don't have to work as hard, so they slowly get weaker.", V("xray-lungs", 4.0, 1.15), {}),
    ("On the space station, astronauts can lose about one percent of the bone in their hips and legs every month if they don't exercise.",
     V("iss2", 4.0, 1.1), {"overlays": [RM("pct1", "@one-0.2")]}),
    ("So you run on the treadmill. A lot.", I("mars-treadmill", (.5, .5), 1.0, tz=1.3), {}),
    ("Strapped down with bungee cords, so you don't bounce off it.", I("space-treadmill", (.5, .55), 1.3, tz=1.7), {"sfx": [{"name": "pop", "at": "@bounce"}]}),
    ("Then, one clear evening, you climb a hill and look up, and there it is.", I("earth-dot", (.5, .55), 1.0, to=(.5, .3), tz=1.3), {}),
    ("A tiny bright dot in the sky. That's Earth.", I("earth-dot", (.45, .2), 2.0, tz=2.6), {"sfx": [{"name": "sparkle", "at": "@Earth"}]}),
    ("Everyone you've ever known is on that dot.", I("earth-dot", (.5, .45), 1.2, tz=1.0), {"music_fx": "muffle"}),
    ("And for a moment, it's very quiet.", V("milkyway2", 6.0, 1.1), {"music_fx": "muffle"}),
    ("Then your crewmate says, \"Hey, the potatoes are ready,\" and life goes on.", I("potatoes", (.5, .5), 1.0, tz=1.3), {"in": "flash", "music": "warm",
                                                                                                                          "sfx": [{"name": "pop", "at": "@potatoes"}]}),
]

CH6 = [
    ("Month ten. The big trip.", HF("ch6"), {"chapter": True, "music": "confident"}),
    ("You've been saving up for this.", I("hab-outside", (.5, .5), 1.0, tz=1.2), {}),
    ("A road trip to the biggest volcano in the solar system.", I("rover-trip", (.5, .55), 1.0, tz=1.3), {"sfx": [{"name": "whoosh", "at": "@road"}]}),
    ("Olympus Mons.", I("olympus-orbit", (.5, .5), 1.0, tz=1.3), {"in": "cut", "overlays": [RM("olympus", 0.0)], "sfx": [{"name": "boom", "gain": 0.5}]}),
    ("It's about twenty two kilometres tall, roughly two and a half times the height of Mount Everest,", HF("olympus"), {"captions": False}),
    ("and about as wide as the state of Arizona.", I("olympus-orbit", (.5, .5), 1.4, tz=1.0), {}),
    ("Here's the funny part.", K("HERE'S THE", ("FUNNY PART", "yellow"), times=[0.0, "@funny"]), {}),
    ("It's so wide and the slope is so gentle that if you stood on top,", I("olympus-top", (.5, .5), 1.0, tz=1.25), {}),
    ("you might not even realise you're on a mountain.", I("olympus-top", (.5, .45), 1.4, tz=1.7), {}),
    ("The edges would be hidden beyond the horizon.", V("dune-crest", 3.0, 1.1), {}),
    ("The tallest mountain in the solar system, and it looks like a really long hill.", I("olympus-top", (.5, .5), 1.2, tz=1.0), {"sfx": [{"name": "scratch", "at": "@hill", "gain": 0.5}]}),
    ("Classic Mars.", K("CLASSIC", ("MARS.", "red"), times=[0.0, "@Mars"]), {"in": "cut"}),
    ("Day three hundred and sixty five. Your year is finally up.", HF("ch7"), {"chapter": True, "music": "warm"}),
    ("You pack your bags.", V("suitcase-pack", 3.0, 1.15), {}),
    ("You say goodbye to the potatoes.", I("potatoes", (.5, .5), 1.2, tz=1.5), {"sfx": [{"name": "sparkle", "at": "@goodbye"}]}),
    ("You walk to the ship.", I("packing", (.5, .5), 1.0, tz=1.3), {}),
    ("And mission control says, \"Where do you think you're going?\"", I("mission-control", (.5, .5), 1.0, tz=1.3),
     {"overlays": [RM("nope", "@Where")], "sfx": [{"name": "scratch", "at": "@Where", "gain": 0.6}], "music_fx": "muffle"}),
    ("Remember the terms and conditions? Here's the fine print.", I("contract", (.5, .6), 1.2, tz=1.8), {"in": "glitch", "fx": ["vhs"],
                                                                                                        "overlays": [TAG("◀◀ REWIND  DAY 0")], "sfx": [{"name": "rewind"}]}),
    ("A year on Mars is not three hundred and sixty five days.", HF("year"), {"captions": False}),
    ("It takes Mars six hundred and eighty seven Earth days to go around the Sun.", HF("year", 2.0), {"in": "cut", "captions": False,
                                                                                                      "sfx": [{"name": "bass", "at": "@six"}]}),
    ("So technically, you're only halfway through your Martian year.", I("unpacking", (.5, .5), 1.0, tz=1.35), {"punch": {"at": "@halfway", "zoom": 1.8, "focus": [.35, .55]}}),
    ("And even if you wanted to leave, you can't just go.", I("packing", (.5, .5), 1.3, tz=1.0), {}),
    ("Earth and Mars have to line up for the trip home,", I("orbits", (.5, .5), 1.0, tz=1.25), {}),
    ("and that only happens about once every twenty six months.", I("orbits", (.5, .5), 1.3, tz=1.6), {"overlays": [RM("m26", "@twenty-0.2")]}),
    ("Missions in the real plans often stay on Mars for well over a year,", V("mars-base", 9.0, 1.1), {}),
    ("just waiting for the planets to come back into position.", V("hourglass", 1.0, 1.15), {}),
    ("So you put the bags down.", I("unpacking", (.45, .6), 1.5, tz=1.8), {}),
    ("You say hello again to the potatoes.", I("potatoes", (.5, .45), 1.6, tz=2.0), {"sfx": [{"name": "pop", "at": "@hello"}]}),
    ("When you finally do fly home, Earth's gravity hits you like a ton of bricks.", I("return", (.5, .5), 1.0, tz=1.3), {"music": "confident", "shake": ["@ton"],
                                                                                                                         "sfx": [{"name": "impact", "at": "@ton"}]}),
    ("You feel almost three times heavier, because you basically are.", I("earth-heavy", (.5, .5), 1.0, tz=1.3), {}),
    ("You'll wobble, you'll be tired, and you'll need weeks to get your strength back.", I("earth-heavy", (.45, .45), 1.5, tz=1.8), {}),
    ("But you'll also be one of the only humans who ever watched a blue sunset on another planet.", I("final-sunset", (.5, .5), 1.0, tz=1.3),
     {"music": "warm", "sfx": [{"name": "reveal", "at": "@blue"}]}),
    ("So, what if you lived on Mars for a year?", V("mars-globe", 3.0, 1.15), {"in": "dip", "pause_before": 0.3, "captions": False, "overlays": [RM("title", 0.2)]}),
    ("You'd breathe recycled air,", I("recycler", (.5, .5), 1.2, tz=1.5), {}),
    ("eat very careful potatoes,", I("potatoes", (.5, .5), 1.0, tz=1.3), {"in": "cut"}),
    ("wait twenty minutes for your mom to say hi,", I("laptop", (.5, .45), 1.3, tz=1.6), {"in": "cut"}),
    ("and fight dust every single day.", I("dusty-suit", (.5, .45), 1.2, tz=1.6), {"in": "cut"}),
    ("And honestly? You'd probably want to go back.", I("final-sunset", (.5, .45), 1.4, tz=1.0), {}),
    ("Just read the terms and conditions first.", I("contract", (.5, .55), 1.0, tz=1.4), {"captions": False, "overlays": [RM("readit", 0.1, hold=True)],
                                                                                         "sfx": [{"name": "click", "at": "@read"}, {"name": "bass", "at": "@first"}]}),
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
    spec = {"out": "../output/mars-full.mp4", "audio": [f"chapters/take{i}.wav" for i in range(1, 10)], "take_gap": 0.4, "speed": 1.0,
            "music_cues": cues, "music_volume": 0.38, "fade_out": 2.5, "progress": True, "shots": shots}
    (HERE / "video.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False))
    n_img = sum(1 for s in shots if kind(s["v"]) == "img")
    n_vid = sum(1 for s in shots if kind(s["v"]) == "video")
    n_ov = sum(1 for s in shots for o in s.get("overlays", []) if o["mg"] == "clip")
    print(f"{len(shots)} shots: {n_img} AI images, {n_vid} stock videos, {len(shots) - n_img - n_vid} motion-graphic shots, "
          f"{n_ov} Remotion overlays; {len(cues)} music cues")


if __name__ == "__main__":
    main()
