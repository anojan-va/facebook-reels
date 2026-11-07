"""Build video.json for "What if the world ran out of oil overnight?" (~10-11 min, documentary timeline).

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
    ("It's midnight.", V("city-night", 1.0, 1.1, drift=0.1), {"punch": True, "sfx": ["hook", {"name": "tick", "at": 0.3}]}),
    ("And every drop of oil on Earth just vanished.", I("oil-vanish", (.5, .5), 1.0, tz=1.3), {"captions": False, "overlays": [RM("gone", "@vanished-0.1")],
     "sfx": [{"name": "boom", "at": "@vanished", "gain": 0.6}]}),
    ("Not running low.", HF("gauge"), {"in": "flash"}),
    ("Not getting expensive.", HF("gauge", 0.9), {"in": "cut"}),
    ("Gone.", HF("gauge", 1.5), {"in": "cut", "shake": [0.05], "sfx": [{"name": "bass", "at": 0.0}]}),
    ("The crude oil deep underground.", V("pumpjack", 1.0, 1.1), {}),
    ("The giant tanks at every port.", V("refinery", 1.0, 1.1), {}),
    ("The fuel in every truck, every ship, every plane.", V("container-ocean", 1.0, 1.1),
     {"overlays": [KO("EVERY TRUCK.", "EVERY SHIP.", ("EVERY PLANE.", "yellow"), times=["@truck", "@ship", "@plane"], size=110)], "captions": False,
      "sfx": [{"name": "pop", "at": "@truck"}, {"name": "pop", "at": "@ship"}, {"name": "pop", "at": "@plane"}]}),
    ("And the petrol in your car, parked outside right now.", I("car-tank-empty", (.5, .5), 1.0, tz=1.35), {}),
    ("All of it, gone in an instant.", I("car-tank-empty", (.45, .55), 1.5, tz=1.9), {"in": "cut", "music_fx": "muffle", "sfx": [{"name": "glitch-hit", "at": "@instant", "gain": 0.5}]}),
    ("No warning. No countdown.", I("oil-vanish", (.5, .5), 1.3, tz=1.5), {"in": "glitch"}),
    ("Just one quiet second, and the world's most important liquid stops existing.", I("oil-drop", (.5, .5), 1.0, tz=1.5),
     {"voice_fx": {"at": "@existing", "fx": "echo"}, "sfx": [{"name": "reveal", "at": "@liquid"}]}),
    ("Right now, around one and a half billion vehicles are sitting on the world's roads.", V("traffic", 1.0, 1.1), {"overlays": [RM("cars", "@one-0.2")], "captions": False}),
    ("Tonight, almost all of them just became very expensive sculptures.", I("highway-stopped", (.5, .5), 1.0, tz=1.3), {"sfx": [{"name": "scratch", "at": "@sculptures", "gain": 0.4}]}),
    ("And here's the scary part.", V("highway", 1.0, 1.1), {"music": "tense", "sfx": [{"name": "riser", "at": 0.1, "gain": 0.6}]}),
    ("Oil isn't just fuel.", K("OIL ISN'T", ("JUST FUEL", "yellow"), times=[0.0, "@just"], size=170), {"sfx": [{"name": "bass", "at": "@fuel"}]}),
    ("It's hiding in your clothes, your medicine, your phone, and even the food on your plate.", I("plastic-world", (.5, .5), 1.0, tz=1.3),
     {"overlays": [KO("CLOTHES.", "MEDICINE.", "PHONE.", ("FOOD.", "yellow"), times=["@clothes", "@medicine", "@phone", "@food"], size=100)], "captions": False,
      "sfx": [{"name": "pop", "at": "@clothes"}, {"name": "pop", "at": "@medicine"}, {"name": "pop", "at": "@phone"}, {"name": "pop", "at": "@food"}]}),
    ("The world burns through about one hundred million barrels of oil every single day.", I("barrels", (.5, .5), 1.0, tz=1.3), {"overlays": [RM("barrels", "@one-0.2")], "captions": False}),
    ("That's enough to fill around six thousand Olympic swimming pools.", I("oil-pool", (.5, .5), 1.0, tz=1.3), {"overlays": [RM("pools", "@six-0.2")], "captions": False}),
    ("Every day.", I("oil-pool", (.5, .5), 1.6, tz=1.9), {"in": "cut", "sfx": [{"name": "impact", "gain": 0.5}]}),
    ("So what happens when the tap shuts off, all at once?", I("valve", (.5, .5), 1.0, tz=1.35), {"sfx": [{"name": "switch", "at": "@shuts"}]}),
    ("Do we lose our cars?", V("traffic", 4.0, 1.2), {"in": "cut"}),
    ("Our food?", V("supermarket", 1.0, 1.2), {"in": "cut"}),
    ("Our cities?", V("skyline", 1.0, 1.2), {"in": "cut", "sfx": [{"name": "bass"}]}),
    ("And the weirdest part is that some things wouldn't change at all.", I("lights-on", (.5, .5), 1.0, tz=1.25), {"music": "intrigue"}),
    ("While others would fall apart in just a few hours.", I("highway-stopped", (.5, .5), 1.3, tz=1.6), {"in": "glitch", "shake": [0.1]}),
    ("In this video, we'll fast forward through time.", HF("tl0"), {"in": "flash", "sfx": [{"name": "rewind", "at": 0.1, "gain": 0.5}]}),
    ("One hour. One day. One week. One month. One year. And ten years.", HF("tlall"), {"in": "cut", "captions": False,
     "sfx": [{"name": "tick", "at": "@hour"}, {"name": "tick", "at": "@day"}, {"name": "tick", "at": "@week"}, {"name": "tick", "at": "@month"},
             {"name": "tick", "at": "@year"}, {"name": "bass", "at": "@ten"}]}),
    ("And by the end, you'll see why the thing that saves us", V("powerlines", 1.0, 1.1), {}),
    ("might already be plugged into your wall.", I("wall-plug", (.5, .5), 1.0, tz=1.4), {"sfx": [{"name": "click", "at": "@plugged"}, {"name": "reveal", "at": "@wall"}]}),
]

CH2 = [
    ("Plus one hour.", HF("ch1"), {"chapter": True, "music": "tense"}),
    ("It's dark, and the first problem is in the sky.", V("plane", 1.0, 1.1), {}),
    ("At any moment, thousands of planes are in the air.", I("planes-sky", (.5, .5), 1.0, tz=1.25), {}),
    ("Their tanks are suddenly empty.", I("cockpit", (.5, .5), 1.0, tz=1.3), {"sfx": [{"name": "glitch-hit", "at": "@empty", "gain": 0.5}]}),
    ("Every jet engine goes silent.", I("engine-off", (.5, .5), 1.0, tz=1.35), {"music_fx": "muffle"}),
    ("But here's something most people don't know.", I("plane-glide", (.5, .5), 1.0, tz=1.15), {"sfx": [{"name": "bass", "at": 0.0}]}),
    ("A big airliner doesn't fall like a rock.", I("plane-glide", (.5, .5), 1.2, tz=1.4), {"in": "cut"}),
    ("It glides.", I("plane-glide", (.5, .45), 1.5, to=(.4, .45), tz=1.7), {"in": "cut", "sfx": [{"name": "whoosh2", "at": 0.0}]}),
    ("In nineteen eighty three, an Air Canada jet ran out of fuel at forty one thousand feet,", I("gimli-cruise", (.5, .5), 1.0, tz=1.3),
     {"overlays": [RM("gimli", "@nineteen-0.1")], "captions": False}),
    ("because of a mistake with the fuel calculation.", I("fuel-calc", (.5, .5), 1.0, tz=1.3), {"sfx": [{"name": "wrong", "at": "@mistake", "gain": 0.4}]}),
    ("The crew glided it down and landed safely on an old air base.", I("gimli", (.5, .5), 1.0, tz=1.3), {"sfx": [{"name": "impact", "at": "@landed", "gain": 0.5}]}),
    ("It became known as the Gimli Glider.", I("gimli", (.5, .5), 1.4, tz=1.7), {"in": "cut", "overlays": [TAG("THE GIMLI GLIDER")]}),
    ("Tonight, thousands of pilots need their own Gimli moment.", I("cockpit", (.5, .45), 1.4, tz=1.7), {}),
    ("Not all of them will find a runway in time.", I("runway-dark", (.5, .5), 1.0, tz=1.3), {"music_fx": "muffle"}),
    ("On the ground, highways turn into parking lots.", V("highway", 4.0, 1.1), {"sfx": [{"name": "bass", "at": "@parking"}]}),
    ("Cars roll to a stop wherever they are.", I("highway-stopped", (.5, .5), 1.0, to=(.6, .5), tz=1.3), {}),
    ("Headlights stay on for a while, then the batteries start to die.", I("headlights", (.5, .5), 1.0, tz=1.3), {}),
    ("Ambulances stop in the middle of the road.", I("ambulance-stopped", (.5, .5), 1.0, tz=1.3), {}),
    ("Fire engines can't leave the station.", I("fire-station", (.5, .5), 1.0, tz=1.25), {}),
    ("Police cars sit where they were parked.", I("police-parked", (.5, .5), 1.0, tz=1.25), {}),
    ("Millions of people walk home in the dark, leaving their cars behind.", I("walk-home", (.5, .5), 1.0, tz=1.3), {}),
    ("Some of them are hundreds of kilometres from home.", V("walking", 1.0, 1.15), {"overlays": [TAG("HOME: 300 KM")]}),
    ("At sea, around fifty thousand big cargo ships suddenly lose power.", V("cargo-ship", 1.0, 1.1), {"overlays": [RM("ships", "@fifty-0.2")], "captions": False}),
    ("They drift in the dark, carrying the world's food, fuel and phones.", I("ship-drift", (.5, .5), 1.0, tz=1.3), {}),
    ("Many freight trains stop too.", I("freight-train", (.5, .5), 1.0, tz=1.25), {}),
    ("In a lot of the world, the big locomotives that pull them run on diesel.", I("freight-train", (.5, .5), 1.3, tz=1.6), {"in": "cut"}),
    ("And in hospitals, the lights flicker.", V("hosp-corridor", 1.0, 1.15), {"shake": [0.2], "sfx": [{"name": "zap", "at": "@flicker"}]}),
    ("Most of the power still comes from the grid.", V("powerlines", 5.0, 1.1), {}),
    ("But the backup generators?", I("generator", (.5, .5), 1.0, tz=1.3), {"in": "glitch"}),
    ("Most of them run on diesel.", I("generator", (.5, .5), 1.5, tz=1.8), {"in": "cut", "sfx": [{"name": "bass"}]}),
    ("So the first night already has a rule.", I("night-city-dark", (.5, .5), 1.0, tz=1.2), {}),
    ("If something has a fuel tank, it just stopped.", K("IF IT HAS A FUEL TANK,", ("IT JUST STOPPED.", "red"), times=[0.0, "@stopped"], size=130),
     {"sfx": [{"name": "impact", "at": "@stopped"}]}),
    ("And by morning, the whole world is about to find out what else oil was quietly doing.", V("city-night", 6.0, 1.15), {"sfx": [{"name": "riser", "at": 1.0, "gain": 0.6}]}),
]

CH3 = [
    ("Plus one day.", HF("ch2"), {"chapter": True, "music": "intrigue"}),
    ("The sun comes up on a very strange world.", V("skyline", 6.0, 1.1), {}),
    ("Here's the first surprise.", I("lights-on", (.5, .5), 1.2, tz=1.4), {"sfx": [{"name": "sparkle"}]}),
    ("In most countries, the lights are still on.", V("powerlines", 8.0, 1.15), {"sfx": [{"name": "switch", "at": "@lights"}]}),
    ("Oil makes only a tiny slice of the world's electricity, around three percent.", I("power-plant", (.5, .5), 1.0, tz=1.3), {"overlays": [RM("elec", "@three-0.2")], "captions": False}),
    ("Most power comes from coal, gas, nuclear, water, wind and sun.", V("wind", 1.0, 1.1),
     {"overlays": [KO("COAL · GAS · NUCLEAR", ("WATER · WIND · SUN", "yellow"), times=["@coal", "@water"], size=90)], "captions": False}),
    ("So your fridge still hums.", I("fridge", (.5, .5), 1.0, tz=1.25), {}),
    ("Your phone still charges.", V("phone", 1.0, 1.15), {}),
    ("And the internet still works.", I("phone-news", (.5, .5), 1.0, tz=1.25), {}),
    ("Everyone can watch the chaos live.", I("phone-news", (.5, .5), 1.4, tz=1.7), {"in": "cut"}),
    ("But try to go anywhere.", V("traffic", 6.0, 1.15), {"in": "glitch", "music": "tense"}),
    ("Petrol stations are empty.", V("fuel", 1.0, 1.15), {"overlays": [KO(("EMPTY", "red"), size=150)], "captions": False, "sfx": [{"name": "wrong", "at": 0.05, "gain": 0.35}]}),
    ("Buses are parked.", I("bus-depot", (.5, .5), 1.0, tz=1.25), {"in": "cut"}),
    ("Taxis are gone.", I("taxi-rank", (.5, .5), 1.0, tz=1.25), {"in": "cut"}),
    ("Schools close, because the school buses can't run.", I("school-bus", (.5, .5), 1.0, tz=1.25), {}),
    ("Offices empty out, because nobody can get there.", I("empty-office", (.5, .5), 1.0, tz=1.25), {}),
    ("Millions of people work from home, if they still have a job.", V("phone", 6.0, 1.15), {}),
    ("The new kings of the road are bicycles, electric scooters,", V("bike", 1.0, 1.1), {"music": "punchy"}),
    ("and the tens of millions of electric cars on Earth.", V("ev-charge", 1.0, 1.15), {}),
    ("For the first time ever, the guy with the electric car", I("ev-hero", (.5, .5), 1.0, tz=1.2), {}),
    ("is the most popular person in the neighbourhood.", I("ev-hero", (.5, .45), 1.4, tz=1.7), {"in": "cut", "sfx": [{"name": "sparkle", "at": "@popular"}]}),
    ("Electric trains still run, and they're packed like never before.", I("packed-train", (.5, .5), 1.0, tz=1.3), {}),
    ("At airports, the departure boards turn red.", I("departures-red", (.5, .5), 1.0, tz=1.3), {"music": "tense"}),
    ("On a normal day, around one hundred thousand flights take off around the world.", V("airport", 1.0, 1.1), {"overlays": [RM("flights", "@one-0.2")], "captions": False}),
    ("Today, almost none do.", I("empty-runway", (.5, .5), 1.0, tz=1.25), {}),
    ("And what about the emergency oil?", V("refinery", 6.0, 1.15), {"in": "glitch"}),
    ("Many countries store huge amounts for exactly this kind of crisis.", I("tank-farm", (.5, .5), 1.0, tz=1.25), {}),
    ("The United States keeps its reserve in giant salt caves under the ground.", I("salt-cave", (.5, .5), 1.0, tz=1.3), {"overlays": [RM("spr", "@United-0.1")], "captions": False}),
    ("But in our scenario, every drop vanished.", I("salt-cave", (.5, .5), 1.4, tz=1.7), {"in": "cut"}),
    ("Those caves are just empty holes now.", I("salt-cave-empty", (.5, .5), 1.0, tz=1.35), {"voice_fx": {"at": "@holes", "fx": "echo"}}),
    ("But the real problem isn't people.", V("walking", 6.0, 1.15), {}),
    ("It's stuff.", K(("IT'S STUFF.", "yellow"), size=200), {"sfx": [{"name": "bass", "at": 0.0}]}),
    ("Almost everything you buy reached you on a truck, a ship, or a plane.", V("port", 1.0, 1.1), {}),
    ("And more than nine tenths of the energy for all that transport comes from oil.", V("container-ocean", 6.0, 1.15), {"overlays": [RM("transport", "@nine")], "captions": False}),
    ("So on day one, the trucks that deliver food to supermarkets don't come.", I("loading-dock", (.5, .5), 1.0, tz=1.3), {}),
    ("Most stores only keep a few days of food on the shelves.", V("supermarket", 5.0, 1.1), {"overlays": [TAG("A FEW DAYS OF FOOD")]}),
    ("And everyone knows it.", I("panic-shop", (.5, .5), 1.0, tz=1.15), {}),
    ("So everyone goes shopping. At the same time.", I("panic-shop", (.5, .5), 1.3, tz=1.6), {"in": "cut", "shake": ["@same"], "sfx": [{"name": "impact", "at": "@same", "gain": 0.4}]}),
    ("Bread. Rice. Pasta. Canned food. Bottled water. Gone by lunchtime.", I("empty-shelves", (.5, .5), 1.0, tz=1.35),
     {"overlays": [KO("BREAD. RICE. PASTA.", ("GONE BY LUNCHTIME.", "red"), times=["@Bread", "@Gone"], size=110)], "captions": False,
      "sfx": [{"name": "tick", "at": "@Bread"}, {"name": "tick", "at": "@Rice"}, {"name": "tick", "at": "@Pasta"}, {"name": "wrong", "at": "@Gone", "gain": 0.4}]}),
    ("And people who live far from the shops have a new problem.", I("long-walk", (.5, .5), 1.0, tz=1.2), {}),
    ("The nearest supermarket used to be a ten minute drive.", I("long-walk", (.5, .5), 1.3, tz=1.5), {"in": "cut", "overlays": [TAG("10 MIN DRIVE")]}),
    ("Now it's a three hour walk.", I("long-walk", (.55, .5), 1.7, tz=2.0), {"in": "cut", "overlays": [TAG("3 HOUR WALK")], "sfx": [{"name": "scratch", "at": "@three", "gain": 0.4}]}),
]

CH4 = [
    ("Plus one week.", HF("ch3"), {"chapter": True, "music": "tense"}),
    ("Seven days without oil. And the cracks are everywhere.", I("city-hungry", (.5, .5), 1.0, tz=1.3), {}),
    ("The shelves are empty, and they're not filling back up.", I("empty-shelves", (.5, .5), 1.3, tz=1.6), {}),
    ("Cities are the hardest hit.", V("skyline", 10.0, 1.15), {}),
    ("A big city can't feed itself.", I("city-hungry", (.5, .5), 1.3, tz=1.6), {"in": "cut"}),
    ("Its food comes from farms hundreds or even thousands of kilometres away.", V("harvest", 1.0, 1.1), {}),
    ("Without trucks, fresh food rots in fields and warehouses,", I("rotting-farm", (.5, .5), 1.0, tz=1.3), {}),
    ("while people in cities go hungry.", I("food-queue", (.5, .5), 1.0, tz=1.25), {}),
    ("Governments start rationing,", I("army-ration", (.5, .5), 1.0, tz=1.2), {"overlays": [RM("rationed", 0.1)], "captions": False}),
    ("and the army uses its last vehicles that still move.", I("army-ration", (.5, .5), 1.3, tz=1.5), {"in": "cut"}),
    ("Rubbish starts piling up on the streets, because garbage trucks run on diesel too.", V("garbage", 1.0, 1.15), {}),
    ("After a few days, cities start to smell.", I("garbage-street", (.5, .5), 1.0, tz=1.3), {"sfx": [{"name": "wrong", "at": "@smell", "gain": 0.4}]}),
    ("Fire brigades and ambulances share the few electric vehicles that exist.", I("electric-ambulance", (.5, .5), 1.0, tz=1.25), {}),
    ("Doctors and nurses cycle to work.", I("nurse-bike", (.5, .5), 1.0, tz=1.3), {}),
    ("Then we discover how much of our world is made of oil.", I("plastic-world", (.5, .5), 1.2, tz=1.5), {"music": "intrigue", "sfx": [{"name": "reveal", "at": "@made"}]}),
    ("Plastic is made almost entirely from oil and gas.", V("bottles", 1.0, 1.15), {}),
    ("Packaging. Bottles. Phone cases. Car parts.", I("plastic-world", (.5, .5), 1.5, tz=1.8),
     {"in": "cut", "overlays": [KO("PACKAGING.", "BOTTLES.", "PHONE CASES.", ("CAR PARTS.", "yellow"), times=["@Packaging", "@Bottles", "@Phone", "@Car"], size=100)], "captions": False,
      "sfx": [{"name": "pop", "at": "@Packaging"}, {"name": "pop", "at": "@Bottles"}, {"name": "pop", "at": "@Phone"}, {"name": "pop", "at": "@Car"}]}),
    ("And no new oil means no new plastic.", I("plastic-factory", (.5, .5), 1.0, tz=1.3), {"overlays": [RM("noplastic", "@no-0.1")], "captions": False}),
    ("Hospitals feel it first.", V("hosp-corridor", 6.0, 1.15), {"music": "tense"}),
    ("Syringes, gloves, IV bags, tubes.", V("syringe", 1.0, 1.15),
     {"overlays": [KO("SYRINGES. GLOVES.", ("IV BAGS. TUBES.", "yellow"), times=["@Syringes", "@IV"], size=110)], "captions": False}),
    ("Most are plastic, and they're used once and thrown away.", I("syringe-iv", (.5, .5), 1.0, tz=1.3), {}),
    ("Many medicines are made with chemicals that come from oil too.", V("pills", 1.0, 1.15), {}),
    ("Even simple painkillers.", I("painkillers", (.5, .5), 1.0, tz=1.4), {"sfx": [{"name": "pop", "at": "@painkillers"}]}),
    ("So hospitals start doing something they haven't done in decades.", I("sterilize", (.5, .5), 1.0, tz=1.2), {}),
    ("Washing and sterilising equipment, and using it again.", I("sterilize", (.5, .5), 1.4, tz=1.7), {"in": "cut"}),
    ("Around the world, roughly eighty percent of trade moves by sea.", V("cargo-ship", 6.0, 1.1), {"overlays": [RM("sea", "@eighty-0.2")], "captions": False}),
    ("Now the ships just sit there.", I("port-stuck", (.5, .5), 1.0, tz=1.3), {}),
    ("Phones, medicines, spare parts, all stuck in ports.", V("port", 6.0, 1.2), {"overlays": [TAG("STUCK IN PORT")]}),
    ("And some places go dark after all.", I("island-dark", (.5, .5), 1.0, tz=1.2), {"in": "glitch"}),
    ("Many small islands and remote towns make their electricity by burning diesel.", I("diesel-plant", (.5, .5), 1.0, tz=1.3), {}),
    ("For them, the lights finally go out.", I("island-dark", (.5, .5), 1.4, tz=1.7), {"music_fx": "muffle", "sfx": [{"name": "switch", "at": "@out"}]}),
    ("One week in, the question isn't how to get to work anymore.", V("walking", 10.0, 1.15), {}),
    ("It's how to get food to eight billion people.", I("food-queue", (.5, .5), 1.3, tz=1.6), {"overlays": [TAG("8,000,000,000 PEOPLE")]}),
    ("And the answer, for now, is simple.", I("city-hungry", (.5, .5), 1.0, tz=1.2), {}),
    ("We can't. Not all of them.", K(("WE CAN'T.", "red"), "NOT ALL OF THEM.", times=[0.0, "@Not"], size=160), {"sfx": [{"name": "bass", "at": 0.0}], "voice_fx": {"at": 0.1, "fx": "echo"}}),
]

CH5 = [
    ("Plus one month.", HF("ch4"), {"chapter": True, "music": "intrigue"}),
    ("Now the farms are in trouble.", V("tractor", 1.0, 1.1), {}),
    ("Modern farming runs on diesel.", V("harvest", 6.0, 1.15), {}),
    ("Tractors plough. Harvesters harvest.", I("tractor-idle", (.5, .5), 1.0, tz=1.25), {}),
    ("Trucks carry the grain away. Water pumps keep crops alive.", I("grain-truck", (.5, .5), 1.0, tz=1.25), {}),
    ("Fertilizer mostly comes from natural gas, so some of it can still be made.", I("fertilizer", (.5, .5), 1.0, tz=1.25), {}),
    ("But getting it to the fields?", I("tractor-idle", (.5, .5), 1.4, tz=1.6), {"in": "glitch"}),
    ("That needs diesel too.", K("THAT NEEDS", ("DIESEL TOO.", "red"), times=[0.0, "@diesel"], size=170), {"sfx": [{"name": "bass", "at": "@diesel"}]}),
    ("Some farmers bring back horses.", V("horse", 1.0, 1.15), {}),
    ("Others try to convert tractors to run on electricity or on fuel made from plants.", I("tractor-convert", (.5, .5), 1.0, tz=1.3), {}),
    ("But you can't rebuild a whole farm system in a month.", I("horse-plough", (.5, .5), 1.0, tz=1.3), {}),
    ("Food gets more expensive every single day.", I("price-tags", (.5, .5), 1.0, tz=1.3), {"sfx": [{"name": "tick", "at": 0.3}, {"name": "tick", "at": 0.8}]}),
    ("Meat becomes rare, because feeding animals takes huge amounts of grain,", I("cattle-feed", (.5, .5), 1.0, tz=1.25), {}),
    ("and moving that grain takes fuel.", I("grain-truck", (.5, .5), 1.4, tz=1.6), {"in": "cut"}),
    ("People start planting vegetables on balconies, in parks, and in their front gardens.", V("garden", 1.0, 1.15), {"music": "warm"}),
    ("Just like during the world wars.", I("victory-garden", (.5, .5), 1.0, tz=1.3), {"overlays": [TAG("◀◀ 1943")], "sfx": [{"name": "rewind", "at": 0.0, "gain": 0.4}]}),
    ("Meanwhile, the stuff we already have is slowly wearing out.", I("rusty-gears", (.5, .5), 1.0, tz=1.25), {"music": "intrigue"}),
    ("Every engine, every machine, every wind turbine needs lubricant to keep moving.", V("wind", 6.0, 1.15), {}),
    ("Most of it comes from oil.", I("oil-can", (.5, .5), 1.0, tz=1.4), {}),
    ("Car tyres are made with synthetic rubber, mostly from oil.", I("tyres", (.5, .5), 1.0, tz=1.3), {}),
    ("Roads are paved with asphalt, which is made from oil too.", V("asphalt", 1.0, 1.15), {}),
    ("Potholes start appearing, and nobody can fill them.", I("pothole", (.5, .5), 1.0, tz=1.35), {"sfx": [{"name": "impact", "at": "@Potholes", "gain": 0.4}]}),
    ("Even your wardrobe changes.", I("wardrobe", (.5, .5), 1.0, tz=1.2), {}),
    ("More than half of the fibres in our clothes are polyester, which is basically plastic.", V("sewing", 1.0, 1.15), {"overlays": [RM("polyester", "@half-0.1")], "captions": False}),
    ("Cotton and wool suddenly become very fashionable.", I("cotton-wool", (.5, .5), 1.0, tz=1.3), {"sfx": [{"name": "sparkle", "at": "@fashionable"}]}),
    ("And think about your phone.", V("phone", 3.0, 1.15), {}),
    ("Its case, the coating on its wires, even parts of its screen use chemicals made from oil.", I("phone-parts", (.5, .5), 1.0, tz=1.35), {}),
    ("Making new electronics suddenly gets much harder.", I("electronics-factory", (.5, .5), 1.0, tz=1.25), {}),
    ("But humans are good at one thing in a crisis.", V("factory", 1.0, 1.1), {"music": "confident"}),
    ("Getting creative.", K(("GETTING CREATIVE.", "yellow"), size=180), {"sfx": [{"name": "reveal", "at": 0.0}]}),
    ("Factories that made petrol cars start retooling for electric ones.", I("retool-factory", (.5, .5), 1.0, tz=1.3), {}),
    ("Engineers dust off old ideas, some of them more than a hundred years old.", I("old-ideas", (.5, .5), 1.0, tz=1.3), {}),
    ("And that's where things start to turn around.", V("solar", 1.0, 1.1), {}),
    ("Because one thing still works almost everywhere.", V("powerlines", 12.0, 1.15), {}),
    ("The power grid.", I("grid", (.5, .5), 1.0, tz=1.3), {"in": "cut", "sfx": [{"name": "zap", "at": 0.1}, {"name": "bass", "at": 0.2}]}),
    ("And anything that can plug into it suddenly becomes priceless.", I("wall-plug", (.5, .5), 1.3, tz=1.7), {"sfx": [{"name": "click", "at": "@plug"}]}),
]

CH6 = [
    ("Plus one year.", HF("ch5"), {"chapter": True, "music": "confident"}),
    ("The world looks like nineteen hundred and twenty fifty at the same time.", I("horse-bus", (.5, .5), 1.0, tz=1.3), {}),
    ("Horses on the streets next to electric buses.", I("horse-bus", (.5, .5), 1.4, to=(.6, .5), tz=1.6), {"in": "cut"}),
    ("Sailing ships in the harbour next to giant batteries.", I("sail-battery", (.5, .5), 1.0, tz=1.3), {}),
    ("It turns out we've lived without oil before.", V("candle", 1.0, 1.15), {"music": "intrigue"}),
    ("The first commercial oil well was drilled in Pennsylvania in eighteen fifty nine.", I("drake-well", (.5, .5), 1.0, tz=1.3), {"overlays": [RM("drake", "@Pennsylvania-0.2")], "captions": False}),
    ("Before that, people lit their homes with whale oil and candles.", I("whale-lamp", (.5, .5), 1.0, tz=1.3), {}),
    ("Now, every country races to replace oil with something else.", I("world-race", (.5, .5), 1.0, tz=1.25), {"music": "punchy"}),
    ("Countries like Brazil already run millions of cars on ethanol, made from sugarcane.", I("sugarcane-field", (.5, .5), 1.0, tz=1.3), {"overlays": [RM("brazil", "@Brazil-0.1")], "captions": False}),
    ("Fuel made from plants becomes the new gold.", I("ethanol-gold", (.5, .5), 1.0, tz=1.35), {"sfx": [{"name": "sparkle", "at": "@gold"}]}),
    ("Others turn coal and gas into liquid fuel.", V("coal", 1.0, 1.15), {}),
    ("It's an old trick. Germany did it in the Second World War, and South Africa still does it today.", I("synfuel-plant", (.5, .5), 1.0, tz=1.3),
     {"overlays": [RM("synfuel", "@old")], "captions": False}),
    ("It's expensive and dirty, but it keeps the planes flying.", V("plane", 6.0, 1.15), {}),
    ("Barely.", I("plane-glide", (.5, .5), 1.7, tz=1.9), {"in": "cut", "sfx": [{"name": "scratch", "gain": 0.4}]}),
    ("And electricity becomes king.", I("grid", (.5, .5), 1.3, tz=1.6), {"sfx": [{"name": "bass", "at": "@king"}]}),
    ("Electric trucks. Electric tractors. Electric ferries.", I("electric-truck", (.5, .5), 1.0, tz=1.3),
     {"overlays": [KO("ELECTRIC TRUCKS.", "ELECTRIC TRACTORS.", ("ELECTRIC FERRIES.", "yellow"), times=["@trucks", "@tractors", "@ferries"], size=100)], "captions": False,
      "sfx": [{"name": "pop", "at": "@trucks"}, {"name": "pop", "at": "@tractors"}, {"name": "pop", "at": "@ferries"}]}),
    ("Factories that once built petrol cars now build electric ones around the clock.", V("factory", 6.0, 1.15), {}),
    ("Solar panels and wind turbines go up faster than ever,", V("solar", 6.0, 1.15), {}),
    ("because now they're not just about the climate.", V("wind", 10.0, 1.15), {}),
    ("They're about survival.", K("THEY'RE ABOUT", ("SURVIVAL.", "yellow"), times=[0.0, "@survival"], size=170), {"sfx": [{"name": "bass", "at": "@survival"}]}),
    ("Batteries become the most valuable thing you can own.", I("battery-gold", (.5, .5), 1.0, tz=1.35), {}),
    ("Cities change too.", V("bike", 6.0, 1.15), {}),
    ("People move closer to where they work, and closer to where their food grows.", I("bike-city", (.5, .5), 1.0, tz=1.25), {}),
    ("Bikes outnumber cars on many streets.", V("bike", 10.0, 1.2), {}),
    ("Plus ten years.", HF("tl10"), {"in": "dip", "pause_before": 0.3, "captions": False, "music": "warm", "sfx": [{"name": "tunnel"}, {"name": "tick", "at": 0.65}]}),
    ("The world has survived.", I("ten-years", (.5, .5), 1.0, tz=1.25), {}),
    ("But it's poorer, smaller and slower.", I("ten-years", (.5, .5), 1.3, tz=1.5), {"in": "cut",
     "overlays": [KO("POORER.", "SMALLER.", ("SLOWER.", "yellow"), times=["@poorer", "@smaller", "@slower"], size=110)], "captions": False}),
    ("Flying is a luxury again.", V("airport", 8.0, 1.15), {}),
    ("Fruit from the other side of the world is a treat, not a snack.", I("fruit-treat", (.5, .5), 1.0, tz=1.35), {}),
    ("And plastic? It's so precious that nobody throws it away.", V("bottles", 6.0, 1.15), {}),
    ("Every bottle gets used again and again.", I("refill", (.5, .5), 1.0, tz=1.3), {}),
    ("Holidays happen by train.", I("train-holiday", (.5, .5), 1.0, tz=1.25), {}),
    ("Your clothes are made to last.", V("sewing", 6.0, 1.15), {}),
    ("And repair shops are busier than ever,", I("repair-shop", (.5, .5), 1.0, tz=1.25), {}),
    ("because fixing something is cheaper than making a new one.", I("repair-shop", (.5, .5), 1.4, tz=1.7), {"in": "cut"}),
    ("Here's the strange twist.", V("skyline", 14.0, 1.15), {"music": "sad"}),
    ("In a world without oil, the air gets cleaner.", I("blue-sky-city", (.5, .5), 1.0, tz=1.25), {}),
    ("The skies over cities turn bluer.", I("blue-sky-city", (.5, .4), 1.3, to=(.5, .3), tz=1.6), {"in": "cut"}),
    ("But the cost of getting there is enormous.", I("city-hungry", (.5, .5), 1.0, tz=1.2), {}),
    ("Because we didn't choose the change.", I("valve", (.5, .5), 1.3, tz=1.6), {}),
    ("It was forced on us overnight.", I("oil-vanish", (.5, .5), 1.4, tz=1.7), {"in": "glitch", "sfx": [{"name": "glitch-hit", "at": "@overnight", "gain": 0.4}]}),
    ("And that's the real lesson.", V("pumpjack", 6.0, 1.15), {}),
    ("Oil will not vanish tomorrow.", V("refinery", 10.0, 1.15), {}),
    ("But one day, the world will move beyond it anyway.", V("solar", 10.0, 1.15), {}),
    ("The only question is whether we do it slowly and on purpose,", I("blue-sky-city", (.5, .5), 1.2, tz=1.4), {}),
    ("or suddenly, and in the dark.", I("night-city-dark", (.5, .5), 1.3, tz=1.6), {"in": "glitch", "music_fx": "muffle", "voice_fx": {"at": "@dark", "fx": "echo"}}),
    ("So, if the tap shut off tonight, would you be ready?", I("valve", (.5, .5), 1.6, tz=2.0), {"captions": False, "overlays": [RM("ending", "@would-0.1")],
     "sfx": [{"name": "bass", "at": "@ready"}]}),
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


def takes():
    out = []
    for i in range(1, 11):
        w = HERE / "chapters" / f"take{i}.wav"
        out += [f"chapters/take{i}.wav"] if w.exists() else [f"chapters/take{i}{h}.wav" for h in "ab"]
    return out


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
    spec = {"out": "../output/oil-full.mp4", "audio": takes(), "take_gap": 0.4, "speed": 1.0,
            "music_cues": cues, "music_volume": 0.38, "fade_out": 2.5, "progress": True, "shots": shots}
    (HERE / "video.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False))
    n_img = sum(1 for s in shots if kind(s["v"]) == "img")
    n_vid = sum(1 for s in shots if kind(s["v"]) == "video")
    n_ov = sum(1 for s in shots for o in s.get("overlays", []) if o["mg"] == "clip")
    print(f"{len(shots)} shots: {n_img} AI images, {n_vid} stock videos, {len(shots) - n_img - n_vid} motion-graphic shots, "
          f"{n_ov} Remotion overlays; {len(cues)} music cues")


if __name__ == "__main__":
    main()
