import json, sys
sys.path.insert(0, "/home/user/facebook-reels/reels")
from jobs60 import *
F = {}
SPLIT = "a giant WHITE boulder broken cleanly into TWO separate halves with a wide gap between them, fallen apart, white-filled with thin dark outlines"
F["stone-cutter-100"] = [
 ("s02-sweat", *hero("man.jpg", MAN, Q, "chest-up shot: the main character, tired, wipes sweat from his forehead with the back of his LEFT hand; his RIGHT hand grips the handle of a sledgehammer whose head rests on the ground beside him.", alone=True)),
 ("s05-split", *hero("man.jpg", MAN, Q, f"the main character stands holding a sledgehammer down in both hands right after the final blow; in front of him is {SPLIT}, a bright flash of light in the gap, dust flying.", alone=True)),
 ("s06-lucky", *scene(Q, f"three grown men {WM} stand around {SPLIT}, amazed with mouths open, one of them pointing at it, each standing clearly apart. " + ANAT))]
F["pencil-lesson"] = [("p03-show", *hero("boy.jpg", BOY, DESK, f"{GRAN} SITS at the desk and holds up a yellow pencil in HER right hand, smiling, showing it to the small boy; the small boy stands beside her chair with EMPTY hands at his sides, looking at the pencil with wide eyes. The boy is a small child, his head at her shoulder height. " + ONLY2))]
OWN2 = f"a boat owner {WM}, bareheaded with short white hair, NO cap"
CAP = "The main character in the YELLOW hoodie wears the white painter's cap; the white man has no cap. "
F["hole-in-boat"] = [
 ("h01-hire", *hero("man.jpg", MAN, DOCK, CAP + f"{OWN2} hands a white paintbrush to {PAINTER}, who takes it with one hand; the owner points at {BOAT} with his other hand. " + ONLY2)),
 ("h06-reward", *hero("man.jpg", MAN, DOCK, CAP + f"{OWN2} holds out a bag of coins with both hands toward {PAINTER}, grateful, tears in his eyes; the painter in yellow looks surprised, receiving it. " + ONLY2))]
F["donkey-salt"] = [("d01-load", *scene(RIV, f"{MER} STANDS on the ground beside {DON} and lifts a heavy white sack of salt with both hands onto the donkey's back; nobody rides the donkey. " + ANAT))]
F["wolf-sheep"] = [
 ("w02-shepherd", *hero("man.jpg", MAN, FLD, f"the main character, a shepherd, stands on the hill GRIPPING a long wooden staff in his RIGHT hand, the staff's bottom on the ground; his LEFT hand is raised to shade his eyes as he watches over a flock of {SHEEP}.", alone=True)),
 ("w04-sleep", *scene(FLD.replace("Setting:", "Setting: at night under the moon,"), f"a flock of {SHEEP} sleeps peacefully; among them lies a wolf wearing a white sheepskin, its WHITE wolf face with one eye open and a sly grin peeking out. Every animal is WHITE-filled, no black or dark animals. No people."))]
F["three-sieves"] = [
 ("t04-two", *hero("man.jpg", MAN, AG, f"chest-up shot: {SOC} holds his right hand up beside his face making a V sign: exactly TWO fingers raised (index and middle), the other fingers folded; eyebrows raised. His left arm hangs at his side.", alone=True)),
 ("t06-three", *hero("man.jpg", MAN, AG, f"chest-up shot: {SOC} holds his right hand up beside his face with exactly THREE fingers raised (index, middle and ring finger), thumb and little finger folded; a gentle knowing smile. His left arm hangs at his side.", alone=True))]
F["woodcutter-axe"] = [("a07-three", *colored(FR, "the main character in his mustard-YELLOW hoodie, black cargo pants and white sneakers, with a short brown beard, smiles amazed and grateful, hugging THREE axes against his chest with both arms: one shining GOLD axe, one shining SILVER axe and one plain old iron axe with a wooden handle, all three clearly visible. Only he and the golden axe have colour."))]
if __name__ == "__main__":
    for n, (slug, jobs) in enumerate(F.items()):
        js = [{"out": f"img/cand/{o}-{k}.jpg", "refs": r, "seed": 18000 + 41 * n + 3 * i + j, "prompt": p + WORLD}
              for i, (o, p, r) in enumerate(jobs) for j, k in enumerate("cd")]
        json.dump({"model": "black-forest-labs/flux.2-klein-4b", "size": "1152x2048", "workers": 4, "jobs": js},
                  open(f"/home/user/facebook-reels/reels/{slug}/jobs-fix.json", "w"), indent=1)
        print(slug, len(js))
