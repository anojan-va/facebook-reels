"""Record one take with Gemini TTS only (no Pollinations fallback: its Algenib sounds like another narrator).
Mars video style: playful, witty storyteller talking straight to the viewer, with comic timing.
Usage: python3 tts_gemini.py take.txt take.wav"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "reels"))
import tts  # noqa: E402

STYLE = ("as a witty, warm, playful YouTube storyteller talking directly to one friend, with great comic timing: "
         "deadpan on the jokes, a little smile in the voice, energetic and brisk, short pauses before punchlines")
tts.speak_polli = lambda *a, **k: sys.exit("gemini failed (no fallback)")
tts.speak(Path(sys.argv[1]).read_text().strip(), Path(sys.argv[2]), "Algenib", STYLE)
