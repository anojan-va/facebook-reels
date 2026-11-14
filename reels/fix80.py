import json, sys
sys.path.insert(0, "/home/user/facebook-reels/reels")
from jobs80 import *
F = {}
F["long-spoons"] = [("h0-feed", *colored(HALL, f"close-up across the table: two smiling men {WM} sit facing each other; each one holds ONE very long spoon (as long as a broom) in both hands and puts the food at its end into the OTHER man's open mouth across the table; the two long spoons cross in the middle above the bowls. Warm golden light. Only the warm light has colour. ONLY these two people. " + ANAT))]
F["ant-grasshopper"] = [("h0-snow", *scene("Setting: a meadow in a heavy BLIZZARD at night in thin white line art; thick white snow covers the ground, big snowflakes falling everywhere, frozen grass. ", f"close-up: {HOP} sits half-buried in white snow, hugging itself with its front legs, shivering, sad hungry eyes, icicles hanging from its antennae, snowflakes on its back. No people."))]
if __name__ == "__main__":
    for n, (slug, jobs) in enumerate(F.items()):
        js = [{"out": f"img/cand/{o}-{k}.jpg", "refs": r, "seed": 26000 + 41 * n + 3 * i + j, "prompt": p + WORLD}
              for i, (o, p, r) in enumerate(jobs) for j, k in enumerate("cde")]
        json.dump({"model": "black-forest-labs/flux.2-klein-4b", "size": "1152x2048", "workers": 3, "jobs": js},
                  open(f"/home/user/facebook-reels/reels/{slug}/jobs-fix.json", "w"), indent=1)
        print(slug, len(js))
