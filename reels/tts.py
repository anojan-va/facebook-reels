"""Record a whole script as ONE Gemini TTS take (one call = one consistent voice).

Usage: python tts.py <script.txt> <out.wav> [voice] [style] [--free] [--model gemini-2.5-pro-tts]

Default: PREMIUM voice = Gemini 2.5 Pro TTS on Vertex AI (paid, no daily limit, best quality).
  Key: $GOOGLE_VERTEX_API_KEY, else ~/.vertex-key (local PC); in a Claude cloud session neither exists and the
  network-secret proxy adds x-goog-api-key to requests for aiplatform.googleapis.com. The key is a Vertex AI
  "express mode" key (starts with AQ.); Google's classic Cloud Text-to-Speech (Chirp 3 HD) does not accept it.
--free: the old free tier on AI Studio (gemini-2.5-flash-preview-tts, 3 requests/min, 10/day).
  Key: $GEMINI_API_KEY, else ~/.flow-mcp/gemini-key; in the cloud the proxy adds it for generativelanguage.googleapis.com.
Channel defaults (match reel 1's opening voice): Charon, CHANNEL_STYLE below.
"""
import base64
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

PREMIUM_MODEL = "gemini-2.5-pro-tts"
FREE_MODEL = "gemini-2.5-flash-preview-tts"
CHANNEL_VOICE = "Charon"
CHANNEL_STYLE = ("in a deep, low-pitched, relaxed male voice at a natural conversational pace, calm and confident, "
                 "like a friendly psychology explainer")


def key_from(env: str, path: Path) -> str:
    return os.environ.get(env) or (path.read_text().strip() if path.exists() else "")


def speak(text: str, out: Path, voice=CHANNEL_VOICE, style=CHANNEL_STYLE, free=False, model=None):
    body = {"contents": [{"role": "user", "parts": [{"text": f"Say {style}: {text}"}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    if free:
        key = key_from("GEMINI_API_KEY", Path.home() / ".flow-mcp" / "gemini-key")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model or FREE_MODEL}:generateContent"
    else:
        key = key_from("GOOGLE_VERTEX_API_KEY", Path.home() / ".vertex-key")
        url = f"https://aiplatform.googleapis.com/v1/publishers/google/models/{model or PREMIUM_MODEL}:generateContent"
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"content-type": "application/json", **({"x-goog-api-key": key} if key else {})})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        hint = ""
        if e.code in (401, 403) and not free:
            hint = ("\nNo Vertex key reached Google: add a network secret for aiplatform.googleapis.com "
                    "(header x-goog-api-key) in the cloud environment, or set GOOGLE_VERTEX_API_KEY.")
        sys.exit(f"TTS HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:400]}{hint}")
    part = next(p for p in data["candidates"][0]["content"]["parts"] if "inlineData" in p)["inlineData"]
    rate = part.get("mimeType", "").split("rate=")[-1] if "rate=" in part.get("mimeType", "") else "24000"
    pcm = base64.b64decode(part["data"])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", rate, "-ac", "1", "-i", "-",
                    "-af", "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "2", str(out)],
                   input=pcm, check=True)
    print(out)


if __name__ == "__main__":
    args = sys.argv[1:]
    free = "--free" in args
    model = None
    if "--model" in args:
        i = args.index("--model"); model = args[i + 1]; del args[i:i + 2]
    args = [a for a in args if a != "--free"]
    speak(Path(args[0]).read_text(encoding="utf-8").strip(), Path(args[1]), *args[2:4], free=free, model=model)
