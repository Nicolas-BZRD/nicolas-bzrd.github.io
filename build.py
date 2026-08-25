#!/usr/bin/env python3
"""Builds the whole site from the JSON files in data/.

Edit only these:
    data/site.json      identity, bio, profile links, filters
    data/timeline.json  publications and news, in display order
    data/icons.json     inline SVG icon set (touch only to add an icon)

Everything else is generated and must never be hand-edited:
    index.html          pre-rendered page + JSON-LD (readable with JS disabled)
    404.html            not-found page
    llms.txt            llmstxt.org overview for LLM crawlers
    publications.md     plain-text mirror for dataset scrapers
    sitemap.xml         crawlable URLs

Run ./build.sh, which also rebuilds tailwind.css.
"""

import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data"

site = json.loads((DATA / "site.json").read_text())
items = json.loads((DATA / "timeline.json").read_text())
icons = json.loads((DATA / "icons.json").read_text())

SITE = site["url"].rstrip("/")
TAG_LABELS = site["tagLabels"]
ICON_CLS = "w-4 h-4 shrink-0"


def e(text):
    """HTML-escape a value coming from the JSON data."""
    return html.escape(str(text), quote=True)


def tags(item):
    return item.get("type", "").split()


def is_news(item):
    return "news" in tags(item)


def abs_url(path):
    return f"{SITE}/{str(path).lstrip('/')}"


def icon(name, classes="", label=None):
    """Inline <svg> from data/icons.json. Decorative unless `label` is given."""
    if name not in icons:
        raise SystemExit(f"unknown icon {name!r}; add it to data/icons.json")
    ic = icons[name]
    a11y = (
        f'role="img" aria-label="{e(label)}"'
        if label
        else 'aria-hidden="true" focusable="false"'
    )
    return (
        f'<svg class="{classes}" viewBox="{ic["viewBox"]}" fill="currentColor" '
        f'xmlns="http://www.w3.org/2000/svg" {a11y}><path d="{ic["path"]}"/></svg>'
    )


def authors_list(item):
    """'N Boizard, T Deschamps-Berger, ...' -> ['N Boizard', 'T Deschamps-Berger']"""
    names = [a.strip() for a in item.get("authors", "").split(",")]
    return [a for a in names if a and a not in {"...", "et al.", "et al"}]


def keywords(item):
    return [TAG_LABELS[t] for t in tags(item) if t in TAG_LABELS]


def first_url(item):
    links = item.get("links", [])
    return links[0]["url"] if links else ""


papers = [i for i in items if not is_news(i)]
news = [i for i in items if is_news(i)]

# --- <head> -------------------------------------------------------------------


def render_head():
    title = f'{site["name"]} — {site["titleShort"]}'
    desc = site["metaDescription"]
    portrait = abs_url(site["portrait"]["src"])
    meta = [
        ("property", "og:title", title),
        ("property", "og:description", desc),
        ("property", "og:type", "profile"),
        ("property", "og:url", f"{SITE}/"),
        ("property", "og:site_name", site["name"]),
        ("property", "og:locale", "en_US"),
        ("property", "og:image", portrait),
        ("property", "og:image:width", site["portrait"]["width"]),
        ("property", "og:image:height", site["portrait"]["height"]),
        ("property", "og:image:alt", site["portrait"]["alt"]),
        ("property", "profile:first_name", site["givenName"]),
        ("property", "profile:last_name", site["familyName"]),
        ("name", "twitter:card", "summary"),
        ("name", "twitter:site", site["twitterHandle"]),
        ("name", "twitter:creator", site["twitterHandle"]),
        ("name", "twitter:title", title),
        ("name", "twitter:description", desc),
        ("name", "twitter:image", portrait),
        ("name", "twitter:image:alt", site["portrait"]["alt"]),
    ]
    social = "\n".join(f'    <meta {a}="{k}" content="{e(v)}">' for a, k, v in meta)
    return f"""<meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{e(title)}</title>
    <meta name="description" content="{e(desc)}">
    <meta name="author" content="{e(site['name'])}">
    <meta name="theme-color" content="#f9fafb">
    <link rel="canonical" href="{SITE}/">
    <link rel="icon" type="image/png" href="img/favicon.png">
    <link rel="alternate" type="application/json" href="/data/timeline.json" title="Publications and timeline (JSON)">
    <link rel="alternate" type="text/markdown" href="/publications.md" title="Publications and timeline (Markdown)">
{social}
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="tailwind.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
    <link rel="stylesheet" href="style.css">"""


# --- about section ------------------------------------------------------------


def render_about():
    bio = "<br><br>\n                    ".join(site["bioHtml"])
    stats = []
    for i, s in enumerate(site["stats"]):
        if i:
            stats.append('<span class="text-gray-300" aria-hidden="true">·</span>')
        if s.get("valueAfter"):
            stats.append(
                f'<span>{e(s["label"])} <b class="text-gray-900">{e(s["value"])}</b></span>'
            )
        else:
            stats.append(
                f'<span><b class="text-gray-900 text-lg">{e(s["value"])}</b> {e(s["label"])}</span>'
            )
    links = "\n                    ".join(
        f'<a href="{e(p["url"])}" class="text-gray-600 hover:text-blue-600 transition-colors '
        f'inline-flex items-center gap-1.5" target="_blank" rel="noopener noreferrer" '
        f'title="{e(site["name"])} on {e(p["name"])}">'
        f'{icon(p["icon"], ICON_CLS)}{e(p["name"])}</a>'
        for p in site["profiles"]
    )
    pt = site["portrait"]
    return f"""        <section id="about" class="flex flex-col md:flex-row items-center mb-20">
            <div class="md:w-1/5 text-center md:text-left mb-8 md:mb-0">
                <img class="w-60 h-60 rounded-full mx-auto md:mx-0 shadow-lg" src="{e(pt['src'])}"
                     width="{e(pt['width'])}" height="{e(pt['height'])}" alt="{e(pt['alt'])}">
            </div>
            <div class="md:w-4/5 md:pl-12">
                <h1 class="text-4xl font-bold text-gray-900 mb-4">{e(site['heading'])}</h1>
                <p class="text-lg text-gray-700 mb-6">
                    {bio}
                </p>
                <div class="flex flex-wrap items-center gap-x-3 gap-y-2 text-sm text-gray-600 mb-6">
                    {"".join(stats)}
                </div>
                <div class="flex flex-wrap justify-center md:justify-start gap-3">
                    {links}
                </div>
            </div>
        </section>"""


# --- timeline ----------------------------------------------------------------


def render_news_item(item):
    link = ""
    if item.get("link"):
        link = (
            f'<a href="{e(item["link"])}" target="_blank" rel="noopener noreferrer" '
            f'class="ml-2 text-gray-500 hover:text-blue-600" '
            f'title="Source: {e(item["title"])}">'
            f'{icon("external", "w-3 h-3 inline", label="Open source link")}</a>'
        )
    return f"""            <div class="timeline-entry mb-8 relative" data-tags="news">
                <div class="timeline-dot absolute left-0 top-2 w-2.5 h-2.5 bg-gray-300 rounded-full border-2 border-white"></div>
                <div class="ml-10">
                    <p class="text-xs text-gray-400 mb-1 font-medium"><time datetime="{e(item['date'])}">{e(item['date'])}</time></p>
                    <div class="inline-flex items-center text-gray-500 text-sm italic">
                        {icon(item.get('icon', 'star'), 'w-3.5 h-3.5 text-gray-400 mr-2')}
                        <span>{e(item['title'])}</span>{link}
                    </div>
                </div>
            </div>
"""


def render_paper(item):
    links = "\n                            ".join(
        f'<a href="{e(l["url"])}" target="_blank" rel="noopener noreferrer" '
        f'class="inline-flex items-center gap-2 bg-gray-100 hover:bg-blue-100 text-gray-800 '
        f'hover:text-blue-700 text-sm font-medium py-2 px-4 rounded-lg transition-colors">'
        f'{icon(l["icon"], ICON_CLS)}{e(l["type"])}</a>'
        for l in item.get("links", [])
    )
    conference = (
        f'\n                                <p class="text-blue-600 font-semibold mb-2">{e(item["conference"])}</p>'
        if item.get("conference")
        else ""
    )
    authors = (
        f'\n                                <p class="text-sm text-gray-600 mb-4">{e(item["authors"])}</p>'
        if item.get("authors")
        else ""
    )
    logo = ""
    if item.get("logoUrl"):
        alt = e(item.get("conference") or item["title"])
        logo = f"""
                            <div class="w-24 h-24 mb-4 md:mb-0 md:mr-6 flex-shrink-0">
                                <img src="{e(item['logoUrl'])}" alt="{alt} illustration" width="96" height="96"
                                     loading="lazy" decoding="async" class="w-full h-full object-cover rounded-lg shadow-md">
                            </div>"""
    return f"""            <article class="timeline-entry mb-12 relative" data-tags="{e(item.get('type', ''))}">
                <div class="timeline-dot absolute left-0 top-1.5 w-4 h-4 bg-blue-500 rounded-full border-4 border-white"></div>
                <div class="ml-10">
                    <p class="text-sm text-gray-500 mb-2 font-medium"><time datetime="{e(item['date'])}">{e(item['date'])}</time></p>
                    <div class="timeline-card bg-white p-6 rounded-lg shadow-lg border border-gray-200">
                        <div class="flex flex-col md:flex-row items-start mb-4">{logo}
                            <div class="flex-grow">
                                <h3 class="text-xl font-bold text-gray-900 mb-2">{e(item['title'])}</h3>{authors}{conference}
                            </div>
                        </div>
                        <p class="text-gray-700 mb-6">{e(item.get('description', ''))}</p>
                        <div class="flex flex-wrap gap-3 mt-4">
                            {links}
                        </div>
                    </div>
                </div>
            </article>
"""


def render_timeline():
    buttons = "\n                    ".join(
        f'<button class="filter-btn {"bg-blue-600 text-white" if f["id"] == "all" else "bg-gray-200 text-gray-700"} '
        f'hover:bg-blue-100 hover:text-blue-700 transition-colors px-4 py-2 rounded-full text-sm '
        f'font-semibold cursor-pointer" data-filter="{e(f["id"])}" '
        f'aria-pressed="{"true" if f["id"] == "all" else "false"}">{e(f["label"])}</button>'
        for f in site["filters"]
    )
    entries = "".join(
        render_news_item(i) if is_news(i) else render_paper(i) for i in items
    )
    return f"""        <section id="timeline">
            <h2 class="text-3xl font-bold mb-10 text-center text-gray-900">My Research Journey &amp; Publications</h2>
            <div class="top-0 bg-gray-50 z-10 py-4">
                <div class="flex flex-wrap justify-center gap-2" role="group" aria-label="Filter publications">
                    {buttons}
                </div>
            </div>
            <div id="timeline-container" class="relative border-l-2 border-gray-200 pl-6">
{entries}            </div>
            <p id="timeline-empty" class="hidden text-gray-500 text-center">No items to display for this category.</p>
        </section>"""


# --- JSON-LD -----------------------------------------------------------------


def render_jsonld():
    person = {
        "@type": "Person",
        "@id": f"{SITE}/#person",
        "name": site["name"],
        "givenName": site["givenName"],
        "familyName": site["familyName"],
        "image": abs_url(site["portrait"]["src"]),
        "jobTitle": site["jobTitle"],
        "description": site["bioPlain"],
        "url": f"{SITE}/",
        "mainEntityOfPage": {"@id": f"{SITE}/#webpage"},
        "affiliation": [
            {"@type": a["type"], "name": a["name"], "url": a["url"]}
            for a in site["affiliations"]
        ],
        "knowsAbout": site["knowsAbout"],
        "sameAs": [p["url"] for p in site["profiles"]],
    }
    articles = []
    for item in papers:
        node = {
            "@type": "ScholarlyArticle",
            "headline": item["title"],
            "name": item["title"],
            "author": [{"@type": "Person", "name": a} for a in authors_list(item)],
            "datePublished": item["date"],
            "abstract": item.get("description", ""),
            "image": abs_url(item["logoUrl"]) if item.get("logoUrl") else None,
            "keywords": keywords(item),
            "inLanguage": "en",
        }
        if item.get("conference"):
            node["isPartOf"] = {"@type": "CreativeWork", "name": item["conference"]}
        urls = [l["url"] for l in item.get("links", [])]
        if urls:
            node["url"] = urls[0]
            node["sameAs"] = urls
        articles.append({k: v for k, v in node.items() if v})

    graph = [
        {
            "@type": "ProfilePage",
            "@id": f"{SITE}/#webpage",
            "url": f"{SITE}/",
            "name": f'{site["name"]} — {site["tagline"]}',
            "description": site["metaDescription"],
            "inLanguage": "en",
            "mainEntity": {"@id": f"{SITE}/#person"},
        },
        person,
        *articles,
    ]
    body = json.dumps(
        {"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False
    )
    return f'    <script type="application/ld+json">\n{body}\n    </script>'


# --- page assembly -----------------------------------------------------------

GENERATED = "<!-- Generated by build.py from data/*.json — do not edit by hand. -->"

header = f"""    <header class="bg-white/80 backdrop-blur-sm shadow-sm sticky top-0 z-50">
        <div class="container mx-auto px-6 py-4 flex justify-between items-center">
            <a href="/" class="text-2xl font-bold text-gray-900">{e(site['name'])}</a>
            <nav class="hidden md:flex space-x-6" aria-label="Primary">
                <a href="/#about" class="text-gray-600 hover:text-blue-600 transition-colors">About {e(site['givenName'])}</a>
                <a href="/#timeline" class="text-gray-600 hover:text-blue-600 transition-colors">Research Timeline</a>
            </nav>
        </div>
    </header>"""

footer = f"""    <footer class="bg-white mt-16 py-6 border-t">
        <div class="container mx-auto px-6 text-gray-600">
            <p>&copy; {date.today().year} {e(site['name'])}, {e(site['footerNote'])}. All rights reserved.
               <span class="sr-only">Personal portfolio and research website.</span></p>
        </div>
    </footer>"""


def page(body, *, head_extra="", noindex=False):
    robots = '\n    <meta name="robots" content="noindex">' if noindex else ""
    return f"""<!DOCTYPE html>
<html lang="en">
{GENERATED}
<head>
    {render_head()}{robots}{head_extra}
</head>
<body class="bg-gray-50 text-gray-800">
{header}

{body}

{footer}
</body>
</html>
"""


(ROOT / "index.html").write_text(
    page(
        f"""    <main class="container mx-auto px-6 py-12">

{render_about()}

{render_timeline()}

    </main>

    <script src="timeline.js" defer></script>""",
        head_extra="\n" + render_jsonld(),
    )
)

(ROOT / "404.html").write_text(
    page(
        """    <main class="container mx-auto px-6 py-24 text-center">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">Page not found</h1>
        <p class="text-lg text-gray-700">That page does not exist. Try the
           <a href="/" class="text-blue-600 hover:underline">home page</a> or the
           <a href="/#timeline" class="text-blue-600 hover:underline">research timeline</a>.</p>
    </main>""",
        noindex=True,
    )
)

# --- llms.txt ----------------------------------------------------------------

lines = [
    f'# {site["name"]}',
    "",
    f'> {site["tagline"]}. {site["bioPlain"]}',
    "",
    "Machine-readable copies of everything on this site: "
    f"[timeline.json]({abs_url('data/timeline.json')}) (all entries, structured), "
    f"[publications.md]({abs_url('publications.md')}) (full abstracts, plain text). "
    "The home page also embeds schema.org JSON-LD (`ProfilePage`, `Person`, `ScholarlyArticle`).",
    "",
    "## Publications",
    "",
]
for p in papers:
    venue = f' — {p["conference"]}' if p.get("conference") else ""
    url = first_url(p)
    title = f'[{p["title"]}]({url})' if url else p["title"]
    lines.append(f'- {title}: {p["date"]}{venue}. {p.get("authors", "")}')

lines += ["", "## News and talks", ""]
for n in news:
    label = f'[{n["title"]}]({n["link"]})' if n.get("link") else n["title"]
    lines.append(f'- {n["date"]}: {label}')

lines += ["", "## Profiles", ""]
lines += [f'- [{p["name"]}]({p["url"]})' for p in site["profiles"]]
lines.append("")
(ROOT / "llms.txt").write_text("\n".join(lines))

# --- publications.md ---------------------------------------------------------

md = [
    f'# {site["name"]} — Publications and Research Timeline',
    "",
    f'{site["tagline"]}. Canonical page: {SITE}/',
    "",
    site["bioPlain"],
    "",
    "---",
    "",
]
for p in papers:
    md += [f'## {p["title"]}', "", f'- **Year:** {p["date"]}']
    if p.get("conference"):
        md.append(f'- **Venue:** {p["conference"]}')
    if p.get("authors"):
        md.append(f'- **Authors:** {p["authors"]}')
    if keywords(p):
        md.append(f'- **Topics:** {", ".join(keywords(p))}')
    md += [f'- **{l["type"]}:** {l["url"]}' for l in p.get("links", [])]
    md += ["", f'**Abstract.** {p.get("description", "")}', ""]

md += ["---", "", "## News and Talks", ""]
for n in news:
    suffix = f' ({n["link"]})' if n.get("link") else ""
    md.append(f'- **{n["date"]}** — {n["title"]}{suffix}')
md += ["", "## Profiles", ""]
md += [f'- {p["name"]}: {p["url"]}' for p in site["profiles"]]
md.append("")
(ROOT / "publications.md").write_text("\n".join(md))

# --- sitemap.xml -------------------------------------------------------------

# Only the canonical HTML page. llms.txt and publications.md are plain-text mirrors
# of it, and GitHub Pages cannot send a rel=canonical header for non-HTML files, so
# listing them here would just invite duplicate-content warnings. Crawlers still
# reach them: llms.txt by convention, publications.md via <link rel="alternate">.
today = date.today().isoformat()
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
      "  <url>", f"    <loc>{SITE}/</loc>", f"    <lastmod>{today}</lastmod>",
      "    <changefreq>monthly</changefreq>", "    <priority>1.0</priority>", "  </url>"]
sm += ["</urlset>", ""]
(ROOT / "sitemap.xml").write_text("\n".join(sm))

print(f"OK  {len(papers)} papers, {len(news)} news, {len(icons)} inline icons")
print("    index.html  404.html  llms.txt  publications.md  sitemap.xml")
