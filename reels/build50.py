"""reel.json for parable reels 41-50. Usage: python3 build50.py [slug ...]  (helpers shared with build40.py)"""
import json
import sys
from pathlib import Path

from build40 import C, END, HOOK, MUS, S

LONG = json.load(open(Path(__file__).parent / "split50.json")) if (Path(__file__).parent / "split50.json").exists() else {}


def split(s):
    """Cut a shot longer than 3.1 s at the phrase break nearest its middle; the second half reframes the same image."""
    w = s["text"].split()
    breaks = [i for i in range(1, len(w)) if w[i - 1][-1] in ",.!?:;"] or [len(w) // 2]
    k = min(breaks, key=lambda i: abs(i - len(w) / 2))
    a, b = dict(s), dict(s)
    a["text"], b["text"] = " ".join(w[:k]), " ".join(w[k:])
    if s.get("drift", 0) < 0:                     # closing pull-out: keep it on the second half
        a.update(focus="wide", zoom=1.0, drift=0.05, sfx=[x for x in s["sfx"] if isinstance(x, dict) and x.get("at", 0) < 0])
        b["sfx"] = [x for x in s["sfx"] if not (isinstance(x, dict) and x.get("at", 0) < 0)]
    else:
        b.pop("pause_before", None); b.pop("flash", None)
        b.update(focus=C if s["focus"] == "wide" else s["focus"], zoom=round(s["zoom"] + 0.25, 2), sfx=[])
        b.pop("punch", None); b["drift"] = 0.05
        if s.get("punch"):
            a.pop("punch"); a["drift"] = 0.05; b["punch"] = True; b.pop("drift")
    return [a, b]


VOICE = {"echo-life": "voice-cand-3.wav", "planting-tree": "voice-cand-3.wav"}
R = {}
R["echo-life"] = ("echoes", [
    HOOK("h0-shout", "Whatever you send out|comes back to you.", "man-face", 1.2),
    S("e01-walk", "A little boy was walking in the mountains", pause=True),
    S("e01-walk", "with his father.", C, 1.2),
    S("e02-trip", "He tripped and shouted, \"Ow!\"", sfx=["pop"]),
    S("e03-echo", "From the mountains, a voice shouted back,", sfx=["whoosh2"]),
    S("e03-echo", "\"Ow!\"", C, 1.4, punch=True, sfx=["pop"]),
    S("e04-who", "Surprised, he yelled, \"Who are you?\"", "man-face", 1.2),
    S("e03-echo", "\"Who are you?\" came the answer.", "wide", 1.05, sfx=["whoosh2"]),
    S("e05-angry", "Angry, he screamed, \"I hate you!\"", sfx=["bass"]),
    S("e03-echo", "\"I hate you!\"", C, 1.5, punch=True, sfx=["glitch"]),
    S("e06-father", "His father smiled and shouted,", pause=True),
    S("e06-father", "\"You are amazing!\"", C, 1.35, punch=True, sfx=["sparkle"]),
    S("e03-echo", "The voice answered, \"You are amazing!\"", "wide", 1.1, sfx=["sparkle"]),
    S("e07-amazed", "\"Son, this is called an echo.", pause=True),
    S("e07-amazed", "But really, it's life.\"", "man-face", 1.4, punch=True),
    S("k1-sunset", "Give love, and love comes back.", pause=True),
    END("k2-love", "Give hate, and hate comes back."),
], "His father smiled and shouted,")
R["empty-boat"] = ("tense", [
    HOOK("h0-yell", "Your anger|is not caused by other people.", "man-face", 1.2),
    S("b01-row", "A man was rowing his boat", pause=True),
    S("b01-row", "on a quiet lake in the fog.", "wide", 1.1),
    S("b02-crash", "Suddenly, another boat crashed into his.", sfx=["bass"]),
    S("b03-furious", "He was furious.", "man-face", 1.3, punch=True),
    S("b04-shout", "\"Watch where you're going!\" he shouted.", sfx=["glitch"]),
    S("b04-shout", "\"Are you blind?\"", "man-face", 1.5, punch=True),
    S("b05-empty", "But when the fog cleared,", pause=True),
    S("b05-empty", "he saw the other boat was empty.", C, 1.3, sfx=["heartbeat"]),
    S("b05-empty", "It had just drifted loose.", "wide", 1.05),
    S("b06-calm", "His anger disappeared.", "man-face", 1.3, sfx=["sparkle"]),
    S("b07-push", "There was no one to blame.", "wide", 1.0),
    S("b07-push", "The crash was the same.", "man-face", 1.3),
    S("k1-sunrise", "Only his story changed.", pause=True),
    S("k1-sunrise", "Every time someone", "wide", 1.05),
    S("k1-sunrise", "hits your boat, remember:", "man-face", 1.3),
    END("k2-peace", "maybe they're just an empty boat."),
], "Only his story changed.")
R["wooden-bowl"] = ("tense", [
    HOOK("h0-corner", "Your children will treat you|the way you treat your parents.", C, 1.3),
    S("w01-spill", "An old grandfather's hands were shaking.", pause=True),
    S("w01-spill", "He spilled food and broke plates.", C, 1.3, sfx=["glitch"]),
    S("w02-send", "So his son made him eat alone,", sfx=["whoosh2"]),
    S("h0-corner", "in the corner, from a wooden bowl.", C, 1.25, sfx=["heartbeat"]),
    S("w04-carve", "One evening, the son saw his little boy", pause=True),
    S("w04-carve", "carving a piece of wood.", C, 1.3),
    S("w05-ask", "\"What are you making?\"", "man-face", 1.4),
    S("w06-answer", "\"A bowl for you and Mom,", C, 1.2),
    S("w06-answer", "for when you get old.\"", C, 1.5, punch=True, sfx=["bass"]),
    S("w07-tears", "The son froze.", "man-face", 1.3),
    S("w07-tears", "Tears filled his eyes.", "man-face", 1.7, punch=True),
    S("k1-lead", "That night, he led his father back to the table.", pause=True),
    S("k2-family", "And never sent him away again.", "wide", 1.0, sfx=["sparkle"]),
    S("k2-family", "Children don't listen to what you say.", C, 1.2),
    END("k2-family", "They copy what you do."),
], "That night, he led his father back to the table.")
R["thousand-mirrors"] = ("echoes", [
    HOOK("h0-growl", "The world you see|is a reflection of you.", C, 1.3),
    S("m01-house", "There was a house with a thousand mirrors.", pause=True),
    S("m02-enter", "A happy little dog walked in, wagging its tail.", sfx=["pop"]),
    S("m03-wag", "A thousand dogs wagged back.", C, 1.25, sfx=["sparkle"]),
    S("m04-leave", "It left thinking, \"What a friendly place.\""),
    S("m05-enter2", "Later, an angry dog walked in, growling.", pause=True, sfx=["bass"]),
    S("m06-many", "A thousand dogs growled back.", C, 1.3, punch=True, sfx=["glitch"]),
    S("m07-run", "It ran out thinking,", sfx=["whoosh2"]),
    S("m07-run", "\"What a terrible place.\"", C, 1.3),
    S("m01-house", "Same house. Same mirrors.", "wide", 1.0, pause=True),
    S("m03-wag", "Different dogs.", C, 1.4, punch=True),
    S("k1-mirror", "If everyone around you seems angry,", pause=True),
    S("k1-mirror", "check what you're bringing into the room.", "man-face", 1.35),
    S("k1-mirror", "The world is a mirror.", "wide", 1.0),
    END("k2-smile", "Smile first."),
], "If everyone around you seems angry,")
R["insult-gift"] = ("tense", [
    HOOK("h0-face", "Someone insults you.|Here's the smartest way to respond.", C, 1.25),
    S("i01-come", "An angry man walked up to a calm monk", pause=True),
    S("i02-insult", "and insulted him for an hour.", sfx=["glitch"]),
    S("i03-smile", "The monk just listened, smiling.", "man-face", 1.25),
    S("i04-why", "Finally, the man shouted,", sfx=["bass"]),
    S("i04-why", "\"Why don't you say anything?\"", C, 1.35, punch=True),
    S("i05-gift", "The monk asked, \"If someone offers you a gift,", pause=True),
    S("i05-gift", "and you don't accept it,", C, 1.25),
    S("i05-gift", "who does it belong to?\"", "man-face", 1.5, punch=True),
    S("i06-think", "\"To the one who offered it.\"", C, 1.2),
    S("i07-exact", "\"Exactly. I don't accept your anger.", "man-face", 1.3, sfx=["sparkle"]),
    S("i07-exact", "So it still belongs to you.\"", "man-face", 1.7, punch=True),
    S("i08-leave", "The man walked away", sfx=["whoosh2"]),
    S("i08-leave", "speechless.", C, 1.3, punch=True),
    S("k1-calm", "Their insult is their gift.", pause=True),
    END("k1-calm", "You don't have to take it.", "man-face"),
], "\"Exactly. I don't accept your anger.")
R["bird-branch"] = ("tense", [
    HOOK("h0-crack", "Stop depending on the branch.|Trust your wings.", C, 1.3),
    S("r01-sit", "A bird sat on a thin dry branch.", pause=True),
    S("r02-wind", "The wind grew stronger,", sfx=["whoosh2"]),
    S("r02-wind", "and the branch began to shake.", C, 1.25),
    S("r03-break", "Then it cracked.", C, 1.3, punch=True, sfx=["glitch"]),
    S("r04-animals", "The other animals watched, worried.", sfx=["heartbeat"]),
    S("r04-animals", "\"The branch is breaking! The bird will fall!\"", C, 1.3),
    S("r05-calm", "But the bird didn't panic.", pause=True),
    S("r05-calm", "It didn't even look down.", C, 1.4, punch=True),
    S("r06-fly", "When the branch broke,", sfx=["bass"]),
    S("r06-fly", "the bird simply opened its wings", "wide", 1.0),
    S("r07-sky", "and flew.", C, 1.2, sfx=["sparkle"]),
    S("r07-sky", "Its trust was never in the branch.", pause=True),
    S("r07-sky", "It was in its own", "wide", 1.05),
    S("r07-sky", "wings.", C, 1.5, punch=True, sfx=["sparkle"]),
    S("k0-box", "Jobs break.", pause=True, sfx=["heartbeat"]),
    S("k0-box", "People leave.", "man-face", 1.3, sfx=["heartbeat"]),
    S("k0-box", "Plans fail.", "wide", 1.1, sfx=["heartbeat"]),
    S("k1-wings", "Build your wings,", "man-face", 1.3),
    END("k1-wings", "and no branch can scare you."),
], "Its trust was never in the branch.")
R["planting-tree"] = ("echoes", [
    HOOK("h0-plant", "The best things you do might be|for people you'll never meet.", "man-face", 1.2),
    S("t01-dig", "An old man was planting a small mango tree.", pause=True),
    S("t02-laugh", "A young man laughed.", sfx=["pop"]),
    S("t02-laugh", "\"You're ninety! You'll never eat its fruit.\"", C, 1.25),
    S("t03-keep", "The old man kept digging.", "man-face", 1.25),
    S("t04-memory", "\"When I was a boy, I ate mangoes", pause=True),
    S("t04-memory", "from trees I didn't plant.", C, 1.25),
    S("t03-keep", "Someone planted them for me.\"", "man-face", 1.5, punch=True),
    S("t05-pat", "He patted the soil gently.", sfx=["sparkle"]),
    S("t05-pat", "\"Now I'm planting for someone else.\"", "man-face", 1.4, punch=True),
    S("t06-years", "Years later, the young man sat under that tree", pause=True),
    S("t06-years", "with his children, eating its fruit.", C, 1.25),
    S("t07-understand", "And he finally understood.", C, 1.2),
    S("k1-sapling", "Plant trees whose shade", pause=True),
    END("k1-sapling", "you'll never sit in.", "man-face"),
], "\"When I was a boy, I ate mangoes")
R["frogs-cream"] = ("tense", [
    HOOK("h0-kick", "This tiny story could change|how you face problems.", C, 1.3),
    S("c01-fall", "Two frogs fell into a deep bucket of cream.", pause=True, sfx=["pop"]),
    S("c02-walls", "The walls were too slippery to climb.", sfx=["wrong"]),
    S("c03-sink", "The first frog said, \"It's hopeless,\"", sfx=["heartbeat"]),
    S("c03-sink", "stopped swimming, and sank.", C, 1.35, punch=True),
    S("c04-tired", "The second frog was just as tired.", pause=True),
    S("c04-tired", "But he refused to give up.", C, 1.4, punch=True, sfx=["bass"]),
    S("c05-kicking", "He kicked. And kicked. And kicked.", sfx=["pop", {"name": "pop", "at": 0.6}, {"name": "pop", "at": 1.2}]),
    S("c05-kicking", "Hours passed.", C, 1.3),
    S("c06-butter", "Slowly, his kicking churned the cream into butter.", pause=True, sfx=["sparkle"]),
    S("c06-butter", "It became solid.", C, 1.35, punch=True),
    S("c07-jump", "He climbed on top and jumped out.", sfx=["whoosh"]),
    S("k1-climb", "When you feel like quitting, keep kicking.", pause=True),
    S("k2-top", "Your problem might turn into", "man-face", 1.3),
    END("k2-top", "the ground you stand on."),
], "Slowly, his kicking churned the cream into butter.")
R["leather-shoes"] = ("tense", [
    HOOK("h0-feet", "Stop trying|to change the whole world.", "man-face", 1.2),
    S("l01-walk", "A king walked barefoot across his kingdom", pause=True),
    S("h0-feet", "and came back with bleeding feet.", "wide", 1.05, sfx=["glitch"]),
    S("l02-order", "Angry, he ordered,", sfx=["bass"]),
    S("l02-order", "\"Cover every road in my kingdom with leather!\"", "man-face", 1.3),
    S("l03-ministers", "His ministers panicked.", sfx=["heartbeat"]),
    S("l04-cows", "That would take every cow in the land.", C, 1.2),
    S("l05-servant", "Then a wise servant stepped forward.", pause=True),
    S("l05-servant", "\"My king, why not just cover your own feet?\"", C, 1.25, sfx=["sparkle"]),
    S("l06-laugh", "The king laughed", "man-face", 1.2),
    S("l07-shoes", "and made the first pair of shoes.", sfx=["pop"]),
    S("k1-wear", "You can't change every person,", pause=True),
    S("k1-wear", "every road, every problem.", "wide", 1.1),
    S("l07-shoes", "But you can change yourself.", "man-face", 1.4, punch=True),
    END("k1-wear", "Wear your shoes."),
], "You can't change every person,")
R["two-bricks"] = ("tense", [
    HOOK("h0-stare", "You are judging yourself|completely wrong.", "man-face", 1.2),
    S("k01-build", "A young monk built his first brick wall.", pause=True),
    S("k02-care", "He worked slowly, placing every brick with care.", "man-face", 1.15),
    S("k03-done", "When it was finished,", sfx=["whoosh2"]),
    S("k04-crooked", "he saw two bricks crooked.", C, 1.4, punch=True, sfx=["wrong"]),
    S("k05-ashamed", "He was ashamed.", "man-face", 1.2, sfx=["heartbeat"]),
    S("k05-ashamed", "He wanted to tear the whole wall down.", "wide", 1.0),
    S("k06-visitor", "One day, a visitor said,", pause=True),
    S("k06-visitor", "\"What a beautiful wall.\"", C, 1.25, sfx=["sparkle"]),
    S("k07-point", "\"Can't you see the two bad bricks?\"", "man-face", 1.3),
    S("k07-point", "\"Yes. But I also see", "wide", 1.0),
    S("k04-crooked", "nine hundred and ninety-eight good ones.\"", "wide", 1.0, sfx=["sparkle"]),
    S("k08-cry", "The monk looked again and cried.", "man-face", 1.3),
    S("k1-whole", "You are not your two bad bricks.", pause=True),
    END("k1-whole", "Look at the whole wall."),
], "One day, a visitor said,")

if __name__ == "__main__":
    here = Path(__file__).parent
    for slug in sys.argv[1:] or R:
        m1, shots, sw = R[slug]
        shots = [x for s in shots for x in (s if isinstance(s, list) else [s])]
        shots = [x for s in shots for x in (split(s) if s["text"] in LONG.get(slug, ()) else [s])]
        i = next(n for n, s in enumerate(shots) if sw.startswith(s["text"]))
        cue = lambda k, n: {"music": f"../audio/music/{MUS[k][0]}.mp3", "start": MUS[k][1], "shot": n}
        d = {"out": f"../output/{slug}.mp4", "audio": [VOICE.get(slug, "voice-cand-1.wav")], "speed": 1.0,
             "music_volume": 0.4, "fade_out": 1.0, "music_cues": [cue(m1, 0), cue("warm", i)], "shots": shots}
        json.dump(d, open(here / slug / "reel.json", "w"), indent=1)
        print(slug, len(shots))
