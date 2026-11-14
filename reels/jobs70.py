"""Image jobs for parable reels 61-70 (kintsugi-bowl … search-within). Two candidates per shot. Writes <slug>/jobs.json.

Same conventions as jobs50/jobs60: h0 = hook image, WORLD appended to every prompt. Lessons from 51-60 are in the
prompts: who holds what is stated per person, roles get "the man in WHITE is the one who …", counts of things are
drawn as overlays, never asked of Klein."""
import json
from jobs25 import BOY, MONK, ONLY2, STAND, colored, hero
from jobs50 import WM, WORLD
from style_new import ANAT, MAN, OLD_MAN, scene

R = {}

TEA = "Setting: a quiet Japanese room in thin white line art, a low wooden table, paper screens. "
BOWL = "a WHITE ceramic tea bowl"
GOLDBOWL = "a WHITE ceramic tea bowl repaired with shining GOLD lines running through its cracks"
CRAFT = f"an old craftsman {WM}, short white beard"
R["kintsugi-bowl"] = [
    ("h0-gold", *colored(TEA, f"close-up: {GOLDBOWL}, glowing, on the low table. Only the gold lines have colour. No people.")),
    ("k01-drop", *hero("man.jpg", MAN, TEA, f"the main character's hands open in shock as {BOWL} falls from them toward the floor, his face horrified, both arms reaching down.", alone=True)),
    ("k02-shards", *scene(TEA, f"close-up: {BOWL} shattered into many white pieces on the wooden floor. No people.")),
    ("k03-sad", *hero("man.jpg", MAN, TEA, "the main character kneels on both knees on the floor looking down sadly at white broken pieces in front of him, both hands resting on his thighs.", alone=True)),
    ("k04-glue", *colored(TEA, f"{CRAFT} sits at the low table and carefully paints a thin GOLD line along a crack of a white tea bowl with a small brush in his right hand, holding the bowl with his left hand. Only the gold has colour. Only one person. " + ANAT)),
    ("k05-gasp", *hero("man.jpg", MAN, TEA, f"chest-up shot: the main character gasps in amazement, eyes wide, both hands raised in front of his chest, looking down at {GOLDBOWL} on the table. Only the gold lines and the main character have colour.", alone=True)),
    ("k06-smile", *colored(TEA, f"chest-up shot: {CRAFT} smiles wisely, holding {GOLDBOWL} in both hands. Only the gold has colour. Only one person.")),
    ("k1-hold", *hero("man.jpg", MAN, TEA.replace("Setting:", "Setting: in warm evening light,"), f"the main character sits at the low table holding {GOLDBOWL} in both hands, a calm grateful smile. Only the gold lines and the main character have colour.", alone=True)),
]

CORN = "Setting: a tall cornfield in thin white line art, a small farmhouse, a fence. "
REP = f"a reporter {WM} holding a notepad and pen"
R["farmer-best-corn"] = [
    ("h0-wind", *scene(CORN, "wide view: strong wind blows across many neighbouring cornfields, little glowing white pollen dots flying from field to field in curved lines. No people.")),
    ("c01-prize", *colored(CORN, "the main character in his mustard-YELLOW hoodie, black cargo pants and white sneakers, short brown beard, stands proudly in his cornfield holding up a big GOLD prize ribbon in his right hand, his left hand at his side.")),
    ("c02-seeds", *hero("man.jpg", MAN, CORN, f"the main character pours seeds from a small sack into the open hands of a neighbour farmer {WM}, who smiles gratefully. " + ONLY2)),
    ("c03-reporter", *hero("man.jpg", MAN, CORN, f"{REP} stands frowning in confusion, asking a question; the main character stands beside his corn smiling calmly, both hands at his sides. The man in WHITE holds the notepad. " + ONLY2)),
    ("c04-explain", *hero("man.jpg", MAN, CORN, "chest-up shot: the main character points with his right hand toward the neighbouring fields, explaining, his left hand at his side, a wise smile.", alone=True)),
    ("c05-bad", *scene(CORN, "close-up: a weak bent cornstalk with small withered cobs in a poor field, wind blowing white pollen dots toward a healthy field beside it. No people.")),
    ("c06-neighbors", *scene(CORN.replace("Setting:", "Setting: at sunset,"), f"three farmers {WM} stand in their own tall healthy cornfields, waving happily, each standing clearly apart. " + ANAT)),
    ("k1-together", *hero("man.jpg", MAN, CORN.replace("Setting:", "Setting: at sunset,"), "the main character stands in a huge field of tall healthy corn at sunset, looking out over all the neighbouring fields, a warm satisfied smile. " + STAND, alone=True)),
]

PEAK = "Setting: a rocky mountain peak above the clouds in thin white line art. "
EAG = "an old eagle drawn all in WHITE (white feathers), NOT black-filled"
R["eagle-rebirth"] = [
    ("h0-strike", *scene(PEAK, f"{EAG} strikes its long bent beak hard against a rock, white sparks and chips flying, eyes fierce. No people.")),
    ("e01-old", *scene(PEAK, f"{EAG} sits hunched on a rock, tired, its claws curled and weak, its beak long and bent, its feathers heavy and drooping. No people.")),
    ("e02-hunt", *scene("Setting: a river valley in thin white line art. ", f"{EAG} swoops down slowly toward a fish in a river and misses, the fish escaping. No people.")),
    ("e03-choice", *scene(PEAK, f"{EAG} sits alone on the edge of the cliff looking down at the clouds, thoughtful. No people.")),
    ("e04-fly-up", *scene(PEAK, f"{EAG} flies slowly and heavily up toward the mountain peak. No people.")),
    ("e05-wait", *scene(PEAK.replace("Setting:", "Setting: at night under the moon,"), f"{EAG} sits hidden in a rocky nest on the peak, waiting patiently, featherless patches on its body. No people.")),
    ("e06-new", *scene(PEAK.replace("Setting:", "Setting: at sunrise,"), "a strong young-looking eagle drawn all in WHITE with fresh bright feathers spreads its huge wings wide on the peak, proud. No people.")),
    ("e07-soar", *scene("Setting: a wide sky above the clouds at sunrise in thin white line art. ", "a strong white eagle soars high and fast, wings fully spread, powerful. No people.")),
    ("k1-hero", *hero("man.jpg", MAN, PEAK.replace("Setting:", "Setting: at sunrise,"), "the main character stands on the mountain peak at sunrise, chin up, a determined calm face, both hands at his sides, a white eagle flying above him. " + STAND, alone=True)),
]

HOUSE = "Setting: a big modern house in thin white line art, a swimming pool, a car. "
FARM = "Setting: a small poor farm in thin white line art, a wooden hut, a river, fields. "
DAD = f"his rich father {WM}, short white hair, a white shirt"
R["rich-poor-trip"] = [
    ("h0-stars", *hero("boy.jpg", BOY, FARM.replace("Setting:", "Setting: at night under a sky FULL of bright white stars,"), "the small boy lies on his back on the grass looking up at a sky full of stars, amazed, a big smile, arms spread out.", alone=True)),
    ("r01-car", *hero("boy.jpg", BOY, HOUSE, f"the small boy and {DAD} get into a big car together; the boy is a small child, his head at the father's waist. " + ONLY2)),
    ("r02-farm", *scene(FARM, f"a poor family {WM}, a mother, a father and two children, wave hello in front of a wooden hut, each standing clearly apart. " + ANAT)),
    ("r03-ask", *hero("boy.jpg", BOY, "Setting: inside a car at sunset in thin white line art. ", f"{DAD} drives the car and asks a question, looking at the small boy, who sits in the passenger seat thinking. The boy is a small child. " + ONLY2)),
    ("r04-dogs", *hero("boy.jpg", BOY, FARM, "the small boy kneels on both knees and happily hugs four small white dogs around him.", alone=True)),
    ("r05-river", *scene(FARM, "a wide beautiful river flowing through green-less white line art fields, no pool, endless. No people.")),
    ("r06-food", *scene(FARM, f"a farmer {WM} picks vegetables in his own garden, a full basket beside him. Only one person. " + ANAT)),
    ("r07-dad", *scene("Setting: inside a car at sunset in thin white line art. ", f"chest-up shot: {DAD} sits speechless at the wheel, mouth open, surprised. Only one person. " + ANAT)),
    ("k1-boy", *hero("boy.jpg", BOY, "Setting: inside a car at sunset in thin white line art. ", "chest-up shot: the small boy smiles innocently and kindly, looking up.", alone=True)),
]

HILL = "Setting: a windy green hill in thin white line art, a lone tree, wide sky. "
GRAN = f"his grandmother {WM}, white hair in a bun, kind face"
R["words-feathers"] = [
    ("h0-feathers", *hero("boy.jpg", BOY, HILL, "the small boy stands on the hill holding an open white pillow, and hundreds of small white feathers fly out of it into the wind, scattering everywhere.", alone=True)),
    ("w01-shout", *hero("boy.jpg", BOY, "Setting: a schoolyard in thin white line art. ", "the small boy shouts angrily with his fists clenched at another small boy drawn all in WHITE, who looks hurt and sad. Two small children. " + ONLY2)),
    ("w02-sorry", *hero("boy.jpg", BOY, "Setting: a schoolyard in thin white line art. ", "the small boy holds out his hand apologising to another small boy drawn all in WHITE, who looks away silently with crossed arms. Two small children. " + ONLY2)),
    ("w03-pillow", *hero("boy.jpg", BOY, "Setting: a garden outside a house in thin white line art. ", f"{GRAN} hands a big white feather pillow to the small boy, who takes it with both hands. The boy is a small child. " + ONLY2)),
    ("w04-climb", *hero("boy.jpg", BOY, HILL, "the small boy climbs up the hill holding a big white pillow in both arms.", alone=True)),
    ("w05-wind", *scene(HILL, "hundreds of small white feathers blow away across the wide sky, far over fields and rooftops, scattering in every direction. No people.")),
    ("w06-search", *hero("boy.jpg", BOY, HILL, "the small boy runs across the hill trying to catch flying white feathers with both hands, frustrated, feathers everywhere out of reach.", alone=True)),
    ("w07-gran", *scene("Setting: a garden outside a house in thin white line art. ", f"chest-up shot: {GRAN.replace('his grandmother', 'an old grandmother')} smiles gently and wisely, one hand on her chest. Only one person. " + ANAT)),
    ("k1-think", *hero("boy.jpg", BOY, HILL.replace("Setting:", "Setting: at sunset,"), "the small boy sits on the hill at sunset holding one single white feather in his hand, looking at it thoughtfully.", alone=True)),
]

SAV = "Setting: an African savanna in thin white line art, tall grass, an acacia tree. "
LION = "a big lion drawn all in WHITE with a big white mane, NOT black-filled, NOT yellow"
MOUSE = "a tiny mouse drawn all in WHITE, NOT black-filled"
R["lion-mouse"] = [
    ("h0-chew", *scene(SAV, f"close-up: {MOUSE} chews through a thick rope of a net; behind the net, {LION} watches with hopeful eyes. No people.")),
    ("l01-sleep", *scene(SAV, f"{LION} sleeps under the acacia tree; {MOUSE} runs across its nose. No people.")),
    ("l02-catch", *scene(SAV, f"{LION} holds {MOUSE} by its tail under one huge paw, mouth open, ready to eat it. No people.")),
    ("l03-beg", *scene(SAV, f"close-up: {MOUSE} pleads with tiny paws pressed together, big teary eyes. No people.")),
    ("l04-laugh", *scene(SAV, f"{LION} laughs loudly, head thrown back, lifting its paw to let {MOUSE} run away. No people.")),
    ("l05-net", *scene(SAV, f"{LION} is trapped inside a big white rope net hanging from a tree, roaring, struggling. No people.")),
    ("l06-hunters", *scene(SAV, f"two hunters {WM} walk away in the distance, satisfied, each clearly apart. " + ANAT)),
    ("l07-free", *scene(SAV.replace("Setting:", "Setting: at sunset,"), f"{LION} steps out of a torn rope net, free; {MOUSE} sits proudly on its head. No people.")),
    ("k1-hero", *hero("man.jpg", MAN, SAV.replace("Setting:", "Setting: at sunset,"), f"the main character crouches and smiles warmly at {MOUSE} sitting on his open right palm, his left hand resting on his knee.", alone=True)),
]

ROAD = "Setting: a country road in thin white line art, fields, a few trees. "
CART = "a WHITE wooden cart pulled by a white horse"
FMR = f"an old farmer {WM}, white straw hat"
BAG = "a heavy white cloth bag"
R["bag-on-cart"] = [
    ("h0-ride", *hero("man.jpg", MAN, ROAD, f"the main character sits in the back of {CART}, still holding {BAG} on his right shoulder with both hands, sweating, tired.", alone=True)),
    ("b01-walk", *hero("man.jpg", MAN, ROAD, f"the main character walks along the road carrying {BAG} on his right shoulder with both hands, tired, sweating.", alone=True)),
    ("b02-offer", *hero("man.jpg", MAN, ROAD, f"{FMR} sits on the driver's seat of {CART} and waves to the main character standing on the road with {BAG} on his shoulder. The man in WHITE drives the cart. " + ONLY2)),
    ("b03-ask", *scene(ROAD, f"chest-up shot: {FMR} looks back over his shoulder, puzzled, one hand on the reins. Only one person. " + ANAT)),
    ("b04-answer", *hero("man.jpg", MAN, ROAD, f"chest-up shot: the main character, sitting in a cart, smiles politely, still holding {BAG} on his shoulder with both hands.", alone=True)),
    ("b05-laugh", *scene(ROAD, f"chest-up shot: {FMR} laughs heartily, head tilted back, one hand on his belly. Only one person. " + ANAT)),
    ("k1-down", *hero("man.jpg", MAN, ROAD.replace("Setting:", "Setting: at sunset,"), f"the main character sits relaxed in the back of {CART}, {BAG} set down beside him, both arms resting behind his head, enjoying the ride, a peaceful smile.", alone=True)),
]

STR = "Setting: a dusty roadside in a town in thin white line art. "
BEG = "the main character as a poor beggar, his yellow hoodie old and torn, holding a small bowl"
BOX = "an old WHITE wooden box"
STRANGER = f"a stranger {WM}, a long white coat"
R["busy-beggar"] = [
    ("h0-gold", *colored(STR, f"close-up: the lid of {BOX} is open and it is FULL of shining GOLD coins glowing. Only the gold has colour. No people.")),
    ("g01-beg", *hero("man.jpg", MAN, STR, f"{BEG}, sits on {BOX} by the road holding out the small bowl in both hands, sad.", alone=True)),
    ("g02-years", *hero("man.jpg", MAN, STR.replace("Setting:", "Setting: at night,"), f"{BEG}, sits on {BOX} by the empty road, tired, head down.", alone=True)),
    ("g03-stranger", *hero("man.jpg", MAN, STR, f"{STRANGER} stands and points at the box; {BEG} sits on {BOX} looking up at him. The man in WHITE stands; the man in yellow sits. " + ONLY2)),
    ("g04-shrug", *hero("man.jpg", MAN, STR, f"chest-up shot: {BEG} shrugs, both palms up, confused.", alone=True)),
    ("g05-open", *hero("man.jpg", MAN, STR, f"{BEG} kneels on both knees in front of {BOX} and pries the lid open with both hands, golden light shining out onto his face.", alone=True)),
    ("g06-shock", *hero("man.jpg", MAN, STR, "chest-up shot: the main character, a poor beggar in a torn yellow hoodie, stares in shock, both hands on his cheeks, golden light on his face.", alone=True)),
    ("k1-within", *hero("man.jpg", MAN, STR.replace("Setting:", "Setting: at sunrise,"), "the main character stands tall and calm, his right hand on his chest over his heart, his left hand at his side, a glowing golden light shining from his chest. " + STAND, alone=True)),
]

SNOW = "Setting: a snowy forest at night in thin white line art, falling snow. "
HOG = "small hedgehogs drawn all in WHITE with white spines, NOT black-filled"
R["hedgehogs-winter"] = [
    ("h0-ouch", *scene(SNOW, f"close-up: two {HOG} pressed together, both wincing 'ouch' as their sharp spines prick each other. No animals other than hedgehogs. No people.")),
    ("q01-cold", *scene(SNOW, f"a group of {HOG} shiver alone in the snow, scattered apart, cold. No people.")),
    ("q02-huddle", *scene(SNOW, f"a group of {HOG} huddle tightly together in a ball to stay warm. No people.")),
    ("q03-apart", *scene(SNOW, f"a group of {HOG} jump apart from each other, annoyed, rubbing where they got pricked. No people.")),
    ("q04-freeze", *scene(SNOW, f"a group of {HOG} sit far apart, shivering, covered in snow, icicles on their noses. No people.")),
    ("q05-balance", *scene(SNOW, f"a group of {HOG} sit in a circle at a small careful distance from each other, warm and comfortable, a soft glow between them. No people.")),
    ("q06-dawn", *scene(SNOW.replace("at night", "at sunrise"), f"a group of {HOG} sleep peacefully in a circle at a gentle distance in the morning sun. No people.")),
    ("k1-hero", *hero("man.jpg", MAN, "Setting: a cozy room with a fireplace in thin white line art. ", f"the main character sits by a warm fireplace beside a friend {WM}, sitting at a comfortable distance from each other, both smiling. The man in WHITE sits on the right. " + ONLY2)),
]

MTN = "Setting: a long mountain road in thin white line art. "
TEMPLE = "Setting: an old mountain temple in thin white line art, stone steps, a big bell. "
SEEK = "the main character as a traveller with a backpack"
OLDMONK = f"an old monk {WM} in a white robe, bald, kind wrinkled face"
R["search-within"] = [
    ("h0-mirror", *hero("man.jpg", MAN, TEMPLE, "close-up: the main character holds a small round WHITE hand mirror in both hands and looks into it, seeing his own face reflected, surprised.", alone=True)),
    ("s01-travel", *hero("man.jpg", MAN, MTN, f"{SEEK} walks along a long mountain road, tired, dusty.", alone=True)),
    ("s02-desert", *hero("man.jpg", MAN, "Setting: a vast desert of sand dunes in thin white line art. ", f"{SEEK} crosses huge sand dunes under a hot sun, determined.", alone=True)),
    ("s03-temples", *hero("man.jpg", MAN, TEMPLE, f"{SEEK} kneels on both knees praying on the temple steps, palms together.", alone=True)),
    ("s04-monk", *hero("man.jpg", MAN, TEMPLE, f"{OLDMONK} stands on the temple steps and speaks gently to {SEEK}, who stands below him. The man in WHITE is the monk. " + ONLY2)),
    ("s05-give", *hero("man.jpg", MAN, TEMPLE, f"{OLDMONK} hands a small round WHITE hand mirror to {SEEK}, who takes it with both hands, confused. " + ONLY2)),
    ("s06-smile", *scene(TEMPLE, f"chest-up shot: {OLDMONK} smiles wisely and warmly. Only one person. " + ANAT)),
    ("k1-within", *hero("man.jpg", MAN, TEMPLE.replace("Setting:", "Setting: at sunset,"), "the main character sits cross-legged on the temple steps at sunset with eyes closed, meditating peacefully, hands resting on his knees.", alone=True)),
]

if __name__ == "__main__":
    for n, (slug, jobs) in enumerate(R.items()):
        js = [{"out": f"img/cand/{o}-{k}.jpg", "refs": r, "seed": 20000 + 37 * n + 2 * i + (k == "b"), "prompt": p + WORLD}
              for i, (o, p, r) in enumerate(jobs) for k in "ab"]
        json.dump({"model": "black-forest-labs/flux.2-klein-4b", "size": "1152x2048", "workers": 2, "jobs": js},
                  open(f"{slug}/jobs.json", "w"), indent=1)
        print(slug, len(js))
