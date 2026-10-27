"""Build parts/partN.json for "Why People Lose Interest in You", one render spec per part (rendered and reviewed
separately, merged at the end with merge.py).

Editing style differs from the Spotlight Effect video on purpose: warm grade, pill captions, "REASON 0N" cards,
chat / highlighter / quote / curve graphics, slide and blur transitions, a corner chip instead of a progress bar.
Usage: python3 build.py
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
OLD = "../../spotlight-effect/stock"   # clips reused from the previous video (paths relative to parts/)


def I(n, f=(.5, .5), z=1.1, **kw):
    return {"img": f"../img/{n}.jpg", "focus": list(f), "zoom": z, **kw}


def V(n, st=1.0, z=1.08, **kw):
    src = f"{OLD}/{n[4:]}.mp4" if n.startswith("old:") else f"../stock/{n}.mp4"
    return {"video": src, "start": st, "zoom": z, **kw}


def K(*lines, times=None, **kw):
    lines = [[l, "white"] if isinstance(l, str) else list(l) for l in lines]
    return {"mg": "kinetic", "lines": lines, "times": times or [0.0] * len(lines), **kw}


def M(*lines, mark=None, times=None, **kw):
    return {"mg": "marker", "lines": list(lines), "mark": mark or [lines[-1]], "times": times or [0.0] * len(lines), **kw}


def Q(text, end=None, by=None, width=26):
    return {"mg": "quote", "text": text, **({"end": end} if end else {}), **({"by": by} if by else {}), "width": width}


def REASON(num, title, title_at=0.35):
    return {"mg": "reason", "num": num, "title": title, "title_at": title_at}


def CHAT(messages, title="Michael", status=None, status_at=None):
    return {"mg": "chat", "messages": messages, "title": title,
            **({"status": status, "status_at": status_at} if status else {})}


def VS(left, right, at, left_at=0.0):
    return {"mg": "versus", "left": left, "right": right, "at": at, "left_at": left_at}


def LT(title, sub, at=0.1):
    return {"mg": "lower_third", "title": title, "sub": sub, "at": at}


def TITLE(text, at):
    return {"mg": "title", "text": text, "at": at, "y": 0.78, "size": 120}


FIXES = ["ASK THE SECOND QUESTION", "PUT YOUR PHONE AWAY", "BRING SOMETHING NEW", "HAVE A LIFE OF YOUR OWN",
         "BRING LIGHTNESS INTO THE ROOM", "LEAVE WHILE IT'S GOOD", "KEEP GROWING"]


def FIX(k):
    return {"mg": "checklist", "title": "THE FIX", "items": FIXES, "times": [-1.0] * k + [0.05] + [999.0] * (6 - k)}


def TOLD(k):
    items = ["HE LIKES YOU A LOT", "HE LIKES YOU AN AVERAGE AMOUNT", "NOBODY KNOWS"]
    return {"mg": "checklist", "title": "WHAT THEY WERE TOLD", "items": items, "times": [-1.0] * k + [0.05] + [999.0] * (2 - k)}


TRACKS = {"tense": ("../../../reels/audio/music/out-of-this-world.mp3", 30.0),
          "intrigue": ("../../../reels/audio/music/echoes.mp3", 20.0),
          "confident": ("../../../reels/audio/music/unforgiven.mp3", 70.0),
          "warm": ("../../../reels/audio/music/fifth-of-february.mp3", 30.0),
          "sad": ("../../../reels/audio/music/silent-descent.mp3", 20.0)}

P1 = [
    ("You know that feeling.", I("li-phone-waiting", (.55, .35), 1.3, drift=0.06), {"sfx": ["hook"], "music": "tense"}),
    ("You text someone, and the replies keep getting shorter. \"lol.\" \"nice.\" A thumbs up. Then nothing.",
     CHAT([["Hey! Saturday still on?", "me", 0.1], ["lol", "them", "@lol"], ["So are we going?", "me", "@nice-0.6"],
           ["nice", "them", "@nice"], ["\U0001F44D", "them", "@thumbs"], ["Hello?", "me", "@Then"]],
          title="Jake", status="Read 9:42 PM", status_at="@nothing"),
     {"captions": False, "sfx": [{"name": "pop", "at": "@lol"}, {"name": "pop", "at": "@nice"}, {"name": "pop", "at": "@thumbs"}, {"name": "heartbeat", "at": "@nothing"}]}),
    ("Plans that used to happen every weekend just... stop happening.", V("friends-dinner-5", 2.0, 1.1), {}),
    ("The group chat keeps going, but somehow without you.", I("li-groupchat", (.4, .5), 1.0, to=[.35, .4], to_zoom=1.5, drift=0), {}),
    ("Nobody's mad at you. There was no fight.", V("lonely-5", 3.0, 1.1), {}),
    ("People just slowly lose interest,", I("li-drift", (.55, .5), 1.0, drift=0.08), {}),
    ("and you're left wondering what you did wrong.", V("waiting-1", 2.0, 1.15), {}),
    ("And the worst part is, nobody will ever tell you.", M("NOBODY WILL", "EVER TELL YOU", times=[0.0, "@ever"]), {}),
    ("Nobody says, \"You talk about yourself too much,\"", I("li-dinner", (.5, .5), 1.1), {}),
    ("or \"You're always on your phone when we hang out.\"", I("li-cafe-phone", (.5, .5), 1.1), {}),
    ("They just quietly drift away,", I("li-leave", (.5, .5), 1.0, drift=0.06), {}),
    ("and you never get the chance to fix it.", V("sad-woman-0", 2.0), {}),
    ("So in this video, I'm going to tell you", V("texting-7", 2.0, 1.3), {}),
    ("what nobody will say to your face.", M("WHAT NOBODY", "WILL SAY TO", "YOUR FACE", times=[0.0, "@will", "@your"]), {}),
    ("Seven reasons people lose interest in you, backed by real psychology, and what to do about each one.",
     {"mg": "list", "headline": "7 REASONS THEY LOSE INTEREST", "n": 7, "stagger": 0.16},
     {"sfx": [{"name": "pop", "at": 0.3 + 0.16 * k} for k in range(7)]}),
    ("Some of them are going to sting.", I("li-mirror", (.4, .4), 1.3), {}),
    ("One of them, I was doing for years without noticing.", I("li-recording", (.5, .4), 1.2), {}),
    ("And the last one is the reason most people never figure any of this out.", I("li-empty", (.5, .5), 1.0, to_zoom=1.5, drift=0), {}),
    ("If you've ever felt forgotten by people you care about,", V("lonely-1", 3.0), {}),
    ("stay with me until the end.", V("texting-7", 7.0, 1.25), {}),
    ("I know this feeling well.", V("rain-window-1", 1.0), {"pause_before": 0.35, "in": "blur"}),
    ("A few years ago I had a friend I'll call Michael.", I("li-bench", (.5, .5), 1.1), {"overlays": [LT("MICHAEL", "Name changed", at="@Michael")]}),
    ("We talked every single day.", V("video-call-6", 2.0), {}),
    ("Texts, memes at 2 AM, plans every weekend.", V("group-of-friends-5", 1.0), {}),
    ("And then, slowly, it stopped.", I("li-drift", (.75, .4), 1.4), {}),
    ("No fight. No drama.", K("NO FIGHT.", ("NO DRAMA.", "yellow"), times=[0.0, "@drama"]), {}),
    ("His replies got shorter. \"Haha.\" \"Nice.\" Then a thumbs up. Then nothing.",
     CHAT([["Dinner this week?", "me", 0.1], ["Haha", "them", "@haha"], ["So... Thursday?", "me", "@nice-0.5"],
           ["Nice", "them", "@nice"], ["\U0001F44D", "them", "@thumbs"], ["Michael?", "me", "@nothing-0.3"]]),
     {"captions": False, "sfx": [{"name": "pop", "at": "@haha"}, {"name": "pop", "at": "@nice"}, {"name": "pop", "at": "@thumbs"}]}),
    ("I remember staring at the little \"Read 9:42 PM\" under my last message,",
     CHAT([["Dinner this week?", "me", -1.0], ["Haha", "them", -1.0], ["So... Thursday?", "me", -1.0],
           ["Nice", "them", -1.0], ["\U0001F44D", "them", -1.0], ["Michael?", "me", -1.0]], status="Read 9:42 PM", status_at="@read"),
     {"in": "cut", "captions": False, "sfx": [{"name": "heartbeat", "at": "@read"}, {"name": "heartbeat", "at": "@read+0.45"}]}),
    ("thinking: what did I do?", I("li-phone-waiting", (.55, .3), 1.8), {}),
    ("For a long time I told myself it was him.", V("waiting-4", 3.0), {}),
    ("Then it happened again, with someone else.", V("bar-friends-6", 2.0), {}),
    ("And that's when I had to admit something uncomfortable.", I("li-mirror", (.45, .45), 1.0), {}),
    ("When it keeps happening, the common factor is you.", I("li-mirror", (.45, .45), 1.05),
     {"punch": {"at": "@you", "zoom": 2.0, "focus": [.62, .45]}, "shake": ["@you"], "sfx": [{"name": "bass", "at": "@you", "gain": 0.7}]}),
    ("So I went looking for answers. Not the \"just be yourself\" kind.", I("li-research", (.5, .45), 1.0), {"music": "intrigue", "pause_before": 0.25}),
    ("Real research on why people drift away from us.", I("li-research", (.5, .4), 1.6), {}),
    ("And what I found changed the way I talk to people.", V("coffee-shop-4", 3.0), {}),
    ("Here's the first thing I had to accept.", M("THE FIRST THING", "I HAD TO ACCEPT", times=[0.0, "@had"]), {}),
    ("People don't lose interest in you all at once.", I("li-drift", (.5, .5), 1.0), {}),
    ("They lose it in tiny moments you don't even notice.", V("bored-5", 2.0), {}),
    ("A conversation where they leave feeling a little worse than when they arrived.", I("li-heavy", (.4, .5), 1.1), {}),
    ("Then another one.", V("bored-2", 3.0), {}),
    ("Nobody leaves a person. They leave a feeling.", Q("Nobody leaves a person. They leave a feeling.", end="@feeling"),
     {"sfx": [{"name": "reveal", "at": "@feeling"}]}),
    ("And honestly, I think most of us create that feeling", V("friends-dinner-2", 4.0), {}),
    ("without ever realising it.", I("li-cafe-phone", (.5, .5), 1.0, drift=-0.08), {}),
]

P2 = [
    ("Let's start with the most common one.", REASON("01", ["THE MOST", "COMMON ONE"]), {"chapter": True, "music": "intrigue"}),
    ("A sociologist called Charles Derber studied everyday conversations,", V("friends-dinner-5", 5.0),
     {"overlays": [LT("CHARLES DERBER", "Sociologist · The Pursuit of Attention (1979)")]}),
    ("at dinner tables, at work, between friends.", V("coffee-shop-4", 1.0), {}),
    ("He noticed that people constantly pull the conversation back to themselves.", I("li-dinner", (.5, .45), 1.0, to=[.5, .3], to_zoom=1.5, drift=0), {}),
    ("He called it conversational narcissism.", I("li-dinner", (.5, .45), 1.05), {"captions": False, "overlays": [TITLE("CONVERSATIONAL NARCISSISM", "@conversational")]}),
    ("And it's sneaky, because it doesn't look selfish. It looks like relating.",
     M("IT DOESN'T LOOK SELFISH", "IT LOOKS LIKE", "RELATING", times=[0.0, "@looks", "@relating"]), {}),
    ("Your friend says, \"I'm so tired, work has been crazy this week.\"",
     CHAT([["So tired. Work is crazy this week", "them", 0.3]], title="Sarah"), {"captions": False, "sfx": [{"name": "pop", "at": 0.3}]}),
    ("And you say, \"Tell me about it, my boss kept me until nine yesterday.\"",
     CHAT([["So tired. Work is crazy this week", "them", -1.0], ["Tell me about it!", "me", "@tell"], ["My boss kept me till 9 yesterday", "me", "@boss"]], title="Sarah"),
     {"in": "cut", "captions": False, "sfx": [{"name": "pop", "at": "@tell"}, {"name": "pop", "at": "@boss"}]}),
    ("You think you're connecting. You're showing you understand.", V("bar-friends-5", 3.0), {}),
    ("But what you actually did was take the spotlight.", I("li-mic", (.5, .5), 1.0),
     {"punch": {"at": "@spotlight", "zoom": 1.6, "focus": [.6, .45]}, "sfx": [{"name": "scratch", "at": "@spotlight"}]}),
    ("Derber called that a shift response.", VS(["SHIFT RESPONSE", "ME, ME, ME"], ["SUPPORT RESPONSE", "TELL ME MORE"], 999.0), {}),
    ("The other option is a support response: \"Crazy how? What happened?\"",
     VS(["SHIFT RESPONSE", "ME, ME, ME"], ["SUPPORT RESPONSE", "TELL ME MORE"], "@support", left_at=-1.0),
     {"in": "cut", "sfx": [{"name": "reveal", "at": "@support"}]}),
    ("That one keeps the spotlight on them.", I("li-listen", (.6, .5), 1.2), {}),
    ("When I first read about this,", I("li-research", (.5, .35), 1.3), {"pause_before": 0.25}),
    ("I recorded myself on a call with a friend, just to check.", I("li-recording", (.5, .45), 1.0), {}),
    ("Then I counted.", I("li-recording", (.62, .72), 2.0), {"sfx": [{"name": "typing", "at": 0.1, "gain": 0.5}]}),
    ("I pulled the conversation back to me eleven times in twenty minutes.",
     {"mg": "year", "from": 0, "to": 11, "roll": 2.4, "label": "TIMES IN 20 MINUTES"},
     {"sfx": [{"name": "tick", "at": 0.25 + 0.2 * k} for k in range(11)]}),
    ("Eleven.", K(("ELEVEN.", "red")), {"in": "cut", "shake": [0.05], "sfx": [{"name": "bass", "at": 0.0, "gain": 0.7}]}),
    ("I wanted to disappear.", I("li-empty", (.5, .55), 1.4), {}),
    ("And there's a reason this hurts more than you'd think.", V("sad-woman-1", 2.0), {}),
    ("In 2012, two Harvard neuroscientists, Diana Tamir and Jason Mitchell,", V("old:brain", 6.0, 1.15),
     {"overlays": [LT("TAMIR & MITCHELL", "Harvard University · PNAS (2012)")]}),
    ("scanned people's brains while they talked about themselves.", I("li-brain", (.49, .42), 1.0, drift=0.1), {}),
    ("The brain's reward system lit up, the same system that responds to food and money.", I("li-brain", (.49, .42), 1.1),
     {"punch": {"at": "@lit", "zoom": 1.8, "focus": [.49, .42]}, "sfx": [{"name": "sparkle", "at": "@lit"}]}),
    ("People were even willing to give up real money just to keep talking about themselves.",
     M("THEY GAVE UP", "REAL MONEY", "TO TALK ABOUT", "THEMSELVES", mark=["REAL MONEY"], times=[0.0, "@real", "@keep", "@themselves"]), {}),
    ("So when you take someone's turn to talk, you're not just being rude.", V("bored-5", 4.0), {}),
    ("You're taking away something their brain actually enjoys.", I("li-brain", (.49, .42), 1.0, drift=-0.1), {}),
    ("The fix sounds simple, but it takes practice.", M("THE FIX", times=[0.0]), {"music": "confident", "pause_before": 0.25}),
    ("When someone tells you something,", V("coffee-shop-1", 2.0), {}),
    ("ask one more question before you say anything about yourself.", I("li-listen", (.5, .5), 1.0, to=[.47, .3], to_zoom=1.6, drift=0), {}),
    ("Just one.", K(("JUST ONE.", "yellow")), {}),
    ("Researchers at Harvard found", V("bar-friends-5", 6.0), {"overlays": [LT("HUANG ET AL.", "Harvard Business School (2017)")]}),
    ("that people who ask follow-up questions are rated as more likeable.", V("coffee-shop-4", 8.0), {}),
    ("Not the people with the best stories.", I("li-dinner", (.5, .3), 1.6), {}),
    ("The people who ask the second question.", I("li-listen", (.5, .45), 1.2), {"sfx": [{"name": "sparkle", "at": "@second"}]}),
]

P3 = [
    ("Okay. The second thing, and there's a good chance you're doing it right now.", REASON("02", ["YOUR", "PHONE"], title_at="@right"),
     {"chapter": True, "music": "tense"}),
    ("Your phone.", V("texting-2", 2.0, 1.2), {"in": "glitch", "sfx": [{"name": "zap", "at": 0.05}]}),
    ("In 2012, two researchers in England, Andrew Przybylski and Netta Weinstein,", V("coffee-shop-4", 4.0),
     {"overlays": [LT("PRZYBYLSKI & WEINSTEIN", "University of Essex (2012)")]}),
    ("had pairs of strangers sit down and talk.", V("bar-friends-6", 1.0), {}),
    ("For some pairs, a phone was simply lying nearby.", I("li-phone-table", (.5, .4), 1.0, to_zoom=1.5, drift=0), {}),
    ("Not ringing. Not being used. Just there.", K("NOT RINGING.", "NOT BEING USED.", ("JUST THERE.", "yellow"), times=[0.0, "@being", "@just"]), {}),
    ("The pairs with the phone in view felt less close to each other and trusted each other less.",
     VS(["NO PHONE", "CLOSER"], ["PHONE IN VIEW", "LESS TRUST"], "@trusted"), {"sfx": [{"name": "wrong", "at": "@trusted", "gain": 0.4}]}),
    ("Just because a phone was on the table.", I("li-phone-table", (.5, .35), 2.0), {"sfx": [{"name": "glass", "at": 0.1}]}),
    ("I think this is the quietest relationship killer of our time.", Q("The quietest relationship killer of our time.", end="@time"), {}),
    ("Every time you glance at your screen in the middle of someone's sentence,", I("li-cafe-phone", (.4, .45), 1.0, to=[.4, .35], to_zoom=1.5, drift=0), {}),
    ("you send a tiny message: something else might be more interesting than you.",
     M("SOMETHING ELSE", "IS MORE", "INTERESTING", "THAN YOU", mark=["INTERESTING"], times=[0.0, "@more", "@interesting", "@than"]), {}),
    ("They won't say anything.", V("sad-woman-0", 4.0), {}),
    ("They'll just stop telling you the good stuff.", I("li-cafe-phone", (.75, .4), 1.7), {}),
    ("A friend once stopped in the middle of a story", V("coffee-shop-1", 4.0), {"pause_before": 0.25}),
    ("and said, \"Go on, reply to it, I'll wait.\"", Q("Go on, reply to it. I'll wait.", end="@wait"), {}),
    ("She was smiling.", V("coffee-shop-4", 6.0), {}),
    ("But she never finished that story, and I still don't know how it ended.", V("rain-window-1", 3.0), {}),
    ("So put it away.", K(("PUT IT AWAY.", "yellow")), {"music": "warm", "pause_before": 0.25}),
    ("Not face down on the table. Away.", I("li-phone-table", (.5, .45), 1.2), {"sfx": [{"name": "click", "at": "@away"}]}),
    ("In your pocket, in your bag.", I("li-pocket", (.5, .45), 1.0), {}),
    ("It's the cheapest way there is to make someone feel important.", V("bar-friends-5", 8.0), {"sfx": [{"name": "sparkle", "at": "@important"}]}),
]

P4 = [
    ("The third reason is harder to see,", REASON("03", ["BEING", "PREDICTABLE"], title_at=0.5), {"chapter": True, "music": "intrigue"}),
    ("because you can be a great listener and still lose people.", I("li-listen", (.5, .5), 1.0, drift=0.07), {}),
    ("It happens when you become completely predictable.", I("li-same-cafe", (.5, .45), 1.0),
     {"punch": {"at": "@predictable", "zoom": 1.5, "focus": [.62, .2]}, "sfx": [{"name": "tick", "at": "@predictable"}, {"name": "tick", "at": "@predictable+0.5"}]}),
    ("The psychologist Arthur Aron has a theory about why we're drawn to certain people.", V("group-of-friends-0", 3.0),
     {"overlays": [LT("ARTHUR ARON", "Psychologist · Stony Brook University")]}),
    ("He calls it self-expansion.", I("li-door-world", (.5, .5), 1.0), {"captions": False, "overlays": [TITLE("SELF-EXPANSION", "@self")]}),
    ("We like people who make our world bigger,", I("li-door-world", (.6, .45), 1.6), {}),
    ("who bring new ideas, new places and new experiences into our lives.", V("travel-adventure-0", 2.0), {}),
    ("And when someone stops doing that, the interest fades,", I("li-same-cafe", (.5, .5), 1.2, drift=-0.08), {}),
    ("even when nothing is wrong.", V("lonely-5", 8.0), {}),
    ("Aron and his colleagues tested this with married couples.", V("old:first-date-0", 3.0), {}),
    ("Some couples spent time each week doing new, exciting activities together.", I("li-coaster", (.5, .5), 1.0, to_zoom=1.4, drift=0), {}),
    ("Others did pleasant but familiar things.", V("bored-5", 6.0), {}),
    ("After ten weeks, the couples who tried new things were more satisfied with their relationship.",
     {"mg": "bars", "headline": "SATISFACTION AFTER 10 WEEKS", "values": False, "bars": [["FAMILIAR", 50, "grey"], ["NEW THINGS", 82, "yellow"]]},
     {"sfx": [{"name": "pop", "at": 0.2}, {"name": "pop", "at": 0.45}]}),
    ("I think this is why so many friendships die in the", V("bored-5", 1.0), {}),
    ("same-place, same-food, same-complaints loop.",
     M("SAME PLACE.", "SAME FOOD.", "SAME COMPLAINTS.", mark=["SAME COMPLAINTS."], times=["@sameplace", "@samefood", "@samecomplaints"]), {}),
    ("You meet at the same cafe,", V("coffee-shop-1", 6.0), {}),
    ("tell the same stories about the same people,", I("li-same-cafe", (.5, .45), 1.3), {}),
    ("and you both leave a little bored.", V("bored-2", 5.0), {}),
    ("Not of each other. Of the routine you've become together.", V("friends-dinner-2", 6.0), {}),
    ("The fix isn't to become a different person.", K(("THE FIX", "yellow")), {"music": "warm", "pause_before": 0.25}),
    ("It's to bring something new to the table.", I("li-book", (.5, .5), 1.0), {}),
    ("A book you're reading.", V("reading-book-4", 2.0), {}),
    ("A strange fact you learned.", I("li-brain", (.49, .42), 1.3), {"sfx": [{"name": "sparkle", "at": 0.1}]}),
    ("A plan you've never tried.", V("hiking-7", 3.0), {}),
    ("Ask, \"Have you ever wanted to try...?\"", Q("Have you ever wanted to try...?", end="@try"), {}),
    ("When new experiences happen with you,", V("rollercoaster-4", 3.0), {}),
    ("people start to connect that feeling of excitement with you.", I("li-coaster", (.5, .4), 1.3), {}),
]

P5 = [
    ("The fourth reason is one I see everywhere, especially in dating.", REASON("04", ["BEING TOO", "AVAILABLE"], title_at=0.5),
     {"chapter": True, "music": "confident"}),
    ("Being too available.", I("li-instant", (.45, .4), 1.2), {"punch": {"at": "@available", "zoom": 1.7, "focus": [.45, .3]}}),
    ("I'm not talking about playing games. I hate games.", K("NOT PLAYING GAMES.", ("I HATE GAMES.", "red"), times=[0.0, "@hate"]), {}),
    ("But there's a difference between being kind and being instantly, completely, always available.",
     M("BEING KIND", "VS.", "ALWAYS AVAILABLE", times=["@kind", "@instantly", "@always"]), {}),
    ("In 2011, researchers Erin Whitchurch, Timothy Wilson and Daniel Gilbert", V("texting-7", 4.0, 1.2),
     {"overlays": [LT("WHITCHURCH, WILSON & GILBERT", "Psychological Science (2011)")]}),
    ("showed women the profiles of men who had supposedly looked at their profile too.", I("li-wonder", (.5, .45), 1.0), {}),
    ("Some were told the men liked them a lot.", TOLD(0), {"sfx": [{"name": "pop", "at": 0.05}]}),
    ("Some were told the men liked them an average amount.", TOLD(1), {"in": "cut", "sfx": [{"name": "pop", "at": 0.05}]}),
    ("And some were told nobody knew how much the men liked them.", TOLD(2), {"in": "cut", "sfx": [{"name": "pop", "at": 0.05}]}),
    ("Guess which men they thought about most, and found most attractive?", I("li-wonder", (.5, .2), 1.8),
     {"sfx": [{"name": "riser", "at": "@attractive+0.5", "gain": 0.7}]}),
    ("The uncertain ones.", K(("THE UNCERTAIN ONES.", "yellow")), {"shake": [0.05], "sfx": [{"name": "bass", "at": 0.0, "gain": 0.7}]}),
    ("A little uncertainty keeps the mind busy.", I("li-wonder", (.5, .4), 1.3), {}),
    ("When everything is guaranteed, the brain stops paying attention.", V("bored-2", 6.0), {}),
    ("I learned this the embarrassing way.", I("li-instant", (.5, .45), 1.0), {"pause_before": 0.25}),
    ("I used to reply within seconds,", V("typing-phone-2", 2.0), {"sfx": [{"name": "typing", "at": 0.1, "gain": 0.6}]}),
    ("cancel my own plans the moment someone texted,", I("li-cancel", (.5, .5), 1.1), {}),
    ("and agree with everything.", I("li-instant", (.45, .27), 1.9), {}),
    ("I thought I was being a good friend.", V("waiting-4", 6.0), {}),
    ("In reality, I had no life of my own to bring into the friendship.", I("li-empty", (.5, .5), 1.2), {}),
    ("And people could feel it.", V("sad-woman-0", 6.0), {}),
    ("So have a life that doesn't revolve around anyone.", M("HAVE A LIFE", "THAT'S YOURS", times=[0.0, "@revolve"]), {}),
    ("Your own hobbies,", V("guitar-7", 2.0), {}),
    ("your own goals,", V("gym-workout-6", 2.0), {}),
    ("your own friends.", V("group-of-friends-5", 1.0), {}),
    ("Not to look busy. To actually be interesting.", I("li-guitar", (.4, .5), 1.1), {}),
    ("When you have somewhere to be, people want to know where you're going.", I("li-going-out", (.4, .5), 1.0, to=[.62, .6], to_zoom=1.5, drift=0), {}),
]

P6 = [
    ("The fifth reason is what you bring into the room emotionally.", REASON("05", ["YOUR", "ENERGY"], title_at=0.5),
     {"chapter": True, "music": "tense"}),
    ("Emotions are contagious.", I("li-raincloud", (.5, .45), 1.0), {}),
    ("Psychologists call it emotional contagion.", I("li-raincloud", (.5, .45), 1.1), {"captions": False, "overlays": [TITLE("EMOTIONAL CONTAGION", "@emotional")]}),
    ("Without realising it, we copy the expressions,", V("bar-friends-6", 4.0), {}),
    ("the tone and the mood of the people around us.", V("friends-dinner-5", 7.0), {}),
    ("So if every conversation with you starts with a complaint,", I("li-raincloud", (.5, .3), 1.8), {}),
    ("the other person walks away carrying a little of that weight.", I("li-heavy", (.35, .5), 1.3), {}),
    ("I'm not saying fake being happy.", K(("DON'T FAKE IT.", "white")), {}),
    ("Real friends should be able to share the heavy stuff,", V("old:hug-3", 2.0), {}),
    ("and if you're going through a hard time, talk about it.", V("sad-woman-1", 6.0), {}),
    ("But there's a difference between going through something and making negativity your personality.",
     VS(["GOING THROUGH", "SOMETHING"], ["NEGATIVITY AS YOUR", "PERSONALITY"], "@negativity"), {"sfx": [{"name": "wrong", "at": "@personality", "gain": 0.4}]}),
    ("If people have to brace themselves before they call you,", V("waiting-1", 6.0), {}),
    ("something needs to change.", I("li-mirror", (.45, .45), 1.2), {}),
    ("I had a phase where every catch-up started with what was wrong with my job.", I("li-raincloud", (.5, .5), 1.0), {"pause_before": 0.25}),
    ("One day a friend said, half joking, \"So what's the disaster this week?\"",
     CHAT([["So what's the disaster this week?", "them", "@disaster"]], title="Emma"), {"captions": False, "sfx": [{"name": "pop", "at": "@disaster"}]}),
    ("It was funny. It also hurt, because she was right.", V("lonely-1", 6.0), {}),
    ("Try this.", K(("TRY THIS.", "yellow")), {"music": "warm", "pause_before": 0.25}),
    ("Next time you meet someone, open with something good.", I("li-sunny", (.45, .45), 1.0), {}),
    ("Something small that made you laugh, something you're looking forward to.", V("bar-friends-5", 2.0), {}),
    ("It changes the temperature of the whole conversation.", I("li-sunny", (.6, .5), 1.4), {}),
    ("The sixth reason is about how conversations end, and almost nobody thinks about it.", REASON("06", ["HOW IT", "ENDS"], title_at=0.6),
     {"chapter": True, "music": "intrigue"}),
    ("The Nobel Prize-winning psychologist Daniel Kahneman", I("li-research", (.5, .45), 1.2),
     {"overlays": [LT("DANIEL KAHNEMAN", "Nobel Prize in Economics (2002)")]}),
    ("described something called the peak-end rule.", I("li-laugh", (.5, .45), 1.0), {"captions": False, "overlays": [TITLE("THE PEAK-END RULE", "@peakend")]}),
    ("When we remember an experience, we don't remember every minute of it.", V("group-of-friends-5", 2.0), {}),
    ("We mostly remember the most intense moment, and how it ended.",
     {"mg": "curve", "title": "WHAT WE REMEMBER", "draw": 2.0, "peak_at": "@intense", "end_at": "@ended"}, {}),
    ("That means the last few minutes of a conversation matter far more than you think.", I("li-laugh", (.5, .4), 1.1), {}),
    ("If you drag it out until there's nothing left to say,", I("li-watch", (.5, .5), 1.0), {}),
    ("until you're both checking the time,", V("wrist-watch-2", 3.0), {"sfx": [{"name": "tick", "at": 0.2}, {"name": "tick", "at": 0.7}]}),
    ("that awkward fade is what they remember.",
     {"mg": "curve", "title": "WHAT THEY REMEMBER", "draw": 1.2, "end_low": True, "peak_at": 0.6, "end_at": "@remember"}, {}),
    ("This is the one I changed first, and it worked almost immediately.", V("video-call-6", 6.0), {"music": "confident", "pause_before": 0.25}),
    ("I started leaving on a high.", M("LEAVE ON", "A HIGH", times=[0.0, "@high"]), {}),
    ("When we're laughing and the energy is good,", I("li-laugh", (.5, .45), 1.0), {}),
    ("that's when I say, \"I have to go, but this was great.\"", I("li-goodbye", (.5, .5), 1.0), {}),
    ("It feels rude at first. It isn't.", K("FEELS RUDE?", ("IT ISN'T.", "yellow"), times=[0.0, "@isn"]), {}),
    ("It makes them want the next conversation.", V("goodbye-0", 2.0), {}),
]

P7 = [
    ("And the last reason is the one nobody talks about. The one that fixed it for me.",
     REASON("07", ["THE ONE", "NOBODY", "TALKS ABOUT"], title_at=0.5), {"chapter": True, "music": "sad"}),
    ("Sometimes people lose interest in you because you lost interest in yourself.",
     Q("Sometimes people lose interest in you because you lost interest in yourself.", end="@yourself", width=30),
     {"sfx": [{"name": "boom", "at": "@yourself", "gain": 0.6}]}),
    ("When Michael drifted away, I was in the worst year of my life.", I("li-empty", (.5, .5), 1.0, to_zoom=1.4, drift=0), {}),
    ("I'd stopped going to the gym,", I("li-couch", (.2, .75), 1.8), {}),
    ("stopped reading,", I("li-couch", (.8, .72), 1.8), {"in": "cut"}),
    ("stopped doing anything that excited me.", I("li-couch", (.4, .45), 1.3), {"in": "cut"}),
    ("I wasn't growing, so I had nothing new to share.", V("lonely-5", 6.0), {}),
    ("I was just waiting for other people to make me feel better.", V("waiting-1", 4.0), {}),
    ("And when you hand that job to someone else,", I("li-burden", (.5, .5), 1.0, to_zoom=1.3, drift=0), {}),
    ("it slowly becomes a burden for them.", V("sad-woman-1", 9.0), {}),
    ("I genuinely believe this is the root of almost everything else in this video.",
     M("THE ROOT OF", "EVERYTHING", times=[0.0, "@everything"]), {"pause_before": 0.25}),
    ("When you feel empty, you talk about yourself because you need the validation.", I("li-dinner", (.5, .3), 1.5), {}),
    ("You check your phone because the moment isn't enough.", I("li-cafe-phone", (.4, .4), 1.4), {"in": "cut"}),
    ("You cling to people because you're scared of being alone.", I("li-burden", (.5, .4), 1.6), {"in": "cut"}),
    ("You complain because nothing feels like it's going right.", I("li-raincloud", (.5, .3), 1.5), {"in": "cut"}),
    ("And here's the part that gave me hope.", M("THE PART THAT", "GAVE ME HOPE", times=[0.0, "@gave"]), {"music": "warm", "pause_before": 0.3}),
    ("Research on what's called the liking gap, by Erica Boothby and her colleagues,", V("bar-friends-5", 4.0),
     {"overlays": [LT("BOOTHBY, COONEY, SANDSTROM & CLARK", "Psychological Science (2018)")]}),
    ("found that after a conversation, people consistently underestimate how much the other person liked them.",
     VS(["WHAT YOU THINK", "A LITTLE"], ["WHAT THEY FELT", "A LOT"], "@liked"), {"sfx": [{"name": "reveal", "at": "@liked"}]}),
    ("So part of the problem isn't even real.", K("IT'S NOT", ("EVEN REAL.", "yellow"), times=[0.0, "@real"]), {}),
    ("We walk away convinced we were boring,", I("li-goodbye", (.5, .5), 1.2), {}),
    ("when the other person actually enjoyed it.", V("goodbye-0", 6.0), {}),
    ("So here's what I want you to take from this.", V("old:sunrise-4", 2.0), {"pause_before": 0.25}),
    ("You don't need to become a different person to keep people interested.", I("li-mirror", (.45, .45), 1.0), {}),
    ("You need to come back to yourself.", I("li-grow", (.5, .5), 1.0, to_zoom=1.4, drift=0), {"sfx": [{"name": "sparkle", "at": "@yourself"}]}),
    ("Listen more than you talk, and ask that second question.", FIX(0), {"sfx": [{"name": "pop", "at": 0.05}]}),
    ("Put your phone away.", FIX(1), {"in": "cut", "sfx": [{"name": "pop", "at": 0.05}]}),
    ("Bring something new into people's lives.", FIX(2), {"in": "cut", "sfx": [{"name": "pop", "at": 0.05}]}),
    ("Have a life of your own.", FIX(3), {"in": "cut", "sfx": [{"name": "pop", "at": 0.05}]}),
    ("Bring a little lightness into the room.", FIX(4), {"in": "cut", "sfx": [{"name": "pop", "at": 0.05}]}),
    ("Leave while it's good.", FIX(5), {"in": "cut", "sfx": [{"name": "pop", "at": 0.05}]}),
    ("And keep growing, so you always have something to share.", FIX(6), {"in": "cut", "sfx": [{"name": "sparkle", "at": 0.05}]}),
    ("As for Michael, we're talking again.", I("li-bench", (.5, .5), 1.0), {"pause_before": 0.3}),
    ("It took two years,", V("group-of-friends-0", 6.0), {}),
    ("and it started with me asking him a question and actually listening to the answer.", I("li-bench", (.42, .42), 1.5, drift=0.06), {}),
    ("People don't lose interest in you because you're not enough.", V("hiking-7", 5.0), {}),
    ("They lose interest when you stop showing up as yourself.", I("li-grow", (.5, .4), 1.5), {}),
    ("So show up.", M("SHOW UP.", times=[0.0]), {"shake": [0.05], "sfx": [{"name": "bass", "at": 0.0, "gain": 0.6}]}),
    ("And if this video made you think of someone you've drifted away from,", I("li-drift", (.5, .5), 1.0), {"pause_before": 0.3}),
    ("maybe send them a message today.", I("li-text", (.55, .45), 1.0, to_zoom=1.4, drift=0), {}),
    ("You never know who's been waiting for it.",
     CHAT([["Hey! Been thinking about you. Coffee this week?", "me", 0.1], ["Yes!! I'd love that", "them", "@waiting"]]),
     {"captions": False, "sfx": [{"name": "pop", "at": 0.1}, {"name": "sparkle", "at": "@waiting"}]}),
]

PARTS = [P1, P2, P3, P4, P5, P6, P7]
CHIPS = [None, "REASON 1 / 7", "REASON 2 / 7", "REASON 3 / 7", "REASON 4 / 7", "REASONS 5 & 6 / 7", "REASON 7 / 7"]
SFX_FOR = {"whip": "swoosh-fast", "zoom": "sweep", "slide": "swoosh", "blur": "tunnel", "glitch": "glitch-hit"}


def kind(v):
    return "img" if "img" in v else "video" if "video" in v else "mg"


def auto(shots):
    """Transitions for this video: slide up into graphics, zoom out of them, blur from image to video,
    hard cuts between clips; each transition with its own sound."""
    out, prev = [], None
    for sh in shots:
        sh = dict(sh)
        k = kind(sh["v"])
        if sh.pop("chapter", False):
            sh.setdefault("in", "dip")
            sh["sfx"] = [{"name": "trailer", "at": 0.0, "gain": 0.7}] + sh.get("sfx", [])
        if "in" not in sh and prev:
            sh["in"] = "slide" if k == "mg" and prev != "mg" else "zoom" if prev == "mg" else \
                "blur" if (prev, k) == ("img", "video") else "whip" if (prev, k) == ("video", "img") else "cut"
        if sh.get("in") in SFX_FOR:
            sh["sfx"] = [{"name": SFX_FOR[sh["in"]], "gain": 0.6}] + sh.get("sfx", [])
        v = sh["v"]
        if k == "mg" and v["mg"] not in ("year",):
            sh.setdefault("captions", False)
        for ov in sh.get("overlays", []):
            if ov["mg"] == "title":
                sh["sfx"] = sh.get("sfx", []) + [{"name": "reveal", "at": ov["at"]}, {"name": "impact", "at": ov["at"], "gain": 0.6}]
            if ov["mg"] == "lower_third":
                sh["sfx"] = sh.get("sfx", []) + [{"name": "swoosh-fast", "at": ov["at"], "gain": 0.5}]
        if v.get("mg") == "reason":
            sh["sfx"] = sh.get("sfx", []) + [{"name": "boom", "at": v["title_at"], "gain": 0.6}]
        out.append(sh)
        prev = k
    return out


def words(s):
    return [re.sub(r"[^a-z0-9']", "", w.lower()) for w in s.split()]


def main():
    (HERE / "parts").mkdir(exist_ok=True)
    total_shots = 0
    for n, part in enumerate(PARTS, 1):
        want = words((HERE / "parts" / f"p{n}.txt").read_text())
        got = [w for text, _, _ in part for w in words(text)]
        if want != got:
            i = next(i for i, (a, b) in enumerate(zip(want + ["<end>"], got + ["<end>"])) if a != b)
            raise SystemExit(f"part {n}: shot text differs from the script at word {i}: script {want[i:i + 6]} vs shots {got[i:i + 6]}")
        shots = auto([{"text": t, "v": v, **ex} for t, v, ex in part])
        cues = []
        for i, sh in enumerate(shots):
            m = sh.pop("music", None)
            if m:
                cues.append({"shot": i, "music": TRACKS[m][0], **({"start": TRACKS[m][1]} if m not in [c["m"] for c in cues] else {}), "m": m})
        for c in cues:
            c.pop("m")
        if cues[0]["shot"] != 0:
            raise SystemExit(f"part {n}: first shot needs a music cue")
        last = n == len(PARTS)
        spec = {"out": f"../../output/lose-interest/part{n}.mp4", "audio": f"p{n}.wav", "speed": 1.0,
                "tail": 2.0 if last else 0.45, "music_fade": 2.0 if last else 0.5, "music_cues": cues, "music_volume": 0.34,
                **({"fade_out": 2.0} if last else {}),
                "style": {"grade": "warm", "captions": "pill", "caption_y": 0.85, "vignette": 0.3, "grain": 3,
                          **({"chip": {"text": CHIPS[n - 1], "from": 3.0}} if CHIPS[n - 1] else {})},
                "shots": shots}
        (HERE / "parts" / f"part{n}.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False))
        kinds = [kind(s["v"]) for s in shots]
        print(f"part {n}: {len(shots)} shots ({kinds.count('img')} AI, {kinds.count('video')} stock, {kinds.count('mg')} graphics), {len(cues)} music cues")
        total_shots += len(shots)
    print("total shots", total_shots)


if __name__ == "__main__":
    main()
