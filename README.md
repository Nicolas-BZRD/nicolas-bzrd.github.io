# nicolas-bzrd.github.io

Static personal research site. Everything is generated from JSON by [`build.py`](build.py),
so the page is fully readable without JavaScript — which is what lets Google, LLM crawlers
(GPTBot, ClaudeBot, PerplexityBot) and dataset scrapers (CCBot / Common Crawl) actually
index the publication list.

## Making a change

```
edit data/*.json  ->  ./build.sh  ->  git commit
```

| Edit this | To change |
| --- | --- |
| `data/timeline.json` | publications and news, in display order |
| `data/site.json` | name, bio, stats, "What I build" rows, profile links, filter buttons |
| `data/icons.json` | the inline SVG icon set (only to add a new icon) |
| `data/stickers.json` | pixel art for the hero assembly line (machine, tokens, logos) |
| `style.css` | styling (plain CSS, light + dark via `prefers-color-scheme`) |
| `site.js` | filters, abstract toggles, active nav link |

**Never hand-edit these — `./build.sh` overwrites them:**
`index.html`, `404.html`, `llms.txt`, `publications.md`, `sitemap.xml`

## Adding a publication

Prepend to `data/timeline.json`:

```json
{
  "date": "2026",
  "title": "Paper title",
  "authors": "N Boizard, ...",
  "type": "paper main_author efficient_training",
  "description": "Abstract. Used verbatim as schema.org `abstract` and in publications.md.",
  "conference": "NeurIPS 2026",
  "logoUrl": "img/paper.webp",
  "links": [{ "type": "arXiv", "url": "https://arxiv.org/abs/...", "icon": "pdf" }]
}
```

`type` is space-separated: `paper` plus any of `main_author`, `large_scale_training`,
`efficient_training` (these drive the filter buttons and the JSON-LD `keywords`).
News items use `"type": "news"` with a `title`, `icon`, and optional `link`. Only press items
(`"icon": "newspaper"`, title written `Outlet — headline`) appear on the page, as cards in the
Press section; the other news (milestones, talks) stays in `llms.txt` and `publications.md`.

Paper anchors are derived from the title (`EuroBERT: ...` → `#eurobert`); the `highlights`
rows in `site.json` link to them, and the build fails if one points to a missing paper.

Valid `icon` values are the keys of `data/icons.json`: `star`, `microphone`, `newspaper`,
`robot`, `pdf`, `scholar`, `external`, `github`, `linkedin`, `x`. An unknown name fails the
build rather than rendering a blank box.

## Images

Thumbnails render at up to 80x80 CSS px, so ship them at **192x192 WebP** (~6 KB), not full size:

```
cwebp -q 82 -resize 192 192 source.png -o img/name.webp
```

`img/nicolas_boizard.jpg` stays JPEG on purpose — it is the `og:image`, and some social
crawlers do not handle WebP. `img/portrait.webp` (sidebar, 480x660) and `img/avatar.webp`
(mobile top bar, 192x192) are crops of the same photo.

## Hero assembly line

`data/stickers.json` holds the pixel art for the strip at the top of the page: the
`machine`, the `tokens` it swallows, and the `stickers` (logos) it pushes onto the belt.
Each grid is one string per row, one character per pixel, `.` for transparent and any
other character a key of `palette`. `target` is the anchor a logo links to (a paper id,
or `about`). Logos come out in shuffled rounds, each once per round. Without JS or
with reduced motion, the logos just sit in a row on the belt.

## What makes it crawlable

- Everything is pre-rendered into `index.html`; `site.js` only toggles `hidden` on
  existing nodes, and abstracts are only folded once JS has run, so filtering and
  toggles work without hiding content from crawlers or no-JS readers.
- schema.org JSON-LD in `index.html`: `ProfilePage` + `Person` + one `ScholarlyArticle`
  per paper, with `author` as real `Person` nodes.
- `llms.txt` ([llmstxt.org](https://llmstxt.org)) and `publications.md` mirror the data as
  plain text; `<link rel="alternate">` points crawlers at them.
- `.nojekyll` stops GitHub Pages from rewriting `publications.md` into HTML.
