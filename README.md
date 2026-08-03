# AI + Data for Science (AIDa4Sci)

Quarto website for the Stanford seminar series **AI + Data for
Science** (STATS 282 / EE 292R / PSYCH 292R), Wednesdays 4:30–5:30 pm
in CoDA E160.

## Local preview and build

```sh
quarto preview   # live-reloading local server
quarto render    # builds the site into _site/
```

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
- `images/` — logo (`logo-mark.svg`, `logo-lockup.svg`), hero
  background, speaker photos
