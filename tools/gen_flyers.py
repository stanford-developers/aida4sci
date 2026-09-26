#!/usr/bin/env python3
"""Print-ready US Letter flyers, one per confirmed talk, for bulletin boards.

Reads the same `speakers/*.yml` files as the site and the calendar feed, lays
each talk out as an HTML page in the site's type and palette, and prints it to
PDF with headless Chrome:

    uv run --with pyyaml python tools/gen_flyers.py                  # all talks
    uv run --with pyyaml python tools/gen_flyers.py --date 2026-09-23

Output goes to `_flyers/` (ignored by git and by Quarto). Long abstracts are
shrunk to fit the page rather than spilling onto a second sheet.
"""
import argparse
import html
import pathlib
import subprocess
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from gen_ics import (  # noqa: E402  (shared YAML loading and defaults)
    DEFAULT_END,
    DEFAULT_START,
    REPO,
    as_date,
    as_time,
    load_entries,
)

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DEFAULT_ROOM = "CoDA E160"   # keep in step with ejs/speaker.ejs
PLATE = "images/banners/plate-fold.svg"
COURSES = "EE 292R · PSYCH 292R · STATS 282"
SITE = "aida4sci.stanford.edu"

CSS = """
@page { size: 8.5in 11in; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; }
body {
  width: 8.5in; height: 11in; overflow: hidden;
  display: flex; flex-direction: column;
  background: #FBFAF8; color: #2E2D29;
  font-family: "Source Sans 3", sans-serif;
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
.masthead {
  position: relative; height: 2.9in; flex: none;
  background: #171310 url("%(plate)s") right center / cover no-repeat;
  padding: 0.55in 0.65in 0;
  color: #FAF6F0;
}
.masthead .brand { display: flex; align-items: center; gap: 0.22in; }
.masthead img { width: 1.05in; height: 1.05in; }
.eyebrow {
  font-family: ui-monospace, "SF Mono", Menlo, monospace;
  font-size: 9.5pt; letter-spacing: 0.2em; text-transform: uppercase;
  color: #E9A03E; margin-bottom: 0.08in;
}
.series {
  font-family: "Newsreader", serif; font-weight: 600;
  font-size: 40pt; line-height: 1.02; letter-spacing: -0.022em;
}
.series em { font-style: italic; color: #E9A03E; }
.courses {
  margin-top: 0.12in; font-size: 11pt; letter-spacing: 0.08em;
  color: rgba(232, 226, 217, 0.78);
}
.when {
  flex: none; display: flex; gap: 0.35in; align-items: baseline;
  background: #8C1515; color: #FFFFFF;
  padding: 0.16in 0.65in; font-size: 17pt; font-weight: 600;
}
.when .date { font-family: "Newsreader", serif; font-size: 21pt; }
.when .note { font-size: 11pt; font-weight: 400; opacity: 0.9; }
.content { flex: 1; display: flex; flex-direction: column; min-height: 0;
  padding: 0.45in 0.65in 0; }
.speaker { display: flex; align-items: center; gap: 0.3in; flex: none; }
.speaker img {
  width: 1.55in; height: 1.55in; object-fit: cover; border-radius: 50%%;
  border: 3px solid #E5E2DD;
}
.name { font-family: "Newsreader", serif; font-weight: 600; font-size: 28pt;
  line-height: 1.1; }
.affiliation { font-size: 14pt; color: #53565A; margin-top: 0.04in; }
.title {
  flex: none; font-family: "Newsreader", serif; font-weight: 600;
  font-size: 23pt; line-height: 1.18; color: #8C1515;
  margin: 0.32in 0 0.2in; text-wrap: balance;
}
.abstract { flex: 1; min-height: 0; overflow: hidden;
  font-size: 12.5pt; line-height: 1.45; text-align: justify; hyphens: auto; }
.abstract p { margin: 0; }
footer {
  flex: none; display: flex; justify-content: space-between;
  margin: 0 0.65in; padding: 0.14in 0 0.4in; border-top: 1px solid #E5E2DD;
  font-size: 10.5pt; color: #746C6B;
}
footer strong { color: #8C1515; }
"""

# Shrink the abstract until the page stops overflowing; floor at 9pt.
FIT = """
document.fonts.ready.then(function () {
  var box = document.querySelector(".abstract");
  var size = parseFloat(getComputedStyle(box).fontSize);
  while (box.scrollHeight > box.clientHeight + 1 && size > 12) {
    size -= 0.25;
    box.style.fontSize = size + "px";
  }
  document.body.dataset.fitted = "1";
});
"""


def clock(t) -> str:
    """16:30 -> '4:30'."""
    return f"{t.hour % 12 or 12}:{t.minute:02d}"


def page(entry: dict) -> str:
    e = lambda key: html.escape(str(entry.get(key) or "").strip())  # noqa: E731
    day = as_date(entry["date"])
    start = as_time(entry.get("start_time"), DEFAULT_START)
    end = as_time(entry.get("end_time"), DEFAULT_END)
    room = str(entry.get("location") or DEFAULT_ROOM).strip()
    note = (f'<span class="note">not the usual {DEFAULT_ROOM}</span>'
            if room != DEFAULT_ROOM else "")
    photo = entry.get("photo") or "images/speakers/placeholder.svg"
    quarter = {9: "Fall", 10: "Fall", 11: "Fall", 12: "Fall",
               1: "Winter", 2: "Winter", 3: "Winter"}.get(day.month, "Spring")
    abstract = e("abstract")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<base href="{REPO.as_uri()}/">
<title>{e('name')} · {day:%B %-d} · AI + Data for Science</title>
<link rel="stylesheet" href="fonts.css">
<style>{CSS % {'plate': PLATE}}</style>
</head><body>
<header class="masthead"><div class="brand">
<img src="images/logo-mark-light.svg" alt="">
<div>
<div class="eyebrow">Stanford University · Seminar · {quarter} {day.year}</div>
<div class="series">AI + Data for <em>Science</em></div>
<div class="courses">{COURSES}</div>
</div></div></header>
<div class="when">
<span class="date">{day:%A, %B %-d}</span>
<span>{clock(start)}–{clock(end)} pm</span>
<span>{html.escape(room)} {note}</span>
</div>
<main class="content">
<div class="speaker">
<img src="{html.escape(photo)}" alt="">
<div><div class="name">{e('name')}</div>
<div class="affiliation">{e('affiliation')}</div></div>
</div>
<div class="title">{e('title_plain') or e('title')}</div>
<div class="abstract">{f'<p>{abstract}</p>' if abstract else ''}</div>
</main>
<footer><span><strong>{SITE}</strong> · schedule, calendar feed, mailing list</span>
<span>Wednesdays · {DEFAULT_ROOM}</span></footer>
<script>{FIT}</script>
</body></html>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--date", action="append",
                    help="only this talk (YYYY-MM-DD); repeatable")
    ap.add_argument("--out", type=pathlib.Path, default=REPO / "_flyers")
    args = ap.parse_args()

    talks = [t for t in load_entries(REPO / "speakers")
             if t.get("name") and not t.get("tba")]
    if args.date:
        talks = [t for t in talks if str(as_date(t["date"])) in args.date]
    if not talks:
        print("no matching confirmed talks", file=sys.stderr)
        return 1

    args.out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as profile:
        for talk in talks:
            day = as_date(talk["date"])
            slug = str(talk["name"]).lower().replace(" ", "-")
            src = args.out / f"{day}-{slug}.html"
            pdf = src.with_suffix(".pdf")
            src.write_text(page(talk), encoding="utf-8")
            subprocess.run(
                [CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                 f"--user-data-dir={profile}", "--allow-file-access-from-files",
                 "--virtual-time-budget=5000", f"--print-to-pdf={pdf}",
                 src.as_uri()],
                check=True, capture_output=True)
            print(pdf)
    return 0


if __name__ == "__main__":
    sys.exit(main())
