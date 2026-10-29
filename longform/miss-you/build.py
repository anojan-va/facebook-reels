"""Build parts/partN.json for "How to Make Someone Miss You (Without Playing Games)".

Editing style for this video (different from videos 1 and 2 on purpose): black-and-white stock so the yellow man is
the only colour, cinematic letterbox bars on the Emma story, white "LESSON 0N" cards, polaroid memories,
notification banners, punch captions (spoken word grows and turns yellow), iris and push transitions, no chip/bar.
Usage: python3 build.py
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
IMG = (HERE / "img").resolve()


def I(n, f=(.5, .5), z=1.1, **kw):
    return {"img": f"../img/{n}.jpg", "focus": list(f), "zoom": z, **kw}


def V(n, st=1.0, z=1.08, **kw):
    return {"video": f"../stock/{n}.mp4", "start": st, "zoom": z, **kw}


def K(*lines, times=None, **kw):
    lines = [[l, "white"] if isinstance(l, str) else list(l) for l in lines]
    return {"mg": "kinetic", "lines": lines, "times": times or [0.0] * len(lines), **kw}


def M(*lines, mark=None, times=None, **kw):
    return {"mg": "marker", "lines": list(lines), "mark": mark or [lines[-1]], "times": times or [0.0] * len(lines), **kw}


def Q(text, end=None, width=26):
    return {"mg": "quote", "text": text, **({"end": end} if end else {}), "width": width}


def LESSON(num, title, title_at=0.4):
    return {"mg": "lesson", "num": num, "title": title, "title_at": title_at}


def CHAT(messages, title="Emma", status=None, status_at=None):
    return {"mg": "chat", "messages": messages, "title": title, **({"status": status, "status_at": status_at} if status else {})}


def POL(*items):
    return {"mg": "polaroid", "items": [[str(IMG / f"{n}.jpg"), cap, at] for n, cap, at in items]}


def VS(left, right, at, left_at=0.0):
    return {"mg": "versus", "left": left, "right": right, "at": at, "left_at": left_at}


def NOTE(text, at=0.1, title="Emma", dur=None):
    return {"mg": "notify", "title": title, "text": text, "at": at, **({"dur": dur} if dur else {})}


def TITLE(text, at):
    return {"mg": "title", "text": text, "at": at, "y": 0.78, "size": 120}


LB = ["letterbox"]   # story-moment look

TRACKS = {"tense": ("../../../reels/audio/music/out-of-this-world.mp3", 60.0),
          "intrigue": ("../../../reels/audio/music/echoes.mp3", 60.0),
          "confident": ("../../../reels/audio/music/unforgiven.mp3", 110.0),
          "warm": ("../../../reels/audio/music/fifth-of-february.mp3", 45.0),
          "sad": ("../../../reels/audio/music/silent-descent.mp3", 40.0)}

P1 = [
    ("Here's a strange truth.", K(("A STRANGE TRUTH", "yellow")), {"sfx": ["hook"], "music": "tense", "shake": [0.05]}),
    ("The more you try to make someone miss you,", I("m-juggle", (.5, .45), 1.0, to_zoom=1.5, drift=0), {}),
    ("the less they actually do.", M("THE LESS THEY", "ACTUALLY DO", times=[0.0, "@actually"]), {"sfx": [{"name": "bass", "at": "@do", "gain": 0.6}]}),
    ("You've been there.", V("sad-man-3", 2.0, 1.15), {}),
    ("You're the one who texts first. Every time.",
     CHAT([["Morning! ☀️", "me", 0.2], ["How did the meeting go?", "me", "@first"], ["Still on for tonight?", "me", "@every"],
           ["Hello?", "me", "@time"]], title="Jordan"),
     {"sfx": [{"name": "pop", "at": 0.2}, {"name": "pop", "at": "@first"}, {"name": "pop", "at": "@every"}, {"name": "pop", "at": "@time"}]}),
    ("You're the one who plans, who checks in, who remembers the little things.", I("m-juggle", (.6, .3), 1.8), {}),
    ("And if you stopped, just for a week,", V("phone-notification-0", 1.0, 1.1), {}),
    ("you're scared of what you'd find out.", I("m-staring", (.55, .4), 1.0, to_zoom=1.6, drift=0), {"sfx": [{"name": "heartbeat", "at": "@scared"}]}),
    ("That they wouldn't even notice.", K("THEY WOULDN'T", ("EVEN NOTICE", "red"), times=[0.0, "@even"]), {"shake": ["@notice"], "sfx": [{"name": "boom", "at": "@notice", "gain": 0.6}]}),
    ("So you look it up. How to make someone miss you.", V("night-phone-call-1", 2.0, 1.15), {}),
    ("And everything you find is a game.", I("m-chess", (.4, .5), 1.0), {"punch": {"at": "@game", "zoom": 1.7, "focus": [.38, .3]}}),
    ("Wait three hours before you reply.", {"mg": "year", "from": 0, "to": 3, "roll": 0.8, "label": "HOURS BEFORE YOU REPLY"}, {"sfx": [{"name": "tick", "at": 0.2}, {"name": "tick", "at": 0.5}, {"name": "tick", "at": 0.8}]}),
    ("Post a picture where you look happy without them.", I("m-mask", (.45, .35), 1.2), {"sfx": [{"name": "shutter", "at": "@picture"}]}),
    ("Go cold. Make them jealous.", K("GO COLD.", ("MAKE THEM JEALOUS.", "red"), times=[0.0, "@make"]), {}),
    ("Disappear and see if they chase you.", I("m-bus", (.5, .5), 1.0), {}),
    ("I tried most of those.", V("sad-man-2", 3.0, 1.15), {"pause_before": 0.25}),
    ("And I'm going to save you the trouble: they work for about two days.", M("THEY WORK FOR", "ABOUT TWO DAYS", times=[0.0, "@about"]), {}),
    ("Then you're back where you started,", I("m-staring", (.5, .4), 1.2), {}),
    ("except now you're also exhausted from pretending.", I("m-mask", (.5, .4), 1.0, drift=-0.08), {}),
    ("So in this video, I'm not going to give you tricks.", K("NO TRICKS.", times=[0.0]), {"music": "intrigue", "pause_before": 0.25}),
    ("I'm going to tell you what actually makes someone miss you,", I("m-empty-outline", (.6, .5), 1.0, drift=0.07), {}),
    ("the real reasons people feel your absence,", I("m-empty-outline", (.78, .45), 1.6), {}),
    ("and how to become that person without playing a single game.", I("m-road", (.5, .5), 1.0, to_zoom=1.4, drift=0), {}),
    ("And at the end, I'll tell you the one thing nobody wants to hear about this topic.", M("THE ONE THING", "NOBODY WANTS", "TO HEAR", mark=["NOBODY WANTS"], times=[0.0, "@nobody", "@hear"]), {}),
    ("It's the part that finally set me free.", V("road-trip-7", 2.0), {}),
    ("A few years ago I was seeing someone I'll call Emma.", V("couple-walking-3", 2.0), {"fx": [{"name": "letterbox", "anim": True}], "in": "iris", "pause_before": 0.35, "music": "sad"}),
    ("And I was all in.", I("m-door-coffee", (.5, .5), 1.0), {"fx": LB}),
    ("Good morning texts every day. I replied in seconds.",
     CHAT([["Good morning beautiful ☀️", "me", 0.2], ["Have a great day!", "me", "@every"], ["hey", "them", "@replied"], ["Hey!! What's up? \U0001F60A", "me", "@seconds"]]),
     {"sfx": [{"name": "pop", "at": 0.2}, {"name": "pop", "at": "@every"}, {"name": "pop", "at": "@replied"}, {"name": "pop", "at": "@seconds"}]}),
    ("I cancelled plans with my friends whenever she was free.", I("m-cancel-friends", (.5, .5), 1.0), {"fx": LB}),
    ("I thought that's what love looked like. Being there. Always.", I("m-door-coffee", (.5, .4), 1.6), {"fx": LB}),
    ("And slowly, I watched her get bored.", I("m-bored-emma", (.6, .5), 1.0, drift=0.08), {"fx": LB}),
    ("Not mean. Not cold. Just... less interested.", V("couple-bored-1", 1.0), {"fx": LB}),
    ("Her replies got lazier. She stopped asking about my day.",
     CHAT([["How was your day? \U0001F60A", "me", 0.2], ["fine", "them", "@lazier"], ["Mine was crazy, so...", "me", "@stopped"], ["\U0001F44D", "them", "@day"]]),
     {"sfx": [{"name": "pop", "at": "@lazier"}, {"name": "pop", "at": "@day"}]}),
    ("And one night she said something I'll never forget.", I("m-bored-emma", (.65, .3), 1.8), {"fx": LB, "sfx": [{"name": "heartbeat", "at": "@never"}]}),
    ("She said, \"I always know exactly where you are.\"", Q("\"I always know exactly where you are.\"", end="@are"), {}),
    ("She meant it kindly. But it hit me like a slap.", I("m-bored-emma", (.45, .3), 1.9), {"fx": LB, "shake": ["@slap"], "sfx": [{"name": "glass", "at": "@slap"}]}),
    ("Because she was right. There was no space for her to miss me.", I("m-bridge", (.5, .5), 1.0, drift=0.06), {"fx": LB}),
    ("I had made myself so available that I'd become furniture.", I("m-bored-emma", (.5, .55), 1.1), {"fx": LB}),
    ("Nice furniture. But furniture.", K("NICE FURNITURE.", ("BUT FURNITURE.", "yellow"), times=[0.0, "@but"]), {}),
]

P2 = [
    ("And here's the first thing I learned, and it sounds obvious, but almost nobody lives by it.",
     LESSON("01", ["YOU CAN'T MISS", "WHO NEVER LEAVES"], title_at=0.7), {"chapter": True, "music": "intrigue"}),
    ("You cannot miss someone who never leaves.", Q("You cannot miss someone who never leaves.", end="@leaves"), {}),
    ("Missing someone needs a gap. A little distance.", I("m-bridge", (.5, .5), 1.0, drift=-0.1), {}),
    ("A moment where you're not there, and they notice.", I("m-empty-outline", (.5, .5), 1.0, to=[.72, .45], to_zoom=1.6, drift=0), {}),
    ("Now, that does not mean you should disappear on purpose.", K("DON'T DISAPPEAR", ("ON PURPOSE", "red"), times=[0.0, "@purpose"]), {"pause_before": 0.25}),
    ("That's the game, and games are just anxiety wearing a costume.", I("m-mask", (.4, .35), 1.0), {"punch": {"at": "@costume", "zoom": 1.7, "focus": [.4, .3]}}),
    ("If you go silent to punish someone or to test them, they can feel it.", I("m-chess", (.45, .5), 1.2), {}),
    ("It makes you look insecure, not interesting.", VS(["INSECURE", "SILENCE"], ["INTERESTING", "A LIFE"], "@interesting"), {}),
    ("I've watched friends do this.", V("friends-laughing-7", 2.0), {}),
    ("They go silent for three days, then check their phone every five minutes to see if the other person noticed.",
     I("m-chain", (.5, .55), 1.0, to_zoom=1.5, drift=0), {"sfx": [{"name": "tick", "at": "@five"}, {"name": "tick", "at": "@five+0.4"}]}),
    ("That's not space. That's a hostage situation with your own phone.", I("m-chain", (.55, .75), 2.0), {"sfx": [{"name": "zap", "at": "@hostage"}]}),
    ("The real version is simpler.", K(("THE REAL VERSION", "yellow")), {"music": "warm", "pause_before": 0.25}),
    ("You stop filling every gap yourself.", I("m-texts-first", (.45, .45), 1.0), {}),
    ("You let a conversation end without sending one more message.", I("m-phone-down", (.45, .6), 1.2), {}),
    ("You let them text first sometimes.", V("phone-notification-0", 3.0, 1.15), {"overlays": [NOTE("Hey! Was thinking about you \U0001F60A", at=0.4, title="Emma")]}),
    ("Not as a tactic.", K("NOT A TACTIC."), {}),
    ("Just because you trust that the connection doesn't need you to hold it up every single second.", I("m-calm-bench", (.5, .5), 1.0, drift=0.07), {}),
    ("After Emma, I made a rule for myself.", V("sad-man-6", 2.0), {"fx": LB, "pause_before": 0.3}),
    ("If I'd sent the last two messages, I'd wait.",
     CHAT([["How was your trip?", "me", 0.1], ["Send me a photo!", "me", "@two"]], title="Sam"), {"sfx": [{"name": "pop", "at": 0.1}, {"name": "pop", "at": "@two"}]}),
    ("Not to win anything.", K(("NOT TO WIN.", "white")), {}),
    ("Just to see what happened when I stopped carrying the whole conversation.", I("m-juggle", (.5, .45), 1.2), {}),
    ("And honestly, the first few times were terrifying.", V("night-phone-call-4", 2.0), {}),
    ("I'd stare at my phone like it owed me money.", I("m-staring", (.55, .45), 1.0), {"punch": {"at": "@owed", "zoom": 1.8, "focus": [.6, .35]}}),
    ("But something changed.", K(("SOMETHING CHANGED.", "yellow")), {}),
    ("The people who cared started showing up.", V("friends-laughing-3", 2.0), {"overlays": [NOTE("Coffee this week?", at=0.5, title="Sam")]}),
    ("And the ones who didn't... well, I finally had my answer.", I("m-road", (.5, .5), 1.0, drift=0.06), {}),
]

P3 = [
    ("And that brings me to the second thing, the one that actually made the difference.",
     LESSON("02", ["BE WORTH", "MISSING"], title_at=0.7), {"chapter": True, "music": "confident"}),
    ("People don't miss you because you're gone.", I("m-empty-outline", (.5, .5), 1.0), {}),
    ("They miss you because of what's missing when you're gone.", M("THEY MISS", "WHAT'S MISSING", times=[0.0, "@what's"]), {}),
    ("Think about that for a second.", V("sad-man-6", 4.0), {}),
    ("If someone spends a weekend without you, what exactly are they losing?", I("m-empty-outline", (.75, .45), 1.6), {}),
    ("If the honest answer is \"someone who agrees with everything and is always free,\" there's nothing to miss.",
     VS(["ALWAYS FREE", "NOTHING TO MISS"], ["FULL LIFE", "WORTH MISSING"], 999.0), {}),
    ("But if you're the person who makes them laugh until it hurts,", I("m-laugh", (.6, .45), 1.0), {}),
    ("who notices when they're quiet,", V("couple-coffee-6", 2.0), {}),
    ("who drags them into some ridiculous adventure,", V("road-trip-2", 2.0), {}),
    ("that's a real hole when you're not there.", I("m-empty-outline", (.72, .5), 1.4, drift=-0.1), {}),
    ("So the question isn't \"How do I make them miss me?\"", K("NOT \"HOW DO I MAKE", "THEM MISS ME?\"", times=[0.0, "@them"]), {}),
    ("The question is \"What am I bringing that's worth missing?\"", M("WHAT AM I BRINGING", "THAT'S WORTH", "MISSING?", times=[0.0, "@that's", "@missing"]), {"sfx": [{"name": "reveal", "at": "@worth"}]}),
    ("And this is where most people get it backwards.", I("m-juggle", (.5, .5), 1.0), {"pause_before": 0.25}),
    ("They try to make themselves more available, when what they actually need is to make themselves more alive.",
     VS(["MORE", "AVAILABLE"], ["MORE", "ALIVE"], "@alive"), {"sfx": [{"name": "reveal", "at": "@alive"}]}),
    ("A life of your own.", I("m-hobbies", (.5, .5), 1.0, to_zoom=1.3, drift=0), {}),
    ("Your own friends,", V("friends-laughing-3", 4.0), {"in": "push"}),
    ("your own plans,", V("road-trip-7", 4.0), {"in": "push"}),
    ("your own weird hobbies,", V("climbing-2", 2.0), {"in": "push"}),
    ("the gym,", I("m-gym", (.5, .4), 1.3), {"in": "push"}),
    ("the guitar you never finish learning.", I("m-hobbies", (.2, .25), 2.2), {"in": "push"}),
    ("Not to look busy. To actually be someone with a world worth stepping into.", I("m-hobbies", (.5, .5), 1.0, drift=-0.1), {}),
    ("The funniest part is that when I finally started living like this,", V("climbing-1", 2.0), {"fx": LB, "pause_before": 0.3, "music": "warm"}),
    ("I wasn't even trying to make anyone miss me.", I("m-calm-bench", (.5, .45), 1.2), {"fx": LB}),
    ("I joined a Thursday night climbing group because a friend dragged me.", I("m-climb", (.75, .5), 1.0, to=[.79, .4], to_zoom=1.7, drift=0), {"fx": LB}),
    ("And three weeks in, the girl I'd just started seeing said,", V("couple-coffee-1", 3.0), {"fx": LB}),
    ("\"Wait, you're not free Thursday? What do you even do there?\"",
     CHAT([["Dinner Thursday?", "them", 0.1], ["Can't, climbing night \U0001F9D7", "me", "@thursday"], ["Wait what?? What do you even do there? \U0001F602", "them", "@even"]], title="Mia"),
     {"sfx": [{"name": "pop", "at": 0.1}, {"name": "pop", "at": "@thursday"}, {"name": "pop", "at": "@even"}]}),
    ("She was curious.", I("m-curious", (.35, .4), 1.3), {"fx": LB}),
    ("For the first time, someone was curious about my life instead of just expecting me to be in theirs.", I("m-curious", (.5, .5), 1.0, drift=0.06), {"fx": LB}),
    ("There's a principle psychologists talk about called scarcity.", V("bus-6", 2.0), {"captions": False, "overlays": [TITLE("SCARCITY", "@scarcity")], "pause_before": 0.25}),
    ("Robert Cialdini wrote about it years ago.", V("diner-1", 1.0), {"overlays": [{"mg": "lower_third", "title": "ROBERT CIALDINI", "sub": "Influence: The Psychology of Persuasion (1984)", "at": 0.1}]}),
    ("We value things more when they're a little harder to get.", K("HARDER TO GET", ("= MORE VALUE", "yellow"), times=[0.0, "@harder+0.4"]), {}),
    ("But here's how I see it.", V("sad-man-3", 5.0), {}),
    ("Scarcity is ugly when you fake it.", I("m-chess", (.4, .45), 1.4), {"sfx": [{"name": "wrong", "at": "@fake", "gain": 0.4}]}),
    ("It's magnetic when it's real.", I("m-climb", (.78, .45), 1.4), {"sfx": [{"name": "sparkle", "at": "@real"}]}),
    ("When you genuinely have a full life, your time becomes valuable on its own.", V("running-0", 2.0), {}),
    ("You don't have to pretend.", K(("NO PRETENDING.", "yellow")), {}),
]

P4 = [
    ("The third thing I learned is about the moments themselves.", LESSON("03", ["LEAVE", "MEMORIES"], title_at=0.7), {"chapter": True, "music": "warm"}),
    ("Because when someone misses you, they don't miss you in general. They miss specific moments.", V("couple-walking-0", 2.0), {}),
    ("The way you laughed at that terrible movie together.", I("m-movie", (.55, .45), 1.0), {}),
    ("The song you always played in the car.", I("m-car-song", (.4, .4), 1.0), {}),
    ("The stupid inside joke that nobody else gets.", V("couple-laughing-3", 2.0), {}),
    ("The way you always order the same dessert and then steal theirs.", I("m-dessert", (.6, .5), 1.0), {"sfx": [{"name": "pop", "at": "@steal"}]}),
    ("Nobody has ever said, \"I really miss how available he was.\"", Q("\"I really miss how available he was.\"", end="@was"), {"sfx": [{"name": "scratch", "at": "@was+0.2"}]}),
    ("They say, \"I miss how he made me laugh.\" \"I miss our Sunday pancakes.\"",
     POL(("m-laugh", "how he made me laugh", "@laugh-0.6"), ("m-pancakes", "Sunday pancakes", "@sunday")),
     {"sfx": [{"name": "shutter", "at": "@laugh-0.6"}, {"name": "shutter", "at": "@sunday"}]}),
    ("Moments. Always moments.",
     POL(("m-movie", "that terrible movie", -1.0), ("m-car-song", "our song", 0.05), ("m-dessert", "stolen dessert", "@always")),
     {"in": "cut", "sfx": [{"name": "shutter", "at": 0.05}, {"name": "shutter", "at": "@always"}]}),
    ("I really believe the people we miss most are the ones who leave little pieces of themselves in our everyday lives.", V("couple-walking-2", 2.0), {"pause_before": 0.25}),
    ("So when they hear that song, they think of you.", I("m-coffee-shop", (.6, .4), 1.1), {}),
    ("When they walk past that diner, they think of you.", V("diner-1", 3.0), {}),
    ("That's not manipulation.", K("NOT MANIPULATION.", times=[0.0]), {}),
    ("That's just what happens when you actually share your life with someone.", V("couple-laughing-5", 2.0), {}),
    ("So stop trying to be impressive and start trying to be memorable.", VS(["STOP BEING", "IMPRESSIVE"], ["START BEING", "MEMORABLE"], "@memorable"), {"sfx": [{"name": "reveal", "at": "@memorable"}]}),
    ("Do something new together.", V("road-trip-2", 6.0), {"in": "push"}),
    ("Start a tiny ritual.", I("m-pancakes", (.5, .45), 1.1), {"in": "push"}),
    ("Give them a story they'll want to tell later.", V("campfire-3", 2.0), {"in": "push"}),
    ("One great evening does more than a hundred \"good morning\" texts.", VS(["100 TEXTS", "MORNINGS"], ["ONE GREAT", "EVENING"], "@than"), {}),
]

P5 = [
    ("And there's one more piece to this that changed everything for me. How you leave.",
     LESSON("04", ["HOW YOU", "LEAVE"], title_at=0.7), {"chapter": True, "music": "intrigue"}),
    ("There's a well-known effect in psychology called the Zeigarnik effect.", I("m-tv-question", (.5, .5), 1.0), {"captions": False, "overlays": [TITLE("THE ZEIGARNIK EFFECT", "@zeigarnik")]}),
    ("Our minds keep coming back to things that feel unfinished.", M("UNFINISHED THINGS", "STAY IN", "YOUR HEAD", mark=["UNFINISHED THINGS"], times=[0.0, "@back", "@unfinished"]), {}),
    ("An interrupted story sticks in your head longer than one that's wrapped up neatly.", I("m-tv-question", (.75, .4), 1.6), {}),
    ("It's why TV shows end on cliffhangers.", V("movie-night-4", 2.0), {"sfx": [{"name": "riser", "at": "@cliffhangers", "gain": 0.6}]}),
    ("And it works with people too, in a much more innocent way.", V("couple-laughing-0", 2.0), {}),
    ("I used to be the guy who stayed until the very end.", I("m-closing-bar", (.35, .5), 1.0), {"fx": LB, "pause_before": 0.3}),
    ("The last one at the bar,", I("m-closing-bar", (.25, .55), 1.7), {"fx": LB}),
    ("the last text of the night,", I("m-texts-first", (.4, .45), 1.4), {"fx": LB}),
    ("the phone call that went on until both of us were yawning.", I("m-yawn-call", (.35, .55), 1.2), {"fx": LB}),
    ("And every conversation slowly ran out of gas.", V("sad-man-2", 6.0), {"fx": LB}),
    ("Now I do the opposite.", K(("THE OPPOSITE.", "yellow")), {"music": "confident"}),
    ("When we're laughing, when the energy is at its best,", I("m-laugh", (.5, .45), 1.0), {}),
    ("that's when I say, \"I have to go, but tell me the rest of that story tomorrow.\"", I("m-wave-cafe", (.45, .5), 1.0, to_zoom=1.3, drift=0), {}),
    ("And they always do.", V("phone-notification-0", 4.0, 1.15), {"overlays": [NOTE("Ok so where was I... \U0001F602", at=0.15, title="Mia")]}),
    ("Because now there's something to come back to.", I("m-wave-cafe", (.6, .5), 1.4), {}),
    ("Leave while it's good.", M("LEAVE WHILE", "IT'S GOOD", times=[0.0, "@good"]), {"sfx": [{"name": "sparkle", "at": "@good"}]}),
    ("Leave them wanting the next conversation, not relieved that this one is finally over.",
     {"mg": "curve", "title": "HOW THEY REMEMBER IT", "draw": 2.2, "peak_at": "@wanting", "end_at": "@relieved"}, {}),
]

P6 = [
    ("Now let's talk about the hardest part. What do you do when they pull away?",
     LESSON("05", ["WHEN THEY", "PULL AWAY"], title_at=0.7), {"chapter": True, "music": "tense"}),
    ("This is where most of us lose it.", V("sad-man-3", 2.0), {}),
    ("They take longer to reply, and the panic kicks in.", I("m-staring", (.55, .4), 1.0), {"sfx": [{"name": "heartbeat", "at": "@panic"}, {"name": "heartbeat", "at": "@panic+0.45"}]}),
    ("You double text. Then triple text. You ask, \"Is everything okay?\" three different ways.",
     CHAT([["Hey?", "me", "@double"], ["Did you get my message?", "me", "@triple"], ["Is everything okay?", "me", "@okay"],
           ["Are we good?", "me", "@three"], ["Did I do something?", "me", "@different"]], title="Emma"),
     {"sfx": [{"name": "pop", "at": "@double"}, {"name": "pop", "at": "@triple"}, {"name": "pop", "at": "@okay"}, {"name": "pop", "at": "@three"}, {"name": "pop", "at": "@different"}]}),
    ("You start analysing every emoji like it's a secret code.", I("m-pacing", (.5, .5), 1.0), {"overlays": [{"mg": "scan", "box": [0.42, 0.25, 0.62, 0.8], "label": "DECODING EMOJI...", "at": 0.2}]}),
    ("I know that feeling in my chest.", V("sad-man-6", 3.0), {"pause_before": 0.25}),
    ("But chasing someone who's pulling away is like running after a bus that's already left.", I("m-bus", (.5, .5), 1.0, to=[.6, .45], to_zoom=1.4, drift=0), {}),
    ("You look desperate, you get out of breath,", I("m-bus", (.45, .35), 1.8), {"shake": ["@desperate"]}),
    ("and the bus doesn't stop anyway.", V("bus-3", 2.0), {}),
    ("And pulling away isn't always about you.", K("IT'S NOT ALWAYS", ("ABOUT YOU.", "yellow"), times=[0.0, "@about"]), {}),
    ("Sometimes people are stressed, busy, or going through something they haven't told anyone.", V("night-phone-call-4", 4.0), {}),
    ("Your panic turns their quiet week into a problem they now have to manage.", I("m-pacing", (.45, .45), 1.4), {}),
    ("What works is the opposite.", K(("THE OPPOSITE", "yellow")), {"music": "warm", "pause_before": 0.25}),
    ("Stay calm. Stay kind.", I("m-calm-bench", (.5, .45), 1.0, to_zoom=1.3, drift=0), {}),
    ("Say something simple and honest, once.", K("SIMPLE.", "HONEST.", ("ONCE.", "yellow"), times=["@simple", "@honest", "@once"]), {}),
    ("Something like, \"Hey, I've noticed we've been a bit distant. No pressure, I'm here if you want to talk.\"",
     CHAT([["Hey, I've noticed we've been a bit distant. No pressure, I'm here if you want to talk \U0001F642", "me", 0.6]]), {"sfx": [{"name": "pop", "at": 0.6}]}),
    ("And then go live your life. Really live it.", I("m-road", (.5, .5), 1.0, drift=0.07), {}),
    ("Go to the gym,", I("m-gym", (.5, .4), 1.2), {"in": "push"}),
    ("call your friends,", V("friends-laughing-3", 6.0), {"in": "push"}),
    ("finish that project.", I("m-hobbies", (.5, .5), 1.3), {"in": "push"}),
    ("The first time I actually did this, I expected it to backfire.", V("sad-man-2", 8.0), {"fx": LB, "pause_before": 0.3}),
    ("Instead, she called me two days later and said,", V("night-phone-call-1", 4.0), {"fx": LB, "overlays": [NOTE("Incoming call...", at="@called", title="Emma")]}),
    ("\"You're different lately. In a good way.\"", Q("\"You're different lately. In a good way.\"", end="@way"), {"sfx": [{"name": "sparkle", "at": "@way"}]}),
    ("I hadn't changed anything about how I felt about her.", V("couple-walking-3", 6.0), {"fx": LB}),
    ("I'd just stopped begging the relationship to prove itself every hour.", I("m-puppet", (.55, .5), 1.0), {"fx": LB}),
]

P7 = [
    ("And that leads me to the part I promised. The thing nobody wants to hear.",
     LESSON("06", ["NOBODY WANTS", "TO HEAR THIS"], title_at=0.7), {"chapter": True, "music": "sad"}),
    ("You can't actually make anyone miss you.", Q("You can't actually make anyone miss you.", end="@miss"), {"sfx": [{"name": "boom", "at": "@miss", "gain": 0.6}]}),
    ("I know. That's the title of the video.", K("I KNOW.", ("IT'S THE TITLE.", "yellow"), times=[0.0, "@title"]), {}),
    ("But it's the truth. You can't control what someone else feels.", I("m-puppet", (.55, .5), 1.0, to_zoom=1.4, drift=0), {}),
    ("All the waiting, the strategy, the perfectly timed posts,", I("m-chess", (.45, .45), 1.2), {}),
    ("none of it can create feelings that aren't there.", I("m-puppet", (.75, .55), 1.7), {}),
    ("What you can do is become someone worth missing.", M("BECOME SOMEONE", "WORTH MISSING", times=[0.0, "@worth"]), {"music": "warm", "pause_before": 0.25}),
    ("Someone with a full life,", I("m-hobbies", (.5, .5), 1.0), {"in": "push"}),
    ("who shares it generously,", V("couple-laughing-0", 3.0), {"in": "push"}),
    ("who leaves good memories behind,", POL(("m-movie", "movie night", 0.05), ("m-pancakes", "pancakes", 0.25), ("m-car-song", "our song", 0.45)),
     {"in": "push", "sfx": [{"name": "shutter", "at": 0.05}, {"name": "shutter", "at": 0.25}, {"name": "shutter", "at": 0.45}]}),
    ("who doesn't chase,", I("m-calm-bench", (.5, .45), 1.2), {"in": "push"}),
    ("and who knows their own value.", I("m-road", (.5, .45), 1.2), {"in": "push"}),
    ("I think about it like a campfire.", V("campfire-1", 2.0), {}),
    ("You don't chase people to make them sit by your fire.", I("m-campfire", (.4, .55), 1.1), {}),
    ("You just keep it burning.", V("campfire-3", 3.0, 1.2), {"sfx": [{"name": "sparkle", "at": "@burning"}]}),
    ("The people who are cold will find their way to you.", I("m-campfire", (.6, .5), 1.0, drift=-0.1), {}),
    ("And if you become that person, and they still don't miss you?", I("m-empty-outline", (.5, .5), 1.0), {"pause_before": 0.25}),
    ("That's not rejection. That's information.", VS(["NOT", "REJECTION"], ["IT'S", "INFORMATION"], "@information"), {"sfx": [{"name": "reveal", "at": "@information"}]}),
    ("It tells you this connection wasn't meant to be carried by you alone.", I("m-juggle", (.5, .5), 1.1), {}),
    ("And the space they leave behind is space for someone who will notice when you're gone.", I("m-road", (.5, .5), 1.0, to_zoom=1.4, drift=0), {}),
    ("Emma and I didn't end up together.", V("couple-walking-0", 6.0), {"fx": [{"name": "letterbox", "anim": True}], "in": "iris", "pause_before": 0.35}),
    ("But years later, she sent me a message out of nowhere.", I("m-balcony", (.5, .45), 1.0), {"fx": LB, "overlays": [NOTE("Hey stranger \U0001F642", at="@message", title="Emma", dur=2.5)]}),
    ("She said she'd heard our song in a coffee shop and thought of me.", I("m-coffee-shop", (.55, .45), 1.0, to_zoom=1.3, drift=0),
     {"fx": LB, "overlays": [NOTE("Heard our song today and thought of you", at=0.3, title="Emma")]}),
    ("And I smiled.", I("m-balcony", (.6, .28), 1.9), {"fx": LB}),
    ("Not because I wanted her back.", V("couple-walking-2", 3.0), {"fx": LB}),
    ("But because I realised I'd finally become the kind of person who leaves something behind.", I("m-balcony", (.5, .45), 1.0, drift=-0.1), {"fx": LB}),
    ("So don't play games.", {"mg": "checklist", "title": "HOW TO BE MISSED", "items": ["DON'T PLAY GAMES", "BUILD A LIFE", "SHARE THE GOOD PARTS", "LEAVE WHILE IT'S GOOD", "STOP CHASING"],
                               "times": [0.05, 999, 999, 999, 999]}, {"music": "confident", "pause_before": 0.25, "sfx": [{"name": "pop", "at": 0.05}]}),
    ("Build a life.", {"mg": "checklist", "title": "HOW TO BE MISSED", "items": ["DON'T PLAY GAMES", "BUILD A LIFE", "SHARE THE GOOD PARTS", "LEAVE WHILE IT'S GOOD", "STOP CHASING"],
                       "times": [-1, 0.05, 999, 999, 999]}, {"in": "cut", "sfx": [{"name": "pop", "at": 0.05}]}),
    ("Share the good parts.", {"mg": "checklist", "title": "HOW TO BE MISSED", "items": ["DON'T PLAY GAMES", "BUILD A LIFE", "SHARE THE GOOD PARTS", "LEAVE WHILE IT'S GOOD", "STOP CHASING"],
                               "times": [-1, -1, 0.05, 999, 999]}, {"in": "cut", "sfx": [{"name": "pop", "at": 0.05}]}),
    ("Leave while it's good.", {"mg": "checklist", "title": "HOW TO BE MISSED", "items": ["DON'T PLAY GAMES", "BUILD A LIFE", "SHARE THE GOOD PARTS", "LEAVE WHILE IT'S GOOD", "STOP CHASING"],
                                "times": [-1, -1, -1, 0.05, 999]}, {"in": "cut", "sfx": [{"name": "pop", "at": 0.05}]}),
    ("And stop chasing people who aren't walking toward you.", {"mg": "checklist", "title": "HOW TO BE MISSED", "items": ["DON'T PLAY GAMES", "BUILD A LIFE", "SHARE THE GOOD PARTS", "LEAVE WHILE IT'S GOOD", "STOP CHASING"],
                                                                "times": [-1, -1, -1, -1, 0.05]}, {"in": "cut", "sfx": [{"name": "sparkle", "at": 0.05}]}),
    ("The right people will miss you.", I("m-campfire", (.5, .5), 1.0, drift=0.06), {}),
    ("You won't even have to try.", M("YOU WON'T EVEN", "HAVE TO TRY", times=[0.0, "@have"]), {}),
    ("If this video helped you, send it to someone who always texts first.", K("SEND THIS TO SOMEONE", ("WHO ALWAYS TEXTS FIRST", "yellow"), times=["@send", "@always"]),
     {"sfx": [{"name": "pop", "at": "@send"}, {"name": "pop", "at": "@always"}]}),
    ("They need to hear this. And I'll see you in the next one.", I("m-road", (.5, .45), 1.1, drift=-0.12), {}),
]

PARTS = [P1, P2, P3, P4, P5, P6, P7]
SFX_FOR = {"iris": "reveal", "push": "swoosh-fast", "zoom": "sweep", "glitch": "glitch-hit", "flash": "swoosh"}


def kind(v):
    return "img" if "img" in v else "video" if "video" in v else "mg"


def auto(shots):
    """This video's transition grammar: iris into graphics, flash out of them, zoom from image to video,
    hard cuts between clips, a glitch when the tone turns. Each transition with its own sound."""
    out, prev = [], None
    for sh in shots:
        sh = dict(sh)
        k = kind(sh["v"])
        if sh.pop("chapter", False):
            sh.setdefault("in", "dip")
            sh["sfx"] = [{"name": "tunnel", "at": 0.0, "gain": 0.6}] + sh.get("sfx", [])
        if "in" not in sh and prev:
            sh["in"] = "iris" if k == "mg" and prev != "mg" else "flash" if prev == "mg" and k != "mg" else \
                "zoom" if (prev, k) == ("img", "video") else "cut"
        if sh.get("in") in SFX_FOR:
            sh["sfx"] = [{"name": SFX_FOR[sh["in"]], "gain": 0.55}] + sh.get("sfx", [])
        v = sh["v"]
        if k == "mg" and v["mg"] not in ("year",):
            sh.setdefault("captions", False)
        for ov in sh.get("overlays", []):
            if ov["mg"] == "title":
                sh["sfx"] = sh.get("sfx", []) + [{"name": "reveal", "at": ov["at"]}, {"name": "impact", "at": ov["at"], "gain": 0.6}]
            if ov["mg"] == "notify":
                sh["sfx"] = sh.get("sfx", []) + [{"name": "pop", "at": ov["at"], "gain": 1.2}]
            if ov["mg"] == "lower_third":
                sh["sfx"] = sh.get("sfx", []) + [{"name": "swoosh-fast", "at": ov["at"], "gain": 0.5}]
        if v.get("mg") == "lesson":
            sh["sfx"] = sh.get("sfx", []) + [{"name": "boom", "at": v["title_at"], "gain": 0.55}]
        out.append(sh)
        prev = k
    return out


def words(s):
    return [re.sub(r"[^a-z0-9']", "", w.lower()) for w in s.split()]


def main():
    total = 0
    for n, part in enumerate(PARTS, 1):
        want = words((HERE / "parts" / f"p{n}.txt").read_text())
        got = [w for t, _, _ in part for w in words(t)]
        if want != got:
            i = next(i for i, (a, b) in enumerate(zip(want + ["<end>"], got + ["<end>"])) if a != b)
            raise SystemExit(f"part {n}: shot text differs at word {i}: script {want[i:i + 6]} vs shots {got[i:i + 6]}")
        shots = auto([{"text": t, "v": v, **ex} for t, v, ex in part])
        cues, used = [], set()
        for i, sh in enumerate(shots):
            m = sh.pop("music", None)
            if m:
                cues.append({"shot": i, "music": TRACKS[m][0], **({"start": TRACKS[m][1]} if m not in used else {})})
                used.add(m)
        last = n == len(PARTS)
        spec = {"out": f"../../output/miss-you/part{n}.mp4", "audio": f"p{n}.wav", "speed": 1.0,
                "tail": 2.0 if last else 0.45, "music_fade": 2.0 if last else 0.5, "music_cues": cues, "music_volume": 0.33,
                **({"fade_out": 2.0} if last else {}),
                "style": {"grade": "bw", "captions": "punch", "caption_y": 0.84, "vignette": 0.42, "grain": 5},
                "shots": shots}
        (HERE / "parts" / f"part{n}.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False))
        kinds = [kind(s["v"]) for s in shots]
        print(f"part {n}: {len(shots)} shots ({kinds.count('img')} AI, {kinds.count('video')} stock, {kinds.count('mg')} graphics)")
        total += len(shots)
    print("total", total)


if __name__ == "__main__":
    main()
