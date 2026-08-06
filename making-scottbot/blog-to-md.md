---
name: scholarly-blog-html-to-markdown
description: "Use this skill to convert academic WordPress blog posts saved as HTML from the Internet Archive Wayback Machine into faithful Markdown artifacts. Use it whenever the user uploads HTML files that are Wayback snapshots of blog posts (URL pattern web.archive.org/web/YYYYMMDD/...), even when phrased casually ('clean up these archived posts', 'turn these wayback HTML into markdown', 'a folder of saved scholarly posts'). Strips ALL Wayback chrome (toolbar, injected scripts, rewritten URLs) AND ALL WordPress chrome (header, footer, sidebar, nav, sharing widgets, related posts, comment forms) — leaving ONLY the post: title, byline, date, body, images, footnotes, and (by default) reader comments in their own section. Body preserved WORD-FOR-WORD. Output is Markdown with YAML frontmatter (original URL, archive date, author, blog title, post date, tags), an images/ folder, and a .zip download. Also works on non-Wayback WordPress HTML. Do NOT use for live web pages, non-WordPress sites, or summary-only requests."
---

# Wayback-Archived Scholarly Blog → Markdown

## The cardinal rule

**This skill produces a verbatim transcription of the post body, not a summary.** Every paragraph, every block quote, every list item, every footnote, every figure caption, and every preserved comment is reproduced exactly as it appears in the post. The only things removed are Wayback Machine chrome (the toolbar, injected scripts, archived-on banners, URL rewrites) and WordPress site chrome (header, footer, sidebar widgets, navigation, sharing buttons, related posts, comment forms). What you keep is the *post*; what you discard is the *envelope* the post arrived in.

If you find yourself thinking "this post is long, I'll condense it" — stop. The user wants a clean, archival, citable artifact, not a summary. Compression destroys the artifact.

If a folder of HTML files is too large to handle in one go, **write each post to disk progressively** — file by file — rather than truncating any of them.

## The second cardinal rule: no live-web embeds in the markdown

**The output Markdown contains zero live-web URLs in any *embedded* resource.** An "embedded resource" is anything the rendering tool auto-fetches without the user clicking — images, video, audio, iframes, `<object>`/`<embed>`, lazy-load `srcset`s, inline-CSS `background-image`. All of these get rewritten to local paths under `images/` (or `assets/` for media files).

**Hyperlinks (`<a href="...">`) are fine, regardless of what they point at** — a webpage, a PDF, a dataset, a tarball, a podcast episode, anything. A hyperlink is something the user clicks intentionally. It is not auto-fetched at render time, it doesn't leak the reader's IP to the host, and it doesn't make the markdown look "broken" if the host goes offline (the link just stops working — same as any other dead link in any document). Hyperlinks pointing at downloadable file types (`.pdf`, `.csv`, `.zip`, etc.) stay as live URLs unless the user explicitly asks otherwise.

So the rule is narrower than it sounds: convert *embeds* to local files; leave *hyperlinks* alone. Phase 7 implements this; Phase 10's Check 4 enforces it as a hard build-abort.

If an *embed* cannot be downloaded (no network, dead link, host returns 404 from every fallback), the skill emits a local placeholder image and records the original URL in YAML — **never** a live URL inside an `<img>`/`<video>`/`<iframe>`. The artifact's *embedded content* must be referentially closed when it leaves this skill: open the zip on a disconnected machine and every image still renders inline. Hyperlinks may still point off-machine; that's their nature.

## Operating discipline: never echo the post into chat

The single most common cause of *"Claude's response could not be fully generated"* on this kind of task is the model trying to render the converted post text directly into its own reply. A single long-form academic blog post — let alone a folder of fifty of them — well exceeds any single-response budget; once you start streaming the converted text into your message, the response is killed mid-flight and the user sees a truncation error. Avoid this failure mode by treating the rules below as non-negotiable.

**The artifact lives on disk. Your reply describes the artifact; it never contains it.**

### Rule 1 — Use a script as the primary extractor

Write a single Python script at `/home/claude/extract.py` that does the entire pipeline — Wayback stripping, body location, WordPress chrome removal, metadata extraction, image fetching, markdown conversion, YAML composition, zipping — and writes the final Markdown and zip to `/mnt/user-data/outputs/`. Run it once via `bash_tool`. Your conversational reply contains only a short summary of what was produced.

This is dramatically more reliable than emitting the converted markdown through repeated tool messages because the script's `stdout` does not compete with your reply for the response buffer. The model emits the script source plus a one-paragraph wrap-up — both small.

A safe scaffold:

```python
# /home/claude/extract.py
import sys, json, re, hashlib, shutil
from pathlib import Path
from bs4 import BeautifulSoup

INPUT  = Path(sys.argv[1])               # an .html file or a folder of .html files
OUTROOT = Path(sys.argv[2])              # /mnt/user-data/outputs
OUTROOT.mkdir(parents=True, exist_ok=True)

html_files = sorted(INPUT.rglob("*.htm*")) if INPUT.is_dir() else [INPUT]

allow_network = probe_network()      # Phase 7.4 — one probe per run, not per asset
processed, failed = [], []
for html_path in html_files:
    soup = BeautifulSoup(html_path.read_bytes(), "lxml")
    strip_wayback(soup)                  # Phase 2
    archive_url, archive_ts, original_url = capture_archive_meta(soup, html_path)
    unrewrite_all(soup)                  # Phase 2.2
    article = locate_article(soup)       # Phase 3
    strip_wordpress_chrome(article)      # Phase 4
    meta = extract_metadata(soup, article, html_path)   # Phase 5

    slug = make_slug(meta)               # e.g. "2018-05-15-on-paradigms"
    out_dir = OUTROOT / slug
    out_dir.mkdir(exist_ok=True)

    convert_iframes(article)             # Phase 7.6 — iframes → hyperlinks
    asset_report = localize_assets(      # Phase 7 — download every embed
        article, out_dir,
        archive_timestamp=archive_ts,
        original_post_url=original_url,
        allow_network=allow_network,
    )
    body_md = html_to_markdown(article, meta)           # Phase 6
    comments_md = render_comments(soup) if KEEP_COMMENTS else ""    # Phase 9
    write_markdown(out_dir / f"{slug}.md", meta, body_md, comments_md, asset_report)

    violations = audit_no_live_embeds(out_dir / f"{slug}.md")       # Phase 10, check 4
    if violations:
        print(f"FAIL {slug}: {len(violations)} live-embed URL(s) leaked")
        failed.append((slug, violations))
        continue

    package_zip(out_dir)                 # Phase 12
    processed.append(slug)

print(f"OK: processed {len(processed)} posts; {len(failed)} failed audit")
```

The functions referenced here are drafted in the phases below. Implement them in the script, not in chat.

### Rule 2 — Append, don't accumulate

If a folder contains many HTML files, write each post out as you process it. Do not accumulate all converted markdown in memory and then write at the end — partial progress is preserved if the script fails mid-run, and memory stays bounded.

### Rule 3 — Do not paste the converted text into your message

Not the YAML frontmatter, not the title, not a "preview snippet," not the comment list. Use `present_files` to surface the zip and let the user open it. Pasting fields in chat looks polite but pushes you toward the truncation cliff on a long-tailed batch.

### Rule 4 — Don't `view` the converted file just to inspect it

Once the file is written, never `view` the full markdown to confirm. Use shell tools that summarize:

```bash
wc -l -w "$MD_PATH"             # confirms size
head -25 "$MD_PATH"             # peek at YAML only
sed -n '/^---$/,/^---$/p' "$MD_PATH" | head -40   # YAML block only
grep -c '^## ' "$MD_PATH"       # heading count
ls -la "$OUT_DIR/images/"       # confirms image extraction
```

### Rule 5 — Process big batches in resumable passes

For folders containing dozens or hundreds of posts, structure the script with a `--resume` flag that skips posts whose output zip already exists. Each invocation processes a bounded slice and emits short stdout. A `progress.json` next to the outputs records what's done.

### Rule 6 — Cap your final user-facing reply

Aim for **roughly 150 words**: one paragraph stating how many posts were converted from which blog over what date range, the path to the deliverable zip, any caveats from `extraction_notes` (images that couldn't be fetched, posts where chrome was unusual, etc.), and the `present_files` call. If you find yourself writing a third paragraph, stop and delete.

### Rule 7 — If the truncation error has already happened, restart in script mode

If a previous attempt in the same conversation triggered the truncation error, the user has a partial or empty output. Acknowledge in one sentence, then resume by writing and running the extraction script per Rule 1. Do not try to "continue from where you left off" by emitting the next chunk of converted text — that retriggers the same failure.

### Rule 8 — Detection signal

If you find yourself about to type a code fence in your reply that contains more than ~50 lines of converted post content, **you are about to fail**. Stop. Move that content into a file write inside the script.

## When this skill applies

- A single `.html` file that is a Wayback Machine snapshot of an academic blog post.
- A folder of such HTML files (e.g., a researcher's whole archived blog, or a topical series).
- HTML files saved from non-Wayback WordPress sites — the Wayback-stripping pass simply finds nothing to strip and the rest of the pipeline runs unchanged.
- HTML from common scholarly blog hosts that run on WordPress: Hypotheses.org, the LSE Impact Blog, Crooked Timber, Public Books, the Chronicle blogs, individual academics' WordPress sites, university-hosted research blogs.

The skill works less well on non-WordPress platforms (Substack, Medium, Ghost, custom static sites) — the body-location and chrome-stripping heuristics are tuned to WordPress's DOM conventions. It can usually still produce *something* useful from these, but with more manual selector tuning. Note that as a caveat in `extraction_notes`.

## The output you produce

For an input file `2018-05-15-on-paradigms.html` (or a folder containing such files), produce in `/mnt/user-data/outputs/`:

```
2018-05-15-on-paradigms/             ← per-post working folder (one per HTML file)
├── 2018-05-15-on-paradigms.md       ← the converted markdown with YAML frontmatter
├── images/                          ← all post-body images, downloaded locally
│   ├── img-001.png
│   ├── img-002.jpg
│   └── _missing.png                 ← placeholder used when an image couldn't be fetched
└── assets/                          ← embedded video/audio media only
    ├── 001-podcast-episode.mp3
    ├── 002-lecture.mp4
    └── ...
2018-05-15-on-paradigms.zip          ← single-file deliverable per post
```

The `images/` and `assets/` folders together hold every **embedded** asset the post originally referenced — i.e., things the renderer auto-fetches (images, video, audio, iframe-converted media). The contract from Phase 7 guarantees that the `.md` file contains zero live URLs in any embedded resource. Hyperlinks (`[text](https://...)`) — including hyperlinks to PDFs, datasets, archives, podcast episodes, anything else the user clicks intentionally — pass through unchanged, because they're part of what the post says, not what the post displays.

For a multi-post batch, also produce a top-level zip and an index:

```
posts/
├── 2018-05-15-on-paradigms/...      (each with its own images/ and assets/)
├── 2018-06-20-replication-crisis/...
├── 2018-09-10-peer-review-failure/...
└── INDEX.md                         ← table of converted posts with links
posts.zip                            ← single deliverable for the whole batch
```

The zip is the **primary download**. The unzipped folder is kept on disk in case the user wants to browse markdown directly without unzipping.

When you finish, call `present_files` with the zip path **first** and the markdown path (or `INDEX.md` for batches) second. See Phase 11.

---

## Phase 1 — Triage the HTML

Before extracting anything, find out what you're working with.

### 1.1 Identify the input

- A single `.html` / `.htm` file → process as one post.
- A folder → process every `.html` / `.htm` it contains, recursively.
- A `.zip` of HTML files → unzip first, then process the folder.
- A mix of HTML and other files → process the HTML files only and ignore the rest.

### 1.2 Sample one file before processing the batch

For batches, open the first file and confirm the script's heuristics work on it before unleashing on hundreds. This catches theme-specific surprises early.

```bash
file /mnt/user-data/uploads/some-post.html
head -50 /mnt/user-data/uploads/some-post.html       # look for Wayback markers
grep -c "wm-ipp\|__wm\|web.archive.org" /mnt/user-data/uploads/some-post.html
```

### 1.3 Confirm it's actually a Wayback snapshot

The unmistakable signatures of a Wayback snapshot:

| Signature | Where it appears |
|---|---|
| `<!-- BEGIN WAYBACK TOOLBAR INSERT -->` HTML comment | near the opening of `<body>` |
| `<div id="wm-ipp-base">` or `<div id="wm-ipp">` | injected toolbar block |
| URLs containing `/web/<14 digits>/` | rewritten anchors and image srcs |
| `<script src="//web.archive.org/static/...">` | injected JS |
| Inline `__wm.init(...)` / `__wm.wombat(...)` calls | bottom of `<body>` |
| `archive_analytics`, `wbhack`, `wombat` JS globals | inline `<script>` content |

If none of these are present, the HTML is from a live site (or another archive service); skip Phase 2 and proceed to Phase 3.

### 1.4 Confirm it looks like WordPress

Common signatures:

| Signature | Where it appears |
|---|---|
| `<meta name="generator" content="WordPress …">` | `<head>` |
| Body classes: `wordpress`, `single-post`, `single-format-standard`, `postid-*` | `<body class="…">` |
| `<article id="post-<num>" class="post hentry">` | main content area |
| `<div class="entry-content">` | the post body wrapper |
| `<link rel="https://api.w.org/" …>` | `<head>` (REST API discovery) |
| `<link rel="pingback" …>` | `<head>` |
| Wp-content paths: `/wp-content/uploads/`, `/wp-content/themes/` | image and asset URLs |
| Comment markup: `<ol class="comment-list">`, `<article id="comment-<num>">` | comments section |

If most are present, you're on solid WordPress ground. If only a few are, the page may be a hybrid (e.g., a custom theme on a non-WordPress engine that mimics WP markup); proceed but expect to tune the body-location selectors in Phase 3.

---

## Phase 2 — Strip Wayback Machine chrome

Always run this pass first if Phase 1 confirmed Wayback signatures. After this pass, the DOM should look as close as possible to the original archived page.

### 2.1 Remove the toolbar block

```python
def strip_wayback(soup):
    # Toolbar wrappers
    for sel in ["#wm-ipp-base", "#wm-ipp", "#donato"]:
        for el in soup.select(sel):
            el.decompose()

    # Injected scripts referencing archive.org or wombat
    for s in soup.find_all("script"):
        src = s.get("src", "") or ""
        body = s.string or ""
        if ("archive.org" in src
            or "wombat" in src
            or "__wm" in body
            or "archive_analytics" in body
            or "wbhack" in body):
            s.decompose()

    # Injected stylesheets and links
    for link in soup.find_all("link"):
        if "archive.org" in (link.get("href") or ""):
            link.decompose()

    # HTML comments delimiting the toolbar
    from bs4 import Comment
    for c in soup.find_all(string=lambda x: isinstance(x, Comment)):
        if "WAYBACK TOOLBAR" in c or "End Wayback Rewrite" in c:
            c.extract()

    # Noscript fallbacks for the toolbar
    for ns in soup.find_all("noscript"):
        if "archive.org" in (ns.get_text() or ""):
            ns.decompose()
```

### 2.2 Rewrite Wayback-rewritten URLs back to originals

Wayback rewrites every `href` and `src` to a `/web/<timestamp>[<flag>]/<original>` form. Strip the prefix so the URLs in the markdown point at the original sites (with the original Wayback URL preserved in YAML for citation).

```python
WAYBACK_RE = re.compile(
    r"^(?:https?:)?//web\.archive\.org/web/\d{14}[a-z_]*/(https?://.+)$"
)
WAYBACK_PATH_RE = re.compile(
    r"^/web/\d{14}[a-z_]*/(https?://.+)$"
)

def unrewrite(url):
    if not url:
        return url
    m = WAYBACK_RE.match(url) or WAYBACK_PATH_RE.match(url)
    return m.group(1) if m else url

def unrewrite_all(soup):
    for tag, attr in [("a", "href"), ("img", "src"), ("img", "data-src"),
                      ("source", "srcset"), ("link", "href"),
                      ("video", "src"), ("audio", "src"),
                      ("iframe", "src")]:
        for el in soup.find_all(tag):
            if el.has_attr(attr):
                el[attr] = unrewrite(el[attr])
```

The flag suffix (`im_`, `cs_`, `js_`, `if_`, `oe_`) just tells Wayback what kind of resource to serve unaltered — strip them all alike.

### 2.3 Capture the archive URL and timestamp before unrewriting

The original-URL-and-archive-date metadata is **derived from one of the Wayback URLs you're about to rewrite away**. Capture it first:

```python
def capture_archive_meta(soup, html_path):
    """
    Returns (archive_url, archive_timestamp, original_url) or (None, None, None).
    """
    # The canonical link or og:url often holds the bare wayback URL
    for sel in ['link[rel="canonical"]', 'meta[property="og:url"]']:
        el = soup.select_one(sel)
        if el:
            url = el.get("href") or el.get("content") or ""
            m = re.match(r"(https?://web\.archive\.org/web/(\d{14})[a-z_]*/(https?://.+))", url)
            if m:
                return m.group(1), m.group(2), m.group(3)
    # Fallback: any anchor that points to a wayback URL of the same page
    for a in soup.find_all("a", href=True):
        m = re.match(r"(https?://web\.archive\.org/web/(\d{14})[a-z_]*/(https?://.+))", a["href"])
        if m:
            return m.group(1), m.group(2), m.group(3)
    # Final fallback: filename pattern
    m = re.search(r"(\d{14})", html_path.name)
    return None, m.group(1) if m else None, None
```

The archive timestamp goes into YAML as `archive_date` (formatted `YYYY-MM-DD` from the leading 8 digits). The original URL goes into YAML as `original_url`. The full Wayback URL goes into YAML as `archive_url`.

---

## Phase 3 — Locate the post body

WordPress themes vary, but cluster around predictable patterns. Try these selectors in order; the first non-empty match wins.

```python
ARTICLE_SELECTORS = [
    "article.hentry",
    "article.post",
    "article[id^='post-']",
    "main article",
    "article",                      # last-ditch HTML5 article
    "div.entry",                    # older themes
    "div.post",                     # older themes still
    "#content .post",
    "[itemtype*='BlogPosting']",
    "[itemtype*='Article']",
]

def locate_article(soup):
    for sel in ARTICLE_SELECTORS:
        nodes = soup.select(sel)
        if nodes:
            # If multiple matches (e.g., archive page vs single-post page),
            # prefer the one with the most text content.
            return max(nodes, key=lambda n: len(n.get_text(strip=True)))
    raise RuntimeError("Could not locate article element")
```

If `locate_article` raises, the page may be an index/archive page rather than a single post — note in `extraction_notes` and skip, or fall back to the largest `<div>` whose text length dominates the page (a heuristic of last resort).

The body content within the article is usually further wrapped in `.entry-content` or `.post-content`. Find it for tight scoping:

```python
BODY_SELECTORS = [".entry-content", ".post-content", ".entry", ".content"]

def locate_body(article):
    for sel in BODY_SELECTORS:
        node = article.select_one(sel)
        if node:
            return node
    return article   # whole article is the body
```

---

## Phase 4 — Strip WordPress chrome from inside the article

Even after isolating the article, themes inject sharing widgets, related-post lists, author boxes, post-navigation, and ads inside the article element. Remove them.

```python
CHROME_SELECTORS = [
    # Jetpack
    ".sharedaddy", ".sd-block", ".sd-sharing-enabled",
    ".jp-relatedposts", "#jp-post-flair",
    ".sd-rating", ".sd-like",
    # WordPress.com / generic
    ".wp-block-latest-posts", ".wp-block-latest-comments",
    ".post-navigation", ".nav-links", ".nav-previous", ".nav-next",
    ".entry-footer .cat-tags",      # we'll capture tags into YAML separately
    ".entry-meta",                   # ditto for date/author
    # Common social-sharing plugins
    ".addtoany_share_save_container", ".addthis_toolbox",
    ".sharebox", ".social-share", ".st_sharethis", ".sharing-buttons",
    # Related/recommended-post plugins
    ".yarpp-related", ".crp_related", ".related-posts",
    # Author box plugins
    ".author-bio", ".author-box", ".about-author",   # decision: also capture into YAML, then strip
    # Ads and donation widgets
    ".adsbygoogle", ".ad-container", ".donation-widget",
    # Subscribe / newsletter widgets injected mid-post
    ".subscribe-form", ".newsletter-signup", ".mc4wp-form",
    # Print/email post links
    ".print-link", ".email-link",
    # Comment form (separate from the comment list — the *form* gets stripped)
    "#respond", ".comment-respond", "#commentform", "#reply-title",
    # WordPress emoji helper
    "img.wp-smiley",
    # Pingback/trackback markers in the comment list (if comments preserved)
    ".pingback", ".trackback",
]

def strip_wordpress_chrome(article):
    for sel in CHROME_SELECTORS:
        for el in article.select(sel):
            el.decompose()
    # Strip empty paragraphs left behind
    for p in article.find_all("p"):
        if not p.get_text(strip=True) and not p.find(["img", "iframe", "video"]):
            p.decompose()
```

### 4.1 Strip surrounding chrome at the page level

Once the article is isolated and cleaned, the rest of the soup (header, footer, sidebar) is irrelevant — but if you continue to walk the soup for metadata, ignore these regions:

```python
PAGE_CHROME_SELECTORS = [
    "header#masthead", ".site-header", "#site-header",
    "footer#colophon", ".site-footer", "#site-footer",
    "aside#secondary", ".widget-area", "#sidebar", ".sidebar",
    "nav#site-navigation", ".main-navigation", ".primary-menu",
    "#wpadminbar",                    # if logged in when the page was archived
]
```

If you're producing the markdown from the article subtree only, these never enter the output and you don't need to remove them — but you'll filter them out when you scan for metadata in Phase 5.

---

## Phase 5 — Extract bibliographic metadata

Pull from every available source and reconcile, in order of reliability.

### 5.1 JSON-LD (most reliable when present)

```python
import json

def extract_jsonld(soup):
    out = {}
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "")
        except Exception:
            continue
        if isinstance(data, list):
            data = next((d for d in data
                         if isinstance(d, dict)
                         and d.get("@type") in ("BlogPosting", "Article", "NewsArticle")), None)
        if not isinstance(data, dict):
            continue
        if data.get("@type") in ("BlogPosting", "Article", "NewsArticle"):
            return data
    return out
```

JSON-LD on a well-configured WordPress site gives you `headline`, `datePublished`, `dateModified`, `author` (often a structured object), `publisher`, `description`, `image`, `mainEntityOfPage`, `keywords` — basically everything you need.

### 5.2 Open Graph and standard meta tags

Fall through to OG tags when JSON-LD is missing:

```python
def extract_og(soup):
    return {
        "og_title":       _meta(soup, "og:title"),
        "og_description": _meta(soup, "og:description"),
        "og_url":         _meta(soup, "og:url"),
        "og_type":        _meta(soup, "og:type"),
        "og_site_name":   _meta(soup, "og:site_name"),
        "article_published_time":   _meta(soup, "article:published_time"),
        "article_modified_time":    _meta(soup, "article:modified_time"),
        "article_author":  _meta(soup, "article:author"),
        "article_section": _meta(soup, "article:section"),
        "article_tag":     [m.get("content") for m in soup.find_all("meta", attrs={"property": "article:tag"})],
        "twitter_creator": _meta(soup, "twitter:creator"),
    }

def _meta(soup, prop):
    el = soup.find("meta", attrs={"property": prop}) \
       or soup.find("meta", attrs={"name": prop})
    return el.get("content") if el else None
```

### 5.3 Visible markup (fallback)

If JSON-LD and OG both fail, harvest from the visible WordPress markup:

```python
def extract_visible(article, soup):
    out = {}
    title = article.select_one(".entry-title, h1.post-title, h1") \
         or soup.select_one("title")
    out["title"] = (title.get_text(strip=True) if title else "")

    time_el = article.select_one("time[datetime], .entry-date, .published")
    if time_el:
        out["date"] = time_el.get("datetime") or time_el.get_text(strip=True)

    author = article.select_one(".author.vcard .fn, .byline .author, [rel='author']")
    if author:
        out["author"] = author.get_text(strip=True)

    out["categories"] = [a.get_text(strip=True) for a in article.select(".cat-links a, [rel='category']")]
    out["tags"] = [a.get_text(strip=True) for a in article.select(".tags-links a, [rel='tag']")]

    # Author bio paragraph (often present in academic blogs above or below the post)
    bio = article.select_one(".author-bio, .author-box, .about-author")
    if bio:
        out["author_bio"] = bio.get_text(" ", strip=True)
    return out
```

### 5.4 Blog-level metadata

The blog (not the post) has its own metadata too: site title, tagline, primary author/editor for solo blogs.

```python
def extract_blog_meta(soup):
    out = {}
    site_title = soup.select_one(".site-title, #site-title, h1.site-title")
    out["blog_title"] = site_title.get_text(strip=True) if site_title else _meta(soup, "og:site_name") or ""
    tagline = soup.select_one(".site-description, .site-tagline")
    out["blog_tagline"] = tagline.get_text(strip=True) if tagline else ""
    return out
```

### 5.5 Compose the YAML frontmatter

```yaml
---
# --- post identity ---
title: "On Paradigm Shifts in Science"
subtitle: ""
authors:
  - family: "Galloway"
    given: "Anne"
    affiliation: "Victoria University of Wellington"
    url: "https://example.com/author/agalloway"
post_date: "2018-05-15"
modified_date: "2018-05-17"

# --- blog identity ---
blog_title: "Crooked Scholarship"
blog_tagline: "Notes from a working researcher"
blog_url: "https://crookedscholarship.example.com/"
blog_platform: "WordPress"

# --- categorization ---
categories: ["philosophy of science", "history of ideas"]
tags: ["paradigms", "kuhn", "scientific revolution"]

# --- archival provenance ---
original_url: "https://crookedscholarship.example.com/2018/05/15/on-paradigm-shifts/"
archive_url: "https://web.archive.org/web/20180520142733/https://crookedscholarship.example.com/2018/05/15/on-paradigm-shifts/"
archive_date: "2018-05-20"
archive_timestamp: "20180520142733"

# --- descriptive ---
description: |
  Verbatim post description / excerpt as it appeared in the source meta tags.
language: "en"

# --- comments ---
comments_preserved: true
comment_count: 12

# --- provenance ---
source_html: "2018-05-15-on-paradigms.html"
source_html_sha256: "ab12...cd34"
extraction_date: "2026-04-26"
extraction_tool: "claude scholarly-blog-html-to-markdown skill"
extraction_notes: |
  Wayback toolbar and injected scripts stripped. Post body taken from
  article.hentry > .entry-content. Comments preserved (12 of 12). All
  inline images downloaded from Wayback (200 DPI originals where available).
  Footnotes converted from sup/anchor pattern to Markdown footnote syntax.
---
```

Compute SHA-256 with `hashlib.sha256(html_path.read_bytes()).hexdigest()`. The hash lets a future reader prove the markdown corresponds to the exact HTML bytes processed.

---

## Phase 6 — Convert the body to Markdown

The cleaned article subtree maps cleanly to Markdown. The two viable paths are:

1. **Hand-roll using BeautifulSoup walking** — total control, ~150 lines, predictable output.
2. **Use a converter library** — `markdownify` is the best fit; pip-install if missing.

Use option 2 by default, with a custom converter class that handles WordPress-specific patterns. Option 1 is the fallback when markdownify produces noisy output for an unusual theme.

```python
# pip install markdownify --break-system-packages
from markdownify import MarkdownConverter

class BlogConverter(MarkdownConverter):
    """WordPress-tuned HTML→Markdown converter."""

    def convert_blockquote(self, el, text, parent_tags):
        # Markdownify's default is fine, but ensure trailing blank line
        return super().convert_blockquote(el, text, parent_tags) + "\n"

    def convert_pre(self, el, text, parent_tags):
        # Preserve fenced code blocks; detect language from class
        code_el = el.find("code")
        lang = ""
        if code_el and code_el.get("class"):
            for c in code_el["class"]:
                if c.startswith("language-"):
                    lang = c[len("language-"):]
        return f"\n```{lang}\n{el.get_text()}\n```\n"

    def convert_figure(self, el, text, parent_tags):
        # <figure><img …><figcaption>…</figcaption></figure>
        img = el.find("img")
        cap = el.find("figcaption")
        if not img: return text
        alt = img.get("alt", "") or (cap.get_text(strip=True) if cap else "")
        src = img.get("src", "")
        out = f"\n![{alt}]({src})\n"
        if cap:
            out += f"\n*{cap.get_text(strip=True)}*\n"
        return out

def html_to_markdown(article, images_dir, meta):
    converter = BlogConverter(
        heading_style="ATX",            # # H1, ## H2, etc.
        bullets="-",
        strong_em_symbol="*",
        code_language="",
        escape_underscores=False,
        escape_asterisks=False,
        wrap=False,
    )
    md = converter.convert_soup(article)
    md = postprocess(md)                # see 6.1
    return md
```

### 6.1 Post-process the markdown

```python
def postprocess(md):
    # Collapse runs of >2 blank lines
    md = re.sub(r"\n{3,}", "\n\n", md)
    # Trim trailing whitespace per line
    md = "\n".join(line.rstrip() for line in md.splitlines())
    # Normalize NBSPs to regular spaces
    md = md.replace("\u00a0", " ")
    # Strip WordPress's autop artifacts: <p>\u00a0</p> patterns leave " " paragraphs
    md = re.sub(r"^\s*\\$", "", md, flags=re.MULTILINE)
    return md.strip() + "\n"
```

### 6.2 Block-level fidelity

Verify the converter handles these correctly; if not, write a custom handler:

| HTML element | Markdown output |
|---|---|
| `<h1>` … `<h6>` | `#` … `######` (use ATX style) |
| `<p>` | paragraph + blank line |
| `<blockquote>` | `>` prefix; nested blockquotes get `>>` |
| `<ul>` / `<ol>` | `-` / `1.`; preserve nesting via indentation |
| `<pre><code>` | fenced code block with language detection |
| `<code>` (inline) | backticks |
| `<em>`, `<i>` | `*…*` |
| `<strong>`, `<b>` | `**…**` |
| `<a href="X">Y</a>` | `[Y](X)` |
| `<img src="X" alt="Y">` | `![Y](X)` (where X is `images/img-NNN.ext` after Phase 7 localization, never a live URL) |
| `<figure>` + `<figcaption>` | image + italicized caption paragraph |
| `<table>` | GitHub-flavored Markdown table |
| `<hr>` | `---` |
| `<sup>` (footnote ref) | `[^N]` (see Phase 8) |
| `<dl><dt><dd>` | `**term**\n: definition` (definition-list extension) or fall back to bold + paragraph |

### 6.3 Tables

Markdownify handles simple tables. For complex ones (merged cells, nested content), it falls back to keeping the HTML table inline, which is valid in most Markdown flavors but ugly. If you encounter complex tables and the user's downstream tooling handles inline HTML, leave them as `<table>`. Otherwise, render to Markdown by hand using the same approach as the PDF skill's table converter.

### 6.4 Block quotes with attribution

Academic posts often quote sources with attribution lines. Preserve them:

```markdown
> The structure of revolutions is itself revolutionary.
>
> — Kuhn 1962, 84
```

### 6.5 What about the post title?

The title belongs in the YAML frontmatter (`title:`). Optionally also emit it as `# Title` at the top of the body — most users expect this. Default: emit the H1.

```python
def write_markdown(md_path, meta, body_md, comments_md):
    yaml_block = compose_yaml(meta)
    parts = ["---", yaml_block, "---", "", f"# {meta['title']}", "", body_md]
    if comments_md:
        parts += ["", "---", "", "## Reader Comments", "", comments_md]
    md_path.write_text("\n".join(parts), encoding="utf-8")
```

---

## Phase 7 — Localize embedded assets (the no-live-embed contract)

**The contract:** the only live-web URLs that survive into the final Markdown are inside hyperlinks (`[anchor text](URL)`) and inside YAML provenance fields. Every *embedded* resource — anything the rendering tool auto-fetches without the user clicking — must be rewritten to a local path under `images/` (or `assets/` for non-image media). No exceptions on embeds. No surgery on hyperlinks.

The distinction that matters: **does the markdown renderer fetch the resource on its own, or does the reader click to fetch it?**

- Auto-fetched (must localize): `<img>`, `<video>`, `<audio>`, `<iframe>`, `<object>`, `<embed>`, `<picture>`/`<source>`, `srcset`, inline-CSS `background-image`.
- User-clicked (leave alone): `<a href="...">`, no matter what file type it points at — webpage, PDF, dataset, tarball, podcast, anything. Hyperlinks are part of the post's content; rewriting them would silently change what the post says.

This embed/hyperlink distinction matters because:

- Live-URL `<img src>` rots silently the day the source goes offline. The markdown renders with broken-image icons and the reader doesn't know what was supposed to be there.
- Live-URL embeds also leak the reader's IP to whatever third-party host the blog used (often a CDN with tracking), which is a privacy regression compared to the original archived page.
- Hyperlinks have neither problem: they don't fire at render time, they don't leak IPs, and a dead hyperlink is a normal failure mode every reader knows how to interpret.

If an embed cannot be localized (network failure, 404 at every fallback URL), **do not emit a live URL inside an `<img>`/`<video>`/`<iframe>`**. Substitute a local placeholder image and record the failure in `extraction_notes`. Hyperlinks, by contrast, never need a placeholder — even a dead `<a href>` is a faithful preservation of what the post said.

### 7.1 The catalog of embeds to localize

Walk the article subtree and collect every *embedded* asset reference. The full list:

| HTML element | Attribute(s) | Asset class | Localized to |
|---|---|---|---|
| `<img>` | `src`, `data-src`, `data-lazy-src`, `data-original`, `srcset` | image | `images/` |
| `<picture>` / `<source>` | `srcset` | image | `images/` |
| `<video>` | `src`, `poster` | video / image | `assets/` and `images/` |
| `<source>` (inside video/audio) | `src`, `srcset` | video/audio | `assets/` |
| `<audio>` | `src` | audio | `assets/` |
| `<embed>` / `<object>` | `src` / `data` | embedded asset | `assets/` |
| `<iframe>` | `src` | embedded page | **do NOT auto-localize**; convert to a hyperlink (§7.6) |
| Inline CSS `background-image: url(...)` | — | image | `images/` |
| **`<a href="...">`** | `href` | **hyperlink** | **leave as-is, regardless of file extension** |

The lazy-load attributes (`data-src`, `data-lazy-src`, `data-original`, `data-srcset`) matter because many WordPress themes ship with lazy-load plugins; the *real* image URL is in the `data-*` attribute and `src` is a 1-pixel placeholder GIF. Always check the data-attributes first, fall back to `src`.

Note explicitly: `<a href="https://example.com/paper.pdf">the supplementary PDF</a>` stays as a live hyperlink in the markdown. The reader will click it the same way they click any other link. The skill does not download it, does not move it under `assets/`, and does not rewrite the URL.

### 7.2 The download routine

```python
import urllib.request, urllib.parse, urllib.error, mimetypes, hashlib, re, time
from pathlib import Path

# Media file extensions that may appear as src on <video>/<audio>/<source>.
# These are auto-fetched embeds when present in those elements; in <a href>
# they are hyperlinks and we leave them alone.
MEDIA_EXTS = {
    ".mp3", ".m4a", ".wav", ".ogg", ".oga", ".flac", ".opus",
    ".mp4", ".m4v", ".mov", ".webm", ".mkv", ".ogv",
}

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp", ".avif", ".tiff"}

class AssetLocalizer:
    def __init__(self, post_dir: Path, archive_timestamp: str | None,
                 original_post_url: str | None, allow_network: bool):
        self.images_dir = post_dir / "images"
        self.assets_dir = post_dir / "assets"
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        self.archive_timestamp = archive_timestamp
        self.original_post_url = original_post_url
        self.allow_network = allow_network
        self.url_to_local = {}        # dedup: same URL → same local file
        self.failures = []            # (url, reason)
        self.success_count = 0
        self.image_counter = 0
        self.asset_counter = 0

    def localize_article(self, article):
        self._handle_imgs(article)
        self._handle_picture_sources(article)
        self._handle_video_audio(article)
        self._handle_object_embed(article)
        self._handle_inline_bg(article)
        # Hyperlinks (<a href>) are NOT touched — they're user-clicked, not embedded.
        # Iframes are converted to hyperlinks separately in §7.6.
        return self.success_count, self.failures

    # ---- handlers ----

    def _handle_imgs(self, article):
        for img in article.find_all("img"):
            url = self._best_img_url(img)
            if not url or url.startswith("data:"):
                continue
            local = self._fetch_to(url, kind="image")
            if local:
                img["src"] = f"images/{local.name}"
                img["data-original-src"] = url
            else:
                # Placeholder + alt-text augmentation — see §7.5
                self._make_placeholder(img, url, kind="image")
            # Always strip lazy-load attrs and srcset to prevent live fetches
            for a in ("srcset", "data-src", "data-lazy-src", "data-srcset",
                      "data-original", "data-orig-src", "data-lazy-srcset"):
                if img.has_attr(a):
                    del img[a]

    def _handle_picture_sources(self, article):
        # <picture><source srcset="..."><img src="..."></picture>
        # Markdown has no <picture> equivalent. Strip <source> elements;
        # the inner <img> was already handled above.
        for source in article.select("picture source"):
            source.decompose()

    def _handle_video_audio(self, article):
        for media in article.find_all(["video", "audio"]):
            srcs = []
            if media.get("src"):
                srcs.append(media["src"])
            for s in media.find_all("source"):
                if s.get("src"):
                    srcs.append(s["src"])
                if s.has_attr("srcset"):
                    del s["srcset"]
            poster = media.get("poster")
            local_media = None
            for url in srcs:
                local_media = self._fetch_to(url, kind="asset")
                if local_media:
                    media["src"] = f"assets/{local_media.name}"
                    # Drop child <source> elements; we've localized one src
                    for s in media.find_all("source"):
                        s.decompose()
                    break
            if not local_media and srcs:
                self.failures.append((srcs[0], "media download failed"))
                # Replace the whole media element with a hyperlink placeholder
                from bs4 import BeautifulSoup
                placeholder = BeautifulSoup(
                    f'<p><em>[Media unavailable — original URL recorded '
                    f'in YAML extraction_notes]</em></p>', "lxml"
                ).p
                media.replace_with(placeholder)
                continue
            if poster:
                local_poster = self._fetch_to(poster, kind="image")
                if local_poster:
                    media["poster"] = f"images/{local_poster.name}"
                else:
                    del media["poster"]

    def _handle_object_embed(self, article):
        for el in article.find_all(["object", "embed"]):
            url = el.get("data") or el.get("src")
            if not url:
                el.decompose()
                continue
            local = self._fetch_to(url, kind="asset")
            if local:
                # Replace with a hyperlink, since markdown won't render <object>
                from bs4 import BeautifulSoup
                link = BeautifulSoup(
                    f'<p><a href="assets/{local.name}">'
                    f'Embedded asset: {local.name}</a></p>', "lxml"
                ).p
                el.replace_with(link)
            else:
                el.decompose()

    def _handle_inline_bg(self, article):
        # CSS-style background-image references in inline style attrs
        bg_re = re.compile(r"background(?:-image)?\s*:\s*url\(['\"]?([^'\")]+)['\"]?\)")
        for el in article.find_all(style=True):
            new_style = el["style"]
            for url in bg_re.findall(el["style"]):
                local = self._fetch_to(url, kind="image")
                if local:
                    new_style = new_style.replace(url, f"images/{local.name}")
                else:
                    # Drop the rule entirely; markdown won't render it anyway
                    new_style = bg_re.sub("", new_style)
            el["style"] = new_style.strip()
            if not el["style"]:
                del el["style"]

    # ---- helpers ----

    def _best_img_url(self, img):
        """Pick the best URL: prefer real srcset largest, then data-*, then src."""
        # srcset gives multiple candidates; pick the widest
        if img.get("srcset"):
            candidates = []
            for part in img["srcset"].split(","):
                tokens = part.strip().split()
                if not tokens:
                    continue
                url = tokens[0]
                width = 0
                if len(tokens) > 1 and tokens[1].endswith("w"):
                    try: width = int(tokens[1][:-1])
                    except ValueError: pass
                candidates.append((width, url))
            if candidates:
                return max(candidates, key=lambda x: x[0])[1]
        for attr in ("data-src", "data-lazy-src", "data-original", "data-orig-src"):
            if img.get(attr):
                return img[attr]
        return img.get("src")

    def _url_ext(self, url):
        path = urllib.parse.urlparse(url).path.lower()
        # strip query/fragment, take last extension
        for ext in sorted(MEDIA_EXTS | IMAGE_EXTS, key=len, reverse=True):
            if path.endswith(ext):
                return ext
        return ""

    def _make_placeholder(self, img, url, kind):
        # 1x1 transparent PNG, written once and reused
        ph = self.images_dir / "_missing.png"
        if not ph.exists():
            # bytes for a 1x1 transparent PNG
            ph.write_bytes(bytes.fromhex(
                "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
                "0000000d49444154789c6300010000000500010d0a2db40000000049454e44ae426082"
            ))
        img["src"] = f"images/{ph.name}"
        existing_alt = img.get("alt", "")
        img["alt"] = (existing_alt + " [image unavailable]").strip()
        img["data-original-src"] = url
        self.failures.append((url, "image download failed; placeholder used"))

    def _fetch_to(self, url, kind):
        if not self.allow_network:
            return None
        url = self._absolutize(url)
        if url in self.url_to_local:
            return self.url_to_local[url]
        candidates = self._candidate_urls(url, kind)
        for candidate in candidates:
            try:
                return self._do_fetch(candidate, original=url, kind=kind)
            except Exception as e:
                self.failures.append((candidate, str(e)))
        return None

    def _absolutize(self, url):
        if url.startswith(("http://", "https://", "//")):
            return url if not url.startswith("//") else "https:" + url
        if self.original_post_url:
            return urllib.parse.urljoin(self.original_post_url, url)
        return url

    def _candidate_urls(self, url, kind):
        """Try the original first, then the Wayback equivalent, then any
        alternate Wayback flag for the asset class."""
        out = [url]
        if self.archive_timestamp and not url.startswith("https://web.archive.org/"):
            flag = "im_" if kind == "image" else "if_"
            out.append(f"https://web.archive.org/web/{self.archive_timestamp}{flag}/{url}")
            # Without the flag (gives the rewritten variant; sometimes the only one)
            out.append(f"https://web.archive.org/web/{self.archive_timestamp}/{url}")
        return out

    def _do_fetch(self, url, original, kind):
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; ScholarlyBlogToMD/1.0)",
                "Accept": "*/*",
            },
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
            ctype = (r.headers.get("Content-Type") or "").split(";")[0].strip().lower()
        if not data:
            raise ValueError("empty response")
        if len(data) < 100 and kind == "image":
            raise ValueError(f"suspiciously small image ({len(data)} bytes)")
        # Determine extension and target directory
        if kind == "image":
            ext = mimetypes.guess_extension(ctype) or self._url_ext(original) or ".bin"
            if ext == ".jpe": ext = ".jpg"
            self.image_counter += 1
            target = self.images_dir / f"img-{self.image_counter:03d}{ext}"
        else:
            ext = self._url_ext(original) or mimetypes.guess_extension(ctype) or ".bin"
            self.asset_counter += 1
            # Try to keep a meaningful filename for downloads
            base = Path(urllib.parse.urlparse(original).path).stem or f"asset-{self.asset_counter:03d}"
            base = re.sub(r"[^A-Za-z0-9._-]", "-", base)[:60]
            target = self.assets_dir / f"{self.asset_counter:03d}-{base}{ext}"
        target.write_bytes(data)
        self.url_to_local[url] = target
        self.url_to_local[original] = target
        self.success_count += 1
        return target
```

### 7.3 Wire it into the pipeline

```python
def localize_assets(article, post_dir, archive_timestamp, original_post_url, allow_network):
    loc = AssetLocalizer(post_dir, archive_timestamp, original_post_url, allow_network)
    succeeded, failures = loc.localize_article(article)
    return {
        "succeeded": succeeded,
        "failures": failures,
        "had_network": allow_network,
        "image_count": loc.image_counter,
        "asset_count": loc.asset_counter,
    }
```

Call this **after** Phase 4 (chrome stripped) and **before** Phase 6 (markdown conversion). When the converter walks `<img src="images/img-001.png">` it produces clean local paths in the output.

### 7.4 Network policy in this environment

The sandbox network has an allowlist (see system context). Image hosts and `web.archive.org` are typically **not** on the default allowlist. Three strategies, applied in order:

1. **Probe once, before the batch.** Hit one of the URLs you're going to need (e.g., `https://web.archive.org/`) with a 5-second timeout. If it fails, set `allow_network=False` for the whole run and **switch to the placeholder strategy below** — do not let the script try-and-fail on every single asset.

2. **If the probe succeeds**, run the localizer normally. Track per-asset failures and keep going; one 404 doesn't fail the post.

3. **If the user has an alternate environment** (Cowork, a local install with full network, an environment where Wayback is allowlisted), they can rerun the script with `--with-network` and the same input. The script must be deterministic on the input HTML so reruns produce identical output.

```python
def probe_network():
    try:
        urllib.request.urlopen("https://web.archive.org/", timeout=5)
        return True
    except Exception:
        return False
```

### 7.5 Placeholder strategy when the network is unavailable

When `allow_network=False`, **do not leave live URLs in the markdown.** Instead:

- Every `<img>` gets its `src` replaced with `images/_missing.png` (a 1×1 transparent PNG written once into `images/`).
- The original URL is preserved in two places: the `data-original-src` HTML attribute (which markdown converters typically discard, which is fine — the markdown has no live URL) and the per-asset entry in `extraction_notes` (which the user can read).
- The image's `alt` attribute is augmented with `[image unavailable]` so the user reading the rendered markdown sees that something was supposed to be there.
- For other assets (videos, downloads), the element is replaced with an inline note `[Media unavailable — original URL recorded in YAML extraction_notes]`. Again: no live URL in the rendered output.

Then write a structured manifest of missing assets into the YAML so the user can run a side script later to fetch them (or re-run the skill with network):

```yaml
extraction_notes: |
  Network access was unavailable; 12 images and 1 PDF were not localized.
  Placeholder image (images/_missing.png) substituted for each missing image.
  Original URLs are listed under `missing_assets:` below — re-run with
  network access (or feed the listed URLs to a downloader) to localize them.

missing_assets:
  - kind: image
    placeholder: "images/_missing.png"
    original_url: "https://example.com/wp-content/uploads/2018/05/fig1.png"
    archive_url: "https://web.archive.org/web/20180520142733im_/https://example.com/wp-content/uploads/2018/05/fig1.png"
  - kind: pdf
    placeholder: null
    original_url: "https://example.com/papers/draft.pdf"
    archive_url: "https://web.archive.org/web/20180520142733if_/https://example.com/papers/draft.pdf"
```

This keeps the markdown referentially closed while also keeping the recovery information machine-readable.

### 7.6 Iframes and other embeddable widgets

Iframes (YouTube, Vimeo, SlideShare, embedded tweets, Genially, Datawrapper, Flourish, etc.) are different from images and downloadable files: their content is dynamic and dependent on a live third-party service. Do not try to localize iframe targets. Instead, **convert each iframe to a Markdown hyperlink** to the embedded URL:

```python
def convert_iframes(article):
    for iframe in article.find_all("iframe"):
        src = iframe.get("src")
        title = iframe.get("title") or "Embedded content"
        if not src:
            iframe.decompose()
            continue
        # Resolve the underlying URL where possible (e.g., YouTube embed → watch URL)
        canonical = _canonical_embed_url(src)
        from bs4 import BeautifulSoup
        replacement = BeautifulSoup(
            f'<p><em>Embedded: <a href="{canonical}">{title}</a></em></p>',
            "lxml"
        ).p
        iframe.replace_with(replacement)

def _canonical_embed_url(src):
    # YouTube
    m = re.search(r"youtube(?:-nocookie)?\.com/embed/([^/?#]+)", src)
    if m:
        return f"https://www.youtube.com/watch?v={m.group(1)}"
    # Vimeo
    m = re.search(r"player\.vimeo\.com/video/(\d+)", src)
    if m:
        return f"https://vimeo.com/{m.group(1)}"
    return src
```

A hyperlink to YouTube is allowed by the contract (it's a hyperlink, not an embedded asset) and it preserves the user's ability to find the content. The iframe itself is gone from the markdown — no auto-fetch happens at render time.

### 7.7 Summary of the contract

After Phase 7, the article subtree must satisfy:

**Forbidden (live URLs in embedded resources):**
- Zero `<img src="http…">` — every `<img>` either has a `src="images/…"` local path or has been replaced with a placeholder.
- Zero `<video src="http…">` / `<audio src="http…">` / `<source src="http…">` — same rule.
- Zero `<object data="http…">` / `<embed src="http…">` — replaced with hyperlinks or removed.
- Zero `<iframe src="http…">` — replaced with hyperlinks per §7.6.
- Zero `srcset` attributes containing live URLs — stripped during img localization.
- Zero inline `style="background-image: url(http…)"` rules — rewritten to local or removed.

**Allowed (live URLs in user-clicked references):**
- `<a href="http…">` pointing at any URL — webpages, PDFs, datasets, audio, video, archives, anything. Hyperlinks are user-clicked, not auto-fetched. They are part of the post's content and stay verbatim.
- YAML frontmatter provenance fields (`original_url`, `archive_url`, `blog_url`, etc.).

When this subtree is converted to Markdown in Phase 6, the resulting `.md` file inherits the contract: no live URLs in any embedded resource, but hyperlinks to anywhere on the web (regardless of file type) pass through unchanged.



---

## Phase 8 — Footnotes and academic apparatus

Academic blog posts on WordPress use one of three footnote conventions; detect which and convert to Markdown footnote syntax.

### 8.1 Convention A: superscript anchors with an `<ol>` at the end

The most common pattern, used by plugins like *footnotes for WordPress*:

```html
<p>...as Kuhn argued<sup id="fnref-1"><a href="#fn-1">[1]</a></sup>.</p>
...
<ol class="footnotes">
  <li id="fn-1">For an alternative formulation, see Smith 2009. <a href="#fnref-1">↩</a></li>
</ol>
```

```python
def convert_footnotes_a(article):
    notes = {}
    # Capture definitions
    for ol in article.select("ol.footnotes, ol.fn, .footnotes ol"):
        for li in ol.find_all("li"):
            fid = li.get("id", "")
            # Strip the back-link
            for a in li.find_all("a"):
                if a.get("href", "").startswith("#fnref"):
                    a.decompose()
            notes[fid] = li.get_text(" ", strip=True)
        ol.decompose()
    # Replace <sup><a href="#fn-N">[N]</a></sup> with [^N]
    for sup in article.find_all("sup"):
        a = sup.find("a")
        if a and (a.get("href") or "").startswith("#fn"):
            target = a["href"][1:]
            num = re.search(r"\d+", target)
            if num:
                sup.replace_with(f"[^{num.group()}]")
    return notes
```

Append the definitions at the end of the markdown body:

```markdown
…as Kuhn argued[^1].

[^1]: For an alternative formulation, see Smith 2009.
```

### 8.2 Convention B: inline parenthetical with a "Notes" section

Some bloggers number references inline like `(1)` and use a `<h2>Notes</h2>` followed by an `<ol>`. Detect by finding a heading with text "Notes" or "Footnotes" near the end of the article and converting the following `<ol>` the same way.

### 8.3 Convention C: shortcode-rendered tooltips

Some plugins render footnotes as `<a class="footnote-link">` with the note content in a `<span class="footnote-content">`. The note text is in the DOM but visually hidden until hover. Extract:

```python
def convert_footnotes_c(article):
    notes = {}
    counter = 0
    for a in article.select("a.footnote-link, span.footnote, .footnote-tooltip"):
        counter += 1
        content = a.find(class_=re.compile("footnote-content|footnote-text"))
        text = content.get_text(" ", strip=True) if content else a.get("title") or ""
        notes[str(counter)] = text
        a.replace_with(f"[^{counter}]")
    return notes
```

### 8.4 Output

Always emit footnotes as Markdown footnote syntax (`[^N]` in body, `[^N]:` definition at end). Number sequentially within the post (do not preserve "1, 1a, 2" mixed numberings — flatten to `1, 2, 3` and note the original numbering in the definition body if non-trivial).

### 8.5 Bibliography section

If the post has a "References", "Bibliography", or "Works Cited" heading at the end, preserve that section verbatim — do not convert the entries to footnotes. Bibliography entries are not footnotes; they're a separate scholarly apparatus that lives at the post end.

---

## Phase 9 — Comments (preserve by default)

Academic blog comments are often substantive — counter-arguments, citation suggestions, peer corrections. Preserve them by default in their own clearly-marked section. Allow a `--no-comments` flag to suppress.

### 9.1 Locate the comment list

```python
def extract_comments(soup):
    container = soup.select_one("#comments, .comments-area, ol.comment-list")
    if not container:
        return []
    out = []
    for c in container.select("li.comment, article.comment, .comment-body"):
        author = c.select_one(".comment-author .fn, .comment-author cite, .vcard .fn")
        date = c.select_one(".comment-meta time, .comment-date, time")
        body = c.select_one(".comment-content, .comment-body")
        if not body:
            continue
        # Strip reply links
        for r in body.select(".reply, .comment-reply-link"):
            r.decompose()
        out.append({
            "author": author.get_text(strip=True) if author else "anonymous",
            "date": (date.get("datetime") if date else "") or (date.get_text(strip=True) if date else ""),
            "html": str(body),
            "depth": _comment_depth(c),
        })
    return out
```

### 9.2 Render as Markdown

Each comment becomes a block quote with a header line. Nested replies indent further:

```markdown
## Reader Comments

> **Anne Galloway**, 2018-05-16 14:22
>
> Thanks for the engagement. I think the point about Kuhn's "exemplars" deserves more emphasis…

>> **R. Smith**, 2018-05-17 09:05
>>
>> Anne, I'd push back on the second paragraph. The standard view is…

> **Pat Lin**, 2018-05-17 11:40
>
> One small correction: the citation should be *Structure*, p. 84, not p. 48.
```

The `>` per nesting level encodes thread depth. The bold author + date line keeps each comment scannable.

### 9.3 Strip the comment form, keep the comment list

The form (`#respond`, `#commentform`, "Leave a Reply" heading) was already removed in Phase 4. The comment **list** is preserved here. The "Pingbacks" and "Trackbacks" sub-list, if present, is typically promotional or self-referential — strip it (Phase 4 selectors handle it).

### 9.4 Comment count in YAML

Record `comment_count: <N>` in YAML so a future reader knows the comments section is N comments (and can spot missing ones if the markdown is later trimmed).

---

## Phase 10 — Quality checks before delivery

After producing each post's markdown, run these checks. Catch silent failures.

1. **Body length is non-trivial.** If the converted markdown body is under 200 words *and* the original HTML's article element had >2000 words, body extraction failed (the script picked up the wrong element). Re-locate the article.

2. **No Wayback artifacts remain.** `grep -E "wm-ipp|__wm|web\.archive\.org/web/[0-9]{14}|wbhack" "$MD_PATH"` should find nothing (excluding YAML provenance fields, which legitimately contain the archive URL).

3. **No WordPress chrome leaked.** `grep -E "sharedaddy|jp-relatedposts|wp-block-latest|nav-previous|comment-respond" "$MD_PATH"` should find nothing.

4. **No live-embed URLs in the body.** **This is the hard guard for the Phase 7 contract.** Run the embed-URL audit below; the build must abort on any failure. Note: the audit only flags **embedded resources** (auto-fetched at render time). Hyperlinks (`[text](https://...)`) are explicitly allowed regardless of where they point — including PDFs, datasets, audio, video, archives, anything. Hyperlinks are user-clicked, not embedded.

   ```python
   def audit_no_live_embeds(md_path: Path) -> list[str]:
       """
       Returns a list of violations. An empty list means the contract holds.
       The audit reads the Markdown body (NOT the YAML frontmatter, which
       legitimately contains live URLs in `original_url`, `archive_url`, etc.).

       Only EMBEDS are checked — things the renderer auto-fetches without the
       user clicking. Hyperlinks are out of scope: a `[text](https://x.pdf)`
       link is fine, because the reader has to click it to fetch it.
       """
       text = md_path.read_text(encoding="utf-8")
       # Strip the frontmatter
       if text.startswith("---"):
           _, _, body = text.split("---", 2)
       else:
           body = text

       violations = []

       # 1. Image embeds with live URLs:  ![alt](http...)
       for m in re.finditer(r"!\[[^\]]*\]\((https?://[^)]+)\)", body):
           violations.append(f"live image embed: {m.group(1)}")

       # 2. Reference-style image definitions:  [id]: http... (preceded by !)
       # Markdown reference images are rare in our output but possible.
       for m in re.finditer(r"^\s*\[[^\]]+\]:\s*(https?://\S+\.(?:png|jpe?g|gif|webp|svg|bmp|avif|tiff))\b",
                            body, flags=re.MULTILINE | re.IGNORECASE):
           violations.append(f"live image reference: {m.group(1)}")

       # 3. Raw HTML in the markdown body referencing live embedded assets
       for m in re.finditer(r"<img[^>]+src=[\"'](https?://[^\"']+)[\"']", body):
           violations.append(f"raw <img> with live src: {m.group(1)}")
       for m in re.finditer(r"<(?:video|audio|source|iframe|embed)[^>]+(?:src|data)=[\"'](https?://[^\"']+)[\"']",
                            body):
           violations.append(f"raw embedded element with live URL: {m.group(1)}")
       # srcset is the lazy-load trap — must be gone
       for m in re.finditer(r"srcset=[\"'][^\"']*https?://", body):
           violations.append("raw srcset with live URL(s) survived")

       # 4. Inline background-image
       for m in re.finditer(r"background(?:-image)?\s*:\s*url\(['\"]?(https?://[^'\")]+)",
                            body):
           violations.append(f"inline CSS background with live URL: {m.group(1)}")

       # NOTE: We do NOT audit `<a href="http...">` or `[text](http...)` —
       # those are hyperlinks, which are allowed by the Phase 7 contract
       # regardless of what file extension they point at.

       return violations
   ```

   In the script:

   ```python
   violations = audit_no_live_embeds(md_path)
   if violations:
       # Do NOT deliver. Print and abort this post.
       print(f"FAIL {md_path}: {len(violations)} live-embed URL(s) leaked")
       for v in violations[:10]:
           print(f"  - {v}")
       failed_posts.append((md_path, violations))
       continue
   ```

   If the audit fails, the most likely causes are: a lazy-load `srcset` that the localizer missed, an inline `<img>` inside a `<noscript>` block, an exotic embed plugin (Genially, Padlet) whose markup wasn't recognized, or markdownify preserving raw HTML the localizer didn't reach. Fix the localizer for that pattern, rerun, re-audit. Do not "just deliver it anyway."

5. **Footnote markers and definitions match.** Every `[^N]` in the body should have a corresponding `[^N]:` definition.

6. **Image references resolve.** Every `images/...` and `assets/...` path in the markdown should exist on disk. Every file in `images/` and `assets/` should be referenced (except `_missing.png`, the placeholder).

7. **YAML parses.** `python -c "import yaml; yaml.safe_load(open('$MD_PATH').read().split('---', 2)[1])"` succeeds.

8. **Spot-check.** Pick one post at random. Compare the rendered markdown against the original HTML rendered in a browser (or against the article's text content in BeautifulSoup). Confirm: same paragraphs in the same order, same number of headings, same number of images (counting placeholders), same number of comments preserved.

If any check fails, fix and re-check. Do not deliver markdown that fails any check without disclosing in `extraction_notes`. **Check 4 is the only one that should hard-abort the build** — the others can be disclosed as caveats; live-asset leakage cannot.

---

## Phase 11 — Output & handoff

Write each post's markdown to `/mnt/user-data/outputs/<slug>/<slug>.md` with `images/` beside it. Then proceed to Phase 12 to package, then surface with `present_files`.

For a single post:

```python
present_files(filepaths=[
    "/mnt/user-data/outputs/2018-05-15-on-paradigms.zip",
    "/mnt/user-data/outputs/2018-05-15-on-paradigms/2018-05-15-on-paradigms.md",
])
```

For a batch:

```python
present_files(filepaths=[
    "/mnt/user-data/outputs/posts.zip",
    "/mnt/user-data/outputs/posts/INDEX.md",
])
```

Your final message to the user should be **short** — see Operating discipline, Rule 6:

- One paragraph: how many posts, from which blog, over what date range, in what language.
- A note that the zip contains all markdown plus the `images/` folders and an `INDEX.md` (for batches).
- Caveats from `extraction_notes`: images that couldn't be fetched, posts with unusual chrome that needed manual selectors, theme idiosyncrasies, comments suppressed, etc.
- The `present_files` call.

**Do not paste the YAML, the post body, the comment list, or the index into your message.** Use `present_files`.

---

## Phase 12 — Package as a downloadable zip

Bundle the per-post folders so the user gets one round-tripping deliverable. Same pattern as the sister scholarly-pdf skill.

### 12.1 Single post

```python
import shutil
from pathlib import Path

def package_zip(out_dir: Path) -> Path:
    parent = out_dir.parent
    name   = out_dir.name
    base   = parent / name
    zip_path = shutil.make_archive(
        base_name=str(base),
        format="zip",
        root_dir=str(parent),
        base_dir=name,
    )
    return Path(zip_path)
```

### 12.2 Batch of posts

For a multi-post batch, package the wrapper `posts/` folder:

```python
def package_batch(posts_root: Path) -> Path:
    zip_path = shutil.make_archive(
        base_name=str(posts_root.parent / posts_root.name),
        format="zip",
        root_dir=str(posts_root.parent),
        base_dir=posts_root.name,
    )
    return Path(zip_path)
```

### 12.3 Build INDEX.md for batches

A simple table of contents pointing into each post folder:

```python
def write_index(posts_root: Path, processed: list[dict]):
    lines = ["# Converted posts", "",
             f"Generated {datetime.date.today().isoformat()}.",
             f"Source: {processed[0].get('blog_title', 'mixed')}.",
             f"Total: {len(processed)} posts.",
             "",
             "| Date | Title | Author | File |",
             "|------|-------|--------|------|"]
    for p in sorted(processed, key=lambda x: x.get("post_date") or ""):
        slug = p["slug"]
        lines.append(
            f"| {p.get('post_date','')} | {p.get('title','')} "
            f"| {p.get('author','')} | [{slug}.md]({slug}/{slug}.md) |"
        )
    (posts_root / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
```

### 12.4 Verification

After packaging:

```bash
unzip -l /mnt/user-data/outputs/posts.zip | head -40
unzip -l /mnt/user-data/outputs/posts.zip | wc -l
ls -la /mnt/user-data/outputs/posts.zip
```

Confirm the markdown files are present, each has a sibling `images/` folder, and the size is reasonable. If something is missing, regenerate; do not deliver a broken archive.

---

## Worked example: the skeleton of a finished post

```markdown
---
title: "On Paradigm Shifts in Science"
authors:
  - { family: "Galloway", given: "Anne", affiliation: "Victoria University of Wellington" }
post_date: "2018-05-15"
blog_title: "Crooked Scholarship"
blog_url: "https://crookedscholarship.example.com/"
categories: ["philosophy of science"]
tags: ["paradigms", "kuhn"]
original_url: "https://crookedscholarship.example.com/2018/05/15/on-paradigm-shifts/"
archive_url: "https://web.archive.org/web/20180520142733/https://crookedscholarship.example.com/2018/05/15/on-paradigm-shifts/"
archive_date: "2018-05-20"
language: "en"
comments_preserved: true
comment_count: 3
source_html: "snapshot.html"
source_html_sha256: "ab12…cd34"
extraction_date: "2026-04-26"
extraction_notes: |
  Wayback toolbar and injected scripts removed. Images downloaded from
  the original host (3/3 succeeded). Footnotes converted from sup/anchor
  pattern. 3 of 3 reader comments preserved.
---

# On Paradigm Shifts in Science

Last week's seminar circled back, again, to the same question: how does Kuhn's account of paradigm shifts hold up after six decades of normal science[^1]?

> A paradigm is what the members of a scientific community share, and, conversely, a scientific community consists of men who share a paradigm.
>
> — Kuhn 1962, 176

The standard objection — that "paradigm" was so loosely defined Kuhn had to publish a postscript narrowing the term to twenty-one distinct senses — has always struck me as missing the point…

![Diagram of pre-paradigm vs normal science](images/img-001.png)

*Figure 1. The transition from pre-paradigmatic competition to normal science under a settled exemplar.*

…and that's why I think the *Structure* framework remains generative rather than merely historical[^2].

## References

Kuhn, Thomas S. *The Structure of Scientific Revolutions*. Chicago: University of Chicago Press, 1962.

[^1]: For a contemporary defense, see Bird (2018), "Kuhn's Wrong Turning."
[^2]: I owe this phrasing to a conversation with R. Smith, July 2017.

---

## Reader Comments

> **R. Smith**, 2018-05-16 09:14
>
> Anne, this is good but I'd push the second paragraph harder. The standard objection isn't really about loose definition…

>> **Anne Galloway**, 2018-05-16 14:22
>>
>> Fair — though I think the postscript should be read as a clarification, not a retreat.

> **Pat Lin**, 2018-05-17 11:40
>
> Small correction: the citation should be *Structure*, p. 84, not p. 48.
```

That's the bar. Verbatim post body, intact footnotes, preserved comments, faithful metadata, archived images, original-URL provenance, archive-date provenance, citable.

---

## Common gotchas

- **Multiple `<article>` elements.** A WordPress home page or category archive includes multiple posts. The triage step in Phase 1 should reject these — a single archived blog post page contains exactly one substantive `<article>`. If multiple, the user gave you the wrong URL; flag it.
- **Themes that don't use `<article>`.** Older or custom themes may use `<div class="post">` only. The fallback selectors in Phase 3 handle this.
- **AMP versions.** `web.archive.org/web/.../amp/` URLs save the AMP variant of a post, which has its own chrome. The body extraction still works but the chrome selectors are different (`amp-img`, `amp-iframe`); add `amp-*` selectors to `CHROME_SELECTORS` if needed.
- **Wayback's "Save Page Now" overlay.** Recent Wayback snapshots include a banner overlay separate from the toolbar. Selector: `#donato`, `.donato-banner`. Already in the strip list.
- **Wayback timestamp embedded in non-URL contexts.** Sometimes the timestamp ends up in JavaScript variables that survive script removal. Check that the rewritten markdown has zero `\d{14}` 14-digit numbers attached to URLs.
- **`<noscript>` content** sometimes contains a non-Wayback fallback image src. Don't strip noscript blindly; check whether they contain useful image fallbacks first.
- **WordPress emoji shim** — every paragraph may have a tiny `<img class="wp-smiley">` for `:)` and similar. Strip these (already in `CHROME_SELECTORS`); they aren't post content.
- **Inline styles preserved by markdownify.** `style="…"` attributes don't survive Markdown conversion, but `style="text-align:center"` on a wrapper paragraph means a centered figure caption — detect and emit as `<p align="center">…</p>` if you want to preserve, or just discard for clean Markdown.
- **Self-closing `<br>` inside `<p>`** — these create soft line breaks. Markdownify converts to `  \n` (two spaces + newline, the Markdown soft break). Confirm this is what you want; for academic prose, hard breaks are usually fine.
- **Cookies / GDPR banners** captured in the snapshot. Strip with `#cookie-banner, .cookie-notice, .cc-banner, #cmplz-document` selectors.
- **Hyperlink targets that point at archived URLs of *other* archived pages.** Phase 2's `unrewrite` strips these to original URLs. The user may want the Wayback URLs preserved instead — make this configurable via a `--keep-wayback-links` flag.
- **Posts in non-English languages.** Markdown is encoding-agnostic; UTF-8 throughout. The body-location and chrome selectors work the same. The only thing that changes is the heading text patterns ("Notes" / "Bibliography") used in Phase 8 — extend with the appropriate translations if you encounter them.
- **Pages that are search results, tag archives, or category indexes** — these have `body class="search"` or `body class="archive"`. Detect early and refuse to process; tell the user to provide the single-post snapshot instead.
- **Encrypted HTML** — does not exist as a thing. If the file looks like binary or starts with `PK` (zip header), the user uploaded the wrong file.

---

## When to ask the user before proceeding

You can convert a single post or a small batch (≤10 posts) without asking — just deliver. For larger or ambiguous jobs, ask **once** before doing the work:

- Batches over ~20 posts: confirm the user wants the entire set, and confirm comment-preservation policy (default is yes, preserved).
- Foreign-language blogs: confirm the language and any non-English heading conventions for footnotes/bibliography.
- Mixed snapshots (different blogs in one folder): confirm whether to consolidate into one zip or separate per blog.
- Snapshots that fail Phase 1 triage (don't look like Wayback or don't look like WordPress): confirm the user wants to proceed with the heuristics anyway.

One question at most. Default to "yes, do the whole thing, preserve comments, the standard way" if the user doesn't reply.