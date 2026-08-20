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

### Pointing a stanford.edu address at it

Until a stanford.edu host is wired up, the live address is
<https://stanford-developers.github.io/aida4sci/>, and `website.site-url` in
`_quarto.yml` matches it.

**Ask NetDB for a DNS `CNAME` record, not a redirect.** The record wanted is

```
aida4sci.stanford.edu.   IN   CNAME   stanford-developers.github.io.
```

A first attempt produced a host pointed at Stanford's link service
(`stanford.dns.bl.ink`), which answered with a 307 to the `github.io` URL.
That is a forwarder, not a custom domain: the address bar still showed the
`github.io` URL, GitHub could not issue a certificate for the name, and
adding a `CNAME` file under it would have failed domain verification and
unpublished the site. If NetDB will not put a `CNAME` at that name, the
fallback is `A` records to GitHub's Pages addresses — `185.199.108.153`,
`185.199.109.153`, `185.199.110.153`, `185.199.111.153` — but the `CNAME`
is preferred, since it survives GitHub renumbering those.

Once `dig +short aida4sci.stanford.edu` answers with `stanford-developers.github.io`:

1. Add a file named `CNAME` at the repository root containing just the
   hostname, and list it under `project.resources` in `_quarto.yml` so it is
   copied into `_site/` on every render.
2. Set the domain under *Settings → Pages* (or
   `gh api -X PUT repos/stanford-developers/aida4sci/pages -f cname=aida4sci.stanford.edu`).
3. Wait for GitHub to provision the certificate, then tick **Enforce HTTPS**.
4. Set `website.site-url` in `_quarto.yml` to `https://aida4sci.stanford.edu/`
   — it feeds the sitemap and the link previews shown by search engines and
   chat apps. GitHub will then redirect the old `github.io` URL to the new one.

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
