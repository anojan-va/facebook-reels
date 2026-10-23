"""Image jobs for parable reels 21-25 (deaf-frog … starfish). Two candidates per shot. Writes <slug>/jobs.json."""
import json
from style_new import ANAT as _A
from style_new import ANAT, HOUSE, HOUSE_EMPTY, MAN, OLD_MAN, PEOPLE, REF, TWO_ARMS, WHITE_MAN, man_scene, scene

W = WHITE_MAN
STAND = "He stands still with both feet flat on the ground side by side. "
ONLY2 = "ONLY these two people in the whole image, nobody else anywhere, no figure behind anyone. "
ALONE = "He is completely ALONE: no other people, no figures anywhere. "


COLOR = ("Minimalist illustration on a pure black background, clean thin white line art with no shading. Everything is white "
         "line art except the colours described. No text, letters or captions. Vertical 9:16 composition. ")


def colored(setting, sc):
    return COLOR + setting + "Scene: " + sc, []


def hero(ref, look, setting, sc, alone=False):
    """A shot with one of the hero variants: ref = refs/<file>, look = his description."""
    r = (f"Reference image 1 shows exactly how the main character looks: copy his face, hair and clothes exactly, "
         f"NOT the reference's beige background or layout; draw a NEW scene as described. ")
    return (r + HOUSE + look + ("" if alone else PEOPLE) + ANAT + TWO_ARMS + (ALONE if alone else "") + setting
            + "Scene: " + sc), [f"../refs/{ref}"]


MONK = ("The main character is a young Buddhist monk with short tousled brown hair and a short neat brown beard, wearing a long "
        "mustard-yellow monk robe wrapped over one shoulder and sandals, drawn in clean anime line art with flat colours and a "
        "soft warm yellow glow. ")
OLDMONK = ("The main character is an OLD Buddhist monk about 70 with short grey-white hair, a short grey-white beard and wrinkles, "
           "wearing a long mustard-yellow monk robe and sandals, drawn in clean anime line art with flat colours and a soft warm "
           "yellow glow. He is clearly OLD. ")
KING = MAN + "He wears a golden crown and a long royal white cape over his yellow hoodie. "
BOY = ("The main character is a small BOY about 8 years old, a child, with short tousled brown hair and no beard, wearing a "
       "mustard-yellow hoodie, black jogger pants and white sneakers, drawn in clean anime line art with flat colours and a soft "
       "warm yellow glow. ")

R = {}
T = "Setting: a forest at sunrise in thin white line art, a very tall thin stone tower with many ledges rising high into the sky. "
YF = "a small frog glowing mustard-YELLOW with a soft yellow glow"
WF = "frogs drawn all in solid WHITE"
R["deaf-frog"] = [
    ("a01-start", *colored(T, f"at the foot of the tall tower a crowd of many {WF} gathers around {YF}, ready for a race. Only the yellow frog has colour. No people.")),
    ("a02-shout", *scene(T, f"close view: a crowd of {WF} at the bottom shout up with wide-open mouths and waving arms, angry and mocking. No people.")),
    ("a03-giveup", *scene(T, f"on the side of the tower several {WF} slide down and fall off, giving up, tired and sad. No people.")),
    ("a04-climb", *colored(T, f"high up the tower, {YF} keeps climbing steadily upward, determined; far below tiny white frogs. Only the yellow frog has colour. No people.")),
    ("a05-top", *colored(T + "Golden sunrise. ", f"{YF} stands proudly on the very top of the tall tower, the rising sun behind it. Only the yellow frog has colour. No people.")),
    ("a06-ask", *colored(T, f"at the foot of the tower many {WF} crowd around {YF}, asking it something with curious faces; the yellow frog smiles calmly. Only the yellow frog has colour. No people.")),
    ("a07-ear", *colored("Setting: plain black background. ", f"big close-up of the head of {YF}, calm and smiling, with a small white hearing aid clearly visible in its ear. Only the frog has colour. No people.")),
    ("k1-top", *colored(T + "Sunrise. ", f"{YF} sits peacefully on the top of the tower with its eyes closed, smiling, the whole sunrise sky behind it. Only the frog has colour. No people.")),
    ("k2-walk", *hero("man.jpg", MAN, "Setting: a city street in thin white line art. ", "the main character walks calmly forward wearing big headphones, a confident smile, while people drawn all in WHITE on both sides point and shout at him; he ignores them. Both his hands in his hoodie pocket.")),
]
RIV = "Setting: a rushing river at dusk in thin white line art, rocks, a forest on both banks. "
YM = f"a young monk drawn all in WHITE with a shaved head and white robes"
WOMAN = "a young woman drawn all in WHITE with a white long dress and long hair"
R["carrying-woman"] = [
    ("b01-river", *hero("monk-old.jpg", OLDMONK, RIV, f"the old monk and {YM} arrive at the river bank; {WOMAN} stands stuck at the edge of the rushing water, worried. Exactly three people, standing clearly apart. " + STAND.replace("He stands", "Everyone stands"))),
    ("b02-carry", *hero("monk-old.jpg", OLDMONK, RIV, f"the old monk wades through the river carrying {WOMAN} in both arms, one arm under her back and one under her knees; she holds onto his shoulder. Only these two in the river.")),
    ("b03-walk", *hero("monk-old.jpg", OLDMONK, "Setting: a forest path in thin white line art. ", f"the old monk walks calmly on the path in front; behind him {YM} walks with a troubled, frowning face, both his hands clenched. " + ONLY2)),
    ("b04-burst", *hero("monk-old.jpg", OLDMONK, "Setting: a forest at night in thin white line art, a moon. ", f"{YM} stops and bursts out angrily, one arm pointing back toward the river, the other hand in a fist; the old monk stands calm facing him, both hands together. " + ONLY2)),
    ("b05-smile", *hero("monk-old.jpg", OLDMONK, "Setting: a forest at night in thin white line art, a moon. ", "the old monk smiles gently, both hands resting together in front of him.", alone=True)),
    ("b06-close", *hero("monk-old.jpg", OLDMONK, "Setting: a forest at night in thin white line art. ", "close-up from the chest up of the old monk, a kind wise knowing smile, looking at the viewer.", alone=True)),
    ("b07-rock", *hero("man.jpg", MAN, "Setting: a dark bedroom at night in thin white line art. ", "the main character lies awake in bed under a blanket, eyes open, worried; a huge heavy grey rock floats above him with faint shapes of two people arguing on it.", alone=True)),
    ("k1-drop", *hero("man.jpg", MAN, "Setting: a riverbank at sunrise in thin white line art. ", "the main character lets a big heavy rock drop from both hands into the river with a splash, relieved, a light smile. " + STAND, alone=True)),
    ("k2-light", *hero("man.jpg", MAN, "Setting: a path along a river at sunrise in thin white line art. ", "the main character walks away lightly along the path, arms relaxed and swinging, a free relieved smile.", alone=True)),
]
PAL = "Setting: a royal palace throne room in thin white line art: tall pillars, a throne, banners. "
ADV = "wise advisors drawn all in WHITE with white robes and long beards"
SERV = "an old servant drawn all in WHITE with a white robe, bald, a long white beard"
R["kings-ring"] = [
    ("c01-throne", *hero("man.jpg", KING, PAL, "the king sits on his throne looking troubled, chin resting on one hand, the other hand on the armrest.", alone=True)),
    ("c02-ask", *hero("man.jpg", KING, PAL, f"the king stands in front of his throne speaking to four {ADV} who stand in a row before him, each clearly apart; he holds one open hand out to them, the other at his side.")),
    ("c03-argue", *scene(PAL, f"four {ADV} argue with each other, confused, scratching heads and shrugging, standing clearly apart. " + ANAT)),
    ("c04-servant", *hero("man.jpg", KING, PAL, f"{SERV} bows and holds out a small simple ring on his open palm to the king, who reaches for it with one hand. " + ONLY2)),
    ("c05-ring", *colored("Setting: plain black background. ", "big close-up of a simple plain gold ring lying on an open palm drawn in white line art, a soft golden glow, no text, no engraving visible. No face. Only the ring is gold.")),
    ("c06-war", *hero("man.jpg", KING, "Setting: a battlefield in thin white line art, smoke, broken spears. ", "the king stands in the smoke, tired and sad, looking down at a ring held in his right hand, his left hand on his chest, taking a calm breath.", alone=True)),
    ("c07-feast", *hero("man.jpg", KING, "Setting: a grand celebration hall in thin white line art, lanterns, a long feast table, people drawn in white cheering in the background. ", "the king stands in the celebration looking down at the ring on his finger with a humble calm face, both hands in front of his chest.")),
    ("c08-rain", *hero("man.jpg", MAN, "Setting: a park bench in heavy rain in thin white line art. ", "the main character sits alone on the bench in the rain, sad, both elbows on his knees, head lowered.", alone=True)),
    ("k1-sun", *hero("man.jpg", MAN, "Setting: a park path in bright sunshine in thin white line art. ", "the main character walks happily in the sunshine, calm smile, both arms relaxed, looking at a simple ring on his finger.", alone=True)),
]
RB = "Setting: a quiet riverbank in thin white line art, reeds, flowing water. "
SCO = "a black-outlined WHITE scorpion with a curled tail"
R["scorpion-monk"] = [
    ("d01-see", *hero("monk.jpg", MONK, RB, f"the monk stands on the riverbank and sees {SCO} struggling and drowning in the water near the edge, worried face. " + STAND, alone=True)),
    ("d02-scoop", *hero("monk.jpg", MONK, RB, f"the monk kneels on both knees at the river edge and scoops {SCO} out of the water in his RIGHT palm; the scorpion's tail stings his hand; his LEFT hand rests on his knee.", alone=True)),
    ("d03-pain", *hero("monk.jpg", MONK, RB, f"the monk winces in pain shaking his stung right hand; {SCO} falls from his hand back into the water with a splash; his left hand rests on his knee.", alone=True)),
    ("d04-again", *hero("monk.jpg", MONK, RB, f"the monk kneels at the river and picks up {SCO} again in his right hand and is stung again; standing a few steps behind on the bank, {W} watches shocked with both hands raised. " + ONLY2)),
    ("d05-ask", *hero("monk.jpg", MONK, RB, f"{W} stands on the right asking the monk a question with one open hand; the monk on the left listens calmly, both hands together. " + ONLY2)),
    ("d06-land", *hero("monk.jpg", MONK, RB, f"the monk kneels and gently places {SCO} on dry land with his right hand, smiling kindly; his left hand on his knee.", alone=True)),
    ("d07-close", *hero("monk.jpg", MONK, RB, "close-up from the chest up of the monk, a calm kind wise smile, both hands together in front of his chest.", alone=True)),
    ("k1-leaf", *hero("monk.jpg", MONK, RB + "Sunrise. ", f"the monk kneels at the river edge and lifts {SCO} out of the water safely on a big green leaf held in both hands, smiling; the leaf is the only green in the image.", alone=True)),
]
BEACH = "Setting: a long beach at sunrise in thin white line art, gentle waves, the rising sun. "
STAR = "starfish drawn all in solid WHITE"
R["starfish"] = [
    ("e01-beach", *scene(BEACH, f"wide view: the whole beach is covered with thousands of {STAR} washed up after a storm. No people.")),
    ("e02-throw", *hero("boy.jpg", BOY, BEACH, f"the small boy throws one of the {STAR} into the sea with his right arm; his left arm at his side; many starfish lie on the sand around his feet.", alone=True)),
    ("e03-laugh", *hero("boy.jpg", BOY, BEACH, f"{W} walks up laughing, pointing at the thousands of starfish on the sand with one hand; the small boy looks up at him. The boy is a small child, the man an adult. " + ONLY2)),
    ("e04-pick", *hero("boy.jpg", BOY, BEACH, "close-up: the small boy crouches and holds one white starfish in both hands, looking at it gently.", alone=True)),
    ("e05-into", *hero("boy.jpg", BOY, BEACH, "the small boy stands at the edge of the waves, his right arm stretched out after throwing; a white starfish lands softly in the sea; his left arm at his side.", alone=True)),
    ("e06-help", *hero("boy.jpg", BOY, BEACH, f"{W} bends down and picks up a starfish from the sand with both hands; the small boy beside him smiles up at him. The boy is a small child. " + ONLY2)),
    ("e07-village", *scene(BEACH, f"wide shot: many people drawn all in WHITE spread out along the beach, each picking up and throwing {STAR} back into the sea, standing clearly apart. " + PEOPLE + ANAT)),
    ("k1-world", *hero("boy.jpg", BOY, BEACH + "Golden sunrise. ", "the small boy stands at the water's edge holding one white starfish up to the sunrise in both hands, smiling happily.", alone=True)),
]

if __name__ == "__main__":
    n = 0
    for slug, jobs in R.items():
        js = []
        for i, (o, p, r) in enumerate(jobs):
            for k in "ab":
                js.append({"out": f"img/cand/{o}-{k}.jpg", "refs": r, "seed": 4100 + 31 * n + 2 * i + (k == "b"), "prompt": p})
        n += 1
        json.dump({"model": "black-forest-labs/flux.2-klein-4b", "size": "1152x2048", "workers": 2, "jobs": js},
                  open(f"{slug}/jobs.json", "w"), indent=1)
        print(slug, len(js))
