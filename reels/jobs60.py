"""Image jobs for parable reels 51-60 (stone-cutter-100 … two-seeds). Two candidates per shot. Writes <slug>/jobs.json.

Same conventions as jobs50.py: h0 = hook image, WORLD appended to every prompt."""
import json
from jobs25 import BOY, KING, ONLY2, STAND, colored, hero
from jobs50 import WM, WORLD
from style_new import ANAT, MAN, OLD_MAN, scene

R = {}

Q = "Setting: a rocky quarry in daylight in thin white line art, cliffs, scattered stones. "
ROCK = "a giant WHITE boulder as tall as a man, white-filled with thin dark outlines"
CROWD = f"three villagers {WM}, standing clearly apart"
R["stone-cutter-100"] = [
    ("h0-strike", *hero("man.jpg", MAN, Q, f"the main character swings a big sledgehammer high over his head with BOTH hands on the handle, about to strike {ROCK}, determined face, side view.", alone=True)),
    ("s01-first", *hero("man.jpg", MAN, Q, f"the main character strikes {ROCK} with a sledgehammer held in both hands; the rock is completely unharmed, no crack.", alone=True)),
    ("s02-sweat", *hero("man.jpg", MAN, Q, "chest-up shot: the main character wipes sweat from his forehead with the back of his right hand, his left hand holding a sledgehammer resting on his shoulder, tired but focused.", alone=True)),
    ("s03-laugh", *scene(Q, f"{CROWD} laugh and point at a huge white boulder, mocking. " + ANAT)),
    ("s04-again", *hero("man.jpg", MAN, Q, f"the main character keeps striking {ROCK} with a sledgehammer in both hands, small chips flying, the sun lower in the sky behind him.", alone=True)),
    ("s05-split", *hero("man.jpg", MAN, Q, f"the main character's sledgehammer strikes and {ROCK} splits cleanly in two halves with a bright crack of light down the middle; he holds the hammer with both hands.", alone=True)),
    ("s06-lucky", *scene(Q, f"{CROWD} stand amazed beside a huge boulder split in two halves, mouths open, one of them clapping. " + ANAT)),
    ("s07-knows", *hero("man.jpg", MAN, Q, "chest-up shot: the main character smiles quietly and knowingly, the sledgehammer resting on his right shoulder in his right hand, his left hand at his side.", alone=True)),
    ("k1-next", *hero("man.jpg", MAN, Q.replace("in daylight", "at sunset"), "the main character walks toward the next giant white boulder at sunset, sledgehammer on his shoulder, determined.", alone=True)),
]

DES = "Setting: a desert of sand dunes in thin white line art. "
ZOO = "Setting: a small zoo enclosure with tall white bars and a fence in thin white line art. "
CAMEL = "a big mother camel drawn all in WHITE (white fur) with one hump, NOT black-filled"
BABY = "a small baby camel drawn all in WHITE (white fur), NOT black-filled"
R["camel-hump"] = [
    ("h0-zoo", *scene(ZOO, f"{CAMEL} and {BABY} stand behind white zoo bars, looking out sadly. No people.")),
    ("c01-ask", *scene(ZOO, f"{BABY} looks up curiously at {CAMEL}, asking a question. No people.")),
    ("c02-hump", *scene(DES, f"close-up of {CAMEL}'s big hump with small glowing white water drops drawn inside it, the desert behind. No people.")),
    ("c03-lashes", *scene(DES, f"close-up of the face of {CAMEL} with long eyelashes, eyes half closed, a sandstorm blowing past. No people.")),
    ("c04-feet", *scene(DES, f"close-up of the wide flat feet of {CAMEL} standing firmly on soft sand without sinking. No people.")),
    ("c05-think", *scene(ZOO, f"close-up of {BABY} thinking, looking at the bars, confused. No people.")),
    ("c06-stuck", *scene(ZOO, f"wide view: {CAMEL} and {BABY} inside a small zoo pen, white bars all around, tiny space. No people.")),
    ("k0-office", *hero("man.jpg", MAN, "Setting: a small grey office cubicle at night in thin white line art. ", "the main character sits squeezed in a tiny cubicle looking out of the window at the desert far away, sad and trapped.", alone=True)),
    ("k1-desert", *hero("man.jpg", MAN, DES.replace("Setting:", "Setting: at sunrise,"), "the main character walks confidently across the sand dunes at sunrise, free, arms swinging.", alone=True)),
]

DESK = "Setting: a cozy room in thin white line art, a wooden desk with paper and a lamp. "
GRAN = f"an old grandmother {WM}, white hair in a bun, kind face, glasses"
R["pencil-lesson"] = [
    ("h0-pencil", *colored(DESK, "close-up: a single YELLOW pencil standing upright on a sheet of paper, glowing softly. Only the pencil has colour. No people.")),
    ("p01-writing", *scene(DESK, f"{GRAN} sits at the desk writing a letter with a pencil in her right hand, her left hand holding the paper. Only one person. " + ANAT)),
    ("p02-boy", *hero("boy.jpg", BOY, DESK, f"the small boy leans on the desk beside {GRAN}, who sits writing; he looks curiously at her letter. The boy is a small child. " + ONLY2)),
    ("p03-show", *hero("boy.jpg", BOY, DESK, f"{GRAN} holds up a yellow pencil in her right hand, showing it to the small boy, who looks at it with wide eyes. " + ONLY2)),
    ("p04-hand", *colored(DESK, "close-up: an old WHITE hand guiding a YELLOW pencil across the paper, drawing a long line. Only the pencil has colour.")),
    ("p05-sharpen", *colored(DESK, "close-up: a YELLOW pencil being sharpened in a small white sharpener, curly wood shavings falling. Only the pencil has colour. No people.")),
    ("p06-erase", *colored(DESK, "close-up: the pink eraser of a YELLOW pencil rubbing out a crooked line on white paper, eraser crumbs. Only the pencil has colour. No people.")),
    ("p07-inside", *colored(DESK, "close-up cross-section of a YELLOW pencil cut in half, showing its dark graphite core glowing white inside. No people.")),
    ("k1-boy", *hero("boy.jpg", BOY, DESK.replace("in thin", "in warm lamp light, thin"), "the small boy sits at the desk happily drawing with a yellow pencil, a proud smile.", alone=True)),
]

DOCK = "Setting: a small harbour in thin white line art, a wooden dock, calm sea. "
BOAT = "a WHITE wooden fishing boat on blocks on the dock"
PAINTER = "the main character, a painter, wearing his yellow hoodie and a white painter's cap"
OWNER = f"a boat owner {WM}"
R["hole-in-boat"] = [
    ("h0-hole", *hero("man.jpg", MAN, DOCK, f"close-up: {PAINTER} kneels beside {BOAT} and presses a small wooden patch over a small hole in the hull with both hands, focused.", alone=True)),
    ("h01-hire", *hero("man.jpg", MAN, DOCK, f"{OWNER} hands a white paintbrush to {PAINTER} and points at {BOAT}. " + ONLY2)),
    ("h02-paint", *hero("man.jpg", MAN, DOCK, f"{PAINTER} paints the side of {BOAT} with a white brush in his right hand, a paint bucket at his feet.", alone=True)),
    ("h03-notice", *hero("man.jpg", MAN, DOCK, f"{PAINTER} crouches and looks closely at a small hole in the hull of {BOAT}, curious, one finger pointing at it.", alone=True)),
    ("h04-kids", *scene(DOCK.replace("calm sea", "a stormy sea with big waves"), "a white fishing boat sails out on the rough sea with three small children drawn all in WHITE inside it, clearly apart. " + ANAT)),
    ("h05-run", *scene(DOCK, f"{OWNER} runs along the dock holding a small bag of coins, urgent face. Only one person. " + ANAT)),
    ("h06-reward", *hero("man.jpg", MAN, DOCK, f"{OWNER} gives a bag of coins to {PAINTER} with both hands, grateful, tears in his eyes; the painter looks surprised. " + ONLY2)),
    ("h07-surprised", *hero("man.jpg", MAN, DOCK, "chest-up shot: the main character, wearing a white painter's cap, looks surprised and touched, his right hand on his chest.", alone=True)),
    ("k1-sunset", *hero("man.jpg", MAN, DOCK.replace("Setting:", "Setting: at sunset,"), f"{PAINTER} sits on the edge of the dock at sunset looking at the sea, a calm smile, the boat floating safely nearby.", alone=True)),
]

VIL = "Setting: a dark village street at night in thin white line art, small houses, a moon. "
BM = "a blind old man drawn all in WHITE (white robe, white beard), eyes closed, holding a lit oil lamp with a warm YELLOW flame"
R["blind-lamp"] = [
    ("h0-lamp", *colored(VIL, f"{BM} walks slowly down the dark street, the warm yellow glow of his lamp lighting the path around him. Only the flame has colour.")),
    ("b01-walk", *colored(VIL, f"wide view: {BM} walks through the dark village, a tiny warm yellow light in the night. Only the flame has colour.")),
    ("b02-laugh", *colored(VIL, f"three villagers {WM} laugh and point at {BM} who walks past them, each standing clearly apart. Only the flame has colour.")),
    ("b03-smile", *colored(VIL, f"close-up: {BM} smiles gently, the lamp held up near his face, eyes closed. Only the flame has colour.")),
    ("b04-path", *colored(VIL, f"a villager {WM} walking in the dark safely steps aside to avoid {BM} thanks to the yellow lamp light. Only the flame has colour.")),
    ("b05-quiet", *colored(VIL, f"the three villagers {WM} stop laughing, silent and thoughtful, looking at the lamp glow. Only the flame has colour.")),
    ("k1-hero", *hero("man.jpg", MAN, VIL, "the main character walks down the dark street holding a lit oil lamp up in his right hand, its warm glow lighting the path for others, a kind calm face, left hand at his side.", alone=True)),
    ("k2-glow", *hero("man.jpg", MAN, VIL, "chest-up shot: the main character holds a glowing oil lamp near his chest with both hands, a gentle smile, warm light on his face.", alone=True)),
]

RIV = "Setting: a shallow river crossing in thin white line art, rocks, a path on both banks. "
DON = "a donkey drawn all in WHITE (white fur), NOT black-filled"
MER = f"a merchant {WM} with a white turban"
R["donkey-salt"] = [
    ("h0-fall", *scene(RIV, f"{DON} carrying two big white sacks falls sideways into the river with a big splash. No people.")),
    ("d01-load", *scene(RIV, f"{MER} loads two heavy white sacks of salt onto the back of {DON}. " + ANAT)),
    ("d02-cross", *scene(RIV, f"{DON} carrying two heavy white sacks walks into the river, {MER} walking ahead holding its rope. " + ANAT)),
    ("d03-light", *scene(RIV, f"{DON} stands up in the river, the sacks on its back now small and empty, the donkey looking happy. No people.")),
    ("d04-sneaky", *scene(RIV, f"{DON} winks and deliberately lies down in the river on purpose, sacks on its back. No people.")),
    ("d05-notice", *scene(RIV, f"{MER} stands on the bank with arms crossed, frowning suspiciously at the donkey in the river. Only one person. " + ANAT)),
    ("d06-sponges", *scene(RIV, f"{MER} smiles slyly and loads big fluffy white sponges onto {DON}. " + ANAT)),
    ("d07-heavy", *scene(RIV, f"{DON} struggles to stand up in the river, the sponges on its back swollen huge with water, dripping, very heavy, its legs shaking. No people.")),
    ("k1-hero", *hero("man.jpg", MAN, "Setting: a riverbank at sunset in thin white line art. ", "the main character stands on the riverbank thinking, one hand on his chin, looking at the water, a thoughtful wise smile. " + STAND, alone=True)),
]

FLD = "Setting: a grassy hill pasture in thin white line art, a wooden fence. "
SHEEP = "fluffy sheep drawn all in WHITE, NOT black-filled"
WOLF = "a wolf drawn all in WHITE (white fur), NOT black-filled, with sharp teeth"
R["wolf-sheep"] = [
    ("h0-disguise", *scene(FLD, f"close-up: {WOLF} pulls a fluffy white sheepskin over its head with its paws, grinning slyly, sharp teeth showing. No people.")),
    ("w01-watch", *scene(FLD, f"{WOLF} hides behind a bush on the hill, hungrily watching a flock of {SHEEP} grazing below. No people.")),
    ("w02-shepherd", *hero("man.jpg", MAN, FLD, f"the main character, a shepherd, stands on the hill holding a wooden staff in his right hand, watching over a flock of {SHEEP}, his left hand shading his eyes.", alone=True)),
    ("w03-walk", *scene(FLD, f"{WOLF} wearing a sheepskin costume walks into the middle of a flock of {SHEEP}; its wolf tail sticks out behind. No people.")),
    ("w04-sleep", *scene(FLD.replace("Setting:", "Setting: at night under the moon,"), f"a flock of {SHEEP} sleeps peacefully; among them the wolf in a sheepskin lies with one eye open, grinning. No people.")),
    ("w05-dark", *hero("man.jpg", MAN, FLD.replace("Setting:", "Setting: at night under the moon,"), "the main character, the shepherd, walks into the dark field holding a lantern in his left hand, looking for the biggest sheep.", alone=True)),
    ("w06-grab", *hero("man.jpg", MAN, FLD.replace("Setting:", "Setting: at night under the moon,"), f"the main character grabs the biggest 'sheep' with both hands, and the sheepskin slips off revealing {WOLF} underneath, shocked.", alone=True)),
    ("w07-caught", *scene(FLD.replace("Setting:", "Setting: at night under the moon,"), f"{WOLF} sits tangled in a rope net with a sheepskin hanging off it, defeated and embarrassed. No people.")),
    ("k1-flock", *hero("man.jpg", MAN, FLD.replace("Setting:", "Setting: at sunrise,"), f"the main character, the shepherd, stands calmly with his staff in his right hand, surrounded by his flock of {SHEEP}, peaceful smile.", alone=True)),
]

AG = "Setting: an ancient Greek courtyard in thin white line art, marble columns, a fountain. "
SOC = ("the main character as a wise philosopher, in his yellow hoodie with a long WHITE Greek toga draped over one shoulder")
GOS = f"a gossiping man {WM} with a white Greek tunic, excited face"
R["three-sieves"] = [
    ("h0-stop", *hero("man.jpg", MAN, AG, f"{SOC} raises his right hand palm-out saying stop, calm and wise; {GOS} rushes toward him, mouth open to speak. " + ONLY2)),
    ("t01-run", *scene(AG, f"{GOS} runs across the courtyard excitedly, waving one hand. Only one person. " + ANAT)),
    ("t02-one", *hero("man.jpg", MAN, AG, f"chest-up shot: {SOC} holds up ONE finger of his right hand, a calm questioning look.", alone=True)),
    ("t03-shrug", *scene(AG, f"chest-up shot: {GOS} shrugs uncertainly, both palms up. Only one person. " + ANAT)),
    ("t04-two", *hero("man.jpg", MAN, AG, f"chest-up shot: {SOC} holds up TWO fingers of his right hand, eyebrows raised.", alone=True)),
    ("t05-bad", *scene(AG, f"chest-up shot: {GOS} looks down guiltily, rubbing the back of his neck with one hand. Only one person. " + ANAT)),
    ("t06-three", *hero("man.jpg", MAN, AG, f"chest-up shot: {SOC} holds up THREE fingers of his right hand, a gentle knowing smile.", alone=True)),
    ("t07-quiet", *scene(AG, f"{GOS} stands silent with his mouth closed and his hand over his mouth, embarrassed. Only one person. " + ANAT)),
    ("k1-wise", *hero("man.jpg", MAN, AG.replace("Setting:", "Setting: at sunset,"), f"{SOC} sits calmly on the steps between the marble columns at sunset, a peaceful wise smile, both hands resting on his knees.", alone=True)),
]

FR = "Setting: a deep river in a forest in thin white line art, tall trees, rocks on the bank. "
SPIRIT = "a glowing river spirit drawn all in WHITE, a kind old figure made of flowing water rising from the river"
R["woodcutter-axe"] = [
    ("h0-gold", *colored(FR, f"{SPIRIT} rises from the river holding up a shining GOLDEN axe. Only the axe has colour.")),
    ("a01-chop", *hero("man.jpg", MAN, FR, "the main character, a poor woodcutter, chops a tree beside the river with an old iron axe held in both hands.", alone=True)),
    ("a02-drop", *hero("man.jpg", MAN, FR, "the main character reaches out in panic with both hands as his iron axe slips and falls into the deep river with a splash.", alone=True)),
    ("a03-cry", *hero("man.jpg", MAN, FR, "the main character sits on a rock by the river with his face in his hands, crying.", alone=True)),
    ("a04-offer", *hero("man.jpg", MAN, FR, f"{SPIRIT} holds out a shining golden axe toward the main character, who stands on the bank shaking his head no, one hand raised.")),
    ("a05-silver", *colored(FR, f"{SPIRIT} holds up a shining SILVER axe. Only the axe has a metallic shine.")),
    ("a06-iron", *hero("man.jpg", MAN, FR, f"{SPIRIT} holds up an old iron axe; the main character on the bank smiles happily, both hands reaching for it, nodding yes.")),
    ("a07-three", *hero("man.jpg", MAN, FR, "the main character holds three axes in his arms, a golden one, a silver one and an iron one, amazed and grateful.", alone=True)),
    ("k1-walk", *hero("man.jpg", MAN, FR.replace("Setting:", "Setting: at sunset,"), "the main character walks home along the forest path at sunset, a golden axe over his shoulder, a peaceful smile.", alone=True)),
]

SOIL = "Setting: underground in rich dark soil drawn in thin white line art, a cross-section with the surface above. "
SEED = "a small round seed drawn all in WHITE, NOT black-filled, with a tiny cute face"
R["two-seeds"] = [
    ("h0-hen", *scene(SOIL, f"a hen drawn all in WHITE scratches the surface soil with its feet and pecks down at {SEED} hiding in a hole, the seed's eyes wide with fear. No people.")),
    ("g01-two", *scene(SOIL, f"two of {SEED}, side by side underground, one smiling bravely, the other nervous. No people.")),
    ("g02-roots", *colored(SOIL, "the brave seed pushes long white roots down deep and a small GREEN sprout up through the surface toward the sun. Only the sprout is green. No people.")),
    ("g03-sun", *colored(SOIL.replace("underground in rich dark soil drawn in", "a garden in"), "a young GREEN plant with leaves reaching toward a bright sun in the sky. Only the plant is green. No people.")),
    ("g04-scared", *scene(SOIL, f"close-up: {SEED} curled up tightly underground, trembling, imagining rocks and bugs in small white thought bubbles. No people.")),
    ("g05-wait", *scene(SOIL, f"{SEED} sits alone underground, waiting, a small clock ticking above it. No people.")),
    ("g06-eat", *scene(SOIL, f"a hen drawn all in WHITE swallows {SEED} with its beak; feathers flying. No people.")),
    ("k1-hero", *hero("man.jpg", MAN, "Setting: a sunny garden in thin white line art. ", "the main character kneels on both knees and plants a seed in the soil with both hands, a hopeful smile.", alone=True)),
    ("k2-tall", *colored("Setting: a hill at sunrise in thin white line art. ", "a tall strong tree with a GREEN crown stands alone on the hill at sunrise. Only the leaves are green. No people.")),
]

if __name__ == "__main__":
    for n, (slug, jobs) in enumerate(R.items()):
        js = [{"out": f"img/cand/{o}-{k}.jpg", "refs": r, "seed": 16000 + 37 * n + 2 * i + (k == "b"), "prompt": p + WORLD}
              for i, (o, p, r) in enumerate(jobs) for k in "ab"]
        json.dump({"model": "black-forest-labs/flux.2-klein-4b", "size": "1152x2048", "workers": 2, "jobs": js},
                  open(f"{slug}/jobs.json", "w"), indent=1)
        print(slug, len(js))
