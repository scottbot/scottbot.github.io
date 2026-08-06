#!/usr/bin/env python3
"""
ingest.py — content-ingestion pipeline for the Hugo site.

Usage:
    python3 scripts/ingest.py [--corpus PATH] [--csv PATH] [--site PATH]
                              [--only DIRNAME ...] [--force]

MODES — the default is safe and additive:

  (default)      ADD NEW MATERIAL ONLY. Corpus directories that already
                 have a generated bundle are left completely untouched
                 (hand-edits preserved); directories without one are
                 converted and added, and data/workmap.yaml gains their
                 entries. Safe to run whenever you drop a new conversion
                 into the corpus.

  --only NAME…   Ingest just the named corpus directories (exact folder
                 names). Refuses to overwrite an existing bundle unless
                 --force is also given, in which case ONLY those named
                 bundles are rebuilt.

  --force alone  FULL REBUILD: regenerates every corpus-backed bundle from
                 the corpus, which is the source of truth — every correction
                 to the published pages lives there, so a full rebuild
                 reproduces them exactly. Hand-edits made only to content/
                 (not the corpus) are lost. Pages that were never generated
                 from the corpus (hand-made bundles, _index.md files) are
                 not touched; their workmap entries survive if their pages
                 still exist. Bundles no longer backed by any corpus
                 directory are reported as orphans, never deleted.

Note for additive runs: cross-links are rewritten only inside the pages
being written. If a new post is the target of links in OLD posts, those
old links are not touched (they point at the original URLs, which still
resolve or are archived).

What it does:
  1. Walks every corpus directory (skipping ones starting with "_"), finds the
     single main .md file (ignoring *.bak, desktop.ini, MANIFEST.txt).
  2. Classifies each directory:
       - "blog":  dir named YYYY-MM-DD-slug  -> content/blog/<slug>/index.md
                  (slug = dir name minus the date prefix; the full dir name is
                  kept only if stripping would collide with another post)
       - "work":  everything else            -> content/works/<slug>/index.md
                  (slug from the curated WORK_SLUGS table below; unknown dirs
                  fall back to a kebab-cased dir name, with a warning)
  3. Replaces the source YAML frontmatter with normalized Hugo frontmatter
     (title, subtitle, date/yearOnly, author, author_note, worktype, venue,
     publisher, doi, original_url, archive_url, volume, issue, pages, isbn,
     tags, sbw, citation, abstract, comment_count, caveat_extra, bibkey).
     Provenance/extraction keys are intentionally dropped; the archive corpus
     retains them.
  4. Joins "List of Outputs.csv" on its "Local MD" column to add the sbw ID
     and (for works only) the Full Citation string.
  5. Body transformations (everything else is left byte-identical):
       - drops the body's first heading if it is an H1 equal to the title
         (case- and punctuation-insensitive) — Hugo renders the title;
       - demotes any remaining H1s to H2 (outside code fences);
       - removes the LLM-conversion caveat paragraph if the source carries
         one: the site template prints that caveat on every works/blog page,
         so leaving it in the body would show it twice.  Any extra sentence
         the author wedged into the caveat's middle is preserved as the
         `caveat_extra` frontmatter field, which the template reinserts;
       - rewrites markdown links whose target is another page's
         original_url / archive_url (including http/https, www/no-www,
         trailing-slash, port, Wayback-wrapped, and the WordPress-static
         /HIAL/index.html@p=NNNN.html variants) to that page's new
         site-relative path.
  6. Copies each directory's images/ and assets/ subdirs into the page bundle
     unchanged (junk files excluded).
  7. Writes data/workmap.yaml: ORIGINAL corpus dir name -> site path
     ("/blog/<slug>/" or "/works/<slug>/"), used by the CV templates to
     resolve `work:` references.
  8. Sanity checks: every generated index.md must YAML-parse; every
     images/... or assets/... reference in a body must exist in its bundle
     (missing ones are reported, not fatal).

Only touches: content/blog/, content/works/, data/workmap.yaml, and
data/sources.yaml (site path -> corpus source file, for edit links).  Never
touches layouts/, assets/, data/cv/, hugo.toml.  Only the bundles being
(re)written in this run are removed before regeneration (top-level files
such as _index.md are always preserved).
"""

import argparse
import csv
import datetime
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlsplit

import yaml

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

# Defaults resolve relative to this script's home (site\\scripts), so a
# bare `python scripts/ingest.py` works anywhere the site folder goes.
# The corpus and its CSV live INSIDE the site (site\\corpus\\), so the
# whole apparatus — sources, converter, and pages — migrates as one folder.
_HERE = Path(__file__).resolve().parent
SITE_DEFAULT = str(_HERE.parent)
CORPUS_DEFAULT = str(_HERE.parent / "corpus" / "Markdown")
CSV_DEFAULT = str(_HERE.parent / "corpus" / "List of Outputs.csv")

JUNK_FILES = {"desktop.ini", "MANIFEST.txt", "Thumbs.db", ".DS_Store"}

# Curated, human-friendly slugs for the non-dated ("works") directories.
# Edit here if a slug should change; re-running the script (with --force)
# cleans up the old bundle automatically — but see the warning in the
# module docstring: a re-run discards any hand-edits under content/.
WORK_SLUGS = {
    "Allen_et_al_2010_An_API_for_Philosophy": "api-for-philosophy",
    "Borner_et_al_2009_NWB_User_Manual": "network-workbench-user-manual",
    "Burton_et_al_2019_Digits": "digits",
    "CMU_Library_Labs_2020-2024": "cmu-library-labs",
    "Conroy_et_al_2019_Visualizing_Networks_and_Temporality":
        "visualizing-networks-and-temporality",
    "Conroy_et_al_2024_Uncertainty_Humanities_Network_Visualization":
        "uncertainty-in-humanities-network-visualization",
    "Eichmann-Kalwara_et_al_2018_Representation_at_DH_Conferences":
        "representation-at-dh-conferences",
    "Ekbia_et_al_2015_Big_data_bigger_dilemmas": "big-data-bigger-dilemmas",
    "Gomez_et_al_2020_Latin_American_Comics_Archive":
        "latin-american-comics-archive",
    "Graham_Weingart_2014_Equifinality_Archaeological_Networks":
        "equifinality-of-archaeological-networks",
    "Graham_et_al_2012_topic_modeling": "topic-modeling-and-mallet",
    "Graham_et_al_2014_Writing_Macroscope_in_Public":
        "writing-macroscope-in-public",
    "Guo_et_al_2011_Mixed_indicators_model": "mixed-indicators-model",
    "Journal_of_Digital_Humanities_2-1": "journal-of-digital-humanities-2-1",
    "Ladd_et_al_2017_Exploring_Network_Data_with_Python":
        "exploring-network-data-with-python",
    "Langmead_et_al_2016_Interoperable_Network_Ontologies":
        "interoperable-network-ontologies",
    "Lincoln_et_al_2020_CAMPI": "campi",
    "Lincoln_et_al_2021_Index_of_DH_Conferences": "index-of-dh-conferences",
    "Milojevic_et_al_2012_Information_visualization":
        "information-visualization-state-of-the-art",
    "NEH_2024_Assessing_the_State_of_the_Humanities_Preliminary":
        "assessing-the-state-of-the-humanities",
    "NEH_2025_State_and_Impact_of_the_Humanities_NOFO":
        "state-and-impact-of-the-humanities-nofo",
    "Network Turn": "network-turn",
    "Sack_and_Weingart_Literary_Network_Analysis": "literary-network-analysis",
    "Sugimoto_and_Weingart_2015_kaleidoscope_of_disciplinarity":
        "kaleidoscope-of-disciplinarity",
    "Thelwall_et_al_2013_Tweeting_Links": "tweeting-links-to-academic-articles",
    "Van_den_Heuvel_et_al_2016_Circles_of_Confidence": "circles-of-confidence",
    "Weingart_2011_Demystifying_Networks": "demystifying-networks",
    "Weingart_2013_From_Trees_to_Webs": "from-trees-to-webs",
    "Weingart_2014_Networks_In_and_Of_Society":
        "moral-role-of-dh-in-a-data-driven-world",
    "Weingart_2015_Connecting_the_Dots": "connecting-the-dots",
    "Weingart_2015_Finding_the_History_and_Philosophy_of_Science":
        "finding-the-history-and-philosophy-of-science",
    "Weingart_2016_Punched_Card_Humanities": "punched-card-humanities",
    "Weingart_and_Eichmann_2017_Whats_Under_the_Big_Tent":
        "whats-under-the-big-tent",
    "Weingart_and_Jorgensen_2012": "body-in-european-fairy-tales",
    "Weingart_and_Meeks_2013_DH_Contribution_to_Topic_Modeling":
        "dh-contribution-to-topic-modeling",
    "Weingart_et_al_2011_Sci2_User_Manual": "sci2-user-manual",
    "heberling-et-al-2021-data-integration-enables-global-biodiversity-synthesis":
        "data-integration-enables-global-biodiversity-synthesis",
    "macroscope-1stEd": "historians-macroscope",
    "macroscope-2e": "historians-macroscope-2e",
    "the-route-of-a-text-message-a-love-story":
        "the-route-of-a-text-message-a-love-story",
}

# publication_type -> normalized worktype
PTYPE_MAP = {
    "article": "article",
    "book": "book",
    "book_chapter": "chapter",
    "conference_paper": "article",
    "report": "report",
    "manual": "manual",
    "magazine_article": "magazine",
    "journal_issue": "issue",
    "blog_post": "blog",
}
# CSV "Type" fallback when frontmatter has no publication_type
CSV_TYPE_MAP = {
    "article": "article", "book": "book", "blog post": "blog",
    "report": "report", "book chapter": "chapter",
}

# Variant spellings of the site owner's name, normalized for the author list.
OWNER_CANONICAL = "Scott B. Weingart"
OWNER_ALIASES = {
    "scottbot", "scott weingart", "scott b. weingart", "scott b weingart",
    "weingart, scott", "weingart, scott b.",
}

# Normalized URLs that are too generic to identify a single page.
GENERIC_URLS = {"", "scottbot.net", "scottbot.net/HIAL"}


def too_generic(key):
    """A normalized URL that is a bare host (no path, no query) identifies a
    whole site, not a page — never index or match it."""
    return key in GENERIC_URLS or ("/" not in key and "?" not in key)

DATED_DIR_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)$")
FULL_DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)
WAYBACK_RE = re.compile(r"^https?://web\.archive\.org/web/[^/]+/(https?://.*)$", re.I)
STATIC_P_RE = re.compile(r"^(.*)/index\.html@p=(\d+)\.html$")


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

def strip_markdown(text):
    """Strip inline markdown (emphasis, code, links) from a title string.
    Leaves plain '#'/'/' characters alone ('#humnets paper/review' is a title,
    not markup)."""
    s = str(text)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)          # [text](url) -> text
    for pat in (r"\*\*(.+?)\*\*", r"__(.+?)__", r"\*(.+?)\*", r"`(.+?)`"):
        while re.search(pat, s):
            s = re.sub(pat, r"\1", s)
    return s.strip()


def norm_title(text):
    """Case- and punctuation-insensitive form for comparing headings/titles."""
    return re.sub(r"[^0-9a-z]+", "", strip_markdown(text).lower())


def kebab(s):
    s = re.sub(r"[^0-9A-Za-z]+", "-", s).strip("-").lower()
    return re.sub(r"-{2,}", "-", s)


def parse_full_date(value):
    """Return datetime.date if value is a full ISO date, else None."""
    if isinstance(value, datetime.datetime):
        return value.date()
    if isinstance(value, datetime.date):
        return value
    m = FULL_DATE_RE.match(str(value).strip()) if value is not None else None
    if m:
        try:
            return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None
    return None


def extract_year(*values):
    """First 4-digit year found in any of the given values, else None."""
    for v in values:
        if v is None:
            continue
        if isinstance(v, int) and 1000 <= v <= 9999:
            return v
        m = re.search(r"\b(1[89]\d{2}|20\d{2})\b", str(v))
        if m:
            return int(m.group(1))
    return None


def normalize_url(url):
    """Canonical form of a URL for cross-link matching.

    - unwraps Wayback Machine URLs to their embedded original
    - drops scheme (http == https), fragment, leading 'www.', ports 80/443
    - strips trailing slash
    - folds WordPress-static '/HIAL/index.html@p=NNNN.html' to '/HIAL/?p=NNNN'
    Returns (key, fragment).
    """
    if not url:
        return "", ""
    u = str(url).strip()
    frag = ""
    if "#" in u:
        u, frag = u.split("#", 1)
    for _ in range(3):                       # unwrap (possibly nested) Wayback
        m = WAYBACK_RE.match(u)
        if not m:
            break
        u = m.group(1)
    parts = urlsplit(u)
    if parts.scheme not in ("http", "https"):
        return "", frag
    host = parts.netloc.lower()
    host = re.sub(r":(80|443)$", "", host)
    if host.startswith("www."):
        host = host[4:]
    path, query = parts.path, parts.query
    m = STATIC_P_RE.match(path)
    if m:                                    # /HIAL/index.html@p=123.html
        path, query = m.group(1) + "/", "p=" + m.group(2)
    path = path.rstrip("/")
    key = host + path
    if query:
        key += "?" + query
    return key, frag


def load_frontmatter(md_path):
    # utf-8-sig: Windows editors (Notepad's "UTF-8 with BOM") prepend a byte
    # order mark that would otherwise hide the frontmatter from FRONTMATTER_RE.
    text = md_path.read_text(encoding="utf-8-sig")
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError(f"{md_path}: no YAML frontmatter")
    fm = yaml.safe_load(m.group(1))
    if not isinstance(fm, dict):
        raise ValueError(f"{md_path}: frontmatter is not a mapping")
    return fm, text[m.end():]


def person_name(entry):
    """Display name from an authors/editors entry (dict or string)."""
    if isinstance(entry, str):
        name = entry.strip()
    elif isinstance(entry, dict):
        family = str(entry.get("family") or "").strip()
        given = str(entry.get("given") or "").strip()
        if family or given:
            name = (given + " " + family).strip()
        else:
            name = str(entry.get("display") or entry.get("name")
                       or entry.get("literal") or "").strip()
    else:
        name = str(entry).strip()
    if name.lower() in OWNER_ALIASES:
        return OWNER_CANONICAL
    return name


def author_list(fm):
    names = [person_name(a) for a in (fm.get("authors") or [])]
    names = [n for n in names if n]
    if not names and fm.get("corporate_author"):
        names = [str(fm["corporate_author"]).strip()]
    if not names and fm.get("editors"):
        names = [n for n in (person_name(e) for e in fm["editors"]) if n]
    # dedupe, preserving order
    seen, out = set(), []
    for n in names:
        if n not in seen:
            seen.add(n)
            out.append(n)
    return out


def nonempty(value):
    """Value if it is a non-empty scalar/string, else None."""
    if value is None:
        return None
    if isinstance(value, str) and not value.strip():
        return None
    return value


# --------------------------------------------------------------------------
# Body transformations
# --------------------------------------------------------------------------

CODE_FENCE_RE = re.compile(r"^(\s{0,3})(`{3,}|~{3,})")

# The LLM-conversion caveat some corpus files carry in their body.  The site
# template prints this caveat on every works/blog page, so the body copy is
# removed at ingest.  The optional sentence between "Errors likely exist."
# and "To correct errors" is author-written and survives as caveat_extra.
CAVEAT_RE = re.compile(
    r"^\*Note: The conversion of this .{1,60}? to a website \(via markdown\) "
    r"was assisted with an LLM\. Errors likely exist\."
    r"(?: (?P<extra>.*?))?"
    r" To correct errors or to issue a copyright takedown request.*\*\s*$")
INLINE_LINK_RE = re.compile(r"\]\(\s*(<?)(https?://[^)\s>]+)(>?)((?:\s+\"[^\"]*\")?\s*)\)")
REF_DEF_RE = re.compile(r"^(\s{0,3}\[[^\]]+\]:\s*)(https?://\S+)(.*)$")
AUTOLINK_RE = re.compile(r"<(https?://[^>\s]+)>")


def transform_body(body, title, url_index, self_path, stats):
    """Apply the body transformations.

    Returns (new_body, caveat_extra) — caveat_extra is the author's extra
    sentence rescued from a stripped caveat paragraph, or None.
    """
    lines = body.split("\n")
    out = []
    in_fence = False
    fence_marker, fence_len = "", 0
    first_heading_done = False
    caveat_extra = None

    def rewrite_target(url):
        key, frag = normalize_url(url)
        if key and not too_generic(key) and key in url_index:
            new = url_index[key]
            stats["links_rewritten"] += 1
            if new == self_path:
                stats["links_self"] += 1
            return new + ("#" + frag if frag else "")
        return None

    def rewrite_links(line):
        def sub_inline(m):
            new = rewrite_target(m.group(2))
            return f"]({new}{m.group(4)})" if new else m.group(0)

        def sub_refdef(m):
            new = rewrite_target(m.group(2))
            return f"{m.group(1)}{new}{m.group(3)}" if new else m.group(0)

        def sub_auto(m):
            new = rewrite_target(m.group(1))
            return f"<{new}>" if new else m.group(0)

        line = INLINE_LINK_RE.sub(sub_inline, line)
        m = REF_DEF_RE.match(line)
        if m:
            line = sub_refdef(m)
        line = AUTOLINK_RE.sub(sub_auto, line)
        return line

    want_title = norm_title(title)
    i = 0
    while i < len(lines):
        line = lines[i]
        fence = CODE_FENCE_RE.match(line)
        if fence:
            if not in_fence:
                in_fence = True
                fence_marker, fence_len = fence.group(2)[0], len(fence.group(2))
            elif (fence.group(2)[0] == fence_marker
                  and len(fence.group(2)) >= fence_len):
                # CommonMark: a closing fence must be at least as long as
                # the opening one; a shorter run inside the block is content.
                in_fence = False
            out.append(line)
            i += 1
            continue
        if in_fence:
            out.append(line)
            i += 1
            continue

        caveat = CAVEAT_RE.match(line)
        if caveat:
            # Template supplies this paragraph; drop it (plus one blank line).
            stats["caveats_stripped"] += 1
            extra = (caveat.group("extra") or "").strip()
            if extra:
                caveat_extra = extra
            if i + 1 < len(lines) and lines[i + 1].strip() == "":
                i += 1
            i += 1
            continue

        heading = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if heading and not first_heading_done:
            first_heading_done = True
            if len(heading.group(1)) == 1 and norm_title(heading.group(2)) == want_title:
                # Drop the redundant H1; swallow one adjacent blank line.
                stats["h1_removed"] += 1
                if i + 1 < len(lines) and lines[i + 1].strip() == "":
                    i += 1
                i += 1
                continue
        if heading and len(heading.group(1)) == 1:
            stats["h1_demoted"] += 1
            line = "#" + line

        out.append(rewrite_links(line))
        i += 1
    return "\n".join(out), caveat_extra


# --------------------------------------------------------------------------
# Frontmatter building
# --------------------------------------------------------------------------

def build_frontmatter(kind, dirname, fm, csv_row, warnings):
    """kind: 'blog' or 'work'. Returns an ordered dict for YAML emission."""
    out = {}

    def put(key, *alt_keys, strip=False):
        """Pass a corpus frontmatter value straight through, first key wins."""
        for k in (key,) + alt_keys:
            v = nonempty(fm.get(k))
            if v is not None:
                out[key] = str(v).strip() if strip else str(v)
                return

    out["title"] = strip_markdown(fm.get("title") or dirname)
    subtitle = nonempty(fm.get("subtitle"))
    if subtitle:
        out["subtitle"] = strip_markdown(subtitle)

    # ---- date ----
    date = None
    for candidate in (fm.get("post_date"), fm.get("issued"), fm.get("date")):
        date = parse_full_date(candidate)
        if date:
            break
    if not date and kind == "blog":
        # A blog page usually comes from a YYYY-MM-DD-slug directory, but can
        # also arrive via workmap adoption with an undated dirname.
        m = DATED_DIR_RE.match(dirname)
        date = parse_full_date(m.group(1)) if m else None
    year_only = False
    if not date:
        year = extract_year(fm.get("year"), fm.get("issued"),
                            (csv_row or {}).get("Date"))
        if year:
            date, year_only = datetime.date(year, 1, 1), True
        else:
            warnings.append(f"{dirname}: no date could be determined")
    if date:
        out["date"] = date
        if year_only:
            out["yearOnly"] = True

    # ---- author ----
    authors = author_list(fm)
    if authors:
        out["author"] = authors
    else:
        warnings.append(f"{dirname}: no authors resolved")
    put("author_note", strip=True)

    # ---- worktype ----
    if kind == "blog":
        out["worktype"] = "blog"
    else:
        ptype = nonempty(fm.get("publication_type"))
        if ptype and str(ptype) in PTYPE_MAP:
            out["worktype"] = PTYPE_MAP[str(ptype)]
        else:
            csv_type = str((csv_row or {}).get("Type") or "").strip().lower()
            out["worktype"] = CSV_TYPE_MAP.get(csv_type, "article")
            if ptype:
                warnings.append(f"{dirname}: unmapped publication_type {ptype!r}")

    # ---- venue / publisher ----
    venue = None
    for key in ("container_title", "journal", "blog_title", "publisher"):
        venue = nonempty(fm.get(key))
        if venue:
            break
    if venue:
        out["venue"] = str(venue)
    publisher = nonempty(fm.get("publisher"))
    if publisher:
        out["publisher"] = str(publisher)

    # ---- identifiers / links ----
    put("doi")
    put("original_url", "url")
    put("archive_url")

    # ---- bibliographic detail (straight passthrough, unrendered metadata) ----
    put("volume")
    put("issue", "number")
    put("pages")
    put("isbn")

    # ---- tags (tags + categories, deduped, order-preserving) ----
    tags, seen = [], set()
    for src in (fm.get("tags"), fm.get("categories")):
        if isinstance(src, str):
            src = [src]
        for t in src or []:
            t = str(t).strip()
            if t and t not in seen:
                seen.add(t)
                tags.append(t)
    if tags:
        out["tags"] = tags

    # ---- CSV join ----
    if csv_row:
        out["sbw"] = csv_row["ID"]
        citation = (csv_row.get("Full Citation") or "").strip()
        if kind == "work" and citation:
            out["citation"] = citation

    # ---- abstract / comment_count ----
    put("abstract", strip=True)
    cc = fm.get("comment_count")
    if isinstance(cc, int) and cc > 0:
        out["comment_count"] = cc

    # ---- caveat_extra / bibkey ----
    put("caveat_extra", strip=True)
    put("bibkey")
    return out


def dump_frontmatter(meta):
    return "---\n" + yaml.safe_dump(
        meta, sort_keys=False, allow_unicode=True,
        default_flow_style=False, width=1000) + "---\n"


# --------------------------------------------------------------------------
# Main pipeline
# --------------------------------------------------------------------------

def find_main_md(dirpath):
    mds = sorted(p for p in dirpath.iterdir()
                 if p.suffix == ".md" and p.is_file())
    return mds[0] if len(mds) == 1 else (mds or None)


def main():
    # On Windows, redirected output (python ingest.py > log.txt) defaults to
    # a legacy codepage that chokes on em-dashes and accented names; force
    # UTF-8 so the report never crashes after the files are already written.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(
        description="Convert the corpus of markdown conversions into "
                    "Hugo page bundles (default mode: additive and safe).")
    ap.add_argument("--corpus", default=CORPUS_DEFAULT)
    ap.add_argument("--csv", default=CSV_DEFAULT)
    ap.add_argument("--site", default=SITE_DEFAULT)
    ap.add_argument("--only", nargs="+", metavar="DIRNAME", default=None,
                    help="ingest only these corpus directories (exact names)")
    ap.add_argument("--force", action="store_true",
                    help="with --only: rebuild those bundles even if they "
                         "exist; alone: FULL rebuild of everything "
                         "(destroys all hand-edits since ingestion)")
    args = ap.parse_args()

    corpus = Path(args.corpus)
    site = Path(args.site)
    blog_root = site / "content" / "blog"
    works_root = site / "content" / "works"
    warnings, skipped = [], []
    stats = {"links_rewritten": 0, "links_self": 0, "h1_removed": 0,
             "h1_demoted": 0, "caveats_stripped": 0, "images_copied": 0}

    # ---- mode: additive (default) / --only subset / --force full rebuild ----
    full_rebuild = args.force and not args.only
    existing_map = {}                    # corpus dirname -> site path, from workmap
    workmap_path = site / "data" / "workmap.yaml"
    if workmap_path.is_file():
        loaded = yaml.safe_load(workmap_path.read_text(encoding="utf-8")) or {}
        if isinstance(loaded, dict):
            existing_map = loaded
    if full_rebuild:
        print("FULL REBUILD (--force): regenerating every corpus-backed "
              "bundle from the corpus. Edits made only to content/ (not "
              "the corpus) are lost; hand-made pages and _index.md files "
              "are not touched.", file=sys.stderr)

    # ---- CSV join table ----
    csv_by_localmd = {}
    if not Path(args.csv).is_file():
        print(f"ERROR: CSV not found: {args.csv}\n"
              "Pass --csv with the path to 'List of Outputs.csv'.",
              file=sys.stderr)
        return 2
    with open(args.csv, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            local_md = (row.get("Local MD") or "").strip()
            if local_md:
                if local_md in csv_by_localmd:
                    warnings.append(f"CSV: duplicate Local MD {local_md!r}")
                csv_by_localmd[local_md] = row

    # ---- pass 1: scan corpus, classify, assign slugs ----
    pages = []          # dicts: dirname, kind, slug, path, fm, body, srcdir
    for d in sorted(corpus.iterdir()):
        if not d.is_dir():
            continue
        if d.name.startswith("_"):
            skipped.append((d.name, "starts with '_'"))
            continue
        md = find_main_md(d)
        if md is None or isinstance(md, list):
            skipped.append((d.name, f"expected exactly 1 .md, found {md or []}"))
            continue
        try:
            fm, body = load_frontmatter(md)
        except Exception as e:
            skipped.append((d.name, f"unreadable frontmatter: {e}"))
            continue
        m = DATED_DIR_RE.match(d.name)
        if d.name in existing_map:
            # Adopt the published slug so cross-links and workmap stay
            # stable regardless of any drift in the slug table above.
            path = existing_map[d.name].strip("/")
            section, slug = path.split("/", 1)
            kind = "blog" if section == "blog" else "work"
        elif m:
            kind, slug = "blog", m.group(2)
        else:
            kind = "work"
            slug = WORK_SLUGS.get(d.name)
            if not slug:
                slug = kebab(d.name)
                warnings.append(
                    f"{d.name}: not in WORK_SLUGS; auto-slugged as {slug!r}")
        # Windows caps paths at 260 characters and not every git honors
        # core.longpaths; keep corpus paths comfortably clear of trouble.
        rel = f"corpus/Markdown/{d.name}/{md.name}"
        if len(rel) > 200:
            warnings.append(
                f"{d.name}: corpus path is {len(rel)} characters — rename "
                "the .md file shorter (the folder name can stay) or "
                "Windows checkouts will break")
        section_root = blog_root if kind == "blog" else works_root
        pages.append({"dirname": d.name, "kind": kind, "slug": slug,
                      "fm": fm, "body": body, "srcdir": d, "srcname": md.name,
                      "bundled": (section_root / slug / "index.md").exists()})

    # ---- resolve slug collisions ----
    by_key = {}
    for p in pages:
        by_key.setdefault((p["kind"], p["slug"]), []).append(p)
    collisions = []
    for (kind, slug), group in by_key.items():
        if len(group) > 1:
            for p in group:
                if p["bundled"]:
                    continue             # published slugs never move
                old = p["slug"]
                p["slug"] = kebab(p["dirname"])
                collisions.append(
                    f"{kind} slug {old!r} collided; {p['dirname']} -> {p['slug']!r}")
    # Re-check: if the fallback slugs still collide (or two published
    # bundles share one), refuse to overwrite silently.
    recheck = {}
    for p in pages:
        recheck.setdefault((p["kind"], p["slug"]), []).append(p)
    unresolved = {}
    for (kind, slug), group in recheck.items():
        if len(group) > 1:
            unresolved[(kind, slug)] = [p["dirname"] for p in group]
    if unresolved:
        print("ERROR: unresolved slug collisions — these corpus directories "
              "map to the same page and would overwrite each other:",
              file=sys.stderr)
        for (kind, slug), names in sorted(unresolved.items()):
            print(f"  {kind}/{slug}: " + ", ".join(names), file=sys.stderr)
        print("Rename a corpus directory or add a WORK_SLUGS entry, then "
              "re-run. Nothing was written.", file=sys.stderr)
        return 2
    for p in pages:
        section = "blog" if p["kind"] == "blog" else "works"
        p["path"] = f"/{section}/{p['slug']}/"

    # ---- build cross-link URL index ----
    url_index, url_owner = {}, {}

    def index_url(raw, page, priority):
        key, _ = normalize_url(raw)
        if not key or too_generic(key):
            return
        if key in url_index:
            if url_index[key] != page["path"] and priority == 0:
                warnings.append(
                    f"URL index collision: {key!r} claimed by "
                    f"{url_owner[key]} and {page['dirname']}; keeping first")
            return
        url_index[key] = page["path"]
        url_owner[key] = page["dirname"]

    for p in pages:                                   # primary URLs first
        index_url(p["fm"].get("original_url"), p, 0)
        index_url(p["fm"].get("url"), p, 0)
    for p in pages:                                   # then archive URLs
        index_url(p["fm"].get("archive_url"), p, 1)
    # Finally, each blog post's modern-permalink form: scottbot.net moved from
    # /HIAL/?p=NNNN to /<slug>/ permalinks, so old posts are also linked as
    # scottbot.net/<slug>/.  Registered last, so a real original_url always
    # wins the key.
    for p in pages:
        if p["kind"] == "blog":
            index_url(f"http://scottbot.net/{p['slug']}/", p, 2)

    # ---- decide which pages to write ----
    by_dirname = {p["dirname"]: p for p in pages}
    if args.only:
        unknown = [n for n in args.only if n not in by_dirname]
        if unknown:
            print("ERROR: --only names not found in the corpus:\n  " +
                  "\n  ".join(unknown), file=sys.stderr)
            return 2
        to_write = [by_dirname[n] for n in args.only]
        clobbers = [p for p in to_write if p["bundled"]]
        if clobbers and not args.force:
            print("REFUSING: these bundles already exist (add --force to "
                  "rebuild JUST them, losing any hand-edits to them):\n  " +
                  "\n  ".join(p["dirname"] for p in clobbers),
                  file=sys.stderr)
            return 2
    elif full_rebuild:
        to_write = pages
    else:
        to_write = [p for p in pages if not p["bundled"]]
        if not to_write:
            print("Nothing new to ingest: every corpus directory already "
                  "has a bundle. (Use --only NAME --force to rebuild one, "
                  "or --force alone for a full rebuild.)")
    written_names = {p["dirname"] for p in to_write}
    untouched = sum(1 for p in pages
                    if p["bundled"] and p["dirname"] not in written_names)

    # ---- orphans: bundles on disk that no corpus page will claim ----
    # Never deleted (they may be hand-made pages, which are legitimate),
    # but reported so stale strays don't publish silently forever.
    claimed = {(p["kind"], p["slug"]) for p in pages}
    orphans = []
    for kind, root in (("blog", blog_root), ("work", works_root)):
        if root.is_dir():
            for c in sorted(root.iterdir()):
                if (c.is_dir() and (c / "index.md").exists()
                        and (kind, c.name) not in claimed):
                    orphans.append(f"{c.relative_to(site)}")

    # ---- clean only the bundles being rewritten ----
    for root in (blog_root, works_root):
        root.mkdir(parents=True, exist_ok=True)
    for p in to_write:
        bundle = (blog_root if p["kind"] == "blog" else works_root) / p["slug"]
        if bundle.is_dir():
            shutil.rmtree(bundle)

    # ---- pass 2: write bundles ----
    counts = {"blog": 0, "work": 0}
    csv_joined = 0
    missing_images = []
    ignore_junk = shutil.ignore_patterns(*JUNK_FILES, "*.bak")

    for p in to_write:
        csv_row = csv_by_localmd.get(p["dirname"])
        if csv_row:
            csv_joined += 1
        meta = build_frontmatter(p["kind"], p["dirname"], p["fm"], csv_row,
                                 warnings)
        body, caveat_extra = transform_body(p["body"], meta["title"],
                                            url_index, p["path"], stats)
        if caveat_extra:
            if not meta.get("caveat_extra"):
                meta["caveat_extra"] = caveat_extra
            elif meta["caveat_extra"] != caveat_extra:
                warnings.append(
                    f"{p['dirname']}: caveat sentence in the body "
                    f"({caveat_extra!r}) differs from frontmatter "
                    "caveat_extra; keeping the frontmatter one")
        # The template supplies the LLM-conversion caveat on every page; if
        # one survives in the body (e.g. hard-wrapped, so CAVEAT_RE missed
        # it), the page would show it twice.
        if "assisted with an LLM" in body:
            warnings.append(
                f"{p['dirname']}: body still contains an LLM-conversion "
                "caveat the template will duplicate — reflow it onto one "
                "line in the corpus so ingest can strip it")
        section_root = blog_root if p["kind"] == "blog" else works_root
        bundle = section_root / p["slug"]
        bundle.mkdir(parents=True, exist_ok=True)
        # newline="\n": generated files are byte-identical on every OS
        # (Windows must not silently write CRLF).
        with open(bundle / "index.md", "w", encoding="utf-8",
                  newline="\n") as fh:
            fh.write(dump_frontmatter(meta) + body)
        for sub in ("images", "assets"):
            src = p["srcdir"] / sub
            if src.is_dir():
                shutil.copytree(src, bundle / sub, ignore=ignore_junk)
                stats["images_copied"] += sum(
                    1 for f in (bundle / sub).rglob("*") if f.is_file())
        counts[p["kind"]] += 1

        # sanity: images/assets referenced in body must exist in the bundle
        refs = set(re.findall(
            r"[(\"']((?:images|assets)/[^)\s\"'>]+)", body))
        for ref in sorted(refs):
            target = bundle / re.sub(r"[?#].*$", "", ref)
            if not target.exists():
                missing_images.append(f"{p['path']} -> {ref}")

    # ---- workmap.yaml ----
    # Corpus pages get an entry once their bundle actually exists (written
    # this run or already on disk) — never for pages that were merely
    # scanned, which would produce dead links on the CV.  Existing entries
    # for non-corpus pages (e.g. hand-made bundles) survive every mode as
    # long as their page still exists.
    corpus_names = {p["dirname"] for p in pages}
    workmap = {}
    for dirname, path in existing_map.items():
        if dirname in corpus_names:
            continue                     # re-added from pages below
        target = site / "content" / path.strip("/") / "index.md"
        if target.exists():
            workmap[dirname] = path
        else:
            warnings.append(
                f"workmap: dropped entry {dirname!r} -> {path!r} "
                "(no such page exists)")
    workmap.update({p["dirname"]: p["path"] for p in pages
                    if p["dirname"] in written_names or p["bundled"]})
    data_dir = site / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    with open(data_dir / "workmap.yaml", "w", encoding="utf-8",
              newline="\n") as f:
        f.write("# Generated by scripts/ingest.py.  Hand-added entries\n"
                "# survive regeneration as long as their pages exist, but\n"
                "# comments and ordering do not.  Maps original corpus\n"
                "# directory names to site paths.\n")
        yaml.safe_dump(workmap, f, sort_keys=True, allow_unicode=True,
                       default_flow_style=False, width=1000)

    # ---- sources.yaml: site path -> corpus source file ----
    # Lets the work-page caveat link straight to editing the page's actual
    # source on GitHub (which proposes a pull request), instead of the
    # repository's generic pull-request list.  Hand-made pages aren't
    # listed; the template falls back to their content/ file.
    sources = {p["path"]: f"corpus/Markdown/{p['dirname']}/{p['srcname']}"
               for p in pages
               if p["dirname"] in written_names or p["bundled"]}
    with open(data_dir / "sources.yaml", "w", encoding="utf-8",
              newline="\n") as f:
        f.write("# Generated by scripts/ingest.py — do not edit by hand.\n"
                "# Maps each generated page to its corpus source file,\n"
                "# for the caveat's create-a-pull-request link.\n")
        yaml.safe_dump(sources, f, sort_keys=True, allow_unicode=True,
                       default_flow_style=False, width=1000)

    # ---- sanity: every generated index.md must YAML-parse ----
    parse_failures = []
    for root in (blog_root, works_root):
        for idx in sorted(root.glob("*/index.md")):
            text = idx.read_text(encoding="utf-8")
            m = FRONTMATTER_RE.match(text)
            try:
                assert m, "no frontmatter block"
                fm = yaml.safe_load(m.group(1))
                assert isinstance(fm, dict) and fm.get("title"), "no title"
            except Exception as e:
                parse_failures.append(f"{idx}: {e}")

    # ---- report ----
    print("=" * 62)
    print("ingest.py report")
    print("=" * 62)
    print(f"pages written:        {counts['blog']} blog, {counts['work']} works")
    print(f"existing untouched:   {untouched}")
    print(f"images/assets copied: {stats['images_copied']} files")
    print(f"cross-links rewritten:{stats['links_rewritten']:>5} "
          f"(of which self-links: {stats['links_self']})")
    print(f"redundant H1s removed:{stats['h1_removed']:>5}")
    print(f"H1s demoted to H2:    {stats['h1_demoted']:>5}")
    print(f"caveats -> template:  {stats['caveats_stripped']:>5}")
    print(f"CSV joins:            {csv_joined} matched, "
          f"{len(pages) - csv_joined} unmatched dirs, "
          f"{len(csv_by_localmd) - csv_joined} unmatched CSV rows")
    print(f"workmap entries:      {len(workmap)}")
    print(f"skipped dirs:         {len(skipped)}")
    for name, why in skipped:
        print(f"  - {name}: {why}")
    print(f"slug collisions:      {len(collisions)}")
    for c in collisions:
        print(f"  - {c}")
    print(f"orphan bundles:       {len(orphans)}"
          + ("  (not from the corpus; left alone)" if orphans else ""))
    for o in orphans:
        print(f"  - {o}")
    print(f"missing image refs:   {len(missing_images)}")
    for miss in missing_images:
        print(f"  - {miss}")
    print(f"warnings:             {len(warnings)}")
    for w in warnings:
        print(f"  - {w}")
    if parse_failures:
        print("YAML PARSE FAILURES (fatal):")
        for pf in parse_failures:
            print(f"  - {pf}")
        sys.exit(1)
    print("all generated index.md files parse cleanly")
    return 0


if __name__ == "__main__":
    sys.exit(main())
