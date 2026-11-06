"""Build parts/partN.json for "Why You Can't Focus Anymore".

Editing style (the 6th look): teal/orange "teal" grade on stock, UPPERCASE "highlight" captions (spoken word on a
yellow box), pixelate transitions into graphics, RGB-split punches on twists, push cuts from stock to images,
progress bar, and screen-themed graphics: browser tabs piling up, attention-span countdown, attention battery,
phone-distance rooms, urge wave, 25-minute timer, notification banners.
Usage: python3 build.py   (after the first render, long image/stock shots are re-split from Whisper timings)
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent


def I(n, f=(.5, .5), z=1.1, **kw):
    return {"img": f"../img/f-{n}.jpg", "focus": list(f), "zoom": z, **kw}


def V(n, st=1.0, z=1.08, **kw):
    return {"video": f"../stock/{n}.mp4", "start": st, "zoom": z, **kw}


def K(*lines, times=None, **kw):
    lines = [[l, "white"] if isinstance(l, str) else list(l) for l in lines]
    return {"mg": "kinetic", "lines": lines, "times": times or [0.0] * len(lines), **kw}


def M(*lines, mark=None, times=None, **kw):
    return {"mg": "marker", "lines": list(lines), "mark": mark or [lines[-1]], "times": times or [0.0] * len(lines), **kw}


def Q(text, end=None, width=26):
    return {"mg": "quote", "text": text, **({"end": end} if end else {}), "width": width}


def VS(left, right, at, left_at=0.0):
    return {"mg": "versus", "left": left, "right": right, "at": at, "left_at": left_at}


def TABS(tabs, times):
    return {"mg": "tabs", "tabs": tabs, "times": times}


def LT(title, sub, at=0.1):
    return {"mg": "lower_third", "title": title, "sub": sub, "at": at}


def NOTE(title, text, at=0.1):
    return {"mg": "notify", "title": title, "text": text, "at": at}


def TITLE(text, at, y=0.78):
    return {"mg": "title", "text": text, "at": at, "y": y, "size": 96}


TRACKS = {"sad": ("../../../reels/audio/music/silent-descent.mp3", 50.0),
          "intrigue": ("../../../reels/audio/music/echoes.mp3", 140.0),
          "tense": ("../../../reels/audio/music/out-of-this-world.mp3", 80.0),
          "warm": ("../../../reels/audio/music/fifth-of-february.mp3", 20.0),
          "confident": ("../../../reels/audio/music/unforgiven.mp3", 90.0)}

P1 = [
    ("You sit down to do one thing. Just one.", I("one-thing", (.55, .5), 1.0, to=[.5, .55], to_zoom=1.35, drift=0), {"sfx": ["hook"], "music": "intrigue"}),
    ("Maybe it's a report, maybe it's a book you've been meaning to finish,", V("man-laptop-office-2", 1.0), {}),
    ("maybe it's just answering one email.", V("typing-keyboard-7", 1.0), {}),
    ("And then you check your phone.", V("smartphone-hand-0", 1.0, z=1.15), {"sfx": [{"name": "pop", "at": "@phone"}], "overlays": [NOTE("Messages", "you up? 👀", at="@phone")]}),
    ("Just for a second.", I("self-interrupt", (.5, .35), 1.2, to_zoom=1.5, drift=0), {}),
    ("Forty minutes later, you have eleven tabs open,", TABS(["Inbox (3)", "Weather", "News", "Video", "Shop", "Video 2", "Recipe", "Wiki", "Map", "Reddit", "Video 3"],
                                                            [0.1, 0.4, 0.7, 0.95, 1.15, 1.35, 1.5, 1.65, 1.8, 1.9, "@eleven"]), {"sfx": [{"name": "click", "at": t, "gain": 0.4} for t in (0.1, 0.7, 1.15, 1.5, 1.8)] + [{"name": "impact", "at": "@eleven", "gain": 0.6}]}),
    ("you've watched half of three different videos,", V("phone-screen-scrolling-2", 1.0), {}),
    ("you've read the first paragraph of an article you don't even care about,", I("tabs-chaos", (.6, .5), 1.0, to=[.65, .45], to_zoom=1.4, drift=0), {}),
    ("and the one thing you sat down to do?", I("one-thing", (.55, .45), 1.4), {"music_fx": "muffle"}),
    ("Still not done.", K(("STILL NOT DONE.", "red")), {"sfx": [{"name": "bass", "gain": 0.7}]}),
    ("You read the same page of a book three times", V("reading-book-6", 1.0), {}),
    ("and still can't say what it was about.", I("book-reread", (.45, .4), 1.0, to_zoom=1.5, drift=0), {}),
    ("You start a movie and pick up your phone before the opening credits are over.", I("movie-phone", (.4, .45), 1.0, to=[.35, .4], to_zoom=1.4, drift=0), {}),
    ("Even this video.", K("EVEN", ("THIS VIDEO.", "yellow"), times=[0.0, "@this"]), {"in": "rgb"}),
    ("Be honest.", I("reach-empty", (.4, .4), 1.5), {"punch": {"at": "@honest", "zoom": 1.9, "focus": [.38, .3]}}),
    ("Some part of you is already wondering if there's something better to watch.", V("woman-using-phone-6", 1.0), {}),
    ("And the worst part isn't that it happens.", I("tired-morning", (.5, .4), 1.1), {"music": "sad"}),
    ("It's that you remember a time when it didn't.", I("old-reading", (.5, .55), 1.0, to_zoom=1.3, drift=0), {}),
    ("When you could read for an hour.", V("reading-book-1", 1.0), {}),
    ("When you could sit through a whole movie.", I("movie-phone", (.7, .3), 1.3), {}),
    ("When your mind just stayed.", I("stay", (.5, .55), 1.0, drift=0.07), {"voice_fx": {"at": "@stayed", "fx": "echo"}}),
    ("So what happened to you?", K("SO WHAT", ("HAPPENED?", "yellow"), times=[0.0, "@happened"]), {"in": "pixel"}),
    ("Here's the good news first. You're not lazy. You're not broken.", M("NOT LAZY.", "NOT BROKEN.", mark=["NOT LAZY.", "NOT BROKEN."], times=["@lazy", "@broken"]), {"music": "intrigue"}),
    ("And no, you probably don't have a goldfish brain.", I("goldfish", (.6, .45), 1.0, to=[.62, .45], to_zoom=1.5, drift=0), {"sfx": [{"name": "pop", "at": "@goldfish"}]}),
    ("That famous line about humans having an eight-second attention span, shorter than a goldfish?",
     VS(["HUMANS", "8 SEC"], ["GOLDFISH", "9 SEC"], "@shorter"), {}),
    ("Nobody has ever found the study behind it.", K("NO STUDY.", ("JUST A MYTH.", "red"), times=[0.0, "@behind"]), {"in": "rgb", "sfx": [{"name": "glitch-hit", "at": "@behind", "gain": 0.5}]}),
    ("What's really going on is more interesting than that.", I("switching", (.5, .4), 1.0, to_zoom=1.3, drift=0), {}),
    ("And a lot more fixable.", I("forty-pages", (.55, .4), 1.2), {"sfx": [{"name": "sparkle", "at": "@fixable"}]}),
    ("But the thing most people try first,", V("man-laptop-office-4", 1.0), {"in": "rgb"}),
    ("forcing themselves to focus harder,", I("force-focus", (.5, .35), 1.0, to_zoom=1.4, drift=0), {"shake": ["@harder"]}),
    ("is exactly the thing that makes it worse.", K("MAKES IT", ("WORSE.", "red"), times=[0.0, "@worse"]), {"sfx": [{"name": "boom", "at": "@worse", "gain": 0.5}]}),
    ("Stay with me, because by the end of this video,", I("stay", (.5, .45), 1.25), {}),
    ("you'll know why, and what to do instead.", K("WHY.", ("WHAT TO DO.", "yellow"), times=[0.0, "@what"]), {}),
]

P2 = [
    ("A couple of years ago, I noticed I couldn't read anymore.", V("reading-book-2", 1.0), {"music": "sad"}),
    ("Not properly.", I("book-reread", (.45, .4), 1.5), {}),
    ("I'd get two pages into a book and my hand would just reach for my phone.", I("hand-reflex", (.55, .5), 1.0, to=[.62, .55], to_zoom=1.6, drift=0), {}),
    ("I didn't decide to do it.", V("woman-using-phone-5", 1.0), {}),
    ("It just happened, like a reflex.", I("hand-reflex", (.66, .55), 1.8), {"sfx": [{"name": "click", "at": "@reflex"}]}),
    ("At first I thought I was just tired.", I("tired-morning", (.5, .35), 1.3), {}),
    ("Then I thought maybe something was wrong with me.", V("man-staring-window-0", 1.0), {}),
    ("And then I found the work of a researcher called Gloria Mark.", I("stopwatch", (.6, .45), 1.0, drift=0.06),
     {"music": "tense", "pause_before": 0.25, "overlays": [LT("GLORIA MARK", "UC Irvine · attention research", at="@Gloria")]}),
    ("She's spent around twenty years at the University of California, Irvine,", V("man-laptop-office-5", 1.0), {}),
    ("watching how people really use their screens at work.", V("typing-keyboard-0", 1.0), {}),
    ("Not asking them. Watching,", I("stopwatch", (.68, .4), 1.6), {}),
    ("first with a stopwatch and later with software.", V("stopwatch-1", 1.0), {"sfx": [{"name": "tick", "at": "@stopwatch"}]}),
    ("In 2004, people stayed on one screen for about two and a half minutes before switching to something else.",
     {"mg": "countdown", "title": "TIME ON ONE SCREEN", "steps": [[2004, 150, ""]], "times": [0.0]}, {"sfx": [{"name": "tick", "at": "@two"}]}),
    ("By 2012, it was about seventy-five seconds.", V("stopwatch-4", 1.0, z=1.15), {"overlays": [TITLE("2012: 75 SEC", "@seventy", y=0.15)]}),
    ("In her more recent studies, it's around forty-seven seconds.",
     {"mg": "countdown", "title": "TIME ON ONE SCREEN", "steps": [[2004, 150, ""], [2012, 75, ""], ["TODAY", 47, ""]], "times": [-1.0, -0.6, "@around"]},
     {"sfx": [{"name": "impact", "at": "@forty", "gain": 0.6}]}),
    ("Forty-seven seconds.", K(("47 SECONDS.", "yellow")), {"sfx": [{"name": "bass", "gain": 0.7}], "in": "pixel"}),
    ("That's how long the average person stays on one thing before jumping.", I("switching", (.5, .4), 1.2, to_zoom=1.5, drift=0), {"shake": ["@jumping"]}),
    ("And here's what got me.", I("self-interrupt", (.5, .35), 1.3), {"music_fx": "muffle"}),
    ("A lot of those switches weren't caused by a notification.", V("phone-on-desk-6", 1.0), {"overlays": [NOTE("Notifications", "No new notifications", at=0.3)]}),
    ("Nobody interrupted them.", K("NOBODY", ("INTERRUPTED", "white"), times=[0.0, "@interrupted"]), {}),
    ("They interrupted themselves.", K("THEY INTERRUPTED", ("THEMSELVES.", "yellow"), times=[0.0, "@themselves"]), {"in": "rgb", "sfx": [{"name": "bass", "at": "@themselves", "gain": 0.6}]}),
    ("Think about that for a second.", I("daydream", (.5, .4), 1.1), {}),
    ("You open your email, nothing new.", V("smartphone-hand-4", 1.0), {"sfx": [{"name": "click", "at": "@nothing"}]}),
    ("You check the news, nothing new.", V("woman-using-phone-0", 1.0), {"sfx": [{"name": "click", "at": "@nothing"}]}),
    ("You open the same app you closed thirty seconds ago. Nothing new.", I("reward-spark", (.5, .4), 1.0, to_zoom=1.4, drift=0), {"sfx": [{"name": "click", "at": "@Nothing"}]}),
    ("And you do it again anyway.", I("juggler", (.5, .45), 1.1, drift=0.06), {}),
    ("That's the first thing you need to understand.", K("#1", ("IT'S TRAINED", "yellow"), times=[0.0, "@understand"]), {"music": "intrigue", "pause_before": 0.25}),
    ("Your attention isn't broken. It's trained.", VS(["NOT", "BROKEN"], ["JUST", "TRAINED"], "@trained"), {}),
    ("Every time you switch, your brain gets a tiny reward.", I("reward-spark", (.45, .35), 1.5), {"sfx": [{"name": "sparkle", "at": "@reward"}]}),
    ("Something new. Something different.", V("smartphone-hand-6", 1.0), {}),
    ("A little hit of \"what's this?\"", I("reward-spark", (.42, .3), 1.9), {"punch": {"at": "@this", "zoom": 2.2, "focus": [.42, .3]}}),
    ("And anything you repeat thousands of times a day becomes a habit.", M("THOUSANDS OF TIMES", "= A HABIT", mark=["= A HABIT"], times=[0.0, "@habit"]), {}),
    ("You've been practising switching for years.", I("juggler", (.5, .35), 1.4), {}),
    ("You're really, really good at it.", I("switching", (.5, .3), 1.5), {}),
    ("You just never practised staying.", K("YOU NEVER PRACTISED", ("STAYING.", "yellow"), times=[0.0, "@staying"]), {"voice_fx": {"at": "@staying", "fx": "echo"}}),
]

P3 = [
    ("The second thing surprised me even more.", K("#2", ("THE PHONE YOU DON'T TOUCH", "yellow"), times=[0.0, "@surprised"]), {"music": "tense"}),
    ("You'd think the fix is simple.", I("guard-duty", (.5, .45), 1.0, drift=0.06), {}),
    ("Turn notifications off, put the phone face down, done.", V("phone-notification-0", 1.0), {"sfx": [{"name": "click", "at": "@off"}, {"name": "click", "at": "@down"}]}),
    ("It isn't.", K(("IT ISN'T.", "red")), {"in": "rgb", "sfx": [{"name": "glitch-hit", "gain": 0.5}]}),
    ("In 2017, a team led by Adrian Ward at the University of Texas", V("students-exam-4", 1.0), {"overlays": [LT("WARD ET AL. (2017)", "University of Texas · 'Brain Drain'", at="@Adrian")]}),
    ("ran an experiment with around eight hundred people.", {"mg": "grid", "rows": 4, "cols": 12, "h": 110, "cy": 0.45, "lit": [0, 48, 0.1, 1.6], "label": "AROUND 800 PEOPLE"}, {}),
    ("They gave them tests that needed real concentration.", V("students-exam-5", 1.0), {}),
    ("Some people had their phone on the desk, face down. Some had it in their bag or pocket. And some left it in another room.",
     {"mg": "rooms", "title": "WHERE WAS THE PHONE?", "cols": [["ON THE DESK", 55], ["BAG / POCKET", 70], ["ANOTHER ROOM", 88]], "times": [0.0, "@bag", "@another"], "unit": ""},
     {"sfx": [{"name": "pop", "at": 0.1}, {"name": "pop", "at": "@bag"}, {"name": "pop", "at": "@another"}]}),
    ("The phones were silent. Nobody checked them.", V("phone-on-desk-6", 3.0, z=1.2), {}),
    ("And still, the people with the phone in another room", I("one-tab", (.5, .45), 1.0, drift=0.06), {"music_fx": "muffle"}),
    ("did noticeably better than the people with it on the desk.",
     {"mg": "bars", "headline": "CONCENTRATION", "bars": [["ANOTHER ROOM", 88, "yellow"], ["ON THE DESK", 55, "grey"]], "values": False}, {"sfx": [{"name": "bass", "gain": 0.6}]}),
    ("Just having it close was enough to drain them.", {"mg": "battery", "start": 100, "end": 35, "label": "BRAIN POWER", "at": "@close"}, {"in": "pixel"}),
    ("Think about what that means.", I("guard-duty", (.55, .3), 1.4), {}),
    ("Part of your brain is always on guard duty.", I("guard-duty", (.6, .15), 1.0, to=[.6, .2], to_zoom=1.7, drift=0), {"sfx": [{"name": "zap", "at": "@guard", "gain": 0.4}]}),
    ("Is it buzzing? Did someone reply? Am I missing something?", K("BUZZING?", "REPLY?", ("MISSING SOMETHING?", "yellow"), times=[0.0, "@reply", "@missing"]), {}),
    ("You're not using your phone,", V("man-laptop-office-5", 2.0), {}),
    ("but you're still spending attention on not using it.", {"mg": "battery", "start": 60, "end": 20, "label": "ATTENTION", "at": 0.2}, {}),
    ("It's like trying to work with someone standing behind you,", I("shoulder-tap", (.5, .45), 1.0, drift=0.06), {}),
    ("tapping your shoulder every few seconds.", I("shoulder-tap", (.62, .35), 1.7), {"sfx": [{"name": "tick", "at": "@tapping"}, {"name": "tick", "at": "@shoulder"}, {"name": "tick", "at": "@seconds"}]}),
    ("Except that someone lives in your pocket.", V("smartphone-hand-0", 3.0, z=1.25), {"in": "rgb"}),
    ("And it gets worse when you're stuck.", I("stuck-hard", (.5, .4), 1.0, to_zoom=1.4, drift=0), {}),
    ("The moment the work gets hard, that little voice in your head says, just check.", I("stuck-hard", (.55, .7), 1.6), {"overlays": [NOTE("Your brain", "just check 👀", at="@just")]}),
    ("And the phone is right there to say yes.", V("woman-using-phone-6", 2.0), {}),
    ("I tested this on myself.", I("next-step", (.5, .4), 1.1), {"music": "warm", "pause_before": 0.25}),
    ("Same desk, same work.", V("writing-notebook-5", 1.0), {}),
    ("One week with the phone face down on the desk,", I("guard-duty", (.6, .6), 1.2), {}),
    ("one week with the phone in the kitchen.", V("kitchen-counter-0", 1.0), {}),
    ("The second week, I finished more before lunch than I used to finish all day.", I("lunch-done", (.5, .45), 1.0, to=[.55, .3], to_zoom=1.4, drift=0), {"sfx": [{"name": "reveal", "at": "@lunch"}]}),
]

P4 = [
    ("The third reason is the one nobody wants to hear.", K("#3", ("NO BOREDOM", "yellow"), times=[0.0, "@nobody"]), {"music": "intrigue"}),
    ("You've forgotten how to be bored.", I("itch", (.55, .5), 1.0, to_zoom=1.4, drift=0), {}),
    ("Think about the last time you just waited.", I("coffee-line", (.45, .6), 1.0, drift=0.06), {}),
    ("In a line,", I("coffee-line", (.45, .65), 1.6), {}),
    ("at a red light,", I("red-light", (.6, .55), 1.1), {}),
    ("in the two minutes before a meeting starts.", V("man-laptop-office-2", 3.0), {}),
    ("No phone. No podcast. Just you and your thoughts.", K("NO PHONE.", "NO PODCAST.", ("JUST YOU.", "yellow"), times=[0.0, "@podcast", "@just"]), {}),
    ("For most people, it's been years.", I("daydream", (.5, .5), 1.0, to_zoom=1.3, drift=0), {}),
    ("Every empty second now gets filled.", {"mg": "battery", "start": 0, "end": 100, "label": "EVERY SECOND FILLED", "at": 0.2}, {"in": "pixel"}),
    ("Waiting for coffee, scroll.", V("coffee-shop-6", 1.0), {"sfx": [{"name": "swoosh-fast", "at": "@scroll", "gain": 0.5}]}),
    ("Ad comes on, scroll.", V("smartphone-hand-4", 2.0), {"sfx": [{"name": "swoosh-fast", "at": "@scroll", "gain": 0.5}]}),
    ("Brushing your teeth, podcast.", V("brushing-teeth-2", 1.0), {}),
    ("Even in the bathroom, we bring a screen.", I("bathroom", (.4, .35), 1.0, to_zoom=1.4, drift=0), {}),
    ("I used to think that was efficient. Why waste two minutes?", V("traffic-night-6", 1.0), {"music": "sad"}),
    ("But those two minutes were never wasted.", K("NEVER", ("WASTED.", "yellow"), times=[0.0, "@wasted"]), {"in": "rgb"}),
    ("That's where your mind used to wander, plan, daydream, and come up with ideas.", I("daydream", (.5, .3), 1.0, to=[.45, .2], to_zoom=1.6, drift=0), {"sfx": [{"name": "sparkle", "at": "@ideas"}]}),
    ("And we've handed every single one of them to an app.", V("bed-phone-dark-0", 2.0), {}),
    ("And that sounds harmless. But here's the problem.", I("boring-start", (.5, .45), 1.1), {"music": "tense"}),
    ("Deep focus always starts with a boring bit.", M("DEEP FOCUS", "STARTS BORING", mark=["STARTS BORING"], times=[0.0, "@boring"]), {}),
    ("The first few pages of a book.", V("reading-book-6", 3.0), {}),
    ("The first ten minutes of real work.", V("writing-notebook-1", 1.0), {}),
    ("That slow, slightly uncomfortable stretch before you get into it.", I("boring-start", (.5, .4), 1.6), {}),
    ("If your brain has learned that any boring moment gets rescued within seconds,", I("rescued", (.55, .5), 1.0, to=[.6, .45], to_zoom=1.3, drift=0), {}),
    ("it will never sit through that stretch.", I("itch", (.55, .45), 1.5), {}),
    ("The second things slow down, it starts looking for the exit.", I("exit-door", (.55, .55), 1.0, to=[.7, .5], to_zoom=1.5, drift=0), {}),
    ("And it always finds one, because the exit is in your pocket.", V("smartphone-hand-6", 2.0), {"in": "rgb", "sfx": [{"name": "bass", "at": "@pocket", "gain": 0.6}]}),
    ("My friend Jake said something that stuck with me.", I("jake", (.5, .45), 1.0, drift=0.06), {"music": "warm", "pause_before": 0.25, "overlays": [LT("JAKE", "My friend", at="@Jake")]}),
    ("He said, \"I don't get distracted. I get rescued from being bored, and I never asked to be rescued.\"",
     Q("\"I don't get distracted. I get rescued from being bored, and I never asked to be rescued.\"", end="@asked", width=30), {}),
]

P5 = [
    ("The fourth thing is how we rest.", K("#4", ("FAKE REST", "yellow"), times=[0.0, "@rest"]), {"music": "intrigue"}),
    ("Or rather, how we think we rest.", I("break-scroll", (.55, .4), 1.0, drift=0.06), {}),
    ("You work for twenty minutes, you feel tired, so you take a break.", V("man-laptop-office-4", 2.0), {}),
    ("And what does the break look like?", I("break-scroll", (.55, .3), 1.5), {"music_fx": "muffle"}),
    ("Your phone. Videos, news, messages.", K("VIDEOS.", "NEWS.", ("MESSAGES.", "yellow"), times=[0.0, "@news", "@messages"]), {"sfx": [{"name": "pop", "at": "@news"}, {"name": "pop", "at": "@messages"}]}),
    ("But that's not a break for your brain. That's more input.", {"mg": "battery", "start": 70, "end": 25, "label": "NOT A BREAK", "at": 0.3}, {"in": "pixel"}),
    ("Faster, louder, more colourful than the work you just left.", V("traffic-night-6", 3.0, rate=1.0), {}),
    ("So when you go back, the work feels even slower and even more boring than before.", I("boring-start", (.5, .45), 1.0, to_zoom=1.4, drift=0), {}),
    ("You've just made the contrast worse.", VS(["THE PHONE", "LOUD"], ["THE WORK", "DULL"], "@contrast"), {}),
    ("It's like taking a break from running by sprinting.", I("sprint", (.5, .5), 1.0, to_zoom=1.3, drift=0), {"sfx": [{"name": "whoosh", "at": "@sprinting"}]}),
    ("And then there's the night.", V("traffic-night-5", 1.0), {"music": "sad", "pause_before": 0.25}),
    ("You get into bed, you're exhausted, and you scroll for an hour anyway.", I("bed-scroll", (.55, .5), 1.0, to=[.6, .45], to_zoom=1.5, drift=0), {}),
    ("Not because it's fun.", V("woman-using-phone-5", 2.0), {}),
    ("Because it's the first moment all day that feels like yours, and you don't want to give it up.", V("bed-phone-dark-0", 4.0), {}),
    ("People call it revenge bedtime procrastination.", K("REVENGE BEDTIME", ("PROCRASTINATION", "yellow"), times=[0.0, "@procrastination"]), {"sfx": [{"name": "reveal", "at": "@procrastination"}]}),
    ("But you pay for it the next morning, because a tired brain is a distracted brain.", I("tired-morning", (.5, .4), 1.0, to_zoom=1.4, drift=0), {}),
    ("Everything in this video gets harder on five hours of sleep.", {"mg": "battery", "start": 40, "end": 8, "label": "5 HOURS OF SLEEP", "at": 0.2}, {}),
    ("And there's one more thing that makes all of this worse.", V("man-staring-window-0", 2.0), {"music": "tense", "in": "rgb"}),
    ("Sometimes you can't focus because you don't know what you're supposed to do next.", I("fog", (.5, .6), 1.0, to=[.5, .75], to_zoom=1.6, drift=0), {}),
    ("\"Work on the project\" isn't a task. It's a fog.", VS(["NOT A", "TASK"], ["IT'S A", "FOG"], "@fog"), {}),
    ("And when your brain looks into a fog, it doesn't want to go in.", V("fog-forest-4", 1.0), {}),
    ("It wants something clear and easy.", V("walking-park-2", 4.0), {}),
    ("And what's always clear and easy? The next video.", V("smartphone-hand-4", 3.0, z=1.2), {"sfx": [{"name": "pop", "at": "@next"}]}),
    ("A lot of what feels like a focus problem is really a clarity problem.", M("NOT A FOCUS PROBLEM", "A CLARITY PROBLEM", mark=["A CLARITY PROBLEM"], times=[0.0, "@clarity"]), {"sfx": [{"name": "impact", "at": "@clarity", "gain": 0.6}]}),
]

P6 = [
    ("So what do you actually do?", K("SO WHAT DO YOU", ("ACTUALLY DO?", "yellow"), times=[0.0, "@actually"]), {"music": "warm"}),
    ("The first thing is the easiest, and it works better than any app.", I("phone-away", (.5, .5), 1.0, drift=0.06), {"overlays": [TITLE("FIX #1", 0.1, y=0.08)]}),
    ("Put your phone in another room.", K("PHONE IN", ("ANOTHER ROOM.", "yellow"), times=[0.0, "@another"]), {"sfx": [{"name": "bass", "at": "@another", "gain": 0.6}]}),
    ("Not face down.", V("phone-notification-0", 2.0), {}),
    ("Not in a drawer next to you.", I("guard-duty", (.6, .6), 1.3), {}),
    ("Another room.", I("phone-away", (.3, .55), 1.5), {}),
    ("Remember the study. Distance is the whole point.", {"mg": "rooms", "title": "DISTANCE IS THE POINT", "cols": [["DESK", 55], ["POCKET", 70], ["ANOTHER ROOM", 88]], "times": [0.0, 0.2, 0.4], "unit": ""}, {"in": "pixel"}),
    ("If you're waiting for something urgent, turn the ringer on and you'll hear it.", V("kitchen-counter-0", 3.0), {}),
    ("The second thing is to train boredom on purpose.", I("coffee-window", (.45, .45), 1.0, drift=0.06), {"overlays": [TITLE("FIX #2", 0.1, y=0.08)]}),
    ("Start small. Ten minutes a day where you do nothing.", {"mg": "timer", "seconds": 600, "label": "DO NOTHING", "end_label": "DONE"}, {"in": "pixel"}),
    ("A walk without headphones.", V("walking-park-2", 1.0), {}),
    ("Waiting in line without your phone.", I("coffee-line", (.45, .55), 1.3), {}),
    ("Sitting with your coffee and just drinking it.", I("coffee-window", (.45, .45), 1.4, to_zoom=1.7, drift=0), {}),
    ("It will feel strange. You'll feel the itch.", I("itch", (.55, .5), 1.0, to=[.52, .55], to_zoom=1.5, drift=0), {}),
    ("That itch is the whole point.", K("THE ITCH", ("IS THE POINT.", "yellow"), times=[0.0, "@point"]), {}),
    ("Every time you sit through it, you're teaching your brain that a slow moment isn't an emergency.", I("walk-park", (.5, .55), 1.0, to_zoom=1.3, drift=0), {}),
    ("The third thing is to clear the fog before you start.", I("fog", (.5, .7), 1.5), {"overlays": [TITLE("FIX #3", 0.1, y=0.08)]}),
    ("Before you sit down, write the very next physical step.", I("next-step", (.55, .5), 1.0, to=[.6, .6], to_zoom=1.6, drift=0), {}),
    ("Not \"write the report\".", V("writing-notebook-1", 2.0), {}),
    ("Something like \"open the document and write three bullet points for the introduction\".",
     {"mg": "checklist", "title": "NEXT STEP", "items": ["OPEN THE DOCUMENT", "WRITE 3 BULLET POINTS", "FOR THE INTRODUCTION"], "times": ["@open", "@three", "@introduction"]}, {"in": "pixel"}),
    ("Small enough that your brain can't argue with it.", I("next-step", (.5, .4), 1.3), {}),
    ("The fourth thing is to stop trying to focus forever.", I("force-focus", (.5, .4), 1.2), {"overlays": [TITLE("FIX #4", 0.1, y=0.08)]}),
    ("Pick twenty-five minutes. Just twenty-five.", {"mg": "timer", "seconds": 1500, "label": "ONE ROUND", "end_label": "BREAK"}, {"in": "pixel", "sfx": [{"name": "tick", "at": 0.3}]}),
    ("Close every tab except the one you need.", I("one-tab", (.55, .45), 1.0, to=[.6, .45], to_zoom=1.4, drift=0), {"sfx": [{"name": "click", "at": "@close"}]}),
    ("And when the time is up, take a real break.", V("stopwatch-4", 1.0), {"sfx": [{"name": "correct", "at": "@up", "gain": 0.6}]}),
    ("Stand up, look out a window, get some water.", I("window-water", (.55, .45), 1.0, drift=0.06), {}),
    ("Anything but a screen.", K("ANYTHING BUT", ("A SCREEN.", "yellow"), times=[0.0, "@screen"]), {}),
    ("And if twenty-five minutes feels impossible right now, start with ten.", V("man-laptop-office-2", 4.0), {}),
    ("That's fine. You're not trying to become a monk.", I("count-ten", (.5, .45), 1.1), {"sfx": [{"name": "pop", "at": "@monk"}]}),
    ("You're trying to win one small round today, and another one tomorrow.", M("ONE ROUND TODAY.", "ONE TOMORROW.", mark=["ONE ROUND TODAY.", "ONE TOMORROW."], times=[0.0, "@another"]), {}),
]

P7 = [
    ("And the last one is my favourite.", I("count-ten", (.5, .3), 1.3, drift=0.06), {"music": "intrigue", "overlays": [TITLE("FIX #5", 0.1, y=0.08)]}),
    ("When the urge to check your phone hits, and it will,", V("smartphone-hand-6", 1.0), {"overlays": [NOTE("Your brain", "check it. now.", at="@hits")]}),
    ("don't fight it, and don't follow it. Just notice it.", VS(["DON'T FIGHT.", "DON'T FOLLOW."], ["JUST", "NOTICE"], "@notice"), {}),
    ("Say to yourself, \"There's the urge.\"", Q("\"There's the urge.\"", width=26), {}),
    ("Then count slowly to ten.", I("count-ten", (.55, .4), 1.5), {"sfx": [{"name": "tick", "at": "@ten"}]}),
    ("Most of the time, by the time you get to ten, it's gone.", {"mg": "wave", "label": "THE URGE"}, {"in": "pixel"}),
    ("An urge is like a wave.", V("ocean-wave-7", 1.0), {"sfx": [{"name": "whoosh", "at": "@wave"}]}),
    ("It rises, it peaks, and it falls on its own, if you don't feed it.", I("surf", (.5, .55), 1.0, to=[.5, .6], to_zoom=1.4, drift=0), {}),
    ("Remember what I said at the beginning?", I("force-focus", (.5, .4), 1.1), {"music_fx": "muffle", "overlays": [{"mg": "tag", "text": "◀◀ 01:27", "at": 0.1}]}),
    ("Most people try to force themselves to focus harder.", I("force-focus", (.5, .3), 1.5), {"shake": ["@harder"]}),
    ("That's why it doesn't work.", K("THAT'S WHY", ("IT FAILS.", "red"), times=[0.0, "@work"]), {"in": "rgb", "sfx": [{"name": "bass", "gain": 0.6}]}),
    ("You can't beat a habit with willpower alone.", VS(["WILLPOWER", "ALONE"], ["CHANGE", "WHAT'S AROUND"], "@alone"), {}),
    ("You beat it by changing what's around you, and practising the opposite.", I("one-tab", (.5, .45), 1.0, to_zoom=1.3, drift=0), {"music": "warm"}),
    ("When I started doing this, the first week was honestly uncomfortable.", I("itch", (.55, .5), 1.2), {}),
    ("I felt restless.", V("woman-using-phone-5", 3.0), {}),
    ("I kept reaching for a phone that wasn't there.", I("reach-empty", (.45, .45), 1.0, to=[.5, .45], to_zoom=1.4, drift=0), {}),
    ("But around the second week, something changed.", I("stay", (.5, .45), 1.1), {"in": "rgb"}),
    ("I read forty pages in one sitting for the first time in years.", I("forty-pages", (.55, .45), 1.0, to=[.5, .35], to_zoom=1.4, drift=0), {"sfx": [{"name": "reveal", "at": "@forty"}]}),
    ("It wasn't magic. My phone was still there. The apps were still there.", V("phone-on-desk-6", 2.0), {}),
    ("I just stopped letting them decide where my attention went every forty-seven seconds.", K("NOT EVERY", ("47 SECONDS.", "yellow"), times=[0.0, "@forty"]), {}),
    ("Your focus isn't gone. It's just out of practice.", M("NOT GONE.", "OUT OF PRACTICE.", mark=["OUT OF PRACTICE."], times=[0.0, "@practice"]), {"music": "confident", "pause_before": 0.25}),
    ("And like anything out of practice, it comes back faster than you think.", V("running-track-4", 1.0), {}),
    ("So the next time you sit down to do one thing,", I("one-thing", (.55, .5), 1.0, drift=0.06), {}),
    ("and you feel your hand reaching for your phone, remember.", I("hand-reflex", (.62, .55), 1.5), {}),
    ("You're not lazy, and you're not broken.", M("NOT LAZY.", "NOT BROKEN.", mark=["NOT LAZY.", "NOT BROKEN."], times=["@lazy", "@broken"]), {}),
    ("You just learned to switch.", I("switching", (.5, .45), 1.1), {}),
    ("And you can learn to stay.", I("stay", (.5, .5), 1.0, to_zoom=1.25, drift=0), {"voice_fx": {"at": "@stay", "fx": "echo"}, "sfx": [{"name": "sparkle", "at": "@stay"}]}),
    ("If this hit home, send it to the friend who watches videos with eleven tabs open.", K("SEND THIS TO", ("THE 11-TABS FRIEND", "yellow"), times=[0.0, "@friend"]), {"in": "pixel"}),
    ("And if you made it to the end of this video without checking your phone,", I("old-reading", (.5, .5), 1.1), {}),
    ("honestly, that's already a start. I'll see you in the next one.", V("walking-park-6", 1.0), {}),
]

PARTS = [P1, P2, P3, P4, P5, P6, P7]
SFX_FOR = {"pixel": "glitch-hit", "rgb": "zap", "push": "swoosh", "zoom": "sweep", "flash": "swoosh-fast", "dip": "whoosh"}


def kind(v):
    return "img" if "img" in v else "video" if "video" in v else "mg"


def auto(shots):
    """Transition grammar for this video: pixelate into graphics, push from stock into images, flash out of
    graphics, cuts otherwise; explicit "in" (rgb on twists) wins."""
    out, prev = [], None
    for sh in shots:
        sh = dict(sh)
        k = kind(sh["v"])
        if "in" not in sh and prev:
            sh["in"] = "pixel" if k == "mg" and prev != "mg" else "flash" if prev == "mg" and k != "mg" else \
                "push" if (prev, k) == ("video", "img") else "cut"
        if sh.get("in") in SFX_FOR:
            sh["sfx"] = [{"name": SFX_FOR[sh["in"]], "gain": 0.45}] + sh.get("sfx", [])
        v = sh["v"]
        if k == "mg":
            sh.setdefault("captions", False)
        for ov in sh.get("overlays", []):
            if ov["mg"] == "title":
                sh["sfx"] = sh.get("sfx", []) + [{"name": "impact", "at": ov["at"], "gain": 0.5}]
            if ov["mg"] == "lower_third":
                sh["sfx"] = sh.get("sfx", []) + [{"name": "swoosh-fast", "at": ov["at"], "gain": 0.5}]
            if ov["mg"] == "notify":
                sh["sfx"] = sh.get("sfx", []) + [{"name": "pop", "at": ov["at"], "gain": 0.6}]
        out.append(sh)
        prev = k
    return out


def words(s):
    return [re.sub(r"[^a-z0-9']", "", w.lower()) for w in s.split()]


def split_long(shots, n, limit=4.6):
    """Recut image/stock shots longer than `limit` s (from the last render's Whisper words) at the phrase break
    nearest the middle; the second half punches in on the same picture (zooms out if already tight)."""
    wj = HERE.parent / "output" / "focus" / f"part{n}_work" / "whisper.json"
    if not wj.exists():
        return shots
    ws_t = [w["start"] for w in json.loads(wj.read_text())["words"]]
    counts = [len(words(sh["text"])) for sh in shots]
    scale = len(ws_t) / sum(counts)
    starts, c = [], 0
    for k in counts:
        starts.append(ws_t[min(len(ws_t) - 1, round(c * scale))])
        c += k
    ends = starts[1:] + [ws_t[-1] + 0.6]
    out = []
    for sh, b, e in zip(shots, starts, ends):
        d, k = e - b, kind(sh["v"])
        ws = sh["text"].split()
        if d <= limit or k == "mg" or len(ws) < 6 or sh.get("punch"):
            out.append(sh)
            continue
        mid = len(ws) / 2
        cand = [i for i in range(2, len(ws) - 2) if ws[i - 1][-1] in ",.?!;:"] or list(range(2, len(ws) - 2))
        cut = min(cand, key=lambda i: abs(i - mid) - (0.6 if ws[i - 1][-1] in ",.?!;:" else 0))
        first, second = " ".join(ws[:cut]), " ".join(ws[cut:])
        tail = set(words(second))
        a = dict(sh, text=first)
        b2 = {"text": second, "in": "cut", "sfx": [{"name": "swoosh-fast", "gain": 0.3}]}
        for key in ("sfx", "overlays", "shake"):
            items = sh.get(key, [])
            mv = [x for x in items if isinstance(x.get("at") if isinstance(x, dict) else x, str)
                  and re.sub(r"[+\-][\d.]+$", "", (x["at"] if isinstance(x, dict) else x))[1:].lower() in tail]
            if items:
                a[key] = [x for x in items if x not in mv]
            if mv:
                b2[key] = b2.get(key, []) + mv
        if "voice_fx" in sh and sh["voice_fx"]["at"][1:].lower() in tail:
            b2["voice_fx"] = a.pop("voice_fx")
        v = dict(sh["v"])
        if k == "img":
            v.pop("to", None), v.pop("to_zoom", None), v.pop("drift", None)
            z = v.get("zoom", 1.1)
            v["zoom"] = round(z / 1.3, 2) if z >= 1.45 else round(min(1.6, z * 1.25), 2)
        else:
            v.update(start=round(v.get("start", 1.0) + d * cut / len(ws), 2), zoom=round(v.get("zoom", 1.08) * 1.15, 2))
        b2["v"] = v
        out += [a, b2]
    return out


def main():
    total = 0
    for n, part in enumerate(PARTS, 1):
        want = words((HERE / "parts" / f"p{n}.txt").read_text())
        got = [w for t, _, _ in part for w in words(t)]
        if want != got:
            i = next(i for i, (a, b) in enumerate(zip(want + ["<end>"], got + ["<end>"])) if a != b)
            raise SystemExit(f"part {n}: shot text differs at word {i}: script {want[i:i + 6]} vs shots {got[i:i + 6]}")
        shots = split_long(auto([{"text": t, "v": v, **ex} for t, v, ex in part]), n)
        cues, used = [], set()
        for i, sh in enumerate(shots):
            m = sh.pop("music", None)
            if m:
                cues.append({"shot": i, "music": TRACKS[m][0], **({"start": TRACKS[m][1]} if m not in used else {})})
                used.add(m)
        if not cues or cues[0]["shot"] != 0:
            raise SystemExit(f"part {n}: first shot needs a music cue")
        last = n == len(PARTS)
        spec = {"out": f"../../output/focus/part{n}.mp4", "audio": f"p{n}.wav", "speed": 1.0,
                "tail": 2.0 if last else 0.45, "music_fade": 2.0 if last else 0.5, "music_cues": cues, "music_volume": 0.32,
                **({"fade_out": 2.0} if last else {}), "progress": True,
                "style": {"grade": "teal", "captions": "highlight", "caption_y": 0.86, "vignette": 0.4, "grain": 5},
                "shots": shots}
        (HERE / "parts" / f"part{n}.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False))
        kinds = [kind(s["v"]) for s in shots]
        print(f"part {n}: {len(shots)} shots ({kinds.count('img')} AI, {kinds.count('video')} stock, {kinds.count('mg')} graphics)")
        total += len(shots)
    print("total", total)


if __name__ == "__main__":
    main()
