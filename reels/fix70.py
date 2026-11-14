import json, sys
sys.path.insert(0, "/home/user/facebook-reels/reels")
from jobs70 import *
F = {}
F["kintsugi-bowl"] = [
 ("k01-drop", *hero("man.jpg", MAN, TEA, f"the main character stands with both hands open in front of him, shocked; {BOWL} is in mid-air falling down between his hands and the floor, motion lines above it.", alone=True)),
 ("k02-shards", *scene(TEA, "close-up of the wooden floor: a white ceramic tea bowl smashed into many broken jagged pieces scattered on the floor; NO whole bowl, NO cup, only broken fragments. No people."))]
F["rich-poor-trip"] = [("r01-car", *hero("boy.jpg", BOY, "Setting: the driveway of a big modern house at night in thin white line art, a big WHITE car. Nobody else around, no figures in the background, no pool. ", f"the small boy stands beside {DAD} next to the open door of the big white car, the father's hand on the boy's shoulder; the boy is a small child, his head at the father's waist. " + ONLY2))]
F["words-feathers"] = [("w01-shout", *hero("boy.jpg", BOY, "Setting: an EMPTY schoolyard in thin white line art, nobody else around, no figures in the background, no buildings with people. ", "the small boy shouts angrily with his fists clenched at another small boy drawn all in WHITE, who looks hurt and sad. Two small children, ONLY these two in the whole image."))]
CARTSIDE = "Side view of the road: a white horse in front pulls a WHITE wooden cart behind it; "
F["bag-on-cart"] = [
 ("b02-offer", *hero("man.jpg", MAN, ROAD, CARTSIDE + f"{FMR} sits on the cart's front seat holding the reins and waves; the main character STANDS on the road beside the cart with {BAG} on his shoulder, looking up at the farmer. The farmer has WHITE hair and a white straw hat. " + ONLY2)),
 ("k1-down", *hero("man.jpg", MAN, ROAD.replace("Setting:", "Setting: at sunset,"), CARTSIDE + f"the main character sits INSIDE the cart bed with both legs inside the cart, leaning back, both hands behind his head, a peaceful smile; {BAG} lies on the cart floor beside him. Exactly two legs, both inside the cart.", alone=True))]
F["busy-beggar"] = [("g03-stranger", *hero("man.jpg", MAN, STR, f"on the RIGHT the main character in his torn mustard-YELLOW hoodie SITS on {BOX} holding a small bowl, looking up; on the LEFT {STRANGER} STANDS and points down at the box. The standing stranger is ALL WHITE: white coat, white hair, white skin, NOT yellow, NOT brown hair. Only the sitting man is coloured. " + ONLY2))]
MONKROBE = "an old bald monk in a long WHITE monk ROBE wrapped over one shoulder and sandals, NO hoodie, NO backpack, kind wrinkled face"
F["search-within"] = [("s05-give", *hero("man.jpg", MAN, TEMPLE, f"{MONKROBE} holds out a small round hand mirror toward the main character, a traveller in his yellow hoodie with a backpack, who reaches for it with one hand, confused. The monk is ALL WHITE; only the traveller is coloured. " + ONLY2))]
if __name__ == "__main__":
    for n, (slug, jobs) in enumerate(F.items()):
        js = [{"out": f"img/cand/{o}-{k}.jpg", "refs": r, "seed": 22000 + 41 * n + 3 * i + j, "prompt": p + WORLD}
              for i, (o, p, r) in enumerate(jobs) for j, k in enumerate("cde")]
        json.dump({"model": "black-forest-labs/flux.2-klein-4b", "size": "1152x2048", "workers": 3, "jobs": js},
                  open(f"/home/user/facebook-reels/reels/{slug}/jobs-fix.json", "w"), indent=1)
        print(slug, len(js))
