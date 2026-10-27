#!/bin/bash
# The exact TTS takes used (one Gemini call per ad).
T=../../reels/tts.py
python3 $T ad1/script.txt ad1/voice-1.wav Zephyr "with high energy, polished and upbeat, like a premium mobile app commercial voice-over, crisp and fast-paced, smiling"
python3 $T ad2/script.txt ad2/voice-1.wav Orus "confident and punchy, like a modern premium commercial voice-over: intriguing and low on the first lines, then bright, upbeat and energetic from 'Noli does the opposite'"
python3 $T ad3/script.txt ad3/voice-1.wav Leda "casually, like a young friendly content creator talking to her phone camera in a TikTok video, natural, a little excited, quick conversational pace"
