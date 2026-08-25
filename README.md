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
| `data/site.json` | name, bio, stats, profile links, filter buttons |
| `data/icons.json` | the inline SVG icon set (only to add a new icon) |
| `tailwind.input.css`, `style.css` | styling |

**Never hand-edit these — `./build.sh` overwrites them:**
`index.html`, `404.html`, `llms.txt`, `publications.md`, `sitemap.xml`, `tailwind.css`

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
News items use `"type": "news"` with a `title`, `icon`, and optional `link`.

Valid `icon` values are the keys of `data/icons.json`: `star`, `microphone`, `newspaper`,
`robot`, `pdf`, `scholar`, `external`, `github`, `linkedin`, `x`. An unknown name fails the
build rather than rendering a blank box.

## Images

Thumbnails render at 96x96 CSS px, so ship them at **192x192 WebP** (~6 KB), not full size:

```
cwebp -q 82 -resize 192 192 source.png -o img/name.webp
```

`img/nicolas_boizard.png` stays PNG on purpose — it is the `og:image`, and some social
crawlers do not handle WebP.

## What makes it crawlable

- The timeline is pre-rendered into `index.html`; `timeline.js` only toggles `hidden` on
  existing nodes, so filtering works without hiding content from crawlers.
- schema.org JSON-LD in `index.html`: `ProfilePage` + `Person` + one `ScholarlyArticle`
  per paper, with `author` as real `Person` nodes.
- `llms.txt` ([llmstxt.org](https://llmstxt.org)) and `publications.md` mirror the data as
  plain text; `<link rel="alternate">` points crawlers at them.
- `.nojekyll` stops GitHub Pages from rewriting `publications.md` into HTML.
