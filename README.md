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

**Nothing here needs setting up again.** *Settings → Pages* already has
**Source** set to **GitHub Actions**, and both the repository and the Pages
site are public:

```sh
gh api repos/stanford-developers/aida4sci --jq '.visibility'
gh api repos/stanford-developers/aida4sci/pages --jq '.build_type, .public'
```

Keep it that way. While this repository was private inside an enterprise
organization, Pages defaulted to **private** visibility — served from a
randomized `*.pages.github.io` hostname, behind a GitHub login with
organization membership. Returning to that would put the schedule out of reach
of every external speaker, and would take the custom domain with it, since a
private Pages site cannot carry one.

The workflow also runs on a schedule, Thursdays at 08:00 UTC. That is
deliberate: the home page's "Up next" card is resolved against the build
date, so without a periodic rebuild the site would keep advertising a
seminar that already happened. The weekly run rolls the card over the
morning after each Wednesday seminar. You can also trigger a rebuild by
hand from the Actions tab.

### The stanford.edu address

The site is served at <https://aida4sci.stanford.edu>, with HTTPS enforced
under a GitHub-issued certificate. `website.site-url` in `_quarto.yml` matches
that address — it feeds the sitemap and the link previews search engines and
chat apps show — and GitHub redirects the older
<https://stanford-developers.github.io/aida4sci/> URL to it.

Two things hold the address up, and **neither is visible in this repository**:

- a NetDB DNS record,
  `aida4sci.stanford.edu.  IN  CNAME  stanford-developers.github.io.`
- the custom domain set under *Settings → Pages*, stored on GitHub's side.

There is no `CNAME` file at the repository root. If one is ever added it must
also be listed under `project.resources` in `_quarto.yml`, or `quarto render`
will leave it out of `_site/` and the deploy can drop the domain.

Check both from the command line:

```sh
dig +short aida4sci.stanford.edu CNAME
gh api repos/stanford-developers/aida4sci/pages --jq '.cname, .https_enforced'
```

**If the name ever has to be re-established, ask NetDB for a `CNAME` record,
not a redirect.** The first attempt produced a host pointed at Stanford's link
service (`stanford.dns.bl.ink`), which answered with a 307 to the `github.io`
URL. That is a forwarder, not a custom domain: the address bar still showed the
`github.io` URL, GitHub could not issue a certificate for the name, and setting
the domain under it would have failed verification and unpublished the site. If
NetDB will not put a `CNAME` at that name, the fallback is `A` records to
GitHub's Pages addresses — `185.199.108.153`, `185.199.109.153`,
`185.199.110.153`, `185.199.111.153` — but the `CNAME` is preferred, since it
survives GitHub renumbering those.

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
