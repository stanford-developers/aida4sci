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

Because this repository is private inside an enterprise organization,
Pages defaults to **private** visibility — it is then served from a
randomized `*.pages.github.io` hostname and requires a GitHub login with
organization membership. Set the Pages visibility to **Public** in the
same settings page, or external speakers cannot reach the schedule.

The workflow also runs on a schedule, Thursdays at 08:00 UTC. That is
deliberate: the home page's "Up next" card is resolved against the build
date, so without a periodic rebuild the site would keep advertising a
seminar that already happened. The weekly run rolls the card over the
morning after each Wednesday seminar. You can also trigger a rebuild by
hand from the Actions tab.

### The stanford.edu address

**<https://aida4sci.stanford.edu>** is the address to hand out — on slides,
in speaker invitations, anywhere human-facing.

It is a **redirect, not a GitHub Pages custom domain**. Stanford points the
host at their link service (`stanford.dns.bl.ink`), which answers with a
307 to `https://stanford-developers.github.io/aida4sci/`. Paths are
forwarded, so deep links work; the redirect inserts a harmless double
slash (`/aida4sci//schedule.html`) that Pages resolves fine.

Because DNS does **not** point at GitHub, do *not* add a `CNAME` file or set
a custom domain under *Settings → Pages*. GitHub would attempt to verify the
domain, fail, and unpublish the site. For the same reason `website.site-url`
in `_quarto.yml` stays on the `github.io` address: that is where the pages
actually live, and it is what belongs in the sitemap and in canonical link
previews.

Should Stanford ever repoint the host at `stanford-developers.github.io`
directly, the custom-domain route becomes available: add a `CNAME` file at
the repository root, list it under `project.resources` in `_quarto.yml` so
it is copied into `_site/`, set the domain in *Settings → Pages*, and update
`site-url` to match.

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
