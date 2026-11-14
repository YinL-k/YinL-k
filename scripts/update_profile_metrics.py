#!/usr/bin/env python3
"""Generate self-hosted GitHub Profile statistics and language SVGs.

Public repository metadata and code language bytes come from GitHub REST.
The contribution total comes from GitHub\u0027s *publicly visible* contribution
calendar (including anonymized private counts ONLY if the user opts in).
No private repository contents or personal access token are needed.
"""
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
import json
import math
import os
from xml.sax.saxutils import escape

USER = os.getenv("PROFILE_USERNAME", "YinL-k")
TOKEN = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
OUT.mkdir(parents=True, exist_ok=True)
TODAY = datetime.now(timezone.utc).date()
START = TODAY - timedelta(days=364)
HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "public-github-profile-graphics",
    "X-GitHub-Api-Version": "2022-11-28",
}
if TOKEN:
    HEADERS["Authorization"] = "Bearer " + TOKEN


def api(path):
    request = Request("https://api.github.com" + path, headers=HEADERS)
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def pages(path, cap=20):
    items = []
    for page in range(1, cap + 1):
        separator = "&" if "?" in path else "?"
        batch = api(path + separator + "per_page=100&page=" + str(page))
        if not isinstance(batch, list):
            raise ValueError("Unexpected GitHub API response")
        items.extend(batch)
        if len(batch) < 100:
            break
    return items


def txt(value):
    return escape(str(value), {'"': '&quot;'})


def svg_start(width, height, label):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{txt(label)}">'
        '<rect width="100%" height="100%" rx="14" fill="#0d1117"/>'
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" '
        'rx="13" fill="none" stroke="#30363d"/>'
        '<style>text{font-family:Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,Arial,sans-serif;}</style>'
    )


def text_at(x, y, value, size=14, color="#c9d1d9", weight=400, extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" {extra}>{txt(value)}</text>'


def write(name, fragments):
    (OUT / name).write_text("".join(fragments) + "</svg>\n", encoding="utf-8")
    print(f"Generated assets/{name}")


def stats_svg(public_repos, originals, stars, contributions):
    a = [svg_start(530, 210, "GitHub profile statistics and publicly visible contributions")]
    a.append(text_at(26, 37, "GITHUB PROFILE SNAPSHOT", 13, "#8b949e", 700))
    data = [
        (len(public_repos), "Public repositories"),
        (len(originals), "Non-fork projects"),
        (stars, "Stars received"),
        (contributions, "Visible contributions · 12 mo"),
    ]
    for i, (number, label) in enumerate(data):
        x = 26 if i % 2 == 0 else 284
        y = 92 if i < 2 else 163
        a.append(text_at(x, y, f"{number:,}", 30, "#f0f6fc", 750))
        a.append(text_at(x, y + 22, label, 12, "#8b949e"))
    a.append('<line x1="265" y1="54" x2="265" y2="191" stroke="#21262d"/>')
    a.append('<line x1="26" y1="121" x2="506" y2="121" stroke="#21262d"/>')
    return write("github-stats.svg", a)


def languages_svg(language_bytes):
    a = [svg_start(530, 210, "Most common languages in public, non-fork repositories")]
    a.append(text_at(26, 35, "TOP PUBLIC-REPO LANGUAGES", 13, "#8b949e", 700))
    total = sum(language_bytes.values())
    top = language_bytes.most_common(5)
    palette = ["#58a6ff", "#a371f7", "#3fb950", "#f2cc60", "#ff7b72"]
    for i, (language, byte_count) in enumerate(top):
        y = 64 + i * 29
        share = 100 * byte_count / total if total else 0
        a.append(text_at(26, y, language, 13, "#c9d1d9", 500))
        a.append(f'<rect x="178" y="{y-11}" width="255" height="10" rx="5" fill="#21262d"/>')
        a.append(f'<rect x="178" y="{y-11}" width="{255 * byte_count / total if total else 0:.1f}" height="10" rx="5" fill="{palette[i]}"/>')
        a.append(text_at(447, y, f"{share:.1f}%", 12, "#8b949e"))
    if not top:
        a.append(text_at(26, 104, "No language data available.", 14))
    a.append(text_at(26, 202, "Based on GitHub language bytes; not a measure of proficiency.", 10, "#8b949e"))
    return write("top-languages.svg", a)


def main():
    account = quote(USER, safe="")
    repos = pages(f"/users/{account}/repos?type=owner")
    public = [r for r in repos if not r.get("private") and r.get("owner", {}).get("login", "").lower() == USER.lower()]
    originals = [r for r in public if not r.get("fork")]
    languages = Counter()
    for repo in originals:
        url_name = "/".join(quote(part, safe="") for part in repo["full_name"].split("/"))
        languages.update(api(f"/repos/{url_name}/languages"))

    # The public calendar is generated first by public_contributions.py.
    # Never mislabel public commit counts as complete contributions.
    summary = json.loads((OUT / "contribution-summary.json").read_text(encoding="utf-8"))
    total = int(summary["contributions"])
    stars = sum(repo.get("stargazers_count", 0) for repo in public)
    stats_svg(public, originals, stars, total)
    languages_svg(languages)


if __name__ == "__main__":
    main()
