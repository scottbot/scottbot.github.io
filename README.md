# scottbot.net

A portfolio, CV, and blog archive for Scott B. Weingart, built as a static
site with [Hugo](https://gohugo.io) — a single-executable site generator with
no dependency chain to rot. The design follows the CV's early-modern printing
style: EB Garamond with discretionary ligatures, oldstyle numerals, italic
ampersands, marginalia, manicules, and one colophon.
 

## The one-minute tour

| Folder | What lives there |
|---|---|
| `content/blog/` | the scottbot irregular, one folder per post (`index.md` + `images/`) |
| `content/works/` | books, articles, chapters, reports — same shape |
| `content/colophon.md` | the site's colophon (the CV carries its own) |
| `data/cv/` | **the CV, decomposed** — one YAML file per section |
| `assets/cv-prose/` | the CV's prose passages (biography, By The Numbers) |
| `data/workmap.yaml` | connects CV entries to their full-text pages |
| `layouts/`, `assets/css/`, `assets/js/` | the theme; you rarely need to touch it |
| `static/fonts/`, `static/images/` | EB Garamond and the site art |
| `static/cv.pdf` | the printed CV (August 2026 edition), served at `/cv.pdf` so the address that links in the wild already point at keeps working after migration |
| `corpus/` | **the source of truth**: the faithful markdown conversions (`corpus/Markdown/`, one folder per work), plus `List of Outputs.csv` and `weingartpubs.bib`. Lives inside the site so the whole apparatus migrates as one folder. The copy in `PhD\Outputs\Markdown` is now a frozen archive; edit this one. |
| `scripts/ingest.py` | the converter between `corpus/Markdown/` and `content/`. Its default mode is **additive and safe**: it converts only corpus folders that don't yet have a page, and never touches existing ones. See "add a new publication" below. Every correction ever made to the generated pages has been carried back into the corpus, so a full rebuild (`--force`) reproduces today's pages exactly. That guarantee only holds if future fixes go into the corpus too — edit the corpus copy (and its MANIFEST hash), not just `content/`, or your fix will vanish on the next rebuild of that page. |

## Previewing on your machine

1. Once: download `hugo_extended_0.164.0_windows-amd64.zip` from
   <https://github.com/gohugoio/hugo/releases/tag/v0.164.0>, unzip, and put
   `hugo.exe` in this folder (it is git-ignored).
2. Double-click **`serve.bat`**.
3. Open <http://localhost:1313>. The preview live-reloads as you edit files.

That's the whole toolchain. If Hugo ever vanishes from the internet, the copy
of `hugo.exe` on your disk keeps working forever.

## How do I…

### …add a line to the CV?
Open the matching file in `data/cv/` (e.g. `awards.yaml`, `talks-other.yaml`,
`appointments.yaml`) and copy an existing entry:

```yaml
- year: "2026"
  text: "A New Thing I Did. *Some Venue*, Some City."
  note: "award-winning"        # optional — appears in the right margin
  icon: manicule               # optional — prints a ☜ beside the note
  work: "folder-or-key"        # optional — links to a full text, via workmap
```

Formatting is Markdown: `*italics*`, `**bold**`, `[links](https://…)`.
Ampersands (`&`) automatically appear in italic, because they look swooshy
and neat. Year groups: give the year only to the first entry of a group and
`year: ""` to the rest, exactly like the printed CV.

Publications live in `data/cv/publications.yaml`, grouped in sections, each
entry using `citation:` instead of `text:`.

### …write a new blog post?
Create `content/blog/my-new-post/index.md`:

```yaml
---
title: "My New Post"
date: 2026-08-15
author: ["Scott B. Weingart"]
worktype: blog
venue: "the scottbot irregular"
---
The text of the post, in Markdown. Put pictures in an `images/` folder
beside this file and reference them as `images/whatever.png`.
```

It appears on `/blog/`, in the RSS feed, and (on wide screens) in the
reading pane.

### …add a new publication with full text?
Two ways.

**Via the corpus (recommended for converted works):** put the conversion in
`corpus\Markdown\<name>\` (one `.md` plus an `images/` folder, same shape
as its neighbors), then run

```
python scripts\ingest.py
```

The default mode only *adds*: it converts the new folder into
`content/works/<slug>/` (or `content/blog/` if the folder name starts with a
date), registers it in `data/workmap.yaml`, and leaves every existing page
completely untouched. To re-convert one existing page from its corpus source
(losing any hand-edits to that one page only):
`python scripts\ingest.py --only "<folder name>" --force`.

**By hand (fine for anything):** create `content/works/my-new-work/index.md`
with frontmatter modeled on any existing work (`citation:`, `doi:`, `venue:`,
etc.) and add a line to `data/workmap.yaml`:

```yaml
my-new-work: /works/my-new-work/
```

(Hand-added workmap lines survive every ingest run — including `--force` —
as long as the page they point at exists.)

Either way, use `work: "my-new-work"` on the CV entry to get the ❧ read
link. Pages carry a `bibkey:` field naming their entry in your Zotero
library's `weingartpubs.bib`, so the two stay cross-referenced; give new
works one too if they have one.

### …change the home page or colophon?
They're ordinary Markdown: `content/_index.md` and `content/colophon.md`.

## Publishing to GitHub Pages

One-time setup (GitHub Desktop is the no-command-line route):

1. Create a repository on GitHub (e.g. `scottbot/scottbot.github.io`, which
   must match `repoURL` in `hugo.toml` — that's where each work page's
   "create a pull request" link points), add this folder to it, commit, and
   push to the `main` branch.
2. On GitHub: **Settings → Pages → Source: GitHub Actions.**
3. Every push to `main` now rebuilds and publishes the site automatically
   (the recipe is `.github/workflows/deploy.yml`; Hugo's version is pinned
   there, so builds are reproducible for years).

> Windows notes, already handled in this copy: the repository's local git
> config sets `core.longpaths true` (a few corpus paths exceed Windows'
> old 260-character limit) and `.gitattributes` keeps every text file LF
> so no CRLF warnings appear. **If you ever clone this repository fresh
> onto another Windows machine**, run once, before cloning:
> `git config --global core.longpaths true`

### Custom domain (scottbot.net)
When you're ready: rename `static/CNAME.txt` to `static/CNAME`, push, and add
the DNS records GitHub's Pages settings page tells you to add. Until then the
site lives at `https://<username>.github.io/<repo>/`.

> Note: the deploy recipe asks GitHub Pages for the site's real URL and
> builds with it, so the interim `github.io` address works without touching
> `hugo.toml`. One honest caveat: the theme's internal links (nav, fonts,
> the reading pane, `data/workmap.yaml`) are written as root paths like
> `/works/…`, so the site must live at the *root* of its domain — a custom
> domain or a `<username>.github.io` repo, not `…github.io/<reponame>/`.
> A project-subpath deploy would need those paths reworked, not just
> `baseURL`.

## Design notes

Palette, per the CV's colophon: `#000000` most text · `#A6A6A6` headers &
footers · `#808080` marginalia · `#AA610D` headings & highlights · `#724109`
the name accent. Type is EB Garamond (variable, self-hosted, SIL OFL — see
`static/fonts/OFL.txt`) with `liga`, `dlig`, `hlig`, and `onum` on everywhere
(historical ligatures only fire on text containing ſ, so they cost nothing
outside the colophon). Every works page carries the LLM-conversion caveat
automatically via the template; add `caveat_extra: "…"` to a work's
frontmatter to insert an extra sentence into it. All the site's JavaScript —
the reading pane, the contents rail, the back-to-top manicule, the yielding
mobile header, and the table-overflow guard — is ~270 dependency-free lines
in `assets/js/reader.js`; everything degrades to ordinary links without it.
