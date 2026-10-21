"""Record a whole script as ONE Gemini TTS take (one call = one consistent voice).

Usage: python tts.py <script.txt> <out.wav> [voice] [style]
Key: $GEMINI_API_KEY, else ~/.flow-mcp/gemini-key; in a Claude cloud session neither exists and the network-secret
proxy adds x-goog-api-key to requests for generativelanguage.googleapis.com. Free tier: 3 requests/minute, 10/day.
Channel defaults (match reel 1's opening voice): Charon, CHANNEL_STYLE below, then speed 1.15 in reel.json.
"""
import base64
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

MODEL = "gemini-2.5-flash-preview-tts"
CHANNEL_VOICE = "Charon"
CHANNEL_STYLE = "calm, confident, conversational, slightly slow, like a friendly psychology explainer"


def speak(text: str, out: Path, voice=CHANNEL_VOICE, style=CHANNEL_STYLE):
    kf = Path.home() / ".flow-mcp" / "gemini-key"
    key = os.environ.get("GEMINI_API_KEY") or (kf.read_text().strip() if kf.exists() else "")
    body = {"contents": [{"parts": [{"text": f"Say {style}: {text}"}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
                                 data=json.dumps(body).encode(), method="POST",
                                 headers={"content-type": "application/json", **({"x-goog-api-key": key} if key else {})})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"Gemini TTS HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:400]}")
    part = next(p for p in data["candidates"][0]["content"]["parts"] if "inlineData" in p)["inlineData"]
    rate = part.get("mimeType", "").split("rate=")[-1] if "rate=" in part.get("mimeType", "") else "24000"
    pcm = base64.b64decode(part["data"])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", rate, "-ac", "1", "-i", "-",
                    "-af", "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "2", str(out)],
                   input=pcm, check=True)
    print(out)


if __name__ == "__main__":
    args = sys.argv[1:]
    speak(Path(args[0]).read_text(encoding="utf-8").strip(), Path(args[1]), *args[2:4])
