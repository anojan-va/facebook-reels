"""Image jobs for parable reels 81-90 (well-frog … four-oxen). Two candidates per shot. Writes <slug>/jobs.json.

Same conventions as jobs80.py: h0 = hook image, WORLD appended, roles spelled out per person."""
import json
from jobs25 import BOY, MONK, ONLY2, STAND, colored, hero
from jobs50 import WM, WORLD
from style_new import ANAT, MAN, OLD_MAN, scene

R = {}

WELL = "Setting: the inside of a deep round stone well in thin white line art, looking up at a small circle of sky. "
FROG = "a small frog drawn all in WHITE, NOT black-filled, NOT green"
TURTLE = "a big sea turtle drawn all in WHITE, NOT black-filled, NOT green"
R["well-frog"] = [
    ("h0-sky", *scene(WELL, f"{FROG} sits on a stone at the bottom of the deep well, looking up at the tiny circle of sky far above, small and alone. No people.")),
    ("w01-bottom", *scene(WELL, f"close-up: {FROG} sits proudly on a wet stone at the bottom of the well, chest out, content. No people.")),
    ("w02-circle", *scene(WELL, "view straight up from the bottom of the deep well: a tiny bright circle of sky with one small cloud, the round stone walls all around. No people.")),
    ("w03-turtle", *scene(WELL, f"{TURTLE} leans over the top edge of the well, looking down into it, curious; the tiny frog far below. No people.")),
    ("w04-ask", *scene(WELL, f"close-up: {FROG} looks up and calls out proudly, one little hand raised. No people.")),
    ("w05-ocean", *scene("Setting: a huge endless ocean in thin white line art, big waves, a wide horizon. ", f"{TURTLE} swims across the endless ocean, tiny against the huge waves stretching to the horizon. No people.")),
    ("w06-doubt", *scene(WELL, f"close-up: {FROG} crosses its arms and shakes its head, not believing. No people.")),
    ("k1-climb", *hero("man.jpg", MAN, "Setting: the top of a stone well on a hill at sunrise in thin white line art, a wide open world beyond. ", "the main character climbs out over the edge of a stone well and stands up, looking out at a wide open landscape at sunrise, amazed, arms open.", alone=True)),
]

RD = "Setting: a city road under a low concrete bridge in thin white line art, a long line of cars. "
TRUCK = "a big WHITE truck with a tall box trailer, white-filled with thin dark outlines"
ENG = f"three engineers {WM} with white hard hats"
GIRL = "a little girl about 7 years old drawn all in WHITE (white dress, white hair in pigtails)"
R["truck-bridge"] = [
    ("h0-stuck", *scene(RD, f"{TRUCK} is jammed tight under the low concrete bridge, its roof scraping the bridge, cracks in the concrete, cars backed up behind it. No people.")),
    ("t01-jam", *scene(RD, f"close-up: the roof of {TRUCK} pressed hard against the underside of the bridge, sparks and dust. No people.")),
    ("t02-traffic", *scene("Setting: a long city road in thin white line art. ", "a very long traffic jam of white cars stretching to the horizon, drivers honking, little white sound lines. No people visible.")),
    ("t03-engineers", *scene(RD, f"{ENG} stand beside the stuck truck arguing, one pointing at the bridge, one at the truck, one scratching his head, each clearly apart. " + ANAT)),
    ("t04-plans", *scene(RD, f"close-up: two of {ENG} hold up big white blueprint papers, frowning, confused. " + ANAT)),
    ("t05-girl", *scene(RD, f"{GIRL} leans out of a white car window and points at the truck's tyres, a bright idea on her face. Only one person. " + ANAT)),
    ("t06-quiet", *scene(RD, f"{ENG} stop and turn to look at the little girl, mouths open in surprise. " + ANAT)),
    ("t07-tyre", *scene(RD, "close-up: air hissing out of a big white truck tyre, little white air lines, the tyre slightly flatter. No people.")),
    ("t08-free", *scene(RD, f"{TRUCK} rolls free out from under the bridge, a small gap now between its roof and the bridge. No people.")),
    ("k1-hero", *hero("man.jpg", MAN, "Setting: a desk in a bright office in thin white line art. ", "the main character smiles with a simple bright idea, snapping his fingers with his right hand, his left hand on the desk.", alone=True)),
]

MTN = "Setting: a tiny wooden hut on a mountain at night in thin white line art, a big bright full moon, pine trees. "
OLDM = "The main character is an OLD Buddhist monk about 70 with short grey-white hair, a short grey-white beard and wrinkles, wearing a long mustard-yellow monk robe and sandals, drawn in clean anime line art with flat colours and a soft warm yellow glow. He is clearly OLD. "
THIEF = f"a thief {WM}, a white mask over his eyes"
R["ryokan-moon"] = [
    ("h0-moon", *hero("monk-old.jpg", OLDM, MTN, "the old monk sits peacefully outside his tiny hut looking up at the huge bright full moon, a gentle smile, hands resting on his knees.", alone=True)),
    ("r01-hut", *scene(MTN, "a tiny empty wooden hut alone on the mountain under the moon, almost nothing inside. No people.")),
    ("r02-thief", *scene(MTN, f"{THIEF} searches inside the tiny empty hut, finding nothing, frustrated, hands spread. Only one person. " + ANAT)),
    ("r03-home", *hero("monk-old.jpg", OLDM, MTN, f"the old monk stands in the doorway of his hut looking calmly at {THIEF}, who freezes in surprise. " + ONLY2)),
    ("r04-robe", *hero("monk-old.jpg", OLDM.replace("long mustard-yellow monk robe", "simple mustard-yellow under-robe"), MTN, f"the old monk holds out a folded white outer robe with both hands, offering it to {THIEF}, who stares at it confused. " + ONLY2)),
    ("r05-run", *scene(MTN, f"{THIEF} runs away down the mountain path clutching a folded robe, looking back confused. Only one person. " + ANAT)),
    ("r06-sit", *hero("monk-old.jpg", OLDM, MTN, "chest-up shot: the old monk looks up at the moon with a kind, slightly sad smile.", alone=True)),
    ("k1-moon", *scene(MTN, "a huge bright full moon over the mountains and the tiny hut, peaceful, glowing. No people.")),
]

HILL = "Setting: a country road over green-less white line art hills, a wide sky. "
WIND = "the wind drawn as a big puffy WHITE cloud face blowing hard with puffed cheeks"
SUN = "the sun drawn as a smiling face with soft glowing GOLDEN rays"
WALKER = f"a man {WM} wearing a long WHITE coat"
R["wind-sun"] = [
    ("h0-duel", *colored(HILL, f"in the sky, {WIND} on the left and {SUN} on the right face each other; far below, {WALKER} walks along the road. Only the sun has colour.")),
    ("s01-argue", *colored(HILL, f"close-up in the sky: {WIND} and {SUN} argue face to face. Only the sun has colour. No people.")),
    ("s02-walker", *scene(HILL, f"{WALKER} walks along the road calmly. Only one person. " + ANAT)),
    ("s03-blow", *scene(HILL, f"{WIND} blows a huge storm of swirling wind down at the road. No people.")),
    ("s04-hold", *scene(HILL, f"{WALKER} leans into a strong wind, holding his coat tightly closed with both hands, freezing, leaves flying. Only one person. " + ANAT)),
    ("s05-shine", *colored(HILL, f"{SUN} shines softly and warmly down on the road, golden rays. Only the sun has colour. No people.")),
    ("s06-warm", *colored(HILL, f"{WALKER} smiles in warm golden sunlight and wipes his forehead with one hand. Only the sunlight has colour. Only one person. " + ANAT)),
    ("s07-coat", *colored(HILL, f"{WALKER} takes off his white coat with both hands, smiling, in warm golden sunlight. Only the sunlight has colour. Only one person. " + ANAT)),
    ("k1-hero", *hero("man.jpg", MAN, "Setting: a park bench at sunset in thin white line art. ", f"the main character sits on a bench and gently puts his hand on the shoulder of a sad friend {WM} beside him, smiling warmly; the friend begins to smile. " + ONLY2)),
]

RIV = "Setting: a small wooden bridge over a calm river in thin white line art. "
DOG = "a dog drawn all in WHITE (white fur), NOT black-filled"
BONE = "a big WHITE bone"
R["dog-bone"] = [
    ("h0-drop", *scene(RIV, f"{DOG} stands on the bridge barking at the water, mouth wide open; {BONE} falls from its mouth toward the river with a splash. No people.")),
    ("d01-find", *scene("Setting: a village street in thin white line art. ", f"{DOG} happily picks up {BONE}, tail wagging. No people.")),
    ("d02-run", *scene("Setting: a village path in thin white line art. ", f"{DOG} trots happily along the path holding {BONE} in its mouth. No people.")),
    ("d03-bridge", *scene(RIV, f"{DOG} walks onto the bridge with {BONE} in its mouth. No people.")),
    ("d04-look", *scene(RIV, f"{DOG} on the bridge looks down at its reflection in the calm water: a dog holding a bone looks back up. No people.")),
    ("d05-want", *scene(RIV, f"close-up: {DOG} with {BONE} in its mouth stares greedily down at the water, eyes narrowed. No people.")),
    ("d06-sink", *scene(RIV, f"close-up: {BONE} sinking down into the river water, ripples above. No people.")),
    ("d07-empty", *scene(RIV, f"{DOG} stands on the bridge with an empty mouth, ears down, sad, looking at ripples in the water. No people.")),
    ("k1-hero", *hero("man.jpg", MAN, "Setting: a cozy small home in thin white line art, a table with a simple meal. ", "the main character sits at a small table smiling gratefully at a simple bowl of food, hands together, content.", alone=True)),
]

FARM = "Setting: a small poor farmyard in thin white line art, a wooden barn, a straw nest. "
GOOSE = "a goose drawn all in WHITE, NOT black-filled"
EGG = "a shining GOLDEN egg"
FARMER = "the main character as a poor farmer, his yellow hoodie old and patched"
R["golden-goose"] = [
    ("h0-egg", *colored(FARM, f"close-up: {EGG} glowing in a straw nest beside {GOOSE}. Only the egg has colour. No people.")),
    ("g01-goose", *scene(FARM, f"{GOOSE} sits calmly on a straw nest. No people.")),
    ("g02-find", *hero("man.jpg", MAN, FARM, f"{FARMER} kneels by the nest and holds up {EGG} in both hands, amazed, golden light on his face.", alone=True)),
    ("g03-rich", *colored("Setting: a nice house in thin white line art. ", "a growing pile of shining GOLDEN eggs on a table in a nicer house. Only the eggs have colour. No people.")),
    ("g04-greedy", *hero("man.jpg", MAN, FARM.replace("Setting:", "Setting: at night,"), f"chest-up shot: {FARMER} rubs his hands together with a greedy grin, eyes narrowed, staring at the goose.", alone=True)),
    ("g05-knife", *hero("man.jpg", MAN, FARM.replace("Setting:", "Setting: at night,"), f"{FARMER} reaches toward the sleeping goose in the nest with a dark greedy look, a small knife in his right hand. The goose is unharmed.", alone=True)),
    ("g06-nothing", *hero("man.jpg", MAN, FARM.replace("Setting:", "Setting: at dawn,"), f"{FARMER} kneels by an empty straw nest with only white feathers scattered in it, both hands on his head, horrified.", alone=True)),
    ("k1-patient", *hero("man.jpg", MAN, "Setting: a garden at sunrise in thin white line art. ", "the main character kneels and calmly waters a small young tree with a watering can, a patient peaceful smile.", alone=True)),
]

HALL = "Setting: inside a mouse hole under a house in thin white line art, a meeting hall made of books and spools. "
MICE = "mice drawn all in WHITE, NOT black-filled"
CAT = "a big cat drawn all in WHITE (white fur), NOT black-filled, sharp eyes"
R["bell-cat"] = [
    ("h0-bell", *colored(HALL, f"close-up: a small shining GOLDEN bell on a red ribbon lies in the middle of a circle of worried {MICE}, all staring at it. Only the bell has colour. No people.")),
    ("b01-cat", *scene("Setting: a kitchen floor in thin white line art. ", f"{CAT} chases small {MICE} across the kitchen floor, the mice running in fear. No people.")),
    ("b02-meeting", *scene(HALL, f"a big meeting of {MICE} sitting in rows, one mouse on a spool like a stage. No people.")),
    ("b03-idea", *colored(HALL, f"a young mouse drawn all in WHITE stands on a spool and proudly holds up a small GOLDEN bell, explaining. Only the bell has colour. No people.")),
    ("b04-cheer", *scene(HALL, f"many {MICE} cheer and clap, throwing their arms up happily. No people.")),
    ("b05-old", *scene(HALL, f"close-up: an old grey-whiskered mouse drawn all in WHITE with a walking stick raises one finger, asking a quiet question. No people.")),
    ("b06-silence", *scene(HALL, f"all the {MICE} sit frozen in silence, looking away nervously, nobody moving. No people.")),
    ("k1-hero", *colored("Setting: a street at sunrise in thin white line art. ", "the main character in his mustard-YELLOW hoodie, black cargo pants and white sneakers, short brown beard, steps forward confidently with one hand raised, volunteering, a brave determined face. Only the main character has colour.")),
]

HOME = "Setting: a simple village home in thin white line art, a fireplace. "
FATHER = "The main character is an OLD man about 70 with short grey-white hair, a short neat grey-white beard and wrinkles, wearing a mustard-yellow hoodie, black cargo pants and white sneakers, drawn in clean anime line art with flat colours and a soft warm yellow glow. He is clearly OLD. "
SONS = f"three grown sons {WM}"
R["bundle-sticks"] = [
    ("h0-strain", *scene(HOME, f"a strong young man {WM} strains with all his might to break a thick bundle of sticks tied with rope across his knee, but it won't break. Only one person. " + ANAT)),
    ("s01-fight", *scene(HOME, f"{SONS} argue loudly and point at each other angrily, each standing clearly apart. " + ANAT)),
    ("s02-give", *hero("man-old.jpg", FATHER, HOME, f"the old father hands a single thin stick to each of {SONS}, who stand in front of him. Exactly four people, each clearly apart.")),
    ("s03-snap", *scene(HOME, f"close-up: two hands snap a single thin stick in half easily. " + ANAT)),
    ("s04-bundle", *hero("man-old.jpg", FATHER, HOME, "the old father ties many sticks together into a bundle with a rope, both hands working, a wise calm face.", alone=True)),
    ("s05-try", *scene(HOME, f"{SONS} take turns trying to break the bundle of sticks, straining, failing, each clearly apart. " + ANAT)),
    ("s06-father", *hero("man-old.jpg", FATHER, HOME, "chest-up shot: the old father speaks with a kind wise smile, holding the unbroken bundle of sticks in both hands.", alone=True)),
    ("k1-hug", *scene(HOME.replace("Setting:", "Setting: in warm firelight,"), f"{SONS} put their arms around each other's shoulders, smiling, together. " + ANAT)),
]

TREE = "Setting: a forest clearing in thin white line art, a tall tree with a branch. "
CROW = "a crow drawn all in WHITE (white feathers), NOT black-filled"
FOX = "a fox drawn all in WHITE (white fur), NOT black-filled, NOT orange"
CHEESE = "a piece of YELLOW cheese"
R["fox-crow-cheese"] = [
    ("h0-fall", *colored(TREE, f"{CROW} on a branch opens its beak wide to sing, and {CHEESE} falls straight down toward {FOX} waiting below with open jaws. Only the cheese has colour. No people.")),
    ("f01-crow", *colored(TREE, f"{CROW} sits proudly on a high branch holding {CHEESE} in its beak. Only the cheese has colour. No people.")),
    ("f02-fox", *colored(TREE, f"{FOX} looks up hungrily at the crow with the cheese, licking its lips. Only the cheese has colour. No people.")),
    ("f03-praise", *colored(TREE, f"{FOX} smiles sweetly up at the crow, paws pressed together, flattering it. Only the cheese has colour. No people.")),
    ("f04-proud", *colored(TREE, f"close-up: {CROW} puffs up its chest proudly, eyes closed, {CHEESE} in its beak. Only the cheese has colour. No people.")),
    ("f05-catch", *colored(TREE, f"{FOX} catches {CHEESE} in its mouth and runs away laughing. Only the cheese has colour. No people.")),
    ("f06-sad", *scene(TREE, f"{CROW} sits on the branch with an empty beak, shocked and embarrassed. No people.")),
    ("k1-hero", *hero("man.jpg", MAN, "Setting: an office hallway in thin white line art. ", f"the main character listens to a smiling man {WM} who praises him with both hands spread; the main character raises one eyebrow, calm and wise, one hand on his chin. " + ONLY2)),
]

FLD = "Setting: a wide grassy field in thin white line art, a few trees, hills. "
OX = "oxen drawn all in WHITE with white horns, NOT black-filled, NOT brown"
LION = "a lion drawn all in WHITE with a big white mane, NOT black-filled, NOT yellow"
R["four-oxen"] = [
    ("h0-circle", *scene(FLD, f"four {OX} stand back to back in a tight circle, horns facing out; {LION} prowls around them, unable to attack. No people.")),
    ("o01-field", *scene(FLD, f"four {OX} graze peacefully together in the field. No people.")),
    ("o02-lion", *scene(FLD, f"{LION} hides in the tall grass, watching the oxen hungrily. No people.")),
    ("o03-whisper", *scene(FLD, f"{LION} whispers sneakily into the ear of one ox. No people.")),
    ("o04-argue", *scene(FLD, f"four {OX} argue, glaring at each other angrily, turning their backs. No people.")),
    ("o05-alone", *scene(FLD, f"wide view: four {OX} graze alone, each in a different far corner of the field, far apart. No people.")),
    ("o06-hunt", *scene(FLD.replace("Setting:", "Setting: at dusk,"), f"{LION} stalks toward one lonely ox standing alone in the corner of the field. No people.")),
    ("k1-hero", *hero("man.jpg", MAN, "Setting: a hilltop at sunset in thin white line art. ", f"the main character stands with three friends {WM}, all with arms around each other's shoulders, smiling, facing the sunset. Exactly four people, standing side by side.")),
]

if __name__ == "__main__":
    for n, (slug, jobs) in enumerate(R.items()):
        js = [{"out": f"img/cand/{o}-{k}.jpg", "refs": r, "seed": 28000 + 37 * n + 2 * i + (k == "b"), "prompt": p + WORLD}
              for i, (o, p, r) in enumerate(jobs) for k in "ab"]
        json.dump({"model": "black-forest-labs/flux.2-klein-4b", "size": "1152x2048", "workers": 2, "jobs": js},
                  open(f"{slug}/jobs.json", "w"), indent=1)
        print(slug, len(js))
