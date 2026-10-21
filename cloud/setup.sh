#!/bin/bash
# Cloud environment setup for the Facebook reels pipeline (Ubuntu 24.04, runs as root).
# Paste this into the cloud environment's "Setup script" field. It is cached, so it runs once per environment.
set -e
apt-get update -qq
apt-get install -y -qq ffmpeg fonts-liberation fonts-dejavu-core fonts-noto-color-emoji >/dev/null
PKGS='numpy<2.3 faster-whisper av<16 librosa soundfile pillow'
pip install -q $PKGS 2>/dev/null || pip install -q --break-system-packages $PKGS
# Pre-download the Whisper model used for caption timing (needs huggingface.co in the network allowlist).
python3 -c "from faster_whisper import WhisperModel; WhisperModel('small.en', device='cpu', compute_type='int8')"
echo "reels setup done"
