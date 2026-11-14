"""reel.json for parable reels 61-70. Usage: python3 build70.py [slug ...]  (helpers from build40/build50)

Shots that render longer than 3.1 s are listed in split70.json and cut automatically at a phrase break."""
import json
import sys
from pathlib import Path

import build50
from build40 import C, END, HOOK, MUS, S

HERE = Path(__file__).parent
LONG = json.load(open(HERE / "split70.json")) if (HERE / "split70.json").exists() else {}
VOICE = {}
R = {}
R["kintsugi-bowl"] = ("echoes", [
    HOOK("h0-gold", "Your scars might be|the most beautiful thing about you.", C, 1.3),
    S("k01-drop", "A rich man dropped his favourite tea bowl.", pause=True, sfx=["bass"]),
    S("k02-shards", "It shattered into pieces.", C, 1.25, sfx=["glitch"]),
    S("k03-sad", "He was heartbroken.", "man-face", 1.3, sfx=["heartbeat"]),
    S("k04-glue", "Instead of throwing it away,", pause=True),
    S("k04-glue", "a craftsman glued the pieces back together with gold.", C, 1.3, sfx=["sparkle"]),
    S("h0-gold", "Every crack became a shining golden line.", "wide", 1.0, sfx=["sparkle"]),
    S("k05-gasp", "When the man saw it, he gasped.", "man-face", 1.3),
    S("k05-gasp", "\"It's more beautiful than before.\"", "wide", 1.05),
    S("k06-smile", "The craftsman smiled.", pause=True),
    S("k06-smile", "\"Because now it has a story.\"", C, 1.3, punch=True),
    S("h0-gold", "In Japan, this is called Kintsugi.", C, 1.5, sfx=["sparkle"]),
    S("k1-hold", "You don't have to hide your broken parts.", pause=True),
    END("k1-hold", "They're where the gold goes."),
], "You don't have to hide your broken parts.")
R["farmer-best-corn"] = ("echoes", [
    HOOK("h0-wind", "Want to win?|Help the people around you win.", C, 1.3),
    S("c01-prize", "A farmer won the prize for the best corn every single year.", pause=True, sfx=["sparkle"]),
    S("c02-seeds", "A reporter found out he shared his best seeds", sfx=["pop"]),
    S("c02-seeds", "with all his neighbours.", C, 1.25),
    S("c03-reporter", "\"Why would you help your competition?\"", sfx=["whoosh2"]),
    S("c04-explain", "The farmer smiled.", "man-face", 1.3, pause=True),
    S("h0-wind", "\"The wind carries pollen from field to field.", "wide", 1.0),
    S("c05-bad", "If my neighbours grow bad corn,", sfx=["heartbeat"]),
    S("c05-bad", "the wind brings it to my field, and my corn gets worse.\"", C, 1.3),
    S("c06-neighbors", "To grow good corn,", pause=True),
    S("c06-neighbors", "he had to help his neighbours grow good corn.", C, 1.25, sfx=["sparkle"]),
    S("k1-together", "Your success is tied to the people around you.", pause=True),
    END("k1-together", "Lift them, and you rise."),
], "Your success is tied to the people around you.")
R["eagle-rebirth"] = ("tense", [
    HOOK("h0-strike", "Sometimes you have to break yourself|to survive.", C, 1.3),
    S("e01-old", "An old eagle's claws grew weak.", pause=True),
    S("e01-old", "Its beak became long and bent. Its feathers grew heavy.", C, 1.3),
    S("e02-hunt", "It couldn't hunt anymore.", sfx=["wrong"]),
    S("e03-choice", "It had two choices.", pause=True, sfx=["heartbeat"]),
    S("e03-choice", "Die, or go through a painful change.", C, 1.35, punch=True),
    S("e04-fly-up", "The eagle flew to a mountaintop.", sfx=["whoosh2"]),
    S("h0-strike", "It struck its old beak against a rock until it broke off.", "wide", 1.0, sfx=["bass"]),
    S("e05-wait", "It waited for a new one to grow.", sfx=["heartbeat"]),
    S("e05-wait", "Then it pulled out its old claws. Then its heavy feathers.", C, 1.3),
    S("e06-new", "Five months later,", pause=True),
    S("e07-soar", "it flew again, stronger than ever.", sfx=["sparkle"]),
    S("k1-hero", "Growth hurts.", pause=True),
    END("k1-hero", "But staying the same hurts more."),
], "Five months later,")
R["rich-poor-trip"] = ("echoes", [
    HOOK("h0-stars", "This boy taught his rich father|what wealth really means.", "man-face", 1.2),
    S("r01-car", "A rich father took his son to the countryside", pause=True),
    S("r01-car", "to show him how poor people live.", C, 1.2),
    S("r02-farm", "They stayed a few days with a poor family."),
    S("r03-ask", "On the way home, the father asked,", pause=True),
    S("r03-ask", "\"So, what did you learn?\"", C, 1.3),
    S("r04-dogs", "\"We have one dog. They have four.", sfx=["pop"]),
    S("r05-river", "We have a pool. They have a whole river.", sfx=["pop"]),
    S("h0-stars", "We have lamps. They have the stars.", "wide", 1.0, sfx=["sparkle"]),
    S("r06-food", "We buy our food. They grow theirs.\"", sfx=["pop"]),
    S("r07-dad", "The father was speechless.", pause=True, sfx=["heartbeat"]),
    S("k1-boy", "The boy added, \"Thanks, Dad,", "man-face", 1.2),
    S("k1-boy", "for showing me how poor we are.\"", "man-face", 1.6, punch=True, sfx=["bass"]),
    S("h0-stars", "Wealth isn't what you own.", "wide", 1.0, pause=True),
    END("h0-stars", "It's what you see."),
], "Wealth isn't what you own.")
R["words-feathers"] = ("tense", [
    HOOK("h0-feathers", "Be careful.|Your words can cut deeper than a knife.", "man-face", 1.2),
    S("w01-shout", "A little boy shouted at his friend in anger.", pause=True, sfx=["bass"]),
    S("w01-shout", "He said terrible things.", C, 1.3, punch=True),
    S("w02-sorry", "Later, he felt sorry and apologised.", sfx=["whoosh2"]),
    S("w02-sorry", "But his friend stayed quiet.", C, 1.3, sfx=["heartbeat"]),
    S("w03-pillow", "His grandmother took him outside", pause=True),
    S("w03-pillow", "and gave him a pillow full of feathers.", C, 1.25),
    S("w04-climb", "\"Climb the hill and scatter them in the wind.\""),
    S("h0-feathers", "He did.", "wide", 1.0, sfx=["whoosh"]),
    S("w05-wind", "\"Now go and collect every feather.\"", pause=True),
    S("w06-search", "\"That's impossible! The wind took them everywhere.\"", sfx=["wrong"]),
    S("w07-gran", "\"Words are like feathers.", pause=True),
    S("w07-gran", "Once they're out, you can never take them all back.\"", C, 1.3, punch=True),
    END("k1-think", "Think before you speak."),
], "\"Words are like feathers.")
R["lion-mouse"] = ("tense", [
    HOOK("h0-chew", "The smallest one in the room|is not always the weakest.", C, 1.3),
    S("l01-sleep", "A lion was sleeping when a tiny mouse ran over his face.", pause=True),
    S("l02-catch", "The lion caught him, ready to eat him.", sfx=["bass"]),
    S("l03-beg", "\"Please let me go! One day, I'll help you.\"", C, 1.25),
    S("l04-laugh", "The lion laughed.", sfx=["pop"]),
    S("l04-laugh", "\"How could a tiny mouse ever help me?\"", C, 1.25),
    S("l04-laugh", "But he let him go.", "wide", 1.0),
    S("l05-net", "Weeks later, hunters caught the lion in a strong rope net.", pause=True, sfx=["glitch"]),
    S("l05-net", "He roared, but couldn't escape.", C, 1.3, punch=True),
    S("h0-chew", "Then the mouse appeared.", "wide", 1.0, pause=True),
    S("h0-chew", "He chewed through the ropes, one by one,", C, 1.35),
    S("l07-free", "until the lion was free.", sfx=["sparkle"]),
    S("k1-hero", "Never underestimate anyone.", pause=True),
    END("k1-hero", "Even the smallest friend can save you."),
], "Never underestimate anyone.")
R["bag-on-cart"] = ("echoes", [
    HOOK("h0-ride", "Why are you|still carrying yesterday?", "man-face", 1.2),
    S("b01-walk", "A traveller was walking with a heavy bag.", pause=True),
    S("b02-offer", "A farmer offered him a ride on his cart.", sfx=["whoosh2"]),
    S("h0-ride", "The traveller climbed on,", "wide", 1.0),
    S("h0-ride", "but kept the heavy bag on his shoulder.", "man-face", 1.35),
    S("b03-ask", "The farmer asked, \"Why don't you put the bag down?\"", pause=True),
    S("b04-answer", "\"Oh, you're already carrying me.", "man-face", 1.2),
    S("b04-answer", "I don't want to make it heavier for you.\"", "wide", 1.05),
    S("b05-laugh", "The farmer laughed.", sfx=["pop"]),
    S("b05-laugh", "\"The cart carries you and the bag either way.\"", C, 1.3),
    S("k1-down", "Life is carrying you.", pause=True),
    S("k1-down", "Stop holding your worries on your shoulders.", "man-face", 1.3),
    END("k1-down", "Put the bag down and enjoy the ride."),
], "Life is carrying you.")
R["busy-beggar"] = ("tense", [
    HOOK("h0-gold", "You might be sitting|on a treasure right now.", C, 1.3),
    S("g01-beg", "A beggar sat on an old wooden box by the road", pause=True),
    S("g02-years", "for thirty years, asking for coins.", sfx=["heartbeat"]),
    S("g03-stranger", "One day, a stranger walked by.", pause=True),
    S("g03-stranger", "\"I have nothing to give.", C, 1.2),
    S("g03-stranger", "But what's in that box you're sitting on?\"", "wide", 1.05),
    S("g04-shrug", "\"Nothing. It's just an old box.\"", "man-face", 1.2),
    S("g03-stranger", "\"Have you ever looked inside?\"", C, 1.3, sfx=["pop"]),
    S("g04-shrug", "\"No. Why would I?\"", "man-face", 1.5),
    S("g05-open", "The stranger insisted. The beggar pried open the lid.", pause=True),
    S("h0-gold", "It was full of gold.", C, 1.4, punch=True, sfx=["sparkle"]),
    S("g06-shock", "For thirty years, he begged while sitting on treasure.", "man-face", 1.3),
    END("k1-within", "Stop looking outside for what's already inside you."),
], "For thirty years, he begged while sitting on treasure.")
R["hedgehogs-winter"] = ("echoes", [
    HOOK("h0-ouch", "Every relationship has thorns.|Here's how to survive them.", C, 1.3),
    S("q01-cold", "On a freezing winter night,", pause=True),
    S("q02-huddle", "a group of hedgehogs huddled together to stay warm.", sfx=["sparkle"]),
    S("h0-ouch", "But their sharp spines pricked each other.", "wide", 1.0, sfx=["glitch"]),
    S("q03-apart", "So they moved apart.", sfx=["whoosh2"]),
    S("q04-freeze", "Then they began to freeze.", sfx=["heartbeat"]),
    S("q02-huddle", "So they moved close again.", C, 1.25),
    S("h0-ouch", "And got hurt again.", C, 1.5, punch=True, sfx=["glitch"]),
    S("q05-balance", "Finally, they found the right distance.", pause=True, sfx=["sparkle"]),
    S("q05-balance", "Close enough to stay warm. Far enough not to hurt each other.", C, 1.25),
    S("q06-dawn", "That's how they survived the winter."),
    S("k1-hero", "No one is perfect.", pause=True),
    END("k1-hero", "Learn to live with other people's thorns, and take the warmth they give."),
], "Finally, they found the right distance.")
R["search-within"] = ("echoes", [
    HOOK("h0-mirror", "Everything you're searching for|is already in you.", "man-face", 1.2),
    S("s01-travel", "A young man travelled for years looking for God.", pause=True),
    S("s02-desert", "He crossed mountains and deserts.", sfx=["whoosh2"]),
    S("s03-temples", "He visited every temple."),
    S("s04-monk", "Finally, an old monk asked him,", pause=True),
    S("s04-monk", "\"Why are you searching so hard?\"", C, 1.25),
    S("s03-temples", "\"Because I want to find God.\"", "man-face", 1.3),
    S("s05-give", "The monk handed him a mirror.", sfx=["sparkle"]),
    S("h0-mirror", "The young man looked into it and saw only himself.", "wide", 1.0),
    S("h0-mirror", "\"I don't understand.\"", "man-face", 1.5, punch=True),
    S("s06-smile", "The monk smiled.", pause=True),
    S("s06-smile", "\"You walked a thousand miles to find what was with you the whole time.\"", C, 1.25),
    S("k1-within", "Stop searching everywhere.", pause=True),
    END("k1-within", "Look within."),
], "Stop searching everywhere.")

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
