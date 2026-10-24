"""Image jobs for parable reels 26-30 (carrot-egg-coffee … blind-elephant). Two candidates per shot."""
import json
from jobs25 import ALONE, ONLY2, STAND, colored, hero
from style_new import ANAT, MAN, OLD_MAN, PEOPLE, WHITE_MAN, scene

W = WHITE_MAN
KING = MAN + "He wears a golden crown and a long royal white cape over his yellow hoodie. "
R = {}

K = "Setting: a small kitchen at night in thin white line art: a stove with burners, a wooden table, a window, a hanging lamp. "
GIRL = "his teenage daughter drawn all in WHITE (white t-shirt, long white hair in a ponytail)"
POTS = "three white cooking pots of boiling water on the stove, steam rising"
R["carrot-egg-coffee"] = [
    ("a01-sad", *hero("man.jpg", MAN, K, f"{GIRL} sits at the table with her head in her hands, sad; the main character, her father, stands by the stove looking at her calmly, both hands at his sides. " + ONLY2)),
    ("a02-pots", *hero("man.jpg", MAN, K, f"the main character stands at the stove placing the last of {POTS} on the fire with both hands, quiet and calm, seen from the side.", alone=True)),
    ("a03-carrot", *hero("man.jpg", MAN, K, f"close-up at the stove: the main character drops one whole orange carrot into the first pot with his right hand; his left hand rests on the counter; next to it two more white pots. Only the carrot is orange.", alone=True)),
    ("a04-egg", *scene(K, "close-up: a white egg drops into a white pot of boiling water, a splash, steam rising. No people.")),
    ("a05-beans", *colored(K, "close-up: a handful of dark brown coffee beans pours from a white scoop into a white pot of boiling water, steam rising. Only the coffee beans are brown. No people.")),
    ("a06-clock", *colored(K, "a round white wall clock above the stove with three steaming white pots below, clouds of steam rising. No people.")),
    ("a07-carrot-soft", *hero("man.jpg", MAN, K, "close-up from the chest up: the main character holds up a soft limp drooping orange carrot between his right thumb and fingers, showing it; his left hand at his side. Only the carrot is orange.", alone=True)),
    ("a08-egg-crack", *hero("man.jpg", MAN, K, "close-up from the chest up: the main character holds a peeled hard-boiled egg cut in half in his open right palm, showing the firm white and yellow yolk inside; his left hand at his side.", alone=True)),
    ("a09-coffee", *hero("man.jpg", MAN, K, "the main character holds a white pot by its handle in his right hand and pours dark brown coffee from it straight DOWN into a white mug standing on the table; his left hand rests flat on the table; warm steam curls up from the mug. Only the coffee is brown.", alone=True)),
    ("a10-hand", *hero("man.jpg", MAN, K, f"the main character holds out a white mug of steaming coffee to {GIRL}, who sits at the table and reaches for it with both hands, curious. He holds it with one hand, his other hand on her shoulder. " + ONLY2)),
    ("k1-smile", *hero("man.jpg", MAN, K, f"{GIRL} sits at the table holding the warm mug of coffee in both hands and smiles, hopeful; the main character sits across the table smiling warmly, both his hands resting on the table. " + ONLY2)),
]

B = "Setting: a quiet sandy beach at noon in thin white line art: calm sea, a small wooden fishing boat pulled up on the sand, a palm tree. "
BIZ = "a rich businessman drawn all in WHITE wearing a white suit and a white tie"
R["fisherman"] = [
    ("b01-relax", *hero("man.jpg", MAN, B, "the main character, a fisherman, sits relaxed on the sand leaning against his small boat, hands behind his head, a basket with a few white fish beside him, a calm happy face.", alone=True)),
    ("b02-ask", *hero("man.jpg", MAN, B, f"{BIZ} stands looking down at the main character, who sits relaxed by his boat smiling up at him, one hand on his knee. " + ONLY2)),
    ("b03-count", *scene(B, f"{BIZ} stands on the beach counting on his fingers excitedly, holding up three fingers of his right hand, his left hand open, eager face. " + ANAT)),
    ("b04-dream", *scene("Setting: a big round thought bubble on a black background. ", "inside the thought bubble: tall skyscrapers, stacks of money, a big factory and a fleet of fishing ships, all drawn in white line art. No people.")),
    ("b05-tilt", *hero("man.jpg", MAN, B, "close-up from the chest up: the main character tilts his head to one side with a curious gentle smile, one eyebrow raised.", alone=True)),
    ("b06-proud", *scene(B, f"{BIZ} smiles proudly, chin up, one hand on his chest, the other hand gesturing out toward the sea. " + ANAT)),
    ("b07-family", *hero("man.jpg", MAN, B.replace("at noon", "at sunset") + "A small wooden hut on the beach. ", "two small children drawn all in WHITE run happily toward the main character, who kneels on both knees with his arms open to hug them; in the background his wife, drawn all in WHITE, waves from the door of their small hut. Exactly four people, standing clearly apart.")),
    ("b08-silent", *scene(B.replace("at noon", "at sunset"), f"{BIZ} stands alone on the beach, silent and thoughtful, his tie blowing in the wind, both hands at his sides. " + ANAT)),
    ("k1-sunset", *hero("man.jpg", MAN, B.replace("at noon", "at sunset"), "the main character sits on the sand by his boat at sunset with his arm around one small child drawn all in WHITE, both looking at the sea, peaceful. Only these two people.")),
]

HALL = "Setting: a lamp-lit village hall in thin white line art: wooden beams, hanging oil lamps, benches. "
OM = "the old main character"
R["same-joke"] = [
    ("c01-joke", *hero("man-old.jpg", OLD_MAN, HALL, f"{OM} stands at the front telling a story with one open hand raised, his other hand at his side; a crowd of villagers drawn all in WHITE sits on benches facing him, seen from behind. " + PEOPLE)),
    ("c02-laugh", *scene(HALL, "a crowd of villagers drawn all in WHITE sitting on benches laugh loudly, heads thrown back, holding their bellies, each sitting clearly apart. " + PEOPLE + ANAT)),
    ("c03-again", *hero("man-old.jpg", OLD_MAN, HALL, f"{OM} stands at the front with a playful smile, holding up one finger, telling the joke again.", alone=True)),
    ("c04-few", *scene(HALL, "the crowd of villagers drawn all in WHITE on benches: most sit with flat bored faces, only two people smile a little. " + PEOPLE + ANAT)),
    ("c05-silent", *scene(HALL, "the crowd of villagers drawn all in WHITE on benches sit completely silent and confused, frowning, some scratching their heads, nobody laughing. " + PEOPLE + ANAT)),
    ("c06-gentle", *hero("man-old.jpg", OLD_MAN, HALL, f"{OM} smiles gently and kindly, both hands open in front of him.", alone=True)),
    ("c07-eyes", *hero("man-old.jpg", OLD_MAN, HALL, f"big close-up of the face of {OM}: kind wise eyes looking straight at the viewer, a soft knowing smile.", alone=True)),
    ("c08-photo", *hero("man.jpg", MAN, "Setting: a small bedroom at night in thin white line art: a desk with a drawer, a lamp. ", "the main character sits at the desk looking sadly at an old photo held in both hands.", alone=True)),
    ("k1-drawer", *hero("man.jpg", MAN, "Setting: a small bedroom in morning light in thin white line art: a desk with an open drawer, a window. ", "the main character places an old photo into the open desk drawer with his right hand and closes it, a calm relieved face; his left hand rests on the desk.", alone=True)),
    ("k2-window", *hero("man.jpg", MAN, "Setting: a small bedroom in morning light in thin white line art: an open window with sunlight. ", "the main character stands at the open window breathing in the morning air, eyes closed, a peaceful smile, both hands resting on the window sill. " + STAND, alone=True)),
]

RD = "Setting: a dirt road through a village at night in thin white line art, bushes on both sides, a moon. "
GD = "two guards drawn all in WHITE with white helmets and spears"
R["boulder-road"] = [
    ("d01-place", *hero("man.jpg", KING, RD, f"the king points at a huge round boulder in the middle of the road while {GD} push it into place with both hands, each guard standing clearly apart.")),
    ("d02-hide", *hero("man.jpg", KING, RD.replace("at night", "at dawn"), "the king crouches behind a big bush at the side of the road, peeking out at the huge boulder on the road, curious, one hand parting the leaves.", alone=True)),
    ("d03-traders", *scene(RD.replace("at night", "in daylight"), "two rich traders drawn all in WHITE with white robes and turbans walk around the huge boulder on the road, complaining, one pointing angrily at it, standing clearly apart. " + ANAT)),
    ("d04-pass", *scene(RD.replace("at night", "in daylight"), "several travellers drawn all in WHITE walk past the huge boulder on the road shaking their heads, nobody touching it, standing clearly apart. " + PEOPLE + ANAT)),
    ("d05-farmer", *scene(RD.replace("at night", "in daylight"), "a poor farmer drawn all in WHITE with a white shirt and a straw hat sets down a big basket of vegetables beside the road, looking at the huge boulder. " + ANAT)),
    ("d06-push", *scene(RD.replace("at night", "in daylight"), "the poor farmer drawn all in WHITE pushes the huge boulder with both hands and his shoulder, leaning forward, legs braced, straining with all his strength. " + ANAT)),
    ("d07-rolls", *scene(RD.replace("at night", "in daylight"), "the huge boulder rolls off the road into the grass, dust flying; the farmer drawn all in WHITE stands beside it panting. " + ANAT)),
    ("d08-gold", *colored(RD.replace("at night", "in daylight"), "close-up of the ground where the boulder was: a small bag of shining GOLD coins spilling out and a rolled paper note with a red wax seal. Only the gold and the red seal have colour. No people.")),
    ("d09-amazed", *scene(RD.replace("at night", "in daylight"), "the farmer drawn all in WHITE holds a bag of gold coins in both hands, amazed, eyes wide, mouth open. " + ANAT)),
    ("k1-king", *hero("man.jpg", KING, RD.replace("at night", "at sunrise"), "the king steps out from behind the bush and smiles proudly at the farmer drawn all in WHITE who holds the bag of gold, the king's right hand raised in greeting, his left hand at his side. " + ONLY2)),
]

YARD = "Setting: a village courtyard in daylight in thin white line art: houses, a tree, a stone path. "
ELE = "a big calm elephant drawn all in WHITE with four legs, two ears, one trunk and one tail"
BLIND = "blind men drawn all in WHITE with white robes, eyes closed"
R["blind-elephant"] = [
    ("e01-four", *scene(YARD, f"{ELE} stands calmly in the courtyard; four {BLIND} walk toward it with arms stretched out in front of them, feeling the air, each standing clearly apart. " + ANAT)),
    ("e02-trunk", *scene(YARD, f"one of the {BLIND} holds the elephant's long trunk with both hands, eyes closed, a surprised face. Only one man and the elephant. " + ANAT)),
    ("e03-leg", *scene(YARD, f"one of the {BLIND} hugs one thick elephant leg with both arms like a tree trunk, eyes closed. Only one man and the elephant. " + ANAT)),
    ("e04-ear", *scene(YARD, f"one of the {BLIND} holds the edge of the elephant's big flat ear with both hands, flapping it like a fan, eyes closed. Only one man and the elephant. " + ANAT)),
    ("e05-tail", *scene(YARD, f"one of the {BLIND} holds the elephant's thin tail with both hands like a rope, eyes closed. Only one man and the elephant. " + ANAT)),
    ("e06-fight", *scene(YARD, f"the four {BLIND} argue angrily in a group, shouting with mouths open, pointing at each other, standing clearly apart; the elephant stands behind them. " + ANAT)),
    ("e07-wise", *hero("man.jpg", MAN, YARD, f"the main character walks in between two of the {BLIND} and gently puts one hand on each of their shoulders, a calm wise smile; the other two blind men stand nearby; the elephant behind. Exactly five people, standing clearly apart.")),
    ("e08-shape", *hero("man.jpg", MAN, "Setting: a plain room in thin white line art. ", f"the main character and a friend, {W}, stand on opposite sides of a big glowing white cylinder: from his side he sees a circle, from the friend's side a rectangle; they argue, each pointing at the shape with one hand. " + ONLY2)),
    ("k1-see", *hero("man.jpg", MAN, YARD.replace("in daylight", "at sunset"), f"the main character stands calmly beside {ELE}, one hand resting on its side, looking at the whole elephant with a thoughtful smile. " + STAND, alone=True)),
]

if __name__ == "__main__":
    n = 0
    for slug, jobs in R.items():
        js = []
        for i, (o, p, r) in enumerate(jobs):
            for k in "ab":
                js.append({"out": f"img/cand/{o}-{k}.jpg", "refs": r, "seed": 5000 + 31 * n + 2 * i + (k == "b"), "prompt": p})
        n += 1
        json.dump({"model": "black-forest-labs/flux.2-klein-4b", "size": "1152x2048", "workers": 2, "jobs": js},
                  open(f"{slug}/jobs.json", "w"), indent=1)
        print(slug, len(js))
