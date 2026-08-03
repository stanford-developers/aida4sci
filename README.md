# AI + Data for Science (AIDa4Sci)

Quarto website for the Stanford seminar series **AI + Data for
Science** (EE 292R / PSYCH 292R / STATS 282), Wednesdays 4:30–5:30 pm
in CoDA E160.

## Local preview and build

```sh
quarto preview   # live-reloading local server
quarto render    # builds the site into _site/
```

## Publishing

Pushing to `main` builds and deploys the site via GitHub Actions
(`.github/workflows/publish.yml`). Nothing is committed to a `gh-pages`
branch — the built site is uploaded straight to Pages.

**One-time setup:** in the repository's *Settings → Pages*, set **Source**
to **GitHub Actions**. Until that is done the deploy step fails.

The workflow also runs on a schedule, Thursdays at 08:00 UTC. That is
deliberate: the home page's "Up next" card is resolved against the build
date, so without a periodic rebuild the site would keep advertising a
seminar that already happened. The weekly run rolls the card over the
morning after each Wednesday seminar. You can also trigger a rebuild by
hand from the Actions tab.

### Pointing a stanford.edu domain at it

1. Ask for a CNAME record for the desired host (e.g. `stats282.stanford.edu`)
   pointing at `bnaras.github.io`.
2. Add a file named `CNAME` at the repository root containing just that
   hostname, and list it under `project.resources` in `_quarto.yml` so it is
   copied into `_site/`.
3. Set `website.site-url` in `_quarto.yml` to the new address — it feeds the
   sitemap and the link previews shown by search engines and chat apps.

## "Up next" on the home page

The home page shows the next seminar automatically — there is nothing to
update by hand. `ejs/upnext.ejs` reads the same quarter YAML file as the
schedule and picks the next *confirmed* speaker whose date has not passed.
If the nearest dates are still unbooked it falls back to the next
scheduled date and says the speaker is not announced yet; once the whole
quarter is past, the block disappears rather than showing something stale.

## Adding a speaker

1. Open the current quarter's data file, e.g. `speakers/fall-2026.yml`.
2. Replace the `tba: true` entry for the chosen date with a filled-in
   block — copy the example in `speakers/_template.yml`. Fields you
   omit (url, photo, bio, …) are simply not shown.
3. Drop a square-ish photo into `images/speakers/` (e.g.
   `images/speakers/jane-doe.jpg`) and reference it in the `photo`
   field. If there is no photo, omit the field and a neutral
   placeholder is used.
4. `quarto render`.

## Starting a new quarter

1. Create `speakers/<quarter>.yml` (e.g. `speakers/2027-winter.yml`)
   with one entry per seminar Wednesday.
2. Point the listing in `schedule.qmd` at the new file and update its
   title.
3. Archive the finished quarter: create `past/<quarter>.qmd` with the
   same listing front matter pointing at the old YAML file, and link it
   from `past.qmd`.

## Structure

- `_quarto.yml` — site config (navbar, footer, theme)
- `styles.scss` — Stanford-cardinal styling, talk-card layout
- `speakers/*.yml` — one file per quarter; the single source of truth
  for the schedule
- `ejs/speaker.ejs` — template that renders each talk card
- `images/` — logo, page mastheads, speaker photos; see
  `images/README.md` for the art direction and how to regenerate them
- `tools/` — the generators that produce the artwork and bundle the fonts.
  The mastheads and logo are *generated, not hand-drawn*: change the
  parameters and re-run rather than editing SVG by hand
- `fonts/` + `fonts.css` — bundled webfonts, so the site needs no CDN
- `js/convergence.js` — the home page's live hero animation
