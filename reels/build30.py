import json, sys
C = [0.5, 0.5, 0.5]
MUS = {"echoes": ("echoes", 162.865), "tense": ("out-of-this-world", 117.26), "warm": ("fifth-of-february", 4.85)}

def S(img, text, focus="wide", zoom=1.0, sfx=(), punch=False, pause=False, drift=0.05):
    s = {"image": f"img/{img}.jpg", "text": text, "focus": focus, "zoom": zoom}
    if punch: s["punch"] = True
    else: s["drift"] = drift
    sfx = list(sfx)
    if pause:
        s["pause_before"] = 0.25; sfx = [{"name": "whoosh", "at": -0.15}] + sfx
    s["sfx"] = sfx
    return s

R = {}
R["carrot-egg-coffee"] = ("voice-cand-1.wav", "echoes", [
    S("a01-sad", "A girl told her father,", sfx=["hook"]),
    S("a01-sad", "\"Life is too hard.", zoom=1.25),
    S("a01-sad", "I want to give up.\"", zoom=1.45, punch=True, sfx=["heartbeat"]),
    S("a02-pots", "He said nothing.", pause=True),
    S("a02-pots", "He just put three pots of water", "man-face", 1.3),
    S("a02-pots", "on the fire.", C, 1.2, sfx=["whoosh2"]),
    S("a03-carrot", "In the first, he put a carrot.", sfx=["pop"]),
    S("a04-egg", "In the second, an egg.", sfx=["pop"]),
    S("a05-beans", "In the third, coffee beans.", sfx=["pop"]),
    S("a06-clock", "After twenty minutes,", pause=True),
    S("a06-clock", "he took them out.", C, 1.3, sfx=["whoosh2"]),
    S("a07-carrot-soft", "\"The carrot went in strong and hard,"),
    S("a07-carrot-soft", "but the boiling water made it weak.\"", "man-face", 1.4, punch=True),
    S("a08-egg-crack", "\"The egg was soft inside,"),
    S("a08-egg-crack", "but the heat made it hard.\"", "man-face", 1.4, punch=True),
    S("a09-coffee", "\"But the coffee beans", pause=True),
    S("a09-coffee", "did something different.", "man-face", 1.4),
    S("a05-beans", "They changed the water.\"", C, 1.4, punch=True, sfx=["sparkle"]),
    S("a10-hand", "\"The boiling water is your problem.", pause=True),
    S("a10-hand", "So which one are you?\"", "wide", 1.2, punch=True, sfx=["bass"]),
    S("k1-smile", "Don't let hard times change you.", pause=True),
    S("k1-smile", "Change the hard times.", "wide", 1.15, drift=-0.08, sfx=["whoosh", {"name": "sparkle", "at": 0.3}]),
], "\"But the coffee beans")
R["fisherman"] = ("voice-cand-1.wav", "echoes", [
    S("b01-relax", "A rich businessman saw a fisherman", sfx=["hook"]),
    S("b01-relax", "relaxing by the sea.", "man-face", 1.4),
    S("b02-ask", "\"Why aren't you fishing?\" he asked.", sfx=["whoosh2"]),
    S("b02-ask", "\"I caught enough for today.\"", "man-face", 1.5, punch=True),
    S("b03-count", "\"Fish more! Buy a bigger boat.", sfx=["pop"]),
    S("b04-dream", "Then many boats.", sfx=["whoosh2"]),
    S("b04-dream", "Build a company.", C, 1.3, sfx=["pop"]),
    S("b04-dream", "In twenty years, you'll be rich.\"", "wide", 1.1, drift=-0.06, sfx=["sparkle"]),
    S("b05-tilt", "\"And then what?\"", "man-face", 1.2, punch=True, sfx=["scratch"]),
    S("b06-proud", "\"Then you can retire,", pause=True),
    S("b06-proud", "live by the sea, fish a little", C, 1.25),
    S("b06-proud", "and spend time with your family.\"", "wide", 1.05),
    S("b01-relax", "The fisherman smiled.", "man-face", 1.6, pause=True),
    S("b07-family", "\"That's what I'm doing right now.\"", sfx=["sparkle"]),
    S("b08-silent", "The businessman had nothing to say.", sfx=["heartbeat"]),
    S("k1-sunset", "Some people chase", pause=True),
    S("k1-sunset", "their whole life for what", "man-face", 1.3),
    S("k1-sunset", "they already have.", "wide", 1.15, drift=-0.08, sfx=["whoosh", {"name": "sparkle", "at": 0.3}]),
], "The fisherman smiled.")
R["same-joke"] = ("voice-cand-1.wav", "echoes", [
    S("c01-joke", "A wise man stood before a crowd", sfx=["hook"]),
    S("c01-joke", "and told them a joke.", "man-face", 1.4),
    S("c02-laugh", "Everyone laughed loudly.", sfx=["pop"]),
    S("c03-again", "A minute later,", pause=True),
    S("c03-again", "he told the same joke again.", "man-face", 1.4),
    S("c04-few", "Only a few people laughed.", sfx=["whoosh2"]),
    S("c03-again", "Then he told it a third time.", "wide", 1.1),
    S("c05-silent", "Nobody laughed.", C, 1.2, punch=True, sfx=["wrong"]),
    S("c06-gentle", "He said,", pause=True),
    S("c06-gentle", "\"You can't laugh at the same joke", "man-face", 1.3),
    S("c06-gentle", "again and again.\"", "man-face", 1.6, punch=True),
    S("c07-eyes", "\"So why do you keep crying", "wide", 1.0),
    S("c07-eyes", "over the same problem", "man-face", 1.3),
    S("c07-eyes", "again and again?\"", "man-face", 1.6, punch=True, sfx=["bass"]),
    S("c08-photo", "The pain was real,", pause=True),
    S("c08-photo", "but every time you replay it,", "man-face", 1.4, sfx=["rewind"]),
    S("c08-photo", "you choose to feel it again.", "wide", 1.1),
    S("k1-drawer", "Learn the lesson.", pause=True),
    S("k2-window", "Then let it go.", "wide", 1.15, drift=-0.08, sfx=["whoosh", {"name": "sparkle", "at": 0.3}]),
], "The pain was real,")
R["boulder-road"] = ("voice-cand-1.wav", "tense", [
    S("d01-place", "One night, a king placed a huge rock", sfx=["hook"]),
    S("d01-place", "in the middle of a busy road.", C, 1.3),
    S("d02-hide", "Then he hid and watched.", "man-face", 1.3, pause=True),
    S("d03-traders", "Rich traders came and walked around it,", sfx=["whoosh2"]),
    S("d03-traders", "complaining,", C, 1.3, punch=True),
    S("d03-traders", "\"Why doesn't the king clear this road?\"", "wide", 1.1),
    S("d04-pass", "Many people passed.", sfx=["whoosh2"]),
    S("d04-pass", "Nobody tried.", C, 1.3, punch=True, sfx=["wrong"]),
    S("d05-farmer", "Then a poor farmer came.", pause=True),
    S("d05-farmer", "He put down his load", C, 1.3),
    S("d06-push", "and pushed with all his strength.", sfx=["heartbeat"]),
    S("d07-rolls", "Finally, the rock moved.", sfx=["impact"]),
    S("d08-gold", "Underneath was a bag of gold,", sfx=["sparkle"]),
    S("d08-gold", "with a note from the king:", C, 1.35),
    S("d09-amazed", "\"This belongs to the one", pause=True),
    S("d09-amazed", "who moved the rock.\"", C, 1.3, punch=True, sfx=["pop"]),
    S("k1-king", "Everyone saw a problem.", pause=True),
    S("k1-king", "Only one man saw a chance.", "wide", 1.2, punch=True, sfx=["bass"]),
    S("k1-king", "The obstacle in your path", "wide", 1.0),
    S("k1-king", "might be the gift", "wide", 1.08),
    S("k1-king", "you're looking for.", "wide", 1.15, drift=-0.08, sfx=["whoosh", {"name": "sparkle", "at": 0.3}]),
], "Underneath was a bag of gold,")
R["blind-elephant"] = ("voice-cand-2.wav", "tense", [
    S("e01-four", "Four blind men touched an elephant", sfx=["hook"]),
    S("e01-four", "for the first time.", C, 1.25),
    S("e02-trunk", "The first touched the trunk and said,", sfx=["whoosh2"]),
    S("e02-trunk", "\"An elephant is like a snake.\"", [0.4, 0.5, 0.45], 1.4, punch=True),
    S("e03-leg", "The second touched a leg.", sfx=["whoosh2"]),
    S("e03-leg", "\"No, it's like a tree.\"", [0.65, 0.6, 0.45], 1.4, punch=True),
    S("e04-ear", "The third touched the ear.", sfx=["whoosh2"]),
    S("e04-ear", "\"You're wrong, it's like a fan.\"", [0.65, 0.45, 0.45], 1.4, punch=True),
    S("e05-tail", "The fourth touched the tail.", sfx=["whoosh2"]),
    S("e05-tail", "\"It's a rope!\"", [0.6, 0.6, 0.45], 1.4, punch=True, sfx=["pop"]),
    S("e06-fight", "They began to fight.", sfx=["glitch"]),
    S("e06-fight", "Each one was sure he was right.", C, 1.3),
    S("e07-wise", "A wise man said,", pause=True),
    S("e07-wise", "\"You are all right,", "man-face", 1.4),
    S("e07-wise", "and you are all wrong.", "man-face", 1.7, punch=True),
    S("e07-wise", "Each of you touched", "wide", 1.05),
    S("e07-wise", "only one part.\"", C, 1.25),
    S("e08-shape", "Most arguments are just people", pause=True),
    S("e08-shape", "holding different parts", C, 1.3),
    S("e08-shape", "of the same truth.", "wide", 1.05, sfx=["sparkle"]),
    S("k1-see", "Before you judge,", pause=True),
    S("k1-see", "ask yourself what part", "man-face", 1.4),
    S("k1-see", "you can't see.", "wide", 1.15, drift=-0.08, sfx=["whoosh", {"name": "sparkle", "at": 0.3}]),
], "A wise man said,")

for slug in sys.argv[1:] or R:
    voice, m1, shots, sw = R[slug]
    i = next(n for n, s in enumerate(shots) if s["text"] == sw)
    cue = lambda k, n: {"music": f"../audio/music/{MUS[k][0]}.mp3", "start": MUS[k][1], "shot": n}
    d = {"out": f"../output/{slug}.mp4", "audio": [voice], "speed": 1.0, "music_volume": 0.4, "fade_out": 1.0,
         "music_cues": [cue(m1, 0), cue("warm", i)], "shots": shots}
    json.dump(d, open(f"/home/user/facebook-reels/reels/{slug}/reel.json", "w"), indent=1)
    print(slug, len(shots))
