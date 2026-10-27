"""Writes gen1.json: Noli poses (white background, cut out later), background plates, UGC creator + POV shots."""
import json
NOLI = ("Use the reference image for exactly how this character looks: Noli, a glossy translucent cyan-blue 3D water-drop "
        "mascot with a curled pointed tip, big eyes with dark-blue irises and white highlights, thin dark-blue eyebrows, "
        "pink blush cheeks, small rounded arms with mitten hands, short round feet. Keep the identical character design, "
        "colours, glossy material and proportions; Pixar-style 3D render. ")
WHITE = " Full body, centred, on a pure plain white background, no floor, no shadow, no text, no other objects."
REF = ["refs/noli-thumbsup.jpg"]
jobs = []
def noli(name, pose, seed=1):
    jobs.append({"out": f"img/{name}.jpg", "prompt": NOLI + "New pose: " + pose + WHITE, "refs": REF, "seed": seed,
                 "size": "1152x1152"})
noli("n-worried", "worried and stressed, both hands pressed to its cheeks, eyebrows raised, eyes wide, mouth a small wavy 'o', two tiny sweat drops")
noli("n-point", "happy and excited, mouth open in a big smile, pointing with one hand to the viewer's left side, body turned slightly")
noli("n-dive", "jumping joyfully in mid-air, both arms raised high above its head, eyes squeezed shut in delight, big open smile, feet tucked")
noli("n-wave", "waving hello with one hand raised high, friendly open-mouth smile")
noli("n-wink", "winking one eye with a confident smile, tapping the side of its head with one finger like 'I know the answer'")
noli("n-present", "presenting proudly with both arms open wide to the sides, big open-mouth smile, eyes sparkling")
noli("n-confused", "confused, scratching its head with one hand, one eyebrow raised, mouth tilted, looking up")

POOL = ("Photorealistic, bright sunny summer daylight, crisp, high-end commercial photography. Vertical 9:16 composition. "
        "No people, no text, no logos. ")
def plate(name, prompt, refs=None, seed=1):
    j = {"out": f"img/{name}.jpg", "prompt": prompt, "seed": seed}
    if refs: j["refs"] = refs
    jobs.append(j)
plate("bg-pool-sunny", POOL + "A luxurious Mediterranean villa swimming pool with sparkling turquoise water and a beige stone deck, "
      "white sun loungers and umbrellas, cypress trees, the blue sea and soft hills in the distance, clear blue sky. Low camera at the pool edge, shallow depth of field.")
plate("bg-pool-green", POOL + "Top-down drone view looking straight down at a residential backyard swimming pool whose water is murky, "
      "cloudy dark green with algae, floating leaves, stone coping around it, the pool fills most of the frame.")
plate("bg-tubs", POOL + "On a stone table beside a swimming pool: many plain white plastic pool-chemical tubs and buckets with blank "
      "labels, a few bottles and a test-strip tube, piled in a messy cluster, shallow depth of field, blurred pool behind. Labels completely blank.")
NIGHT = "Photorealistic, cinematic, dark moody night, deep navy blue and teal colours, high-end commercial. Vertical 9:16. No people, no text. "
plate("bg-night-under", NIGHT + "Underwater view inside a swimming pool at night: shimmering caustic light patterns on the tiled floor and walls, "
      "light rays from above, a few bubbles, dark empty water in the centre.")
plate("bg-night-pool", NIGHT + "A backyard swimming pool at night lit by its underwater lights glowing turquoise, calm water, a modern house and palm "
      "silhouettes behind, starry sky, low camera at the water level.")
plate("bg-brain", NIGHT + "A glowing neon red outline of a human brain, made of thin light lines, floating in dark underwater pool water, "
      "small bubbles and red light reflections, centred, dramatic.")
plate("bg-cart", NIGHT + "A chrome shopping cart overflowing with plain white pool-chemical tubs and bottles with blank labels, on a dark "
      "studio floor, dramatic teal rim light from behind, centred. Labels completely blank.")

UGC = ("Photorealistic smartphone photo, natural and casual, like a frame from a TikTok video filmed on an iPhone. "
       "A friendly woman in her late 20s with shoulder-length wavy light-brown hair, sunglasses pushed up on her head, "
       "a white tank top and a thin gold necklace, in her sunny backyard by her swimming pool in golden-hour light. "
       "Correct anatomy: exactly two arms, two hands, five fingers on each hand. Vertical 9:16. No text. ")
plate("u-hook", UGC + "Selfie angle at arm's length, she looks into the camera with wide eyes, mouth open mid-sentence like 'wait!', "
      "and points down with her other hand toward the pool beside her, whose water is murky cloudy green.")
plate("u-wink", UGC + "Selfie angle at arm's length, she winks at the camera with a playful smile, the pool behind her is sparkling clear blue.",
      refs=["img/u-hook.jpg"])
plate("u-talk", UGC + "Selfie angle at arm's length, she talks to the camera enthusiastically, eyebrows raised, a hand gesturing near her chin, "
      "the pool behind her.", refs=["img/u-hook.jpg"])
POV = ("Photorealistic first-person POV smartphone photo looking down: a woman's hand with natural light pink nails holds a "
       "modern smartphone in portrait orientation, the phone screen is facing the viewer and shows a uniform solid bright "
       "chroma green (#00FF00) colour filling the whole screen, completely flat, no reflections, no UI. "
       "Correct anatomy: one hand, five fingers. Sunny golden-hour daylight. Vertical 9:16. No text. ")
plate("pov-cloudy", POV + "Below the phone, the backyard pool water is murky cloudy green with algae, stone pool edge, her bare feet at the bottom of the frame.")
plate("pov-deck", POV + "Below the phone, a sunny beige stone pool deck and the edge of a swimming pool, slightly blurred.")
json.dump({"model": "black-forest-labs/flux.2-klein-4b", "size": "1152x2048", "workers": 8,
           "jobs": [j for j in jobs if "u-hook.jpg" not in str(j.get("refs"))]}, open("gen1.json", "w"), indent=1)
json.dump({"model": "black-forest-labs/flux.2-klein-4b", "size": "1152x2048", "workers": 4,
           "jobs": [j for j in jobs if "u-hook.jpg" in str(j.get("refs"))]}, open("gen1b.json", "w"), indent=1)
print(len(jobs))
