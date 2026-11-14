"""reel.json for parable reels 71-80. Usage: python3 build70.py [slug ...]  (helpers from build40/build50)

Shots that render longer than 3.1 s are listed in split80.json and cut automatically at a phrase break."""
import json
import sys
from pathlib import Path

import build50
from build40 import C, END, HOOK, MUS, S

HERE = Path(__file__).parent
LONG = json.load(open(HERE / "split80.json")) if (HERE / "split80.json").exists() else {}
VOICE = {"cookie-thief": "voice-cand-2.wav", "tortoise-hare": "voice-cand-3.wav"}
R = {}
R["long-spoons"] = ("echoes", [
    HOOK("h0-feed", "The difference between heaven and hell|might shock you.", C, 1.3),
    S("l01-ask", "A man asked to see both.", pause=True),
    S("l02-hell", "First, he was shown hell.", pause=True, sfx=["heartbeat"]),
    S("l02-hell", "A huge table full of delicious food.", C, 1.2),
    S("l02-hell", "But everyone was starving.", "wide", 1.05, sfx=["bass"]),
    S("l03-spoon", "Their spoons were longer than their arms,", sfx=["whoosh2"]),
    S("l03-spoon", "so they couldn't reach their own mouths.", C, 1.3),
    S("l04-watch", "Then he was shown heaven.", "man-face", 1.25, pause=True),
    S("l05-heaven", "The same table. The same food. The same long spoons.", sfx=["sparkle"]),
    S("l05-heaven", "But everyone was happy and full.", C, 1.25),
    S("h0-feed", "Because in heaven, they used their long spoons", "wide", 1.0, pause=True),
    S("h0-feed", "to feed each other.", C, 1.4, punch=True, sfx=["sparkle"]),
    S("l06-smile", "Same world. Same problem.", "man-face", 1.25, pause=True),
    END("k1-share", "The only difference was how they treated each other."),
], "Same world. Same problem.")
R["ant-grasshopper"] = ("tense", [
    HOOK("h0-snow", "What you do in summer|decides how you survive winter.", C, 1.3),
    S("a01-carry", "All summer long, an ant carried food to its home,", pause=True),
    S("a02-line", "one grain at a time.", C, 1.2, sfx=["pop"]),
    S("a04-laugh", "A grasshopper laughed at him.", sfx=["pop"]),
    S("a03-sing", "\"Why work so hard? Come and sing with me.", C, 1.2),
    S("a03-sing", "Enjoy the sun.\"", "wide", 1.05, sfx=["sparkle"]),
    S("a01-carry", "The ant kept working.", C, 1.3),
    S("a03-sing", "The grasshopper kept playing.", C, 1.35),
    S("a05-winter", "Then winter came.", pause=True, sfx=["bass"]),
    S("a05-winter", "Snow covered everything.", C, 1.25),
    S("a06-warm", "The ant was warm, with plenty of food.", sfx=["sparkle"]),
    S("h0-snow", "The grasshopper was cold and hungry, with nothing at all.", "wide", 1.0, sfx=["heartbeat"]),
    S("k1-hero", "Enjoy today. But prepare for tomorrow.", pause=True),
    END("k1-hero", "Because winter always comes."),
], "Enjoy today. But prepare for tomorrow.")
R["tortoise-hare"] = ("echoes", [
    HOOK("h0-finish", "Talent without consistency|loses to effort every time.", C, 1.3),
    S("t01-mock", "A fast hare laughed at a slow tortoise.", pause=True),
    S("t01-mock", "\"You're so slow. I could beat you sleeping.\"", C, 1.25),
    S("t02-start", "The tortoise said, \"Then let's race.\"", sfx=["pop"]),
    S("t03-zoom", "The hare shot ahead and soon couldn't even see the tortoise.", sfx=["whoosh"]),
    S("t04-nap", "So confident, he lay down under a tree for a nap.", sfx=["heartbeat"]),
    S("t05-walk", "The tortoise kept walking.", pause=True),
    S("t05-walk", "Slowly. Step by step. Never stopping.", C, 1.3),
    S("t06-wake", "When the hare woke up,", pause=True, sfx=["bass"]),
    S("t07-run", "he ran as fast as he could.", sfx=["whoosh2"]),
    S("t07-run", "But it was too late.", C, 1.3, punch=True),
    S("h0-finish", "The tortoise had already crossed the finish line.", "wide", 1.0, sfx=["sparkle"]),
    S("k1-hero", "Slow progress is still progress.", pause=True),
    END("k1-hero", "Keep going."),
], "Slow progress is still progress.")
R["cookie-thief"] = ("tense", [
    HOOK("h0-take", "Before you judge someone,|read this.", C, 1.3),
    S("c01-sit", "A woman waiting for her flight bought a pack of cookies and sat down.", pause=True),
    S("c02-stranger", "A stranger sat beside her."),
    S("c03-he-takes", "She took a cookie. Then he took one too.", sfx=["pop"]),
    S("c04-furious", "She was furious.", C, 1.3, punch=True, sfx=["bass"]),
    S("h0-take", "Every time she took one, so did he.", "wide", 1.0),
    S("c05-half", "When only one was left, he broke it in half,", pause=True),
    S("c05-half", "gave her one half and walked away smiling.", C, 1.2),
    S("c06-leave", "She was so angry."),
    S("c07-bag", "On the plane, she opened her bag.", pause=True, sfx=["heartbeat"]),
    S("c07-bag", "And there was her pack of cookies. Unopened.", C, 1.35, punch=True, sfx=["bass"]),
    S("c07-bag", "She had been eating his cookies the whole time.", "wide", 1.0),
    S("k1-kind", "Sometimes the person you're angry at", "man-face", 1.2, pause=True),
    END("k1-kind", "is the one being kind."),
], "Sometimes the person you're angry at")
R["bear-friend"] = ("tense", [
    HOOK("h0-sniff", "Trouble shows you|who your real friends are.", C, 1.3),
    S("f01-walk", "Two friends were walking through a forest.", pause=True),
    S("f02-bear", "Suddenly, a huge bear appeared.", sfx=["bass"]),
    S("f03-climb", "One friend climbed a tree as fast as he could", sfx=["whoosh2"]),
    S("f04-alone", "and left the other alone.", "man-face", 1.3, sfx=["heartbeat"]),
    S("f04-alone", "The second man had no time to run.", "wide", 1.0),
    S("h0-sniff", "He lay on the ground and held his breath, pretending to be dead.", "wide", 1.0, pause=True),
    S("h0-sniff", "The bear sniffed his ear,", C, 1.35, sfx=["heartbeat"]),
    S("f05-leave", "then walked away."),
    S("f06-down", "His friend climbed down.", pause=True),
    S("f06-down", "\"What did the bear whisper to you?\"", C, 1.25),
    S("f07-answer", "\"He said, never trust a friend who leaves you in danger.\"", "man-face", 1.3, sfx=["bass"]),
    S("k1-alone", "When life gets hard,", pause=True),
    END("k1-alone", "watch who stays."),
], "When life gets hard,")
R["miser-gold"] = ("tense", [
    HOOK("h0-stare", "Money you never use|is worth nothing.", C, 1.3),
    S("m01-sell", "A rich miser sold everything he owned and bought a lump of gold.", pause=True),
    S("m02-bury", "He buried it in his garden", sfx=["sparkle"]),
    S("m03-visit", "and went every single day just to look at it."),
    S("m04-thief", "One night, a thief dug it up and stole it.", pause=True, sfx=["bass"]),
    S("m05-cry", "The next morning, the miser screamed and cried.", sfx=["heartbeat"]),
    S("m06-neighbor", "His neighbour asked, \"Did you ever use that gold?\"", pause=True),
    S("m05-cry", "\"No. I only looked at it.\"", C, 1.3),
    S("m07-stone", "\"Then bury a stone in that hole and look at it instead.", "man-face", 1.2),
    S("m07-stone", "It will do you the same good.\"", "man-face", 1.5, punch=True),
    S("k1-share", "What you never use,", pause=True),
    END("k1-share", "you never really had."),
], "What you never use,")
R["cried-wolf"] = ("tense", [
    HOOK("h0-scream", "One lie|can cost you everything.", "man-face", 1.2),
    S("w01-bored", "A shepherd boy was bored watching his sheep.", pause=True),
    S("w02-shout", "So he shouted, \"Wolf! Wolf!\"", "man-face", 1.25, sfx=["bass"]),
    S("w03-run", "The villagers ran up the hill to help.", sfx=["whoosh2"]),
    S("w04-laugh", "But there was no wolf. The boy laughed."),
    S("w02-shout", "A few days later, he did it again. \"Wolf!\"", pause=True),
    S("w03-run", "Again, the villagers came running.", C, 1.25),
    S("w05-angry", "Again, no wolf.", C, 1.3, sfx=["wrong"]),
    S("w06-wolf", "Then one evening, a real wolf came.", pause=True, sfx=["heartbeat"]),
    S("h0-scream", "The boy screamed, \"Wolf! Please help!\"", "wide", 1.0, sfx=["bass"]),
    S("w07-nobody", "But this time, nobody came.", C, 1.25),
    S("w07-nobody", "They thought he was lying again.", "wide", 1.05),
    S("k1-sad", "Trust takes years to build and seconds to break.", pause=True),
    S("k1-sad", "Never lie,", "man-face", 1.3),
    S("k1-sad", "because one day", "wide", 1.0),
    END("k1-sad", "you'll need someone to believe you."),
], "Trust takes years to build and seconds to break.")
R["thirsty-crow"] = ("echoes", [
    HOOK("h0-pebble", "When the answer seems impossible,|think differently.", C, 1.3),
    S("c01-search", "On a hot summer day, a thirsty crow searched everywhere for water.", pause=True),
    S("c02-found", "At last, it found a pitcher.", sfx=["sparkle"]),
    S("c03-low", "But the water was too low.", sfx=["wrong"]),
    S("c03-low", "Its beak couldn't reach it.", C, 1.3),
    S("c04-push", "It tried to push the pitcher over. Too heavy.", sfx=["bass"]),
    S("c05-think", "Most birds would have flown away.", pause=True),
    S("c05-think", "But the crow looked around and saw small pebbles.", C, 1.25),
    S("h0-pebble", "One by one, it dropped them into the pitcher.", "wide", 1.0, sfx=["pop", {"name": "pop", "at": 0.6}]),
    S("c06-rise", "Slowly, the water rose. Higher and higher.", sfx=["sparkle"]),
    S("c07-drink", "Until finally, the crow could drink."),
    S("k1-hero", "Every problem has a way through.", pause=True),
    END("k1-hero", "You just have to find it."),
], "Every problem has a way through.")
R["empty-pot"] = ("echoes", [
    HOOK("h0-pot", "Sometimes an empty pot|is worth more than a garden of flowers.", "man-face", 1.2),
    S("p01-seeds", "An old emperor needed to choose the next ruler.", pause=True),
    S("p01-seeds", "He gave every child in the kingdom one seed.", C, 1.2),
    S("p06-smile", "\"Whoever grows the most beautiful flower will be the next emperor.\""),
    S("p02-plant", "A boy named Ping planted his seed", pause=True),
    S("p03-water", "and cared for it every day."),
    S("p04-nothing", "But nothing grew.", "man-face", 1.3, sfx=["heartbeat"]),
    S("p05-flowers", "When the day came, all the other children carried beautiful flowers.", pause=True, sfx=["sparkle"]),
    S("h0-pot", "Ping carried an empty pot. He was ashamed.", "wide", 1.0),
    S("p06-smile", "The emperor smiled.", C, 1.3, pause=True),
    S("p07-boiled", "\"I boiled every seed. None of them could grow.", sfx=["bass"]),
    S("p06-smile", "Only you were honest.\"", C, 1.4, punch=True),
    S("k1-crown", "Ping became the next emperor.", sfx=["sparkle"]),
    END("k1-crown", "Honesty always wins."),
], "The emperor smiled.")
R["sour-grapes"] = ("tense", [
    HOOK("h0-nose", "Watch out for this lie|we all tell ourselves.", C, 1.3),
    S("g01-see", "A hungry fox saw a bunch of juicy grapes hanging high on a vine.", pause=True),
    S("g02-jump", "He jumped to reach them. He missed.", sfx=["wrong"]),
    S("g03-higher", "He jumped again, higher this time. Still nothing.", sfx=["wrong"]),
    S("g04-tired", "Again and again he tried, until he was exhausted.", sfx=["heartbeat"]),
    S("h0-nose", "Finally, he walked away with his nose in the air.", "wide", 1.0, pause=True),
    S("h0-nose", "\"Those grapes are probably sour anyway.\"", C, 1.35, punch=True),
    S("k0-hero", "When we fail, it's easy to say we never wanted it.", pause=True),
    S("k0-hero", "But that lie keeps us from trying again.", "man-face", 1.3),
    S("k1-reach", "Be honest about what you want.", pause=True),
    END("k1-reach", "Then keep reaching."),
], "When we fail, it's easy to say we never wanted it.")

if __name__ == "__main__":
    for slug in sys.argv[1:] or R:
        m1, shots, sw = R[slug]
        shots = [x for s in shots for x in (s if isinstance(s, list) else [s])]
        shots = [x for s in shots for x in (build50.split(s) if s["text"] in LONG.get(slug, ()) else [s])]
        i = next(n for n, s in enumerate(shots) if sw.startswith(s["text"]))
        cue = lambda k, n: {"music": f"../audio/music/{MUS[k][0]}.mp3", "start": MUS[k][1], "shot": n}
        d = {"out": f"../output/{slug}.mp4", "audio": [VOICE.get(slug, "voice-cand-1.wav")], "speed": 1.0,
             "music_volume": 0.4, "fade_out": 1.0, "music_cues": [cue(m1, 0), cue("warm", i)], "shots": shots}
        json.dump(d, open(HERE / slug / "reel.json", "w"), indent=1)
        print(slug, len(shots))
