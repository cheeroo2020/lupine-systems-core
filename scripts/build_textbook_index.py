#!/usr/bin/env python3
"""
Lupine — index the course text's printed page labels.

Reads the textbook PDF and writes website/lab/textbook-pages.json, mapping each
printed label (01-08 = Part 01, page 8) to its PDF page number and title. The
lab cites pages by these labels; tests/test_lab.py fails if the lab cites a
label that is not in this index, so every study reference is a real page.

Run:  pip install pypdfium2
      python scripts/build_textbook_index.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "docs" / "textbook" / "energy-infrastructure-visual-handbook-8-part-2026-10-17.pdf"
OUT = ROOT / "website" / "lab" / "textbook-pages.json"

# The footer of every numbered page reads "THE VISUAL ENERGY SERIES / ... 01-08".
LABEL = re.compile(r"(?:THE VISUAL ENERGY SERIES|LUPINE)[^\n]*?\b(0[1-8]-\d\d)\b")


def build() -> dict:
    pdf = pdfium.PdfDocument(str(PDF))
    pages = {}
    for i in range(len(pdf)):
        text = pdf[i].get_textpage().get_text_range().replace("\r", "")
        found = LABEL.search(text)
        if not found:
            continue                      # the three unnumbered front pages
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        pages[found.group(1)] = {"pdf_page": i + 1, "title": lines[1] if len(lines) > 1 else ""}
    return {"source": f"docs/textbook/{PDF.name}", "pages": pages}


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    index = build()
    OUT.write_text(json.dumps(index, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(index['pages'])} labelled pages)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
