import json, sys
sys.path.insert(0, "/home/user/facebook-reels/reels")
from jobs90 import *
F = {}
SIDE = "Setting: side view at road level of a LOW concrete bridge passing over a city road in thin white line art. "
F["truck-bridge"] = [
 ("h0-stuck", *scene(SIDE, f"{TRUCK} is driving UNDER the low bridge and is jammed: the top of its box trailer is pressed hard against the underside of the concrete bridge, which is cracked and chipped where they touch; the truck is half under the bridge; dust falls. No people.")),
 ("t08-free", *scene(SIDE, f"{TRUCK} drives out from UNDER the low bridge on the road below it, a small clear gap now visible between the top of the trailer and the underside of the bridge, motion lines behind the truck. No people."))]
UP = f"a tall tree: high up on a branch sits {CROW} holding {CHEESE} in its beak; on the ground far below sits {FOX}, alone, looking UP at the crow. Exactly ONE fox and ONE crow, both WHITE, no black birds. "
F["fox-crow-cheese"] = [
 ("f02-fox", *colored(TREE, UP + "The fox licks its lips hungrily. Only the cheese has colour. No people.")),
 ("f03-praise", *colored(TREE, UP + "The fox smiles sweetly with its front paws pressed together, flattering the crow. Only the cheese has colour. No people."))]
if __name__ == "__main__":
    for n, (slug, jobs) in enumerate(F.items()):
        js = [{"out": f"img/cand/{o}-{k}.jpg", "refs": r, "seed": 30000 + 41 * n + 3 * i + j, "prompt": p + WORLD}
              for i, (o, p, r) in enumerate(jobs) for j, k in enumerate("cde")]
        json.dump({"model": "black-forest-labs/flux.2-klein-4b", "size": "1152x2048", "workers": 3, "jobs": js},
                  open(f"/home/user/facebook-reels/reels/{slug}/jobs-fix.json", "w"), indent=1)
        print(slug, len(js))
