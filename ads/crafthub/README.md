# The Craft Hub (Berlin) - Instagram Reels

Craft workshop studio and community in Berlin-Friedrichshain (thecrafthub.de, @thecrafthub.de). Brand: cream #fffaf6,
deep green #1f3b2c, terracotta #d45541; fonts Annie Use Your Telescope / Architects Daughter / Poppins (all Google Fonts).

| Reel | File | Idea | Music (Mixkit) |
|---|---|---|---|
| 1 "Berlin, you need a new hobby" | `reel1.py` | six real workshops as a scrapbook countdown, comment-a-number CTA | `okay` from 15.28 s |
| 2 "Making friends in Berlin is hard" | `reel2.py` | paper-cut strangers become friends at a craft table + membership checklist | `happy-home` from 11.28 s |
| 3 UGC "POV: I went to a craft night alone" | (Omni clips by the user) | storyboard + prompts in the chat / concepts | - |

Look (`craftkit.py`, on top of `../nolidrop/adkit.py`): paper texture that boils, torn photo cards, washi tape,
handwritten labels, self-drawing doodles (ticks, hearts, stars, stitches), paper-cut people, stop-motion on twos with jitter,
paper-tear and page-turn transitions with paper SFX.

Rebuild: `./voices.sh` (Gemini TTS, voice Aoede) · `python3 ../../reels/polli.py gen1.json` then `gen2.json` (Klein) ·
`python3 cutout.py img/p-person*.jpg img/p-tower.jpg` · `python3 reel1.py [--stills|--frame t]` → `output/`.

Notes: product photos stay on their white cards (scrapbook style) - cutting out white/cream objects and glass failed;
paper-cut person 1 wears mustard because a white cardigan merged with the background in the cut-out.
