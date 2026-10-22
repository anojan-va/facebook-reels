"""Image jobs for parable reels 11-15 (donkey-well … stonecutter). Writes <slug>/jobs.json."""
import json
from style_new import ANAT, PEOPLE, SAME, WHITE_MAN, man_scene, scene, REF, HOUSE, MAN

W = WHITE_MAN
STAND = "He stands still with both feet flat on the ground side by side. "
ALONE = "He is completely ALONE in the image: no other people, no figures, no silhouettes anywhere. "
def alone(setting, sc):
    return REF + HOUSE + MAN + ANAT + ALONE + setting + "Scene: " + sc, ["../refs/man.jpg"]

DONKEY = "an old donkey drawn all in solid WHITE, four legs, long ears"
R = {}
V = "Setting: a small village at dusk in thin white line art: huts, a dry stone well with a wooden frame, a low moon. "
WELL = "Setting: inside a deep round stone well in thin white line art, stone walls all around, a circle of dusk sky at the top. "
R["donkey-well"] = [
    ("a01-fall", *scene(V, f"close-up of the stone well; deep inside, {DONKEY} looks up and brays, its mouth open, scared. No people.")),
    ("a02-farmer", *scene(V, f"{W}, an old farmer with a straw hat, leans over the edge of the well looking down, shaking his head, holding a rope. " + ANAT)),
    ("a03-shovel", *scene(V, "four villagers drawn all in WHITE stand around the well, each throwing a shovel of dirt into it, standing clearly apart. " + PEOPLE + ANAT)),
    ("a04-shake", *scene(WELL, f"looking down into the well: {DONKEY} shakes dirt off its back, a cloud of dust flying off, its front hooves stepping up onto a pile of dirt. No people.")),
    ("a05-higher", *scene(WELL, f"{DONKEY} stands high up on a tall mound of dirt inside the well, close to the top, the rim of the well just above its head. No people.")),
    ("a06-out", *scene(V, f"{DONKEY} steps out over the rim of the well onto the ground; villagers drawn all in WHITE stand frozen in shock holding their shovels, mouths open. " + PEOPLE + ANAT)),
    ("a07-gossip", *man_scene("Setting: a village street in thin white line art. ", "the main character walks calmly down the street, looking ahead; on both sides villagers drawn all in WHITE whisper behind their hands and point at him, standing clearly apart. " + STAND.replace("stands still", "walks slowly"))),
    ("k1-shake", *alone("Setting: a village street in thin white line art. ", "medium shot from the waist up: he brushes dust off his shoulder with one hand, a small cloud of dust flying away, a calm confident smile.")),
    ("k2-higher", *alone("Setting: hills at sunrise in thin white line art, a big rising sun. ", "he stands on top of a hill, relaxed and proud, looking out at the sunrise. " + STAND)),
]

SHOP = "Setting: a carpenter's workshop at sunset in thin white line art: a workbench, hand tools on the wall, planks of wood. "
LOT = "Setting: a building plot at the edge of a village in thin white line art. "
R["carpenter-house"] = [
    ("b01-tools", *alone(SHOP, "he stands at the workbench and puts down his hammer and saw with a tired, decided face. " + STAND)),
    ("b02-boss", *man_scene(SHOP, f"his boss, {W} in a white shirt, stands facing him and puts one hand on his shoulder, asking kindly. " + SAME)),
    ("b03-lazy", *alone(LOT, "he hammers a crooked nail into a cheap cracked plank lazily, yawning, a bored face, a half-built wooden house frame behind him.")),
    ("b04-house", *scene(LOT, "a small finished wooden house drawn in white line art that looks weak and crooked: a leaning wall, a sagging roof, gaps between cheap planks, a crooked door. No people.")),
    ("b05-keys", *man_scene(LOT, f"in front of the crooked house, the boss, {W}, smiles and hands a set of house keys to the main character, who holds out his open hand. " + SAME)),
    ("b06-shock", *alone(LOT, "close-up from the chest up: he stares at the keys in his hand, shocked, eyes wide, mouth open, his hand trembling.")),
    ("b07-phone", *alone("Setting: an office at night in thin white line art: a desk, a laptop, a lamp. ", "he slumps at the desk half-asleep, scrolling his phone with one hand, the laptop ignored, a bored lazy face. He sits on a chair.")),
    ("k1-build", *alone(SHOP, "he carefully measures a fine straight plank with a ruler and pencil, focused and proud, good tools neatly laid out. " + STAND)),
    ("k2-home", *alone(LOT + "Golden sunset. ", "he stands smiling in front of a beautiful solid wooden house with a straight roof, neat windows and a flower box, holding the keys. " + STAND)),
]

PATH = "Setting: a village dirt path at dawn in thin white line art, a stream in the distance. "
POLE = "he carries a wooden pole across his shoulders with a clay pot hanging from each end, both pots drawn in WHITE. "
R["cracked-pot"] = [
    ("c01-carry", *alone(PATH, "wide shot: " + POLE + "He walks along the path. " + STAND.replace("stands still", "walks steadily"))),
    ("c02-pots", *scene(PATH, "close-up of two white clay pots hanging side by side from a wooden pole: the left pot is perfect; the right pot has a long crack and water drips out of it onto the path. No people.")),
    ("c03-sad", *scene(PATH, "close-up of one white clay pot with a crack, a small sad cartoon face drawn on the clay, a tear-like water drop running down the crack. No people.")),
    ("c04-sorry", *scene("Setting: a plain black background. ", "close-up of one white clay pot with a crack and a small sad cartoon face drawn on the clay, looking down, apologetic. Empty dark space above it. No people.")),
    ("c05-point", *alone(PATH, "he smiles kindly and points at the path with one hand, the pole with the two white pots resting on his shoulder. " + STAND)),
    ("c06-flowers", *scene(PATH, "wide shot looking down the path: on the right side of the path many flowers bloom in white line art all along the edge; on the left side the ground is bare. No people.")),
    ("c07-close", *alone(PATH, "close-up from the chest up: he smiles warmly, holding the cracked white pot gently in both arms.")),
    ("k1-path", *alone(PATH + "Sunrise. ", "he walks happily along the path lined with blooming white flowers, carrying the two white pots on the pole across his shoulders. " + STAND.replace("stands still", "walks steadily"))),
]

FARM = "Setting: a farm at sunset in thin white line art: a wooden fence, a small barn, fields. "
HORSE = "horse drawn all in solid WHITE, four legs"
R["good-luck"] = [
    ("d01-fence", *alone(FARM, "he stands calmly beside an empty corral with a broken open gate, looking at the empty field. " + STAND)),
    ("d02-neighbors", *man_scene(FARM, "three neighbours drawn all in WHITE shake their heads at him, sad faces; he stands calm with a small shrug, standing clearly apart from them. " + STAND)),
    ("d03-horses", *scene(FARM, f"a {HORSE} gallops back toward the farm leading three wild horses, all drawn in solid WHITE, dust behind them. No people.")),
    ("d04-cheer", *man_scene(FARM, "the neighbours drawn all in WHITE cheer with raised arms beside the corral full of white horses; he stands calm with a small smile. " + STAND)),
    ("d05-cast", *man_scene("Setting: inside a simple farmhouse in thin white line art. ", f"his son, a young man drawn all in WHITE, sits on a bed with one leg in a white plaster cast resting on a stool; the main character stands beside him, calm, a hand on his shoulder.")),
    ("d06-army", *scene("Setting: a village street in thin white line art. ", "a line of soldiers drawn all in WHITE with spears marches through the village, leading young men away, each soldier standing clearly apart. " + PEOPLE + ANAT)),
    ("d07-passed", *scene("Setting: inside a simple farmhouse in thin white line art, a doorway. ", "through the open doorway soldiers drawn all in WHITE walk past outside without stopping; inside, a young man drawn all in WHITE sits on a bed with his leg in a plaster cast. " + ANAT)),
    ("d08-tea", *alone(FARM, "he sits calmly on a wooden bench drinking a cup of tea, peaceful face, white horses grazing in the field behind him.")),
    ("k1-sunset", *man_scene(FARM + "A big golden sunset. ", "the main character and his son (drawn all in WHITE, leg healed) lean side by side on the fence watching the white horses at sunset, calm and content. " + SAME)),
]

MT = "Setting: a rocky mountainside on a hot day in thin white line art, a blazing sun. "
R["stonecutter"] = [
    ("e01-hammer", *alone(MT, "he swings a hammer and chisel at a huge rock face, sweating, sweat drops flying, tired. Both feet planted wide apart on the rocks.")),
    ("e02-merchant", *man_scene("Setting: a dusty road in thin white line art. ", f"a rich merchant, {W} in fine white robes, rides past in a fancy white horse-drawn cart; the main character stands by the road holding his hammer, watching with longing. " + STAND)),
    ("e03-rich", *alone("Setting: a fancy courtyard in thin white line art. ", "he wears a fine white merchant's robe over his yellow hoodie and a jewelled cap, standing proudly, counting gold coins. " + STAND)),
    ("e04-king", *man_scene("Setting: a dusty road in thin white line art. ", "the main character, in a white merchant's robe over his yellow hoodie, bows low by the road as a royal procession passes: a king drawn all in WHITE on a white elephant with servants. " + PEOPLE)),
    ("e05-crown", *alone(MT.replace("a rocky mountainside", "a palace balcony") , "he wears a gold crown and a royal white cape over his yellow hoodie, sweating under the blazing sun, shielding his eyes with one hand. " + STAND)),
    ("e06-sun", *scene("Setting: the sky. ", "a huge blazing sun drawn in white line art with rays, a big white cloud drifting in front of it and covering half of it, wind lines blowing the cloud. No people.")),
    ("e07-mountain", *scene("Setting: a landscape in thin white line art. ", "a giant solid mountain drawn in white line art, strong winds and swirling cloud lines blowing against it, the mountain unmoved. No people.")),
    ("e08-tap", *scene("Setting: the foot of a giant mountain in thin white line art. ", f"at the foot of the huge mountain, a tiny {W.replace('a man','man')} with a hammer and chisel chips at the rock, small pieces of stone flying. " + ANAT)),
    ("e09-cutter", *scene("Setting: a rocky mountainside in thin white line art. ", f"close-up from the chest up of a humble stonecutter, {W}, sweating, holding a hammer, a determined face. " + ANAT)),
    ("k1-proud", *alone(MT.replace("on a hot day", "at sunset"), "he stands proudly on a big rock with his hammer resting on his shoulder, a calm confident smile, the mountain behind him. " + STAND)),
]

if __name__ == "__main__":
    n = 0
    for slug, jobs in R.items():
        js = [{"out": f"img/{o}.jpg", "refs": r, "seed": 2000 + 13 * n + i, "prompt": p} for i, (o, p, r) in enumerate(jobs)]
        n += 1
        json.dump({"model": "black-forest-labs/flux.2-klein-4b", "size": "1152x2048", "workers": 2, "jobs": js},
                  open(f"{slug}/jobs.json", "w"), indent=1)
        print(slug, len(js))
