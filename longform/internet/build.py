"""Build video.json for "What if the internet shut down worldwide for a week?" (~11 min, comedic second-person story).

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
    ("It's seven in the morning.", V("sunrise", 1.0, 1.1, drift=0.1), {"punch": True, "sfx": ["hook", {"name": "tick", "at": 0.3}]}),
    ("Your alarm goes off.", V("alarm-hand", 0.5, 1.15), {"sfx": [{"name": "tick", "at": 0.1}, {"name": "tick", "at": 0.25}, {"name": "tick", "at": 0.4}, {"name": "tick", "at": 0.55}]}),
    ("Good news: the alarm still works.", I("bed-alarm", (.5, .5), 1.0, tz=1.25), {"sfx": [{"name": "correct", "at": "@works", "gain": 0.4}]}),
    ("You grab your phone, still half asleep,", I("grab-phone", (.5, .5), 1.0, tz=1.3), {}),
    ("and open it like you do every single morning.", V("phone-bed", 1.0, 1.1), {}),
    ("And nothing loads.", HF("loading"), {"captions": False, "music_fx": "muffle", "sfx": [{"name": "glitch-hit", "at": "@loads", "gain": 0.5}]}),
    ("No messages. No news. No videos of cats falling off tables.", I("cat-table", (.5, .5), 1.0, tz=1.3),
     {"overlays": [KO(("NO MESSAGES", "red"), ("NO NEWS", "red"), ("NO CATS", "red"), times=["@messages", "@news", "@cats"], size=110)], "captions": False,
      "sfx": [{"name": "wrong", "at": "@messages", "gain": 0.35}, {"name": "wrong", "at": "@news", "gain": 0.35}, {"name": "wrong", "at": "@cats", "gain": 0.35}]}),
    ("Just a little spinning circle.", HF("loading", 2.0), {"in": "cut"}),
    ("Spinning. And spinning.", HF("loading", 4.0), {"in": "cut", "sfx": [{"name": "tick", "at": 0.1}, {"name": "tick", "at": "@spinning"}]}),
    ("So you do what every expert does.", I("router-stare", (.5, .5), 1.0, tz=1.2), {}),
    ("You turn the Wi-Fi off, and on again.", I("router", (.5, .5), 1.1, tz=1.4), {"sfx": [{"name": "switch", "at": "@off"}, {"name": "switch", "at": "@on"}]}),
    ("Nothing.", I("router", (.5, .45), 1.6, tz=1.8), {"in": "cut", "captions": False, "overlays": [KO(("NOTHING.", "red"), size=170)], "sfx": [{"name": "scratch", "gain": 0.5}]}),
    ("You restart the router.", V("netcables", 1.0, 1.15), {"sfx": [{"name": "click", "at": "@restart"}]}),
    ("You stare at its tiny blinking lights like they owe you money.", I("router-stare", (.5, .45), 1.3, tz=1.8),
     {"punch": {"at": "@money", "zoom": 1.6}, "sfx": [{"name": "pop", "at": "@money"}]}),
    ("Still nothing.", I("router", (.5, .5), 1.9, tz=2.1), {"in": "cut", "captions": False, "overlays": [KO(("STILL NOTHING.", "red"), size=150)]}),
    ("Here's what you don't know yet.", V("city-aerial", 1.0, 1.1), {"music": "tense", "sfx": [{"name": "riser", "at": 0.2, "gain": 0.6}]}),
    ("It's not your router. It's not your phone company.", I("router", (.5, .5), 1.0, tz=1.0, drift=0.1), {"in": "glitch"}),
    ("It's everyone.", V("cinema-phones", 1.0, 1.15), {"punch": True, "sfx": [{"name": "bass", "at": "@everyone"}]}),
    ("The entire internet, everywhere on Earth, just went dark.", I("earth-dark", (.5, .5), 1.0, tz=1.3),
     {"captions": False, "overlays": [RM("title", 0.0)], "sfx": [{"name": "boom", "at": "@dark", "gain": 0.6}]}),
    ("And it's going to stay dark for one whole week.", HF("dweek"), {"captions": False, "sfx": [{"name": "tick", "at": 0.3}, {"name": "tick", "at": 0.9}, {"name": "tick", "at": 1.5}, {"name": "bass", "at": 2.6}]}),
    ("Five and a half billion people", V("city-street", 1.0, 1.1), {"overlays": [RM("users", "@Five-0.2")], "captions": False}),
    ("just lost the thing they touch first every morning.", V("phone-scroll", 1.0, 1.15), {}),
    ("Don't panic.", I("panic", (.5, .5), 1.0, tz=1.2), {"music": "punchy"}),
    ("Okay, panic a little.", I("panic", (.5, .45), 1.5, tz=1.9), {"in": "cut", "sfx": [{"name": "scratch", "at": "@panic", "gain": 0.5}]}),
    ("But I'm going to walk you through every day of it.", HF("dweek", 1.0), {"in": "flash"}),
    ("Oh, and a few ground rules before we start.", I("rules", (.5, .5), 1.0, tz=1.2), {}),
    ("No streaming.", I("rules", (.5, .5), 1.2, tz=1.4), {"in": "cut", "overlays": [KO(("NO STREAMING", "red"), size=150)], "captions": False,
                                                       "sfx": [{"name": "wrong", "at": 0.05, "gain": 0.4}]}),
    ("No online shopping.", V("card-term2", 1.0, 1.15), {"in": "cut", "overlays": [KO(("NO ONLINE SHOPPING", "red"), size=130)], "captions": False,
                                                       "sfx": [{"name": "wrong", "at": 0.05, "gain": 0.4}]}),
    ("No looking things up.", V("typing-keys", 1.0, 1.15), {"in": "cut", "overlays": [KO(("NO LOOKING THINGS UP", "red"), size=120)], "captions": False,
                                                          "sfx": [{"name": "wrong", "at": 0.05, "gain": 0.4}]}),
    ("If you don't know something, you'll just have to not know it.", I("shrug", (.5, .5), 1.0, tz=1.25), {}),
    ("Like our ancestors did.", I("caveman", (.5, .5), 1.0, tz=1.3), {"sfx": [{"name": "pop", "at": "@ancestors"}]}),
    ("The funny parts,", I("cat-table", (.5, .5), 1.3, tz=1.6), {"music": "intrigue", "sfx": [{"name": "sparkle"}]}),
    ("the scary parts,", I("empty-aisle", (.5, .5), 1.0, tz=1.3), {"in": "glitch", "shake": [0.1]}),
    ("and the moment on day seven when you realise the hardest part isn't losing the internet.", HF("notifs", 1.0), {"captions": False,
     "overlays": [KO("THE HARDEST PART ISN'T", ("LOSING IT", "yellow"), times=["@hardest", "@losing"], size=90, dy=420)]}),
    ("It's getting it back.", K("IT'S", ("GETTING IT BACK", "yellow"), times=[0.0, "@getting"], size=150), {"voice_fx": {"at": "@back", "fx": "echo"},
     "sfx": [{"name": "glitch-hit", "at": 0.0}, {"name": "bass", "at": "@back"}]}),
]

CH2 = [
    ("Day one.", HF("ch1"), {"chapter": True, "music": "punchy"}),
    ("By eight o'clock, you've checked your phone fourteen times.", V("phone-breakfast", 1.0, 1.1), {"overlays": [TAG("08:00 · CHECKS: 14")]}),
    ("It's still dead.", HF("loading", 1.0), {"in": "cut"}),
    ("You check it again.", V("phone-scroll", 3.0, 1.2), {"in": "cut"}),
    ("Just in case.", I("grab-phone", (.5, .45), 1.6, tz=1.9), {"in": "cut", "sfx": [{"name": "pop"}]}),
    ("You walk into the kitchen and ask the smart speaker what's going on.", I("speaker", (.5, .5), 1.0, tz=1.3), {}),
    ("It says sorry, it's having trouble connecting.", I("speaker", (.5, .5), 1.4, tz=1.7), {"in": "cut",
     "overlays": [KO(("\"SORRY, I'M HAVING TROUBLE CONNECTING\"", "yellow"), size=70, dy=300)], "sfx": [{"name": "wrong", "at": "@trouble", "gain": 0.35}]}),
    ("Yeah, buddy. We all are.", I("speaker", (.5, .5), 1.9, tz=2.1), {"in": "cut", "sfx": [{"name": "scratch", "at": "@all", "gain": 0.5}]}),
    ("You head to work.", V("traffic", 1.0, 1.1), {}),
    ("Or you try to.", V("traffic", 4.0, 1.4), {"in": "cut"}),
    ("Your train app is blank,", I("platform", (.5, .5), 1.0, tz=1.2), {}),
    ("so you just stand on the platform and wait,", I("platform", (.5, .5), 1.3, tz=1.5), {"in": "cut"}),
    ("like it's nineteen eighty five.", I("retro-platform", (.5, .5), 1.0, tz=1.25), {"overlays": [TAG("◀◀ 1985")], "sfx": [{"name": "rewind", "at": 0.0, "gain": 0.5}]}),
    ("At the office, nobody can do anything.", V("office-bored", 1.0, 1.1), {"music": "warm"}),
    ("Email is gone.", V("typing", 1.0, 1.15), {"in": "cut", "overlays": [KO(("EMAIL: GONE", "red"), size=140)], "captions": False, "sfx": [{"name": "wrong", "at": 0.05, "gain": 0.35}]}),
    ("The chat app is gone.", V("typing-keys", 4.0, 1.15), {"in": "cut", "overlays": [KO(("CHAT: GONE", "red"), size=140)], "captions": False, "sfx": [{"name": "wrong", "at": 0.05, "gain": 0.35}]}),
    ("The cloud, where every file you've ever made lives,", V("datacenter", 1.0, 1.1), {}),
    ("is basically a real cloud now.", I("real-cloud", (.5, .5), 1.0, tz=1.3), {"sfx": [{"name": "sparkle", "at": "@real"}]}),
    ("Pretty, far away, and no use to anyone.", I("real-cloud", (.5, .4), 1.5, tz=1.8), {"in": "cut"}),
    ("Your boss calls a meeting to discuss the situation.", I("meeting", (.5, .5), 1.0, tz=1.2), {}),
    ("The meeting is just twelve people saying,", I("meeting", (.5, .5), 1.3, tz=1.5), {"in": "cut"}),
    ("has anyone tried turning it off and on again?", K("\"HAS ANYONE TRIED", ("TURNING IT OFF AND ON AGAIN?\"", "yellow"), times=[0.0, "@turning"], size=110),
     {"sfx": [{"name": "switch", "at": "@off"}, {"name": "switch", "at": "@on"}]}),
    ("Lunch time.", V("toast-butter", 2.0, 1.1), {"in": "dip"}),
    ("You tap your card at the sandwich shop.", V("card-term", 1.0, 1.15), {"sfx": [{"name": "click", "at": "@tap"}]}),
    ("Declined.", V("card-term", 4.0, 1.4), {"in": "cut", "captions": False, "overlays": [RM("declined", 0.0)], "shake": [0.05], "sfx": [{"name": "wrong", "at": 0.05}]}),
    ("Not because you're broke.", I("wallet-empty", (.5, .5), 1.0, tz=1.2), {}),
    ("Well, not only because you're broke.", I("wallet-empty", (.5, .5), 1.5, tz=1.8), {"in": "cut", "sfx": [{"name": "scratch", "at": "@only", "gain": 0.5}]}),
    ("The card machine can't reach your bank.", V("card-term2", 3.0, 1.15), {}),
    ("And cash?", V("wallet", 1.0, 1.15), {"in": "cut"}),
    ("When was the last time you carried cash?", I("wallet-empty", (.45, .55), 1.2, tz=1.5), {}),
    ("Exactly.", I("wallet-empty", (.45, .55), 1.8, tz=2.0), {"in": "cut"}),
    ("You have one coin and a gym receipt.", I("coin-receipt", (.5, .5), 1.0, tz=1.35), {"sfx": [{"name": "pop", "at": "@coin"}, {"name": "pop", "at": "@receipt"}]}),
    ("Then something weird happens.", I("pocket", (.5, .5), 1.0, tz=1.2), {"music": "tense", "sfx": [{"name": "riser", "at": 0.2, "gain": 0.5}]}),
    ("Your pocket buzzes.", I("pocket", (.5, .55), 1.4, tz=1.6), {"in": "cut", "shake": [0.0, 0.15, 0.3], "sfx": [{"name": "heartbeat", "at": 0.0, "gain": 0.6}]}),
    ("You grab your phone.", V("phone-car", 1.0, 1.15), {"in": "cut"}),
    ("Nothing. No message.", HF("loading", 3.0), {"in": "cut"}),
    ("Your brain just made it up.", I("brain", (.5, .5), 1.0, tz=1.3), {"sfx": [{"name": "glitch-hit", "at": "@made", "gain": 0.5}]}),
    ("That's called phantom vibration, and it's real.", I("pocket", (.5, .5), 1.0, tz=1.3), {"overlays": [TAG("PHANTOM VIBRATION")]}),
    ("In one study, almost nine out of ten college students said they'd felt it.", V("library-read", 1.0, 1.1), {"overlays": [RM("phantom", "@nine-0.2")], "captions": False}),
    ("Welcome to withdrawal.", I("withdrawal", (.5, .5), 1.0, tz=1.3), {"voice_fx": {"at": "@withdrawal", "fx": "echo"}}),
    ("It's only day one.", K("IT'S ONLY", ("DAY ONE", "yellow"), times=[0.0, "@day"], size=170), {"sfx": [{"name": "bass", "at": "@day"}]}),
    ("That evening, you get home and flop on the sofa, ready to watch your show.", I("sofa", (.5, .5), 1.0, tz=1.25), {"music": "warm"}),
    ("Except your show lives on the internet.", HF("loading", 5.0), {"in": "glitch"}),
    ("So does your music. So do your games.", I("sofa", (.5, .5), 1.4, tz=1.7),
     {"overlays": [KO(("NO MUSIC", "red"), ("NO GAMES", "red"), times=["@music", "@games"], size=120)], "captions": False,
      "sfx": [{"name": "wrong", "at": "@music", "gain": 0.35}, {"name": "wrong", "at": "@games", "gain": 0.35}]}),
    ("You find the old TV remote and switch to regular TV,", V("tv-remote", 1.0, 1.15), {"sfx": [{"name": "click", "at": "@switch"}]}),
    ("which still comes through the air.", I("antenna", (.5, .5), 1.0, tz=1.3), {}),
    ("Every channel is showing the same thing.", V("tv-static", 1.0, 1.15), {"sfx": [{"name": "click", "at": "@channel"}]}),
    ("People in suits, explaining that nobody knows what's going on.", V("reporter", 2.0, 1.1), {}),
    ("You go to bed at nine.", V("sleep", 1.0, 1.1), {"overlays": [TAG("21:00")]}),
    ("Not because you're tired.", I("awake-bed", (.5, .5), 1.0, tz=1.2), {}),
    ("Because there's literally", I("awake-bed", (.5, .45), 1.4, tz=1.8), {"in": "cut"}),
    ("nothing else to do.", V("clock-close", 4.0, 1.2), {"in": "cut", "sfx": [{"name": "tick", "at": 0.1}, {"name": "tick", "at": 0.6}]}),
]

CH3 = [
    ("Day two. Things get serious.", HF("ch2"), {"chapter": True, "music": "tense"}),
    ("Overnight, the news finally reaches you,", V("city-aerial", 8.0, 1.1), {}),
    ("through the oldest social network in the world.", I("fence", (.5, .5), 1.0, tz=1.2), {"overlays": [TAG("THE OLDEST SOCIAL NETWORK")]}),
    ("Your neighbour, shouting over the fence.", I("fence", (.5, .45), 1.4, tz=1.8), {"in": "cut", "punch": {"at": "@shouting", "zoom": 1.6}, "sfx": [{"name": "pop", "at": "@shouting"}]}),
    ("Here's the problem.", I("warehouse", (.5, .5), 1.0, tz=1.15), {"in": "glitch"}),
    ("Almost everything you buy now travels on information", V("netcables", 8.0, 1.15), {}),
    ("before it travels on a truck.", I("truck-data", (.5, .5), 1.0, tz=1.3), {"in": "cut"}),
    ("Shops order food through computers.", V("supermarket", 1.0, 1.1), {}),
    ("Warehouses track every box online.", I("warehouse", (.5, .5), 1.2, tz=1.5), {}),
    ("Trucks get their routes the same way.", V("traffic", 2.0, 1.15), {}),
    ("And most supermarkets only keep a few days of stock on the shelves.", V("super-fridge", 1.0, 1.1), {"overlays": [TAG("A FEW DAYS OF STOCK")]}),
    ("So by day two, the shelves start looking like the end of a party.", I("empty-aisle", (.5, .5), 1.0, tz=1.3), {}),
    ("Bread, gone.", I("empty-bread", (.5, .5), 1.1, tz=1.3), {"in": "cut", "captions": False, "overlays": [KO(("BREAD: GONE", "red"), size=150)], "sfx": [{"name": "wrong", "at": 0.05, "gain": 0.35}]}),
    ("Water, gone.", I("empty-water", (.5, .5), 1.1, tz=1.3), {"in": "cut", "captions": False, "overlays": [KO(("WATER: GONE", "red"), size=150)], "sfx": [{"name": "wrong", "at": 0.05, "gain": 0.35}]}),
    ("Toilet paper?", I("toilet-paper", (.5, .5), 1.0, tz=1.3), {"in": "cut", "music_fx": "muffle"}),
    ("You already know.", I("toilet-paper", (.5, .5), 1.5, tz=1.8), {"in": "cut", "sfx": [{"name": "bass", "at": 0.0}, {"name": "scratch", "at": 0.1, "gain": 0.4}]}),
    ("Delivery drivers sit in their vans with no addresses.", I("van", (.5, .5), 1.0, tz=1.25), {}),
    ("Somewhere, your parcel is just driving around in circles,", I("parcel-puppy", (.5, .5), 1.0, tz=1.3), {}),
    ("like a lost puppy.", V("dog-run", 0.5, 1.15), {"in": "cut", "sfx": [{"name": "pop", "at": "@puppy"}]}),
    ("At the petrol station, the card readers are down too.", V("fuel", 1.0, 1.15), {}),
    ("The queue for cash only fuel goes around the block.", I("fuel-queue", (.5, .5), 1.0, to=(.7, .5), tz=1.3), {"overlays": [TAG("CASH ONLY")]}),
    ("The banks are open, but they can't do much.", I("bank", (.5, .5), 1.0, tz=1.2), {}),
    ("The cash machines outside are offline.", I("atm", (.5, .5), 1.0, tz=1.3), {"overlays": [RM("offline", 0.2)], "captions": False, "sfx": [{"name": "wrong", "at": 0.25, "gain": 0.4}]}),
    ("And in some countries, like Sweden, cash is so rare that lots of shops don't even take it anymore.", V("coins", 1.0, 1.15),
     {"overlays": [RM("sweden", 0.3)], "captions": False}),
    ("At the airport, the planes can still fly.", V("airport-plane", 1.0, 1.1), {}),
    ("But booking, check in, and flight planning all run on networks.", V("airport-desk", 1.0, 1.1),
     {"overlays": [KO("BOOKING.", "CHECK IN.", ("FLIGHT PLANNING.", "yellow"), times=["@booking", "@check", "@flight"], size=100)], "captions": False,
      "sfx": [{"name": "pop", "at": "@booking"}, {"name": "pop", "at": "@check"}, {"name": "pop", "at": "@flight"}]}),
    ("In July twenty twenty four, one bad software update grounded thousands of flights around the world.", I("departures", (.5, .5), 1.0, tz=1.3),
     {"overlays": [RM("crowdstrike", "@July-0.1")], "captions": False}),
    ("And the internet was still on that day.", V("airport-bag", 1.0, 1.15), {"in": "glitch"}),
    ("Stock markets shut down.", V("stocks-down", 1.0, 1.1), {"sfx": [{"name": "impact", "at": "@shut", "gain": 0.5}]}),
    ("In twenty fifteen, a computer glitch froze the New York Stock Exchange for almost four hours.", V("stocks-board", 1.0, 1.1),
     {"overlays": [RM("nyse", "@twenty-0.1")], "captions": False}),
    ("Now imagine a week.", K("NOW IMAGINE", ("A WEEK", "red"), times=[0.0, "@week"], size=170), {"sfx": [{"name": "bass", "at": "@week"}]}),
    ("But here's the good news.", I("lights-on", (.5, .5), 1.0, tz=1.2), {"music": "warm", "sfx": [{"name": "sparkle"}]}),
    ("Your lights are still on.", I("lights-on", (.5, .5), 1.3, tz=1.6), {"in": "cut", "sfx": [{"name": "switch", "at": "@lights"}]}),
    ("Power grids run on their own control systems, separate from the public internet.", I("grid-control", (.5, .5), 1.0, tz=1.3), {}),
    ("So your fridge keeps humming, your taps still run, and you can still make toast.", V("toaster", 1.0, 1.15), {}),
    ("You've never been so grateful for toast.", I("toast-hero", (.5, .5), 1.0, tz=1.4), {"punch": {"at": "@toast", "zoom": 1.6}, "sfx": [{"name": "sparkle", "at": "@toast"}]}),
    ("Still, by the end of day two, one thing is clear.", V("city-street", 6.0, 1.1), {"music": "tense"}),
    ("This isn't a funny little outage anymore.", I("earth-dark", (.5, .5), 1.2, tz=1.5), {"in": "glitch", "shake": [0.1]}),
    ("And tomorrow, you're going to have to do something you haven't done in years.", I("door-out", (.5, .5), 1.0, tz=1.25), {}),
    ("Find your way somewhere. Alone.", I("lost-street", (.5, .5), 1.0, tz=1.25), {}),
    ("Without your phone telling you where to go.", I("lost-street", (.5, .5), 1.4, tz=1.8), {"in": "cut", "sfx": [{"name": "riser", "at": 0.3, "gain": 0.5}]}),
]

CH4 = [
    ("Day three.", HF("ch3"), {"chapter": True, "music": "punchy"}),
    ("You want to visit your friend across town.", V("sunrise", 14.0, 1.1), {}),
    ("Easy. You open the map app.", V("phone-scroll", 6.0, 1.15), {}),
    ("And here's a fun fact.", I("satellite", (.5, .5), 1.0, tz=1.2), {"sfx": [{"name": "sparkle"}]}),
    ("Your phone still knows exactly where you are.", I("blue-dot", (.5, .5), 1.0, tz=1.3), {"overlays": [RM("gps", 0.2)], "captions": False}),
    ("GPS comes from satellites, not the internet.", I("satellite", (.5, .5), 1.2, to=(.6, .4), tz=1.5), {"overlays": [TAG("GPS = SATELLITES")]}),
    ("So you get a little blue dot, in the middle of a completely blank screen.", I("blue-dot", (.5, .5), 1.4, tz=2.0), {}),
    ("You know where you are.", I("lost-street", (.5, .5), 1.0, tz=1.2), {}),
    ("You just don't know where anything else is.", I("lost-street", (.5, .5), 1.4, tz=1.0), {"in": "cut", "sfx": [{"name": "scratch", "at": "@anything", "gain": 0.4}]}),
    ("So you do something wild.", I("map-wild", (.5, .5), 1.0, tz=1.2), {"in": "glitch"}),
    ("You buy a paper map.", V("map-finger", 1.0, 1.15), {"sfx": [{"name": "correct", "at": "@map", "gain": 0.4}]}),
    ("At a petrol station. With your one coin.", I("coin-receipt", (.5, .5), 1.4, tz=1.8), {"sfx": [{"name": "pop", "at": "@coin"}]}),
    ("It takes twenty minutes to unfold", I("map-wild", (.5, .5), 1.2, tz=1.5), {}),
    ("and the rest of your life to fold back up.", I("map-tangle", (.5, .5), 1.0, tz=1.35), {"punch": {"at": "@life", "zoom": 1.6}, "sfx": [{"name": "scratch", "at": "@life", "gain": 0.5}]}),
    ("Day four.", HF("d4"), {"in": "dip", "pause_before": 0.3, "captions": False, "sfx": [{"name": "tunnel"}, {"name": "tick", "at": 0.65}]}),
    ("Your phone is now the world's most expensive flashlight.", V("flashlight", 1.0, 1.15), {"overlays": [TAG("$1,000 FLASHLIGHT")]}),
    ("And slowly, something strange happens.", V("kids-fountain", 1.0, 1.1), {"music": "warm"}),
    ("People start talking to each other.", I("neighbours", (.5, .5), 1.0, tz=1.2), {}),
    ("On purpose.", I("neighbours", (.5, .5), 1.3, tz=1.5), {"in": "cut", "sfx": [{"name": "pop"}]}),
    ("In real life.", I("neighbours", (.45, .45), 1.7, tz=2.0), {"in": "cut", "sfx": [{"name": "pop"}]}),
    ("Your neighbours, who you've only ever nodded at, turn out to have names.", I("nametag", (.5, .5), 1.0, tz=1.3), {}),
    ("One of them has a radio.", V("radio-vintage", 1.0, 1.15), {"sfx": [{"name": "glitch", "at": 0.2, "gain": 0.3}]}),
    ("Suddenly, she's the most popular person on the street.", I("radio-crowd", (.5, .5), 1.0, tz=1.3), {"sfx": [{"name": "sparkle", "at": "@popular"}]}),
    ("At the library, there's a queue.", V("shelves", 1.0, 1.1), {}),
    ("A queue! For books!", I("library-queue", (.5, .5), 1.0, tz=1.35), {"in": "cut", "punch": {"at": "@books", "zoom": 1.5}, "sfx": [{"name": "pop", "at": "@queue"}, {"name": "pop", "at": "@books"}]}),
    ("The librarian looks like she's waited her whole life for this moment.", I("librarian", (.5, .5), 1.0, tz=1.3), {}),
    ("Families drag out board games nobody has played in years.", V("boardgame", 1.0, 1.1), {}),
    ("Someone flips the board.", I("board-flip", (.5, .5), 1.0, tz=1.3), {"shake": ["@flips"], "sfx": [{"name": "impact", "at": "@flips", "gain": 0.6}]}),
    ("The game is over.", I("board-flip", (.5, .5), 1.5, tz=1.8), {"in": "cut"}),
    ("Some traditions never change.", V("chess-kids", 1.0, 1.15), {}),
    ("Kids go outside.", V("kids-run", 1.0, 1.1), {}),
    ("Like, outside outside.", V("kids-run", 8.0, 1.25), {"in": "cut"}),
    ("They invent a game with a ball and a stick,", I("kids-stick", (.5, .5), 1.0, tz=1.3), {}),
    ("and argue about the rules for three hours.", I("kids-stick", (.6, .5), 1.5, tz=1.8), {"in": "cut", "overlays": [TAG("3 HOURS LATER")]}),
    ("And dating?", I("cafe-hello", (.5, .5), 1.0, tz=1.15), {"in": "glitch"}),
    ("Dating apps are gone.", HF("loading", 6.0), {"in": "cut"}),
    ("If you like someone, you have to walk up to them and say hello.", I("cafe-hello", (.5, .5), 1.2, tz=1.45), {}),
    ("With your actual mouth.", I("cafe-hello", (.45, .45), 1.7, tz=2.0), {"in": "cut", "sfx": [{"name": "pop", "at": "@mouth"}]}),
    ("Terrifying.", K(("TERRIFYING.", "red"), size=200), {"shake": [0.0], "sfx": [{"name": "boom", "at": 0.0, "gain": 0.5}]}),
    ("Meanwhile, hospitals switch to their backup plans.", V("hosp-corridor", 1.0, 1.1), {"music": "intrigue"}),
    ("Paper charts, pens, and runners carrying notes down the hall.", V("clipboard", 1.0, 1.15),
     {"overlays": [KO("PAPER CHARTS.", "PENS.", ("RUNNERS.", "yellow"), times=["@Paper", "@pens", "@runners"], size=100)], "captions": False}),
    ("Slower, but they keep working.", V("monitor", 1.0, 1.15), {"sfx": [{"name": "heartbeat", "at": 0.2, "gain": 0.4}]}),
    ("Because hospitals plan for days exactly like this.", I("hospital-paper", (.5, .5), 1.0, tz=1.25), {}),
    ("That night, you lie in bed and stare at the ceiling.", I("ceiling", (.5, .5), 1.0, tz=1.3), {}),
    ("No scrolling. No last quick video.", I("ceiling", (.5, .5), 1.3, tz=1.5), {"in": "cut"}),
    ("Just you and your thoughts.", I("ceiling", (.5, .45), 1.6, tz=1.9), {"in": "cut", "music_fx": "muffle"}),
    ("It turns out your thoughts are kind of loud.", I("thoughts", (.5, .5), 1.0, tz=1.35), {"sfx": [{"name": "bass", "at": "@loud"}], "voice_fx": {"at": "@loud", "fx": "echo"}}),
    ("Who knew?", I("thoughts", (.5, .5), 1.5, tz=1.7), {"in": "cut", "sfx": [{"name": "pop"}]}),
]

CH5 = [
    ("Day five.", HF("ch4"), {"chapter": True, "music": "intrigue"}),
    ("By now, everyone is asking the same question.", I("radio-crowd", (.5, .5), 1.2, tz=1.4), {}),
    ("How does the whole internet just break?", I("earth-dark", (.5, .5), 1.0, tz=1.3), {"in": "glitch", "sfx": [{"name": "glitch-hit", "at": "@break", "gain": 0.5}]}),
    ("And to answer that, we need to look at where it actually lives.", V("server-walk", 2.0, 1.1), {}),
    ("Because the internet isn't in the sky.", I("real-cloud", (.5, .5), 1.0, tz=1.25), {}),
    ("It's mostly at the bottom of the ocean.", V("ocean-rays", 1.0, 1.15), {"sfx": [{"name": "whoosh2", "at": 0.0}, {"name": "bass", "at": "@ocean"}]}),
    ("Hundreds of cables, some as thin as a garden hose,", I("seabed-cable", (.5, .5), 1.0, tz=1.35), {"overlays": [TAG("AS THIN AS A GARDEN HOSE")]}),
    ("carry almost all the data that moves between continents.", I("cable-map", (.5, .5), 1.0, tz=1.25), {}),
    ("And they break all the time.", V("fiber", 1.0, 1.15), {"in": "glitch"}),
    ("Around one hundred and fifty to two hundred times a year.", I("seabed-cable", (.5, .5), 1.3, tz=1.6), {"overlays": [RM("faults", "@one-0.2")], "captions": False}),
    ("Mostly because of ship anchors and fishing nets.", V("trawler", 1.0, 1.1),
     {"overlays": [KO("SHIP ANCHORS.", ("FISHING NETS.", "yellow"), times=["@anchors", "@fishing"], size=110)], "captions": False}),
    ("And yes, sharks have bitten them too.", V("shark", 1.0, 1.15), {"sfx": [{"name": "impact", "at": "@bitten", "gain": 0.5}]}),
    ("Nobody knows why.", I("shark-cable", (.5, .5), 1.0, tz=1.3), {}),
    ("Maybe they just wanted Wi-Fi.", I("shark-cable", (.5, .45), 1.5, tz=1.9), {"in": "cut", "sfx": [{"name": "scratch", "at": 0.9, "gain": 0.5}]}),
    ("Taking the whole internet down at once is incredibly hard.", V("datacenter", 4.0, 1.1), {}),
    ("It was designed to route around damage.", I("cable-map", (.5, .5), 1.4, tz=1.7), {}),
    ("But smaller blackouts have happened.", V("city-street", 12.0, 1.1), {"in": "glitch", "music": "tense"}),
    ("In twenty eleven, Egypt switched off its internet for about five days.", I("cairo-night", (.5, .5), 1.0, tz=1.3), {"overlays": [RM("egypt", "@twenty-0.1")], "captions": False}),
    ("And in twenty twenty one, Facebook, Instagram and WhatsApp vanished for about six hours,", HF("loading-6h"), {"captions": False,
     "overlays": [RM("fb2021", "@twenty-0.1")]}),
    ("because of one bad configuration change.", V("typing", 4.0, 1.15), {"sfx": [{"name": "typing", "at": 0.0}, {"name": "glitch-hit", "at": "@change", "gain": 0.4}]}),
    ("Some engineers reportedly struggled to get into their own buildings,", I("badge-door", (.5, .5), 1.0, tz=1.3), {}),
    ("because the door badges needed the network too.", I("badge-door", (.55, .5), 1.5, tz=1.9), {"overlays": [RM("locked", "@badges")], "captions": False,
     "sfx": [{"name": "wrong", "at": "@badges", "gain": 0.4}]}),
    ("Imagine being locked out of the building,", I("locked-out", (.5, .5), 1.0, tz=1.25), {"music": "punchy"}),
    ("while trying to fix the thing that locked you out.", I("locked-out", (.5, .5), 1.4, tz=1.8), {"in": "cut", "sfx": [{"name": "scratch", "at": "@locked", "gain": 0.4}]}),
    ("And fun fact.", V("clock-close", 1.0, 1.15), {"sfx": [{"name": "rewind", "at": 0.0, "gain": 0.5}]}),
    ("The very first internet message, in nineteen sixty nine, was supposed to be the word login.", HF("lo"), {"captions": False,
     "overlays": [TAG("◀◀ 1969")]}),
    ("The system crashed after two letters.", HF("lo", 1.6), {"in": "cut", "sfx": [{"name": "glitch-hit", "at": 0.7}], "shake": [0.75]}),
    ("So the first message ever sent on the internet was just, L O.", K("THE FIRST MESSAGE EVER:", ("\"LO\"", "yellow"), times=[0.0, 2.2], size=190),
     {"sfx": [{"name": "bass", "at": 2.2}]}),
    ("The internet has been crashing since day one.", I("retro-computer", (.5, .5), 1.0, tz=1.3), {}),
    ("Today, it just has a lot more people watching.", V("cinema-phones", 4.0, 1.15), {}),
    ("Day five, evening.", HF("d5"), {"in": "dip", "pause_before": 0.3, "captions": False, "music": "warm", "sfx": [{"name": "tunnel"}, {"name": "tick", "at": 0.65}]}),
    ("Without the internet, rumours travel the old way. Mouth to mouth.", I("gossip", (.5, .5), 1.0, tz=1.3), {}),
    ("Your uncle says it was aliens.", I("ufo", (.5, .5), 1.0, tz=1.3), {"sfx": [{"name": "zap", "at": "@aliens"}]}),
    ("Your aunt says it was a solar storm.", I("solar-storm", (.5, .5), 1.0, tz=1.3), {"sfx": [{"name": "boom", "at": "@storm", "gain": 0.4}]}),
    ("Your cousin says a shark did it.", V("shark", 8.0, 1.15), {"sfx": [{"name": "pop", "at": "@shark"}]}),
    ("For the first time in years, nobody can prove anybody wrong.", I("gossip", (.5, .5), 1.4, tz=1.7), {}),
    ("Your uncle is having the best week of his life.", I("uncle", (.5, .5), 1.0, tz=1.35), {"punch": {"at": "@best", "zoom": 1.5}, "sfx": [{"name": "sparkle", "at": "@best"}]}),
    ("The government reads updates on the radio, twice a day.", V("radio-dial", 1.0, 1.15), {}),
    ("And for once, the whole country is listening", V("radio-vintage", 6.0, 1.2), {}),
    ("to the same thing at the same time.", I("radio-crowd", (.5, .5), 1.0, to=(.5, .4), tz=1.4), {"in": "cut"}),
]

CH6 = [
    ("Day six.", HF("ch5"), {"chapter": True, "music": "warm"}),
    ("Something has changed.", V("sunrise", 6.0, 1.1), {}),
    ("And it's you.", I("window-morning", (.5, .5), 1.0, tz=1.3), {"sfx": [{"name": "sparkle", "at": "@you"}]}),
    ("You slept eight hours.", V("sleep-phone", 1.0, 1.1), {"overlays": [TAG("SLEEP: 8 HRS")]}),
    ("Nobody kept you up scrolling at two in the morning.", V("phone-bed", 6.0, 1.15), {"overlays": [TAG("02:00")]}),
    ("You read half a book.", V("book-read", 1.0, 1.15), {}),
    ("You learned your neighbour's dog's name.", V("dog-close", 1.0, 1.15), {}),
    ("It's Biscuit.", V("biscuit", 1.0, 1.2), {"in": "cut", "captions": False, "overlays": [KO(("BISCUIT", "yellow"), size=180, dy=260)], "sfx": [{"name": "pop"}]}),
    ("Biscuit is a good boy.", V("biscuit", 8.0, 1.3), {"in": "cut", "sfx": [{"name": "sparkle", "at": "@good"}]}),
    ("You still reach for your phone sometimes.", I("reach-phone", (.5, .5), 1.0, tz=1.3), {}),
    ("But now, you notice yourself doing it.", I("reach-phone", (.5, .5), 1.4, tz=1.7), {"in": "cut"}),
    ("Your brain feels quieter.", I("calm", (.5, .5), 1.0, tz=1.25), {}),
    ("Like someone finally turned down a radio you didn't know was playing.", V("radio-dial", 8.0, 1.2), {"music_fx": "muffle"}),
    ("And here's the funny thing.", I("calm", (.5, .5), 1.3, tz=1.5), {}),
    ("You don't know what's trending.", I("newsstand", (.5, .5), 1.0, tz=1.25), {}),
    ("You don't know who's angry about what.", I("newsstand", (.5, .5), 1.3, tz=1.6), {"in": "cut"}),
    ("And the world still turned.", V("sunrise", 10.0, 1.15, drift=0.12), {}),
    ("Day seven.", HF("d7"), {"in": "dip", "pause_before": 0.3, "captions": False, "music": "tense", "sfx": [{"name": "tunnel"}, {"name": "tick", "at": 0.65}]}),
    ("At three in the afternoon, your phone buzzes.", I("pocket", (.5, .5), 1.2, tz=1.4), {"overlays": [TAG("15:00")], "shake": ["@buzzes"],
     "sfx": [{"name": "heartbeat", "at": "@buzzes", "gain": 0.6}]}),
    ("And this time, it's real.", I("phone-lit", (.5, .5), 1.0, tz=1.3), {"music_fx": "muffle"}),
    ("The internet is back.", K("THE INTERNET", ("IS BACK", "yellow"), times=[0.0, "@back"], size=180), {"music": "punchy", "sfx": [{"name": "bass", "at": "@back"}, {"name": "boom", "at": "@back", "gain": 0.5}]}),
    ("And then it buzzes again. And again. And again.", HF("notifs"), {"captions": False}),
    ("Every message, every email, every notification from the last seven days arrives at once.", HF("notifs", 3.0), {"in": "cut", "captions": False}),
    ("Your phone gets so hot you could fry an egg on it.", I("phone-egg", (.5, .5), 1.0, tz=1.35), {"punch": {"at": "@egg", "zoom": 1.6}, "sfx": [{"name": "scratch", "at": "@egg", "gain": 0.4}]}),
    ("Remember, the world normally sends hundreds of billions of emails every day.", V("typing-keys", 10.0, 1.15),
     {"overlays": [KO(("HUNDREDS OF BILLIONS", "yellow"), "OF EMAILS A DAY", times=["@hundreds", "@emails"], size=110)], "captions": False}),
    ("And everyone, everywhere,", V("cinema-phones", 8.0, 1.15), {}),
    ("is trying to log back in at the same moment.", V("typing", 8.0, 1.15), {"in": "cut", "sfx": [{"name": "typing", "at": 0.2}]}),
    ("So the internet comes back, and immediately falls over again.", HF("loading", 1.0), {"in": "glitch", "shake": ["@falls"], "sfx": [{"name": "glitch-hit", "at": "@falls"}]}),
    ("Classic internet.", I("earth-dark", (.5, .5), 1.5, tz=1.5), {"in": "cut", "captions": False, "overlays": [RM("classic", 0.0)], "sfx": [{"name": "scratch", "at": 0.0, "gain": 0.6}]}),
    ("Your boss emails.", V("office-party", 1.0, 1.1), {}),
    ("Subject line: urgent, sorry for the delay.", K("SUBJECT:", ("URGENT, SORRY FOR THE DELAY", "yellow"), times=[0.0, "@urgent"], size=110), {"sfx": [{"name": "typing", "at": 0.0}]}),
    ("Your apps all need updates.", V("phone-scroll", 2.0, 1.15), {"overlays": [TAG("34 UPDATES")]}),
    ("Your group chat has nine hundred unread messages,", HF("notifs", 5.0), {"in": "cut", "captions": False}),
    ("and every one of them says, is your internet down too?", K("\"IS YOUR INTERNET", ("DOWN TOO?\"", "yellow"), times=[0.0, "@down"], size=150), {"sfx": [{"name": "pop", "at": "@down"}]}),
    ("Your photos start uploading.", I("upload", (.5, .5), 1.0, tz=1.3), {}),
    ("All of them.", I("upload", (.5, .5), 1.5, tz=1.8), {"in": "cut"}),
    ("Including the forty blurry pictures you took of your neighbour's radio.", V("radio-vintage", 4.0, 1.3), {"sfx": [{"name": "shutter", "at": 0.1}, {"name": "shutter", "at": 0.4}, {"name": "shutter", "at": 0.7}]}),
    ("You open your favourite app, and for a second, it feels amazing.", V("phone-breakfast", 4.0, 1.15), {"music": "intrigue"}),
    ("The noise rushes back in,", I("phone-lit", (.5, .5), 1.2, tz=1.5), {"sfx": [{"name": "riser", "at": 0.2, "gain": 0.6}]}),
    ("like walking out of a quiet room into a stadium.", I("stadium", (.5, .5), 1.0, tz=1.35), {"sfx": [{"name": "boom", "at": "@stadium", "gain": 0.4}]}),
    ("Then you look up, and notice something.", I("street-phones", (.5, .5), 1.0, tz=1.15), {}),
    ("The street is quiet again.", I("street-phones", (.5, .5), 1.2, tz=1.4), {"in": "cut"}),
    ("Everyone is looking down at their phones.", V("cinema-phones", 1.0, 1.25), {}),
    ("Just like before.", I("street-phones", (.5, .5), 1.5, tz=1.8), {"in": "cut"}),
    ("And this is the hardest part.", I("reach-phone", (.5, .5), 1.0, tz=1.2), {"music": "sad"}),
    ("Not losing the internet.", HF("loading", 2.0), {"in": "cut"}),
    ("Getting it back,", I("phone-lit", (.5, .5), 1.6, tz=1.9), {"in": "cut"}),
    ("and deciding how much of your life to give it.", I("phone-door", (.5, .5), 1.0, tz=1.3), {"voice_fx": {"at": "@life", "fx": "echo"}}),
    ("So, the internet is back on.", V("city-street", 18.0, 1.1), {}),
    ("You're holding your phone.", I("phone-door", (.45, .55), 1.4, tz=1.7), {}),
    ("Biscuit is waiting at the door.", I("phone-door", (.72, .62), 1.4, tz=1.8), {}),
    ("What do you do first?", V("biscuit", 4.0, 1.25), {"captions": False, "overlays": [RM("ending", 0.0)], "sfx": [{"name": "bass", "at": "@first"}]}),
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
    for i in range(1, 10):
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
    spec = {"out": "../output/internet-full.mp4", "audio": takes(), "take_gap": 0.4, "speed": 1.0,
            "music_cues": cues, "music_volume": 0.38, "fade_out": 2.5, "progress": True, "shots": shots}
    (HERE / "video.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False))
    n_img = sum(1 for s in shots if kind(s["v"]) == "img")
    n_vid = sum(1 for s in shots if kind(s["v"]) == "video")
    n_ov = sum(1 for s in shots for o in s.get("overlays", []) if o["mg"] == "clip")
    print(f"{len(shots)} shots: {n_img} AI images, {n_vid} stock videos, {len(shots) - n_img - n_vid} motion-graphic shots, "
          f"{n_ov} Remotion overlays; {len(cues)} music cues")


if __name__ == "__main__":
    main()
