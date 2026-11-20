#!/usr/bin/env python3
"""Bangun aset pustaka logo untuk html/ (dipakai web preview dan APK).

Sumber:
  drive_out/*.png           342 hasil potong (master, tidak diubah)
  html/assets/variasi-0*.png  lima konsep lama (3 warna solid)

Keluaran:
  html/assets/logos/*.webp   tampilan penuh, WebP q85
  html/assets/thumbs/*.webp  thumbnail 160 px, WebP q80
  html/assets/manifest.js    window.LOGO_LIBRARY = [...]

Jalankan dari root repository:
  python3 scripts/build_logo_assets.py
Butuh Pillow dengan dukungan WebP.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "drive_out"
LEGACY = ROOT / "html" / "assets"
OUT_LOGO = ROOT / "html" / "assets" / "logos"
OUT_THUMB = ROOT / "html" / "assets" / "thumbs"
MANIFEST = ROOT / "html" / "assets" / "manifest.js"
ROOT_PREVIEW = ROOT / "preview-logo-mcm.html"
INDEX = ROOT / "html" / "index.html"

LEGACY_TITLES = [
    "Evolusi logo lama",
    "Diamond negatif",
    "Lipatan metal",
    "Komposisi horizontal",
    "Bingkai industrial",
]

CUT_PATTERNS = [
    (re.compile(r"kotak_berisi__(\d+)_logo-(\d+)"), "kotak"),
    (re.compile(r"kotak_rasio_1_(\d+)_logo-(\d+)"), "rasio"),
    (re.compile(r"kotak_rasio_1_logo-(\d+)"), "rasio"),
]


def cut_identity(name: str) -> tuple[str, int, int] | None:
    for pattern, group in CUT_PATTERNS:
        match = pattern.search(name)
        if match:
            if len(match.groups()) == 2:
                return group, int(match.group(1)), int(match.group(2))
            return group, 0, int(match.group(1))
    return None


def sheet_label(group: str, sheet: int) -> str:
    if group == "kotak":
        return f"Kotak {sheet}"
    return "Rasio utama" if sheet == 0 else f"Rasio {sheet}"


def main() -> int:
    if not SOURCE.is_dir():
        print(f"folder sumber tidak ada: {SOURCE}", file=sys.stderr)
        return 1

    OUT_LOGO.mkdir(parents=True, exist_ok=True)
    OUT_THUMB.mkdir(parents=True, exist_ok=True)

    items: list[dict] = []

    legacy_files = sorted(LEGACY.glob("variasi-0*.png"))
    if len(legacy_files) != len(LEGACY_TITLES):
        print(f"konsep lama tidak lengkap: {len(legacy_files)}", file=sys.stderr)
        return 1
    for number, path in enumerate(legacy_files, start=1):
        items.append(
            {
                "id": f"legacy-{number:02d}",
                "label": f"{number:02d} · {LEGACY_TITLES[number - 1]}",
                "set": "legacy",
                "sheet": "Konsep lama",
                "index": number,
                "source": path,
            }
        )

    cuts: list[tuple[str, int, int, Path]] = []
    for path in sorted(SOURCE.glob("*.png")):
        identity = cut_identity(path.name)
        if identity is None:
            print(f"nama tidak dikenali, dilewati: {path.name}", file=sys.stderr)
            continue
        group, sheet, index = identity
        cuts.append((group, sheet, index, path))

    order = {"kotak": 0, "rasio": 1}
    cuts.sort(key=lambda c: (order[c[0]], c[1], c[2]))
    for group, sheet, index, path in cuts:
        if group == "kotak":
            item_id = f"kotak-{sheet:02d}-{index:02d}"
        elif sheet == 0:
            item_id = f"rasio-utama-{index:02d}"
        else:
            item_id = f"rasio-{sheet:02d}-{index:02d}"
        label = f"{sheet_label(group, sheet)} · {index:02d}"
        items.append(
            {
                "id": item_id,
                "label": label,
                "set": group,
                "sheet": sheet_label(group, sheet),
                "index": index,
                "source": path,
            }
        )

    total_logo = 0
    total_thumb = 0
    for item in items:
        source: Path = item.pop("source")
        with Image.open(source) as opened:
            image = opened.convert("RGB")
        width, height = image.size
        item["w"], item["h"] = width, height
        item["src"] = f"assets/logos/{item['id']}.webp"
        item["thumb"] = f"assets/thumbs/{item['id']}.webp"

        full_path = OUT_LOGO / f"{item['id']}.webp"
        image.save(full_path, "WEBP", quality=85, method=4)
        total_logo += full_path.stat().st_size

        thumb = image.copy()
        thumb.thumbnail((160, 160), Image.LANCZOS)
        thumb_path = OUT_THUMB / f"{item['id']}.webp"
        thumb.save(thumb_path, "WEBP", quality=80, method=4)
        total_thumb += thumb_path.stat().st_size

    payload = json.dumps(items, ensure_ascii=False, separators=(",", ":"))
    MANIFEST.write_text(
        "// Dibangkitkan oleh scripts/build_logo_assets.py — jangan disunting manual.\n"
        f"window.LOGO_LIBRARY={payload};\n",
        encoding="utf-8",
    )

    if INDEX.is_file():
        html = INDEX.read_text(encoding="utf-8")
        marker = "const ASSET_BASE='';"
        if marker not in html:
            print(f"penanda {marker!r} tidak ditemukan di index.html", file=sys.stderr)
            return 1
        ROOT_PREVIEW.write_text(
            html.replace(marker, "const ASSET_BASE='html/';", 1), encoding="utf-8"
        )

    legacy = sum(1 for item in items if item["set"] == "legacy")
    print(f"item         : {len(items)} (konsep lama {legacy}, potongan {len(items) - legacy})")
    print(f"logo webp    : {total_logo / 1048576:.2f} MB")
    print(f"thumb webp   : {total_thumb / 1048576:.2f} MB")
    print(f"manifest     : {MANIFEST.stat().st_size / 1024:.0f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
