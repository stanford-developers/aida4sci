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

To put one on a page, add its class to a banner div:

```markdown
::: {.page-banner .banner-cell}
::: {.banner-inner}
[Winter 2027]{.banner-title}
[Speakers and topics]{.banner-sub}
:::
:::
```

Available: `.banner-fold`, `.banner-proof`, `.banner-cell`,
`.banner-field`, `.banner-attention`. Giving each quarter its own
masthead is the intended use.

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
