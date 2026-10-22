"""Prompt pieces for reels with the new main character (the bearded man in the yellow hoodie, refs/man.jpg).

Use with refs ["../refs/man.jpg"] whenever he is in the shot. Everyone else is white line art.
"""

HOUSE = ("Minimalist illustration on a pure black background, clean thin white line art with no shading for the world. "
         "The only colour in the image is the main character. All other people, animals and objects are drawn WHITE: "
         "white bodies, white clothes, white fills with thin dark outlines, never black-filled shapes or dark silhouettes. "
         "No text, letters or captions in the image unless described. Vertical 9:16 composition. ")
HOUSE_EMPTY = ("Minimalist illustration on a pure black background, clean thin white line art with no shading, white lines only, "
               "no colour at all. People, animals and objects are drawn WHITE: white bodies, white clothes, white fills, "
               "never black-filled shapes or dark silhouettes. No text, letters or captions in the image. Vertical 9:16 composition. ")
REF = ("Reference image 1 shows exactly how the main character looks: copy his face, hair, beard, yellow hoodie, black cargo "
       "pants and white sneakers. Do NOT copy the reference's beige background or its layout: draw a NEW scene as described. ")
MAN = ("The main character is a young man with short tousled brown hair, a short neat brown beard and warm friendly eyes, "
       "wearing a mustard-yellow hoodie, black cargo jogger pants and white sneakers, drawn in clean anime line art with flat "
       "colours and a soft warm yellow glow around his outline. ")
WHITE_MAN = ("a man drawn all in WHITE, NOT coloured, NOT black-filled: short hair, clean-shaven, a plain WHITE t-shirt and "
             "WHITE trousers, white skin with thin dark outlines")
PEOPLE = ("All other people are figures drawn all in WHITE (white clothes, white fills, thin dark outlines), NOT coloured, "
          "NOT yellow, NOT black-filled, no dark silhouettes. ")
ANAT = "Normal human anatomy: each person has exactly two arms, two hands, two legs and two feet. "
SAME = ("They stand at the same distance from the camera, the same scale, adults of similar height. ")


def man_scene(setting, scene, extra=""):
    """Prompt + refs for a shot with the main character."""
    return REF + HOUSE + MAN + PEOPLE + ANAT + extra + setting + "Scene: " + scene, ["../refs/man.jpg"]


def scene(setting, scene, extra=""):
    """Prompt + refs for a shot without the main character."""
    return HOUSE_EMPTY + extra + setting + "Scene: " + scene, []
