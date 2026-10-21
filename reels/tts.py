"""Record a whole script as ONE Gemini TTS take (one call = one consistent voice).

Usage: python tts.py <script.txt> <out.wav> [voice] [style] [--premium] [--model ...]

Default: the CHANNEL voice = Gemini 2.5 Flash TTS on AI Studio, Charon, deep relaxed style (the user's choice; closest
  to reel 1). Key: $GEMINI_API_KEY, else ~/.flow-mcp/gemini-key; in the cloud the proxy adds it for
  generativelanguage.googleapis.com. Free tier: 3 requests/minute, 10/day per key.
  Several keys: $GEMINI_API_KEYS="key1,key2,..." — on a quota error (429) the next key is tried (keys never go to disk).
--premium: Gemini 2.5 Pro TTS on Vertex AI (paid, no daily limit; sounds richer but higher-pitched, ~125-135 Hz;
  the user preferred the channel voice).
  Key: $GOOGLE_VERTEX_API_KEY, else ~/.vertex-key (local PC); in a Claude cloud session neither exists and the
  network-secret proxy adds x-goog-api-key to requests for aiplatform.googleapis.com. The key is a Vertex AI
  "express mode" key (starts with AQ.); Google's classic Cloud Text-to-Speech (Chirp 3 HD) does not accept it.
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
CHANNEL_STYLE = "calm, confident, conversational, slightly slow, in a deep low relaxed voice, like a friendly psychology explainer"
PREMIUM_STYLE = ("in a deep, low-pitched, relaxed male voice at a natural conversational pace, calm and confident, "
                 "like a friendly psychology explainer")   # Pro reads 25 % slower: never say "slow" to it


def key_from(env: str, path: Path) -> str:
    return os.environ.get(env) or (path.read_text().strip() if path.exists() else "")


def speak(text: str, out: Path, voice=CHANNEL_VOICE, style=None, premium=False, model=None):
    free = not premium
    style = style or (PREMIUM_STYLE if premium else CHANNEL_STYLE)
    body = {"contents": [{"role": "user", "parts": [{"text": f"Say {style}: {text}"}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    if free:
        keys = [k for k in os.environ.get("GEMINI_API_KEYS", "").split(",") if k.strip()] or \
               [key_from("GEMINI_API_KEY", Path.home() / ".flow-mcp" / "gemini-key")]
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model or FREE_MODEL}:generateContent"
    else:
        keys = [key_from("GOOGLE_VERTEX_API_KEY", Path.home() / ".vertex-key")]
        url = f"https://aiplatform.googleapis.com/v1/publishers/google/models/{model or PREMIUM_MODEL}:generateContent"
    for n, key in enumerate(keys):
        # In the cloud the proxy overwrites an x-goog-api-key header with the stored secret, so a key we were given
        # goes in the URL instead (?key=), which the proxy leaves alone.
        req = urllib.request.Request(url + (f"?key={key.strip()}" if key else ""), data=json.dumps(body).encode(),
                                     method="POST", headers={"content-type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                data = json.loads(r.read())
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and n + 1 < len(keys):
                print(f"key {n + 1} over quota, trying key {n + 2}", file=sys.stderr)
                continue
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
    premium = "--premium" in args
    model = None
    if "--model" in args:
        i = args.index("--model"); model = args[i + 1]; del args[i:i + 2]
    args = [a for a in args if a != "--premium"]
    speak(Path(args[0]).read_text(encoding="utf-8").strip(), Path(args[1]), *args[2:4], premium=premium, model=model)
