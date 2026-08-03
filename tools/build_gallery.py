"""Assemble the logo-concept gallery HTML with inlined SVGs."""
import pathlib

TMP = pathlib.Path(__file__).parent
CURRENT = pathlib.Path(__file__).resolve().parent.parent / "images" / "logo-mark.svg"

CONCEPTS = [
    ("A", "spark", "Convergence",
     "Streams of measurements flow together and ignite. Data converging into a moment of discovery — the most dynamic of the six, and the only one that isn't symmetric.",
     "Directional, energetic; works well next to a left-aligned wordmark."),
    ("B", "iris", "Iris",
     "An eye whose iris is a radial neural network, with a catchlight in the pupil. Instruments observe; AI sees. A quiet nod to the vision-science thread among the organizers.",
     "Densest and most emblem-like; strong at large sizes, mandala-like presence."),
    ("C", "helix", "Helix",
     "A double helix where one strand is a smooth fitted model and the other is raw data points, held together by rungs. AI models entwined with scientific measurement.",
     "Reads instantly as science; tall aspect suits stacked lockups and favicons."),
    ("D", "molecule", "Molecule circuit",
     "A benzene ring wired into circuit traces with gold pads — wet lab fused with silicon. The most literal 'AI meets science' of the set.",
     "Crisp at small sizes; the right-angle traces contrast nicely with the ring."),
    ("E", "ascent", "Ascent",
     "A cloud of measurements with faint residual whiskers, a fitted curve rising through it to a summit that flares gold. Every statistician's favorite picture, elevated.",
     "Narrative and optimistic; pairs beautifully with a tagline about discovery."),
    ("F", "four", "The network four",
     "The 4 of AIDa4Sci drawn as a network — nodes at every joint, a gold terminal, faint data dust around it. A monogram no one else can own.",
     "Most brand-forward; doubles as favicon and social avatar with zero loss."),
]

def svg(path):
    return path.read_text().strip()

rows = []
for letter, slug, name, thesis, note in CONCEPTS:
    light = svg(TMP / f"{slug}.svg")
    dark = svg(TMP / f"{slug}-dark.svg")
    rows.append(f"""
<section class="row" id="{slug}">
  <div class="meta">
    <div class="letter">{letter}</div>
    <h2>{name}</h2>
    <p class="thesis">{thesis}</p>
    <p class="note">{note}</p>
  </div>
  <div class="boards">
    <div class="panels">
      <figure class="panel panel-light">{light}<figcaption>light</figcaption></figure>
      <figure class="panel panel-dark">{dark}<figcaption>dark</figcaption></figure>
    </div>
    <div class="context">
      <div class="navmock"><span class="navmark">{light}</span><span class="navtitle">AI + Data for Science</span><span class="navlinks">Home&ensp;Schedule&ensp;Past Quarters</span></div>
      <div class="favrow"><span class="fav fav32">{light}</span><span class="fav fav16">{light}</span><span class="favlabel">32 / 16 px</span></div>
    </div>
  </div>
</section>""")

current = svg(CURRENT)

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AIDa4Sci — Logo Explorations</title>
<style>
:root {{
  --paper: #FBFAF8; --ink: #2E2D29; --stone: #7F7776; --line: #E5E2DD;
  --cardinal: #8C1515; --panel-light: #FFFFFF; --panel-dark: #1B1917;
}}
@media (prefers-color-scheme: dark) {{
  :root {{ --paper: #171512; --ink: #E8E4DD; --stone: #A39D94; --line: #37332E; --cardinal: #D46A6A; }}
}}
:root[data-theme="dark"] {{ --paper: #171512; --ink: #E8E4DD; --stone: #A39D94; --line: #37332E; --cardinal: #D46A6A; }}
:root[data-theme="light"] {{ --paper: #FBFAF8; --ink: #2E2D29; --stone: #7F7776; --line: #E5E2DD; --cardinal: #8C1515; }}

body {{
  background: var(--paper); color: var(--ink);
  font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  margin: 0; padding: 0 1.25rem;
}}
.wrap {{ max-width: 68rem; margin: 0 auto; }}
header {{ padding: 3.5rem 0 2rem; border-bottom: 2px solid var(--cardinal); }}
.eyebrow {{
  font: 600 0.72rem/1 ui-monospace, "SF Mono", Menlo, monospace;
  letter-spacing: 0.18em; color: var(--cardinal); text-transform: uppercase;
}}
h1 {{
  font-family: "Iowan Old Style", Georgia, "Times New Roman", serif;
  font-size: clamp(1.9rem, 4.5vw, 2.8rem); font-weight: 600;
  margin: 0.5rem 0 0.75rem; text-wrap: balance;
}}
header p {{ max-width: 42rem; color: var(--stone); margin: 0 0 1.5rem; }}
.reference {{ display: flex; align-items: center; gap: 0.75rem; color: var(--stone); font-size: 0.85rem; }}
.reference svg {{ width: 44px; height: 44px; flex: none; }}

.row {{ display: grid; grid-template-columns: 17rem 1fr; gap: 2rem; padding: 2.5rem 0; border-bottom: 1px solid var(--line); }}
.letter {{
  font: 700 0.8rem/1.9 ui-monospace, "SF Mono", Menlo, monospace;
  color: var(--paper); background: var(--cardinal); width: 1.9em; height: 1.9em;
  border-radius: 50%; text-align: center; margin-bottom: 0.6rem;
}}
h2 {{
  font-family: "Iowan Old Style", Georgia, "Times New Roman", serif;
  font-size: 1.45rem; font-weight: 600; margin: 0 0 0.5rem;
}}
.thesis {{ margin: 0 0 0.75rem; }}
.note {{ color: var(--stone); font-size: 0.9rem; margin: 0; }}

.panels {{ display: flex; gap: 1rem; flex-wrap: wrap; }}
.panel {{
  margin: 0; border: 1px solid var(--line); border-radius: 0.5rem;
  padding: 1.4rem; width: 200px;
}}
.panel svg {{ width: 100%; height: auto; display: block; }}
.panel-light {{ background: var(--panel-light); }}
.panel-dark {{ background: var(--panel-dark); border-color: #000; }}
figcaption {{
  font: 500 0.68rem/1 ui-monospace, "SF Mono", Menlo, monospace;
  letter-spacing: 0.14em; text-transform: uppercase; color: var(--stone);
  margin-top: 0.9rem; text-align: center;
}}
.panel-dark figcaption {{ color: #8d8779; }}

.context {{ margin-top: 1rem; display: flex; flex-direction: column; gap: 0.75rem; }}
.navmock {{
  display: flex; align-items: center; gap: 0.6rem;
  background: #fff; color: #2E2D29; border: 1px solid var(--line);
  border-top: 3px solid #8C1515; border-radius: 0.4rem;
  padding: 0.55rem 0.9rem; max-width: 34rem;
}}
.navmark svg {{ width: 28px; height: 28px; display: block; }}
.navtitle {{ font-weight: 700; color: #8C1515; font-size: 0.95rem; white-space: nowrap; }}
.navlinks {{ color: #53565A; font-size: 0.83rem; margin-left: auto; white-space: nowrap; }}
.favrow {{ display: flex; align-items: center; gap: 0.7rem; }}
.fav {{ background: var(--panel-light); border: 1px solid var(--line); border-radius: 0.25rem; padding: 3px; line-height: 0; }}
.fav32 svg {{ width: 32px; height: 32px; }}
.fav16 svg {{ width: 16px; height: 16px; }}
.favlabel {{ font: 500 0.7rem/1 ui-monospace, "SF Mono", Menlo, monospace; color: var(--stone); letter-spacing: 0.1em; }}

footer {{ padding: 2rem 0 3.5rem; color: var(--stone); font-size: 0.88rem; max-width: 46rem; }}
footer code {{ font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: 0.82em; }}

@media (max-width: 760px) {{
  .row {{ grid-template-columns: 1fr; gap: 1.25rem; }}
  .navlinks {{ display: none; }}
}}
</style>
</head>
<body>
<div class="wrap">
<header>
  <div class="eyebrow">AIDa4Sci &middot; Logo exploration &middot; August 2026</div>
  <h1>Six directions for the mark</h1>
  <p>Each concept keeps Stanford cardinal as the anchor, adds one gold accent
  where the idea earns it, and is drawn as pure SVG &mdash; crisp at any size,
  trivially recolorable. Every mark is shown on light and dark grounds, in the
  site navbar, and at favicon sizes.</p>
  <div class="reference">{current}<span>For comparison: the current mark &mdash; the &ldquo;observatory&rdquo; ring
  now on the site. The concepts below are denser and more figurative.</span></div>
</header>
{''.join(rows)}
<footer>
  <p>Sources live in <code>~/DSI/Marlowe/Seminar/tmp/</code> &mdash; each concept as
  <code>&lt;name&gt;.svg</code> plus a <code>-dark</code> variant, generated by
  <code>gen_logos.py</code>, with PNG contact sheets. Pick a direction (or a
  hybrid &mdash; e.g. a concept placed inside the current ring) and it will be
  refined into mark + lockup + favicon and dropped into the site.</p>
</footer>
</div>
</body>
</html>
"""

(TMP / "gallery.html").write_text(html)
print("wrote", TMP / "gallery.html", len(html), "bytes")
