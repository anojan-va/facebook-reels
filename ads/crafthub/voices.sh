#!/bin/bash
# The exact TTS takes used (one Gemini call per reel).
T=../../reels/tts.py
python3 $T reel1/script.txt reel1/voice-1.wav Aoede "warmly and upbeat, like a friendly Berlin lifestyle creator recommending fun things to do, smiling, lively but natural pace"
python3 $T reel2/script.txt reel2/voice-1.wav Aoede "warmly and playfully, like a friendly storyteller in a cozy Instagram reel, a little witty, natural conversational pace with small comic pauses"
