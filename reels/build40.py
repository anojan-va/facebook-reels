"""reel.json for parable reels 31-40. Usage: python3 build40.py [slug ...]

Every reel opens on its hook image (h0) with a punch-in, a bass hit and a flash, so the first 3 seconds carry the hook line."""
import json
import sys
from pathlib import Path

C = [0.5, 0.5, 0.5]
MUS = {"echoes": ("echoes", 162.865), "tense": ("out-of-this-world", 117.26), "warm": ("fifth-of-february", 4.85)}


def S(img, text, focus="wide", zoom=1.0, sfx=(), punch=False, pause=False, drift=0.05):
    s = {"image": f"img/{img}.jpg", "text": text, "focus": focus, "zoom": zoom}
    if punch:
        s["punch"] = True
    else:
        s["drift"] = drift
    sfx = list(sfx)
    if pause:
        s["pause_before"] = 0.25
        sfx = [{"name": "whoosh", "at": -0.15}] + sfx
    s["sfx"] = sfx
    return s


def HOOK(img, text, focus="wide", zoom=1.25):
    """Two quick cuts on the hook image: wide with a flash, then a punch-in on the second half of the line."""
    a, b = text.split("|")
    s = S(img, a, "wide", 1.0, sfx=["hook"], drift=0.06)
    s["flash"] = True
    return [s, S(img, b, focus, zoom + 0.25, sfx=["bass"], punch=True)]


def END(img, text, focus="wide"):
    return S(img, text, focus, 1.15, drift=-0.08, sfx=["whoosh", {"name": "sparkle", "at": 0.3}])


VOICE = {"sharp-axe": "voice-cand-2.wav", "monkey-jar": "voice-cand-3.wav"}
R = {}
R["sharp-axe"] = ("tense", [
    HOOK("h0-tired", "Working harder|is not always the answer.", "man-face", 1.3),
    S("f01-hire", "A young woodcutter got a new job.", pause=True),
    S("f02-pile", "On the first day, he cut eighteen trees.", sfx=["pop"]),
    S("f03-amazed", "His boss was amazed.", C, 1.3, punch=True, sfx=["sparkle"]),
    S("f04-harder", "The next day, he worked even harder,", sfx=["whoosh2"]),
    S("f04-harder", "but cut only fifteen.", "man-face", 1.5, punch=True),
    S("f05-stump", "Then ten. Then just five.", sfx=["heartbeat"]),
    S("f06-hands", "He thought he was getting weak.", "man-face", 1.3),
    S("f07-blade", "His boss asked,", pause=True),
    S("f07-blade", "\"When did you last sharpen your axe?\"", C, 1.35, punch=True, sfx=["bass"]),
    S("f08-shrug", "\"Sharpen? I had no time.", "man-face", 1.2),
    S("f08-shrug", "I was too busy cutting trees.\"", "wide", 1.0, sfx=["wrong"]),
    S("f09-sharpen", "Rest is not wasting time.", sfx=["whoosh"]),
    S("f09-sharpen", "It's sharpening your axe.", "man-face", 1.4, punch=True, sfx=["sparkle"]),
    S("k1-rest", "Take care of yourself,", pause=True),
    S("k2-strong", "or you'll keep working harder", "man-face", 1.3),
    END("k2-strong", "for less."),
], "Rest is not wasting time.")
R["lost-watch"] = ("echoes", [
    HOOK("h0-silent", "The one who wins|is often", "man-face", 1.2),
    S("h0-silent", "the quietest one.", "man-face", 1.7, punch=True),
    S("g01-lost", "A farmer lost his precious watch", pause=True),
    S("g01-lost", "in a huge barn full of hay.", "wide", 1.1),
    S("g02-reward", "He promised a reward to whoever found it.", sfx=["pop"]),
    S("g03-chaos", "The children searched everywhere,", sfx=["whoosh2"]),
    S("g03-chaos", "shouting and running. Nothing.", C, 1.3, punch=True),
    S("g04-giveup", "One by one, they gave up.", sfx=["heartbeat"]),
    S("g05-ask", "Then a little boy", pause=True),
    S("g05-ask", "asked for one more chance.", "wide", 1.15),
    S("h0-silent", "He went in alone, sat down,", "wide", 1.0),
    S("h0-silent", "and stayed silent.", "man-face", 1.4, punch=True),
    S("g06-listen", "Soon he heard it.", "man-face", 1.2),
    S("g07-watch", "Tick...", C, 1.15, sfx=["heartbeat"]),
    S("g07-watch", "tick... tick.", C, 1.45, punch=True, sfx=["heartbeat"]),
    S("g06-listen", "He followed the sound", "man-face", 1.0),
    S("g08-found", "and found the watch.", sfx=["sparkle"]),
    S("k1-give", "A calm mind finds answers", pause=True),
    S("k1-give", "a noisy one can't.", C, 1.25),
    S("k2-calm", "Sometimes, all you need", "man-face", 1.3),
    END("k2-calm", "is silence."),
], "A calm mind finds answers")
R["golden-buddha"] = ("echoes", [
    HOOK("h0-crack", "What if your real value|is hidden under mud?", C, 1.3),
    S("j01-gold", "Long ago, monks owned", pause=True),
    S("j01-gold", "a giant golden statue.", C, 1.25, sfx=["sparkle"]),
    S("j02-cover", "When an army came, they covered it in thick clay", sfx=["whoosh2"]),
    S("j02-cover", "so nobody would steal it.", C, 1.3),
    S("j03-army", "The soldiers walked right past.", sfx=["whoosh"]),
    S("j03-army", "They saw only", C, 1.15),
    S("j03-army", "an ugly clay statue.", C, 1.4, punch=True),
    S("j04-years", "For hundreds of years,", pause=True),
    S("j04-years", "everyone forgot what was underneath.", C, 1.25),
    S("j05-notice", "One day, a young monk", "wide", 1.0),
    S("j05-notice", "noticed a small crack.", "man-face", 1.3),
    S("j06-glint", "Through it, he saw a glint of gold.", C, 1.3, punch=True, sfx=["sparkle"]),
    S("j07-chip", "He chipped away the clay,", sfx=["pop"]),
    S("j08-shine", "and the whole statue shone.", "wide", 1.0, sfx=["sparkle"]),
    S("k1-face", "Life covers you in clay:", pause=True),
    S("k1-face", "fear, pain, other people's opinions.", "man-face", 1.3),
    S("k2-walk", "But the gold was never gone.", "wide", 1.0),
    END("k2-walk", "Start chipping.", "man-face"),
], "and the whole statue shone.")
R["twenty-dollar"] = ("echoes", [
    HOOK("h0-hold", "No matter what happens to you,|remember this.", "man-face", 1.25),
    S("t01-stage", "A speaker held up a twenty-dollar bill.", pause=True),
    S("t01-stage", "\"Who wants this?\"", "man-face", 1.6, punch=True),
    S("t02-hands", "Every hand went up.", sfx=["pop"]),
    S("t03-crumple", "He crumpled it.", "man-face", 1.2, sfx=["glitch"]),
    S("t03-crumple", "\"Who still wants it?\"", "wide", 1.0),
    S("t02-hands", "Every hand stayed up.", C, 1.25, sfx=["pop"]),
    S("t04-step", "He threw it on the floor and stepped on it.", sfx=["bass"]),
    S("t05-dirty", "Now it was dirty and wrinkled.", "wide", 1.0),
    S("t05-dirty", "\"Now?\"", "man-face", 1.6, punch=True),
    S("t02-hands", "Still, every hand stayed up.", "wide", 1.1),
    S("t06-value", "\"It didn't lose its value,\" he said.", pause=True),
    S("t06-value", "\"And neither do you.\"", "man-face", 1.5, punch=True, sfx=["sparkle"]),
    S("t07-crushed", "Life may crush you, drop you,", pause=True),
    S("t07-crushed", "or step on you.", "man-face", 1.3, sfx=["heartbeat"]),
    S("k1-rise", "But you are still worth the same.", pause=True),
    END("k2-light", "Never forget your value."),
], "\"It didn't lose its value,\" he said.")
R["jar-rocks"] = ("echoes", [
    HOOK("h0-wrong", "Most people fill their life|in the wrong order.", C, 1.3),
    S("r01-rocks", "A professor put big rocks", pause=True),
    S("r01-rocks", "into a glass jar.", C, 1.2),
    S("r01-rocks", "\"Is it full?\"", "man-face", 1.5, punch=True),
    S("r02-yes", "The students said yes.", sfx=["pop"]),
    S("r03-pebbles", "He poured in small pebbles.", sfx=["whoosh2"]),
    S("r03-pebbles", "They rolled between the rocks.", C, 1.3),
    S("r02-yes", "\"Full now?\" \"Yes.\"", C, 1.2, sfx=["pop"]),
    S("r04-sand", "Then he poured in sand.", sfx=["whoosh2"]),
    S("r05-full", "It filled every gap.", C, 1.2, sfx=["sparkle"]),
    S("r06-point", "\"The rocks are your family,", pause=True),
    S("r06-point", "your health, your dreams.", "man-face", 1.4),
    S("r05-full", "The pebbles are your job and your things.", C, 1.35),
    S("r05-full", "The sand is everything small.", "wide", 1.05),
    S("h0-wrong", "If you fill the jar with sand first,", pause=True),
    S("h0-wrong", "there's no room for the rocks.\"", C, 1.35, punch=True, sfx=["wrong"]),
    S("k1-first", "Put the big rocks in first.", sfx=["whoosh"]),
    END("k2-done", "Everything else will find its place."),
], "\"The rocks are your family,")
R["monkey-jar"] = ("tense", [
    HOOK("h0-stuck", "Your problem might be|that you won't let go.", C, 1.3),
    S("m01-set", "Hunters had a clever way to catch monkeys.", pause=True),
    S("m02-banana", "They put a banana inside a jar", "wide", 1.0),
    S("m02-banana", "with a narrow neck.", C, 1.3),
    S("m03-reach", "A monkey reached in and grabbed it.", sfx=["pop"]),
    S("h0-stuck", "But with its fist closed around the banana,", "wide", 1.0),
    S("h0-stuck", "its hand couldn't come out.", C, 1.35, punch=True, sfx=["glitch"]),
    S("m04-hunters", "The hunters came closer.", sfx=["heartbeat"]),
    S("m05-scream", "The monkey screamed,", sfx=["bass"]),
    S("m05-scream", "but it would not open its hand.", C, 1.3, punch=True),
    S("m06-free", "It was free the whole time.", pause=True),
    S("m06-free", "All it had to do was let go.", C, 1.3, sfx=["sparkle"]),
    S("k0-hold", "What are you holding on to", pause=True),
    S("k0-hold", "that keeps you trapped?", "man-face", 1.4, punch=True),
    END("k1-open", "Open your hand."),
], "It was free the whole time.")
R["salt-lake"] = ("tense", [
    HOOK("h0-sad", "Your pain is not too big.|Your heart is too small.", "man-face", 1.4),
    S("s01-visit", "An unhappy young man", pause=True),
    S("s01-visit", "went to an old master.", C, 1.2),
    S("s02-salt", "The master told him to put a handful of salt", sfx=["whoosh2"]),
    S("s02-salt", "in a glass of water and drink it.", C, 1.25),
    S("s03-drink", "\"How does it taste?\" \"Terrible.\"", "man-face", 1.3, sfx=["wrong"]),
    S("s04-walk", "Then the master took him to a lake", pause=True),
    S("s05-throw", "and told him to throw", sfx=["whoosh2"]),
    S("s05-throw", "the same salt in and drink.", "man-face", 1.3),
    S("s06-sip", "\"How does it taste now?\"", "wide", 1.0),
    S("s06-sip", "\"Fresh.\"", "man-face", 1.5, punch=True, sfx=["sparkle"]),
    S("s07-master", "\"The pain of life is the same salt.", pause=True),
    S("s07-master", "What changes", C, 1.2),
    S("s07-master", "is the container.\"", C, 1.45, punch=True),
    S("k1-lake", "Stop being a glass.", pause=True),
    END("k2-peace", "Become a lake."),
], "Then the master took him to a lake")
R["frog-boil"] = ("tense", [
    HOOK("h0-desk", "This is how most people|waste their life", "man-face", 1.2),
    S("h0-desk", "without noticing.", "man-face", 1.8, punch=True),
    S("p01-jump", "Put a frog in boiling water,", pause=True),
    S("p01-jump", "and it jumps out right away.", C, 1.25, sfx=["pop"]),
    S("p02-cool", "But put it in cool water", sfx=["whoosh2"]),
    S("p02-cool", "and heat it slowly...", C, 1.25),
    S("p03-comfy", "it stays. It gets comfortable.", C, 1.25),
    S("p04-hotter", "The water gets hotter,", sfx=["heartbeat"]),
    S("p04-hotter", "and the frog", C, 1.15),
    S("p04-hotter", "keeps adjusting.", C, 1.4),
    S("p05-weak", "By the time it's too hot,", pause=True),
    S("p05-weak", "it has no strength left to jump.", C, 1.35, punch=True, sfx=["bass"]),
    S("p05-weak", "It wasn't the heat that killed it.", "wide", 1.05),
    S("p05-weak", "It was waiting too long to leave.", C, 1.5, punch=True),
    S("h0-desk", "A bad job.", "wide", 1.0, pause=True),
    S("p06-habit", "A bad habit.", "man-face", 1.2, sfx=["pop"]),
    S("p07-couple", "A bad relationship.", "wide", 1.0, sfx=["pop"]),
    S("k1-leave", "Don't wait until you can't jump.", pause=True),
    END("k2-free", "Leave while you still can."),
], "Don't wait until you can't jump.")
R["potato-grudge"] = ("tense", [
    HOOK("h0-sack", "Hating someone|hurts you more than them.", "man-face", 1.25),
    S("q01-bags", "A teacher gave each student", pause=True),
    S("q01-bags", "a bag and a pile of potatoes.", C, 1.2),
    S("q02-write", "\"For every person you refuse to forgive,", "man-face", 1.2),
    S("q02-write", "write their name on a potato and put it in the bag.\"", "wide", 1.0),
    S("q03-lift", "Some bags got very heavy.", sfx=["bass"]),
    S("q04-street", "\"Now carry it everywhere for one week.\"", pause=True),
    S("q05-bed", "Every day, the bag felt heavier.", sfx=["heartbeat"]),
    S("q06-rot", "The potatoes began to rot and smell.", C, 1.25, sfx=["glitch"]),
    S("q07-teacher", "\"This is what grudges do,\"", pause=True),
    S("q07-teacher", "the teacher said.", C, 1.15),
    S("q07-teacher", "\"You carry them, and they rot inside you.\"", C, 1.4, punch=True, sfx=["heartbeat"]),
    S("k1-down", "Forgive.", pause=True),
    S("k1-down", "Not for them. For you.", "man-face", 1.4, punch=True, sfx=["sparkle"]),
    END("k2-free", "Put the bag down."),
], "Forgive.")
R["farmer-treasure"] = ("echoes", [
    HOOK("h0-dig", "The real treasure|is never where you think.", "man-face", 1.25),
    S("v01-bed", "An old farmer was dying.", pause=True),
    S("v01-bed", "He told his lazy sons,", "wide", 1.1),
    S("v01-bed", "\"There's treasure buried in our field.\"", C, 1.35, punch=True, sfx=["sparkle"]),
    S("v02-dig2", "After he died,", pause=True),
    S("v02-dig2", "the sons dug up the whole field.", C, 1.2),
    S("v03-holes", "Every corner.", C, 1.2, sfx=["pop"]),
    S("v04-nothing", "They found nothing.", "man-face", 1.3, punch=True, sfx=["wrong"]),
    S("v05-sow", "Angry and tired, they planted wheat,", sfx=["whoosh2"]),
    S("v05-sow", "since the soil was already turned.", "man-face", 1.25),
    S("v06-wheat", "That year, their harvest", pause=True, sfx=["sparkle"]),
    S("v06-wheat", "was the biggest in the village.", C, 1.25),
    S("v07-market", "They sold it and became rich.", sfx=["pop"]),
    S("k1-wheat", "Then they understood.", pause=True),
    S("k1-wheat", "The treasure", "wide", 1.05),
    S("k1-wheat", "was the work.", "man-face", 1.5, punch=True),
    S("k2-field", "Stop looking for shortcuts.", "wide", 1.0),
    END("k2-field", "Your treasure is in the effort.", "man-face"),
], "That year, their harvest")

if __name__ == "__main__":
    here = Path(__file__).parent
    for slug in sys.argv[1:] or R:
        m1, shots, sw = R[slug]
        shots = [x for s in shots for x in (s if isinstance(s, list) else [s])]
        i = next(n for n, s in enumerate(shots) if s["text"] == sw)
        cue = lambda k, n: {"music": f"../audio/music/{MUS[k][0]}.mp3", "start": MUS[k][1], "shot": n}
        d = {"out": f"../output/{slug}.mp4", "audio": [VOICE.get(slug, "voice-cand-1.wav")], "speed": 1.0, "music_volume": 0.4,
             "fade_out": 1.0, "music_cues": [cue(m1, 0), cue("warm", i)], "shots": shots}
        json.dump(d, open(here / slug / "reel.json", "w"), indent=1)
        print(slug, len(shots))
