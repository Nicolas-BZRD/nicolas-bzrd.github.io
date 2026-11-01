#!/usr/bin/env python3
"""Builds the whole site from the JSON files in data/.

Edit only these:
    data/site.json      identity, bio, highlights, profile links, filters
    data/timeline.json  publications and news, in display order
    data/icons.json     inline SVG icon set (touch only to add an icon)
    data/stickers.json  pixel art for the hero assembly line (machine, logos, tokens)

Everything else is generated and must never be hand-edited:
    index.html          pre-rendered page + JSON-LD (readable with JS disabled)
    404.html            not-found page
    llms.txt            llmstxt.org overview for LLM crawlers
    publications.md     plain-text mirror for dataset scrapers
    sitemap.xml         crawlable URLs

Styling lives in style.css, behaviour (filters, abstracts, nav) in site.js.
Run ./build.sh.
"""

import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data"

site = json.loads((DATA / "site.json").read_text())
items = json.loads((DATA / "timeline.json").read_text())
icons = json.loads((DATA / "icons.json").read_text())
factory = json.loads((DATA / "stickers.json").read_text())

SITE = site["url"].rstrip("/")
TAG_LABELS = site["tagLabels"]
ME = f'{site["givenName"][0]} {site["familyName"]}'  # how the site owner appears in author lists
NAV = [("about", "About"), ("publications", "Publications"), ("press", "Press")]


def e(text):
    """HTML-escape a value coming from the JSON data."""
    return html.escape(str(text), quote=True)


def tags(item):
    return item.get("type", "").split()


def is_news(item):
    return "news" in tags(item)


def abs_url(path):
    return f"{SITE}/{str(path).lstrip('/')}"


def icon(name, classes="icon", label=None):
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


def slug(item):
    """Stable anchor from the title: 'EuroBERT: Scaling ...' -> 'eurobert'."""
    head = re.split(r"[:?]", item["title"])[0]
    words = re.sub(r"[^a-z0-9]+", " ", head.lower()).split()[:5]
    return "-".join(words)


papers = [i for i in items if not is_news(i)]
news = [i for i in items if is_news(i)]
press = [n for n in news if n.get("icon") == "newspaper"]  # the only news shown on the page
paper_ids = {slug(p) for p in papers}

EXTERNAL = 'target="_blank" rel="noopener noreferrer"'
ARROW = '<span class="arrow" aria-hidden="true">↗</span>'

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
    <meta name="color-scheme" content="light dark">
    <meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
    <meta name="theme-color" content="#0b0b0c" media="(prefers-color-scheme: dark)">
    <link rel="canonical" href="{SITE}/">
    <link rel="icon" type="image/png" href="img/favicon.png">
    <link rel="alternate" type="application/json" href="/data/timeline.json" title="Publications and timeline (JSON)">
    <link rel="alternate" type="text/markdown" href="/publications.md" title="Publications and timeline (Markdown)">
{social}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400..700&family=JetBrains+Mono:wght@400;500&display=swap">
    <link rel="stylesheet" href="style.css">
    <script>document.documentElement.classList.add('js')</script>"""


# --- sidebar / top bar ----------------------------------------------------------


def render_sidebar(home=""):
    links = "\n".join(
        f'                <a href="{home}#{sid}" data-nav="{sid}">'
        f'<span class="nav-num">{n:02d}</span>{label}</a>'
        for n, (sid, label) in enumerate(NAV, 1)
    )
    ph = site["sidebarPhoto"]
    return f"""    <aside class="sidebar">
        <div class="sidebar-inner">
            <figure class="sidebar-photo">
                <img src="{e(ph['src'])}" width="{e(ph['width'])}" height="{e(ph['height'])}" alt="{e(site['portrait']['alt'])}">
                <figcaption>{e(ph['caption'])}</figcaption>
            </figure>
            <a class="brand" href="/">
                <img class="brand-avatar" src="{e(site['avatar'])}" width="32" height="32" alt="">
                <span class="brand-text">
                    <span class="brand-name">{e(site['name'])}</span>
                    <span class="brand-role">{e(site['titleShort'])}</span>
                </span>
            </a>
            <nav class="nav" aria-label="Primary">
{links}
            </nav>
        </div>
    </aside>"""


# --- about ----------------------------------------------------------------------


def render_highlights():
    rows = []
    for h in site.get("highlights", []):
        links = []
        for label, target in h["items"]:
            if target not in paper_ids:
                raise SystemExit(f"highlight {label!r} points to unknown paper #{target}")
            links.append(f'<a href="#{e(target)}">{e(label)}</a>')
        rows.append(
            f"""                <div class="work-row">
                    <dt>{e(h['area'])}</dt>
                    <dd><span class="work-items">{', '.join(links)}</span> <span class="work-note">{e(h['note'])}</span></dd>
                </div>"""
        )
    if not rows:
        return ""
    return f"""
            <div class="work">
                <p class="eyebrow">What I build</p>
                <dl class="work-list">
{chr(10).join(rows)}
                </dl>
            </div>"""


def pixel_svg(rows, palette):
    """Pixel-art grid -> <svg>, merging horizontal runs of one colour into a single rect."""
    rects = []
    for y, row in enumerate(rows):
        x = 0
        while x < len(row):
            c = row[x]
            run = 1
            while x + run < len(row) and row[x + run] == c:
                run += 1
            if c != ".":
                rects.append(f'<rect x="{x}" y="{y}" width="{run}" height="1" fill="{palette[c]}"/>')
            x += run
    w, h = len(rows[0]), len(rows)
    return (
        f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" shape-rendering="crispEdges" '
        f'aria-hidden="true" focusable="false">{"".join(rects)}</svg>'
    )


def render_factory():
    """Assembly-line strip: a pixel machine eats tokens and outputs project logos onto a belt.

    The logos are rendered here as a static row (what crawlers and no-JS/reduced-motion
    visitors see); site.js uses them as templates for the animation.
    """
    items = []
    for st in factory["stickers"]:
        rows = st["pixels"]
        if any(len(r) != len(rows[0]) for r in rows):
            raise SystemExit(f"sticker {st['label']!r} has rows of different lengths")
        target = st.get("target")
        if target and target not in paper_ids | {"about"}:
            raise SystemExit(f"sticker {st['label']!r} points to unknown anchor #{target}")
        style = f"--w:{len(rows[0])};--h:{len(rows)}"
        svg = pixel_svg(rows, factory["palette"])
        label = e(st["label"])
        if target:
            items.append(
                f'                    <a class="sticker" href="#{e(target)}" style="{style}" '
                f'data-label="{label}" aria-label="{label}">{svg}</a>'
            )
        else:
            items.append(
                f'                    <span class="sticker" style="{style}" data-label="{label}" '
                f'role="img" aria-label="{label}">{svg}</span>'
            )
    machine = factory["machine"]
    tokens = e(json.dumps(factory["tokens"], ensure_ascii=False))
    return f"""            <div class="factory" data-tokens="{tokens}">
                <p class="factory-label"><span>NB-1</span> pretraining line</p>
                <p class="factory-meter" aria-hidden="true">
                    <span>params <b data-params>1.0B</b> ↑</span>
                    <span>loss <b data-loss>3.20</b> ↓</span>
                    <svg class="factory-spark" viewBox="0 0 60 20" preserveAspectRatio="none"><polyline points="" /></svg>
                </p>
                <div class="factory-machine" style="--w:{len(machine[0])};--h:{len(machine)}" aria-hidden="true">
                    {pixel_svg(machine, factory["palette"])}
                    <span class="factory-lamp"></span>
                </div>
                <div class="factory-belt" aria-hidden="true"></div>
                <div class="factory-items" role="group" aria-label="Project logos">
{chr(10).join(items)}
                </div>
            </div>"""


def render_about():
    bio = "\n".join(f"                <p>{p}</p>" for p in site["bioHtml"])
    stats = "\n".join(
        f'                <div class="stat">'
        f'<dt>{e(s["label"])}</dt><dd>{e(s["value"])}</dd></div>'
        for s in site["stats"]
    )
    links = "\n".join(
        f'                <a class="btn" href="{e(p["url"])}" {EXTERNAL} '
        f'title="{e(site["name"])} on {e(p["name"])}">'
        f'{icon(p["icon"])}{e(p.get("shortName", p["name"]))}</a>'
        for p in site["profiles"]
    )
    tagline = '<span class="sr-only"> | </span>'.join(
        f'<span class="hero-tagline">{e(part)}</span>' for part in site["tagline"].split(" | ")
    )
    return f"""        <section id="about" class="section hero" aria-labelledby="about-title">
            <h1 id="about-title">{e(site['name'])}<span class="sr-only"> — </span>{tagline}</h1>
{render_factory()}
            <div class="bio">
{bio}
            </div>
            <div class="profiles">
{links}
            </div>
            <dl class="stats">
{stats}
            </dl>{render_highlights()}
        </section>"""


# --- press ----------------------------------------------------------------------


def render_press_item(item):
    outlet, _, headline = item["title"].partition(" — ")
    if not headline:
        outlet, headline = "", outlet
    tag, attrs = ("a", f' href="{e(item["link"])}" {EXTERNAL}') if item.get("link") else ("div", "")
    return f"""                <li>
                    <{tag} class="press-card"{attrs}>
                        <span class="press-top"><span class="press-outlet">{e(outlet)}</span><time datetime="{e(item['date'])}">{e(item['date'])}</time></span>
                        <span class="press-headline">{e(headline)}</span>
                        {ARROW if item.get("link") else ""}
                    </{tag}>
                </li>"""


def render_press():
    if not press:
        return ""
    return f"""        <section id="press" class="section" aria-labelledby="press-title">
            <header class="section-head">
                <h2 id="press-title">Press</h2>
            </header>
            <ul class="press-list">
{chr(10).join(render_press_item(p) for p in press)}
            </ul>
        </section>"""


# --- publications -------------------------------------------------------------------


def highlight_me(authors):
    return e(authors).replace(e(ME), f"<b>{e(ME)}</b>")


def render_paper(item):
    pid = slug(item)
    links = "\n".join(
        f'                            <a class="chip" href="{e(l["url"])}" {EXTERNAL}>'
        f'{icon(l["icon"])}{e(l["type"])}</a>'
        for l in item.get("links", [])
    )
    abstract = ""
    toggle = ""
    if item.get("description"):
        toggle = (
            f'\n                            <button class="chip chip-ghost abstract-toggle" type="button" '
            f'aria-expanded="false" aria-controls="{pid}-abstract">Abstract'
            f'<span class="chev" aria-hidden="true"></span></button>'
        )
        abstract = f'\n                        <p class="pub-abstract" id="{pid}-abstract">{e(item["description"])}</p>'
    meta = []
    if item.get("conference"):
        meta.append(f'<span class="pub-venue">{e(item["conference"])}</span>')
    if "main_author" in tags(item):
        meta.append(f'<span class="pub-badge">{e(TAG_LABELS["main_author"])}</span>')
    authors = (
        f'\n                        <p class="pub-authors">{highlight_me(item["authors"])}</p>'
        if item.get("authors")
        else ""
    )
    title = e(item["title"])
    if first_url(item):
        title = f'<a href="{e(first_url(item))}" {EXTERNAL}>{title}</a>'
    thumb = ""
    if item.get("logoUrl"):
        thumb = (
            f'\n                    <img class="pub-thumb" src="{e(item["logoUrl"])}" alt="" '
            f'width="96" height="96" loading="lazy" decoding="async">'
        )
    return f"""                <article class="pub" id="{pid}" data-tags="{e(item.get('type', ''))}">{thumb}
                    <div class="pub-body">
                        <p class="pub-meta">{"".join(meta)}</p>
                        <h3 class="pub-title">{title}</h3>{authors}
                        <div class="pub-links">
{links}{toggle}
                        </div>{abstract}
                    </div>
                </article>"""


def render_publications():
    def count(fid):
        return len(papers) if fid == "all" else sum(fid in tags(p) for p in papers)

    buttons = "\n".join(
        f'                <button class="filter" type="button" data-filter="{e(f["id"])}" '
        f'aria-pressed="{"true" if f["id"] == "all" else "false"}">'
        f'{e(f["label"])}<span class="filter-count">{count(f["id"])}</span></button>'
        for f in site["filters"]
    )
    years = []
    for year in dict.fromkeys(p["date"] for p in papers):
        entries = "\n".join(render_paper(p) for p in papers if p["date"] == year)
        years.append(
            f"""            <div class="pub-year">
                <p class="pub-year-label">{e(year)}</p>
                <div class="pub-list">
{entries}
                </div>
            </div>"""
        )
    scholar = next((p for p in site["profiles"] if p["icon"] == "scholar"), None)
    scholar_link = (
        f'\n                <a class="section-link" href="{e(scholar["url"])}" {EXTERNAL}>Google Scholar{ARROW}</a>'
        if scholar
        else ""
    )
    return f"""        <section id="publications" class="section" aria-labelledby="publications-title">
            <header class="section-head">
                <h2 id="publications-title">Publications</h2>{scholar_link}
            </header>
            <div class="filters" role="group" aria-label="Filter publications">
{buttons}
            </div>
{chr(10).join(years)}
            <p class="pub-empty" hidden>No publications in this category.</p>
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

footer = f"""        <footer class="footer">
            <p>&copy; {date.today().year} {e(site['name'])} · {e(site['footerNote'])}</p>
            <p class="footer-links"><a href="/llms.txt">llms.txt</a><a href="/publications.md">publications.md</a></p>
        </footer>"""


def page(body, *, home="", head_extra="", noindex=False, scripts=""):
    robots = '\n    <meta name="robots" content="noindex">' if noindex else ""
    return f"""<!DOCTYPE html>
<html lang="en">
{GENERATED}
<head>
    {render_head()}{robots}{head_extra}
</head>
<body>
    <a class="skip" href="#main">Skip to content</a>
    <div class="shell">
{render_sidebar(home)}
    <main id="main" class="main">
{body}

{footer}
    </main>
    </div>{scripts}
</body>
</html>
"""


(ROOT / "index.html").write_text(
    page(
        f"""{render_about()}

{render_publications()}

{render_press()}""",
        head_extra="\n" + render_jsonld(),
        scripts='\n    <script src="site.js" defer></script>',
    )
)

(ROOT / "404.html").write_text(
    page(
        """        <section class="section hero">
            <p class="eyebrow">Error 404</p>
            <h1>Page not found<span class="hero-tagline">That page does not exist.</span></h1>
            <div class="bio">
                <p>Try the <a href="/">home page</a> or the <a href="/#publications">publication list</a>.</p>
            </div>
        </section>""",
        home="/",
        noindex=True,
    )
)

# --- llms.txt ----------------------------------------------------------------

lines = [
    f'# {site["name"]}',
    "",
    f'> {site["bioPlain"]}',
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
