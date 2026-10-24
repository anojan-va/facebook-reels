"""Re-generations for reels 26-30: shots that failed review (three candidates each, suffix c/d/e)."""
import json
from jobs25 import ONLY2, colored, hero
from jobs30 import B, BIZ, ELE, K, KING, MAN, RD, YARD
from style_new import ANAT, scene

ONE_YELLOW = "Only ONE person in the image wears yellow: the main character. The other man is all WHITE. "
WHITE_HAIR = "His hair is drawn WHITE like the rest of him, NOT black, NOT dark; his face is clearly drawn with eyes, nose and mouth. "
WHITE_ELE = ("The elephant is WHITE-filled with thin dark outlines, NOT black, NOT a dark silhouette; it is big and fully in the frame. ")
BM = "ONE blind man drawn all in WHITE with a white robe, white skin, eyes closed"
F = {
    "carrot-egg-coffee": [
        ("a07-carrot-soft", *hero("man.jpg", MAN, K, "close-up from the chest up: the main character holds up a boiled orange carrot by one end between his right thumb and fingers; the carrot is SOFT and LIMP, bent in a deep curve and drooping straight down like a wet noodle; he looks at it calmly; his left hand at his side. Only the carrot is orange.", alone=True)),
        ("a09-coffee", *hero("man.jpg", MAN, K, "the main character sits at the table holding a white mug full of dark brown coffee in both hands, warm steam curling up from the mug, a calm knowing smile. Only the coffee is brown.", alone=True)),
    ],
    "fisherman": [
        ("b02-ask", *hero("man.jpg", MAN, B, f"on the LEFT the main character SITS relaxed on the sand leaning back against his boat, smiling up; on the RIGHT, a few steps away, {BIZ} STANDS tall looking down at him, hands on his hips. " + WHITE_HAIR + ONE_YELLOW + ONLY2)),
        ("b06-proud", *scene(B, f"{BIZ} smiles proudly, chin up, one hand on his chest, the other hand gesturing out toward the sea. " + WHITE_HAIR + ANAT)),
        ("b08-silent", *scene(B.replace("at noon", "at sunset"), f"{BIZ} stands alone on the beach seen from the front, silent and thoughtful, looking down, his white tie blowing in the wind, both hands at his sides. " + WHITE_HAIR + ANAT)),
    ],
    "boulder-road": [
        ("d06-push", *scene(RD.replace("at night", "in daylight"), "a HUGE round WHITE boulder taller than a man sits in the middle of the road; ONE poor farmer drawn all in WHITE with a straw hat, alone, leans into it from the left side pushing it with both palms flat on the rock, body slanted forward, legs braced behind him, straining. Only one person. The boulder is WHITE-filled, not black. " + ANAT)),
        ("k1-king", *hero("man.jpg", KING, RD.replace("at night", "at sunrise"), "the king stands on the left smiling proudly, his right hand raised in greeting, his left hand at his side; on the right a poor farmer drawn all in WHITE with a straw hat faces him, holding a small bag of gold in both hands, amazed. They face each other. " + ONLY2)),
    ],
    "blind-elephant": [
        ("e02-trunk", *scene(YARD, f"side view: {ELE} stands on the right, its long trunk hanging down in front of it; {BM} stands on the left in front of the elephant's head and holds the elephant's trunk with both hands, a surprised face. " + WHITE_ELE + "Only one man and the elephant. " + ANAT)),
        ("e03-leg", *scene(YARD, f"{ELE} stands in the courtyard; {BM} stands beside one of the elephant's thick front legs and wraps both arms around that leg, hugging it like a tree trunk, cheek against it. " + WHITE_ELE + "Only one man and the elephant. " + ANAT)),
        ("e04-ear", *scene(YARD, f"{ELE} stands facing the viewer with its huge flat ears spread wide; {BM} stands beside its head and holds the edge of one big ear with both hands, feeling it like a fan. " + WHITE_ELE + "Only one man and the elephant. " + ANAT)),
        ("e05-tail", *scene(YARD, f"{ELE} seen from behind, its thin tail hanging down; {BM} stands behind the elephant and holds the end of its thin tail with both hands like a rope. " + WHITE_ELE + "Only one man and the elephant. " + ANAT)),
        ("e06-fight", *scene(YARD, f"four blind men drawn all in WHITE with white robes, eyes closed, argue angrily in a row, shouting with mouths open, pointing at each other, standing clearly apart; {ELE} stands behind them. " + WHITE_ELE + ANAT)),
    ],
}

if __name__ == "__main__":
    for n, (slug, jobs) in enumerate(F.items()):
        js = [{"out": f"img/cand/{o}-{k}.jpg", "refs": r, "seed": 7000 + 41 * n + 3 * i + j, "prompt": p}
              for i, (o, p, r) in enumerate(jobs) for j, k in enumerate("cde")]
        json.dump({"model": "black-forest-labs/flux.2-klein-4b", "size": "1152x2048", "workers": 2, "jobs": js},
                  open(f"{slug}/jobs-fix.json", "w"), indent=1)
        print(slug, len(js))
