#!/usr/bin/env python3
"""Generate a subscribable iCalendar feed from the quarterly speaker YAML.

Reads the same `speakers/*.yml` files the Quarto listings use and writes one
VEVENT per seminar date, so people can subscribe once and have every talk land
in their own calendar with their own reminders. Run after `quarto render`; the
output goes into the built site and publishes with everything else.

    python tools/gen_ics.py --out _site/seminar.ics

Times live in the YAML as dates only. The hour, room, and time zone are the
constants below, overridable per entry with `start_time`, `end_time`, and
`location` keys if a talk ever moves.
"""
import argparse
import datetime as dt
import pathlib
import sys
from zoneinfo import ZoneInfo

import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent

TZ = ZoneInfo("America/Los_Angeles")
SITE = "https://aida4sci.stanford.edu"
CAL_NAME = "AI + Data for Science Seminar"
CAL_DESC = "Stanford seminar series on scientific advances driven by AI and data."
UID_DOMAIN = "aida4sci.stanford.edu"

DEFAULT_LOCATION = "CoDA E160, Stanford University"
DEFAULT_START = dt.time(16, 30)
DEFAULT_END = dt.time(17, 30)


def esc(value) -> str:
    """Escape a string for an iCalendar TEXT value (RFC 5545 3.3.11)."""
    s = str(value)
    s = s.replace("\\", "\\\\")
    s = s.replace(";", "\\;")
    s = s.replace(",", "\\,")
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    return s.replace("\n", "\\n")


def fold(line: str) -> str:
    """Fold a content line to 75 octets, continuing with a leading space.

    Folding is by octet, not character, so the split has to avoid landing in
    the middle of a multi-byte sequence.
    """
    raw = line.encode("utf-8")
    if len(raw) <= 75:
        return line
    chunks = []
    start, limit = 0, 75
    while start < len(raw):
        end = min(start + limit, len(raw))
        while end > start and end < len(raw) and raw[end] & 0xC0 == 0x80:
            end -= 1
        chunks.append(raw[start:end].decode("utf-8"))
        start, limit = end, 74
    return "\r\n ".join(chunks)


def as_date(value) -> dt.date:
    """YAML gives a date for `2026-09-23`, but a string if it was quoted."""
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    return dt.date.fromisoformat(str(value).strip())


def as_time(value, default: dt.time) -> dt.time:
    if value is None:
        return default
    if isinstance(value, dt.time):
        return value
    text = str(value).strip()
    for fmt in ("%H:%M", "%H:%M:%S"):
        try:
            return dt.datetime.strptime(text, fmt).time()
        except ValueError:
            continue
    raise ValueError(f"could not parse time {value!r}; expected HH:MM")


def utc_stamp(day: dt.date, clock: dt.time) -> str:
    """Local wall-clock time to a UTC iCalendar timestamp.

    Emitting UTC rather than shipping a VTIMEZONE block keeps the file simple
    and unambiguous, and zoneinfo handles the November DST change for us.
    """
    local = dt.datetime.combine(day, clock, tzinfo=TZ)
    return local.astimezone(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def load_entries(speakers: pathlib.Path) -> list[dict]:
    """Every quarter file in speakers/, minus the template."""
    entries = []
    for path in sorted(speakers.glob("*.yml")):
        if path.name.startswith("_"):
            continue
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not loaded:
            continue
        if not isinstance(loaded, list):
            raise SystemExit(f"{path}: expected a list of entries")
        for entry in loaded:
            if isinstance(entry, dict) and entry.get("date"):
                entries.append(entry)
    return entries


def event_lines(entry: dict, stamp: str) -> list[str]:
    day = as_date(entry["date"])
    start = as_time(entry.get("start_time"), DEFAULT_START)
    end = as_time(entry.get("end_time"), DEFAULT_END)

    name = entry.get("name")
    named = bool(name) and not entry.get("tba")
    summary = f"{CAL_NAME}: {name}" if named else f"{CAL_NAME}: speaker TBA"

    # LaTeX in a title passes through verbatim. A calendar client will show it
    # as source rather than typeset math, which is legible enough for this
    # audience and beats maintaining a second copy of every title.
    title = entry.get("title")

    # Deliberately not the abstract. A calendar entry people see every week
    # should stay scannable; several hundred words of prose in it is clutter,
    # and abstracts are also where math lives, which no calendar client
    # renders. The link goes straight to this talk on the website.
    described = []
    if title:
        described.append(str(title))
    if entry.get("affiliation"):
        described.append(str(entry["affiliation"]))
    if described:
        described.append("")
    described.append(f"Abstract: {SITE}/schedule.html#{day.isoformat()}")

    return [
        "BEGIN:VEVENT",
        # Keyed on the date alone, so a slot keeps its identity when a TBA
        # becomes a named speaker. Changing this scheme would orphan every
        # event already sitting in a subscriber's calendar.
        f"UID:{day.isoformat()}@{UID_DOMAIN}",
        f"DTSTAMP:{stamp}",
        f"DTSTART:{utc_stamp(day, start)}",
        f"DTEND:{utc_stamp(day, end)}",
        f"SUMMARY:{esc(summary)}",
        f"DESCRIPTION:{esc(chr(10).join(described))}",
        f"LOCATION:{esc(entry.get('location') or DEFAULT_LOCATION)}",
        f"URL:{SITE}/schedule.html#{day.isoformat()}",
        "STATUS:CONFIRMED",
        "TRANSP:OPAQUE",
        "SEQUENCE:0",
        "END:VEVENT",
    ]


def build(entries: list[dict]) -> str:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//AI + Data for Science//Seminar Schedule//EN",
        "CALSCALE:GREGORIAN",
        # PUBLISH, never REQUEST: this is a calendar to read, not an invitation
        # that would make every subscriber an attendee and send RSVPs back.
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:{esc(CAL_NAME)}",
        f"X-WR-CALDESC:{esc(CAL_DESC)}",
        "X-WR-TIMEZONE:America/Los_Angeles",
        # Hints only; clients pick their own refresh interval regardless.
        "REFRESH-INTERVAL;VALUE=DURATION:PT12H",
        "X-PUBLISHED-TTL:PT12H",
    ]
    for entry in sorted(entries, key=lambda e: as_date(e["date"])):
        lines.extend(event_lines(entry, stamp))
    lines.append("END:VCALENDAR")
    return "".join(fold(line) + "\r\n" for line in lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--speakers",
        type=pathlib.Path,
        default=REPO / "speakers",
        help="directory of quarter YAML files (default: speakers/)",
    )
    parser.add_argument(
        "--out",
        type=pathlib.Path,
        default=REPO / "_site" / "seminar.ics",
        help="output path (default: _site/seminar.ics)",
    )
    args = parser.parse_args()

    entries = load_entries(args.speakers)
    if not entries:
        # Publishing an empty calendar would quietly delete every event from
        # every subscriber's calendar, so treat it as a build failure.
        print("error: no dated entries found in speakers/*.yml", file=sys.stderr)
        return 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(build(entries).encode("utf-8"))
    print(f"wrote {args.out} ({len(entries)} events)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
