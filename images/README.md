# Artwork

## Page mastheads

Every page opens with a full-bleed dark masthead; the paper-white content
below reads against it as a deliberate, hard contrast. The five masthead
drawings share one art direction:

- **Ground** — night (`#171310`), with a warm raised wash behind the
  subject. The same geometry re-inks onto paper via `set_theme(DAY)` if a
  light masthead is ever wanted.
- **Ink** — cardinal at three weights (hairline / structure / emphasis)
  plus a single warm ember accent, used sparingly.
- **Form** — one dominant subject each, *generated from real mathematics*
  (projected 3D helices, an Apollonian packing built by the Descartes
  reflection formula, marching-squares level sets, sampled mixtures),
  never assembled from stock motifs.
- **Composition** — the left 44% of every drawing is deliberately quiet;
  that is where the page title lands. The subject weights right and bleeds
  off the edge, so each reads as a detail cropped from something larger.
- **No captions.** The artwork carries no titles or numbering. A visitor
  sees a masthead, not a plate in a catalogue, and anything they cannot
  decode is just noise.

| File | Subject |
|------|---------|
| `banners/plate-fold.svg` | Protein structure prediction |
| `banners/plate-proof.svg` | Formalized mathematics (Lean) |
| `banners/plate-cell.svg` | Single-cell atlases |
| `banners/plate-field.svg` | Physical fields / loss surfaces |
| `banners/plate-attention.svg` | The attention mechanism |

The masthead *is* Quarto's title block, styled. A page gets one by giving
itself a title, a subtitle, and a plate — all in its front matter:

```yaml
---
pagetitle: "Schedule · Winter 2027 · AI + Data for Science"
title: "Schedule · Winter 2027"
subtitle: "Speakers and topics"
header-includes: |
  <style>#title-block-header { --plate-image: url("images/banners/plate-cell.svg"); }</style>
---
```

Point `--plate-image` at any of the five plates above. Giving each quarter
its own masthead is the intended use.

Use `header-includes`, not `include-in-header`, for that style block. A
page-level `include-in-header` *replaces* the project-level one in
`_quarto.yml` rather than adding to it, which would silently drop the skip
link and the theme-color meta from that page. `header-includes` merges.

Writing the masthead by hand instead is a mistake worth naming: Quarto hoists
an `<h1>` into its own title block whenever the heading is the first element
in its container, which silently empties a hand-built banner and drops the
title onto the page below it. Letting the title block be the banner sidesteps
that, and gives every page a real `<h1>` first in the document — which is what
screen readers and WCAG 2.4.6 want.

The home page does not use these: its hero is a live particle simulation
(`js/convergence.js`) of measurements streaming in and igniting at a
focus — the logo's idea, moving. It honors `prefers-reduced-motion` by
drawing a single settled frame.

## Regenerating

The mastheads are generated, not hand-drawn — edit the parameters in
`tools/gen_plates.py` and re-run rather than editing SVG by hand:

```sh
mkdir -p /tmp/plates && cd /tmp/plates          # it writes into the cwd
uv run --with resvg-py --with pillow python "$OLDPWD/tools/gen_plates.py"
cp plate-fold.svg plate-proof.svg plate-cell.svg plate-field.svg \
   plate-attention.svg "$OLDPWD/images/banners/"
```

The script writes both night and day (`-day`) variants plus PNG contact
sheets for reviewing the set together. It is deterministic — re-running it
unchanged reproduces the committed SVGs byte for byte.

## Logo

`logo-mark.svg` (emblem), `logo-mark-light.svg` (for the dark navbar), and
`logo-lockup.svg` (emblem + wordmark) are the *Convergence* mark: streams
of measurements flowing together and igniting.

`tools/gen_logos.py` regenerates it along with five alternate concepts
(iris, helix, molecule, ascent, network-four); `tools/build_gallery.py`
then builds a side-by-side comparison page from them, shown on light and
dark grounds, in the navbar, and at favicon sizes. Run `gen_logos.py`
first — the gallery reads the concept SVGs it writes.

## Type

`Newsreader` (display) over `Source Sans 3` (body), bundled locally in
`fonts/` with `fonts.css` — no CDN at runtime. Re-fetch with
`uv run python tools/fetch_fonts.py`, which writes both directly into the
repository.
