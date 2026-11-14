"""reel.json for parable reels 81-90. Usage: python3 build70.py [slug ...]  (helpers from build40/build50)

Shots that render longer than 3.1 s are listed in split90.json and cut automatically at a phrase break."""
import json
import sys
from pathlib import Path

import build50
from build40 import C, END, HOOK, MUS, S

HERE = Path(__file__).parent
LONG = json.load(open(HERE / "split90.json")) if (HERE / "split90.json").exists() else {}
VOICE = {}
R = {}
R["well-frog"] = ("echoes", [
    HOOK("h0-sky", "Your whole world might be|smaller than you think.", C, 1.3),
    S("w01-bottom", "A frog lived at the bottom of a deep well.", pause=True),
    S("w02-circle", "Every day he looked up at the small circle of sky", sfx=["whoosh2"]),
    S("w01-bottom", "and thought, \"This is the whole world.\"", C, 1.3),
    S("w03-turtle", "One day, a turtle from the ocean looked down into the well.", pause=True),
    S("w04-ask", "\"How big is your world?\" asked the frog.", C, 1.2),
    S("w04-ask", "\"Bigger than this well?\"", C, 1.45, punch=True),
    S("w03-turtle", "The turtle laughed.", C, 1.3, sfx=["pop"]),
    S("w05-ocean", "\"The ocean is so big, you can swim for years and never see the end.\"", sfx=["sparkle"]),
    S("w06-doubt", "The frog didn't believe him.", pause=True),
    S("h0-sky", "He had never seen anything else.", C, 1.3, sfx=["heartbeat"]),
    S("k1-climb", "Don't let your well decide how big your world is.", pause=True),
    END("k1-climb", "Climb out and look."),
], "Don't let your well decide how big your world is.")
R["truck-bridge"] = ("tense", [
    HOOK("h0-stuck", "Sometimes the smartest answer|comes from the simplest mind.", C, 1.3),
    S("h0-stuck", "A big truck got stuck under a low bridge.", "wide", 1.0, pause=True, sfx=["bass"]),
    S("t01-jam", "Its roof was jammed tight.", C, 1.25, sfx=["glitch"]),
    S("t02-traffic", "Traffic stopped for miles.", sfx=["heartbeat"]),
    S("t03-engineers", "Engineers came.", pause=True),
    S("t04-plans", "They argued about cutting the bridge or breaking the truck.", C, 1.2),
    S("t03-engineers", "Hours passed. Nobody knew what to do.", C, 1.3),
    S("t05-girl", "Then a little girl in a car nearby said,", pause=True),
    S("t05-girl", "\"Why don't you just let some air out of the tyres?\"", C, 1.3, sfx=["sparkle"]),
    S("t06-quiet", "Everyone went quiet.", sfx=["heartbeat"]),
    S("t07-tyre", "They let the air out.", sfx=["whoosh2"]),
    S("t08-free", "The truck dropped a few centimetres and rolled free.", sfx=["sparkle"]),
    S("k1-hero", "When you're stuck, stop overthinking.", pause=True),
    END("k1-hero", "Look for the simple answer."),
], "When you're stuck, stop overthinking.")
R["ryokan-moon"] = ("echoes", [
    HOOK("h0-moon", "How would you treat someone|who came to rob you?", "man-face", 1.2),
    S("r01-hut", "An old monk lived alone in a tiny hut on a mountain.", pause=True),
    S("r01-hut", "He owned nothing.", C, 1.3),
    S("r02-thief", "One night, a thief broke in and found nothing to steal.", sfx=["bass"]),
    S("r03-home", "The monk came home and saw him.", pause=True, sfx=["heartbeat"]),
    S("r03-home", "\"You came all this way. You shouldn't leave with nothing.\"", C, 1.25),
    S("r04-robe", "He took off his own robe and gave it to him.", sfx=["sparkle"]),
    S("r05-run", "The thief ran away, confused.", sfx=["whoosh2"]),
    S("h0-moon", "The monk sat outside, looking at the full moon.", "wide", 1.0, pause=True),
    S("r06-sit", "\"Poor man.", "man-face", 1.2),
    S("r06-sit", "I wish I could have given him this beautiful moon.\"", "man-face", 1.5, punch=True),
    S("k1-moon", "Kindness is the one thing", pause=True),
    END("k1-moon", "nobody can steal from you."),
], "Kindness is the one thing")
R["wind-sun"] = ("echoes", [
    HOOK("h0-duel", "Force will never win|against kindness.", C, 1.3),
    S("s01-argue", "The wind and the sun argued about who was stronger.", pause=True),
    S("s02-walker", "They saw a man walking in a coat."),
    S("s01-argue", "\"Whoever makes him take off his coat wins,\" said the sun.", C, 1.25),
    S("s03-blow", "The wind went first.", pause=True, sfx=["whoosh"]),
    S("s03-blow", "He blew harder and harder.", C, 1.3, sfx=["whoosh2"]),
    S("s04-hold", "But the colder it got, the tighter the man held his coat.", sfx=["heartbeat"]),
    S("s05-shine", "Then the sun came out.", pause=True, sfx=["sparkle"]),
    S("s05-shine", "He shone softly and warmly.", C, 1.25),
    S("s06-warm", "The man smiled, wiped his forehead", sfx=["pop"]),
    S("s07-coat", "and took off his coat. The sun won.", sfx=["sparkle"]),
    S("k1-hero", "You can't force people to change.", pause=True),
    END("k1-hero", "But warmth makes them open up on their own."),
], "Then the sun came out.")
R["dog-bone"] = ("tense", [
    HOOK("h0-drop", "Greed will make you lose|what you already have.", C, 1.3),
    S("d01-find", "A dog found a big juicy bone", pause=True, sfx=["sparkle"]),
    S("d02-run", "and ran home with it in his mouth."),
    S("d03-bridge", "He crossed a little bridge over a river.", sfx=["whoosh2"]),
    S("d04-look", "Looking down, he saw another dog in the water", pause=True),
    S("d04-look", "holding an even bigger bone.", C, 1.35),
    S("d05-want", "He wanted that one too.", C, 1.3, sfx=["heartbeat"]),
    S("h0-drop", "So he barked at it.", "wide", 1.0, sfx=["bass"]),
    S("d06-sink", "And when he opened his mouth, his bone fell into the river and sank.", sfx=["glitch"]),
    S("d04-look", "There was no other dog. It was only his reflection.", "wide", 1.0, pause=True),
    S("d07-empty", "He went home with nothing.", C, 1.3, sfx=["wrong"]),
    S("k1-hero", "Be grateful for what you have,", pause=True),
    END("k1-hero", "or you might lose it chasing what isn't real."),
], "Be grateful for what you have,")
R["golden-goose"] = ("tense", [
    HOOK("h0-egg", "Being impatient can destroy|your best opportunity.", C, 1.3),
    S("g01-goose", "A poor farmer owned a goose.", pause=True),
    S("g02-find", "One morning, he found a shining golden egg in her nest.", sfx=["sparkle"]),
    S("h0-egg", "Every day after that, the goose laid one golden egg.", "wide", 1.0),
    S("g03-rich", "The farmer became rich.", sfx=["sparkle"]),
    S("g04-greedy", "But he wanted more. And he wanted it faster.", pause=True, sfx=["heartbeat"]),
    S("g04-greedy", "\"If she makes gold every day, she must be full of gold inside.\"", "man-face", 1.3),
    S("g05-knife", "So he killed the goose and cut her open.", sfx=["bass"]),
    S("g06-nothing", "There was nothing inside.", pause=True),
    S("g06-nothing", "No gold. And no more eggs.", "man-face", 1.4, punch=True, sfx=["wrong"]),
    S("k1-patient", "Some things grow slowly for a reason.", pause=True),
    END("k1-patient", "Don't destroy what feeds you because you can't wait."),
], "Some things grow slowly for a reason.")
R["bell-cat"] = ("echoes", [
    HOOK("h0-bell", "Anyone can have an idea.|Very few will act on it.", C, 1.3),
    S("b01-cat", "The mice were tired of being hunted by the cat.", pause=True, sfx=["bass"]),
    S("b02-meeting", "So they held a big meeting."),
    S("b03-idea", "One young mouse stood up. \"I have a plan.", pause=True),
    S("b03-idea", "We tie a bell around the cat's neck.", C, 1.3, sfx=["sparkle"]),
    S("b03-idea", "Then we'll always hear it coming.\"", "wide", 1.05),
    S("b04-cheer", "Everyone cheered. What a brilliant idea!", sfx=["pop"]),
    S("b05-old", "Then an old mouse asked one quiet question.", pause=True),
    S("b05-old", "\"Who will put the bell on the cat?\"", C, 1.4, punch=True, sfx=["bass"]),
    S("b06-silence", "Silence. Nobody moved. Nobody volunteered.", sfx=["heartbeat"]),
    S("k1-hero", "Ideas don't change anything.", pause=True),
    S("k1-hero", "The person brave enough to act does.", "man-face", 1.3),
    END("k1-hero", "Be that person."),
], "Ideas don't change anything.")
R["bundle-sticks"] = ("echoes", [
    HOOK("h0-strain", "Alone you can be broken.|Together you are strong.", C, 1.3),
    S("s01-fight", "An old father had sons who were always fighting.", pause=True, sfx=["glitch"]),
    S("s02-give", "One day, he gave each son a single stick. \"Break it.\""),
    S("s03-snap", "They snapped them easily.", sfx=["pop"]),
    S("s04-bundle", "Then he tied a bundle of sticks together with a rope.", pause=True),
    S("s04-bundle", "\"Now break this.\"", "man-face", 1.35),
    S("s05-try", "Each son tried as hard as he could.", sfx=["heartbeat"]),
    S("h0-strain", "Nobody could break it.", C, 1.35, punch=True),
    S("s06-father", "\"Alone, anyone can break you,\" the father said.", pause=True),
    S("s06-father", "\"But together, nobody can.\"", "man-face", 1.45, punch=True, sfx=["sparkle"]),
    S("k1-hug", "The brothers looked at each other and stopped fighting."),
    S("k1-hug", "Stay close to the people you love.", C, 1.25, pause=True),
    END("k1-hug", "Together you are unbreakable."),
], "Stay close to the people you love.")
R["fox-crow-cheese"] = ("tense", [
    HOOK("h0-fall", "Be careful of people|who only tell you what you want to hear.", C, 1.3),
    S("f01-crow", "A crow found a piece of cheese and flew up to a branch.", pause=True),
    S("f02-fox", "A hungry fox saw her.", sfx=["heartbeat"]),
    S("f03-praise", "\"What a beautiful bird,\" said the fox.", pause=True),
    S("f03-praise", "\"Your feathers shine. Your eyes sparkle.", C, 1.25, sfx=["sparkle"]),
    S("f04-proud", "I bet your voice is the most beautiful of all.", C, 1.2),
    S("f03-praise", "Won't you sing for me?\"", C, 1.4, punch=True),
    S("f04-proud", "The crow felt so proud.", C, 1.35),
    S("h0-fall", "She opened her beak to sing. The cheese fell straight down.", "wide", 1.0, sfx=["bass"]),
    S("f05-catch", "The fox caught it and ran away laughing.", sfx=["wrong"]),
    S("f06-sad", "Flattery is often bait.", pause=True),
    S("k1-hero", "When someone praises you too sweetly,", "wide", 1.0),
    END("k1-hero", "check what they're trying to take."),
], "Flattery is often bait.")
R["four-oxen"] = ("tense", [
    HOOK("h0-circle", "This is how strong people|are defeated.", C, 1.3),
    S("o01-field", "Four oxen lived together in a field.", pause=True),
    S("o02-lion", "A lion wanted to eat them.", sfx=["heartbeat"]),
    S("h0-circle", "But whenever he came close, they stood back to back, horns facing out.", "wide", 1.0),
    S("h0-circle", "He couldn't attack.", C, 1.4, punch=True),
    S("o03-whisper", "So the lion became clever.", pause=True),
    S("o03-whisper", "He whispered lies to each ox about the others.", C, 1.3),
    S("o04-argue", "Slowly, they began to argue. Then they stopped talking.", sfx=["glitch"]),
    S("o05-alone", "Finally, each ox went to graze alone in a different corner of the field.", pause=True),
    S("o06-hunt", "One by one, the lion hunted them all.", sfx=["bass"]),
    S("k1-hero", "Don't let anyone divide you from your people.", pause=True),
    END("k1-hero", "United, you are safe."),
], "Don't let anyone divide you from your people.")

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
