"""Fetch publications from ORCID (+ details from Crossref) into data/publications_auto.json.

Run by .github/workflows/update-publications.yml every week.
You don't need to run this yourself.
"""

import html
import json
import re
import sys
import urllib.request
from pathlib import Path

ORCID_ID = "0000-0003-3356-2512"
# Your name as it appears in author lists, so it can be shown in bold.
MY_FAMILY_NAME = "Huang"
MY_GIVEN_INITIAL = "Y"

OUTPUT = Path(__file__).resolve().parent.parent / "data" / "publications_auto.json"

# ORCID work types to include (others, like talks, are skipped). The label is kept as "type".
TYPES = {
    "journal-article": "journal",
    "conference-paper": "conference",
    "book-chapter": "book",
    "book": "book",
}

HEADERS = {"User-Agent": "yuxihuang.com publications updater"}


def get_json(url, headers=None):
    req = urllib.request.Request(url, headers={**HEADERS, **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def clean(text):
    """Strip HTML tags (Crossref titles sometimes contain <i> etc.) and extra spaces."""
    text = re.sub(r"<[^>]+>", "", html.unescape(text or ""))
    return re.sub(r"\s+", " ", text).strip()


def initials(given):
    parts = re.split(r"[\s\-]+", given.strip())
    return " ".join(p[0].upper() + "." for p in parts if p)


def format_authors(authors):
    names = []
    for a in authors:
        family, given = clean(a.get("family", "")), clean(a.get("given", ""))
        if not family:
            names.append(clean(a.get("name", "")))
            continue
        name = f"{family}, {initials(given)}" if given else family
        if family == MY_FAMILY_NAME and given[:1].upper() == MY_GIVEN_INITIAL:
            name = f"**{name}**"
        names.append(name)
    names = [n for n in names if n]
    if len(names) <= 1:
        return "".join(names)
    return ", ".join(names[:-1]) + ", & " + names[-1]


def find_doi(summary):
    for ext in (summary.get("external-ids") or {}).get("external-id", []):
        if ext.get("external-id-type") == "doi":
            doi = ext.get("external-id-value", "").strip()
            return re.sub(r"^https?://(dx\.)?doi\.org/", "", doi, flags=re.I).lower()
    return ""


def from_crossref(doi):
    msg = get_json(f"https://api.crossref.org/works/{urllib.request.quote(doi)}")["message"]
    year = None
    for key in ("published-print", "published-online", "issued", "published"):
        parts = (msg.get(key) or {}).get("date-parts") or [[None]]
        if parts[0][0]:
            year = parts[0][0]
            break
    return {
        "authors": format_authors(msg.get("author", [])),
        "year": year,
        "title": clean((msg.get("title") or [""])[0]),
        "venue": clean((msg.get("container-title") or [""])[0]),
        "volume": msg.get("volume", ""),
        "issue": msg.get("issue", ""),
        "pages": msg.get("page", "").replace("-", "–"),
    }


def main():
    works = get_json(
        f"https://pub.orcid.org/v3.0/{ORCID_ID}/works",
        {"Accept": "application/json"},
    )
    pubs = []
    for group in works.get("group", []):
        summary = group["work-summary"][0]
        section = TYPES.get(summary.get("type"))
        if not section:
            continue
        doi = find_doi(summary)
        pub = {
            "authors": "",
            "year": int(((summary.get("publication-date") or {}).get("year") or {}).get("value") or 0) or None,
            "title": clean(((summary.get("title") or {}).get("title") or {}).get("value")),
            "venue": clean((summary.get("journal-title") or {}).get("value")),
            "volume": "",
            "issue": "",
            "pages": "",
        }
        if doi:
            try:
                details = from_crossref(doi)
                pub.update({k: v for k, v in details.items() if v})
            except Exception as e:  # keep the ORCID data if Crossref fails
                print(f"Crossref lookup failed for {doi}: {e}", file=sys.stderr)
        pub["doi"] = doi
        pub["type"] = section
        if pub["title"]:
            pubs.append(pub)

    pubs.sort(key=lambda p: (-(p["year"] or 0), p["title"].lower()))
    OUTPUT.write_text(json.dumps(pubs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(pubs)} publications to {OUTPUT}")


if __name__ == "__main__":
    main()
