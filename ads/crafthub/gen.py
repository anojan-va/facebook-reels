"""Writes gen1.json (objects + paper-cut people on white, for cut-outs) and gen2.json (variants that need refs)."""
import json
PHOTO = ("Studio product photo of {}, isolated on a pure plain white background, soft natural daylight, a soft subtle shadow "
         "under it, centred, sharp focus, realistic textures, no text, no logos, no people, no hands.")
PAPER = ("Layered paper cut-out craft illustration of {}, made of textured coloured craft paper with visible cut edges, "
         "paper layers and small drop shadows between layers, flat colours in terracotta, cream, sage green, mustard and "
         "deep green, on a pure plain white background, centred, no text.")
jobs = []
def j(name, prompt, size="1152x1152", seed=1, refs=None):
    d = {"out": f"img/{name}.jpg", "prompt": prompt, "size": size, "seed": seed}
    if refs: d["refs"] = refs
    jobs.append(d)
j("o-mug", PHOTO.format("a handmade wheel-thrown ceramic mug with a glossy terracotta glaze dripping over a raw sand-coloured clay base, slightly imperfect handmade shape"))
j("o-lino", PHOTO.format("a handmade lino-cut printed Christmas card showing a deep green pine tree print on cream paper, with a small wooden lino carving tool and a rubber ink roller next to it"))
j("o-wine-clay", PHOTO.format("a glass of red wine next to a small handmade unglazed clay bowl with fingerprints in the clay"))
j("o-hoop", PHOTO.format("a wooden embroidery hoop with colourful hand-stitched wildflowers in terracotta, mustard and sage green thread on cream linen, a needle with thread hanging from it"))
j("o-wallet", PHOTO.format("a handmade tan leather card wallet with visible white saddle stitching, slightly open"))
j("o-tea", PHOTO.format("two cosy ceramic tea mugs side by side with a ball of mustard yarn, a paintbrush and a few coloured paper scraps"))
j("o-wonky", PHOTO.format("a cute, very lopsided and wonky handmade clay mug with an uneven rim and a crooked handle, glazed sage green, charming beginner pottery"))
j("o-yarn", PHOTO.format("a ball of chunky terracotta wool yarn with two wooden knitting needles"))
j("o-palette", PHOTO.format("a small watercolour paint palette with a paintbrush"))
j("p-tower", PAPER.format("the Berlin TV tower (Fernsehturm) standing tall, simple iconic silhouette with its round sphere"), size="1152x2048")
j("p-table", "Top-down view of a long rectangular wooden craft table seen exactly from above, warm oak wood with visible grain, completely empty, flat even lighting, on a pure plain white background, no chairs, no people, no objects, no text.", size="1152x2048")
for k, who in enumerate(["a friendly young woman with curly dark hair in a claw clip and a mustard yellow cardigan over a terracotta top",
                         "a friendly young man with a short beard and a mustard beanie",
                         "a cheerful young woman wearing a sage green hijab and a terracotta sweater",
                         "a smiling older man with grey hair, round glasses and a deep green knit vest"]):
    j(f"p-person{k + 1}", PAPER.format(f"{who}, waist up, facing the viewer, smiling warmly"))
json.dump({"model": "black-forest-labs/flux.2-klein-4b", "workers": 8, "jobs": jobs}, open("gen1.json", "w"), indent=1)
json.dump({"model": "black-forest-labs/flux.2-klein-4b", "workers": 4, "jobs": [
    {"out": "img/p-person1-sad.jpg", "refs": ["img/p-person1.jpg"], "seed": 2, "size": "1152x1152",
     "prompt": "Keep this exact paper cut-out character and style, same hair, clothes, colours and paper texture, but now she looks lonely and a little sad, small frown, eyes looking down, shoulders slightly slumped. Pure plain white background, no text."},
    {"out": "img/p-person1-laugh.jpg", "refs": ["img/p-person1.jpg"], "seed": 3, "size": "1152x1152",
     "prompt": "Keep this exact paper cut-out character and style, same hair, clothes, colours and paper texture, but now she is laughing happily with eyes closed and one hand raised in a wave. Pure plain white background, no text."}]},
    open("gen2.json", "w"), indent=1)
print(len(jobs))
