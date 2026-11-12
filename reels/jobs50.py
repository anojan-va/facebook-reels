"""Image jobs for parable reels 41-50 (echo-life … two-bricks). Two candidates per shot. Writes <slug>/jobs.json.

h0 is each reel's hook image. Every prompt ends with WORLD (white-filled objects, black ground) — reels 31-40 got
black jars/pots and brown soil without it."""
import json
from jobs25 import BOY, KING, MONK, ONLY2, STAND, colored, hero
from style_new import ANAT, MAN, OLD_MAN, scene

WORLD = (" Every object (boats, bowls, buckets, walls, furniture) is drawn WHITE-filled with thin dark outlines, never "
         "black-filled; the ground and sky are pure black with thin white lines, no brown, no green, no grey fills.")
WM = "drawn all in WHITE (white clothes, white skin, white hair), NOT coloured, NOT black-filled"
R = {}

MT = "Setting: a mountain path in thin white line art, tall rocky mountains and a deep valley ahead. "
DAD = f"his father, a tall adult man {WM}"
R["echo-life"] = [
    ("h0-shout", *hero("boy.jpg", BOY, MT, "the small boy stands at the edge of the path facing the mountains, both hands cupped around his mouth, shouting with all his strength; white sound-wave rings spread toward the mountains.", alone=True)),
    ("e01-walk", *hero("boy.jpg", BOY, MT, f"the small boy walks along the path beside {DAD}; the boy is a small child, his head at the father's waist; both walk side by side seen from the side. " + ONLY2)),
    ("e02-trip", *hero("boy.jpg", BOY, MT, "the small boy sits on the path after tripping, holding his knee with both hands, mouth open saying ow.", alone=True)),
    ("e03-echo", *scene(MT, "wide view of the huge mountains with big white sound-wave rings bouncing back from the rocky cliffs toward the viewer. No people.")),
    ("e04-who", *hero("boy.jpg", BOY, MT, "chest-up shot: the small boy looks around surprised and curious, one hand cupped beside his mouth calling out, his other hand at his side.", alone=True)),
    ("e05-angry", *hero("boy.jpg", BOY, MT, "the small boy screams angrily at the mountains, both fists clenched at his sides, face red, leaning forward.", alone=True)),
    ("e06-father", *scene(MT, f"a tall adult man {WM} stands on the path smiling and shouts toward the mountains with both hands cupped around his mouth. Only one person. " + ANAT)),
    ("e07-amazed", *hero("boy.jpg", BOY, MT, f"the small boy looks up at {DAD} with wide amazed eyes and a big smile; the father kneels on one knee beside him, one hand on the boy's shoulder, explaining. " + ONLY2)),
    ("k1-sunset", *hero("boy.jpg", BOY, MT.replace("Setting:", "Setting: at sunset,"), f"seen from behind: the small boy and {DAD} stand side by side looking at the mountains at sunset, the father's hand on the boy's shoulder. " + ONLY2)),
    ("k2-love", *hero("boy.jpg", BOY, MT.replace("Setting:", "Setting: at sunset,"), "the small boy shouts happily toward the mountains with arms spread wide, small glowing white hearts floating back to him from the mountains.", alone=True)),
]

LK = "Setting: a quiet lake in thick fog in thin white line art, calm water, soft mist. "
ROW = "a small WHITE wooden rowing boat"
R["empty-boat"] = [
    ("h0-yell", *hero("man.jpg", MAN, LK, f"the main character sits in {ROW} and shouts furiously toward the fog, pointing with his right hand, his left hand gripping the side of the boat, face red with anger.", alone=True)),
    ("b01-row", *hero("man.jpg", MAN, LK, f"the main character sits calmly in {ROW} rowing slowly, both hands on the two oars, peaceful face, fog all around.", alone=True)),
    ("b02-crash", *hero("man.jpg", MAN, LK, f"another {ROW} coming out of the fog crashes into the side of the main character's boat with a splash; he grabs the side of his boat with both hands, shocked.", alone=True)),
    ("b03-furious", *hero("man.jpg", MAN, LK, "chest-up shot: the main character, furious, teeth clenched, both fists raised in front of his chest.", alone=True)),
    ("b04-shout", *hero("man.jpg", MAN, LK, f"the main character stands up in {ROW} and shouts angrily into the fog with both hands cupped around his mouth.", alone=True)),
    ("b05-empty", *scene(LK.replace("thick fog", "clearing fog"), f"{ROW} drifts alone on the lake, completely EMPTY, no one inside, two oars resting in it, the fog lifting. No people.")),
    ("b06-calm", *hero("man.jpg", MAN, LK.replace("thick fog", "clearing fog"), f"the main character sits in {ROW} looking at an empty boat beside him, surprised, his anger gone, both hands resting on his knees.", alone=True)),
    ("b07-push", *hero("man.jpg", MAN, LK.replace("thick fog", "clearing fog"), f"the main character gently pushes an empty {ROW} away with one oar held in both hands, a calm small smile.", alone=True)),
    ("k1-sunrise", *hero("man.jpg", MAN, LK.replace("in thick fog", "at sunrise"), f"the main character rows {ROW} calmly across the lake at sunrise, both hands on the oars, a peaceful smile.", alone=True)),
    ("k2-peace", *hero("man.jpg", MAN, LK.replace("in thick fog", "at sunrise"), f"chest-up shot: the main character sits in his boat with eyes closed and a calm peaceful smile, both hands resting in his lap.", alone=True)),
]

HM = "Setting: a simple family dining room in thin white line art, a wooden table with chairs, a lamp. "
GRAN = f"an old grandfather {WM}, white hair and a short white beard, thin and frail"
KID = f"his little son, a small child about 6 years old {WM}"
WB = "a small WHITE wooden bowl"
R["wooden-bowl"] = [
    ("h0-corner", *scene(HM, f"{GRAN} sits alone on a small stool in the corner of the room eating from {WB} held in his shaking hands, sad and lonely; the empty family table in the background. Only one person. " + ANAT)),
    ("w01-spill", *scene(HM, f"chest-up shot: {GRAN} sits at the table, his shaking hands spill soup from a spoon; a broken white plate lies on the table. Only one person. " + ANAT)),
    ("w02-send", *hero("man.jpg", MAN, HM, f"the main character stands frowning and points with his right hand to a small stool in the corner; {GRAN} sits at the table looking down sadly. " + ONLY2)),
    ("w03-bowl", *hero("man.jpg", MAN, HM, f"the main character hands {WB} to {GRAN}, who sits on a stool in the corner and takes it with both hands, head bowed. " + ONLY2)),
    ("w04-carve", *scene(HM.replace("a lamp", "an evening lamp"), f"{KID} sits cross-legged on the floor carving a piece of wood with a small knife in his right hand, the wood in his left hand, concentrating. Only one person. " + ANAT)),
    ("w05-ask", *hero("man.jpg", MAN, HM.replace("a lamp", "an evening lamp"), f"the main character crouches beside {KID}, who sits on the floor carving wood; the father looks at him curiously, hands on his knees. The boy is a small child. " + ONLY2)),
    ("w06-answer", *scene(HM.replace("a lamp", "an evening lamp"), f"{KID} holds up {WB} he carved with both hands and smiles innocently up at the viewer. Only one person. " + ANAT)),
    ("w07-tears", *hero("man.jpg", MAN, HM.replace("a lamp", "an evening lamp"), "chest-up shot: the main character freezes, shocked, tears in his eyes, his right hand over his mouth, his left hand at his side.", alone=True)),
    ("k1-lead", *hero("man.jpg", MAN, HM.replace("a lamp", "an evening lamp"), f"the main character gently leads {GRAN} by the arm from the corner to the family table, one hand holding the old man's arm, the other on his back; the grandfather smiles. " + ONLY2)),
    ("k2-family", *hero("man.jpg", MAN, HM.replace("a lamp", "a warm evening lamp"), f"the main character sits at the family table smiling with {GRAN} on one side and {KID} on the other, all eating together happily. Exactly three people at the table, each sitting clearly apart.")),
]

MH = "Setting: a hall full of tall mirrors on every wall in thin white line art, endless reflections. "
HAPPY = "a small happy dog drawn all in WHITE (white fur), NOT black-filled"
ANGRY = "a small angry dog drawn all in WHITE (white fur), NOT black-filled"
R["thousand-mirrors"] = [
    ("h0-growl", *scene(MH, f"{ANGRY} growls with bared teeth at the mirrors; dozens of angry growling reflections growl back at it from every mirror. No people.")),
    ("m01-house", *scene("Setting: a strange old house at night in thin white line art, its windows shining like mirrors. ", "the old house with a big open door, mysterious. No people.")),
    ("m02-enter", *scene(MH, f"{HAPPY} trots into the mirror hall wagging its tail, ears up, smiling. No people.")),
    ("m03-wag", *scene(MH, f"{HAPPY} wags its tail and dozens of happy tail-wagging dog reflections smile back at it from every mirror. No people.")),
    ("m04-leave", *scene("Setting: the open door of an old house in daylight in thin white line art. ", f"{HAPPY} trots out of the door happily, tail high, little white hearts above it. No people.")),
    ("m05-enter2", *scene(MH, f"{ANGRY} stomps into the mirror hall, growling, fur bristling, teeth showing. No people.")),
    ("m06-many", *scene(MH, f"dozens of growling dog reflections surround {ANGRY} from every mirror, all baring teeth. No people.")),
    ("m07-run", *scene("Setting: the open door of an old house at night in thin white line art. ", f"{ANGRY} runs out of the door in fear, tail between its legs, scared. No people.")),
    ("k1-mirror", *hero("man.jpg", MAN, "Setting: a hall of tall mirrors in thin white line art; the reflections are faint thin WHITE outlines only, not coloured. ", "the main character stands in front of a tall mirror and smiles warmly; his reflection, a faint white outline, smiles back. Both hands at his sides. " + STAND, alone=True)),
    ("k2-smile", *hero("man.jpg", MAN, "Setting: a bright street in thin white line art. ", "chest-up shot: the main character smiles warmly and kindly at the viewer.", alone=True)),
]

GR = "Setting: a quiet temple garden in thin white line art, a big tree, a stone path. "
MAD = f"an angry man {WM}"
R["insult-gift"] = [
    ("h0-face", *hero("monk.jpg", MONK, GR, f"{MAD} shouts furiously right in the face of the young monk, pointing a finger at him; the monk stands calm and smiling, palms together. " + ONLY2)),
    ("i01-come", *hero("monk.jpg", MONK, GR, f"{MAD} stomps along the stone path toward the young monk, who sits peacefully under the big tree. " + ONLY2)),
    ("i02-insult", *hero("monk.jpg", MONK, GR, f"{MAD} stands shouting and waving both arms; the young monk sits cross-legged under the tree listening calmly, hands in his lap. " + ONLY2)),
    ("i03-smile", *hero("monk.jpg", MONK, GR, "chest-up shot: the young monk smiles calmly and kindly, completely relaxed.", alone=True)),
    ("i04-why", *scene(GR, f"{MAD} throws both arms up in frustration, shouting with his mouth wide open. Only one person. " + ANAT)),
    ("i05-gift", *hero("monk.jpg", MONK, GR, f"the young monk holds out a small WHITE gift box with a ribbon in both hands toward {MAD}, who looks at it confused. " + ONLY2)),
    ("i06-think", *scene(GR, f"chest-up shot: {MAD} looks confused, scratching his head with one hand, his other hand at his side. Only one person. " + ANAT)),
    ("i07-exact", *hero("monk.jpg", MONK, GR, "the young monk smiles wisely and raises one open hand gently, his other hand resting on his knee as he sits under the tree.", alone=True)),
    ("i08-leave", *scene(GR, f"{MAD} walks away along the stone path, head down, speechless, seen from behind. Only one person. " + ANAT)),
    ("k1-calm", *hero("monk.jpg", MONK, GR.replace("Setting:", "Setting: at sunset,"), "the young monk sits cross-legged meditating under the big tree at sunset, eyes closed, a peaceful smile, hands resting on his knees.", alone=True)),
]

TR = "Setting: an old tree on a cliff in thin white line art, strong wind, a wide sky. "
BIRD = "a small bird drawn all in WHITE (white feathers), NOT black-filled"
R["bird-branch"] = [
    ("h0-crack", *scene(TR, f"close-up: {BIRD} stands calmly on a thin dry branch that is cracking in the middle, wind blowing leaves around it. No people.")),
    ("r01-sit", *scene(TR.replace("strong wind", "calm air"), f"{BIRD} sits on a thin dry branch of the old tree, peaceful. No people.")),
    ("r02-wind", *scene(TR, f"the strong wind shakes the thin dry branch hard, leaves flying; {BIRD} holds on. No people.")),
    ("r03-break", *scene(TR, "extreme close-up of a thin dry branch splitting and cracking, splinters flying. No people.")),
    ("r04-animals", *scene("Setting: the foot of an old tree in thin white line art. ", "a squirrel, a rabbit and an owl, all drawn WHITE, look up worried with wide eyes, each clearly apart. No people.")),
    ("r05-calm", *scene(TR, f"close-up: {BIRD} looks straight ahead calmly with steady eyes, not looking down, wind ruffling its feathers. No people.")),
    ("r06-fly", *scene(TR, f"the branch breaks and falls; {BIRD} spreads its wings wide and flies up into the sky. No people.")),
    ("r07-sky", *scene("Setting: a wide open sky with clouds in thin white line art. ", f"{BIRD} soars high and free with wings fully spread. No people.")),
    ("k0-box", *hero("man.jpg", MAN, "Setting: a city street in thin white line art. ", "the main character walks out of an office building carrying a cardboard box of his things in both arms, sad, head down.", alone=True)),
    ("k1-wings", *hero("man.jpg", MAN, "Setting: a cliff top at sunrise in thin white line art, wide sky, birds flying. ", "the main character stands at the cliff top with both arms spread wide like wings, chin up, eyes closed, confident and free. " + STAND, alone=True)),
]

GD = "Setting: a village garden in thin white line art, soil, a small fence, a cottage. "
YM = f"a young man {WM}"
MANGO = "a big tree full of ORANGE-YELLOW mangoes"
R["planting-tree"] = [
    ("h0-plant", *hero("man-old.jpg", OLD_MAN, GD, "the old main character kneels on both knees and gently places a small mango sapling into a hole in the soil with both hands.", alone=True)),
    ("t01-dig", *hero("man-old.jpg", OLD_MAN, GD, "the old main character digs a small hole with a small shovel, both hands on the handle, slowly and patiently.", alone=True)),
    ("t02-laugh", *hero("man-old.jpg", OLD_MAN, GD, f"{YM} stands laughing and points at the old main character with one hand, his other hand on his hip; the old man kneels by the hole, digging. " + ONLY2)),
    ("t03-keep", *hero("man-old.jpg", OLD_MAN, GD, "chest-up shot: the old main character keeps digging calmly with a quiet wise smile, not bothered.", alone=True)),
    ("t04-memory", *colored(GD, f"a memory: a small boy drawn all in WHITE sits under {MANGO} and eats a mango happily. Only the mangoes have colour.")),
    ("t05-pat", *hero("man-old.jpg", OLD_MAN, GD, "the old main character kneels and gently pats the soil around a small sapling with both hands, a warm smile.", alone=True)),
    ("t06-years", *colored(GD, f"years later: {YM.replace('a young man', 'a grown man')} sits in the shade under {MANGO} with two small children drawn all in WHITE, all eating mangoes and smiling, each clearly apart. Only the mangoes have colour.")),
    ("t07-understand", *colored(GD, f"{YM.replace('a young man', 'a grown man')} stands under {MANGO}, looking up at it with a touched, thoughtful face, one hand on the trunk. Only the mangoes have colour.")),
    ("k1-sapling", *hero("man-old.jpg", OLD_MAN, GD.replace("Setting:", "Setting: at sunset,"), "the old main character stands beside the small sapling he planted at sunset, leaning on his shovel with both hands, a peaceful smile. " + STAND, alone=True)),
]

BK = "Setting: inside a farm dairy in thin white line art, a big deep WHITE bucket full of white cream. "
FROG = "a small frog drawn all in WHITE, NOT black-filled, NOT green"
R["frogs-cream"] = [
    ("h0-kick", *scene(BK, f"close-up: {FROG} kicks furiously in the thick white cream, determined face, cream splashing everywhere. No people.")),
    ("c01-fall", *scene(BK, f"two frogs drawn all in WHITE fall from above into the big bucket of cream with a splash. No people.")),
    ("c02-walls", *scene(BK, f"{FROG} tries to climb the slippery inside wall of the bucket and slides back down. No people.")),
    ("c03-sink", *scene(BK, f"{FROG} closes its eyes, gives up and sinks into the cream, only its head still showing. No people.")),
    ("c04-tired", *scene(BK, f"close-up: {FROG} floating in cream, exhausted, sweating, but with a determined look. No people.")),
    ("c05-kicking", *scene(BK, f"{FROG} kicks its legs hard, the cream swirling in circles around it, motion lines. No people.")),
    ("c06-butter", *colored(BK, f"{FROG} sits on top of a solid lump of pale YELLOW butter in the bucket, proud. Only the butter has colour. No people.")),
    ("c07-jump", *scene(BK, f"{FROG} leaps high out of the bucket, free, legs stretched out. No people.")),
    ("k1-climb", *hero("man.jpg", MAN, "Setting: a steep rocky hill in thin white line art. ", "the main character climbs the steep hill, tired and sweating but determined, one hand on a rock, leaning forward.", alone=True)),
    ("k2-top", *hero("man.jpg", MAN, "Setting: a hilltop at sunrise in thin white line art, wide sky. ", "the main character stands on top of a big rock at sunrise, confident, both hands on his hips. " + STAND, alone=True)),
]

KG = "Setting: a royal palace hall in thin white line art, a throne, tall pillars. "
RD = "Setting: a rocky dirt road through a kingdom in thin white line art, sharp stones. "
SV = f"a humble servant {WM}"
R["leather-shoes"] = [
    ("h0-feet", *hero("man.jpg", KING, KG, "the king sits on his throne holding his bare sore right foot in both hands, wincing in pain, small red scratches on his foot.", alone=True)),
    ("l01-walk", *hero("man.jpg", KING, RD, "the king walks barefoot on the sharp stones of the road, wincing, arms out for balance.", alone=True)),
    ("l02-order", *hero("man.jpg", KING, KG, "the king sits on his throne and points forward angrily with his right hand, commanding, his left hand gripping the armrest.", alone=True)),
    ("l03-ministers", *scene(KG, f"three ministers {WM} with white robes panic, hands on their heads, mouths open, standing clearly apart. " + ANAT)),
    ("l04-cows", *scene("Setting: wide green hills drawn in thin white line art. ", "a huge herd of cows drawn all in WHITE fills the hills to the horizon. No people.")),
    ("l05-servant", *hero("man.jpg", KING, KG, f"{SV} steps forward and bows, one hand on his chest, speaking to the king, who sits on his throne listening. " + ONLY2)),
    ("l06-laugh", *hero("man.jpg", KING, KG, "chest-up shot: the king laughs warmly, head tilted back, one hand on his belly.", alone=True)),
    ("l07-shoes", *hero("man.jpg", KING, KG, "the king holds up a simple pair of brown leather shoes in both hands, smiling, admiring them.", alone=True)),
    ("k1-wear", *hero("man.jpg", KING, RD.replace("Setting:", "Setting: at sunrise,"), "the king walks confidently along the rocky road wearing simple brown leather shoes, smiling, arms swinging naturally.", alone=True)),
]

BW = "Setting: a monastery courtyard in thin white line art, a long WHITE brick wall, a temple roof. "
VIS = f"a visitor {WM}"
R["two-bricks"] = [
    ("h0-stare", *hero("monk.jpg", MONK, BW, "chest-up shot: the young monk stares sadly at the brick wall in front of him, eyes on two crooked bricks, ashamed, his hands at his sides.", alone=True)),
    ("k01-build", *hero("monk.jpg", MONK, BW, "the young monk carefully places a white brick on the half-built wall with both hands, a trowel resting on the wall beside him, focused.", alone=True)),
    ("k02-care", *hero("monk.jpg", MONK, BW, "the young monk checks a brick with a small spirit level held in both hands, very carefully.", alone=True)),
    ("k03-done", *hero("monk.jpg", MONK, BW, "the young monk steps back and looks at the finished long white brick wall, hands at his sides. " + STAND, alone=True)),
    ("k04-crooked", *scene(BW, "close-up of a white brick wall: hundreds of straight bricks and exactly TWO crooked bricks in the middle, tilted. No people.")),
    ("k05-ashamed", *hero("monk.jpg", MONK, BW, "the young monk covers his face with both hands, ashamed, standing in front of the wall.", alone=True)),
    ("k06-visitor", *hero("monk.jpg", MONK, BW, f"{VIS} stands in front of the long wall admiring it with a big smile, one hand raised toward it; the young monk stands beside him, unhappy. " + ONLY2)),
    ("k07-point", *hero("monk.jpg", MONK, BW, f"the young monk points at two crooked bricks in the wall with his right hand; {VIS} beside him smiles and gestures with an open hand at the whole wall. " + ONLY2)),
    ("k08-cry", *hero("monk.jpg", MONK, BW, "chest-up shot: the young monk smiles through tears, touched, looking at the wall.", alone=True)),
    ("k1-whole", *hero("monk.jpg", MONK, BW.replace("Setting:", "Setting: at sunset,"), "seen from a distance: the young monk stands peacefully looking at the whole long white brick wall at sunset, hands together. " + STAND, alone=True)),
]

if __name__ == "__main__":
    for n, (slug, jobs) in enumerate(R.items()):
        js = [{"out": f"img/cand/{o}-{k}.jpg", "refs": r, "seed": 12000 + 37 * n + 2 * i + (k == "b"), "prompt": p + WORLD}
              for i, (o, p, r) in enumerate(jobs) for k in "ab"]
        json.dump({"model": "black-forest-labs/flux.2-klein-4b", "size": "1152x2048", "workers": 2, "jobs": js},
                  open(f"{slug}/jobs.json", "w"), indent=1)
        print(slug, len(js))
