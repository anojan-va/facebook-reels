"""Image jobs for the 10 parable reels (move-in-silence … silence-reply). Writes <slug>/jobs.json."""
import json
from style_new import ANAT, PEOPLE, SAME, WHITE_MAN, man_scene, scene

W = WHITE_MAN
R = {}

V = "Setting: a small village street at dusk in thin white line art: a tiny tea shop with a tin roof, wooden benches, hanging bulbs, small houses. "
VN = "Setting: a small bare room in a village house at night in thin white line art: one bare light bulb hanging over a wooden table. "
VM = "Setting: the same village street on a bright morning in thin white line art: small shops with metal roller shutters. "
R["move-in-silence"] = [
    ("a01-teashop", *man_scene(V, f"wide shot at the tea shop, two friends sit on a bench with tea glasses: on the right {W}, who talks loudly with big excited arm gestures; on the left the main character listens quietly with a small smile. " + SAME)),
    ("a02-crowd", *scene(V, f"{W} stands in the middle telling a crowd of villagers about his plans with big gestures; the villagers around him laugh and point at him. " + PEOPLE + ANAT)),
    ("a03-talker", *scene(V, f"close-up of {W}, talking excitedly with one hand raised, eyes wide, mouth open, boasting. " + ANAT)),
    ("a04-coins", *man_scene(VN, "the main character sits alone at the wooden table under the single bulb, counting a small pile of coins with both hands, focused and quiet. Nobody else.")),
    ("a05-whisper", *scene(V, f"{W} stands in the foreground looking doubtful and unsure, while behind him villagers whisper to each other behind their hands, glancing at him. " + PEOPLE + ANAT)),
    ("a06-doubt", *scene(V, f"close-up of {W}, worried doubtful face, eyebrows pulled together, looking down. " + ANAT)),
    ("a07-stall", *scene("Setting: a village street in heavy rain at night in thin white line art. ", "an empty abandoned wooden market stall in the rain, a torn awning, an overturned stool, puddles. No people.")),
    ("a08-shop", *man_scene(VM, "the main character lifts the metal roller shutter of a bright new shop full of goods, smiling; across the street a crowd of villagers stares at him in shock, mouths open. " + PEOPLE)),
    ("a09-smile", *man_scene(VM, "close-up of the main character's head and shoulders, a calm quiet confident smile, looking at the viewer. Nobody else.")),
]

D = "Setting: a wooden fishing dock at sunset in thin white line art, the sea and a low sun on the horizon. "
RM = "Setting: a small bedroom at night in thin white line art: a desk with a lamp and stacks of books, a door, a window. "
R["crab-bucket"] = [
    ("b01-bucket", *scene(D, "close view of a fisherman's metal bucket full of many crabs drawn in white line art, standing on the dock planks. No people.")),
    ("b02-climb", *scene(D, "close-up: one crab climbs up the inside wall of the bucket and reaches the rim with its claws. No people.")),
    ("b03-pull", *scene(D, "close-up: inside the bucket, several crabs grab the legs of the crab that is climbing and pull it back down with their claws. No people.")),
    ("b04-study", *man_scene(RM, "the main character sits at the desk studying a book by lamplight; through the window, outside, a group of friends at a party wave at him to come out.")),
    ("b05-mock", *man_scene(RM, "the main character stands at his open door; outside in the hallway a group of friends mock him, laughing and pointing at him. Empty dark space above the friends' heads. " + PEOPLE)),
    ("b06-door", *man_scene(RM, "the main character gently closes his bedroom door from the inside, calm face, one hand on the door handle. Nobody else.")),
    ("b07-focus", *man_scene(RM, "close-up of the main character at the desk, reading a book with a focused determined face, lamp light on his face. Nobody else.")),
    ("b08-hill", *man_scene("Setting: grassy hills at sunrise in thin white line art, a big rising sun on the horizon. ", "very wide shot, the main character walks alone up a path on a hill toward the rising sun, seen from behind, small in the frame.")),
]

F = "Setting: a dry village during a drought in thin white line art: cracked earth, dead trees, small huts. "
FF = "Setting: farmland in thin white line art. "
R["seeds-or-food"] = [
    ("c01-king", *man_scene(F, f"a king's wooden cart pulled by an ox stops in the village; a royal servant hands a sack of seeds to the main character and another sack to {W}. Hungry villagers watch. " + SAME)),
    ("c02-cook", *scene(F, f"at night {W} sits by a small cooking fire, cooking the seeds in a pot and eating happily from a bowl. " + ANAT)),
    ("c03-plant", *man_scene(F, "the main character, thin and tired, kneels in the dry cracked soil planting seeds one by one with his hands. Nobody else.")),
    ("c04-laugh", *man_scene(F, f"the main character sits eating from a very small bowl; next to him {W} points at him and laughs. " + SAME)),
    ("c05-empty", *scene(F, f"months later, {W} sits on the ground holding an empty sack upside down, sad hungry face. " + ANAT)),
    ("c06-field", *man_scene(FF + "A low sun at sunset. ", "the main character stands proudly in a huge field full of tall ripe wheat, the field stretching to the horizon.")),
    ("c07-basket", *man_scene(FF, f"the main character kindly hands a big basket full of grain to {W}, who takes it with a humble grateful face. " + SAME)),
]

ST = "Setting: a city street in thin white line art: shop fronts, a lamp post, a bench. "
R["umbrella"] = [
    ("d01-rain", *man_scene(ST + "Heavy rain falls. ", "the main character stands on the street holding a big open umbrella, rain all around.")),
    ("d02-crowd", *man_scene(ST + "Heavy rain falls. ", "under the main character's big open umbrella five people crowd close around him, smiling at him, staying dry. " + PEOPLE)),
    ("d03-sun", *man_scene(ST + "A sunny day. ", "the main character stands with his umbrella closed while people walk past him without looking at him, ignoring him. " + PEOPLE)),
    ("d04-bench", *man_scene(ST + "A grey day. ", "the main character sits alone on the bench, his closed umbrella leaning beside him, lonely. Nobody else.")),
    ("d05-realize", *man_scene(ST, "close-up of the main character holding his closed umbrella, looking at it with a face of sudden understanding. Nobody else.")),
    ("d06-friend", *man_scene(ST + "A sunny day. ", f"the main character walks along the street laughing with one friend, {W}, the umbrella tucked under his arm. " + SAME)),
]

B = "Setting: a small field at the edge of a village in thin white line art, a wooden fence. "
R["bamboo"] = [
    ("e01-plant", *man_scene(B + "Dawn. ", "the main character kneels and plants one seed in the soil, a small watering can beside him. Nobody else.")),
    ("e02-water", *man_scene(B, "the main character waters a bare patch of soil where nothing grows; behind the fence neighbours laugh at him and point. " + PEOPLE)),
    ("e03-rain", *man_scene(B + "Heavy rain. ", "the main character, tired and soaked, keeps watering the bare patch of soil in the rain. Nobody else.")),
    ("e03b-snow", *man_scene(B + "Snow falls, snow on the ground. ", "the main character, tired, in the snow, keeps watering the bare patch of soil. Nobody else.")),
    ("e04-roots", *scene("", "underground cross-section: a thin strip of soil surface at the top of the frame with nothing growing, and below it a huge network of softly glowing white roots spreading deep and wide through the earth. No people.")),
    ("e05-tower", *man_scene(B, "giant bamboo stalks shoot up into the sky, towering high above the field; at the bottom the small main character and his neighbours look up in shock. " + PEOPLE)),
    ("e06-smile", *man_scene(B, "close-up of the main character looking up at the tall bamboo with a proud quiet smile. Nobody else.")),
]

C = "Setting: a circus camp at night in thin white line art: a striped circus tent, lanterns, wooden wagons. "
EL = "elephant drawn in white line art with four legs, two ears, one trunk and two tusks"
R["elephant-rope"] = [
    ("f01-elephant", *scene(C, f"a huge adult {EL} stands calmly, one back leg tied with a thin rope to a small wooden stake in the ground. No people.")),
    ("f02-ask", *man_scene(C, f"the main character, puzzled, asks a circus trainer, {W} wearing a cap, a question; the huge {EL} stands behind them tied to a small stake. " + SAME)),
    ("f03-baby", *scene(C, f"a small baby {EL} pulls hard with all its strength against a thin rope tied to a small wooden stake, straining. No people.")),
    ("f04-gaveup", *scene(C, f"the small baby {EL} lies down on the ground next to the stake, giving up, sad eyes. No people.")),
    ("f05-rope", *scene(C, "close-up at ground level: a thin rope loosely tied around a giant elephant's leg and a tiny wooden stake in the ground. No people.")),
    ("f06-hands", *man_scene(C, "close-up of the main character looking down at his own open hands, thinking deeply. Nobody else.")),
]

Y = "Setting: a farmyard in thin white line art: a wooden barn, straw, a fence, hills behind. "
R["eagle-chickens"] = [
    ("g01-egg", *scene(Y, f"a farmer, {W} wearing a straw hat, gently places a big egg into a straw nest among chickens in the barn. " + ANAT)),
    ("g02-peck", *scene(Y, "a young eagle drawn in white line art pecks at the ground among a group of chickens. No people.")),
    ("g03-walk", *scene(Y, "wide shot: a young eagle walks in a line with chickens across the farmyard, copying them. No people.")),
    ("g04-sky", *scene(Y + "Sunset sky over mountains. ", "a majestic eagle soars high across the sky above the mountains; below in the farmyard a young eagle among chickens looks up at it. No people.")),
    ("g05-shrug", *scene(Y, "close view: chickens talk to the young eagle, one chicken shrugs with its wings. No people.")),
    ("g06-lower", *scene(Y, "the young eagle lowers its head sadly and keeps pecking at the ground among the chickens. No people.")),
    ("g07-old", *scene(Y, "an old eagle lies peacefully on the straw in the chicken yard, eyes closed, gentle and calm, chickens nearby. No people.")),
    ("g08-circle", *man_scene("Setting: a small living room in thin white line art: a sofa, a coffee table. ", "the main character sits on the sofa among four people who all stare at their phones and complain with bored, frowning faces; he looks away, thinking. " + PEOPLE)),
]

K = "Setting: a dark room at night in thin white line art. "
R["candle"] = [
    ("h01-candle", *man_scene(K, "the main character holds a tall lit candle in front of his chest; several people gather close around its warm light. " + PEOPLE)),
    ("h02-give", *man_scene(K, "the main character, a lit candle on the table beside him, hands coins to one person and puts a comforting hand on another person's shoulder. " + PEOPLE)),
    ("h03-short", *man_scene(K, "the main character holds a very short half-melted candle, looking exhausted, dark circles under his eyes; people still around him. " + PEOPLE)),
    ("h04-leave", *man_scene(K, "the main character holds a tiny candle stub with a weak flame; the people turn their backs and walk away toward a bright light in the distance. " + PEOPLE)),
    ("h05-alone", *man_scene(K, "almost complete darkness, the main character sits alone on the floor, a tiny burnt-out candle stub with a thin wisp of smoke beside him. Nobody else.")),
    ("h06-lantern", *man_scene(K, "the main character carefully lights a new candle and places it inside a glass lantern, his face warm and calm in its light. Nobody else.")),
]

CL = "Setting: a classroom in thin white line art: a blackboard, wooden desks. "
T = f"a teacher, {W} with glasses"
R["glass-of-water"] = [
    ("i01-raise", *man_scene(CL, f"{T} stands at the front raising a glass of water in one hand; the main character sits at a desk in the front row looking up at the glass. " + PEOPLE)),
    ("i02-guess", *scene(CL, "students drawn in white line art at their desks raise their hands and shout guesses, mouths open. Empty dark space above their heads. " + ANAT)),
    ("i03-smile", *scene(CL, f"{T} smiles wisely, holding the glass of water up at shoulder height. " + ANAT)),
    ("i04a-minute", *scene(CL, "close-up of one arm holding a glass of water out straight, relaxed and steady. Only the arm and the glass.")),
    ("i04b-hour", *scene(CL, "close-up of one arm holding a glass of water out straight, the arm trembling a little, small strain lines around the elbow. Only the arm and the glass.")),
    ("i04c-day", *scene(CL, "close-up of one arm holding a glass of water out straight, shaking hard with pain, many jagged pain lines, the water spilling. Only the arm and the glass.")),
    ("i05-night", *man_scene("Setting: a dark bedroom at night in thin white line art: a bed, a window with the moon. ", "the main character lies awake in bed staring at the ceiling, replaying an old argument; a heavy dark storm cloud hangs over his head. Nobody else.")),
    ("i06-down", *man_scene("Setting: a dark bedroom at night in thin white line art: a bed, a nightstand. ", "the main character sits on the edge of the bed, eyes closed, breathing out calmly, slowly placing an empty hand down on the nightstand as if putting down an invisible glass. Nobody else.")),
]

M = "Setting: a busy open-air market in thin white line art: fruit stalls, baskets, awnings, shoppers. "
R["silence-reply"] = [
    ("j01-insult", *man_scene(M, f"the main character stands behind his fruit stall; in front of it {W} points at him angrily, shouting insults; shoppers turn to look. " + PEOPLE)),
    ("j02-calm", *man_scene(M, "the main character calmly arranges apples on his fruit stall, peaceful face, eyes down. Nobody else in focus.")),
    ("j03-louder", *scene(M, f"{W} shouts louder with both fists clenched, red-faced anger lines, a crowd of shoppers watching. " + PEOPLE + ANAT)),
    ("j04-leave", *scene(M, f"{W} storms off through the market, frustrated and embarrassed, looking back over his shoulder. " + ANAT)),
    ("j05-boy", *man_scene(M, "a young boy drawn in white line art looks up at the main character behind his fruit stall and asks him a question. The boy is a child, the main character an adult.")),
    ("j06-fruit", *man_scene(M, "the main character kneels and holds out an apple to the young boy, kind wise smile; the boy, drawn in white line art, looks at the apple. The boy is a child.")),
    ("j07-think", *scene(M, "close-up of a young boy drawn in white line art thinking, one finger on his chin, eyes looking up. " + ANAT)),
]

if __name__ == "__main__":
    n = 0
    for slug, jobs in R.items():
        js = [{"out": f"img/{o}.jpg", "refs": r, "seed": 900 + 13 * n + i, "prompt": p} for i, (o, p, r) in enumerate(jobs)]
        n += 1
        json.dump({"model": "black-forest-labs/flux.2-klein-4b", "size": "1152x2048", "workers": 2, "jobs": js},
                  open(f"{slug}/jobs.json", "w"), indent=1)
        print(slug, len(js))
