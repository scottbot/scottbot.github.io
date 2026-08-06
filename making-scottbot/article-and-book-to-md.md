---
name: scholarly-pdf-to-markdown
description: "Convert a scholarly article, journal paper, monograph, dissertation, edited-volume chapter, conference paper, or academic book from PDF into a faithful, scholarly-grade Markdown artifact. Use whenever the user uploads an academic PDF, even when phrased casually ('turn this paper into markdown', 'convert this book', 'extract the text to quote it'), and for PDFs printed from scholarly HTML pages (JSTOR, PubMed Central, arXiv, etc.). The conversion is WORD-FOR-WORD with full typographic fidelity, not a summary: body, footnotes, captions, tables, lists, headings, equations, bibliography, and every italic/bold run preserved verbatim. Output is Markdown with YAML bibliographic metadata, an images/ folder, page anchors, a checksum MANIFEST, and a single-file .zip. Method: one PyMuPDF extractor, then prove fidelity with a QA battery plus a page-by-page visual review against rendered pages. Do NOT use for non-scholarly PDFs (forms, receipts, slides, memos), summary-only requests, or PDF creation (use the pdf skill)."
---

# Scholarly PDF → Markdown (absolute-fidelity)

## The cardinal rule

**This skill produces a verbatim transcription with complete typographic fidelity, not a summary.** Every word of the source — main text, footnotes, endnotes, captions, table cells, figure labels, list items, headings, bibliography — is reproduced exactly as it appears. Every *meaningful* typographic feature is carried across too: italic, bold, and bold-italic emphasis; super/subscripts; small caps; block quotes; lists and their nesting; tables; equations. The ONLY things removed are typographic noise that does not belong to the work itself: running heads, page numbers (repositioned as anchors, not deleted from the record), preprint/typesetting stamps, ligature glyphs (normalized to letter pairs), word-break hyphens at line ends, and the various Unicode whitespace characters (normalized to a regular space).

If you find yourself thinking "this paragraph is long, I'll condense it" — stop. That is a failure mode. The user wants a scholarly artifact they can quote, search, cite, and feed to other tools. Compression destroys the artifact. The same applies to emphasis: if a word is italic in the source and you render it roman, you have silently altered the work. **If it exists in the original, it must exist in the output.** Never judge a source feature "not worth preserving"; that is the author's decision, already made, printed on the page.

If the document is too long to reproduce in one response, **write it to disk progressively** — the artifact lives in a file, never in your reply.

---

## Operating discipline: never echo the document into chat

The single most common cause of *"Claude's response could not be fully generated"* on this task is the model trying to emit the converted text into its own reply. A 300-page book rendered verbatim is far past any single-response budget; once you start streaming it into your message, the response is killed mid-flight and the user sees a truncation error with nothing usable.

**The artifact lives on disk. Your reply describes the artifact; it never contains it.** These rules are load-bearing — the fidelity guarantee depends on never silently truncating, and the only way to never truncate on a 400-page book is to keep the document out of your response stream entirely.

1. **Use a script as the primary extractor.** For anything longer than a very short article (more than ~5 pages), write one Python script (e.g. `/home/claude/extract.py`) that does the entire pipeline — diagnostic, metadata, body, footnotes, figures, tables, index, YAML, packaging — and writes the Markdown to `/mnt/user-data/outputs/<basename>/<basename>.md`. Run it via `bash`. Your conversational reply contains only a short summary. The script's `stdout` does not compete with your reply for the response buffer, so the whole job costs you only the script source plus a one-paragraph wrap-up.

2. **Append, don't accumulate.** If a workflow requires chunked processing (per-chapter, large books), open the output file in append mode and flush after each chunk. Never build a multi-megabyte string in memory and emit it in one shot. Append-as-you-go also preserves partial progress if the script fails mid-run.

3. **Do not paste the converted text into your message.** Not the YAML. Not the abstract. Not the bibliography. Not a "preview snippet." Use `present_files` and let the user open the file. A snippet looks polite but costs tokens against the budget; on a long book that snippet tips you over.

4. **Do not `view` the finished file in full** just to inspect it — that pulls the whole document into context and tempts you to echo it. Use shell tools that summarize: `wc -l -w`, `head -40` (YAML peek only), `grep -c '^## '` (heading count), `ls -la images/`. For body spot-checks, `view` only small line ranges.

5. **Process very long books in resumable passes.** For 300+ pages, split the script into idempotent phases invoked separately (`--phase metadata`, `--phase images`, `--phase body --pages 1-100`, …, `--phase notes`, `--phase package`). Each writes a small stdout line (`OK: appended pages 1-100`) and is independently retryable. A `progress.json` next to the markdown records which phases completed.

6. **Cap your final reply at roughly 150 words:** one paragraph of what you produced (type, length, language), the paths, any caveats from `extraction_notes`, and a `present_files` call. If you are writing a third paragraph or pasting YAML fields, stop and delete.

7. **If the truncation error already happened, restart in script mode.** Do not "continue from where you left off" by emitting the next chunk into your next reply — that retriggers the failure. Move the work into a script that writes to disk.

8. **Detection signal:** if you are about to type a code fence in your reply containing more than ~50 lines of converted content (body, YAML, bibliography, table) — you are about to fail. Redirect it into a file write inside the script.

### Anti-patterns

| Anti-pattern | Why it fails | Do this instead |
|---|---|---|
| `create_file` with the entire converted markdown as `file_text` | the argument is part of your output budget | run a Python script that writes via `open(...).write()` |
| `cat output.md` to "check" it | whole file pulled into context; next reply may echo it | `wc`, `head`, `tail`, `grep -c`, targeted `view` ranges |
| Quoting "just the abstract" in the reply | looks small; on the next book it tips you over | `present_files` only |
| Emitting `<!-- page N -->` progress updates into chat | same problem at smaller scale, repeated | silent until done; one summary at the end |

---

## When this skill applies

A PDF of: a journal article (single- or multi-column); a full book or monograph (hundreds of pages); a book chapter from an edited volume; a dissertation or thesis; a conference or working paper; a "Print to PDF" of a scholarly HTML page; or a scanned book/article requiring OCR.

## The two failure modes that matter most

Every technique below exists to prevent two specific, severe failures. They are worse than any formatting blemish because they are invisible without an audit, and they destroy the artifact's trustworthiness:

1. **Silent content loss** — a paragraph, list item, footnote, caption, table cell, or quote that exists in the source but is missing from the output. In practice the hard content-loss bugs are almost never a clean "page skipped." They are caused by **one block wrongly absorbing or displacing an adjacent one**: a figure crop that swallows the paragraph below it, a table detector that eats the prose beside it, a blockquote band that consumes a following body line, a code-block guess that drops the line after it. Every structural detector you add (table, matrix, code, list, blockquote, caption) is a potential content-loss vector when it misfires on prose — the bug is rarely in the detector's happy path, it is in what the detector does to the paragraph *next to* it.

2. **Invented content** — text in the output that is NOT in the source: a synthesized "Figure Index" heading the book never had, a chapter grouping you inferred, an "(unnumbered note)" container a recovery heuristic created to "preserve" some text. **Meta-lesson:** when a heuristic "preserves" content by inventing a container, be suspicious — the content almost always belongs to an existing structure, and the fix is to *route it there*, not create a new home for it.

Build the audits in Phase 9 FIRST and run them after every change. They are how you know a fix did not cause a regression. Treat every audit miss as real loss until you have proven it a benign false-positive (a reformatted TOC, a known URL/proper-noun artifact).

## Dual-source architecture (when the publisher ships more than the PDF)

Sometimes the user has more than one representation of the same work — e.g. a publisher's clean per-page `.txt` pre-press files plus a page image or assembled PDF, or a publisher HTML page (Cambridge Core, Emerald) plus the PDF. When you have two sources, **split their roles** instead of picking one:

- **Clean text (publisher `.txt` or canonical HTML) is ground truth for WORDS.** Never take body wording from OCR of a page image when a clean text layer exists — the publisher text is correct; OCR is not. The HTML/`.txt` gives the exact prose, the heading hierarchy, and intact italic markup.
- **The PDF / page image is ground truth for STRUCTURE and FIGURES** — font sizes and bold/italic flags, x/y geometry, indentation, the printed page grid (for page anchors), the bibliography and footnote *definitions* that static HTML often omits, and the figures themselves (cropped from the page; a vector figure absent as a raster must be rasterized from the PDF).
- **Map each PDF text block to its clean-text lines** by matching the first line, then render from the clean text: the block tells you the *kind* (heading / body / quote / caption / footnote / code) and *position*; the clean text gives the *exact words*. Record in `extraction_notes` which source supplied what (e.g. "body from Cambridge HTML; footnote defs, bibliography, and Fig. 14 from the PDF").

**HTML-primary variant (publisher HTML + PDF).** When the cleaner source is a publisher HTML export (Cambridge Core, Emerald, Springer), make the HTML the body master and reach into the PDF only for what the static HTML omits. In practice the HTML carries the running prose, heading hierarchy, figures/captions, block quotes, inline italics, and footnote/citation *markers* — but **often omits the footnote/endnote definitions, the full bibliography, and any vector figure** (which you rasterize from the named PDF page). Three HTML-specific cautions learned on a real Cambridge Element:
- **Exclude publisher boilerplate** that `pdftotext` would include but the work does not: title/copyright/series pages, the table of contents if it is navigation chrome, and a per-page running footer (e.g. a repeated "Published online by …" DOI line). Word-count parity will sit around ~92% precisely because this boilerplate is correctly dropped — note that in `extraction_notes` so the gap is not mistaken for content loss.
- **Page anchors from HTML markers are positionally accurate but the NUMBER may drift** a page or two from the printed folio, because the HTML sometimes omits a marker for full-page figure spreads. Say so in `extraction_notes`: use the anchors for navigation/grep, cite by the PDF's printed folio.
- **Find the abstract where it actually is.** A regex that assumes the abstract is on page 1 will silently produce an empty field when the journal/book places it on a later page (one real article had it on PDF page 5). Verify the abstract field is populated; an empty `abstract:` is a fidelity gap, not a formatting nicety.

If there is only an image-only scan with no clean text, OCR is unavoidable — but then verbatim fidelity is best-effort, you must **correct obvious OCR errors against the visible source** (e.g. `API` mis-read as `AP/`, `Figure 1` as `Figure I`), and you must say so in `extraction_notes`. Fidelity is to the *source work*, not to the OCR's mistakes.

## The output you produce

For an input `paper.pdf`, produce in `/mnt/user-data/outputs/`:

```
paper/                   ← working folder
├── paper.md             ← the converted markdown with YAML frontmatter
├── MANIFEST.txt         ← sha256 + byte size of every file (for citation/archival)
└── images/              ← figures, plates, cropped equations (only if any exist)
    ├── fig-001.png  (or fig-3.1.png — see naming below)
    └── eq-145-1.png
paper.zip                ← single-file deliverable: zips paper/ above
```

`paper.zip` is the **primary download**. The unzipped folder is also kept on disk so the user can browse the markdown without unzipping. For very long books you may add a `chapters/` directory, but always also produce one combined `paper.md` so the verbatim record is in a single file. When you finish, call `present_files` with the zip path **first** and the markdown path second.

---

## Phase 1 — Triage the PDF

The right strategy depends on which of four types this is. Run a diagnostic before extracting anything.

```bash
pdfinfo paper.pdf                         # page count, metadata, PDF version, Encrypted?
pdftotext -layout -f 1 -l 3 paper.pdf -   # is there an extractable text layer?
pdfimages -list paper.pdf | head -20      # embedded raster images?
pdffonts paper.pdf | head -20             # fonts embedded? identity-H?
```

**First, confirm the file is actually a PDF.** A surprising number of "scholarly PDFs" delivered by repositories or publishers are something else wearing a `.pdf` extension — most often a **zip archive of per-page assets**. Run `file paper.pdf` and check the magic bytes; if `pdfinfo` errors or `file` reports a Zip/archive, `unzip -l paper.pdf` and look inside. These containers frequently hold, per page, a JPEG raster **plus a parallel `.txt` typesetter dump** (and sometimes a `manifest.json` with structured metadata, or per-line bounding boxes). That `.txt` is the publisher's clean text — **use it as ground truth for words** (far better than OCR), use the JPEGs as ground truth for figures and structure, and note in `extraction_notes` that the source was a zip container, not a born-digital PDF. Missing this detection leads to needlessly OCRing pages whose clean text was sitting right there.

Then **rasterize and actually look** at representative pages — page 1, one interior page (~5 or 10), and one near the end (catches header/footer patterns, footnote style, reference formatting):

```bash
pdftoppm -jpeg -r 150 -f 1 -l 1 paper.pdf /tmp/triage
```

`view` the resulting images. **Looking at the page is not optional** — layout, columns, footnote style, and the exact form of running heads are only visible in the rendered image, not in the text dump.

| Type | Signature | Strategy |
|---|---|---|
| **Digital-native (typeset)** | `pdftotext` returns clean text; fonts embedded; multi-column likely | PyMuPDF line-level reconstruction (below) |
| **PDF-of-HTML** | single full-width column; URL/timestamp footer; web fonts; nav strip on p1 | PyMuPDF; reading order already linear; strip browser chrome |
| **Scanned (image-only)** | `pdftotext` returns ~nothing; one big image per page | OCR with Tesseract at 300 DPI (Phase 7) |
| **Scanned with OCR layer** | both an image AND imperfect text | treat as digital-native, but re-OCR pages where extraction is garbled |
| **Word/cairo-derived ("Print to PDF")** | producer is a word processor or a browser print; paragraph breaks collapse; headings are inline bold/italic runs not blocks; **hyperlink targets are lost** | reconstruct paragraph/heading boundaries from inline font runs; render lost links as `[anchor](#)` placeholders and note it |

**Engine-specific gotchas worth knowing before you start:**
- **OCR engines (ABBYY) often assign headings a *smaller* numeric font size than body text** — so on an OCR'd PDF, detect headings by font *face* (e.g. `TimesNewRoman-Bold`, `AngsanaNew-Bold`) rather than by size, or every heading will be missed.
- **A DjVu twin or a second OCR pass is a cross-check, not a competitor.** When the user supplies both a scanned PDF and a `.djvu` (or asks you to re-OCR), extract text from each, compare per page, and take the more accurate version glyph-by-glyph against the rendered image — fidelity is to the printed source, not to either OCR. (`djvutxt`/`ddjvu` from `djvulibre-bin`.)
- **A two-source agreement is a strong fidelity signal.** When an HTML full text and the PDF agree to ~1.0 word-parity, you can trust the body; when they diverge, the divergence localizes exactly what to inspect.

For a book, ask once whether the user wants the whole thing or specific chapters; default to the whole thing, but extract a sample (front matter + first chapter) and confirm the format meets their needs before doing 400 pages.

### 1.1 Inventory fonts, flags, and colors FIRST

Before writing any extraction logic, inventory exactly what the PDF uses. This tells you how to detect emphasis, headings, footnotes, and which fonts are noise. This single diagnostic prevents most fidelity bugs:

```python
import fitz
from collections import Counter
doc = fitz.open("paper.pdf")
fonts, flags, colors = Counter(), Counter(), Counter()
for page in doc:
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0: continue
        for l in b["lines"]:
            for s in l["spans"]:
                if not s["text"].strip(): continue
                fonts[s["font"]] += 1
                fl = s["flags"]
                if fl & 1:  flags["superscript"] += 1
                if fl & 2:  flags["italic"] += 1
                if fl & 8:  flags["mono"] += 1
                if fl & 16: flags["bold"] += 1
                colors[s.get("color", 0)] += 1
# print fonts (most_common), flags, colors
```

Read the output and decide:
- **Which font names mean italic / bold / bold-italic** (usually the name contains `Italic` / `Bold`). Build `is_italic()`, `is_bold()`, `is_code()` (monospace: Courier/Mono) helpers from the actual font names, not assumptions.
- **The modal body font size** (the heading detector keys off this).
- **Which fonts are noise**: a sans-serif (Helvetica) at a tiny size in a white color is almost always a preprint/typesetting stamp — filter it. A `Symbol`/`TimesNewRoman` font confined to a few pages is usually math inside an equation region (which you will crop as an image).
- **Whether a superscript *flag* ever fires.** Often it does NOT; footnote markers must then be detected by *size* (a span much smaller than body text), not by the flag.
- **Whether any meaningful color exists** (e.g. blue hyperlinks). Usually only near-black body text plus white stamps — confirm there is nothing colored carrying meaning.

---

## Phase 2 — Recover bibliographic metadata

This drives the YAML frontmatter and distinguishes a scholarly artifact from a text dump. Pull from every source and reconcile, preferring the most authoritative.

### 2.1 Sources, most reliable first

1. **DOI / arXiv ID / ISBN in the PDF**, resolved via Crossref / arXiv / Open Library if you have web access. By far the most reliable — prefer it over anything scraped from page 1.
2. **Embedded PDF metadata** (`pdfinfo`, `doc.metadata`). Often right for articles, often blank/wrong for books.
3. **The first one or two pages** (title page, copyright page, masthead). **Read these as rendered images** — layout matters, and on many books the title page is a rasterized image whose text is not in the text layer at all. Author names in particular are often only readable from the title-page image; **never hand-write the author list from memory** (a real failure mode that dropped a co-author on one book — render the title page at ~130 dpi and read it).
4. **The running header** (journal, volume, year).
5. **The last pages** for colophons.

### 2.2 Find an identifier

```python
import re
hay = doc[0].get_text() + (doc[1].get_text() if len(doc) > 1 else "") \
    + doc[-1].get_text() + (doc[-2].get_text() if len(doc) > 1 else "")
doi   = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', hay)
arxiv = re.search(r'arXiv:\s*(\d{4}\.\d{4,5}(v\d+)?)', hay)
isbn  = re.search(r'ISBN[:\s-]*((?:97[89][-\s]?)?(?:\d[-\s]?){9}\d|(?:\d[-\s]?){9}[\dX])', hay)
```

Strip trailing punctuation from a captured DOI. If found and web access is available, fetch Crossref (`https://api.crossref.org/works/{doi}`) for authoritative title, authors, journal, volume, issue, pages, year, publisher, license — **prefer Crossref over page-1 scraping on conflict**. arXiv: `https://export.arxiv.org/api/query?id_list=<id>`. ISBN: `https://openlibrary.org/api/books?bibkeys=ISBN:<isbn>&format=json&jscmd=data`.

If no identifier exists, transcribe from the rendered first page (title, authors with affiliations matched by symbol, abstract, keywords, journal line) for articles; from the title page and its verso (copyright year, ISBN, edition, place) for books.

### 2.3 YAML frontmatter schema

Omit fields you genuinely cannot determine — **never invent them**. Compute the SHA-256 so a future reader can prove the markdown corresponds to the exact PDF bytes.

```yaml
---
# --- identity ---
title: "The Structure of Scientific Revolutions"
subtitle: ""
authors:                                  # ordered as in source; read books' from the title-page image
  - { family: "Kuhn", given: "Thomas S.", affiliation: "University of California, Berkeley", orcid: "", corresponding: false }
editors: []
translators: []
contributors: []
# --- publication ---
publication_type: "book"                  # article | book | book_chapter | thesis | preprint | report | conference_paper
container_title: ""                       # book for a chapter; journal for an article
journal: ""
volume: ""
issue: ""
pages: ""
edition: ""
publisher: "University of Chicago Press"
publisher_place: "Chicago"
series: ""
event: ""                                 # conference papers
# --- dates ---
issued: "1962"
year: 1962
original_publication_year: 1962           # if a later edition
# --- identifiers ---
doi: ""
isbn: ""
issn: ""
arxiv: ""
pmid: ""
oclc: ""
url: ""
# --- descriptive ---
abstract: |
  Verbatim abstract under a literal block scalar so newlines and quotation marks
  survive. Do not paraphrase.
keywords: ["paradigm shift", "philosophy of science", "normal science"]
language: "en"                            # ISO 639-1
license: ""                               # e.g. "CC BY 4.0" if stated
# --- provenance ---
source_pdf: "paper.pdf"
source_pdf_sha256: "ab12...cd34"          # hashlib.sha256(open(path,'rb').read()).hexdigest()
page_count: 174
extraction_date: "2026-06-15"
extraction_tool: "claude scholarly-pdf-to-markdown skill"
extraction_notes: |
  Digital-native PDF, single-column. No OCR. Footnotes continuous, numbered
  globally. Three display equations cropped as images. Figure captions set in
  italic by the publisher; italic book titles within captions rendered roman to
  stay distinct. Running heads and preprint stamps removed. MANIFEST.txt included.
  IMPORTANT: extraction_notes MUST NOT contain the literal preprint strings you
  filtered (e.g. a publisher job code), or the leak-detection QA check will fire.
---
```

---

## Phase 3 — Extraction engine and the line-level principle

Use **PyMuPDF (`fitz`)** as the primary engine — per-span bounding boxes, font names, font flags, fast image extraction. (`pip install pymupdf pillow pdfplumber pytesseract --break-system-packages` as needed; `pdfplumber` for tables, `pytesseract` for OCR.)

**Reconstruct from individual lines/spans, not from PyMuPDF "blocks."** Block grouping is unreliable on list-, footnote-, and multi-column pages: a single "block" can hold the end of one paragraph and the start of the next list item, scrambling reading order. The robust pipeline is:

1. **Collect line records** with geometry (x0, y0, x1, y1), dominant font size, and the full span list (so emphasis survives). Filter out running heads / page numbers / preprint stamps here (Phase 4.3).
2. **Sort by (block-top, block, y, x)** — order blocks by their topmost line's y, but keep each block's lines contiguous. A pure y-sort interleaves two vertically adjacent paragraphs whose lines overlap in y.
3. **Group lines into typed items** (heading, body paragraph, list, code, block quote, figure, table, footnote-def, sidebar, equation) using the geometric and font signals below.
4. **Render each item**, preserving emphasis at the *paragraph* level (Phase 4.5).
5. **Stitch across pages** (Phase 4.7) and **reposition floats** so a float never splits a sentence.

`page.get_text("dict")` gives the rich structure; use it.

---

## Phase 4 — Body text in correct reading order

The pitfalls: multi-column flow, running heads contaminating the text, hyphenated line-ends, sentences split across pages, footnotes interleaving with body.

### 4.1 Columns

Detect columns from a histogram of span `x0` values. Two prominent clusters → two columns: split at the midline, sort each column by y independently, emit left then right. **Never interleave columns**, even when the right column's first line starts higher than the left's. Three columns (reference works) generalize the histogram. PDF-of-HTML is single-column → plain top-to-bottom. **Stitch sentences that break across the column boundary**: the last line of the left column often continues into the first line of the right column (and the last line of a page's right column into the next page's left) — apply the same not-a-terminator continuation rule you use across pages, so a sentence split by the column gutter reads continuously.

### 4.2 Paragraph breaks

Line gaps are often a uniform leading (e.g. 13pt) and therefore **cannot** distinguish paragraphs. The reliable signal is usually **first-line indent**: a body line whose x0 is ~10–18px past the body margin starts a NEW paragraph; a line at the margin continues the current one. Block boundary + sentence-end, and unusually large vertical gaps, are fallback signals. Measure the indent on the actual PDF; do not assume.

### 4.3 Strip running heads / footers (but keep the page number as an anchor)

Detect empirically. Collect the topmost and bottommost line of every page; normalize by replacing digit runs with a placeholder; if the same normalized string recurs on more than ~30% of pages it is a running head/footer — drop it from the body. **Critical false-positive trap:** strip only the *exact* running-head line (a full-line regex at body size), NEVER any paragraph that merely mentions the title. A body sentence like "The *Historian's Macroscope* is part of this conversation" must be KEPT. Also strip preprint/typesetting stamps (publisher job codes, `.indd` filenames, `M/D/YY H:MM AM` timestamps), which are often a tiny sans-serif span in white or near-edge — filter by size + font + color + position, not by content alone.

**Publisher-specific chrome you will meet** — each is noise, not the work; strip it and note it in `extraction_notes`:
- **Springer offprint cover pages and the "Author's personal copy" running head** (the first pages of a Springer offprint are a generated cover; the phrase repeats as a header).
- **Wiley rights-notice running *vertically* along the page edge** (a sideways block on conference/journal pages) — it appears in the text layer as an out-of-flow column; drop it.
- **A repeated per-page download/footer stamp**: a DOI line ("…Published online by Cambridge University Press"), a "Downloaded from … by …" watermark, a Carnegie-Mellon/library download stamp, a PNAS "Downloaded at …" line. These recur on every page and belong to none of the text.
- **Web/CMS chrome on saved HTML pages** (VICE/Motherboard, WordPress, news sites): sharing widgets, in-article ad slots, embedded video players, "related posts" sidebars, comment forms, the site footer. Strip all of it; keep only the article.
- **The page-1 author/affiliation block**: it is captured into the YAML, so replace it in the body rather than duplicating it as prose.

**Collapse a heading that wraps to two physical lines into one** before emitting it — a `## Section title that ran\nonto a second line` must become a single heading line, or the second half leaks into the body as a stray paragraph.

### 4.4 Headings by font

Compute the modal body font size across the document. A span is heading-like when it is substantially larger (≈ ≥1.15×) OR set in the heading font (e.g. Bold/BoldItalic at body size on a short line with no terminal period). Quantize heading sizes/styles into levels: book chapter title → `#` or `##`; section → `##`/`###`; subsection → `###`/`####`. For an article, the paper title is `#` (page 1 only), sections `##`, subsections `###`. Headings rendered as `#…` are NOT emphasis — do not also wrap them in `*`/`**`.

### 4.5 Emphasis — render at the PARAGRAPH level, and get the boundaries right

This is where most fidelity is won or lost. Rules:

- **Accumulate a paragraph's spans across all its lines, then render once**, so a multi-line italic/bold run becomes ONE `*…*`, not fragmented `*a* *b*`. Classify each span from its font: bold-italic → `***`, bold → `**`, italic → `*`, monospace → `` ` ``, else roman. Concatenate consecutive same-style spans before wrapping.
- **Place markers outside leading/trailing whitespace**: `*word* ` not `*word *`. Shift punctuation that opens a run (`fault` + italic `: these…`) outside the markers so you never get a broken mid-word marker.
- **Normalize, but make the merge boundary-aware.** Merge adjacent same-style runs split across line renders (`*a* *b*` → `*a b*`; `**a** **b**` → `**a b**`; `***a*** ***b***` → `***a b***`). **The single-`*` merge MUST NOT collapse a closing italic `*` with the opening `**` of an adjacent bold run** — `*Journal* **3**(3)` must stay intact, not become `*Journal  *3**`. Guard with lookarounds so both matched markers are exactly the same length:
  ```python
  for mk in ("***", "**", "*"):
      e = re.escape(mk)
      prev = None
      while prev != text:
          prev = text
          text = re.sub(rf"(?<!\*){e} {e}(?!\*)", " ", text)
  ```
  This italic-then-bold collision is a whole class — it shows up wherever an italic journal/book title abuts a bold volume number (very common in footnotes/bibliographies).
- **Factor a bold-italic run abutting a bold run** so `***k*****-partite**` (bold-italic `k` + bold `-partite`) becomes `***k*-partite**` (bold throughout, italic only on `k`); collapse any run of 4+ asterisks to `**`.
- **Escape literal Markdown actives** in roman prose: a literal `*`, `_`, or `\` in the source text must be escaped (`\*`) so it does not collide with the emphasis markers you add. Never escape inside code spans.
- Smart quotes (' ' " "), em/en dashes (— –), and ellipsis (…) are **kept as-is** — do not "dumb them down." Non-breaking and other Unicode spaces become regular spaces.

**Context determines how nested emphasis renders.** Three cases recur:
- **Body prose:** italic source → `*italic*`, bold → `**bold**`, bold-italic → `***both***` (normal Markdown).
- **A whole-italic caption** (publisher sets all captions in italic): wrap the whole caption in `*…*`, but render a source-*italic* run (e.g. a book title) as **roman** so it stays visually distinct inside the italic caption — `*Fig. 3.1* War and Peace *as a word cloud.*`. A source-*bold* run stays bold. A lone trailing-punctuation segment must not become its own `*.*` — attach it to the preceding run.
- **A NOT-whole-italic list** (e.g. the front-matter figure list): a source-italic title renders as normal `*italic*`.

Audit emphasis fidelity at the end (Phase 9): compare every italic/bold span in the source against the markdown. Expect the only "misses" to be headings (rendered as `#…`) and equation text (cropped as images).

### 4.6 Dehyphenate line-ends

When a line ends with `-` and the next begins lowercase, the hyphen is almost always a word-break artifact: drop it and join. Keep the hyphen if the stem before it is a proper noun (uppercase) or contains a digit (`x-coordinate`), or if the joined form would be a real compound (`well-being`). Convert soft hyphens (U+00AD, and the 0x02 some publisher exports use) to a real `-` in your `clean()` step *before* the join logic, or you get "pro vide" instead of "provide."

**Trap: soft hyphens are NOT corruption.** If you filter "garbage" lines by counting control characters, EXCLUDE soft hyphens (U+00AD, 0x02) from that count — a naive "drop lines with ≥3 control chars" rule silently deletes any normal paragraph that happens to wrap on several hyphenated breaks. Only genuinely anomalous control bytes (e.g. 0x01, 0x03–0x06) indicate the custom-font garbage that needs recovery. This single mis-filter dropped whole paragraphs book-wide on a real conversion.

**Trap: the consecutive-hyphen loop bug.** When two adjacent lines BOTH end in a word-break hyphen, a dehyphenation loop that does `i += 2` after a join skips the second hyphenated line and leaves it unstitched. Advance by one and re-test the newly joined line, so a run of several hyphenated line-ends all stitch.

**Restore diacritics that extraction or OCR strips.** Some text layers and OCR passes drop or mangle accents (Börner→Borner, Glänzel→Glanzel, Luís→Luis, Akadémiai Kiadó→Akademiai Kiado, durée→duree). Restore the correct accented form against the rendered page — author names and non-English terms must carry their diacritics, and a Crossref author list is an authoritative reference for spellings.

### 4.7 Stitch sentences across pages

The join between page N and N+1 is the danger zone — page N often ends mid-sentence. Rule: if the last non-blank character of page N is **not** a sentence terminator and not the end of a heading, page N+1's first content paragraph continues it — concatenate. **`ends_sentence()` must strip trailing emphasis markers** (`…scholarship.*`) before checking for terminators, or cross-page stitching wrongly merges the next paragraph. A float (figure/table) lying between two wrapping paragraphs must be pushed past the continuation so it never splits the sentence (Phase 5/floats).

### 4.8 Page anchors

After every page boundary insert an invisible HTML comment that survives in the source for grep/citation but does not render: `… end of the argument. <!-- page 14 -->`. For books with printed folios, use the *printed* page number, not the PDF's sequential index. If the user explicitly asks for visible markers, switch to `[p. 14]`; the default is the invisible comment.

---

## Phase 5 — Special elements

### 5.1 Footnotes (per-page) — the part that needs the most care

Detect by: smaller font than body, near the page bottom, often a leading number span. Convert to Markdown footnote syntax. **Footnote-marker integrity is non-negotiable**: every marker placed at the EXACT source superscript position, and full marker↔definition parity. NEVER append an unplaced marker to a nearby paragraph "to achieve parity" — a wrong position is worse than an honest gap.

- **Markers in body:** a tiny span (size < body·0.78) of digits, often with NO superscript flag — detect by size. When it sits within a body line, the paragraph renderer emits `[^N]` inline at that position. **Guard against version strings and filenames:** a digit that is part of a token (`D3.js`, `v1.2`, `3D`, `MP3`) is NOT a marker. The discriminator is what immediately precedes/follows the digit: reject when a letter immediately *precedes* the digit (`D3`) or when the digit is followed by a lowercase letter or by `.<alnum>` (`.js`, `.2`); but ALLOW a digit that follows sentence punctuation/space and is followed by whitespace, or directly by a *capital* letter — the latter is a real marker glued to the next sentence (`attribution and 36Susan`, `successful.38Conferences`). Getting this boundary wrong either mangles `D3.js` into `D[^3].js` or silently drops ~every glued marker — both happened on real books.
- **Isolated marker lines:** PyMuPDF often puts a marker in its own tiny line at a weird x, sometimes as `"73"`, `"73:"`, or `"275 An"` (number + the next paragraph's first word, all superscript). The decisive fix: in a pre-pass, **merge each isolated marker line into the BODY LINE it shares a y-row with**, appending a synthetic marker span — this places the marker exactly where the superscript visually sits. As a backstop, a marker that still lands at the *start* of a paragraph belongs to the *end* of the previous one.
- **Definitions (page foot):** a def START has a small leading-number span at the left margin (x0 ≤ ~145); a continuation line that merely begins with a digit (`135.1, 159…`) must NOT start a new note. **Strip the leading marker from the def text** so it reads `[^N]: <text>`, not `[^N]: [^N] <text>`.
- **Defs wrap across pages:** thread the open definition from page to page (return it from per-page processing, pass it into the next). Do NOT flush an open footnote when a body line appears — the footnote zone is at the page bottom but comes *after* the body in reading order, so flushing on body lines truncates the note. Only a NEW def-start flushes the previous one.
- **No timestamp leak:** never append a date/time-stamp line as a footnote continuation.
- **Renumber globally** if the source resets per chapter or per page, preserving the original printed location so the printed origin is recoverable: `[^47]: (ch. 3, n. 12) …` for a book, or `[^47]: (p. 259, n. 3) …` when numbering resets per page. A short note at the top of the `## Notes` section can explain the global-renumbering scheme. Symbols (`*`, `†`, `‡`) convert to numbered footnotes; record the original symbol in the note text. Put definitions either at chapter ends under `### Notes` or all at the end under `## Notes` (the safe default when numbers reset per chapter).
- **Very small superscripts (≈6–7pt) are still markers.** Some documents set footnote/endnote reference numbers as tiny as 6.6pt — detect by the size ratio to body, not an absolute threshold, or you will miss every marker in a document with small superscripts.

### 5.2 Endnotes

Detect by a "Notes"/"Endnotes" heading followed by a numbered list keyed to superscripts earlier in the text. Convert to `[^N]` markers in place and definitions under a final `## Notes` (or per chapter), preserving chapter context in the note text.

### 5.3 Tables

Use `pdfplumber.extract_tables()` first. Convert each to GitHub-flavored Markdown, positioned where the table appears in reading order, caption directly above. **Be deliberate about three sub-cases:**
- **Real text-layer tables** (gridded, body-font): reconstruct as GFM. Cluster cells into columns by x0; use a **tight cluster threshold** (~14px, not ~24px) so narrow adjacent columns (e.g. `ID | Label`) don't merge into one cell. Drop all-empty columns. Promote a fully-populated first row to the header when the supplied header is blank. **Preserve an empty diagonal / upper-triangular structure** (an adjacency matrix renders with empty cells, not zeros you invented).
- **Rendered-image tables** (a screenshot or a color-coded spreadsheet with NO text layer): these are figures — crop and embed as an image; do NOT try to extract their text, and confirm no embedded text leaked into the prose.
- **`pdfplumber` returns garbage** (merged cells, rotated text): rasterize the table region (`page.get_pixmap(clip=bbox)`), save to `images/table-NN.png`, embed it, and **add a note above the image** that the source table could not be reliably converted to text. **Never silently drop a table.**

**Two cautions, both learned the hard way:**
- **A table detector that misfires on prose causes content loss.** An adjacency-matrix or header-row detector keying on "capitalized words = node labels" will match a sentence full of proper nouns ("Lamar, James Webb, and James Treat…") and turn prose into a garbled table, dropping the real text. Require clean single-token column labels (no trailing comma/paren) AND a data portion that is mostly numeric/money values before emitting a table; after adding any table detector, re-run the content-loss and reverse audits (Phase 9) — the regression is in what it does to the neighbouring paragraph, not the table itself.
- **Header-row data tables in body font.** A header like `topicId rank docId filename` followed by rows whose leading (ncols−1) tokens are numeric and whose final column (a filename/title) contains spaces is a real table the font can't flag — detect 3–6 clean header names followed by numeric-leading rows, and let the last column absorb the remainder.
- **When a multi-part table will not reduce cleanly to one GFM table** (e.g. several small topic-weight tables with labels interleaved, or matrices with shaded diagonals and spanning headers), and forcing it produces duplication/scrambling, it is better to leave the content as faithfully-rendered prose/preformatted text than to emit a corrupted table — **as long as no words are lost.** A correct prose rendering beats a mangled table.

### 5.4 Block quotes

Set-off prose → `>`. The easy case is a smaller font or a wider left margin. **The hard case: a block quotation set in body font at body size**, distinguished ONLY by being indented on *both* margins — invisible to font/size heuristics. Detect these from geometry (or, when only a flat text layer is available, from the rendered page): a quote line is inset on the LEFT beyond the body margin AND inset on the RIGHT (its interior justified lines reach near, but not all the way to, the body right edge). Group ≥3 consecutive quote-like lines into a band with a consistent left edge. Two trimming rules prevent over/under-capture:
- **Trim a band's first line if it runs to the full body right margin** — that is a paragraph first-line indent, not a quote.
- **Include a short final line** that begins at the quote's established left inset (e.g. a trailing "(emphasis added)." or the line carrying the citation marker) — bands are often 1 line too short and drop the quote's last fragment.
- **Skip narrow / off-margin fragments** (a stray superscript or footnote-marker bit) rather than letting them break or truncate a band.

**Exclude code/data/figure regions from blockquote conversion** even when they are indented: skip a band whose content looks like markup (`class=`, `<div`, shell/R commands) or tabular data (word–number frequency pairs, adjacency-list node names, money tokens), and skip a band whose y-range overlaps monospace/code-font text or a figure raster. A region dominated by code lines is a code block, not a quotation (a real bug put a body line between two indented code snippets into a spurious blockquote).

A single PyMuPDF block frequently holds a quote followed by body text; split the block at the band boundary so each part is typed correctly, and cap the split pieces at their own line count plus small slack so the quote neither swallows the next paragraph nor truncates its own wrapped tail. Preserve a trailing citation and inline emphasis. **In kramdown a bare blank line breaks a blockquote** — separate `>` paragraphs with a `>`-only line so a multi-paragraph quotation stays continuous.

### 5.5 Lists

Ordered item: starts with `N.`/`N)` at the body margin (reject decimals like `99.9` with a guard such as `^(\d{1,2})[.)](?!\d)`). Bullet: starts with `•◦▪‣·–—-`. Item text wraps to following lines until the next item or a paragraph break. Strip the list prefix from the rendered text; preserve nesting by indentation; blank line after a list run (or a renderer folds the following paragraph into the list).

**Checkbox lists.** A planning/working document may use ballot boxes (`☐` U+2610, `☑` U+2611) as list markers — render them as GitHub task-list items (`- [ ]` / `- [x]`) so the checkbox structure survives and stays readable.

**The literal-"o" bullet-glyph artifact.** Some PDFs encode a bullet as a literal lowercase "o" (or another letter) in a symbol/dingbat font rather than a real bullet codepoint. Detect the bullet by its *font* (a symbol/Wingdings/Dingbats face), not by the character, and emit `-`. If you miss this, the bullet surfaces in the markdown as a stray "o" — and worse, an emphasis/code pass may wrap that "o" as inline `` `code` ``. Map the known bullet-fonts to `-` up front.

**Multi-criterion rubrics and definition-style lists.** An evaluation rubric or a "term — definition" list reconstructs cleanly as a GFM table (criterion | description) or as a `**term** — definition` list; pick whichever matches the source's visual structure and keeps every word.

**Single-line commands set in body font.** A line like `cd mallet` or `./bin/mallet` is code but typeset in the body font, so font can't flag it. Detect it from an introductory cue (the preceding line ends in "type:" / "enter:" / "run:") OR a short standalone line that is an unambiguous shell command (`cd `, `ls `, `./`, `bin\`, a known tool invocation), and render it as its own fenced/inline code. Keep this conservative — only obvious commands — so prose is never turned into code.

### 5.6 Equations

Math-heavy work extracts as garbled Unicode. In order of preference: (1) if recognizable, transcribe as LaTeX in `$…$`/`$$…$$`; (2) if garbled, **detect the display-math block, crop its region, and embed as `images/eq-<page>-<n>.png`**; (3) keep a numbered equation's number, as `\tag{2.7}` or a trailing `(2.7)`. Verify the crop visually — open the saved PNG and confirm it captured the whole expression (fraction bars, superscripts).

### 5.7 Captions

Figure/table captions begin `Figure 3.`, `Fig. 3.`, `Table 1.`, `Plate IV.` etc. **Disambiguate a standalone caption from an inline cross-reference.** Prose constantly says "as shown in Fig. 5.30, you will see…" or "(Fig. 7.10)" — these are NOT captions and must not anchor a figure crop. A real caption is `Fig. N.M` standing alone or followed by a title (a capital letter or quote), at the caption font size; reject `Fig. N.M` immediately followed by a comma or by lowercase prose. Matching a cross-reference instead of the caption makes the crop grab the wrong region (you get a picture of text instead of the figure) — a recurring real bug. When a page has several figures, pair each crop with the *nearest standalone caption below it*, not the first `Fig.` string on the page. **A caption that wraps to a second/third line must absorb its continuation lines** (same block, caption size, marked consumed) or the tail is lost (or worse, migrates into an adjacent footnote). Render the figure as the image embed followed by the full caption verbatim, with emphasis handled per the whole-italic-caption rule in 4.5:

```markdown
![Fig. 3.1](images/fig-3.1.png)

*Fig. 3.1* War and Peace *as a word cloud.*
```

The bracketed alt text is short; the caption line is verbatim (captions often carry methodological detail — never truncate).

### 5.8 Sidebars / info-boxes

Boxed asides (a distinct x-band, often a smaller size) reconstruct as block quotes, with their internal subheadings (`General Principles`, `Description`, …) preserved and **inline emphasis kept** (a bold or italic word inside an otherwise-roman sidebar line must survive — e.g. a bold term in a concordance example). Thread a box that spans a page boundary. **Scope each field correctly:** a box's labelled field can contain multiple paragraphs, code lines, and lists before the next field label — absorb ALL content *between field labels* into the box, not just the first paragraph, or the box ends early and a field's tail (or the next field) leaks into the body. For the LAST field (no following label to bound it), absorb only its own content paragraph(s), not the body prose that follows the box.

### 5.9 Bibliography / References

The reference list is sacred — reproduce it character-for-character, preserving the original style (APA, Chicago, MLA, Vancouver, numeric brackets). Detect by the heading (References / Bibliography / Works Cited / Literature / Sources, or the language-appropriate term). Render each entry as its own paragraph; if entries are numbered (`[1] Smith…`), preserve the numbers literally — do NOT convert to a Markdown numbered list (it would renumber on render and break in-text `[12]` citations). Italic journal/book titles and bold volume numbers are preserved (this is exactly where the italic-then-bold emphasis boundary rule matters).

**Entry-stitching repairs** when the bibliography comes from a PDF text layer (entries wrap across lines and pages): an entry start is a new author surname at the left margin or a `(year).` continuation of a repeated author; a line that is a bare URL fragment, a `doi:`/page-range tail, or a continued author list (`Duncan, …, &` wrapping to `Nöllenburg`) is a *continuation* of the previous entry, not a new one. Rejoin URL line-breaks (a URL split mid-token across a line end is stitched without the inserted space) and author-list continuations. A reference list rarely yields clean page anchors (no natural paragraph starts) — it is fine for the bibliography pages to carry no `<!-- page N -->` anchors.

### 5.10 TOC, figure lists, and the index

- **Contents (TOC):** one `- ` entry per chapter, title and page number on one line, leader dots stripped.
- **Figure list ("List of Figures"):** one `- ` entry per figure (id + caption), italic titles preserved as normal `*italic*`; a "Chapter N" divider can become a `####` subheading.
- **Index — two-column, and easy to mangle.** Read **column by column** (all of the left column top-to-bottom, then the right), never interleaved by y. Within each column, detect that column's OWN base x0: a line indented past it is a sub-entry; a line at it is a main entry. **Fold wrapped continuation lines** into the preceding entry (`bibliographic coupling network, 206,` + `207` → one entry); keep a bare-number continuation that wrapped, but only inside the index body (a bare number in the header/footer band is a folio — drop it). Don't treat an all-caps word like `XML` as roman numerals (require a digit-start or all-lowercase for a "page list" continuation). Emit `- ` for main entries, `  - ` for sub-entries. A word-level check (every index word present except the filtered preprint filename) confirms nothing was lost.

---

## Phase 6 — Extract images

Use PyMuPDF, which gives both bytes and the on-page bounding box.

```python
def extract_images(doc, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    catalog, seen = [], set()
    for pno, page in enumerate(doc, 1):
        for img in page.get_images(full=True):
            xref = img[0]
            if xref in seen: continue
            seen.add(xref)
            pix = fitz.Pixmap(doc, xref)
            if pix.width < 50 or pix.height < 50: continue      # skip rules/bullets/logos
            if pix.n - pix.alpha > 3: pix = fitz.Pixmap(fitz.csRGB, pix)
            rects = page.get_image_rects(xref)
            catalog.append((pno, rects[0] if rects else None, xref, pix))
    return catalog
```

Notes:
- Skip images < 50×50 px (rules, bullets, logos, masks). Deduplicate by xref (a logo repeats every page).
- **Vector graphics do NOT appear through `get_images`.** If a page visibly contains a chart but `get_images` returns nothing for it, rasterize the chart region: `page.get_pixmap(clip=bbox, dpi=200)`.
- For PDF-of-HTML, embedded images may be low-DPI — that is how the source rendered; don't upscale.

**Naming.** Use a stable, sortable scheme. For articles, `fig-001.png`, `fig-002.png`. For books with chapter.figure numbering, mirror the source label so a citation resolves: `fig-3.1.png`, `fig-3.10.png`, cropped equations `eq-145-1.png`. If the project uses a fixed prefix convention (e.g. a corpus id like `SBW-001-fig3.1.png`), follow it consistently. Whatever scheme you pick, every `images/...` reference in the markdown must resolve to a file on disk, and every file in `images/` must be referenced at least once (Phase 9 checks both directions).

Crop a figure region from just below the previous content's bottom down to just above the `Fig. N.M` caption. **Get the top boundary right:** a common bug is the crop grabbing a tail of prose from *above* the figure. A short line at the body left margin with a small gap before the figure is the previous paragraph's last line — count it as prose so the crop starts *below* it, not above it. Conversely, do not let the crop run *into* the caption. **Spot-check several crops visually** — open the saved PNGs — and adjust the prev-bottom / caption-top boundary for any that grabbed caption text, a stray prose line, or the wrong region.

**Rasterization-determinism caveat (PyMuPDF):** calling `page.get_text("dict")` on a page can change how `page.get_pixmap()` subsequently rasterizes it near threshold boundaries. If you rasterize pages for pixel-level analysis (e.g. visual blockquote detection, 5.4), render those pixmaps from a **separate `fitz` document handle that never has `get_text` called on it**, or the analysis becomes non-deterministic depending on call order.

**Preserve, don't "fix", the figure as printed.** If labels at a figure's edges fade or are clipped in the original publication, that is how the source looks — crop faithfully and note it; do not regenerate or "complete" the figure. When cropping a UI screenshot or a dialog, make sure the crop includes the title bar / topmost field the caption refers to (a too-tight top edge that cuts the dialog title is a real recurring miss). When the publisher ships higher-resolution per-page JPEGs (e.g. 924×1316 inside a zip container) alongside a lower-res assembled PDF, crop figures from the **higher-resolution** page images.

Some publisher text encodes a **bullet glyph as a stray character** (e.g. `&` or a private-use codepoint); normalize it to a Markdown `-` list marker rather than emitting the literal glyph.

**On a scanned/OCR'd page, exclude figure-interior text from the body.** When a page is one big raster, OCR produces text blocks *inside* the figure (axis labels, legend words, screenshot UI text) that are not body prose. Distinguish them with an "anchor" test: a real body block is body-sized, spans a wide fraction of the text column, and contains ≥5 real alphabetic words; blocks above a caption with no anchor block between them are figure interior — drop them from the body so they neither pollute the prose nor displace a real line. (This is the scanned-page form of the figure-internal-text trap.)

**Recover a figure whose caption OCR'd badly via the embedded image rectangle.** If the `Fig. N.M` caption regex misses a figure (the caption text was garbled), fall back to the page's embedded-image rectangle (or, for a full-raster page, the inter-anchor gap) to locate and crop the figure, then attach the caption you do have. Never let a mis-OCR'd caption cause a silently missing figure — cross-check the figure count against the figure list / list-of-figures.

**Prefer publisher-supplied figure files over page crops.** When the user uploads the journal's high-resolution figure PNGs/JPEGs, or an HTML edition carries the figures as real images, use those (renamed to your scheme) instead of cropping from the page raster — they are cleaner and at full resolution. Crop from the page only when no separate image exists (e.g. a vector figure, which you rasterize from its PDF page).

**Screenshot/figure internal text is not separately transcribed.** A figure that is a screenshot of a tool UI carries text inside the image; that text rides along in the embedded PNG and is not reproduced as body prose (note this in `extraction_notes` for manual-style documents heavy with screenshots).

---

## Phase 7 — Scanned PDFs (OCR)

If the diagnostic showed near-empty `pdftotext`, OCR with Tesseract at 300 DPI:

```python
import pytesseract, io
from PIL import Image
def ocr_page(page, dpi=300, lang="eng"):
    pix = page.get_pixmap(dpi=dpi)
    return pytesseract.image_to_string(Image.open(io.BytesIO(pix.tobytes("png"))), lang=lang)
```

Set `lang` for non-English (`deu`, `fra`, `eng+lat` for Latin quotes; install packs with `apt-get install tesseract-ocr-<lang>`). OCR loses font/style, so emphasis is lost — note this in `extraction_notes`. OCR breaks tables — rasterize and embed those. Then run the SAME cross-page stitching, dehyphenation, and header-stripping. For noisy scans (bleed-through), raise DPI to 400 and try `--psm 1`.

## Phase 8 — PDF-of-HTML specifics

Single column, generous margins, URL/timestamp footer, `about:blank` header. Use plain top-to-bottom ordering (skip column detection). Strip the browser print header/footer aggressively (URL pattern, `\d+/\d+` page-of-total, `M/D/YY, H:MM AM/PM`). Reconstruct hyperlinks from `page.get_links()` as `[anchor](url)`. Strip "Cite this article" / "Download PDF" widgets. Verify the bibliography terminates cleanly and the conclusion isn't truncated (print rendering can lose content).

---

## Phase 9 — Quality checks: a QA battery AND a visual review

Fidelity is proven two independent ways. Run BOTH. Fix every failure at the root; treat any miss as real until shown a benign false-positive.

### 9.1 Automated QA battery

Write a `qa.py` you can re-run after every change. Check at least:

1. **Footnote/endnote parity:** unique inline markers == unique definitions == expected count; `orphan defs == []`, `orphan markers == []`. Spot-verify a few markers landed at the right words.
2. **Content-loss audit (forward), two passes:**
   - *Word-set pass:* for each body page, the set of ≥6-letter words in the source text layer should appear in the output (normalize soft hyphens, lowercase, allow dehyphenation joins). Flag pages with >~6% missing.
   - *Bigram-coverage pass (stronger — catches re-ordered loss the word-set pass misses):* join a page's clean text into one word stream, form adjacent word-pairs, and check what fraction appear anywhere in the normalized output. Flag pages where >~8% of bigrams are missing. This is robust to line-wrap differences but sensitive to genuinely dropped phrases; it has caught a dropped footnote, a half-dropped table, and a lost paragraph that the word-set pass reported as clean.
   - Figure-only and TOC/index pages legitimately flag (no prose / reformatted) — whitelist those after confirming all their words are present; every other failing page is real loss to investigate. Never accept prose loss.
3. **Fabrication audit (reverse):** every ≥4-letter word in the markdown body should exist in the source (allowing dehyphenation joins and known title-page additions). This catches invented text. Expect an empty result except genuinely source-present oddities.
4. **Leak detection (must be 0 in body):** preprint job codes, `.indd`, ISBN digits used as a stamp, the exact running-head string, date/time stamps. Also assert these strings are absent from `extraction_notes`.
5. **Emphasis well-formedness:** per non-code line, the count of `*` (after removing `\*` and code spans) is even — every emphasis marker opens and closes. No `****`. (A naive `* *` substring test is WRONG now that valid `*italic* **bold**` adjacency exists — use the per-line balance check.)
6. **Structure:** expected `##` section count; sub/sub-subheadings present; ordered + bullet lists present; dehyphenation clean (`pro vide`, `under stood` == 0); no space before a marker (` [^` == 0); **figure count == image-file count**; every `images/...` path resolves and every image file is referenced; 0 control chars (`\x00`–`\x08`, `\x0e`–`\x1f`); 0 raw `<tag>` outside code; YAML parses.
7. **Special-character integrity:** every meaningful non-ASCII char in the source (curly quotes, em/en dash, ellipsis, accented letters, degree sign, angle quotes) appears in the markdown. The only acceptable "missing" non-ASCII are intentionally-normalized whitespace (en/em/thin/nbsp/line-separator U+2028/U+2029 → space), the soft hyphen (dehyphenated), and bullets (→ `-`), plus any char that lives only inside a cropped equation image. Add U+2028/U+2029 and all Unicode spaces to your whitespace normalization, or a line-separator can leak into (e.g.) an index entry as a stray double-space.
8. **Word-count parity:** `wc -w` of the markdown body (minus YAML and image syntax) within ~5% of `pdftotext -layout`. >10% short ⇒ content missing (a column missed, footnotes dropped, a chapter skipped).

### 9.2 Visual review against rendered screenshots — do this, don't skip it

The automated battery cannot see a figure crop that grabbed the wrong region, a table whose columns merged, a two-column index read in the wrong order, or a caption that lost its emphasis. **Render the pages and look.**

```bash
# render every page at ~95 dpi
python3 - <<'PY'
import fitz
doc = fitz.open("paper.pdf")
for i in range(doc.page_count):
    doc[i].get_pixmap(dpi=95).save(f"/home/claude/pages/p{i:03d}.png")
PY
```

Viewing hundreds of pages one-by-one is infeasible, so build **labeled contact sheets** (montages of ~30 thumbnails each, with the page number drawn on each thumbnail) and `view` those to scan layout at a glance. Then `view` at full resolution only the pages that look structurally complex or "off": every page with a figure, table, sidebar, equation, code block, the TOC, the figure list, and the index. For each, compare the rendered page against the corresponding markdown (use page anchors / `grep` / small `view` ranges — never the whole file). Confirm: text is verbatim, no paragraph missing or duplicated, tables match the grid, figures cropped cleanly with the right caption, emphasis present where the page shows italic/bold, columns and index read in the right order. **First and last body pages get extra scrutiny** — that's where text is most often clipped (title page bleeding into the first paragraph; last bibliography entry cut off).

This visual pass is where the highest-value bugs are caught. It found, on a real book: figure-caption truncation (and the lost tail migrating into a footnote), a two-column index read in interleaved order with right-column entries mis-nested as sub-entries, a network table's narrow `ID|Label` columns merging, and several emphasis-flattening cases — none of which any text linter flagged.

If any check or visual comparison fails, fix and re-run. Do not deliver a file that fails the content-loss or word-count parity test without disclosing it in `extraction_notes`.

---

## Phase 10 — Markdown hygiene for downstream renderers

- **Escape `<` and `>` to `&lt;`/`&gt;` everywhere EXCEPT inside fenced code and inline code**, so a Jekyll/kramdown pipeline doesn't parse the work's HTML/XML examples as tags. (The QA "no raw `<tag>` outside code" check enforces this.)
- Preserve leading indentation inside fenced code blocks (it is part of the literal content). Courier/monospace runs → fenced code; literal `*` inside code is NOT emphasis.
- One blank line between block elements; a `>`-only line between blockquote paragraphs; blank line after a list run.
- **Exactly one top-level `#` — the work's title.** If the source (often a web/magazine article whose section headings were authored as `<h1>`) yields multiple `#` headings, demote the section headings to `##` (and shift the rest down a level) so the document has a single `#`.
- **Image alt text must be a single line.** A multi-line caption flattened into the `![…]()` alt slot breaks the image syntax — collapse the alt text to one line (full caption still goes in the verbatim caption paragraph below the image).

---

## Phase 11 — Package as a downloadable zip (+ MANIFEST)

The markdown loses its image references if the user downloads it without `images/` beside it, so bundle the working folder into one zip placed next to it. Before zipping, write a `MANIFEST.txt` (sha256 + byte size of every file) for reproducibility/citation, so it ends up inside the zip.

```python
import hashlib, shutil
from pathlib import Path

def write_manifest(out_dir: Path):
    lines = []
    for p in sorted(out_dir.rglob("*")):
        if p.is_file() and p.name != "MANIFEST.txt":
            d = hashlib.sha256(p.read_bytes()).hexdigest()
            lines.append(f"{d}  {p.stat().st_size:>10}  {p.relative_to(out_dir)}")
    (out_dir / "MANIFEST.txt").write_text("\n".join(lines) + "\n")

def package_zip(out_dir: Path) -> Path:           # out_dir = .../outputs/paper
    parent, name = out_dir.parent, out_dir.name
    return Path(shutil.make_archive(str(parent / name), "zip",
                                    root_dir=str(parent), base_dir=name))
```

Internal structure is `paper/paper.md`, `paper/images/...`, `paper/MANIFEST.txt` — a single `paper/` folder when unzipped, which every OS expects. Zip an empty `images/` too (absence of figures is itself information). For a 500-page color book exceeding ~500 MB, downsample embedded images to ~200 DPI before zipping and note it in `extraction_notes`. `make_archive` overwrites on rerun. Verify without pulling contents into context:

```bash
unzip -l paper.zip | head -20          # listing only
unzip -l paper.zip | wc -l             # entry count
ls -la paper.zip                       # size
```

Confirm the markdown appears, `images/` has the expected count, and the zip size ≈ markdown + image sizes. Regenerate if a check fails; never deliver a broken archive.

---

## Phase 12 — Output & handoff

`present_files` with **two paths in this order**: the zip first (the all-in-one download), the markdown second (read without unzipping).

```python
present_files(filepaths=[
    "/mnt/user-data/outputs/paper.zip",
    "/mnt/user-data/outputs/paper/paper.md",
])
```

Your final message is **short** (Rule 6): one paragraph of what you converted (type, page count, language); a note that the zip contains the markdown, images, and MANIFEST; any caveats from `extraction_notes` (OCR used, equations as images, tables rasterized, mixed languages). **Do not paste the YAML, abstract, TOC, or any body into the message** — that is what `present_files` is for, and inlining it is the most common way long jobs hit the truncation error. Do not narrate the pipeline step-by-step; the artifact is the deliverable, the message is the receipt.

---

## Worked example — the skeleton of a finished article

```markdown
---
title: "Attention Is All You Need"
authors:
  - { family: "Vaswani", given: "Ashish", affiliation: "Google Brain" }
  - { family: "Shazeer", given: "Noam", affiliation: "Google Brain" }
publication_type: "conference_paper"
event: "NeurIPS 2017"
year: 2017
arxiv: "1706.03762"
doi: "10.48550/arXiv.1706.03762"
language: "en"
abstract: |
  The dominant sequence transduction models are based on complex recurrent or
  convolutional neural networks…
source_pdf: "1706.03762.pdf"
source_pdf_sha256: "…"
page_count: 15
extraction_date: "2026-06-15"
extraction_notes: |
  Two-column NeurIPS layout. Equations transcribed as LaTeX. Figure 1 was vector;
  rasterized at 200 DPI. Bibliography verbatim, numeric style preserved.
---

# Attention Is All You Need

## Abstract

The dominant sequence transduction models… <!-- page 1 -->

## 1 Introduction

Recurrent neural networks, long short-term memory [^13]… <!-- page 2 -->

![Fig. 1](images/fig-001.png)

**Figure 1.** The Transformer — model architecture.

$$ \mathrm{Attention}(Q, K, V) = \mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right) V \tag{1} $$

## References

[1] Jimmy Lei Ba, Jamie Ryan Kiros, and Geoffrey E. Hinton. Layer normalization. *arXiv preprint arXiv:1607.06450*, 2016.

[^13]: We use "recurrent" in the conventional sense; see Elman (1990).
```

That is the bar: verbatim text, structural fidelity, faithful metadata, preserved emphasis, citable anchors, extracted figures, intact equations and bibliography.

---

## Common gotchas, in one place

- **Two-column pages where the right column starts higher than the left** — sort each column by y independently; never interleave.
- **Footnotes spanning a page boundary** — thread the open def; flush only on a new def-start, never on body lines.
- **Parenthetical author-date `(Smith 2009, 47)` vs numeric footnote markers** — only superscript numerals become `[^N]`.
- **Drop caps** at chapter start (one huge initial letter) — prepend to the first word; not a heading.
- **Italic title abutting a bold volume number** in a footnote/bibliography (`*Journal* **3**(3)`) — the emphasis-merge boundary guard in 4.5 keeps it intact; without it you get `*Journal  *3**`.
- **An all-caps word in the index (`XML`)** read as Roman numerals — guard page-list continuations to require a digit-start or all-lowercase.
- **A line-separator (U+2028) or thin space** leaking as a stray space — normalize all Unicode spaces and separators.
- **A rendered-image table / spreadsheet / screenshot** — embed as a figure; do NOT extract its text; confirm none leaked into prose.
- **Figure-internal text matching a real line** — OCR or a text layer *inside* a figure (axis labels, a screenshot's UI text) can match or displace a real body line; drop tiny unmatched garbage blocks inside figure rasters so they don't consume the caption or the following paragraph.
- **Consecutive italic "vignette" paragraphs across a page break** — chapter-opening italic epigraphs/vignettes split across pages must be stitched when the first does not end a sentence (the same cross-page rule, applied to italic runs).
- **A recovery heuristic inventing an "(unnumbered note)" or a synthesized heading** — the orphaned text almost always belongs to an existing structure (the previous footnote, the preceding box); route it there instead of creating a container.
- **Hyperlink annotations** — when the visible text equals the URL, render the plain URL (auto-linkable, faithful); reconstruct `[anchor](url)` only when the printed anchor text genuinely differs. Auto-generated `doi:`/`ISSN`/`PMID` links keep the printed text.
- **Right-to-left scripts** — PyMuPDF returns logical order (correct for Markdown); verify on a sample.
- **Encrypted PDFs** — `pdfinfo` shows `Encrypted: yes`; try `qpdf --decrypt in.pdf out.pdf`, or ask for the password.
- **Redactions** — preserve as `[REDACTED]`; never silently delete.
- **Word-derived PDF** — paragraph breaks inside reference lists and bullet lists often collapse into one block, and headings arrive as inline bold/italic runs with no block boundary; reconstruct boundaries from the inline font runs and note in `extraction_notes` that structure is flatter than the source's logical structure (text is still verbatim).
- **Firefox/cairo "Print to PDF"** — the hyperlink *targets* are gone even though the anchor text remains; render those as `[anchor](#)` placeholders and say so, rather than dropping the link styling silently.

## When to ask the user before proceeding (once, at most one question)

A 5–30 page article: just deliver. Otherwise ask once: books over ~100 pages (whole book or specific chapters?); edited volumes (one file or split per chapter?); scanned foreign-language PDFs (confirm OCR language); handwritten annotations (include as marginalia or ignore?); a PDF that looks corrupt or non-scholarly (confirm they really want the scholarly pipeline). Default to "yes, the whole thing, the standard way" if they don't reply.

**Honor an explicit scope boundary the user gives.** If they say the article starts at a particular heading, or that the first column is the tail of a different article, begin/end exactly there and exclude the out-of-scope material (e.g. a truncated end-of-previous-article footnote list at the top of column 1) — and record the boundary in `extraction_notes`. Their stated scope overrides the document's physical page boundaries.
