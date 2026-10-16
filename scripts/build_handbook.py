#!/usr/bin/env python3
"""
Lupine — build a PDF edition of the Energy Engineering Handbook.

The editable master is docs/handbook/handbook.md. This script turns it into
a paginated PDF with a table of contents, page numbers and PDF bookmarks.

    python scripts/build_handbook.py               # new edition, from front matter
    python scripts/build_handbook.py --out x.pdf   # draft to any path, for checking

Editions are written to docs/handbook/editions/ and never overwritten: raise
`version` in the master's front matter to make a new one. Earlier editions
are preserved by design.

Supported syntax is listed in the handbook's Appendix E.
Requires: pip install -r docs/handbook/requirements.txt
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, ListFlowable, ListItem, NextPageTemplate, PageBreak,
    Image, PageTemplate, Paragraph, Preformatted, Spacer, Table, TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "docs" / "handbook" / "handbook.md"
EDITIONS = ROOT / "docs" / "handbook" / "editions"
LOGO = ROOT / "website" / "assets" / "brand" / "lupine-logo.png"   # derived from the approved original

# ── look ──────────────────────────────────────────────────────────────
NAVY, SLATE, MUTED = colors.HexColor("#0F172A"), colors.HexColor("#475569"), colors.HexColor("#64748B")
FOREST = colors.HexColor("#1B422E")   # sampled from the logo
RULE, PANEL, HEAD = colors.HexColor("#E2E8F0"), colors.HexColor("#F8FAFC"), colors.HexColor("#F1F5F9")
BADGES = {  # label: (text colour, background)
    "ASSUMED":   ("#92400E", "#FEF3C7"),
    "SIMULATED": ("#5B21B6", "#EDE9FE"),
    "MEASURED":  ("#115E59", "#CCFBF1"),
    "VERIFIED":  ("#166534", "#DCFCE7"),
}
BOXES = {  # container kind: (title, background, bar colour)
    "yours":   ("IN MY OWN WORDS — CHRIS", "#F1F5F9", "#0F172A"),
    "note":    ("NOTE", "#F8FAFC", "#94A3B8"),
    "pending": ("PENDING", "#FFFBEB", "#D97706"),
}
PAGE_W, PAGE_H = A4
MARGIN = 20 * mm
TEXT_W = PAGE_W - 2 * MARGIN


def register_fonts() -> tuple[str, str]:
    """Liberation Sans for prose, DejaVu Sans Mono for equations. Falls back to built-ins."""
    lib = [Path("/usr/share/fonts/truetype/liberation"), ROOT / "docs" / "handbook" / "fonts"]
    dj = [Path("/usr/share/fonts/truetype/dejavu"), ROOT / "docs" / "handbook" / "fonts"]
    find = lambda dirs, name: next((d / name for d in dirs if (d / name).exists()), None)
    body = {s: find(lib, f"LiberationSans-{s}.ttf") for s in ("Regular", "Bold", "Italic", "BoldItalic")}
    mono = find(dj, "DejaVuSansMono.ttf")
    if not all(body.values()) or not mono:
        print("WARNING: Liberation Sans / DejaVu Sans Mono not found; using built-in fonts. "
              "Symbols such as × ≈ → may not render.")
        return "Helvetica", "Courier"
    for style, path in body.items():
        pdfmetrics.registerFont(TTFont(f"Body-{style}", str(path)))
    addMapping("Body-Regular", 0, 0, "Body-Regular")
    addMapping("Body-Regular", 1, 0, "Body-Bold")
    addMapping("Body-Regular", 0, 1, "Body-Italic")
    addMapping("Body-Regular", 1, 1, "Body-BoldItalic")
    pdfmetrics.registerFont(TTFont("Mono", str(mono)))
    return "Body-Regular", "Mono"


BODY, MONO = register_fonts()
BOLD = "Body-Bold" if BODY == "Body-Regular" else "Helvetica-Bold"


def style(name, **kw) -> ParagraphStyle:
    base = dict(fontName=BODY, fontSize=10, leading=14.5, textColor=NAVY, spaceAfter=6)
    base.update(kw)
    return ParagraphStyle(name, **base)


S = {
    "body":   style("body"),
    "small":  style("small", fontSize=8.5, leading=11.5, spaceAfter=0),
    "smallb": style("smallb", fontName=BOLD, fontSize=8.5, leading=11.5, spaceAfter=0),
    "h1":     style("h1", fontName=BOLD, fontSize=21, leading=26, spaceAfter=14, keepWithNext=1),
    "h2":     style("h2", fontName=BOLD, fontSize=13.5, leading=18, spaceBefore=14, spaceAfter=6, keepWithNext=1),
    "h3":     style("h3", fontName=BOLD, fontSize=11, leading=15, spaceBefore=10, spaceAfter=4,
                    textColor=SLATE, keepWithNext=1),
    "boxtitle": style("boxtitle", fontName=BOLD, fontSize=7.5, leading=10, textColor=MUTED, spaceAfter=3),
    "code":   style("code", fontName=MONO, fontSize=9, leading=13, spaceAfter=0),
    "cover1": style("cover1", fontName=BOLD, fontSize=30, leading=36, spaceAfter=10),
    "cover2": style("cover2", fontSize=14, leading=19, textColor=SLATE, spaceAfter=28),
    "cover3": style("cover3", fontSize=10.5, leading=16, textColor=SLATE, spaceAfter=2),
}

# ── inline markup ─────────────────────────────────────────────────────

def _esc(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(text: str, size: float = 10) -> str:
    codes: list[str] = []

    def keep_code(m):
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    t = re.sub(r"`([^`]+)`", keep_code, text)
    t = _esc(t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" color="#334155"><u>\1</u></a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", t)
    for label, (fg, bg) in BADGES.items():
        t = t.replace(f"[{label}]", f'<font name="{BOLD}" size="{size - 2.5:.1f}" color="{fg}" '
                                    f'backColor="{bg}">&nbsp;{label}&nbsp;</font>')
    t = re.sub(r"\x00(\d+)\x00",
               lambda m: f'<font name="{MONO}" size="{size - 1:.1f}">{_esc(codes[int(m.group(1))])}</font>', t)
    return t


def plain(text: str) -> str:
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return re.sub(r"[*`]", "", t).strip()

# ── block parsing ─────────────────────────────────────────────────────

class Heading(Paragraph):
    """A heading that registers itself in the table of contents and PDF outline."""
    counter = 0

    def __init__(self, text: str, level: int):
        super().__init__(inline(text, S[f"h{level + 1}"].fontSize), S[f"h{level + 1}"])
        Heading.counter += 1
        self._toc_level, self._plain, self._key = level, plain(text), f"h{Heading.counter}"


def box(kind: str, inner: list, width: float) -> Table:
    title, bg, bar = BOXES.get(kind, BOXES["note"])
    cell = [Paragraph(title, S["boxtitle"])] + inner
    t = Table([[cell]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(bg)),
        ("LINEBEFORE", (0, 0), (0, -1), 2.5, colors.HexColor(bar)),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    t.spaceBefore, t.spaceAfter = 4, 10
    return t


def table(rows: list[list[str]], width: float) -> Table:
    ncol = max(len(r) for r in rows)
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    # every column fits its longest word; the rest of the width goes by content length
    longest = [max((len(w) for r in rows for w in plain(r[c]).split()), default=1) for c in range(ncol)]
    mins = [min(n * 4.9 + 12, width * 0.28) for n in longest]
    if sum(mins) > width:
        mins = [m * width / sum(mins) for m in mins]
    weights = [max(5, min(max(len(plain(r[c])) for r in rows), 48)) ** 0.8 for c in range(ncol)]
    widths = [m + (width - sum(mins)) * w / sum(weights) for m, w in zip(mins, weights)]
    data = [[Paragraph(inline(c, 8.5), S["smallb" if i == 0 else "small"]) for c in r]
            for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HEAD),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    t.spaceBefore, t.spaceAfter = 4, 10
    return t


def code_block(text: str, width: float) -> Table:
    t = Table([[Preformatted(text, S["code"])]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PANEL), ("BOX", (0, 0), (-1, -1), 0.5, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    t.spaceBefore, t.spaceAfter = 4, 10
    return t


def make_list(items: list[str], ordered: bool) -> ListFlowable:
    flow = [ListItem(Paragraph(inline(i), S["body"]), leftIndent=14) for i in items]
    kw = dict(bulletType="1", bulletFormat="%s.") if ordered else dict(bulletType="bullet", start="•")
    return ListFlowable(flow, leftIndent=14, bulletFontName=BODY, bulletFontSize=9.5,
                        bulletColor=SLATE, spaceAfter=6, **kw)


def parse(lines: list[str], width: float, top: bool = True) -> list:
    out: list = []
    i = 0

    def page_break():
        if out and not isinstance(out[-1], PageBreak):
            out.append(PageBreak())

    while i < len(lines):
        line = lines[i].rstrip()
        s = line.strip()
        if not s:
            i += 1
        elif s == r"\pagebreak":
            page_break(); i += 1
        elif s.startswith(":::"):
            kind, inner, i = s[3:].strip() or "note", [], i + 1
            while i < len(lines) and lines[i].strip() != ":::":
                inner.append(lines[i]); i += 1
            out.append(box(kind, parse(inner, width - 22, top=False), width)); i += 1
        elif s.startswith("```"):
            buf, i = [], i + 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i].rstrip()); i += 1
            out.append(code_block("\n".join(buf), width)); i += 1
        elif m := re.match(r"^(#{1,3})\s+(.*)", s):
            level = len(m.group(1)) - 1
            if top and level == 0 and out:
                page_break()
            out.append(Heading(m.group(2), level) if top else Paragraph(inline(m.group(2)), S["h3"]))
            i += 1
        elif s.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                    rows.append(cells)
                i += 1
            out.append(table(rows, width))
        elif re.match(r"^(-|\d+\.)\s+", s):
            ordered = bool(re.match(r"^\d+\.", s))
            items: list[str] = []
            while i < len(lines):
                t = lines[i]
                if re.match(r"^\s*(-|\d+\.)\s+", t):
                    items.append(re.sub(r"^\s*(-|\d+\.)\s+", "", t).strip())
                elif t.strip() and t.startswith((" ", "\t")) and items:
                    items[-1] += " " + t.strip()
                else:
                    break
                i += 1
            out.append(make_list(items, ordered))
        elif s.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip()); i += 1
            out.append(box("note", parse(buf, width - 22, top=False), width))
        else:
            buf = []
            while i < len(lines) and lines[i].strip() and not re.match(
                    r"^(#{1,3}\s|\||```|:::|>|-\s|\d+\.\s|\\pagebreak)", lines[i].strip()):
                buf.append(lines[i].strip()); i += 1
            out.append(Paragraph(inline(" ".join(buf)), S["body"]))
    return out

# ── document ──────────────────────────────────────────────────────────

def read_master(path: Path) -> tuple[dict, list[str]]:
    text = re.sub(r"<!--.*?-->", "", path.read_text(encoding="utf-8"), flags=re.S)
    meta: dict = {}
    m = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        text = text[m.end():]
    for key in ("title", "version", "edition_date"):
        if key not in meta:
            sys.exit(f"Front matter is missing '{key}'.")
    return meta, text.splitlines()


def check_glyphs(text: str) -> None:
    if BODY != "Body-Regular":
        return
    have = set(pdfmetrics.getFont(BODY).face.charToGlyph) | set(pdfmetrics.getFont(MONO).face.charToGlyph)
    missing = sorted({c for c in text if ord(c) > 126 and ord(c) not in have})
    if missing:
        print("WARNING: characters with no glyph in the handbook fonts:", " ".join(missing))


class HandbookDoc(BaseDocTemplate):
    def __init__(self, filename: str, meta: dict):
        super().__init__(filename, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                         topMargin=MARGIN, bottomMargin=MARGIN + 4 * mm,
                         title=meta["title"], author=meta.get("owner", ""),
                         subject=f"Edition {meta['version']} · {meta['edition_date']}")
        self.meta = meta
        self._outline_level = -1
        frame = Frame(MARGIN, MARGIN + 4 * mm, TEXT_W, PAGE_H - 2 * MARGIN - 4 * mm, id="f",
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate("cover", [frame], onPage=self._cover_page),
            PageTemplate("body", [frame], onPage=self._body_page),
        ])

    def _cover_page(self, canv, doc):
        canv.saveState()
        canv.setFillColor(FOREST)
        canv.rect(0, PAGE_H - 9 * mm, PAGE_W, 9 * mm, stroke=0, fill=1)
        canv.restoreState()

    def _body_page(self, canv, doc):
        canv.saveState()
        canv.setStrokeColor(RULE); canv.setLineWidth(0.5)
        canv.line(MARGIN, MARGIN, PAGE_W - MARGIN, MARGIN)
        canv.setFont(BODY, 8); canv.setFillColor(MUTED)
        canv.drawString(MARGIN, MARGIN - 5 * mm,
                        f"{self.meta['title']} · Edition {self.meta['version']} · {self.meta['edition_date']}")
        canv.drawRightString(PAGE_W - MARGIN, MARGIN - 5 * mm, f"Page {doc.page}")
        canv.restoreState()

    def afterFlowable(self, flowable):
        level = getattr(flowable, "_toc_level", None)
        if level is None:
            return
        outline = min(level, self._outline_level + 1)
        self._outline_level = outline
        self.canv.bookmarkPage(flowable._key)
        self.canv.addOutlineEntry(flowable._plain, flowable._key, level=outline, closed=outline > 0)
        self.notify("TOCEntry", (level, flowable._plain, self.page, flowable._key))

    def handle_documentBegin(self):
        self._outline_level = -1
        super().handle_documentBegin()


def build(out: Path) -> None:
    meta, lines = read_master(MASTER)
    check_glyphs("\n".join(lines))
    pretty = date.fromisoformat(meta["edition_date"]).strftime("%-d %B %Y")

    toc = TableOfContents()
    toc.levelStyles = [
        style("toc0", fontName=BOLD, fontSize=10.5, leading=15, spaceBefore=6, spaceAfter=0),
        style("toc1", fontSize=9.5, leading=13, leftIndent=14, spaceAfter=0),
        style("toc2", fontSize=9, leading=12, leftIndent=28, textColor=SLATE, spaceAfter=0),
    ]
    toc.dotsMinLevel = 0

    cover_logo = []
    if LOGO.exists():
        iw, ih = ImageReader(str(LOGO)).getSize()
        logo = Image(str(LOGO), width=52 * mm, height=52 * mm * ih / iw, hAlign="LEFT")
        cover_logo = [Spacer(1, 18 * mm), logo, Spacer(1, 14 * mm)]
    else:
        print(f"WARNING: logo not found at {LOGO}; cover built without it.")
        cover_logo = [Spacer(1, 52 * mm)]

    story = cover_logo + [
        Paragraph(_esc(meta["title"]), S["cover1"]),
        Paragraph(_esc(meta.get("subtitle", "")), S["cover2"]),
        Paragraph(_esc(meta.get("owner", "")), S["cover3"]),
        Paragraph(f"Edition {_esc(meta['version'])} · {pretty}", S["cover3"]),
        Spacer(1, 22 * mm),
        Paragraph("Editable master: <font name=\"%s\">docs/handbook/handbook.md</font>. "
                  "Earlier editions are kept in <font name=\"%s\">docs/handbook/editions/</font>."
                  % (MONO, MONO), style("coverfoot", fontSize=8.5, textColor=MUTED)),
        NextPageTemplate("body"), PageBreak(),
        Paragraph("Contents", S["h1"]), toc, PageBreak(),
    ] + parse(lines, TEXT_W)

    Heading.counter = 0
    out.parent.mkdir(parents=True, exist_ok=True)
    doc = HandbookDoc(str(out), meta)
    doc.multiBuild(story)
    print(f"Built {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}  ({doc.page} pages)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", type=Path, help="write a draft to this path instead of a new edition")
    args = ap.parse_args()
    if args.out:
        build(args.out.resolve())
        return 0
    meta, _ = read_master(MASTER)
    target = EDITIONS / f"lupine-energy-engineering-handbook-v{meta['version']}-{meta['edition_date']}.pdf"
    if target.exists():
        print(f"Edition {meta['version']} already exists at {target.relative_to(ROOT)}.\n"
              "Editions are never overwritten. Raise 'version' in the master's front matter.")
        return 1
    build(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
