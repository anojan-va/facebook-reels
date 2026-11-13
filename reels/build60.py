"""reel.json for parable reels 51-60. Usage: python3 build60.py [slug ...]  (helpers from build40/build50)

Shots that render longer than 3.1 s are listed in split60.json and cut automatically at a phrase break."""
import json
import sys
from pathlib import Path

import build50
from build40 import C, END, HOOK, MUS, S

HERE = Path(__file__).parent
LONG = json.load(open(HERE / "split60.json")) if (HERE / "split60.json").exists() else {}
VOICE = {}
R = {}
R["stone-cutter-100"] = ("tense", [
    HOOK("h0-strike", "You might be one hit away|from breaking through.", "man-face", 1.2),
    S("s01-first", "A stonecutter hit a giant rock with his hammer.", pause=True, sfx=["bass"]),
    S("s01-first", "Once. Nothing.", C, 1.25, punch=True),
    S("s02-sweat", "Ten times. Nothing.", "man-face", 1.2, sfx=["bass"]),
    S("s04-again", "Fifty times. Not even a crack.", sfx=["bass"]),
    S("s03-laugh", "People laughed.", sfx=["wrong"]),
    S("s03-laugh", "\"You're wasting your time.\"", C, 1.3, punch=True),
    S("s04-again", "He kept going.", C, 1.3, sfx=["heartbeat"]),
    S("s05-split", "On the hundred and first blow,", pause=True),
    S("s05-split", "the rock split clean in two.", C, 1.3, punch=True, sfx=["impact"]),
    S("s06-lucky", "The people said, \"Wow, one lucky hit.\"", sfx=["pop"]),
    S("s07-knows", "But he knew.", "man-face", 1.3),
    S("s07-knows", "It wasn't the last blow that broke it.", "wide", 1.0),
    S("s04-again", "It was all hundred before it.", C, 1.3, punch=True, sfx=["sparkle"]),
    S("k1-next", "Don't quit because you can't see the crack yet.", pause=True),
    END("k1-next", "Keep hitting."),
], "Don't quit because you can't see the crack yet.")
R["camel-hump"] = ("echoes", [
    HOOK("h0-zoo", "Stop asking|why you were made this way.", C, 1.3),
    S("c01-ask", "A baby camel asked his mother,", pause=True),
    S("c01-ask", "\"Why do we have these big humps?\"", C, 1.3),
    S("c02-hump", "\"To store water, so we can survive the desert.\"", sfx=["sparkle"]),
    S("c01-ask", "\"And why these long eyelashes?\"", "wide", 1.05, sfx=["pop"]),
    S("c03-lashes", "\"To protect our eyes from the sandstorms.\"", sfx=["whoosh2"]),
    S("c01-ask", "\"And why these wide feet?\"", C, 1.25, sfx=["pop"]),
    S("c04-feet", "\"So we don't sink in the sand.\""),
    S("c05-think", "The baby thought for a moment.", pause=True, sfx=["heartbeat"]),
    S("c06-stuck", "\"Then why are we stuck in a zoo?\"", "wide", 1.0, sfx=["bass"]),
    S("k0-office", "Your strengths are useless in the wrong place.", pause=True),
    S("k0-office", "If you feel trapped, maybe you're not weak.", "man-face", 1.3),
    END("k1-desert", "Maybe you're in the wrong desert."),
], "Your strengths are useless in the wrong place.")
R["pencil-lesson"] = ("echoes", [
    HOOK("h0-pencil", "Everything you need to know about life|is inside a pencil.", C, 1.3),
    S("p01-writing", "A grandmother was writing a letter.", pause=True),
    S("p02-boy", "Her grandson asked, \"What are you writing?\""),
    S("p03-show", "\"Something more important than the words.", "wide", 1.0),
    S("p03-show", "I'm writing with a pencil.\"", C, 1.3, sfx=["sparkle"]),
    S("p03-show", "She smiled.", "wide", 1.1),
    S("p04-hand", "\"First, it can do great things,", pause=True),
    S("p04-hand", "but only if it lets a hand guide it.", C, 1.25),
    S("p05-sharpen", "Second, it hurts to be sharpened,", pause=True, sfx=["glitch"]),
    S("p05-sharpen", "but it writes better after.", C, 1.3),
    S("p06-erase", "Third, it can erase its mistakes.", pause=True, sfx=["rewind"]),
    S("p07-inside", "And fourth, what matters most is not the wood outside.", pause=True),
    S("p07-inside", "It's what's inside.\"", C, 1.4, punch=True, sfx=["sparkle"]),
    S("k1-boy", "Be like a pencil.", pause=True),
    END("k1-boy", "Leave your mark."),
], "Be like a pencil.")
R["hole-in-boat"] = ("tense", [
    HOOK("h0-hole", "The smallest thing you do|could save someone's whole family.", "man-face", 1.2),
    S("h01-hire", "A man hired a painter to paint his boat.", pause=True),
    S("h02-paint", "While painting,", sfx=["whoosh2"]),
    S("h03-notice", "the painter noticed a small hole", "man-face", 1.25),
    S("h0-hole", "and quietly fixed it.", "wide", 1.0, sfx=["sparkle"]),
    S("h05-run", "Weeks later, the man ran to him with a big reward.", pause=True),
    S("h06-reward", "\"You fixed the hole?\"", C, 1.25),
    S("h07-surprised", "\"Yes, but you only paid me to paint.\"", "man-face", 1.2),
    S("h04-kids", "\"My children took the boat to sea while I was away.", pause=True, sfx=["heartbeat"]),
    S("h04-kids", "Without your fix, they would have drowned.\"", C, 1.3, punch=True, sfx=["bass"]),
    S("h07-surprised", "The painter never knew.", "man-face", 1.5, punch=True),
    S("k1-sunset", "Do the small good things, even when no one asks.", pause=True),
    END("k1-sunset", "You may never know whose life you saved."),
], "Do the small good things, even when no one asks.")
R["blind-lamp"] = ("echoes", [
    HOOK("h0-lamp", "Why would a blind man|carry a lamp?", C, 1.3),
    S("b01-walk", "A blind man walked through the village every night", pause=True),
    S("b01-walk", "holding a lit lamp.", C, 1.3, sfx=["sparkle"]),
    S("b02-laugh", "People laughed.", sfx=["pop"]),
    S("b02-laugh", "\"Why carry a lamp? You can't even see.\"", C, 1.25),
    S("b03-smile", "He smiled.", "wide", 1.0, pause=True),
    S("b03-smile", "\"It's not for me. It's for you.", C, 1.3),
    S("b04-path", "So you don't walk into me in the dark.\"", sfx=["whoosh2"]),
    S("b05-quiet", "The laughing stopped.", sfx=["heartbeat"]),
    S("k1-hero", "Sometimes the light you carry isn't for your eyes.", pause=True),
    S("k2-glow", "Your kindness, your patience, your example,", "man-face", 1.2),
    S("k1-hero", "they light the way for others.", "wide", 1.05, sfx=["sparkle"]),
    S("k2-glow", "Keep carrying your lamp,", "man-face", 1.4),
    END("k1-hero", "even when nobody understands why."),
], "Sometimes the light you carry isn't for your eyes.")
R["donkey-salt"] = ("tense", [
    HOOK("h0-fall", "Smart people don't repeat|the same trick forever.", C, 1.3),
    S("d01-load", "A merchant's donkey carried heavy salt", pause=True),
    S("d02-cross", "across a river every day.", "wide", 1.0),
    S("h0-fall", "One day it slipped and fell into the water.", "wide", 1.0, sfx=["bass"]),
    S("d03-light", "When it stood up, the load was lighter.", sfx=["sparkle"]),
    S("d03-light", "The salt had melted.", C, 1.3),
    S("d04-sneaky", "The next day, it fell on purpose.", pause=True, sfx=["pop"]),
    S("d05-notice", "The merchant noticed.", C, 1.3, punch=True),
    S("d06-sponges", "So the next day, he loaded the donkey with sponges.", sfx=["whoosh2"]),
    S("h0-fall", "The donkey fell in again.", C, 1.25, sfx=["bass"]),
    S("d07-heavy", "But this time, the sponges soaked up water.", pause=True),
    S("d07-heavy", "The load became twice as heavy.", C, 1.35, punch=True, sfx=["wrong"]),
    S("k1-hero", "The same shortcut doesn't work forever.", pause=True),
    END("k1-hero", "Life changes the load."),
], "The same shortcut doesn't work forever.")
R["wolf-sheep"] = ("tense", [
    HOOK("h0-disguise", "Be careful|who you let into your life.", C, 1.3),
    S("w01-watch", "A wolf wanted to eat the sheep,", pause=True),
    S("w02-shepherd", "but the shepherd was always watching.", "man-face", 1.2),
    S("h0-disguise", "So the wolf found an old sheepskin and wore it.", "wide", 1.0, sfx=["pop"]),
    S("w03-walk", "He walked in with the flock. Nobody noticed.", sfx=["heartbeat"]),
    S("w04-sleep", "The sheep let him sleep right next to them.", C, 1.2),
    S("w05-dark", "That night, the shepherd wanted meat for dinner.", pause=True),
    S("w05-dark", "He went into the dark field", "man-face", 1.25),
    S("w05-dark", "and grabbed the biggest sheep he could find.", "wide", 1.0),
    S("w06-grab", "It was the wolf.", C, 1.3, punch=True, sfx=["bass"]),
    S("w07-caught", "The wolf was caught by his own disguise.", sfx=["wrong"]),
    S("k1-flock", "Not everyone who looks like you is one of you.", pause=True),
    END("k1-flock", "And lies always find their owner."),
], "Not everyone who looks like you is one of you.")
R["three-sieves"] = ("echoes", [
    HOOK("h0-stop", "Before you repeat what you heard,|ask yourself three questions.", C, 1.25),
    S("t01-run", "A man ran to Socrates.", pause=True),
    S("t01-run", "\"I have news about your friend!\"", C, 1.3, sfx=["pop"]),
    S("t02-one", "\"Wait. First, is it true?\"", "man-face", 1.25),
    S("t03-shrug", "\"Well, I just heard it.\""),
    S("t04-two", "\"Second, is it good?\"", "man-face", 1.25, sfx=["pop"]),
    S("t05-bad", "\"No, it's quite bad.\""),
    S("t06-three", "\"Third, is it useful to me?\"", "man-face", 1.25, sfx=["pop"]),
    S("t05-bad", "\"Not really.\"", C, 1.3),
    S("t06-three", "Socrates smiled.", "wide", 1.0, pause=True),
    S("h0-stop", "\"If it's not true, not good and not useful,", "wide", 1.0),
    S("h0-stop", "why tell me at all?\"", C, 1.35, punch=True, sfx=["bass"]),
    S("t07-quiet", "The man went quiet.", sfx=["heartbeat"]),
    S("k1-wise", "Most drama would disappear if we asked these three questions.", pause=True),
    S("k1-wise", "True. Good. Useful.", "man-face", 1.4, sfx=["pop", {"name": "pop", "at": 0.5}, {"name": "pop", "at": 1.0}]),
    END("k1-wise", "Or stay silent."),
], "Most drama would disappear if we asked these three questions.")
R["woodcutter-axe"] = ("echoes", [
    HOOK("h0-gold", "Honesty might be the most valuable thing|you own.", C, 1.3),
    S("a01-chop", "A poor woodcutter dropped his only axe", pause=True),
    S("a02-drop", "into a deep river.", sfx=["bass"]),
    S("a03-cry", "He sat down and cried.", "man-face", 1.2, sfx=["heartbeat"]),
    S("h0-gold", "A river spirit rose from the water holding a golden axe.", "wide", 1.0, pause=True, sfx=["sparkle"]),
    S("a04-offer", "\"Is this yours?\" \"No.\""),
    S("a05-silver", "The spirit brought a silver axe.", sfx=["sparkle"]),
    S("a05-silver", "\"Is this yours?\" \"No.\"", C, 1.25),
    S("a06-iron", "Then the spirit brought his old iron axe.", pause=True),
    S("a06-iron", "\"Yes! That's mine!\"", "man-face", 1.4, punch=True, sfx=["pop"]),
    S("a07-three", "The spirit smiled and gave him all three axes.", sfx=["sparkle"]),
    S("k1-walk", "When you're honest, you may lose a little today.", pause=True),
    END("k1-walk", "But you'll gain more than gold tomorrow."),
], "When you're honest, you may lose a little today.")
R["two-seeds"] = ("tense", [
    HOOK("h0-hen", "Fear will keep you safe.|And it will keep you small.", C, 1.3),
    S("g01-two", "Two seeds lay side by side in the spring soil.", pause=True),
    S("g01-two", "The first said, \"I want to grow!", C, 1.25),
    S("g02-roots", "I want my roots deep and my leaves touching the sun.\"", sfx=["sparkle"]),
    S("g03-sun", "And it grew.", C, 1.25),
    S("g04-scared", "The second seed said, \"If I grow roots, they might hit rocks.", pause=True),
    S("g04-scared", "If I sprout, bugs might eat me.", C, 1.25, sfx=["heartbeat"]),
    S("g05-wait", "I'll wait until it's safe.\"", "wide", 1.0),
    S("g05-wait", "So it waited.", C, 1.3, sfx=["heartbeat"]),
    S("h0-hen", "A hungry hen came scratching through the soil.", "wide", 1.0, pause=True),
    S("h0-hen", "She found the seed that was waiting.", C, 1.3),
    S("g06-eat", "And ate it.", C, 1.3, punch=True, sfx=["bass"]),
    S("k1-hero", "Waiting for perfect means waiting forever.", pause=True),
    END("k2-tall", "Grow anyway."),
], "Waiting for perfect means waiting forever.")

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
