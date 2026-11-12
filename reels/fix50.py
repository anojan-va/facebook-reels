"""Fix jobs for reels 41-50: FIX[slug] = [(shot, prompt-builder args...)]; writes <slug>/jobs-fix.json with c/d candidates."""
import json, sys
sys.path.insert(0, "/home/user/facebook-reels/reels")
from jobs50 import *
F = {}
F["empty-boat"] = [("b02-crash", *hero("man.jpg", MAN, LK, f"TWO white rowing boats on the water: the main character stays SITTING inside the first boat; a second EMPTY {ROW} drifts out of the fog and bumps into the side of his boat with a splash; he grips the sides of his boat with both hands, shocked, both feet inside his boat.", alone=True))]
F["wooden-bowl"] = [("w05-ask", *hero("man.jpg", MAN, "Setting: an empty dining room at night in thin white line art, a lamp, nobody else in the room. ", f"the main character crouches on the floor beside {KID}, who sits cross-legged carving a small piece of wood; the father looks at him curiously, hands on his knees. ONLY these two people, the room is otherwise completely EMPTY, no figures standing in the background.", alone=False))]
F["thousand-mirrors"] = [("m06-many", *scene(MH, f"{ANGRY} stands in the middle of the hall growling; in every mirror on both walls its reflections growl back with bared teeth; ALL reflections are WHITE-filled dogs with thin dark outlines, NOT black, no dark dogs at all. No people."))]
CALM = "The young monk in the YELLOW robe is CALM, silent and smiling gently, his mouth closed; the man in WHITE is the angry one. "
F["insult-gift"] = [
 ("h0-face", *hero("monk.jpg", MONK, GR, CALM + f"{MAD} leans in and shouts furiously at the young monk, mouth wide open, pointing his finger at him; the young monk stands still, palms pressed together at his chest, calm gentle smile. " + ONLY2)),
 ("i01-come", *hero("monk.jpg", MONK, GR, CALM + f"the young monk sits cross-legged peacefully under the big tree, eyes half closed; {MAD} stomps along the stone path toward him, fists clenched, frowning. " + ONLY2)),
 ("i02-insult", *hero("monk.jpg", MONK, GR, CALM + f"{MAD} stands shouting at the young monk and waving both arms angrily; the young monk sits cross-legged under the tree, hands resting in his lap, listening calmly with a soft smile. " + ONLY2))]
BARE = KING.replace(" and white sneakers", "").replace("white sneakers", "") + "He is BAREFOOT: bare feet, NO shoes, NO sneakers. "
F["leather-shoes"] = [
 ("h0-feet", *hero("man.jpg", BARE, KG, "the king sits on his throne with his right bare foot lifted onto his left knee, holding the bare foot in both hands, wincing in pain; small red scratches on the sole of his foot; both feet bare.", alone=True)),
 ("l01-walk", *hero("man.jpg", BARE, RD, "the king walks BAREFOOT on the sharp stones of the road, wincing, arms out for balance, both bare feet visible.", alone=True)),
 ("l05-servant", *hero("man.jpg", KING, KG, f"the king in the yellow hoodie, crown and white cape SITS on the throne listening; in front of the throne {SV} STANDS and bows slightly, one hand on his chest, speaking. The servant has no crown. " + ONLY2))]
if __name__ == "__main__":
    for n, (slug, jobs) in enumerate(F.items()):
        js = [{"out": f"img/cand/{o}-{k}.jpg", "refs": r, "seed": 14000 + 41 * n + 3 * i + j, "prompt": p + WORLD}
              for i, (o, p, r) in enumerate(jobs) for j, k in enumerate("cd")]
        json.dump({"model": "black-forest-labs/flux.2-klein-4b", "size": "1152x2048", "workers": 4, "jobs": js},
                  open(f"/home/user/facebook-reels/reels/{slug}/jobs-fix.json", "w"), indent=1)
        print(slug, len(js))
