"""Font paths that work on this Windows PC and in the Linux cloud VM.

Linux fonts come from apt (see cloud/setup.sh): Liberation (metric clone of Arial), DejaVu (✓ ✗ ◀ symbols),
Noto Color Emoji. Use font(name) for PIL / ffmpeg paths and emoji_image() for colour emoji.
"""
import os

from PIL import Image, ImageDraw, ImageFont

CANDIDATES = {
    "bold":     ["C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"],
    "regular":  ["C:/Windows/Fonts/segoeui.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
    "semibold": ["C:/Windows/Fonts/segoeuib.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
    "symbol":   ["C:/Windows/Fonts/seguisym.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
    "emoji":    ["C:/Windows/Fonts/seguiemj.ttf", "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"],
}


def font(name: str) -> str:
    for path in CANDIDATES[name]:
        if os.path.exists(path):
            return path
    raise FileNotFoundError(f"No '{name}' font found; tried {CANDIDATES[name]}. In the cloud run cloud/setup.sh.")


def ffmpeg_path(path: str) -> str:
    """Escape a font path for an ffmpeg drawtext fontfile= option (the drive colon needs escaping)."""
    return path.replace("\\", "/").replace(":", "\\:")


def emoji_image(ch: str, size: int) -> Image.Image:
    """A colour emoji as an RGBA image `size` px tall. Noto Color Emoji is a bitmap font that only
    loads at 109 px, so it is drawn there and scaled; Segoe UI Emoji scales natively."""
    path = font("emoji")
    native = 109 if "Noto" in path else size
    f = ImageFont.truetype(path, native)
    im = Image.new("RGBA", (int(native * 1.4), int(native * 1.4)), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((0, 0), ch, font=f, embedded_color=True)
    im = im.crop(im.getbbox() or (0, 0, 1, 1))
    return im.resize((max(1, round(im.width * size / im.height)), size), Image.Resampling.LANCZOS)
