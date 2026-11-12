"""Image jobs for parable reels 31-40 (sharp-axe … farmer-treasure). Two candidates per shot. Writes <slug>/jobs.json.

Shot h0 of every reel is the hook image: the most striking picture of the story, shown with the opening line."""
import json
from jobs25 import ALONE, BOY, MONK, ONLY2, STAND, colored, hero
from style_new import ANAT, MAN, PEOPLE, scene

R = {}
OLDW = "an old man drawn all in WHITE (white hair, long white beard, white robe), NOT coloured, NOT black-filled"

F = "Setting: a pine forest in daylight in thin white line art, tall trees, tree stumps, a few cut logs. "
BOSS = "his boss, a big man drawn all in WHITE (white shirt, white trousers, short white hair), NOT coloured"
R["sharp-axe"] = [
    ("h0-tired", *hero("man.jpg", MAN, F, "the main character, a woodcutter, leans exhausted on the handle of his axe with BOTH hands on top of the handle, the axe head on the ground, sweat dripping, panting, a huge uncut tree behind him.", alone=True)),
    ("f01-hire", *hero("man.jpg", MAN, F, f"the main character holds a new axe across his chest with both hands, eager smile; {BOSS} stands beside him pointing at the forest with one hand, his other hand at his side. " + ONLY2)),
    ("f02-pile", *hero("man.jpg", MAN, F, "the main character stands proudly beside a big pile of eighteen cut logs, his right hand holding the axe resting on his right shoulder, his left hand on his hip. " + STAND, alone=True)),
    ("f03-amazed", *scene(F, f"{BOSS} stands beside a big pile of cut logs, amazed, eyes wide, both hands raised in surprise. Only one person. " + ANAT)),
    ("f04-harder", *hero("man.jpg", MAN, F, "the main character swings the axe hard into a thick tree trunk with BOTH hands gripping the handle, gritted teeth, sweat flying, side view, wood chips.", alone=True)),
    ("f05-stump", *hero("man.jpg", MAN, F, "the main character sits on a tree stump exhausted, head down, both hands resting on his knees, a tiny pile of only five logs beside him, the axe leaning against the stump.", alone=True)),
    ("f06-hands", *hero("man.jpg", MAN, F, "chest-up shot: the main character looks down at his own two open palms held in front of him, worried and confused.", alone=True)),
    ("f07-blade", *hero("man.jpg", MAN, F, f"{BOSS} holds the main character's old axe up with both hands and points his chin at its dull chipped blade; the main character stands facing him, listening, both hands at his sides. " + ONLY2)),
    ("f08-shrug", *hero("man.jpg", MAN, F, "chest-up shot: the main character shrugs with both palms turned up at shoulder height, a tired, stressed face.", alone=True)),
    ("f09-sharpen", *hero("man.jpg", MAN, F, "the main character sits calmly on a log sharpening his axe: he holds the axe with both hands and presses the blade against a round grinding stone on a small wooden stand, sparks flying, focused and relaxed.", alone=True)),
    ("k1-rest", *hero("man.jpg", MAN, F.replace("in daylight", "at sunset"), "the main character sits relaxed with his back against a tree at sunset, eyes closed, a peaceful smile, both hands resting on his lap, his shiny sharp axe leaning against the tree beside him.", alone=True)),
    ("k2-strong", *hero("man.jpg", MAN, F.replace("in daylight", "at sunrise"), "the main character stands beside a huge pile of cut logs at sunrise, his gleaming sharp axe resting on his right shoulder in his right hand, left hand at his side, a confident smile. " + STAND, alone=True)),
]

BARN = "Setting: inside a huge old wooden barn in thin white line art, tall piles of hay, wooden beams, a big open door with light coming in. "
FARMER = "an old farmer drawn all in WHITE (white straw hat, white shirt, white overalls), NOT coloured"
KIDS = "children drawn all in WHITE (white clothes), NOT coloured, NOT black-filled"
R["lost-watch"] = [
    ("h0-silent", *hero("boy.jpg", BOY, BARN, "the boy sits cross-legged alone on the hay in the quiet dark barn, eyes closed, listening carefully, both hands resting on his knees, a single beam of light falling on him.", alone=True)),
    ("g01-lost", *scene(BARN, f"{FARMER} searches through the hay with both hands, worried face, the huge barn around him. Only one person. " + ANAT)),
    ("g02-reward", *scene(BARN, f"{FARMER} holds up one shiny coin in his right hand, his left hand at his side; five {KIDS} stand around him excitedly, each standing clearly apart. " + ANAT)),
    ("g03-chaos", *scene(BARN, f"five {KIDS} run around the barn shouting, throwing hay in the air, digging in the haystacks, chaos, each clearly apart. " + ANAT)),
    ("g04-giveup", *scene(BARN.replace("with light coming in", "with sunset light"), f"four {KIDS} walk out through the big barn door, tired and sad, heads down, seen from behind. " + ANAT)),
    ("g05-ask", *hero("boy.jpg", BOY, BARN, f"the small boy stands in front of {FARMER} and looks up at him, holding up one finger asking for one more chance; the farmer is a tall adult looking down at the small child. " + ONLY2)),
    ("g06-listen", *hero("boy.jpg", BOY, BARN, "close-up from the chest up: the boy, eyes closed, tilts his head and cups his right hand behind his right ear, listening; his left hand rests on his knee.", alone=True)),
    ("g07-watch", *scene(BARN, "close-up: a shiny silver pocket watch half hidden in the hay, small white sound lines glowing around it like ticking. No people.")),
    ("g08-found", *hero("boy.jpg", BOY, BARN, "the boy kneels on both knees in the hay and holds up a shiny silver pocket watch with both hands, a big proud smile.", alone=True)),
    ("k1-give", *hero("boy.jpg", BOY, BARN, f"the small boy hands the silver pocket watch up to {FARMER}, who smiles warmly and pats the boy's head with one hand while taking the watch with the other. " + ONLY2)),
    ("k2-calm", *hero("boy.jpg", BOY, BARN.replace("with light coming in", "with warm sunset light"), "the boy sits peacefully on a hay bale near the big open door at sunset, eyes closed, a calm smile, both hands on his knees.", alone=True)),
]

TEMPLE = "Setting: an old Asian temple courtyard in thin white line art, stone floor, a curved temple roof, trees. "
MONKS = "monks drawn all in WHITE (white robes, shaved heads), NOT coloured, NOT black-filled"
CLAY = "a giant seated Buddha statue completely covered in thick dull rough clay, drawn in white line art with a cracked rough texture"
R["golden-buddha"] = [
    ("h0-crack", *colored(TEMPLE, "big close-up of the face of a giant clay Buddha statue, rough dull clay drawn in white line art, with a deep crack across the cheek through which bright shining GOLD glows. Only the gold has colour. No people.")),
    ("j01-gold", *colored(TEMPLE, f"a giant seated Buddha statue made of shining GOLD in the courtyard; small {MONKS} kneel and bow at its base, each clearly apart. Only the statue is golden. " + ANAT)),
    ("j02-cover", *colored(TEMPLE.replace("Setting:", "Setting: at night,"), f"{MONKS} stand on wooden ladders and spread thick white clay over the giant golden statue with their hands, half of the gold already covered. Only the remaining gold has colour. " + ANAT)),
    ("j03-army", *scene(TEMPLE, f"a line of soldiers drawn all in WHITE with white helmets and spears march past {CLAY}, not even looking at it. " + ANAT)),
    ("j04-years", *scene(TEMPLE.replace("Setting:", "Setting: at night under the moon,"), f"{CLAY} sits alone, overgrown with vines and moss, dead leaves around it, forgotten. No people.")),
    ("j05-notice", *hero("monk.jpg", MONK, TEMPLE, f"the young monk holds a broom in his left hand and leans closer to {CLAY}, looking curiously at a small crack in it, his right hand touching the clay near the crack.", alone=True)),
    ("j06-glint", *colored(TEMPLE, "extreme close-up of a small crack in rough white clay with a bright sparkling glint of GOLD shining through it, light rays. Only the gold has colour. No people.")),
    ("j07-chip", *hero("monk.jpg", MONK, TEMPLE, "the young monk stands on a wooden ladder against the giant statue and chips away the white clay with a small chisel in his left hand and a hammer in his right hand; pieces of clay fall straight down; shining GOLD shows underneath where the clay is gone.", alone=True)),
    ("j08-shine", *hero("monk.jpg", MONK, TEMPLE, "the giant Buddha statue now shines completely GOLD with rays of light; the young monk stands small at its base looking up in awe, both hands at his sides. " + STAND, alone=True)),
    ("k1-face", *hero("monk.jpg", MONK, TEMPLE, "chest-up shot: the young monk smiles peacefully with warm golden light on his face, eyes gently closed, palms pressed together in front of his chest.", alone=True)),
    ("k2-walk", *hero("monk.jpg", MONK, TEMPLE.replace("Setting:", "Setting: at sunset,"), "the young monk walks calmly toward the viewer across the courtyard, the giant shining golden statue glowing behind him, both arms relaxed at his sides.", alone=True)),
]

STAGE = "Setting: a lecture hall stage in thin white line art, a spotlight, rows of seats with an audience. "
AUD = "an audience drawn all in WHITE (white clothes), NOT coloured, NOT black-filled"
BILL = "a crisp GREEN 20 dollar bill"
R["twenty-dollar"] = [
    ("h0-hold", *hero("man.jpg", MAN, STAGE, f"chest-up shot under a spotlight: the main character holds up {BILL} in his right hand at face height and looks straight at the viewer with an intense knowing look; his left hand at his side. The only other colour is the green bill.", alone=True)),
    ("t01-stage", *hero("man.jpg", MAN, STAGE, f"the main character stands on the stage under a spotlight holding {BILL} high in his raised right hand, left hand at his side; {AUD} sits in rows in the foreground seen from behind. The only other colour is the green bill.")),
    ("t02-hands", *scene(STAGE, f"view from the stage: {AUD} sits in rows of seats and every person raises one hand high, eager faces. " + ANAT)),
    ("t03-crumple", *hero("man.jpg", MAN, STAGE, "chest-up shot: the main character crumples a green 20 dollar bill into a tight ball between both of his hands, a calm face. The only other colour is the green bill.", alone=True)),
    ("t04-step", *hero("man.jpg", MAN, STAGE, "full body side view: on the stage floor lies a crumpled green 20 dollar bill and the main character steps on it with his right sneaker, his arms relaxed at his sides. The only other colour is the green bill.", alone=True)),
    ("t05-dirty", *hero("man.jpg", MAN, STAGE, "the main character holds up a dirty, wrinkled, stepped-on green 20 dollar bill in his raised right hand, left hand at his side, under the spotlight. The only other colour is the green bill. " + STAND, alone=True)),
    ("t06-value", *hero("man.jpg", MAN, STAGE, "chest-up shot: the main character smiles warmly and points straight at the viewer with his right index finger; his left hand holds the wrinkled green bill at his side. The only other colour is the green bill.", alone=True)),
    ("t07-crushed", *hero("man.jpg", MAN, "Setting: a dark empty room in thin white line art, rain on a window. ", "the main character sits on the floor against the wall, knees up, arms resting on his knees, head down, sad and broken.", alone=True)),
    ("k1-rise", *hero("man.jpg", MAN, "Setting: a dark empty room in thin white line art, rain on a window. ", "the main character stands up tall, chin up, a calm confident smile, his right hand on his chest, his left hand at his side. " + STAND, alone=True)),
    ("k2-light", *hero("man.jpg", MAN, "Setting: an open doorway with bright morning sunlight pouring in, thin white line art. ", "the main character walks out through the open doorway into the bright sunlight, confident, both arms relaxed at his sides.", alone=True)),
]

CLASS = "Setting: a university classroom in thin white line art, a big chalkboard, a wooden teacher's table. "
STUD = "adult university students drawn all in WHITE (white clothes), NOT coloured, NOT black-filled, sitting at desks"
JAR = "a big clear glass jar on the teacher's table"
R["jar-rocks"] = [
    ("h0-wrong", *scene(CLASS, f"close-up: {JAR} filled to the top with sand only, and five big rocks lying outside the jar that cannot fit in. No people.")),
    ("r01-rocks", *hero("man.jpg", MAN, CLASS, f"the main character, a professor, stands behind the teacher's table and places a big rock into {JAR} with both hands; several {STUD} in the foreground watch him, seen from behind. He stands, they sit, nobody near him.")),
    ("r02-yes", *scene(CLASS, f"several {STUD} nod, two of them raise one hand, answering yes, each clearly apart. " + ANAT)),
    ("r03-pebbles", *hero("man.jpg", MAN, CLASS, f"the main character holds a small bucket with both hands and pours small pebbles into {JAR} full of big rocks; the pebbles fall straight down and roll between the rocks.", alone=True)),
    ("r04-sand", *hero("man.jpg", MAN, CLASS, f"the main character holds a small bucket with both hands and pours fine sand into {JAR} full of rocks and pebbles; the sand pours straight down and fills every gap.", alone=True)),
    ("r05-full", *scene(CLASS, f"close-up: {JAR} with big rocks, small pebbles between them and sand filling every gap, perfectly full. No people.")),
    ("r06-point", *hero("man.jpg", MAN, CLASS, f"the main character points at {JAR} full of rocks, pebbles and sand with his right hand, his left hand at his side, a wise smile, looking at the viewer.", alone=True)),
    ("k1-first", *hero("man.jpg", MAN, CLASS.replace("in thin", "in warm evening light in thin"), "the main character gently places one big rock into an EMPTY clear glass jar on the table with both hands, a calm smile.", alone=True)),
    ("k2-done", *hero("man.jpg", MAN, CLASS.replace("in thin", "in warm evening light in thin"), f"the main character stands beside {JAR} that is full of rocks, pebbles and sand, a satisfied smile, both hands at his sides. " + STAND, alone=True)),
]

JUN = "Setting: a jungle in thin white line art, big leaves, vines, a tall tree. "
MONKEY = "a monkey drawn all in WHITE (white fur), NOT black-filled"
HUNT = "two hunters drawn all in WHITE (white clothes, white hats), NOT coloured"
NJAR = "a clay jar with a very narrow neck"
R["monkey-jar"] = [
    ("h0-stuck", *scene(JUN, f"{MONKEY} sits on the ground with one arm deep inside {NJAR}, pulling hard, screaming with its mouth wide open, panicked. No people.")),
    ("m01-set", *scene(JUN, f"{HUNT} crouch and place {NJAR} at the foot of a tree, one of them puts a banana inside, each clearly apart. " + ANAT)),
    ("m02-banana", *colored(JUN, f"close-up: {NJAR} at the foot of a tree with a YELLOW banana visible inside its narrow neck. Only the banana has colour. No people.")),
    ("m03-reach", *scene(JUN, f"{MONKEY} reaches one arm into the narrow neck of {NJAR}, curious and greedy. No people.")),
    ("m04-hunters", *scene(JUN, f"{HUNT} walk closer through the jungle holding a net between them, sneaking, each clearly apart. " + ANAT)),
    ("m05-scream", *scene(JUN, f"{MONKEY} screams in fear, its hand still stuck inside {NJAR}; in the background {HUNT} come closer with a net. " + ANAT)),
    ("m06-free", *scene(JUN, f"{MONKEY} opens its hand and slides its empty open hand easily out of {NJAR}, the banana left inside, surprised. No people.")),
    ("k0-hold", *hero("man.jpg", MAN, "Setting: a dark empty room in thin white line art. ", "the main character clutches a heavy old box tightly against his chest with both arms, tense, worried, eyes squeezed shut.", alone=True)),
    ("k1-open", *hero("man.jpg", MAN, "Setting: a hilltop at sunrise in thin white line art, wide sky. ", "the main character stands with both arms open wide and both palms open, releasing a flock of small glowing white birds into the sky, a free and relieved smile. " + STAND, alone=True)),
]

TREE = "Setting: a quiet garden in thin white line art, a big old tree, a stone bench. "
LAKE = "Setting: the shore of a wide calm lake at sunset in thin white line art, gentle waves, distant hills. "
R["salt-lake"] = [
    ("h0-sad", *hero("man.jpg", MAN, TREE, "chest-up shot: the main character holds a glass of cloudy water in his right hand, a pained, unhappy face, eyes heavy; his left hand at his side.", alone=True)),
    ("s01-visit", *hero("man.jpg", MAN, TREE, f"the main character walks sadly toward {OLDW}, who sits calmly on the stone bench under the big tree. " + ONLY2)),
    ("s02-salt", *hero("man.jpg", MAN, TREE, f"the main character holds a glass of water in his left hand and drops a handful of white salt into it from his right hand; the salt falls straight down into the glass; {OLDW} sits on the bench watching. " + ONLY2)),
    ("s03-drink", *hero("man.jpg", MAN, TREE, "chest-up shot: the main character drinks from the glass in his right hand and grimaces at the terrible salty taste, eyes squeezed shut, tongue out; his left hand at his side.", alone=True)),
    ("s04-walk", *hero("man.jpg", MAN, LAKE, f"the main character and {OLDW} walk side by side toward the wide lake, seen from behind. " + ONLY2)),
    ("s05-throw", *hero("man.jpg", MAN, LAKE, "the main character throws a handful of salt into the lake with his right arm stretched out, his left arm at his side, salt scattering over the water.", alone=True)),
    ("s06-sip", *hero("man.jpg", MAN, LAKE, "the main character kneels on both knees at the edge of the lake and drinks water from his two cupped hands, refreshed, eyes closed.", alone=True)),
    ("s07-master", *scene(LAKE, f"{OLDW} stands by the lake and smiles wisely, his right hand raised as he explains, his left hand holding a wooden walking stick. Only one person. " + ANAT)),
    ("k1-lake", *hero("man.jpg", MAN, LAKE, "the main character stands at the lake shore looking out over the vast calm water, a calm peaceful smile, both hands at his sides. " + STAND, alone=True)),
    ("k2-peace", *hero("man.jpg", MAN, LAKE, "the main character sits on the sand by the lake with his eyes closed and a peaceful smile, both hands resting on his knees, the sunset reflecting on the water.", alone=True)),
]

KIT = "Setting: a kitchen stove in thin white line art. "
FROG = "a frog drawn all in WHITE (white skin), NOT black-filled, NOT green"
POT = "a big white cooking pot of water on the stove"
OFF = "Setting: a dull grey office at night in thin white line art, a desk, piles of papers, a wall clock. "
R["frog-boil"] = [
    ("h0-desk", *hero("man.jpg", MAN, OFF, "the main character sits slumped at his desk at night, exhausted and empty, his chin resting in his right hand, his left hand on a pile of papers, staring blankly; the wall clock shows late.", alone=True)),
    ("p01-jump", *scene(KIT, f"{FROG} leaps high out of {POT} that is boiling hard with big bubbles and steam, a big splash. No people.")),
    ("p02-cool", *scene(KIT, f"{FROG} floats calmly in {POT} of cool still water, a tiny flame under the pot. No people.")),
    ("p03-comfy", *scene(KIT, f"{FROG} relaxes in {POT} like in a warm bath, eyes half closed, smiling, a little steam rising. No people.")),
    ("p04-hotter", *scene(KIT, f"{FROG} sits in {POT} with lots of steam rising and a bigger flame under it, sweating, but still staying. No people.")),
    ("p05-weak", *scene(KIT, f"{FROG} lies weak and limp in {POT} full of thick steam and bubbles, eyes drooping, too tired to move. No people.")),
    ("p06-habit", *hero("man.jpg", MAN, "Setting: a dark living room at night in thin white line art, a sofa, a TV. ", "the main character lies slumped on the sofa at night, holding a glowing phone with both hands, tired red eyes, snacks around him.", alone=True)),
    ("p07-couple", *hero("man.jpg", MAN, "Setting: a park bench at dusk in thin white line art. ", "the main character sits at one end of a bench looking down, sad; a woman drawn all in WHITE sits at the far other end with her arms crossed, turned away from him. " + ONLY2)),
    ("k1-leave", *hero("man.jpg", MAN, "Setting: an open door with bright sunlight pouring in, thin white line art. ", "the main character steps out through the open door into the bright sunlight with a determined face, both arms swinging naturally.", alone=True)),
    ("k2-free", *hero("man.jpg", MAN, "Setting: a green hill at sunrise in thin white line art, wide open sky. ", "the main character stands on the hill at sunrise breathing in deeply, eyes closed, a free smile, both arms relaxed at his sides. " + STAND, alone=True)),
]

ROOM = "Setting: a university classroom in thin white line art, a chalkboard, a table with a pile of potatoes and empty bags. "
TEACH = "a teacher drawn all in WHITE (an older woman with white hair in a bun, white clothes), NOT coloured"
SACK = "a white cloth sack bulging with potatoes"
R["potato-grudge"] = [
    ("h0-sack", *hero("man.jpg", MAN, "Setting: a city street in thin white line art. ", f"the main character walks bent forward under the weight of {SACK} carried over his right shoulder, holding it with both hands, exhausted, sweating.", alone=True)),
    ("q01-bags", *hero("man.jpg", MAN, ROOM, f"{TEACH} stands at the table and hands an empty cloth bag to the main character, who stands in front of her and takes it with both hands. " + ONLY2)),
    ("q02-write", *hero("man.jpg", MAN, ROOM, "chest-up shot: the main character holds a potato in his left hand and writes a name on it with a black marker in his right hand, an angry frown.", alone=True)),
    ("q03-lift", *hero("man.jpg", MAN, ROOM, f"the main character lifts {SACK} off the table with both hands, straining, it is very heavy.", alone=True)),
    ("q04-street", *hero("man.jpg", MAN, "Setting: a busy city street in thin white line art. ", f"the main character walks down the street carrying {SACK} over his right shoulder with both hands, tired; people drawn all in WHITE walk by in the background, clearly apart. " + ANAT)),
    ("q05-bed", *hero("man.jpg", MAN, "Setting: a small bedroom at night in thin white line art. ", f"the main character sits on the edge of his bed with both feet on the floor, exhausted, head down, both hands on his knees, {SACK} on the floor beside him.", alone=True)),
    ("q06-rot", *scene(ROOM, f"close-up: {SACK} open on the floor, the potatoes inside rotting and sprouting, wavy stink lines rising. No people.")),
    ("q07-teacher", *scene(ROOM, f"{TEACH} stands by the chalkboard and explains with a kind wise smile, her right hand raised, her left hand at her side. Only one person. " + ANAT)),
    ("k1-down", *hero("man.jpg", MAN, "Setting: a city street at sunrise in thin white line art. ", f"the main character sets {SACK} down on the ground with both hands and straightens up, a deep relieved breath, a light smile.", alone=True)),
    ("k2-free", *hero("man.jpg", MAN, "Setting: a city street at sunrise in thin white line art. ", "the main character walks away lightly with a free happy smile, both arms swinging, the sack left behind on the ground far behind him.", alone=True)),
]

FIELD = "Setting: a wide farm field in thin white line art, a small farmhouse, a fence. "
BRO = "his brother drawn all in WHITE (white shirt, white trousers, short white hair), NOT coloured"
R["farmer-treasure"] = [
    ("h0-dig", *hero("man.jpg", MAN, FIELD.replace("Setting:", "Setting: at dusk,"), "the main character digs a deep hole with a shovel, both hands on the handle, his foot on the blade, sweaty and desperate, holes everywhere around him.", alone=True)),
    ("v01-bed", *hero("man.jpg", MAN, "Setting: a small farmhouse bedroom in thin white line art, a candle. ", f"top-down view: {OLDW} lies in bed with a blanket up to his shoulders, whispering; the main character kneels on both knees beside the bed, listening closely. " + ONLY2)),
    ("v02-dig2", *hero("man.jpg", MAN, FIELD, f"the main character and {BRO} dig the field with shovels, each with both hands on his own shovel, standing clearly apart. " + ONLY2)),
    ("v03-holes", *scene(FIELD, "wide view from above: the whole field is dug up with holes and mounds of soil everywhere, every corner. No people.")),
    ("v04-nothing", *hero("man.jpg", MAN, FIELD.replace("Setting:", "Setting: at sunset,"), "the main character sits on a mound of soil next to an empty hole, exhausted and angry, his shovel lying on the ground beside him, both hands on his knees.", alone=True)),
    ("v05-sow", *hero("man.jpg", MAN, FIELD, "the main character walks across the turned soil scattering seeds with his right hand, his left hand holding a seed bag at his hip.", alone=True)),
    ("v06-wheat", *colored(FIELD, "the whole field is full of tall ripe GOLDEN wheat swaying in the wind, a village in the distance. Only the wheat is golden. No people.")),
    ("v07-market", *hero("man.jpg", MAN, "Setting: a village market in thin white line art, stalls, sacks of grain. ", f"the main character and {BRO} stand beside a tall stack of grain sacks, the main character holds up a heavy bag of coins in his right hand, both smiling. " + ONLY2)),
    ("k1-wheat", *hero("man.jpg", MAN, FIELD, "the main character holds a big bundle of golden wheat in both arms against his chest, a warm understanding smile. Only the wheat and the main character have colour.", alone=True)),
    ("k2-field", *hero("man.jpg", MAN, FIELD.replace("Setting:", "Setting: at sunset,"), "the main character stands in the middle of his tall golden wheat field at sunset, peaceful, both hands at his sides.", alone=True)),
]

if __name__ == "__main__":
    for n, (slug, jobs) in enumerate(R.items()):
        js = [{"out": f"img/cand/{o}-{k}.jpg", "refs": r, "seed": 9000 + 37 * n + 2 * i + (k == "b"), "prompt": p}
              for i, (o, p, r) in enumerate(jobs) for k in "ab"]
        json.dump({"model": "black-forest-labs/flux.2-klein-4b", "size": "1152x2048", "workers": 2, "jobs": js},
                  open(f"{slug}/jobs.json", "w"), indent=1)
        print(slug, len(js))
