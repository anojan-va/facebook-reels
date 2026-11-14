"""Image jobs for parable reels 71-80 (long-spoons … sour-grapes). Two candidates per shot. Writes <slug>/jobs.json.

Same conventions as jobs70.py: h0 = hook image, WORLD appended, roles spelled out per person in two-person shots."""
import json
from jobs25 import BOY, ONLY2, STAND, colored, hero
from jobs50 import WM, WORLD
from style_new import ANAT, MAN, OLD_MAN, scene

R = {}

HALL = "Setting: a huge banquet hall in thin white line art, one very long table covered with bowls of food. "
SP = "spoons with VERY long handles, longer than their arms"
R["long-spoons"] = [
    ("h0-feed", *colored(HALL, f"two people {WM} sit facing each other across the long table, each holding one of the {SP} and feeding the OTHER person across the table, both smiling. Only warm golden light has colour. " + ANAT)),
    ("l01-ask", *hero("man.jpg", MAN, "Setting: a misty place between two huge doors, one dark and one glowing, thin white line art. ", "the main character stands between the two huge doors, curious, looking from one to the other, both hands at his sides. " + STAND, alone=True)),
    ("l02-hell", *scene(HALL.replace("Setting:", "Setting: in gloomy dim light,"), f"a row of thin starving people {WM} sit at the long table full of food, each struggling to bring one of the {SP} to his own mouth and failing, food spilling, sad angry faces, each clearly apart. " + ANAT)),
    ("l03-spoon", *scene(HALL.replace("Setting:", "Setting: in gloomy dim light,"), f"close-up: a frustrated man {WM} holds one of the {SP} with food on its end far beyond his face, unable to reach his mouth. Only one person. " + ANAT)),
    ("l04-watch", *hero("man.jpg", MAN, HALL.replace("Setting:", "Setting: in gloomy dim light,"), "chest-up shot: the main character looks on sadly and confused, one hand on his chin.", alone=True)),
    ("l05-heaven", *colored(HALL.replace("Setting:", "Setting: in warm golden light,"), f"a row of happy healthy people {WM} sit at the long table, laughing, each feeding the person across the table with one of the {SP}, each clearly apart. Only the warm light has colour. " + ANAT)),
    ("l06-smile", *hero("man.jpg", MAN, HALL.replace("Setting:", "Setting: in warm golden light,"), "chest-up shot: the main character smiles in understanding, his right hand on his chest, warm light on his face.", alone=True)),
    ("k1-share", *hero("man.jpg", MAN, "Setting: a small home kitchen table at sunset in thin white line art. ", f"the main character smiles and holds a spoon of food out to feed a friend {WM} sitting across the table, who smiles back. " + ONLY2)),
]

FIELD = "Setting: a sunny meadow in thin white line art, tall grass, flowers, a small anthill. "
ANT = "a small ant drawn all in WHITE, NOT black-filled"
HOP = "a grasshopper drawn all in WHITE, NOT black-filled, NOT green"
R["ant-grasshopper"] = [
    ("h0-snow", *scene(FIELD.replace("a sunny meadow", "a snowy meadow in a blizzard").replace("flowers, ", ""), f"{HOP} shivers alone in deep snow, hugging itself, cold and hungry, icicles on its antennae. No people.")),
    ("a01-carry", *scene(FIELD, f"{ANT} carries a big grain of wheat on its back along a path toward the anthill, determined. No people.")),
    ("a02-line", *scene(FIELD, f"a long line of busy {ANT.replace('a small ant', 'small ants')} carry grains into the anthill under the summer sun. No people.")),
    ("a03-sing", *scene(FIELD, f"{HOP} lies on a leaf in the sun playing a tiny violin and singing happily, eyes closed, musical notes floating. No people.")),
    ("a04-laugh", *scene(FIELD, f"{HOP} laughs and points at {ANT} carrying a heavy grain, the ant ignoring it and walking on. No people.")),
    ("a05-winter", *scene(FIELD.replace("a sunny meadow", "a snowy meadow").replace("flowers, ", ""), "thick white snow covers the whole meadow, the anthill a small snowy mound, a cold wind blowing. No people.")),
    ("a06-warm", *colored("Setting: inside a cozy anthill tunnel in thin white line art, rooms full of stored grain. ", f"{ANT} sits warm and cozy beside a big pile of golden grain, a tiny warm glowing lamp. Only the lamp glow and grain have colour. No people.")),
    ("k1-hero", *hero("man.jpg", MAN, "Setting: a small study at night in thin white line art, a desk with books and a lamp. ", "the main character works focused at his desk at night, writing in a notebook with his right hand, his left hand holding the page, a determined calm face.", alone=True)),
]

TRACK = "Setting: a country race track through a meadow in thin white line art, a finish line ribbon, a big shady tree. "
HARE = "a fast hare drawn all in WHITE, NOT black-filled, NOT brown"
TORT = "a slow tortoise drawn all in WHITE with a white shell, NOT black-filled, NOT green"
R["tortoise-hare"] = [
    ("h0-finish", *scene(TRACK, f"{TORT} crosses the finish line, breaking the ribbon, calm and proud; far behind, {HARE} sprints in panic. No people.")),
    ("t01-mock", *scene(TRACK, f"{HARE} laughs and points at {TORT}, who looks back calmly. No people.")),
    ("t02-start", *scene(TRACK, f"{HARE} and {TORT} side by side at the start line, ready to race. No people.")),
    ("t03-zoom", *scene(TRACK, f"{HARE} dashes ahead at top speed with motion lines and a dust cloud; {TORT} is tiny far behind. No people.")),
    ("t04-nap", *scene(TRACK, f"{HARE} sleeps lazily under the big shady tree with arms behind its head, smiling, 'Zzz' bubbles. No people.")),
    ("t05-walk", *scene(TRACK, f"{TORT} walks slowly and steadily past the big tree where the hare sleeps, determined. No people.")),
    ("t06-wake", *scene(TRACK, f"{HARE} wakes up shocked, eyes wide, ears up, seeing the tortoise far ahead near the finish. No people.")),
    ("t07-run", *scene(TRACK, f"{HARE} runs as fast as it can, sweat flying, desperate. No people.")),
    ("k1-hero", *hero("man.jpg", MAN, "Setting: a long road toward a mountain at sunrise in thin white line art. ", "the main character walks steadily along the long road toward the mountain at sunrise, calm and determined, arms swinging naturally.", alone=True)),
]

AIR = "Setting: an airport waiting area in thin white line art, rows of seats, big windows with a plane outside. "
WOM = f"a woman {WM}, long white hair, a white coat, a handbag"
PACK = "an open pack of cookies"
R["cookie-thief"] = [
    ("h0-take", *hero("man.jpg", MAN, AIR, f"close-up: {PACK} on the seat between the main character and {WOM}; both reach for a cookie at the same moment; she glares at him angrily; he smiles kindly. " + ONLY2)),
    ("c01-sit", *scene(AIR, f"{WOM} sits alone on an airport seat with {PACK} on the seat beside her, reading a book. Only one person. " + ANAT)),
    ("c02-stranger", *hero("man.jpg", MAN, AIR, f"the main character sits down on the seat beside {WOM}; the open cookie pack is between them. " + ONLY2)),
    ("c03-he-takes", *hero("man.jpg", MAN, AIR, f"the main character takes a cookie from {PACK} between them and eats it calmly; {WOM} stares at him in shock. " + ONLY2)),
    ("c04-furious", *scene(AIR, f"chest-up shot: {WOM} looks furious, eyebrows down, chewing a cookie angrily. Only one person. " + ANAT)),
    ("c05-half", *hero("man.jpg", MAN, AIR, f"the main character smiles and holds out HALF of the last cookie to {WOM}, holding the other half himself. " + ONLY2)),
    ("c06-leave", *hero("man.jpg", MAN, AIR, "the main character walks away down the airport hall, smiling, a backpack on his back.", alone=True)),
    ("c07-bag", *scene("Setting: inside an airplane in thin white line art, seats and small windows. ", f"{WOM} sits in her plane seat holding open her handbag, inside it an UNOPENED full pack of cookies; she stares at it, shocked, a hand over her mouth. Only one person. " + ANAT)),
    ("k1-kind", *hero("man.jpg", MAN, "Setting: an airport window at sunset in thin white line art, a plane taking off. ", "chest-up shot: the main character looks out the window at a plane taking off, a warm kind smile.", alone=True)),
]

FOR = "Setting: a dense forest path in thin white line art, tall trees. "
FRIEND = f"his friend {WM}"
BEAR = "a huge bear drawn all in WHITE (white fur), NOT black-filled, NOT brown"
R["bear-friend"] = [
    ("h0-sniff", *hero("man.jpg", MAN, FOR, f"the main character lies flat on his back on the forest ground, eyes shut, holding his breath; {BEAR} leans down sniffing his ear.", alone=True)),
    ("f01-walk", *hero("man.jpg", MAN, FOR, f"the main character walks along the forest path with {FRIEND}, both chatting happily, side by side. " + ONLY2)),
    ("f02-bear", *scene(FOR, f"{BEAR} stands up on its hind legs on the path, roaring, huge and terrifying. No people.")),
    ("f03-climb", *scene(FOR, f"{FRIEND.replace('his friend', 'a man')} climbs a tall tree fast with both hands and feet gripping the trunk, looking down, scared. Only one person. " + ANAT)),
    ("f04-alone", *hero("man.jpg", MAN, FOR, "the main character stands alone on the path, terrified, looking up at the tree where his friend escaped, both hands raised in fear.", alone=True)),
    ("f05-leave", *scene(FOR, f"{BEAR} turns and walks away into the forest. No people.")),
    ("f06-down", *hero("man.jpg", MAN, FOR, f"{FRIEND} climbs down from the tree and asks a question with a nervous smile; the main character sits up on the ground, dusting himself off. " + ONLY2)),
    ("f07-answer", *hero("man.jpg", MAN, FOR, "chest-up shot: the main character looks at the viewer with a calm serious face, disappointed, a leaf in his hair.", alone=True)),
    ("k1-alone", *hero("man.jpg", MAN, FOR.replace("Setting:", "Setting: at sunset,"), "the main character walks alone out of the forest into the sunset, calm and wiser, arms relaxed.", alone=True)),
]

GARD = "Setting: a small garden behind a house at night in thin white line art, a moon. "
MISER = f"an old miser {WM}, thin, a long white beard, a white robe"
R["miser-gold"] = [
    ("h0-stare", *colored(GARD, f"{MISER} kneels by a hole in the ground and stares greedily at a lump of shining GOLD inside it, rubbing his hands. Only the gold has colour. Only one person. " + ANAT)),
    ("m01-sell", *scene("Setting: an empty house in thin white line art. ", f"{MISER} hands over furniture to buyers; his house is almost empty. Only one person. " + ANAT)),
    ("m02-bury", *colored(GARD, f"{MISER} buries a lump of shining GOLD in a hole with a shovel, looking around nervously. Only the gold has colour. Only one person. " + ANAT)),
    ("m03-visit", *colored(GARD.replace("at night", "in daylight"), f"{MISER} kneels and digs up the gold just to look at it, smiling. Only the gold has colour. Only one person. " + ANAT)),
    ("m04-thief", *scene(GARD, f"a sneaky thief {WM} with a white mask runs away carrying a sack over his shoulder past an empty hole. Only one person. " + ANAT)),
    ("m05-cry", *scene(GARD.replace("at night", "at dawn"), f"{MISER} kneels beside the empty hole, crying loudly, both hands on his head. Only one person. " + ANAT)),
    ("m06-neighbor", *hero("man.jpg", MAN, GARD.replace("at night", "at dawn"), f"the main character, the neighbour, stands over the fence calmly asking a question; {MISER} kneels crying by the empty hole. " + ONLY2)),
    ("m07-stone", *hero("man.jpg", MAN, GARD.replace("at night", "at dawn"), "chest-up shot: the main character holds up an ordinary grey stone in his right hand, a wise half-smile.", alone=True)),
    ("k1-share", *colored("Setting: a village street at sunset in thin white line art. ", "the main character in his mustard-YELLOW hoodie, black cargo pants and white sneakers, short brown beard, gives a gold coin to a smiling child drawn all in WHITE, both happy. Only the coin and the main character have colour.")),
]

HILL = "Setting: a grassy hillside above a small village in thin white line art. "
SHEEP = "fluffy sheep drawn all in WHITE, NOT black-filled"
VIL = f"villagers {WM} holding sticks"
WOLF = "a wolf drawn all in WHITE (white fur), NOT black-filled, sharp teeth"
R["cried-wolf"] = [
    ("h0-scream", *hero("boy.jpg", BOY, HILL.replace("Setting:", "Setting: at dusk,"), f"the small boy screams for help with both hands around his mouth while {WOLF} charges into a flock of {SHEEP} behind him; nobody comes.", alone=True)),
    ("w01-bored", *hero("boy.jpg", BOY, HILL, f"the small boy sits bored on a rock, chin in his hands, a flock of {SHEEP} grazing around him.", alone=True)),
    ("w02-shout", *hero("boy.jpg", BOY, HILL, "the small boy shouts with both hands cupped around his mouth, a mischievous grin.", alone=True)),
    ("w03-run", *scene(HILL, f"three {VIL} run up the hill in a hurry, worried, each clearly apart. " + ANAT)),
    ("w04-laugh", *hero("boy.jpg", BOY, HILL, "the small boy laughs, holding his belly, pointing down the hill.", alone=True)),
    ("w05-angry", *scene(HILL, f"three {VIL} stand angry and tired with arms crossed, frowning. " + ANAT)),
    ("w06-wolf", *scene(HILL.replace("Setting:", "Setting: at dusk,"), f"{WOLF} creeps out of the bushes toward a flock of {SHEEP}, eyes glowing. No people.")),
    ("w07-nobody", *scene("Setting: a small village at dusk in thin white line art, houses with lit windows. ", f"villagers {WM} inside their houses ignore the distant shouting, shaking their heads. " + ANAT)),
    ("k1-sad", *hero("boy.jpg", BOY, HILL.replace("Setting:", "Setting: at night,"), "the small boy sits alone on the empty hill at night, crying, hugging his knees.", alone=True)),
]

HOT = "Setting: a hot dry land in thin white line art, cracked ground, a blazing sun, a dead tree. "
CROW = "a crow drawn all in WHITE (white feathers), NOT black-filled"
PITCH = "a tall WHITE clay pitcher with a narrow top"
R["thirsty-crow"] = [
    ("h0-pebble", *scene(HOT, f"close-up: {CROW} drops a small pebble from its beak into {PITCH}, water level rising inside. No people.")),
    ("c01-search", *scene(HOT, f"{CROW} flies tired over the cracked dry land under the blazing sun, beak open, thirsty. No people.")),
    ("c02-found", *scene(HOT, f"{CROW} lands next to {PITCH} standing on the ground, excited. No people.")),
    ("c03-low", *scene(HOT, f"cross-section view: {PITCH} with only a little water at the very bottom; {CROW}'s beak cannot reach it. No people.")),
    ("c04-push", *scene(HOT, f"{CROW} pushes against {PITCH} with its body, straining, the pitcher not moving. No people.")),
    ("c05-think", *scene(HOT, f"{CROW} stands thinking, head tilted, looking at a pile of small pebbles on the ground. No people.")),
    ("c06-rise", *scene(HOT, f"cross-section view: {PITCH} filled with pebbles and the water risen almost to the top. No people.")),
    ("c07-drink", *scene(HOT, f"{CROW} drinks happily from the top of {PITCH}, water drops sparkling. No people.")),
    ("k1-hero", *hero("man.jpg", MAN, "Setting: a desk at night in thin white line art, a lamp, scattered papers. ", "the main character smiles with a bright idea, pointing his right index finger up, a small glowing light bulb above his head.", alone=True)),
]

PAL = "Setting: an ancient Chinese palace courtyard in thin white line art, red-less white pillars, a throne. "
EMP = f"an old emperor {WM}, a long white beard, a white robe and a white crown"
KIDS = f"children {WM}"
R["empty-pot"] = [
    ("h0-pot", *hero("boy.jpg", BOY, PAL, "the small boy stands alone holding an EMPTY white flower pot with only soil in it, head down, ashamed, while other children's colourful flowers surround him.", alone=True)),
    ("p01-seeds", *scene(PAL, f"{EMP} hands out tiny seeds to a line of {KIDS}, each standing clearly apart. " + ANAT)),
    ("p02-plant", *hero("boy.jpg", BOY, "Setting: a small poor home in thin white line art, a window. ", "the small boy plants a seed in a white flower pot with both hands, hopeful.", alone=True)),
    ("p03-water", *hero("boy.jpg", BOY, "Setting: a small poor home in thin white line art, a window. ", "the small boy waters the white flower pot carefully with a small watering can, nothing growing in it.", alone=True)),
    ("p04-nothing", *hero("boy.jpg", BOY, "Setting: a small poor home in thin white line art, a window. ", "the small boy sits sadly looking at the empty pot with only soil in it, worried.", alone=True)),
    ("p05-flowers", *colored(PAL, f"a line of proud {KIDS} hold pots with big colourful flowers, smiling, each standing clearly apart. Only the flowers have colour. " + ANAT)),
    ("p06-smile", *scene(PAL, f"{EMP} sits on his throne smiling warmly and pointing at someone in front of him. Only one person. " + ANAT)),
    ("p07-boiled", *scene(PAL, f"close-up: a small white pot of steaming boiling water with tiny seeds inside. No people.")),
    ("k1-crown", *hero("boy.jpg", BOY, PAL.replace("Setting:", "Setting: at sunset,"), "the small boy stands proudly on the palace steps wearing a small golden crown, holding his empty pot, smiling.", alone=True)),
]

VINE = "Setting: a vineyard in thin white line art, a tall vine with leaves on a wooden frame. "
FOX = "a fox drawn all in WHITE (white fur), NOT black-filled, NOT orange"
GRAPES = "a bunch of juicy PURPLE grapes hanging high up"
R["sour-grapes"] = [
    ("h0-nose", *colored(VINE, f"{FOX} walks away with its nose turned up in the air, eyes closed, pretending not to care; behind it, {GRAPES}. Only the grapes have colour. No people.")),
    ("g01-see", *colored(VINE, f"{FOX} looks up hungrily at {GRAPES}, licking its lips. Only the grapes have colour. No people.")),
    ("g02-jump", *colored(VINE, f"{FOX} leaps up toward {GRAPES}, paws stretched, but falls short. Only the grapes have colour. No people.")),
    ("g03-higher", *colored(VINE, f"{FOX} jumps even higher toward {GRAPES}, still missing by a little. Only the grapes have colour. No people.")),
    ("g04-tired", *colored(VINE, f"{FOX} lies on the ground exhausted, panting, tongue out; {GRAPES} above. Only the grapes have colour. No people.")),
    ("k0-hero", *hero("man.jpg", MAN, "Setting: a city street in thin white line art, a tall office building. ", "the main character shrugs and turns away from a tall office building with his hands in his pockets, pretending not to care, a slightly sad face.", alone=True)),
    ("k1-reach", *colored(VINE.replace("Setting:", "Setting: at sunrise,"), "the main character in his mustard-YELLOW hoodie, black cargo pants and white sneakers, short brown beard, stands on a wooden box reaching up with his right hand toward a bunch of purple grapes, determined. Only the grapes and the main character have colour.")),
]

if __name__ == "__main__":
    for n, (slug, jobs) in enumerate(R.items()):
        js = [{"out": f"img/cand/{o}-{k}.jpg", "refs": r, "seed": 24000 + 37 * n + 2 * i + (k == "b"), "prompt": p + WORLD}
              for i, (o, p, r) in enumerate(jobs) for k in "ab"]
        json.dump({"model": "black-forest-labs/flux.2-klein-4b", "size": "1152x2048", "workers": 2, "jobs": js},
                  open(f"{slug}/jobs.json", "w"), indent=1)
        print(slug, len(js))
