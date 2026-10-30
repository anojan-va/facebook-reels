"""Build parts/partN.json for "Why You Can't Stop Thinking About Someone".

Editing style for this video (the 4th look, different from the other three): cold night-blue grade on stock (it's a
2 AM video), lowercase captions with a yellow underline, "spin" and "blur" transitions, an open-loop spinner, a
restaurant receipt that gets a PAID stamp, a craving countdown timer, highlighter text and quote cards for the
punch lines, chat screens for the phone moments, no chapter numbers (the user asked for continuous storytelling).
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


def CHAT(messages, title="Lena", status=None, status_at=None):
    return {"mg": "chat", "messages": messages, "title": title, **({"status": status, "status_at": status_at} if status else {})}


def VS(left, right, at, left_at=0.0):
    return {"mg": "versus", "left": left, "right": right, "at": at, "left_at": left_at}


def NOTE(text, at=0.1, title="Lena", dur=None):
    return {"mg": "notify", "title": title, "text": text, "at": at, **({"dur": dur} if dur else {})}


def TITLE(text, at, y=0.78):
    return {"mg": "title", "text": text, "at": at, "y": y, "size": 120}


def LT(title, sub, at=0.1):
    return {"mg": "lower_third", "title": title, "sub": sub, "at": at}


def TAG(text, at=0.0):
    return {"mg": "tag", "text": text, "at": at, "pos": [0.04, 0.08]}


TRACKS = {"sad": ("../../../reels/audio/music/silent-descent.mp3", 30.0),
          "intrigue": ("../../../reels/audio/music/echoes.mp3", 100.0),
          "tense": ("../../../reels/audio/music/out-of-this-world.mp3", 40.0),
          "warm": ("../../../reels/audio/music/fifth-of-february.mp3", 10.0),
          "confident": ("../../../reels/audio/music/unforgiven.mp3", 40.0)}

P1 = [
    ("It's 2 AM.", {"mg": "year", "from": 0, "to": 2, "roll": 0.5, "label": "AM"}, {"sfx": ["hook"], "music": "sad", "captions": False}),
    ("You should be asleep.", V("insomnia-2", 1.0, 1.1), {}),
    ("But you're lying there, replaying the same conversation for the fortieth time.", I("c-2am", (.45, .45), 1.0, to=[.4, .2], to_zoom=1.6, drift=0),
     {"overlays": [TAG("◀◀ REPLAY  x40", "@replaying")], "sfx": [{"name": "rewind", "at": "@replaying", "gain": 0.6}]}),
    ("What they said. What you should have said.", K("WHAT THEY SAID.", ("WHAT YOU SHOULD", "yellow"), ("HAVE SAID.", "yellow"), times=[0.0, "@should", "@should"], size=140), {}),
    ("The way they looked at you that one time.", V("sad-woman-0", 3.0), {}),
    ("You've told yourself a hundred times to stop thinking about them.", I("c-crazy", (.5, .4), 1.0, to_zoom=1.4, drift=0), {}),
    ("And somehow, telling yourself to stop just makes it louder.", M("TELLING YOURSELF TO STOP", "MAKES IT", "LOUDER", times=[0.0, "@makes", "@louder"]),
     {"shake": ["@louder"], "sfx": [{"name": "boom", "at": "@louder", "gain": 0.6}]}),
    ("You check their profile.", V("night-bed-phone-1", 2.0, 1.15), {}),
    ("You don't even want to. Your thumb just does it.", I("c-thumb", (.6, .55), 1.0), {"punch": {"at": "@thumb", "zoom": 1.8, "focus": [.65, .6]}}),
    ("You read old messages you already know by heart.",
     CHAT([["haha you're ridiculous \U0001F602", "them", -1.0], ["Same time tomorrow?", "me", -1.0], ["obviously \U0001F60A", "them", -1.0]], title="Lena"), {}),
    ("And part of you feels a little bit crazy.", V("night-bed-phone-5", 2.0, 1.15), {}),
    ("Because it's been weeks. Maybe months.", {"mg": "timer", "seconds": 5400, "label": "WEEKS. MONTHS.", "end_label": "STILL HERE"}, {}),
    ("Why is this one person still living in your head?", I("c-loop", (.5, .45), 1.0, spin=-6), {"sfx": [{"name": "heartbeat", "at": "@living"}]}),
    ("Here's what I want you to know before we go any further.", V("rain-4", 1.0), {"pause_before": 0.25, "music": "intrigue"}),
    ("You're not crazy. You're not weak.", K("YOU'RE NOT CRAZY.", ("YOU'RE NOT WEAK.", "yellow"), times=[0.0, "@weak-0.4"]), {}),
    ("Your brain is doing exactly what it was built to do.", I("c-brain-crave", (.35, .5), 1.0, to_zoom=1.4, drift=0), {}),
    ("And once you understand why, you can finally start to turn the volume down.", I("c-volume", (.5, .45), 1.0), {}),
    ("I'm going to show you how I did it,", V("walking-park-0", 1.0), {}),
    ("including the one mistake that kept me stuck for almost a year.", M("THE ONE MISTAKE", "THAT KEPT ME STUCK", "FOR A YEAR", mark=["THE ONE MISTAKE"], times=[0.0, "@kept", "@almost"]), {}),
    ("Stay with me, because the last part is the one that actually set me free.", V("sunrise-1", 2.0), {}),
    ("A few years ago, there was someone I'll call Lena.", I("c-latenight", (.55, .5), 1.0), {"in": "blur", "pause_before": 0.35, "music": "sad"}),
    ("We were never even officially together. That's the embarrassing part.", V("sad-woman-0", 2.0), {}),
    ("Three months of late-night talks, inside jokes, almost-dates.",
     CHAT([["you up?", "them", 0.1], ["always \U0001F602", "me", "@late"], ["ok that joke again \U0001F480", "them", "@inside"], ["coffee saturday?", "me", "@almost"]]),
     {"sfx": [{"name": "pop", "at": 0.1}, {"name": "pop", "at": "@late"}, {"name": "pop", "at": "@inside"}, {"name": "pop", "at": "@almost"}]}),
    ("And then one day she just... stopped.", CHAT([["coffee saturday?", "me", -1.0], ["hey?", "me", 0.3]], status="Read 11:04 PM", status_at="@stopped"),
     {"in": "cut", "sfx": [{"name": "heartbeat", "at": "@stopped"}]}),
    ("No fight. No explanation.", K("NO FIGHT.", ("NO EXPLANATION.", "yellow"), times=[0.0, "@no+0.4"]), {}),
    ("She started seeing someone else, and that was it.", I("c-she-leaves", (.55, .5), 1.0), {}),
    ("And I couldn't let it go.", M("I COULDN'T", "LET IT GO", times=[0.0, "@let"]), {}),
    ("I'd be at work, in the middle of a meeting,", V("office-meeting-7", 1.0), {}),
    ("and suddenly I was thinking about something she said in August.", I("c-meeting", (.6, .3), 1.4), {}),
    ("I'd hear a song in a supermarket and my whole day was gone.", V("supermarket-1", 2.0), {}),
    ("My friends were patient for about two weeks.", V("friends-talking-5", 3.0), {}),
    ("Then they started giving me that look. You know the one.", I("c-friends-look", (.5, .45), 1.0, to=[.7, .4], to_zoom=1.5, drift=0), {}),
    ("\"Are we really talking about her again?\"", Q("\"Are we really talking about her again?\"", end="@again"), {}),
    ("What made it worse was that I didn't understand it.", I("c-shame", (.5, .5), 1.0), {"pause_before": 0.25}),
    ("If we'd been together for five years, sure, that would make sense.", VS(["5 YEARS", "MAKES SENSE"], ["3 MONTHS", "???"], 999.0, left_at="@five"), {}),
    ("But three months? I felt pathetic.", VS(["5 YEARS", "MAKES SENSE"], ["3 MONTHS", "???"], "@three", left_at=-1.0), {"in": "cut"}),
    ("And that shame made me think about her even more.", I("c-shame", (.5, .45), 1.4), {}),
    ("It took me a long time to understand what was actually going on.", V("rain-4", 6.0), {}),
    ("And the first piece of the puzzle was something I learned almost by accident.", I("c-puzzle", (.6, .5), 1.0, to_zoom=1.4, drift=0), {"sfx": [{"name": "reveal", "at": "@puzzle"}]}),
]

P2 = [
    ("There's an old idea in psychology called the Zeigarnik effect.", {"mg": "loop", "text": "OPEN LOOP", "labels": ["what if", "why", "one more time"]},
     {"music": "intrigue", "captions": False, "overlays": [TITLE("THE ZEIGARNIK EFFECT", "@zeigarnik", y=0.86)]}),
    ("Back in the 1920s, a psychologist named Bluma Zeigarnik", V("restaurant-order-0", 1.0), {"overlays": [LT("BLUMA ZEIGARNIK", "Psychologist, Berlin (1927)")]}),
    ("noticed that waiters could remember every detail of an order that hadn't been paid yet.", I("c-waiter", (.6, .4), 1.0, to=[.6, .25], to_zoom=1.5, drift=0), {}),
    ("But the moment the bill was settled, the order vanished from their memory.", {"mg": "receipt", "paid_at": "@settled"},
     {"sfx": [{"name": "bass", "at": "@settled", "gain": 0.6}]}),
    ("Our minds hold on to things that are unfinished. Open loops.", {"mg": "loop", "text": "UNFINISHED", "labels": []}, {}),
    ("It's the same reason a song you only hear half of gets stuck in your head all day.", V("song-headphones-2", 2.0), {}),
    ("And when I read that, I almost laughed.", V("walking-park-0", 3.0), {"pause_before": 0.25}),
    ("Because that was exactly it.", K(("THAT WAS IT.", "yellow")), {}),
    ("Lena wasn't stuck in my head because she was the love of my life.", I("c-latenight", (.65, .45), 1.6), {}),
    ("She was stuck because the story never ended.", Q("She was stuck because the story never ended.", end="@ended"), {}),
    ("There was no last conversation. No explanation. No goodbye.", K("NO LAST CONVERSATION.", "NO EXPLANATION.", ("NO GOODBYE.", "yellow"), times=[0.0, "@explanation", "@goodbye"]), {}),
    ("My brain was like that waiter, standing there holding an unpaid bill,", I("c-unpaid", (.4, .4), 1.1, to_zoom=1.5, drift=0), {}),
    ("refusing to let go until someone settled it.", {"mg": "receipt", "status": "UNPAID", "paid_at": 999.0}, {}),
    ("I really believe this is why the \"almost\" relationships hurt the most.", M("WHY \"ALMOST\"", "HURTS THE MOST", times=[0.0, "@hurt"]), {}),
    ("The situationships. The person who disappeared. The one you never got to say everything to.", V("sad-woman-6", 2.0), {}),
    ("It's not that they mattered more.", V("rain-4", 4.0), {}),
    ("It's that the ending never happened, so your mind keeps trying to write it.", I("c-rewrite", (.5, .45), 1.0), {}),
    ("Over and over, every night, a different version.", I("c-rewrite", (.75, .7), 1.8), {"sfx": [{"name": "typing", "at": 0.1, "gain": 0.5}]}),
    ("What if I'd said this. What if she'd said that.", K("WHAT IF I'D SAID THIS.", "WHAT IF SHE'D SAID THAT.", times=[0.0, "@she'd"]), {}),
    ("Your brain isn't remembering. It's trying to finish.", VS(["NOT", "REMEMBERING"], ["IT'S", "FINISHING"], "@finish"), {"sfx": [{"name": "reveal", "at": "@finish"}]}),
]

P3 = [
    ("And here's the second piece. The one that really changed how I saw myself.", I("c-puzzle", (.65, .5), 1.4), {"music": "tense"}),
    ("The anthropologist Helen Fisher did something fascinating.", V("night-bed-phone-4", 2.0), {"overlays": [LT("HELEN FISHER", "Anthropologist · Rutgers University")]}),
    ("She put people who had just been rejected in love into a brain scanner,", I("c-scanner", (.5, .55), 1.0, to_zoom=1.4, drift=0), {}),
    ("and showed them a photo of the person who left them.", I("c-scanner", (.74, .2), 2.0), {"sfx": [{"name": "shutter", "at": "@photo"}]}),
    ("And the areas that lit up were the same reward and craving areas you see in addiction.", I("c-brain-crave", (.35, .5), 1.0),
     {"punch": {"at": "@reward", "zoom": 1.9, "focus": [.25, .5]}, "sfx": [{"name": "zap", "at": "@reward"}]}),
    ("The same system involved in craving a drug.", M("THE SAME SYSTEM", "AS A", "DRUG", mark=["DRUG"], times=[0.0, "@craving", "@drug"]), {}),
    ("So that 2 AM feeling?", I("c-2am", (.5, .5), 1.2), {}),
    ("That pull to check their profile one more time?", I("c-hook", (.4, .45), 1.0, to=[.6, .3], to_zoom=1.4, drift=0), {}),
    ("That's not you being weak. That's withdrawal.", VS(["NOT", "WEAKNESS"], ["IT'S", "WITHDRAWAL"], "@withdrawal"), {"sfx": [{"name": "boom", "at": "@withdrawal", "gain": 0.6}]}),
    ("Your brain got used to a reward, the texts, the attention, the excitement,", CHAT([["good morning ☀️", "them", 0.1], ["you're the best \U0001F60A", "them", "@attention"], ["call me later?", "them", "@excitement"]]),
     {"sfx": [{"name": "pop", "at": 0.1}, {"name": "pop", "at": "@attention"}, {"name": "pop", "at": "@excitement"}]}),
    ("and now it's craving it like anything else it's hooked on.", I("c-hook", (.5, .45), 1.2), {}),
    ("When I understood this, I stopped hating myself.", V("sunrise-1", 4.0), {"pause_before": 0.3, "music": "warm"}),
    ("I remember sitting on my kitchen floor at midnight, holding my phone,", I("c-kitchen-floor", (.6, .5), 1.0, to_zoom=1.3, drift=0), {}),
    ("about to send her another \"Hey, how have you been?\"", CHAT([["Hey, how have you been?", "me", 0.6]]), {"sfx": [{"name": "typing", "at": 0.1, "gain": 0.6}]}),
    ("And for the first time, instead of thinking \"I'm so pathetic,\"", I("c-kitchen-floor", (.58, .4), 1.5), {}),
    ("I thought, \"Oh. This is a craving. It'll pass in ten minutes.\"", {"mg": "timer", "seconds": 600, "label": "THE CRAVING", "end_label": "PASSED"}, {}),
    ("And it did.", K(("AND IT DID.", "yellow")), {"sfx": [{"name": "sparkle", "at": 0.1}]}),
    ("I put the phone down, made some tea,", I("c-tea", (.55, .55), 1.1), {}),
    ("and the wave went past.", I("c-wave", (.5, .55), 1.0, drift=-0.1), {}),
    ("That was the first time I felt like I had any control at all.", V("tea-1", 2.0), {}),
]

P4 = [
    ("But understanding it is only half of it.", K("UNDERSTANDING IT", ("IS ONLY HALF", "yellow"), times=[0.0, "@only"]), {"music": "intrigue"}),
    ("You also need to know what keeps it going.", V("scrolling-phone-7", 2.0), {}),
    ("Because there are a few things almost all of us do that feed the obsession without realising it.", I("c-loop", (.5, .45), 1.2, spin=6), {}),
    ("The first one is checking.", M("#1", "CHECKING", times=[0.0, "@checking"]), {}),
    ("Their profile, their stories, their last seen, the old photos.", V("scrolling-phone-2", 2.0, 1.15), {"in": "cut"}),
    ("Every time you look, you give your brain a tiny hit of the very thing it's craving.", I("c-brain-crave", (.6, .5), 1.0), {"sfx": [{"name": "zap", "at": "@hit"}]}),
    ("It's like trying to quit sugar while keeping a jar of cookies on your desk and opening it \"just to look\".", I("c-cookie-jar", (.55, .5), 1.0, to=[.75, .6], to_zoom=1.6, drift=0), {}),
    ("I know people say \"just block them\", and I used to think that was childish.", V("night-bed-phone-1", 6.0), {"pause_before": 0.25}),
    ("It's not.", K(("IT'S NOT.", "yellow")), {}),
    ("Blocking or muting isn't about them.", I("c-block", (.65, .5), 1.0), {}),
    ("It's about protecting your own brain while it heals.", M("PROTECTING", "YOUR OWN BRAIN", times=[0.0, "@own"]), {}),
    ("You can always unblock later, when it doesn't hurt anymore.", V("walking-park-0", 6.0), {}),
    ("And funny enough, by then, you usually won't even want to.", I("c-tuesday", (.4, .4), 1.2), {}),
    ("And while you're at it, archive the chat.", CHAT([["Lena", "them", -1.0]], title="Archived"), {"overlays": [NOTE("Chat archived", at=0.3, title="Messages")]}),
    ("Move the photos into a folder you don't open.", V("old-photos-2", 2.0), {}),
    ("Not because the memories don't matter,", I("c-last-page", (.6, .5), 1.2), {}),
    ("but because you can't heal a wound you keep pressing on.", Q("You can't heal a wound you keep pressing on.", end="@on"), {}),
]

P5 = [
    ("The second thing is the fantasy.", M("#2", "THE FANTASY", times=[0.0, "@fantasy"]), {"music": "intrigue"}),
    ("When someone leaves, our mind edits the movie.", I("c-movie-edit", (.4, .5), 1.0, to_zoom=1.4, drift=0), {}),
    ("It cuts out the arguments, the times they didn't reply, the way you never quite felt secure.", I("c-movie-edit", (.5, .75), 1.5), {"sfx": [{"name": "scratch", "at": "@cuts"}]}),
    ("And it keeps the highlights. The best night, the best kiss, the best conversation.", V("sad-woman-3", 6.0), {}),
    ("So you're not actually missing them.", K("YOU'RE NOT", ("MISSING THEM.", "white"), times=[0.0, "@missing"]), {}),
    ("You're missing a trailer your brain put together.", I("c-trailer", (.5, .5), 1.0, to=[.55, .35], to_zoom=1.5, drift=0), {}),
    ("And nobody can compete with a trailer.", M("NOBODY CAN", "COMPETE WITH", "A TRAILER", times=[0.0, "@compete", "@trailer"]), {}),
    ("Not the next person you date, and honestly, not even the real version of them.", V("sad-woman-6", 6.0), {}),
    ("A friend of mine gave me a weird piece of advice that worked.", V("friends-talking-5", 6.0), {"pause_before": 0.25}),
    ("She said, write down every single time she made you feel small, anxious, or ignored. Every one.", V("writing-letter-1", 2.0), {}),
    ("I thought it was petty.", K(("PETTY?", "white")), {}),
    ("But when I read that list a week later,", I("c-list", (.55, .5), 1.0, to_zoom=1.4, drift=0), {}),
    ("I realised I'd spent most of those three months waiting for a text.", CHAT([["hey :)", "me", -1.0], ["you there?", "me", 0.3]], status="Delivered", status_at="@waiting"), {}),
    ("The relationship I was grieving mostly existed in my head.", Q("The relationship I was grieving mostly existed in my head.", end="@head", width=30), {}),
    ("The third thing is the most painful one to admit.", M("#3", "HOLDING ON", times=[0.0, "@painful"]), {"pause_before": 0.25, "music": "sad"}),
    ("Sometimes we hold on because letting go means admitting it's really over.", I("c-candle", (.55, .45), 1.0, to_zoom=1.4, drift=0), {}),
    ("As long as you're still thinking about them, there's a tiny part of you that believes it might still happen.", V("sad-woman-3", 2.0), {}),
    ("The thinking feels like hope.", K("THE THINKING", ("FEELS LIKE HOPE.", "yellow"), times=[0.0, "@feels"]), {}),
    ("And giving it up feels like losing them a second time.", I("c-candle", (.57, .4), 1.8), {"sfx": [{"name": "heartbeat", "at": "@second"}]}),
]

P6 = [
    ("So how do you actually let go?", K("SO HOW DO YOU", ("ACTUALLY LET GO?", "yellow"), times=[0.0, "@actually"]), {"music": "warm", "sfx": [{"name": "riser", "at": "@go+0.4", "gain": 0.6}]}),
    ("Here's what I learned, and this is the part I wish someone had told me at the start.", V("sunrise-4", 2.0), {}),
    ("You have to close the loop yourself.", {"mg": "loop", "text": "CLOSE IT", "labels": []}, {"sfx": [{"name": "reveal", "at": "@close"}]}),
    ("You will probably never get the explanation you want.", V("rain-4", 4.0), {}),
    ("They might not even know why they left.", I("c-she-leaves", (.75, .5), 1.6), {}),
    ("So stop waiting for them to give you an ending, and write it yourself.", M("WRITE THE", "ENDING", "YOURSELF", mark=["ENDING"], times=[0.0, "@ending", "@yourself"]), {}),
    ("I did this literally. I wrote Lena a letter. Three pages.", I("c-letter", (.55, .55), 1.0, to_zoom=1.3, drift=0), {"pause_before": 0.25}),
    ("Everything I never said. What I felt, what hurt, what I was grateful for, and that I was done waiting.", V("writing-letter-5", 2.0), {}),
    ("And then I didn't send it.", K("I DIDN'T", ("SEND IT.", "yellow"), times=[0.0, "@send"]), {}),
    ("I read it out loud once, and I deleted it.", I("c-read-aloud", (.45, .4), 1.1), {"sfx": [{"name": "glitch-hit", "at": "@deleted", "gain": 0.5}]}),
    ("It sounds dramatic, but something in my chest unclenched that night.", V("tea-6", 2.0), {}),
    ("For the first time, the story had a last page.", I("c-last-page", (.6, .5), 1.0, drift=-0.1), {"sfx": [{"name": "sparkle", "at": "@last"}]}),
    ("The second thing is to give the craving somewhere else to go.", {"mg": "timer", "seconds": 600, "label": "WHEN IT HITS", "end_label": "MOVE"}, {"pause_before": 0.25, "music": "confident"}),
    ("When the urge to check hits, have a plan ready.", V("night-bed-phone-1", 4.0, 1.2), {}),
    ("Go for a walk.", V("walking-park-6", 2.0), {"in": "cut"}),
    ("Call a friend.", V("friends-talking-5", 9.0), {"in": "cut"}),
    ("Do ten push-ups.", I("c-pushups", (.4, .55), 1.1), {"in": "cut"}),
    ("Anything that moves your body and gets you out of that loop.", V("running-3", 2.0), {}),
    ("Your brain needs new rewards, not just the absence of the old one.", VS(["NOT", "LESS OF THEM"], ["MORE", "NEW REWARDS"], "@rewards"), {}),
    ("The third is to stop fighting the thoughts.", K("STOP FIGHTING", ("THE THOUGHTS", "yellow"), times=[0.0, "@thoughts"]), {"pause_before": 0.25}),
    ("This sounds backwards, but trying not to think about someone is like trying not to think about a pink elephant.", I("c-elephant", (.55, .45), 1.0, to=[.75, .4], to_zoom=1.3, drift=0), {}),
    ("The harder you push, the louder it gets.", I("c-crazy", (.5, .35), 1.5), {"shake": ["@louder"]}),
    ("So when they pop into your head, just notice it.", V("tea-1", 4.0), {}),
    ("\"There's that thought again.\"", Q("\"There's that thought again.\"", end="@again"), {}),
    ("Let it pass like a car going by.", I("c-car-passing", (.45, .55), 1.0, drift=0.07), {}),
    ("Don't chase it, and don't slam the door on it either.", I("c-car-passing", (.25, .5), 1.6), {}),
    ("Some days it'll pass a hundred times. That's fine.", V("rain-4", 2.0), {}),
    ("Every time you let it go by without following it, the road gets a little quieter.", I("c-car-passing", (.55, .5), 1.0, drift=-0.1), {}),
]

P7 = [
    ("And the last thing, the one that actually set me free.", K("THE ONE THAT", ("SET ME FREE", "yellow"), times=[0.0, "@set"]), {"music": "warm", "sfx": [{"name": "boom", "at": "@free", "gain": 0.5}]}),
    ("Fill the space they left with your own life.", I("c-empty-room", (.5, .5), 1.0), {}),
    ("Not with a new person straight away. With yourself.", K("NOT A NEW PERSON.", ("YOURSELF.", "yellow"), times=[0.0, "@yourself"]), {}),
    ("Your friends, your goals, the hobbies you dropped when you were busy waiting for a reply.", I("c-full-room", (.5, .5), 1.0, to_zoom=1.3, drift=0), {"in": "spin"}),
    ("Because the real reason someone takes over your mind is that there's too much empty room in it.", VS(["EMPTY ROOM", "THEY MOVE IN"], ["FULL LIFE", "NO ROOM"], "@empty"), {}),
    ("For me it was running.", V("running-0", 2.0), {"pause_before": 0.3, "music": "confident"}),
    ("I started because I couldn't sleep, and I needed to be tired.", I("c-run-night", (.5, .45), 1.0, drift=0.07), {}),
    ("Three months later, I signed up for my first half marathon.", V("marathon-1", 2.0), {"overlays": [TAG("HALF MARATHON  13.1 MI", "@half")]}),
    ("Somewhere around mile nine,", V("marathon-0", 2.0), {"overlays": [TAG("MILE 9", 0.1)]}),
    ("I realised I hadn't thought about Lena all day. Not once.", I("c-finish", (.5, .45), 1.0, to_zoom=1.3, drift=0), {}),
    ("I wasn't trying not to. There just wasn't room anymore.", M("THERE WASN'T", "ROOM ANYMORE", times=[0.0, "@room"]), {"sfx": [{"name": "sparkle", "at": "@anymore"}]}),
    ("And here's the thing nobody tells you about getting over someone.", V("sunrise-4", 6.0), {"pause_before": 0.25, "music": "warm"}),
    ("You don't wake up one day and decide it's over.", I("c-sleep", (.45, .45), 1.1), {}),
    ("You just notice, one random Tuesday, that they weren't the first thing you thought about this morning.", I("c-tuesday", (.4, .4), 1.0, drift=0.06), {}),
    ("And then it's a week.", {"mg": "timer", "seconds": 604800 // 60, "label": "ONE WEEK", "end_label": "FREE"}, {}),
    ("And then you hear that song in the supermarket, and you smile, and you keep walking.", I("c-smile-walk", (.45, .45), 1.0, to_zoom=1.3, drift=0), {}),
    ("That smile is how you know.", V("supermarket-5", 2.0), {}),
    ("Not that you forgot them.", K("NOT THAT YOU", "FORGOT THEM.", times=[0.0, "@forgot"]), {}),
    ("That they finally became a memory instead of a wound.", VS(["NOT A", "WOUND"], ["A", "MEMORY"], "@memory"), {"sfx": [{"name": "reveal", "at": "@memory"}]}),
    ("So if you're lying awake tonight thinking about someone, be gentle with yourself.", I("c-2am", (.45, .45), 1.0), {"pause_before": 0.3}),
    ("Your brain isn't broken. It's healing.", K("NOT BROKEN.", ("HEALING.", "yellow"), times=[0.0, "@healing"]), {}),
    ("Close the loop.", {"mg": "checklist", "title": "HOW TO LET GO", "items": ["CLOSE THE LOOP", "STOP FEEDING THE CRAVING", "LET THE THOUGHTS PASS", "BUILD A FULL LIFE"], "times": [0.05, 999, 999, 999]},
     {"sfx": [{"name": "pop", "at": 0.05}]}),
    ("Stop feeding the craving.", {"mg": "checklist", "title": "HOW TO LET GO", "items": ["CLOSE THE LOOP", "STOP FEEDING THE CRAVING", "LET THE THOUGHTS PASS", "BUILD A FULL LIFE"], "times": [-1, 0.05, 999, 999]},
     {"in": "cut", "sfx": [{"name": "pop", "at": 0.05}]}),
    ("Let the thoughts pass.", {"mg": "checklist", "title": "HOW TO LET GO", "items": ["CLOSE THE LOOP", "STOP FEEDING THE CRAVING", "LET THE THOUGHTS PASS", "BUILD A FULL LIFE"], "times": [-1, -1, 0.05, 999]},
     {"in": "cut", "sfx": [{"name": "pop", "at": 0.05}]}),
    ("And build a life so full that one day, there's simply no room left for someone who chose not to stay.",
     {"mg": "checklist", "title": "HOW TO LET GO", "items": ["CLOSE THE LOOP", "STOP FEEDING THE CRAVING", "LET THE THOUGHTS PASS", "BUILD A FULL LIFE"], "times": [-1, -1, -1, 0.05]},
     {"in": "cut", "sfx": [{"name": "sparkle", "at": 0.05}]}),
    ("If this helped you, send it to someone who's been stuck on someone for way too long.", K("SEND THIS TO SOMEONE", ("WHO CAN'T LET GO", "yellow"), times=["@send", "@stuck"]),
     {"sfx": [{"name": "pop", "at": "@send"}, {"name": "pop", "at": "@stuck"}]}),
    ("They need to hear that they're not crazy. And I'll see you in the next one.", I("c-smile-walk", (.45, .45), 1.2, drift=-0.12), {}),
]

PARTS = [P1, P2, P3, P4, P5, P6, P7]
SFX_FOR = {"spin": "swoosh", "blur": "tunnel", "zoom": "sweep", "glitch": "glitch-hit", "dip": "whoosh"}


def kind(v):
    return "img" if "img" in v else "video" if "video" in v else "mg"


def auto(shots):
    """This video's transition grammar: spin into graphics, blur out of them, zoom from image to video,
    hard cuts video to image and between clips."""
    out, prev = [], None
    for sh in shots:
        sh = dict(sh)
        k = kind(sh["v"])
        if "in" not in sh and prev:
            sh["in"] = "spin" if k == "mg" and prev != "mg" else "blur" if prev == "mg" and k != "mg" else \
                "zoom" if (prev, k) == ("img", "video") else "cut"
        if sh.get("in") in SFX_FOR:
            sh["sfx"] = [{"name": SFX_FOR[sh["in"]], "gain": 0.5}] + sh.get("sfx", [])
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
        if v.get("mg") == "timer":
            sh["sfx"] = sh.get("sfx", []) + [{"name": "tick", "at": 0.2 + 0.35 * i} for i in range(4)]
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
        if not cues or cues[0]["shot"] != 0:
            raise SystemExit(f"part {n}: first shot needs a music cue")
        last = n == len(PARTS)
        spec = {"out": f"../../output/cant-let-go/part{n}.mp4", "audio": f"p{n}.wav", "speed": 1.0,
                "tail": 2.0 if last else 0.45, "music_fade": 2.0 if last else 0.5, "music_cues": cues, "music_volume": 0.33,
                **({"fade_out": 2.0} if last else {}),
                "style": {"grade": "night", "captions": "underline", "caption_y": 0.86, "vignette": 0.5, "grain": 4},
                "shots": shots}
        (HERE / "parts" / f"part{n}.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False))
        kinds = [kind(s["v"]) for s in shots]
        print(f"part {n}: {len(shots)} shots ({kinds.count('img')} AI, {kinds.count('video')} stock, {kinds.count('mg')} graphics)")
        total += len(shots)
    print("total", total)


if __name__ == "__main__":
    main()
