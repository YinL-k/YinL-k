#!/usr/bin/env python3
"""Render GitHub's publicly visible contribution calendar as a self-hosted SVG.

GitHub can include anonymized private contributions in the publicly visible
calendar *if the account owner enables Private contributions*. This script
reads only that public calendar; it never accesses private repositories.
The HTML endpoint is undocumented, so parsing fails closed if its format
changes instead of silently publishing an incomplete contribution total.
"""
from datetime import date, timedelta
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
import json
import re
import os
from xml.sax.saxutils import escape

USER = os.getenv("PROFILE_USERNAME", "YinL-k")
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)
END = date.today()
START = END - timedelta(days=364)
COUNT_RE = re.compile(r"([\d,]+)\s+contributions?\s+on\b", re.I)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
COLORS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]


def esc(value):
    return escape(str(value), {'"': "&quot;"})


def label(x, y, value, size=12, color="#8b949e", weight=400, extra=""):
    return f'<text x="{x}" y="{y}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" fill="{color}" font-weight="{weight}" {extra}>{esc(value)}</text>'


class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.cells = {}
        self.tooltips = {}
        self.active_tooltip = None
        self.tooltip_text = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        date_str = d.get("data-date", "")
        level_str = d.get("data-level", "")
        if DATE_RE.fullmatch(date_str) and level_str in {"0", "1", "2", "3", "4"}:
            self.cells[date_str] = {
                "level": int(level_str),
                "id": d.get("id"),
                "direct_count": d.get("data-count") or d.get("aria-label"),
            }
        if tag == "tool-tip" and d.get("for"):
            self.active_tooltip = d["for"]
            self.tooltip_text = []

    def handle_data(self, data):
        if self.active_tooltip is not None:
            self.tooltip_text.append(data)

    def handle_endtag(self, tag):
        if tag == "tool-tip" and self.active_tooltip is not None:
            self.tooltips[self.active_tooltip] = "".join(self.tooltip_text)
            self.active_tooltip = None
            self.tooltip_text = []


def parse_calendar(source):
    parser = CalendarParser()
    parser.feed(source)
    if len(parser.cells) < 330:
        raise ValueError("GitHub did not return a complete contributions calendar")
    days = {}
    for day_str, cell in parser.cells.items():
        day = date.fromisoformat(day_str)
        if not START <= day <= END:
            continue
        level = cell["level"]
        text = str(cell["direct_count"] or parser.tooltips.get(cell["id"], ""))
        match = COUNT_RE.search(text)
        if not match and text.strip().isdigit():
            count = int(text.strip())
        elif match:
            count = int(match.group(1).replace(",", ""))
        elif level == 0:
            count = 0
        else:
            raise ValueError("Missing exact count for an active GitHub day: " + day_str)
        if count > 0 and level == 0:
            raise ValueError("GitHub contribution level/count mismatch: " + day_str)
        days[day] = {"count": count, "level": level}
    if len(days) < 340 or max(days) < END - timedelta(days=3):
        raise ValueError("Incomplete or stale GitHub calendar returned")
    return days


def fetch_public_calendar():
    url = "https://github.com/users/" + USER + "/contributions"
    request = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; github-profile-chart/1.0)",
        "Accept": "text/html,application/xhtml+xml",
    })
    with urlopen(request, timeout=35) as response:
        html = response.read(3_000_000).decode("utf-8", errors="replace")
    return parse_calendar(html)


def draw_calendar(days):
    total = sum(item["count"] for item in days.values())
    active = sum(1 for item in days.values() if item["count"] > 0)
    width, height = 1050, 254
    a = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="GitHub contributions including anonymously shared private activity when enabled">',
        f'<rect width="{width}" height="{height}" rx="14" fill="#0d1117"/>',
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="13" fill="none" stroke="#30363d"/>',
        label(26, 36, "GITHUB CONTRIBUTIONS", 14, "#c9d1d9", 700),
        label(1024, 36, f"{total:,} contributions  ·  {active} active days", 13, "#8b949e", 400, 'text-anchor="end"'),
    ]
    monday = START - timedelta(days=START.weekday())
    cell, gap, left, top = 13, 3, 64, 85
    for weekday, text in [(0, "Mon"), (2, "Wed"), (4, "Fri")]:
        a.append(label(22, top + weekday * (cell+gap) + 10, text, 11))
    last_month = None
    n = (END-monday).days + 1
    for i in range(n):
        day = monday + timedelta(days=i)
        col, row = divmod(i, 7)
        x, y = left + col*(cell+gap), top + row*(cell+gap)
        if day.month != last_month and day.day <= 7 and row == 0:
            a.append(label(x, 72, day.strftime("%b"), 11))
            last_month = day.month
        item = days.get(day, {"count":0,"level":0}) if START <= day <= END else {"count":0,"level":0}
        count, level = item["count"], item["level"]
        a.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{COLORS[level]}"><title>{day.isoformat()}: {count} contributions</title></rect>')
    a.append(label(26, 230, "Public GitHub profile calendar · includes anonymous private activity when enabled", 11))
    a.append(label(836, 230, "Less", 11))
    for i, color in enumerate(COLORS):
        a.append(f'<rect x="{870+i*18}" y="220" width="12" height="12" rx="2" fill="{color}"/>')
    a.append(label(1024, 230, "More", 11, extra='text-anchor="end"'))
    (OUT / "contribution-calendar.svg").write_text("".join(a)+"</svg>\n",encoding="utf-8")
    return {"contributions": total, "active_days": active, "source": "public_github_profile_calendar", "from": str(START), "to": str(END)}


def main():
    days = fetch_public_calendar()
    summary = draw_calendar(days)
    (OUT / "contribution-summary.json").write_text(json.dumps(summary, indent=2)+"\n", encoding="utf-8")
    print("Publicly visible calendar summary:", json.dumps(summary, sort_keys=True))
    print("Private-repository details are never queried or included.")


if __name__ == "__main__":
    main()
