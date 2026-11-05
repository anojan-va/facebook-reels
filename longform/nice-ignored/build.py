"""Build parts/partN.json for "Why Nice People Get Ignored".

Editing style (the 5th look): warm faded "film" grade on stock, karaoke captions (spoken words fill yellow),
diagonal yellow-edged "wipe" transitions, repeated YES stamps, a LIKED vs RESPECTED gauge, sticky notes for the
example sentences, scale/balance images, continuous storytelling with no chapter cards.
Usage: python3 build.py
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent


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


def VS(left, right, at, left_at=0.0):
    return {"mg": "versus", "left": left, "right": right, "at": at, "left_at": left_at}


def CHAT(messages, title="Chloe"):
    return {"mg": "chat", "messages": messages, "title": title}


def STAMPS(times, label=None, label_at=None, word="YES"):
    return {"mg": "stamps", "times": times, "word": word, **({"label": label, "label_at": label_at} if label else {})}


def STICKY(notes, times):
    return {"mg": "sticky", "notes": notes, "times": times}


def LT(title, sub, at=0.1):
    return {"mg": "lower_third", "title": title, "sub": sub, "at": at}


def TITLE(text, at, y=0.78):
    return {"mg": "title", "text": text, "at": at, "y": y, "size": 120}


TRACKS = {"sad": ("../../../reels/audio/music/silent-descent.mp3", 50.0),
          "intrigue": ("../../../reels/audio/music/echoes.mp3", 140.0),
          "tense": ("../../../reels/audio/music/out-of-this-world.mp3", 80.0),
          "warm": ("../../../reels/audio/music/fifth-of-february.mp3", 20.0),
          "confident": ("../../../reels/audio/music/unforgiven.mp3", 90.0)}

P1 = [
    ("You're the one who remembers everyone's birthday.", I("n-cake", (.55, .5), 1.0, to=[.45, .45], to_zoom=1.4, drift=0), {"sfx": ["hook"], "music": "sad"}),
    ("You're the one who stays late to help,", I("n-late-office", (.6, .5), 1.0, drift=0.07), {}),
    ("who says yes when you're exhausted,", STAMPS([0.1, "@yes", "@exhausted"]), {"sfx": [{"name": "bass", "at": 0.1, "gain": 0.4}, {"name": "bass", "at": "@yes", "gain": 0.4}, {"name": "bass", "at": "@exhausted", "gain": 0.4}]}),
    ("who listens to everybody's problems at two in the morning.", I("n-phone-2am", (.4, .4), 1.1), {}),
    ("You're kind. You're reliable. You never cause drama.", K("KIND.", "RELIABLE.", ("NO DRAMA.", "yellow"), times=[0.0, "@reliable", "@never"]), {}),
    ("And somehow, you're the one who gets ignored.", I("n-ignored-party", (.25, .6), 1.6, to=[.5, .55], to_zoom=1.0, drift=0), {"shake": ["@ignored"], "sfx": [{"name": "boom", "at": "@ignored", "gain": 0.6}]}),
    ("The selfish guy gets the girl.", V("couple-night-street-5", 2.0), {}),
    ("The loud coworker gets the promotion.", V("office-meeting-1", 2.0), {}),
    ("The friend who cancels on you every week still has a full group chat,", V("crowd-party-1", 2.0), {}),
    ("while you sit there wondering why nobody ever thinks of you first.", I("n-empty-chat", (.55, .45), 1.0, to_zoom=1.4, drift=0), {}),
    ("It feels unfair.", I("n-unfair", (.55, .55), 1.0, drift=0.06), {}),
    ("It feels like the world rewards bad behaviour and punishes good people.", VS(["GOOD PEOPLE", "PUNISHED"], ["BAD BEHAVIOUR", "REWARDED"], "@rewards", left_at="@punishes"), {}),
    ("And if you've ever thought, \"Maybe I should just stop being nice,\"", I("n-jerk-mask", (.6, .45), 1.0, to=[.72, .35], to_zoom=1.6, drift=0), {}),
    ("stay with me.", K(("STAY WITH ME.", "yellow")), {"music": "intrigue"}),
    ("Because I'm going to tell you why this happens,", V("phone-night-6", 2.0), {}),
    ("why it isn't actually about being too nice,", M("IT'S NOT ABOUT", "BEING TOO NICE", times=[0.0, "@being"]), {}),
    ("and the one change that made people finally start seeing me.", I("n-seen", (.5, .5), 1.0, to_zoom=1.3, drift=0), {}),
    ("It's not what you think, and you definitely don't have to become a jerk.", I("n-jerk-mask", (.55, .45), 1.1), {"sfx": [{"name": "scratch", "at": "@jerk"}]}),
    ("For most of my twenties, I was the nice guy.", V("working-late-1", 2.0), {"in": "wipe", "pause_before": 0.35, "music": "warm"}),
    ("Not in a fake way. I genuinely wanted everyone to be happy.", I("n-yes-everyone", (.5, .5), 1.0), {}),
    ("If a friend needed a ride to the airport at five in the morning, I was there.", I("n-airport", (.45, .5), 1.0, drift=0.06), {}),
    ("If someone at work needed help, I said yes before they even finished the question.", I("n-yes-everyone", (.5, .4), 1.6), {"sfx": [{"name": "pop", "at": "@yes"}]}),
    ("And there was a girl I'll call Chloe.", I("n-chloe-talk", (.7, .45), 1.4), {"overlays": [LT("CHLOE", "Name changed", at="@Chloe")]}),
    ("I liked her for almost a year.", V("couple-night-street-0", 2.0), {}),
    ("I listened to her talk about other guys.", I("n-chloe-talk", (.5, .5), 1.0), {}),
    ("I helped her move apartments twice.", I("n-boxes", (.4, .5), 1.0), {}),
    ("I sent her soup when she was sick.", I("n-soup", (.4, .5), 1.1), {}),
    ("And then she started dating a guy who didn't text her back for days.",
     CHAT([["miss youuu \U0001F97A", "me", 0.2], ["hello??", "me", "@text"], ["are you alive lol", "me", "@days"]], title="him"),
     {"sfx": [{"name": "pop", "at": 0.2}, {"name": "pop", "at": "@text"}, {"name": "pop", "at": "@days"}]}),
    ("A guy who forgot her birthday.", V("birthday-cake-2", 1.0), {}),
    ("And she was crazy about him.", I("n-chloe-bad-guy", (.6, .45), 1.0, to_zoom=1.4, drift=0), {}),
    ("I remember sitting in my car after she told me,", I("n-car-night", (.5, .45), 1.0, drift=0.07), {}),
    ("thinking, \"What is wrong with people? What is wrong with me?\"", Q("\"What is wrong with people? What is wrong with me?\"", end="@me"), {}),
    ("I'd done everything right. I'd been the good guy.", I("n-car-night", (.5, .35), 1.6), {}),
    ("And I still came second to someone who barely tried.", K("SECOND TO SOMEONE", ("WHO BARELY TRIED", "red"), times=[0.0, "@barely"]), {}),
]

P2 = [
    ("It took me years to understand the answer.", V("working-late-0", 2.0), {"music": "intrigue"}),
    ("And the first thing I had to learn was that there's a difference between being nice and being kind.", I("n-two-doors", (.5, .5), 1.0, to_zoom=1.3, drift=0), {}),
    ("Nice is about being liked. Kind is about doing good.", VS(["NICE", "BEING LIKED"], ["KIND", "DOING GOOD"], "@kind"), {"sfx": [{"name": "reveal", "at": "@kind"}]}),
    ("They look the same from the outside, but they come from completely different places.", I("n-two-doors", (.5, .45), 1.2), {}),
    ("When I was being nice, I wasn't really thinking about the other person.", V("phone-night-3", 2.0), {"pause_before": 0.25}),
    ("I was thinking about how they saw me.", I("n-mirror-people", (.4, .45), 1.1), {}),
    ("I said yes because I was scared of what would happen if I said no.", I("n-strings", (.5, .45), 1.0, to_zoom=1.4, drift=0), {}),
    ("I agreed with everyone because disagreeing felt dangerous.", I("n-strings", (.4, .2), 1.8), {}),
    ("My niceness wasn't a gift. It was a strategy to be accepted.", M("NOT A GIFT.", "A STRATEGY", times=[0.0, "@strategy"]), {}),
    ("And people can feel that.", V("office-meeting-5", 3.0), {}),
    ("They might not be able to put it into words, but they sense it.", V("friends-pizza-0", 4.0), {}),
    ("Something feels a little off. A little too eager. A little empty.", K("A LITTLE OFF.", "TOO EAGER.", ("EMPTY.", "yellow"), times=[0.0, "@eager-0.3", "@empty"]), {}),
    ("Like talking to someone who's always waiting for your reaction before they decide how to feel.", I("n-mirror-people", (.6, .45), 1.4), {}),
    ("Kindness is different.", K(("KINDNESS", "yellow"), "IS DIFFERENT.", times=[0.0, "@different"]), {"music": "warm"}),
    ("A kind person helps you because they want to, and says no when they need to.", I("n-boss-no", (.4, .45), 1.0, drift=0.06), {}),
    ("A kind person tells you the truth even when it's uncomfortable.", V("friends-pizza-2", 3.0), {}),
    ("Kindness has a spine. Niceness usually doesn't.", I("n-spine", (.5, .5), 1.0, to_zoom=1.4, drift=0), {"sfx": [{"name": "glass", "at": "@spine"}]}),
]

P3 = [
    ("And here's the part that really surprised me.", V("phone-night-7", 2.0), {"music": "tense"}),
    ("Being too nice can actually make people trust you less.", M("TOO NICE", "= LESS TRUST", times=[0.0, "@trust"]), {"shake": ["@less"], "sfx": [{"name": "bass", "at": "@less", "gain": 0.6}]}),
    ("In 2010, two researchers, Craig Parks and Asako Stone,", V("board-game-6", 2.0), {"overlays": [LT("PARKS & STONE", "Journal of Personality and Social Psychology (2010)")]}),
    ("ran an experiment where people played a group game sharing resources.", I("n-game-table", (.5, .5), 1.0, drift=0.06), {}),
    ("Some players were secretly programmed to be extremely generous, giving a lot and taking almost nothing.", I("n-game-table", (.3, .45), 1.6), {}),
    ("You'd think everyone would love them.", V("coins-0", 2.0), {}),
    ("Instead, most people wanted them kicked out of the group.", I("n-kicked-out", (.45, .5), 1.0, to_zoom=1.3, drift=0), {"sfx": [{"name": "wrong", "at": "@kicked", "gain": 0.5}]}),
    ("When the researchers asked why, people said things like,", V("office-meeting-5", 6.0), {}),
    ("\"They make the rest of us look bad,\"", Q("\"They make the rest of us look bad.\"", end="@bad"), {}),
    ("or, \"What are they really after?\"", Q("\"What are they really after?\"", end="@after"), {"in": "cut"}),
    ("Extreme generosity didn't feel safe. It felt suspicious.", VS(["NOT", "SAFE"], ["IT FELT", "SUSPICIOUS"], "@suspicious"), {"sfx": [{"name": "reveal", "at": "@suspicious"}]}),
    ("When I read that, I thought about every time I'd done too much for someone who barely knew me.", I("n-soup", (.45, .45), 1.4), {"pause_before": 0.25}),
    ("I thought I was being lovely. They were probably wondering what I wanted.", V("sorry-2", 2.0), {}),
    ("And honestly, sometimes I did want something.", K("SOMETIMES I DID", ("WANT SOMETHING", "yellow"), times=[0.0, "@want"]), {}),
    ("I wanted them to like me. I wanted them to notice me.", V("phone-night-6", 4.0), {}),
    ("I was giving with an invisible bill attached, and getting quietly angry when nobody paid it.", I("n-bill", (.5, .5), 1.0, to=[.55, .8], to_zoom=1.6, drift=0), {}),
    ("A lot of nice people do this without realising.", V("office-stress-2", 2.0), {"pause_before": 0.25}),
    ("I'll be nice to you, and in return you'll like me, appreciate me, choose me.", STICKY(["You'll like me", "Appreciate me", "Choose me"], ["@like", "@appreciate", "@choose"]),
     {"sfx": [{"name": "pop", "at": "@like"}, {"name": "pop", "at": "@appreciate"}, {"name": "pop", "at": "@choose"}]}),
    ("But nobody signed that contract.", I("n-contract", (.55, .5), 1.0, to_zoom=1.3, drift=0), {"sfx": [{"name": "scratch", "at": "@signed"}]}),
    ("So when it isn't honoured, you feel used, and they have no idea why you're upset.", I("n-contract", (.75, .4), 1.6), {}),
    ("I spent years feeling like the world owed me for all the favours I'd done.", V("working-late-5", 2.0), {}),
    ("The truth is, nobody asked me to do most of them.", M("NOBODY ASKED", "ME TO", times=[0.0, "@me"]), {}),
]

P4 = [
    ("The second thing I learned is about value.", V("coins-4", 1.0), {"music": "intrigue"}),
    ("When everything is a yes, your yes stops meaning anything.", STAMPS([0.1, 0.35, 0.6, "@yes", "@stops-0.3", "@stops"], label="YOUR YES MEANS NOTHING", label_at="@meaning"),
     {"sfx": [{"name": "bass", "at": t, "gain": 0.35} for t in (0.1, 0.35, 0.6)]}),
    ("Think about it.", K(("THINK ABOUT IT.", "yellow")), {}),
    ("If someone always agrees with you, their agreement doesn't feel special.", I("n-mirror-people", (.5, .5), 1.0), {}),
    ("If someone is always available, their time doesn't feel valuable.", I("n-phone-2am", (.45, .45), 1.4), {}),
    ("If someone praises everything you do, their praise becomes background noise.", I("n-coins", (.55, .6), 1.0, to=[.43, .5], to_zoom=1.6, drift=0), {}),
    ("I used to compliment everyone, all the time.", I("n-compliment", (.4, .45), 1.0), {"pause_before": 0.25}),
    ("I thought it made people feel good.", V("office-meeting-1", 6.0), {}),
    ("But a friend once told me, \"When you say something's great, I never know if you mean it.\"", Q("\"When you say something's great, I never know if you mean it.\"", end="@mean", width=30), {}),
    ("That stung. Because she was right.", I("n-compliment", (.67, .4), 1.7), {}),
    ("I'd given away so many compliments that they'd lost their value.", I("n-coins", (.5, .55), 1.1), {}),
    ("The people who get attention are often the people whose approval feels earned.", V("confident-walk-1", 2.0), {"music": "confident"}),
    ("Not because they're cold, but because their yes is real.", VS(["NOT", "COLD"], ["JUST", "REAL"], "@real"), {}),
    ("When they say \"That's brilliant,\" you know they mean it.", V("friends-pizza-2", 5.0), {}),
    ("So start being honest with your praise. Save it for the things you really mean.", M("SAVE YOUR PRAISE", "FOR WHAT", "YOU MEAN", mark=["YOU MEAN"], times=[0.0, "@things", "@really"]), {}),
    ("You'll be amazed how much more weight your words carry when they're not handed out like free samples.", I("n-coins", (.43, .45), 1.8), {"sfx": [{"name": "sparkle", "at": "@weight"}]}),
]

P5 = [
    ("The third thing is about edges. Nice people often have no shape.", I("n-invisible", (.3, .45), 1.4, to=[.5, .5], to_zoom=1.0, drift=0), {"music": "intrigue"}),
    ("When you're scared of upsetting anyone, you hide your opinions.", I("n-strings", (.5, .5), 1.2), {}),
    ("You say \"I don't mind\" when someone asks where to eat.", CHAT([["where do you wanna eat?", "them", 0.1], ["I don't mind \U0001F642", "me", "@mind"], ["anything is fine!", "me", "@eat"]], title="Group chat"),
     {"sfx": [{"name": "pop", "at": 0.1}, {"name": "pop", "at": "@mind"}, {"name": "pop", "at": "@eat"}]}),
    ("You laugh at jokes you don't find funny.", V("friends-pizza-0", 6.0), {}),
    ("You agree with whoever spoke last.", V("office-meeting-5", 9.0), {}),
    ("And slowly, you become a little bit invisible.", I("n-invisible", (.3, .45), 1.6), {}),
    ("People connect with people, not with mirrors.", I("n-mirror-people", (.5, .5), 1.0, drift=0.06), {"pause_before": 0.25}),
    ("They need something to hold on to.", K("SOMETHING", ("TO HOLD ON TO", "yellow"), times=[0.0, "@hold"]), {}),
    ("An opinion. A taste.", K("AN OPINION.", ("A TASTE.", "yellow"), times=[0.0, "@taste"]), {"in": "cut"}),
    ("A strong feeling about pineapple on pizza.", I("n-pizza", (.6, .45), 1.0, to_zoom=1.3, drift=0), {}),
    ("Something that tells them who you actually are.", V("friends-pizza-2", 9.0), {}),
    ("The next time someone asks where you want to eat, pick a place. Out loud.", CHAT([["where do you wanna eat?", "them", -1.0], ["Tacos. Joe's at 7 \U0001F32E", "me", "@place"]], title="Group chat"),
     {"sfx": [{"name": "pop", "at": "@place"}]}),
    ("It sounds tiny, but it's a muscle, and every time you use it, you become a little more visible.", I("n-seen", (.5, .45), 1.2), {}),
    ("There's a well-known idea in psychology from Susan Fiske and her colleagues.", V("office-meeting-1", 10.0), {"overlays": [LT("SUSAN FISKE", "Princeton University · warmth & competence")], "pause_before": 0.25}),
    ("When we meet someone, we judge them on two things: warmth and competence.", I("n-two-axis", (.5, .45), 1.0), {"captions": False, "overlays": [TITLE("WARMTH + COMPETENCE", "@warmth", y=0.8)]}),
    ("Are they on my side? And are they capable?", K("ON MY SIDE?", ("CAPABLE?", "yellow"), times=[0.0, "@capable"]), {}),
    ("Nice people usually score high on warmth.", {"mg": "gauge", "title": "HOW PEOPLE SEE NICE PEOPLE", "bars": [["WARMTH", 92, "yellow"], ["STRENGTH", 25, "red"]]}, {}),
    ("But if there's no strength behind it, no confidence, no opinions, people don't feel respect.",
     {"mg": "gauge", "title": "WHAT THEY FEEL", "bars": [["LIKED", 90, "yellow"], ["RESPECTED", 20, "red"]]}, {"in": "cut"}),
    ("They feel something closer to pity.", K("CLOSER TO", ("PITY", "red"), times=[0.0, "@pity"]), {}),
    ("They like you. They just don't think about you.", I("n-ignored-party", (.25, .6), 1.6), {}),
    ("And that was exactly my problem with Chloe.", I("n-chloe-talk", (.5, .5), 1.0), {"pause_before": 0.25, "music": "sad"}),
    ("She liked me. She trusted me.", V("couple-night-street-0", 6.0), {}),
    ("But I'd never shown her anything that made her feel a spark.", I("n-chloe-talk", (.3, .4), 1.6), {}),
    ("No opinions, no challenge, no edges. Just agreement.", K("NO OPINIONS.", "NO CHALLENGE.", "NO EDGES.", times=[0.0, "@challenge", "@edges"]), {}),
    ("The guy who forgot her birthday at least felt like a real person with a life of his own.", I("n-chloe-bad-guy", (.68, .4), 1.6), {}),
]

P6 = [
    ("So what do you actually do?", K("SO WHAT DO YOU", ("ACTUALLY DO?", "yellow"), times=[0.0, "@actually"]), {"music": "confident", "sfx": [{"name": "riser", "at": "@do+0.4", "gain": 0.6}]}),
    ("Because the answer is definitely not to become a jerk.", I("n-jerk-mask", (.6, .45), 1.1), {}),
    ("The first thing is to learn to say no.", M("#1", "LEARN TO SAY NO", times=[0.0, "@say"]), {}),
    ("Not rudely. Just honestly.", V("friends-pizza-2", 12.0), {}),
    ("\"I can't this weekend.\" \"I'd rather not.\" \"That doesn't work for me.\"",
     STICKY(["I can't this weekend", "I'd rather not", "That doesn't work for me"], [0.1, "@rather", "@that"]),
     {"sfx": [{"name": "pop", "at": 0.1}, {"name": "pop", "at": "@rather"}, {"name": "pop", "at": "@that"}]}),
    ("You don't need a long explanation.", V("office-meeting-1", 14.0), {}),
    ("A clear no makes your yes worth something again.", STAMPS([0.1, "@yes"], word="NO", label="A CLEAR NO", label_at="@worth"), {"sfx": [{"name": "bass", "at": 0.1, "gain": 0.5}]}),
    ("I'll never forget the first time I said no to my boss.", V("working-late-0", 6.0), {"in": "wipe", "pause_before": 0.3}),
    ("He asked me to take on another project, the third one that month,", I("n-boss-no", (.65, .45), 1.4), {}),
    ("and I said, \"I can't do that well right now with what's already on my plate.\"", I("n-boss-no", (.35, .45), 1.4), {}),
    ("My heart was pounding. I thought I'd get fired.", V("office-stress-6", 2.0), {"sfx": [{"name": "heartbeat", "at": "@pounding"}, {"name": "heartbeat", "at": "@pounding+0.45"}]}),
    ("Instead, he nodded and said, \"Okay, that's fair.\"", I("n-boss-nod", (.35, .45), 1.1), {"sfx": [{"name": "sparkle", "at": "@fair"}]}),
    ("And two months later, a coworker I'll call Mark, who'd been saying yes to everything just like me, was still drowning in extra work.",
     I("n-drowning", (.5, .45), 1.0, to_zoom=1.4, drift=0), {"overlays": [LT("MARK", "Name changed", at="@Mark")]}),
    ("I was the one who got asked to lead the next team.", I("n-lead", (.5, .5), 1.0, drift=0.07), {"sfx": [{"name": "reveal", "at": "@lead"}]}),
    ("The second thing is to stop apologising for existing.", M("#2", "STOP APOLOGISING", times=[0.0, "@apologising"]), {"pause_before": 0.25}),
    ("Watch how many times you say sorry in a day.", V("sorry-0", 1.0), {}),
    ("Sorry for asking. Sorry for being late by one minute. Sorry for having an opinion.", I("n-sorry", (.55, .5), 1.0, to_zoom=1.3, drift=0), {}),
    ("Every unnecessary sorry tells people you see yourself as a burden.", K("EVERY SORRY SAYS", ("I'M A BURDEN", "red"), times=[0.0, "@burden"]), {}),
    ("The third thing is to let people be disappointed.", M("#3", "LET THEM BE", "DISAPPOINTED", times=[0.0, "@let", "@disappointed"]), {"pause_before": 0.25}),
    ("This is the hardest one.", I("n-disappointed", (.7, .45), 1.5), {}),
    ("As a nice person, you feel responsible for everyone's feelings.", I("n-strings", (.5, .5), 1.1), {}),
    ("But other people's disappointment isn't an emergency. It's just a feeling.", VS(["NOT AN", "EMERGENCY"], ["JUST A", "FEELING"], "@feeling"), {}),
    ("They'll survive it, and so will you.", I("n-disappointed", (.35, .45), 1.4), {}),
    ("And the fourth thing is to give from fullness, not from fear.", M("#4", "GIVE FROM", "FULLNESS", times=[0.0, "@give", "@fullness"]), {"pause_before": 0.25, "music": "warm"}),
    ("Help people because you want to, not because you're scared they'll leave if you don't.", I("n-cup-full", (.5, .5), 1.0, drift=0.06), {}),
    ("When your kindness is a choice, not a payment, people feel the difference straight away.", VS(["A", "PAYMENT"], ["A", "CHOICE"], "@choice"), {}),
    ("And here's a test I still use.", K(("THE TEST", "yellow")), {}),
    ("Before you say yes to something, ask yourself:", V("phone-night-3", 4.0), {}),
    ("would I still do this if they never found out it was me?", Q("Would I still do this if they never found out it was me?", end="@me", width=30), {}),
    ("If the answer is yes, that's kindness.", K("YES?", ("THAT'S KINDNESS.", "yellow"), times=[0.0, "@kindness"]), {}),
    ("If the answer is no, you're probably trying to buy their approval.", I("n-bill", (.5, .5), 1.2), {}),
]

P7 = [
    ("Here's what happened when I started living like this.", V("confident-walk-6", 2.0), {"music": "warm"}),
    ("I lost a few people.", K("I LOST", ("A FEW PEOPLE.", "white"), times=[0.0, "@few"]), {}),
    ("The ones who only liked me because I was useful drifted away.", V("crowd-party-5", 2.0), {}),
    ("And honestly, that hurt.", I("n-car-night", (.5, .4), 1.4), {}),
    ("But the people who stayed started treating me differently.", V("friends-pizza-0", 2.0), {}),
    ("They asked my opinion. They invited me first.", I("n-pizza", (.5, .45), 1.1), {}),
    ("They respected my time, because I finally respected it.", {"mg": "gauge", "title": "AFTER", "bars": [["LIKED", 80, "yellow"], ["RESPECTED", 85, "yellow"]]}, {"sfx": [{"name": "sparkle", "at": "@finally"}]}),
    ("And years later, I ran into Chloe at a friend's wedding.", V("wedding-1", 2.0), {"in": "wipe", "pause_before": 0.3}),
    ("We talked for a while, and at one point she laughed and said,", I("n-wedding", (.55, .45), 1.0, to_zoom=1.3, drift=0), {}),
    ("\"You're so different now. You actually tell me when I'm wrong.\"", Q("\"You're so different now. You actually tell me when I'm wrong.\"", end="@wrong", width=30), {}),
    ("She meant it as a compliment.", I("n-wedding", (.7, .35), 1.6), {}),
    ("And for the first time, I realised I didn't need it to be.", I("n-wedding", (.45, .35), 1.6), {}),
    ("So if you're a nice person who keeps getting ignored, I don't want you to stop being good.", V("confident-walk-1", 6.0), {"pause_before": 0.25, "music": "confident"}),
    ("The world needs good people.", K("THE WORLD NEEDS", ("GOOD PEOPLE.", "yellow"), times=[0.0, "@good"]), {}),
    ("I want you to stop being nice and start being kind.", VS(["STOP BEING", "NICE"], ["START BEING", "KIND"], "@kind"), {"sfx": [{"name": "reveal", "at": "@kind"}]}),
    ("Have opinions.", {"mg": "checklist", "title": "BE KIND, NOT NICE", "items": ["HAVE OPINIONS", "SAY NO", "STOP APOLOGISING", "LET PEOPLE BE DISAPPOINTED", "GIVE BECAUSE YOU WANT TO"], "times": [0.05, 999, 999, 999, 999]},
     {"sfx": [{"name": "pop", "at": 0.05}]}),
    ("Say no.", {"mg": "checklist", "title": "BE KIND, NOT NICE", "items": ["HAVE OPINIONS", "SAY NO", "STOP APOLOGISING", "LET PEOPLE BE DISAPPOINTED", "GIVE BECAUSE YOU WANT TO"], "times": [-1, 0.05, 999, 999, 999]},
     {"in": "cut", "sfx": [{"name": "pop", "at": 0.05}]}),
    ("Stop apologising.", {"mg": "checklist", "title": "BE KIND, NOT NICE", "items": ["HAVE OPINIONS", "SAY NO", "STOP APOLOGISING", "LET PEOPLE BE DISAPPOINTED", "GIVE BECAUSE YOU WANT TO"], "times": [-1, -1, 0.05, 999, 999]},
     {"in": "cut", "sfx": [{"name": "pop", "at": 0.05}]}),
    ("Let people be disappointed.", {"mg": "checklist", "title": "BE KIND, NOT NICE", "items": ["HAVE OPINIONS", "SAY NO", "STOP APOLOGISING", "LET PEOPLE BE DISAPPOINTED", "GIVE BECAUSE YOU WANT TO"], "times": [-1, -1, -1, 0.05, 999]},
     {"in": "cut", "sfx": [{"name": "pop", "at": 0.05}]}),
    ("And give because you want to, not because you need something back.", {"mg": "checklist", "title": "BE KIND, NOT NICE", "items": ["HAVE OPINIONS", "SAY NO", "STOP APOLOGISING", "LET PEOPLE BE DISAPPOINTED", "GIVE BECAUSE YOU WANT TO"], "times": [-1, -1, -1, -1, 0.05]},
     {"in": "cut", "sfx": [{"name": "sparkle", "at": 0.05}]}),
    ("You don't have to be less good. You just have to be more you.", M("NOT LESS GOOD.", "MORE YOU.", times=[0.0, "@more"]), {"pause_before": 0.25, "music": "warm"}),
    ("The version of you with opinions, with limits, with a life of your own.", I("n-spine", (.5, .5), 1.0, drift=0.07), {}),
    ("That person isn't less lovable.", I("n-seen", (.5, .45), 1.0, to_zoom=1.3, drift=0), {}),
    ("That person is finally someone people can actually see.", I("n-seen", (.48, .35), 1.5), {"sfx": [{"name": "sparkle", "at": "@see"}]}),
    ("If this hit home, send it to the nicest person you know.", K("SEND THIS TO", ("THE NICEST PERSON", "yellow"), "YOU KNOW", times=["@send", "@nicest", "@know"]), {"sfx": [{"name": "pop", "at": "@send"}, {"name": "pop", "at": "@nicest"}]}),
    ("They probably need to hear it more than anyone. And I'll see you in the next one.", V("confident-walk-6", 6.0), {}),
]

PARTS = [P1, P2, P3, P4, P5, P6, P7]
SFX_FOR = {"wipe": "swoosh", "zoom": "sweep", "glitch": "glitch-hit", "flash": "swoosh-fast", "dip": "whoosh"}


def kind(v):
    return "img" if "img" in v else "video" if "video" in v else "mg"


def auto(shots):
    """Transition grammar for this video: wipe into graphics and between image/video, flash out of graphics, cuts otherwise."""
    out, prev = [], None
    for sh in shots:
        sh = dict(sh)
        k = kind(sh["v"])
        if "in" not in sh and prev:
            sh["in"] = "wipe" if k == "mg" and prev != "mg" else "flash" if prev == "mg" and k != "mg" else \
                "wipe" if (prev, k) == ("video", "img") else "cut"
        if sh.get("in") in SFX_FOR:
            sh["sfx"] = [{"name": SFX_FOR[sh["in"]], "gain": 0.5}] + sh.get("sfx", [])
        v = sh["v"]
        if k == "mg" and v["mg"] not in ("year",):
            sh.setdefault("captions", False)
        for ov in sh.get("overlays", []):
            if ov["mg"] == "title":
                sh["sfx"] = sh.get("sfx", []) + [{"name": "reveal", "at": ov["at"]}, {"name": "impact", "at": ov["at"], "gain": 0.6}]
            if ov["mg"] == "lower_third":
                sh["sfx"] = sh.get("sfx", []) + [{"name": "swoosh-fast", "at": ov["at"], "gain": 0.5}]
        out.append(sh)
        prev = k
    return out


def split_long(shots, n, limit=4.6):
    """Real voice runs slower than the draft: recut image/stock shots longer than `limit` s (durations from the last
    render's timeline.json) at the phrase break nearest the middle; the second half punches in on the same picture."""
    wj = HERE.parent / "output" / "nice-ignored" / f"part{n}_work" / "whisper.json"
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
    durs = {sh["text"]: e - b for sh, b, e in zip(shots, starts, ends)}
    out = []
    for sh in shots:
        d, k = durs.get(sh["text"], 0), kind(sh["v"])
        ws = sh["text"].split()
        if d <= limit or k == "mg" or len(ws) < 6:
            out.append(sh)
            continue
        mid = len(ws) / 2
        cand = [i for i in range(2, len(ws) - 2) if ws[i - 1][-1] in ",.?!;:"] or list(range(2, len(ws) - 2))
        cut = min(cand, key=lambda i: abs(i - mid) - (0.6 if ws[i - 1][-1] in ",.?!;:" else 0))
        first, second = " ".join(ws[:cut]), " ".join(ws[cut:])
        tail = set(words(second))
        a, b = dict(sh, text=first), {"text": second, "in": "cut",
                                      "sfx": [{"name": "swoosh-fast", "gain": 0.3}]}
        for key in ("sfx", "overlays", "shake"):
            items = sh.get(key, [])
            mv = [x for x in items if isinstance(x.get("at") if isinstance(x, dict) else x, str)
                  and re.sub(r"[+\-][\d.]+$", "", (x["at"] if isinstance(x, dict) else x))[1:].lower() in tail]
            if items:
                a[key] = [x for x in items if x not in mv]
            if mv:
                b[key] = b.get(key, []) + mv
        v = dict(sh["v"])
        if k == "img":
            v.pop("to", None), v.pop("to_zoom", None), v.pop("drift", None)
            z = v.get("zoom", 1.1)
            v["zoom"] = round(z / 1.3, 2) if z >= 1.45 else round(min(1.6, z * 1.25), 2)
        else:
            v.update(start=round(v.get("start", 1.0) + d * cut / len(ws), 2), zoom=round(v.get("zoom", 1.08) * 1.15, 2))
        b["v"] = v
        for key in ("captions",):
            if key in sh:
                b[key] = sh[key]
        out += [a, b]
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
        spec = {"out": f"../../output/nice-ignored/part{n}.mp4", "audio": f"p{n}.wav", "speed": 1.0,
                "tail": 2.0 if last else 0.45, "music_fade": 2.0 if last else 0.5, "music_cues": cues, "music_volume": 0.33,
                **({"fade_out": 2.0} if last else {}),
                "style": {"grade": "film", "captions": "karaoke", "caption_y": 0.86, "vignette": 0.36, "grain": 6},
                "shots": shots}
        (HERE / "parts" / f"part{n}.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False))
        kinds = [kind(s["v"]) for s in shots]
        print(f"part {n}: {len(shots)} shots ({kinds.count('img')} AI, {kinds.count('video')} stock, {kinds.count('mg')} graphics)")
        total += len(shots)
    print("total", total)


if __name__ == "__main__":
    main()
