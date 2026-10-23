"""Image jobs for parable reels 16-20 (two-wolves … empty-cup). Writes <slug>/jobs.json."""
import json
from style_new import ANAT, PEOPLE, SAME, WHITE_MAN, man_scene, scene, REF, HOUSE, MAN

W = WHITE_MAN
STAND = "He stands still with both feet flat on the ground side by side. "
ALONE = "He is completely ALONE in the image: no other people, no figures, no silhouettes anywhere. "
TWO = "Exactly TWO arms and TWO hands, each attached to his own shoulder; no extra arm, hand or finger anywhere. "
BOY = "a small boy about eight years old drawn all in WHITE with white clothes, a child, much smaller than the man"
COLOR = ("Minimalist illustration on a pure black background, clean thin white line art with no shading. Everything is white "
         "line art except the colours described. No text, letters or captions. Vertical 9:16 composition. ")
def colored(setting, sc):
    return COLOR + setting + "Scene: " + sc, []
def alone(setting, sc):
    return REF + HOUSE + MAN + ANAT + ALONE + TWO + setting + "Scene: " + sc, ["../refs/man.jpg"]

R = {}
CAMP = "Setting: a forest clearing at night in thin white line art, tall pine trees, stars, a small campfire with warm orange flames. "
R["two-wolves"] = [
    ("a01-fire", *man_scene(CAMP, f"the main character sits cross-legged on a log on the left of the campfire, telling a story with one open hand; on the right sits {BOY} on a smaller log, listening. Both seated clearly apart, each with two arms and two legs. " + TWO)),
    ("a02-wolves", *colored(CAMP, "in the smoke rising above the campfire, two big wolf heads appear facing each other: on the left a wolf drawn in white lines with glowing RED eyes and bared teeth; on the right a calm wolf glowing soft GOLD. No people. Only the red eyes and the golden wolf have colour.")),
    ("a03-dark", *colored("Setting: swirling smoke on a black background. ", "close-up of a snarling wolf drawn in white line art with glowing RED eyes, bared fangs, raised fur, angry. No people. Only the eyes are red.")),
    ("a04-gold", *colored("Setting: swirling smoke on a black background. ", "close-up of a calm noble wolf glowing soft warm GOLD, gentle kind eyes, sitting peacefully. No people. Only the golden wolf has colour.")),
    ("a05-boy", *scene(CAMP, f"close-up of {BOY}, sitting by the fire, looking up worried, both hands holding his knees. " + ANAT)),
    ("a06-smile", *alone(CAMP, "close-up from the chest up: he smiles calmly and wisely, warm firelight glowing on his face, both hands resting together in front of him.")),
    ("a07-phone", *alone("Setting: a dark bedroom at night in thin white line art. ", "he sits on the edge of the bed hunched over his phone held in both hands, an angry frowning face, the phone screen glowing red, small angry symbols floating above it.")),
    ("a08-book", *alone("Setting: a window seat at sunrise in thin white line art, a big rising sun through the window. ", "he sits by the window reading a book held open in both hands, calm and content, sunlight on his face.")),
    ("k1-feed", *alone(CAMP, "he kneels on both knees by the campfire and gently offers food from his open right hand to the calm golden wolf sitting beside him; his left hand rests on his knee.", )),
    ("k2-walk", *alone("Setting: a forest path at sunrise in thin white line art. ", "he walks calmly along the path into the sunrise, the calm golden wolf walking beside him. " + STAND.replace("stands still", "walks steadily"))),
]
GARDEN = "Setting: a garden in soft morning light in thin white line art, leafy branches, flowers. "
R["butterfly"] = [
    ("b01-cocoon", *alone(GARDEN, "he kneels on both knees beside a low branch, looking closely at a white cocoon hanging from it, curious, both hands resting on his knees.")),
    ("b02-hole", *scene(GARDEN, "close-up of a white cocoon hanging from a branch with a tiny hole at the bottom; a small butterfly drawn in WHITE pushes its head and one leg through the tiny hole, struggling, little effort lines. No people.")),
    ("b03-scissors", *alone(GARDEN, "close-up from the chest up: he holds a small pair of scissors in his right hand near the cocoon on the branch, a kind gentle face; his left hand holds the branch steady.")),
    ("b04-crumpled", *scene(GARDEN, "close-up: a butterfly drawn in WHITE has come out of the cut-open cocoon; its body is swollen and its wings are tiny, wrinkled and crumpled. No people.")),
    ("b05-ground", *alone(GARDEN, "he kneels on both knees looking down in shock, both hands raised slightly in surprise, at a small white butterfly crawling on the ground with tiny crumpled wings, unable to fly.")),
    ("b06-diagram", *colored("Setting: plain black background. ", "a simple glowing white line diagram: a butterfly squeezing out of a cocoon, with glowing golden arrows showing fluid flowing from its body into its large, wide, strong open wings. Clean scientific illustration style. No people. Only the arrows are golden.")),
    ("b07-climb", *alone("Setting: a steep rocky hill at sunset in thin white line art, a big setting sun. ", "he climbs a steep rocky path, one foot on a higher rock, both hands gripping a rock above him, determined and strong.")),
    ("k1-fly", *alone("Setting: the top of a rocky hill at sunset in thin white line art. ", "he stands on the hilltop with both arms spread wide open, a big smile, a large white butterfly with wide strong wings flying up beside him into the sky. " + STAND)),
]
FARMH = "Setting: a farmhouse yard in thin white line art: a wooden house with a door, a long wooden fence. "
R["nails-fence"] = [
    ("c01-slam", *man_scene(FARMH, f"{BOY} stomps out of the house slamming the door behind him, an angry face, fists clenched; the main character stands on the porch watching calmly. " + TWO)),
    ("c02-nails", *man_scene(FARMH, f"the main character kneels on both knees to the boy's height and hands {BOY} a small bag of nails with his right hand, pointing at the wooden fence with his left hand. The boy holds a hammer. " + TWO)),
    ("c03-full", *scene(FARMH, "close-up of a long wooden fence board covered with dozens of nails hammered in everywhere, a hammer lying on the ground below. No people.")),
    ("c04-calm", *scene(FARMH, f"{BOY} stands by the fence with his eyes closed, taking a deep calm breath, both hands relaxed at his sides, a hammer leaning on the fence. " + ANAT)),
    ("c05-pull", *man_scene(FARMH, f"the main character stands beside {BOY}, smiling, one hand on the boy's shoulder; the boy pulls a nail out of the fence with the claw of a hammer held in both hands. " + TWO)),
    ("c06-holes", *scene(FARMH, "close-up of the wooden fence board with no nails left but covered in many small dark holes where the nails were. No people.")),
    ("c07-touch", *man_scene(FARMH, f"the main character crouches beside {BOY} at the fence and touches one of the nail holes with his right index finger, explaining gently; the boy looks at the holes, thoughtful. " + TWO)),
    ("c08-hurt", *man_scene("Setting: a living room in thin white line art. ", f"after an argument: the main character stands on the left with a regretful face, both hands at his sides; on the right his friend, {W}, turns away with a hurt sad face, arms crossed. " + SAME)),
    ("k1-sorry", *man_scene("Setting: a living room in thin white line art. ", f"the main character gently puts one hand on his friend's shoulder, apologising sincerely; the friend, {W}, listens, softening. " + SAME + TWO)),
    ("k2-fence", *alone(FARMH + "Sunset. ", "he stands thoughtfully beside the wooden fence full of small holes, one hand resting on top of the fence, the other at his side. " + STAND)),
]
MANS = "Setting: a grand mansion interior in thin white line art: tall arched windows, a marble floor, a chandelier. "
RICH = "a rich man drawn all in WHITE wearing a white suit and a white bow tie"
R["window-mirror"] = [
    ("d01-arrive", *man_scene(MANS, f"{RICH} walks in through the grand doors to visit the main character, who greets him calmly with an open hand. " + SAME + TWO)),
    ("d02-window", *man_scene(MANS, f"the main character leads {RICH} to a tall window, pointing out through it with his right hand; the rich man looks through. Seen from behind, both standing. " + SAME + TWO)),
    ("d03-street", *scene("Setting: a view through a tall window frame in thin white line art. ", "through the window: a busy street below with children playing, families walking, people working at market stalls, all drawn in WHITE, standing clearly apart. " + PEOPLE + ANAT)),
    ("d04-mirror", *man_scene(MANS, f"the main character leads {RICH} to a tall ornate mirror on the wall, gesturing at it with his right hand. " + SAME + TWO)),
    ("d05-self", *scene(MANS, f"{RICH} stands alone facing a tall ornate mirror; in the mirror we see only his own white reflection staring back, nothing else. " + ANAT)),
    ("d06-wise", *alone(MANS, "close-up from the chest up: he speaks wisely with a calm gentle smile, holding up a small shiny silver coin between the finger and thumb of his right hand.")),
    ("d07-ashamed", *scene(MANS, f"{RICH} stands silent in front of the mirror, head lowered, ashamed, both hands at his sides. " + ANAT)),
    ("k1-window", *man_scene(MANS + "Sunrise light through the window. ", f"the main character and {RICH} stand side by side at the open window, both smiling and looking out at the people in the street. Seen from behind. " + SAME)),
]
TEMPLE = "Setting: a mountain temple at sunrise in thin white line art: a wooden temple room with a low table, sliding doors open to mountains. "
SCH = "a proud scholar drawn all in WHITE with white robes and glasses"
R["empty-cup"] = [
    ("e01-arrive", *man_scene(TEMPLE, f"{SCH} arrives at the temple door with his nose in the air; the main character greets him calmly with a small bow, hands together. " + SAME + TWO)),
    ("e02-talk", *man_scene(TEMPLE, f"both sit on cushions at the low table: {SCH} on the right talks nonstop with both hands waving in the air; the main character on the left sits calmly listening, hands resting on his knees. " + TWO)),
    ("e03-pour", *alone(TEMPLE, "he sits at the low table and quietly pours tea from a white teapot held in his right hand into a white cup; his left hand rests on the table.")),
    ("e04-overflow", *scene(TEMPLE, "close-up of a white teacup on the low table overflowing, tea spilling over the rim and across the table, a white teapot still pouring from above. No people.")),
    ("e05-stop", *scene(TEMPLE, f"{SCH} jumps up from his cushion, both hands raised in alarm, mouth open shouting 'Stop!', shocked face. " + ANAT)),
    ("e06-calm", *alone(TEMPLE, "he calmly sets the white teapot down on the table with his right hand, a gentle knowing smile; his left hand rests on his knee.")),
    ("e07-close", *alone(TEMPLE, "close-up from the chest up: he speaks gently with a warm wise smile, holding an empty white teacup in both hands in front of him.")),
    ("k1-empty", *man_scene(TEMPLE, f"the main character and {SCH} sit together at the low table, the scholar now listening humbly with an empty cup in front of him; the main character smiles. " + TWO)),
    ("k2-sunrise", *alone(TEMPLE.replace("a wooden temple room", "a temple balcony"), "he stands on the temple balcony holding an empty white cup in both hands, looking out at the sunrise over the mountains, calm and open. " + STAND)),
]

if __name__ == "__main__":
    n = 0
    for slug, jobs in R.items():
        js = [{"out": f"img/{o}.jpg", "refs": r, "seed": 3000 + 13 * n + i, "prompt": p} for i, (o, p, r) in enumerate(jobs)]
        n += 1
        json.dump({"model": "black-forest-labs/flux.2-klein-4b", "size": "1152x2048", "workers": 2, "jobs": js},
                  open(f"{slug}/jobs.json", "w"), indent=1)
        print(slug, len(js))
