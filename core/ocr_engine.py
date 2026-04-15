"""
OCR Engine – Tesseract-based text extraction with Gemma vision fallback.
"""

from __future__ import annotations

from typing import Optional

from PIL import Image

from config.settings import TESSERACT_CONFIG


# ---------------------------------------------------------------------------
# Check Tesseract availability at import time
# ---------------------------------------------------------------------------
_tesseract_available = False
try:
    import pytesseract
    import shutil

    # On macOS with Homebrew, tesseract may not be on the default PATH.
    # Auto-detect common install locations.
    if not shutil.which("tesseract"):
        for candidate in ["/opt/homebrew/bin/tesseract", "/usr/local/bin/tesseract"]:
            import os
            if os.path.isfile(candidate):
                pytesseract.pytesseract.tesseract_cmd = candidate
                break

    pytesseract.get_tesseract_version()
    _tesseract_available = True
except Exception:
    pass


def is_tesseract_available() -> bool:
    return _tesseract_available


# ---------------------------------------------------------------------------
# Extract text from image
# ---------------------------------------------------------------------------
def extract_text(image: Image.Image, config: str = TESSERACT_CONFIG) -> str:
    """
    Extract text from a PIL Image using Tesseract OCR.
    Returns empty string if Tesseract is not installed.
    """
    if not _tesseract_available:
        return ""
    import pytesseract
    return pytesseract.image_to_string(image, config=config)


def extract_with_details(image: Image.Image, config: str = TESSERACT_CONFIG) -> dict:
    """
    Extract text with confidence data from Tesseract.
    Returns dict with 'text', 'confidence', and 'word_count'.
    """
    if not _tesseract_available:
        return {"text": "", "confidence": 0.0, "word_count": 0}

    import pytesseract

    text = pytesseract.image_to_string(image, config=config)
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, config=config)

    # Compute average confidence (skip -1 values which are block/line separators)
    confs = [int(c) for c in data["conf"] if int(c) > -1]
    avg_conf = sum(confs) / len(confs) if confs else 0.0
    word_count = len([w for w in data["text"] if w.strip()])

    return {
        "text": text,
        "confidence": round(avg_conf, 1),
        "word_count": word_count,
    }


# ---------------------------------------------------------------------------
# Pre-process image for better OCR
# ---------------------------------------------------------------------------
def preprocess_for_ocr(image: Image.Image) -> Image.Image:
    """
    Apply basic preprocessing to improve OCR accuracy:
    - Convert to grayscale
    - Upscale if small
    - Sharpen
    """
    from PIL import ImageEnhance, ImageFilter

    # Convert to grayscale
    img = image.convert("L")

    # Upscale small images (OCR works better on ~300 DPI)
    w, h = img.size
    if w < 1000:
        scale = 1500 / w
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

    # Sharpen
    img = img.filter(ImageFilter.SHARPEN)

    # Increase contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)

    return img
