# AI + Data for Science (AIDa4Sci)

Quarto website for the Stanford seminar series **AI + Data for
Science** (CS 292 / EE 292R / PSYCH 292R / STATS 282), Wednesdays 4:30–5:30 pm
in CoDA E160. A talk held in another room carries a `location` field in
the quarter's YAML file; see "A talk in a different room" below.

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

### The /pickdate short link

<https://aida4sci.stanford.edu/pickdate> sends speakers to the quarter's
Microsoft Bookings page. GitHub Pages has no server-side redirects, so
`pickdate/index.html` is a plain HTML page that forwards in the browser (an
immediate meta refresh, a script, and a fallback link). It is copied into
`_site/` only because `pickdate/` is listed under `project.resources` in
`_quarto.yml`; drop that line and the link breaks.

When a new quarter gets a new Bookings page, replace the URL in
`pickdate/index.html`. It appears four times; change them all.

## "Up next" on the home page

The home page shows the next seminar automatically — there is nothing to
update by hand. `ejs/upnext.ejs` reads the same quarter YAML files as the
schedule (all of them are listed under `contents` in `index.qmd`) and picks
the nearest date that has not passed. If that date is still unbooked it
says the speaker is not announced yet rather than skipping ahead; once
every listed date is past, the block disappears rather than showing
something stale. Because every quarter of the year is listed, the card
rolls from the last Fall talk to the first Winter one on its own.

## Adding a speaker

1. Open the quarter's data file: `speakers/fall-2026.yml`,
   `speakers/winter-2027.yml`, or `speakers/spring-2027.yml`.
2. Replace the `tba: true` entry for the chosen date with a filled-in
   block — copy the example in `speakers/_template.yml`. Fields you
   omit (url, photo, bio, …) are simply not shown.
3. Drop a square-ish photo into `images/speakers/` (e.g.
   `images/speakers/jane-doe.jpg`) and reference it in the `photo`
   field. If there is no photo, omit the field and a neutral
   placeholder is used.
4. `quarto render`.

## A talk in a different room

The usual room, CoDA E160, is not written into the YAML. Add
`location: "Packard 101"` to an entry **only** when that talk meets
somewhere else. Both templates then flag it: the schedule card and the
home page's "Up next" block get an ember notice naming both rooms
("Packard 101, not CoDA E160"), while every other card quietly shows
CoDA E160 beside its date. Leaving `location` off is what means "the
usual room" — do not add it to every entry.

The room links to the campus map by its building name; add
`location_url:` to point somewhere else. The usual room itself is a
constant, `DEFAULT_ROOM`, near the top of both `ejs/speaker.ejs` and
`ejs/upnext.ejs`; if the seminar ever moves for good, change it in both,
and in the prose on the home, schedule, and subscribe pages.

The schedule page also carries a callout listing the exceptions for the
quarter, and the home page's Logistics section repeats it. Those two are
prose, so update them by hand when the exceptions change.

## Quarters and the academic year

The schedule page shows every quarter of the current academic year at
once — Fall, Winter, and Spring, each under its own heading — so speakers
can see the dates still open for the year, and `/pickdate` can book any of
them. All three quarters have to be on the one page: the calendar feed and
the "Up next" card deep-link to a talk as `schedule.html#<ISO date>`, and a
per-quarter page would break those links.

Everything flows from the YAML files, so the whole year is wired up when:

- `speakers/<season>-<year>.yml` exists for each quarter (e.g.
  `speakers/winter-2027.yml`), with one entry per seminar Wednesday —
  `tba: true` until a speaker confirms;
- `schedule.qmd` has a listing (and a heading plus `::: {#id}` block) for
  each file, and a chip for it in the `quarter-nav` jump bar;
- `index.qmd` lists each file under the `upnext` listing's `contents`.

The calendar feed needs nothing: `tools/gen_ics.py` reads every file in
`speakers/`, so unbooked dates publish as "speaker TBA" events that update
in place when a name goes in.

### Adding the next academic year

1. Check the dates against the [Stanford academic
   calendar](https://studentservices.stanford.edu/calendar-events/academic-calendars)
   — drop any Wednesday that is a holiday or recess, as November 25, 2026
   was dropped for Thanksgiving.
2. Create the three YAML files and add them to `schedule.qmd` and
   `index.qmd` as above. Update the year in the schedule page's title and
   the home page's hero eyebrow.
3. Set the Bookings page's availability to match, one window per quarter
   with the breaks between them not bookable.

### Archiving a finished quarter

Once a quarter's last talk has happened (for Fall 2026, after December 2):

1. Create `past/<season>-<year>.qmd` (e.g. `past/fall-2026.qmd`) with a
   title, the plate `header-includes`, and the same listing front matter
   as `schedule.qmd` but pointing only at that quarter's YAML file.
2. Link it from `past.qmd`, replacing the "no past schedules yet" text
   the first time.
3. Remove the quarter from `schedule.qmd`: its listing, its heading and
   `::: {#id}` block, its chip in the jump bar, and any callout that was
   specific to it (the Packard 101 notice is a Fall 2026 one).
4. Remove its YAML file from the `upnext` contents in `index.qmd`, and
   drop any quarter-specific prose from the Logistics section there.

Leave the YAML file where it is — the archive page and the calendar feed
keep reading it. A deep link such as `schedule.html#2026-09-23` from an
old email will no longer land on the card, but the talk stays browsable
in the archive.

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
