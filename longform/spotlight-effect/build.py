"""Build full.json (the full ~11 min video) from compact shot lists.

Each shot: (text, visual, extras). Transitions, transition SFX, graphic SFX, chapter openers and music cues are added
by rule (see auto()); anything in extras overrides. Shot texts are checked word-for-word against chapters/chN.txt.
Usage: python3 build.py  ->  full.json
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent


def I(n, f=(.5, .5), z=1.1, **kw):
    return {"img": f"img/{n}.jpg", "focus": list(f), "zoom": z, **kw}


def V(n, st=1.0, z=1.08, **kw):
    return {"video": f"stock/{n}.mp4", "start": st, "zoom": z, **kw}


def K(*lines, times=None, **kw):
    lines = [[l, "white"] if isinstance(l, str) else list(l) for l in lines]
    return {"mg": "kinetic", "lines": lines, "times": times or [0.0] * len(lines), **kw}


def CH(n, sub, sub_at):
    return {"mg": "chapter", "label": "TRICK", "text": f"#{n}", "sub": sub, "sub_at": sub_at}


def LT(title, sub, at=0.1):
    return {"mg": "lower_third", "title": title, "sub": sub, "at": at}


def TITLE(text, at, sub=None):
    return {"mg": "title", "text": text, "at": at, "y": 0.8, "size": 120, **({"sub": sub} if sub else {})}


def TAG(text, at=0.0):
    return {"mg": "tag", "text": text, "at": at, "pos": [0.04, 0.08]}


def SCAN(box, label, at=0.1):
    return {"mg": "scan", "box": box, "label": label, "at": at}


RECAP = ["STOP HIDING YOUR NERVES", "POINT ATTENTION OUTWARD", "MISTAKES LOOK BRAVER", "JUDGED LESS HARSHLY",
         "LIKED MORE THAN YOU THINK", "NOBODY TRACKS BAD DAYS", "EMBARRASS YOURSELF ON PURPOSE"]


def R(k):   # recap list with items < k shown, item k animating in
    return {"mg": "recap", "items": RECAP, "times": [-1.0] * k + [0.05] + [999.0] * (6 - k) if k >= 0 else [999.0] * 7}


TRACKS = {"intrigue": ("../../reels/audio/music/echoes.mp3", 162.865),
          "confident": ("../../reels/audio/music/unforgiven.mp3", 13.63),
          "tense": ("../../reels/audio/music/out-of-this-world.mp3", 117.26),
          "warm": ("../../reels/audio/music/fifth-of-february.mp3", 1.6)}

CH1 = [
    ("Trick number one. Stop trying to hide your nerves.", K("STOP HIDING", ("YOUR NERVES", "yellow"), times=[0.0, "@hide"]), {"chapter": True, "music": "tense"}),
    ("Picture this.", V("nervous-2", 0.5, 1.15), {}),
    ("You're about to give a presentation.", I("c1-podium", (.5, .5), 1.0, drift=0.06), {}),
    ("Your heart is pounding,", I("c1-podium", (.5, .36), 2.2), {"sfx": [{"name": "heartbeat", "at": 0.1}, {"name": "heartbeat", "at": 0.55}]}),
    ("your hands are sweating,", V("nervous-1", 1.0, 1.15), {}),
    ("your voice feels shaky,", V("audience-applause-0", 2.0, 1.2), {}),
    ("and you're sure everyone in the room can see it.", I("crowd-stare", (.5, .45), 1.0), {"punch": {"at": "@see", "zoom": 1.9, "focus": [.51, .3]}, "shake": ["@see"], "sfx": [{"name": "glass", "at": "@see"}]}),
    ("It feels like your anxiety is written all over your face.", I("c1-glass-head", (.5, .4), 1.2, to=[.5, .3], to_zoom=1.9, drift=0), {}),
    ("Psychologists call this the illusion of transparency.", I("c1-glass-head", (.5, .45), 1.05), {"captions": False, "overlays": [TITLE("ILLUSION OF TRANSPARENCY", "@illusion", "YOUR FEELINGS FEEL VISIBLE")]}),
    ("In one study at Cornell,", V("job-interview-2", 0.3, 1.1), {"overlays": [LT("GILOVICH, SAVITSKY & MEDVEC", "Cornell University (1998)")]}),
    ("people told lies", I("c1-liar", (.3, .45), 1.4), {}),
    ("while a group of observers watched", I("c1-liar", (.78, .45), 1.6), {}),
    ("and tried to catch them.", V("job-interview-2", 2.5, 1.25), {"overlays": [SCAN([0.15, 0.1, 0.6, 0.9], "DETECTING LIES...")]}),
    ("The liars guessed that about half of the observers would see right through them.", {"mg": "grid", "label": "LIARS GUESSED THEY'D BE CAUGHT BY", "lit": [0, 10, "@guessed", "@half"], "pct": [0, 50, "@guessed", "@half"]}, {"sfx": [{"name": "pop", "at": "@guessed"}, {"name": "pop", "at": "@about"}, {"name": "pop", "at": "@half"}]}),
    ("In reality, only about a quarter did.", {"mg": "grid", "label": "ACTUALLY CAUGHT THEM", "lit": [0, 5, 0.0, "@quarter"], "pct": [0, 25, 0.0, "@quarter"]}, {"in": "flash", "shake": ["@quarter"], "sfx": [{"name": "bass", "at": "@quarter"}]}),
    ("Your inner storm is mostly invisible.", I("c1-glass-head", (.5, .45), 1.1), {"punch": {"at": "@invisible", "zoom": 2.1, "focus": [.5, .28]}, "sfx": [{"name": "sparkle", "at": "@invisible"}]}),
    ("And here's the part that almost everyone gets wrong.", K("THE PART", ("EVERYONE GETS WRONG", "red"), times=[0.0, "@everyone"]), {"in": "glitch", "sfx": [{"name": "wrong", "at": "@wrong", "gain": 0.6}]}),
    ("When we feel nervous, we try harder to hide it.", I("c1-stiff", (.45, .45), 1.1), {}),
    ("We tense up,", I("c1-stiff", (.4, .3), 1.9), {"shake": [0.05]}),
    ("we avoid eye contact,", V("nervous-1", 6.0, 1.2), {}),
    ("we rehearse every single word in our head.", I("c1-podium", (.5, .27), 2.0), {"sfx": [{"name": "typing", "at": 0.1, "gain": 0.5}]}),
    ("And that actually makes us look more awkward, not less.", I("c1-stiff", (.65, .45), 1.5), {"sfx": [{"name": "wrong", "at": "@awkward", "gain": 0.4}]}),
    ("So the researchers tried something different.", V("office-4", 2.0, 1.1), {"music": "warm", "pause_before": 0.25}),
    ("Before a group of nervous people gave a speech,", V("audience-applause-0", 6.0, 1.1), {}),
    ("they simply told them about the illusion of transparency.", V("therapy-1", 1.0, 1.1), {"overlays": [LT("SAVITSKY & GILOVICH", "Journal of Experimental Social Psychology (2003)")]}),
    ("That's it.", K(("THAT'S IT.", "yellow")), {}),
    ("No breathing exercises. No pep talk.", K(("NO BREATHING EXERCISES", "red"), ("NO PEP TALK", "red"), times=[0.0, "@pep"]), {"in": "cut", "sfx": [{"name": "wrong", "at": 0.05, "gain": 0.35}, {"name": "wrong", "at": "@pep", "gain": 0.35}]}),
    ("Just the truth: your nerves are far less visible than you think.", K("YOUR NERVES ARE", ("FAR LESS VISIBLE", "yellow"), "THAN YOU THINK", times=[0.0, "@far", "@than"]), {"in": "cut", "sfx": [{"name": "pop", "at": "@far"}, {"name": "pop", "at": "@than"}]}),
    ("Those speakers felt calmer,", I("c1-calm", (.6, .45), 1.3), {}),
    ("and the audience rated their speeches as better and more composed.", V("audience-applause-2", 3.0, 1.1), {"amb": {"name": "crowd-murmur", "gain": 0.1}, "sfx": [{"name": "correct", "at": "@composed", "gain": 0.5}]}),
    ("So the next time your heart starts racing,", I("c1-podium", (.5, .36), 1.8), {"sfx": [{"name": "heartbeat", "at": 0.2}, {"name": "heartbeat", "at": 0.7}]}),
    ("remind yourself: they can't see what I feel.", K("THEY CAN'T SEE", ("WHAT I FEEL", "yellow"), times=[0.0, "@what"]), {"sfx": [{"name": "sparkle", "at": "@what"}]}),
    ("Just knowing that switches half the spotlight off.", I("switch-off", (.5, .45), 1.2), {"fx": [{"name": "light_off", "at": "@off"}], "sfx": [{"name": "switch", "at": "@off"}]}),
    ("But the next trick goes even further,", I("c2-listen", (.55, .4), 1.0), {"overlays": [TAG("NEXT:  TRICK #2")]}),
    ("because it doesn't just calm you down.", V("conversation-3", 1.0), {}),
    ("It makes people like you more.", V("laughing-4", 2.0), {"sfx": [{"name": "sparkle", "at": "@more"}]}),
]

CH2 = [
    ("Trick number two. Point the spotlight outward.", CH(2, "POINT THE SPOTLIGHT OUTWARD", "@Point"), {"chapter": True, "music": "intrigue"}),
    ("Here's what happens inside an anxious brain", V("brain", 12.0, 1.15), {}),
    ("at a party,", V("party-4", 2.0), {"amb": {"name": "crowd-murmur", "gain": 0.12}}),
    ("a date,", V("first-date-0", 1.0), {}),
    ("or a job interview.", V("job-interview-0", 1.0), {}),
    ("Your attention turns inward.", I("c2-camera", (.5, .45), 1.0), {}),
    ("You start watching yourself like a security camera.", I("c2-camera", (.5, .45), 1.1), {"punch": {"at": "@security", "zoom": 2.3, "focus": [.56, .32]}, "sfx": [{"name": "shutter", "at": "@camera"}]}),
    ("How do I sound?", K("HOW DO I SOUND?"), {"in": "glitch"}),
    ("What are my hands doing?", K("WHAT ARE MY", "HANDS DOING?"), {"in": "glitch"}),
    ("Is my face going red?", K("IS MY FACE", ("GOING RED?", "red")), {"in": "glitch"}),
    ("Did that joke land?", K("DID THAT", ("JOKE LAND?", "yellow")), {"in": "glitch"}),
    ("Psychologists who study social anxiety call this self-focused attention,", I("c2-camera", (.5, .4), 1.15), {"captions": False, "overlays": [TITLE("SELF-FOCUSED ATTENTION", "@self")]}),
    ("and it's the fuel that keeps the spotlight burning.", I("stage-spotlight", (.5, .45), 1.3, drift=0.08), {}),
    ("The more you watch yourself, the more awkward you feel.", I("c2-wheel", (.5, .55), 1.0), {}),
    ("And the more awkward you feel, the more you watch yourself.", I("c2-wheel", (.5, .55), 1.6, spin=8), {}),
    ("It's a loop.", K(("IT'S A LOOP", "yellow")), {"sfx": [{"name": "rewind", "at": 0.05, "gain": 0.6}]}),
    ("Imagine two people at the same party.", I("c2-corner", (.5, .5), 1.0), {}),
    ("The first one spends the whole night thinking about how they look.", I("c2-corner", (.25, .5), 1.8), {}),
    ("The second one spends the night", I("c2-corner", (.72, .5), 1.8), {}),
    ("trying to find out one interesting thing about every person they meet.", V("conversation-2", 1.0), {"amb": {"name": "crowd-murmur", "gain": 0.1}}),
    ("Guess which one goes home feeling awkward?", I("c2-corner", (.5, .5), 1.0, to=[.25, .45], to_zoom=2.2, drift=0), {"sfx": [{"name": "tick", "at": 0.3}, {"name": "tick", "at": 0.8}, {"name": "tick", "at": 1.3}]}),
    ("The way out is surprisingly simple.", K("THE WAY OUT", ("SURPRISINGLY SIMPLE", "yellow"), times=[0.0, "@surprisingly"]), {"music": "confident", "pause_before": 0.25}),
    ("Give your attention a job somewhere else.", I("c2-flashlight", (.5, .5), 1.0), {}),
    ("Get curious about the other person.", I("c2-listen", (.5, .45), 1.0), {}),
    ("What are they really saying?", V("listening-3", 2.0), {}),
    ("What do they care about?", V("conversation-3", 3.0), {}),
    ("What's one question you could ask that nobody else would think of?", I("c2-listen", (.5, .45), 1.05), {"punch": {"at": "@question", "zoom": 2.0, "focus": [.62, .2]}, "sfx": [{"name": "pop", "at": "@question"}]}),
    ("Your brain can't fully focus on two things at once.", V("brain", 20.0, 1.15), {}),
    ("Every bit of attention you give to them", I("c2-flashlight", (.7, .5), 1.6), {}),
    ("is attention taken away from your own spotlight.", I("many-spotlights", (.5, .45), 1.6), {}),
    ("And there's a bonus.", K(("BONUS", "yellow")), {"sfx": [{"name": "reveal", "at": 0.05}]}),
    ("Researchers at Harvard found that people who ask more questions,", V("college-students-6", 2.0), {"overlays": [LT("HUANG ET AL.", "Harvard University (2017)")]}),
    ("especially follow-up questions,", V("conversation-5", 2.0), {}),
    ("are rated as more likeable.", V("laughing-1", 3.0), {"sfx": [{"name": "sparkle", "at": "@likeable"}]}),
    ("So the trick that calms you down", I("c2-listen", (.55, .4), 1.2), {}),
    ("also makes you better company.", V("party-3", 1.0), {"sfx": [{"name": "sparkle", "at": "@company"}]}),
    ("Now, what about the moments when you really do mess up?", I("tshirt-doorway", (.2, .4), 1.6), {}),
    ("That's where trick number three comes in.", V("cinema-1", 1.0), {"sfx": [{"name": "shutter", "at": "@three"}]}),
]

CH3 = [
    ("Trick number three. Your mistakes look braver from the outside.", CH(3, "MISTAKES LOOK BRAVER", "@Your"), {"chapter": True, "music": "warm"}),
    ("Imagine you have to admit you made a big mistake at work.", I("c3-confess", (.45, .45), 1.0, to=[.35, .35], to_zoom=1.6, drift=0), {}),
    ("Or tell someone you have feelings for them.", I("c3-flowers", (.5, .45), 1.1), {}),
    ("Or ask for help when you're struggling.", V("couple-park-7", 2.0), {}),
    ("In your head, it feels like weakness.", I("c3-mirror", (.5, .4), 1.1), {}),
    ("Like you're exposing every flaw you have.", I("c3-mirror", (.65, .4), 1.8), {"sfx": [{"name": "zap", "at": 0.1}]}),
    ("But in 2018,", {"mg": "year", "from": 2026, "to": 2018, "roll": 0.6, "label": "GERMANY"}, {"sfx": [{"name": "rewind", "at": 0.05, "gain": 0.6}, {"name": "pop", "at": 0.6}]}),
    ("researchers in Germany tested exactly this.", V("college-students-3", 1.0), {"overlays": [LT("BRUK, SCHOLL & BLESS", "University of Mannheim (2018)")]}),
    ("They asked people to imagine themselves in vulnerable moments like these,", V("therapy-1", 2.0), {}),
    ("and then imagine someone else in the very same situation.", I("c3-admire", (.5, .45), 1.0), {}),
    ("When it was them, they saw weakness and embarrassment.", {"mg": "versus", "left": ["YOU SEE", "WEAKNESS"], "right": ["THEY SEE", "COURAGE"], "at": 999.0}, {}),
    ("When it was someone else, they saw courage, honesty, and strength.", {"mg": "versus", "left": ["YOU SEE", "WEAKNESS"], "right": ["THEY SEE", "COURAGE"], "left_at": -1.0, "at": "@courage"}, {"in": "cut", "sfx": [{"name": "reveal", "at": "@courage"}]}),
    ("The researchers called it the beautiful mess effect.", I("c3-admire", (.5, .45), 1.15), {"captions": False, "overlays": [TITLE("THE BEAUTIFUL MESS EFFECT", "@beautiful")]}),
    ("The same moment that feels like a mess from the inside", I("c3-mirror", (.6, .4), 1.4), {}),
    ("looks beautiful from the outside.", I("c3-admire", (.5, .3), 1.6), {"sfx": [{"name": "sparkle", "at": "@beautiful"}]}),
    ("Think about it.", K("THINK ABOUT IT"), {}),
    ("When a friend tells you they're struggling,", V("hug-2", 1.0), {}),
    ("do you think less of them?", I("c3-hug", (.55, .35), 1.3), {}),
    ("Or do you trust them more?", V("hug-3", 2.0), {}),
    ("Most of us feel closer to people who admit their flaws.", V("couple-park-7", 6.0), {}),
    ("We just forget that the same rule applies to us.", I("tiny-planet", (.5, .45), 1.3), {}),
    ("So when you're about to say, I was wrong,", I("c3-confess", (.35, .3), 1.9), {}),
    ("or I don't know,", K("I DON'T KNOW"), {}),
    ("or I need help,", K(("I NEED HELP", "yellow")), {"in": "cut"}),
    ("remember that the person watching you isn't seeing a fool.", I("c3-admire", (.75, .45), 1.6), {}),
    ("They're seeing someone brave enough to be real.", K(("BRAVE ENOUGH", "yellow"), "TO BE REAL", times=["@brave", "@real"]), {"sfx": [{"name": "sparkle", "at": "@real"}]}),
    ("And that's usually the most memorable thing in the room.", V("therapy-1", 4.0), {"amb": {"name": "crowd-murmur", "gain": 0.08}}),
    ("But what if the mistake is actually embarrassing?", I("tshirt-doorway", (.2, .4), 1.6), {}),
    ("Like, really embarrassing?", I("c4-coffee", (.48, .45), 1.3), {"sfx": [{"name": "scratch", "at": "@really"}]}),
]

CH4 = [
    ("Trick number four. They judge you less harshly than you think.", CH(4, "LESS HARSH THAN YOU THINK", "@They"), {"chapter": True, "music": "tense", "music_restart": True}),
    ("Let's say the worst actually happens.", K(("THE WORST", "red"), "HAPPENS", times=["@worst", "@happens"]), {}),
    ("You trip on the stairs in front of everyone.", I("c4-trip", (.45, .45), 1.0), {"punch": {"at": "@stairs", "zoom": 1.8, "focus": [.38, .4]}, "shake": ["@stairs"], "sfx": [{"name": "bass", "at": "@stairs", "gain": 0.6}]}),
    ("You forget someone's name right after they told you.", I("c4-name", (.5, .45), 1.0, to=[.45, .3], to_zoom=1.6, drift=0), {"sfx": [{"name": "pop", "at": "@name"}]}),
    ("You spill coffee on your shirt", I("c4-coffee", (.48, .45), 1.1), {"punch": {"at": "@coffee", "zoom": 1.8, "focus": [.48, .6]}, "sfx": [{"name": "scratch", "at": "@coffee"}]}),
    ("just before a meeting.", V("office-4", 5.0), {}),
    ("Surely now, people are judging you.", I("crowd-stare", (.5, .45), 1.15), {"punch": {"at": "@judging", "zoom": 1.9, "focus": [.51, .3]}, "shake": ["@judging"]}),
    ("Researchers at Cornell tested this too.", V("campus", 6.0), {"overlays": [LT("SAVITSKY, EPLEY & GILOVICH", "Cornell University (2001)")]}),
    ("They had people fail at a task in front of others,", V("college-students-3", 4.0), {}),
    ("and then predict how harshly those observers would rate them.", V("job-interview-2", 1.5, 1.2), {}),
    ("Again and again, people expected to be judged far more severely than they actually were.", {"mg": "bars", "headline": "HOW HARSHLY YOU'RE JUDGED", "values": False, "bars": [["EXPECTED", 85, "grey"], ["ACTUAL", 40, "yellow"]]}, {"sfx": [{"name": "pop", "at": 0.2}, {"name": "pop", "at": 0.45}]}),
    ("Why does this happen?", K(("WHY?", "yellow")), {"music": "intrigue"}),
    ("Because when it's you, the blunder is the whole story.", I("c4-cinema", (.5, .45), 1.0), {}),
    ("You see it in high definition,", I("c4-cinema", (.7, .25), 2.0), {"overlays": [TAG("HD  1080p")]}),
    ("and you replay it again and again.", I("c4-cinema", (.6, .3), 1.4), {"fx": ["vhs"], "overlays": [TAG("◀◀ REPLAY  x47")], "sfx": ["rewind"]}),
    ("But the people watching see it as one tiny moment in a much bigger picture.", I("c4-wall", (.72, .62), 2.4, to=[.5, .45], to_zoom=1.0, drift=0), {"sfx": [{"name": "tunnel", "at": 0.5}]}),
    ("They know you're more than one mistake,", V("laughing-3", 1.0), {}),
    ("because they make mistakes too.", V("coffee-spill-0", 7.0), {}),
    ("In fact, a classic study on the pratfall effect found", I("c4-coffee", (.48, .45), 1.05), {"music": "warm", "captions": False, "overlays": [TITLE("THE PRATFALL EFFECT", "@pratfall")]}),
    ("that when a competent person spilled coffee on themselves,", V("coffee-spill-0", 2.0), {"overlays": [LT("ARONSON, WILLERMAN & FLOYD", "Psychonomic Science (1966)")]}),
    ("people actually liked them more.", V("laughing-1", 2.0), {"sfx": [{"name": "sparkle", "at": "@liked"}]}),
    ("The mistake made them seem more human.", I("c4-coffee", (.48, .3), 1.6), {}),
    ("Perfect people feel distant.", K("PERFECT PEOPLE", ("FEEL DISTANT", "red"), times=[0.0, "@distant"]), {}),
    ("Slightly clumsy people feel real.", K("SLIGHTLY CLUMSY", ("FEEL REAL", "yellow"), times=[0.0, "@real"]), {"in": "cut", "sfx": [{"name": "sparkle", "at": "@real"}]}),
    ("So the next time you mess up, don't spiral.", I("c2-wheel", (.5, .55), 1.3, spin=10), {}),
    ("Laugh, fix it, and move on.", K("LAUGH.", "FIX IT.", ("MOVE ON.", "yellow"), times=[0.0, "@fix", "@move"]), {"sfx": [{"name": "pop", "at": "@fix"}, {"name": "pop", "at": "@move"}]}),
    ("Because that's exactly what everyone else will do.", V("street-walking-0", 4.0), {"amb": {"name": "crowd-murmur", "gain": 0.1}}),
    ("And trick number five might change how you see", I("c5-talk", (.5, .45), 1.0), {}),
    ("every conversation you've ever had.", V("conversation-2", 3.0), {}),
]

CH5 = [
    ("Trick number five. Assume they liked you more.", CH(5, "ASSUME THEY LIKED YOU MORE", "@Assume"), {"chapter": True, "music": "intrigue"}),
    ("Think about the last time you met someone new.", V("first-date-0", 4.0), {}),
    ("On the way home, did you replay the conversation?", I("c5-walk", (.5, .5), 1.0, to=[.6, .25], to_zoom=1.7, drift=0), {}),
    ("Did you wonder if you talked too much,", V("conversation-5", 1.0), {}),
    ("or said something weird,", I("bed-replay", (.5, .3), 1.5), {}),
    ("or if they were just being polite?", V("first-date-0", 8.0), {}),
    ("You're not alone. Almost everyone does this.", V("street-walking-5", 3.0), {}),
    ("Your brain replays the tape,", I("c5-walk", (.6, .22), 2.0), {"fx": ["vhs"], "overlays": [TAG("◀◀ REPLAY")], "sfx": ["rewind"]}),
    ("looking for every tiny mistake,", V("brain", 30.0, 1.1), {"overlays": [SCAN([0.25, 0.15, 0.75, 0.85], "SEARCHING FOR MISTAKES...")]}),
    ("and it always finds something.", K("IT ALWAYS", ("FINDS SOMETHING", "red"), times=[0.0, "@finds"]), {"sfx": [{"name": "wrong", "at": "@finds", "gain": 0.5}]}),
    ("In 2018,", {"mg": "year", "from": 2026, "to": 2018, "roll": 0.6, "label": "THE CONVERSATION STUDY"}, {"sfx": [{"name": "rewind", "at": 0.05, "gain": 0.6}, {"name": "pop", "at": 0.6}]}),
    ("researchers paired up strangers for a short conversation.", V("conversation-3", 6.0), {"overlays": [LT("BOOTHBY, COONEY, SANDSTROM & CLARK", "Psychological Science (2018)")]}),
    ("Afterwards, they asked each person two questions.", I("c5-talk", (.5, .45), 1.1), {}),
    ("How much did you like your partner?", K("HOW MUCH DID YOU", ("LIKE THEM?", "yellow"), times=[0.0, "@like"]), {}),
    ("And how much do you think your partner liked you?", K("HOW MUCH DID", ("THEY LIKE YOU?", "yellow"), times=[0.0, "@liked"]), {"in": "cut"}),
    ("The results were almost the same every time.", V("college-students-6", 5.0), {}),
    ("People liked their partner more than they believed their partner liked them.", {"mg": "versus", "left": ["WHAT YOU GUESS", "LESS"], "right": ["WHAT THEY FELT", "MORE"], "at": "@believed"}, {"sfx": [{"name": "reveal", "at": "@believed"}]}),
    ("The researchers called this the liking gap.", I("c5-spotlights", (.5, .5), 1.0), {"captions": False, "overlays": [TITLE("THE LIKING GAP", "@liking")]}),
    ("And it didn't disappear quickly.", V("night-walk-7", 2.0), {}),
    ("In one study, it lasted for months between new college roommates.", I("c5-roommates", (.45, .55), 1.1), {"overlays": [TAG("LASTED FOR MONTHS", "@months")]}),
    ("Here's why.", K(("HERE'S WHY", "yellow")), {}),
    ("While you're busy criticising your own performance,", I("c5-spotlights", (.38, .45), 1.8), {}),
    ("the other person is busy criticising theirs.", I("c5-spotlights", (.67, .45), 1.8), {}),
    ("Neither of you is paying much attention", V("conversation-5", 4.0), {}),
    ("to the other person's little mistakes.", I("c5-spotlights", (.5, .5), 1.3), {}),
    ("You're both standing in your own spotlight.", I("many-spotlights", (.5, .5), 1.0, drift=-0.1), {}),
    ("So here's the trick.", K(("THE TRICK", "yellow")), {"music": "warm", "pause_before": 0.25}),
    ("After any conversation,", V("conversation-2", 5.0), {}),
    ("assume you were liked more than you think.", K("YOU WERE LIKED", ("MORE THAN YOU THINK", "yellow"), times=[0.0, "@more"]), {"sfx": [{"name": "sparkle", "at": "@more"}]}),
    ("Statistically, you probably were.", V("laughing-3", 3.0), {"sfx": [{"name": "correct", "at": "@probably", "gain": 0.5}]}),
    ("And the next trick is about something", V("morning-coffee-7", 2.0), {}),
    ("you might worry about every single morning.", I("c6-hair", (.6, .35), 1.3), {}),
]

CH6 = [
    ("Trick number six. Nobody is tracking your bad days.", CH(6, "NOBODY TRACKS YOUR BAD DAYS", "@Nobody"), {"chapter": True, "music": "confident"}),
    ("Some mornings you wake up and everything feels off.", V("morning-coffee-7", 5.0), {}),
    ("Your hair won't sit right.", I("c6-hair", (.62, .3), 1.3), {"sfx": [{"name": "zap", "at": 0.15}]}),
    ("Your skin looks tired.", V("mirror-5", 1.0, 1.15), {}),
    ("Your outfit feels wrong.", V("mirror-3", 2.0), {"overlays": [SCAN([0.55, 0.08, 0.82, 0.95], "OUTFIT CHECK...")], "sfx": [{"name": "typing", "at": 0.2, "gain": 0.5}]}),
    ("And you're sure everyone will notice that today is a bad day.", I("c6-street", (.5, .45), 1.0, to=[.5, .25], to_zoom=1.6, drift=0), {}),
    ("But in another study, the same Cornell team", V("campus", 10.0), {"overlays": [LT("GILOVICH, KRUGER & MEDVEC", "Cornell University (2002)")]}),
    ("asked people to predict how much others would notice", V("college-students-3", 6.0), {}),
    ("the ups and downs in their appearance from one day to the next.", I("c6-calendar", (.5, .35), 1.0, drift=0.08), {}),
    ("And once again, people consistently overestimated it.", {"mg": "bars", "headline": "OVERESTIMATED", "values": False, "bars": [["PREDICTED", 80, "grey"], ["NOTICED", 30, "yellow"]]}, {"sfx": [{"name": "pop", "at": 0.2}, {"name": "pop", "at": 0.45}]}),
    ("Other people simply don't keep a record of how you looked yesterday.", I("c6-calendar", (.5, .35), 1.8), {}),
    ("Here's a quick test.", K(("QUICK TEST", "yellow")), {"sfx": [{"name": "tick", "at": 0.2}, {"name": "tick", "at": 0.7}]}),
    ("Think of three people you saw yesterday.", {"mg": "grid", "label": "3 PEOPLE YOU SAW YESTERDAY", "cols": 3, "rows": 1, "h": 330, "cy": 0.42, "lit": 0}, {"sfx": [{"name": "pop", "at": 0.1}, {"name": "pop", "at": 0.25}, {"name": "pop", "at": 0.4}]}),
    ("Can you remember what any of them were wearing?", {"mg": "grid", "label": "WHAT WERE THEY WEARING?", "cols": 3, "rows": 1, "h": 330, "cy": 0.42, "lit": 0, "question": True}, {"in": "cut", "sfx": [{"name": "heartbeat", "at": 0.1}]}),
    ("Exactly how their hair looked?", V("street-walking-0", 10.0), {}),
    ("Probably not.", K(("PROBABLY NOT.", "yellow")), {}),
    ("Even close friends rarely notice.", V("laughing-4", 7.0), {}),
    ("Your partner might not even realise you got a haircut.", V("first-date-0", 6.0), {"sfx": [{"name": "pop", "at": "@haircut"}]}),
    ("And that's with you paying attention to the world.", V("street-walking-5", 6.0), {}),
    ("Now imagine how little they remember about you.", I("c7-world", (.5, .5), 1.3), {}),
    ("Your best days and your worst days blur together", I("c6-calendar", (.5, .35), 1.2, drift=-0.1), {}),
    ("into one ordinary picture in other people's minds.", I("c4-wall", (.5, .45), 1.1), {}),
    ("So stop treating every bad hair day like a public event.", I("c6-street", (.5, .3), 1.5), {"punch": {"at": "@public", "zoom": 2.0, "focus": [.5, .25]}}),
    ("To everyone else, it's just a normal Tuesday.", I("c6-cafe", (.45, .45), 1.1), {"overlays": [TAG("TUESDAY  8:14 AM")]}),
    ("And that brings us to the last trick.", V("cinema-1", 3.0), {}),
    ("It's the strangest one, and it's also the most powerful.", K("THE STRANGEST", ("THE MOST POWERFUL", "yellow"), times=[0.0, "@most"]), {"sfx": [{"name": "riser", "at": "@powerful+0.6", "gain": 0.7}]}),
]

CH7 = [
    ("Trick number seven. Embarrass yourself on purpose.", CH(7, "EMBARRASS YOURSELF ON PURPOSE", "@Embarrass"), {"chapter": True, "music": "confident"}),
    ("This sounds crazy,", I("tshirt-doorway", (.2, .35), 1.8), {"sfx": [{"name": "scratch", "at": 0.1}]}),
    ("but it's one of the most famous exercises in therapy.", V("therapy-1", 3.0), {}),
    ("The psychologist Albert Ellis created something he called", V("therapy-6", 0.5, 1.1), {"overlays": [LT("ALBERT ELLIS", "Psychologist, founder of REBT", at="@Albert")]}),
    ("a shame attacking exercise.", K(("SHAME-ATTACKING", "yellow"), "EXERCISE", times=[0.0, "@exercise"]), {}),
    ("You deliberately do something mildly embarrassing in public.", I("tshirt-doorway", (.45, .5), 1.0), {}),
    ("Nothing harmful, nothing rude, just a little bit odd.", K("NOTHING HARMFUL", "NOTHING RUDE", ("JUST A LITTLE ODD", "yellow"), times=[0.0, "@rude-0.4", "@just"]), {"sfx": [{"name": "pop", "at": "@rude-0.4"}, {"name": "pop", "at": "@just"}]}),
    ("Ask a shop assistant what year it is.", I("c7-shop", (.45, .45), 1.1), {"punch": {"at": "@year", "zoom": 1.5, "focus": [.5, .42]}, "sfx": [{"name": "pop", "at": "@year"}]}),
    ("Wear two different socks.", V("socks-2", 3.0), {}),
    ("Walk a banana on a lead down the street.", I("c7-banana", (.5, .5), 1.0, to=[.55, .65], to_zoom=1.6, drift=0), {"sfx": [{"name": "pop", "at": "@banana"}]}),
    ("Why would anyone do this?", K(("WHY?", "yellow")), {}),
    ("Because your brain learns from evidence, not from logic.", I("c7-brain", (.62, .5), 1.4), {"sfx": [{"name": "correct", "at": "@evidence", "gain": 0.5}]}),
    ("You can tell yourself a thousand times that nobody cares,", V("nervous-1", 3.0, 1.15), {}),
    ("but your fear only shrinks when you see it with your own eyes.", V("eye", 3.0, 1.2), {}),
    ("You do the awkward thing,", I("c7-banana", (.5, .4), 1.6), {}),
    ("and the world keeps turning.", I("c7-world", (.5, .5), 1.0, spin=3), {"amb": {"name": "crowd-murmur", "gain": 0.12}}),
    ("People glance for a second,", V("street-walking-0", 15.0), {}),
    ("and then they go back to their phones.", V("phone-street-2", 2.0), {}),
    ("Do it a few times, and the spotlight starts to lose its power over you.", I("switch-off", (.5, .45), 1.2), {"fx": [{"name": "light_off", "at": "@lose"}], "sfx": [{"name": "switch", "at": "@lose"}]}),
    ("So let's recap.", R(-1), {"pause_before": 0.25, "music": "intrigue"}),
    ("Stop hiding your nerves.", R(0), {"in": "cut", "sfx": [{"name": "pop", "at": 0.05}]}),
    ("Point your attention outward.", R(1), {"in": "cut", "sfx": [{"name": "pop", "at": 0.05}]}),
    ("Remember that your mistakes look braver than they feel.", R(2), {"in": "cut", "sfx": [{"name": "pop", "at": 0.05}]}),
    ("You're judged less harshly than you fear.", R(3), {"in": "cut", "sfx": [{"name": "pop", "at": 0.05}]}),
    ("You were probably liked more than you think.", R(4), {"in": "cut", "sfx": [{"name": "pop", "at": 0.05}]}),
    ("Nobody tracks your bad days.", R(5), {"in": "cut", "sfx": [{"name": "pop", "at": 0.05}]}),
    ("And when you're ready, embarrass yourself on purpose.", R(6), {"in": "cut", "sfx": [{"name": "sparkle", "at": 0.05}]}),
    ("Because here's the truth we started with.", I("stage-spotlight", (.5, .5), 1.0, drift=0.08), {"music": "warm", "pause_before": 0.3}),
    ("You are the centre of your own world.", I("tiny-planet", (.5, .48), 1.0, to_zoom=1.5, drift=0), {}),
    ("But in everyone else's world, you're a background character.", I("c7-extra", (.5, .5), 1.0, drift=0.06), {}),
    ("And that's not sad.", K("THAT'S NOT SAD."), {}),
    ("It's freedom.", I("c7-free", (.5, .45), 1.2), {"in": "flash", "sfx": [{"name": "reveal", "at": 0.05}]}),
    ("You can stop performing,", V("freedom-5", 1.0), {}),
    ("and start living.", V("freedom-0", 1.0), {}),
    ("If this video helped you, send it to someone who overthinks everything.", K("SEND THIS TO SOMEONE", ("WHO OVERTHINKS", "yellow"), ("EVERYTHING", "yellow"), times=["@send", "@who", "@everything"]), {"sfx": [{"name": "pop", "at": "@send"}, {"name": "pop", "at": "@who"}]}),
    ("And I'll see you in the next one.", I("c7-free", (.5, .45), 1.3, drift=-0.12), {}),
]

CHAPTERS = [CH1, CH2, CH3, CH4, CH5, CH6, CH7]
TRANS_SFX = {"whip": "swoosh-fast", "zoom": "sweep", "flash": "swoosh", "glitch": "glitch-hit"}


def kind(v):
    return "img" if "img" in v else "video" if "video" in v else "mg"


def auto(shots):
    out, prev = [], None
    for sh in shots:
        sh = dict(sh)
        k = kind(sh["v"])
        if sh.pop("chapter", False):
            sh.setdefault("in", "dip")
            sh.setdefault("pause_before", 0.35)
            sh["sfx"] = [{"name": "whoosh", "at": -0.15}] + sh.get("sfx", [])
        if "in" not in sh and prev:
            sh["in"] = ("flash" if prev != "mg" else "cut") if k == "mg" else \
                "whip" if prev == "mg" or (prev, k) == ("img", "video") else \
                "zoom" if (prev, k) == ("video", "img") else "cut"
        t = sh.get("in")
        if t in TRANS_SFX:
            sh["sfx"] = [{"name": TRANS_SFX[t], "gain": 0.7}] + sh.get("sfx", [])
        v = sh["v"]
        if v.get("mg") == "chapter":
            sh["sfx"] = sh.get("sfx", []) + [{"name": "trailer", "at": 0.0, "gain": 0.7}, {"name": "boom", "at": v["sub_at"], "gain": 0.7}]
        if k == "mg" and v["mg"] in ("kinetic", "chapter", "list", "year", "recap", "versus", "bars"):
            sh.setdefault("captions", False)
        for ov in sh.get("overlays", []):
            if ov["mg"] == "title":
                sh["sfx"] = sh.get("sfx", []) + [{"name": "reveal", "at": ov["at"]}, {"name": "impact", "at": ov["at"], "gain": 0.6}]
            if ov["mg"] == "lower_third":
                sh["sfx"] = sh.get("sfx", []) + [{"name": "swoosh-fast", "at": ov["at"], "gain": 0.5}]
        out.append(sh)
        prev = k
    return out


def words(s):
    return [re.sub(r"[^a-z0-9']", "", w.lower()) for w in s.split()]


def main():
    intro = json.loads((HERE / "video.json").read_text())
    shots = [dict(s) for s in intro["shots"]]
    cues = [{"shot": 0, "music": TRACKS["intrigue"][0], "start": TRACKS["intrigue"][1]},
            {"shot": 20, "music": TRACKS["confident"][0], "start": TRACKS["confident"][1]}]
    used = {"intrigue", "confident"}
    for n, ch in enumerate(CHAPTERS, 1):
        want = words((HERE / "chapters" / f"ch{n}.txt").read_text())
        got = [w for text, _, _ in ch for w in words(text)]
        if want != got:
            i = next(i for i, (a, b) in enumerate(zip(want + ["<end>"], got + ["<end>"])) if a != b)
            raise SystemExit(f"ch{n}: shot text differs from the script at word {i}: script {want[i:i + 6]} vs shots {got[i:i + 6]}")
        built = auto([{"text": text, "v": v, **ex} for text, v, ex in ch])
        for sh in built:
            m = sh.pop("music", None)
            if m:
                cue = {"shot": len(shots), "music": TRACKS[m][0]}
                if m not in used or sh.pop("music_restart", False):
                    cue["start"] = TRACKS[m][1]
                    used.add(m)
                cues.append(cue)
            shots.append(sh)
    spec = {"out": "../output/spotlight-effect-full.mp4",
            "audio": ["voice-cand-1.wav"] + [f"chapters/ch{n}.wav" for n in range(1, 8)],
            "take_gap": 0.5, "speed": 1.0, "music_cues": cues, "music_volume": 0.36, "fade_out": 2.0, "progress": True,
            "shots": shots}
    (HERE / "full.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False))
    n_img = sum(1 for s in shots if "img" in s["v"])
    n_vid = sum(1 for s in shots if "video" in s["v"])
    print(f"{len(shots)} shots: {n_img} AI images, {n_vid} stock videos, {len(shots) - n_img - n_vid} motion graphics; {len(cues)} music cues")


if __name__ == "__main__":
    main()
