# CV data schema (Hugo data files)

Every CV section lives in its own YAML file under `data/cv/`. All files are lists or
small maps. General principles:

1. **Text is Markdown.** Italics as `*...*`, bold as `**...**`, links as `[text](url)`.
   Ampersands are written as plain `&` — the site CSS/templating styles them italic.
2. **Normalize ligature glyphs.** The PDF extraction contains presentation forms
   (ﬁ ﬂ ﬆ etc.) — write plain letters (`fi`, `fl`, `st`). Keep curly quotes, en/em
   dashes, and accented characters exactly as in the CV.
3. **Verbatim fidelity.** Reproduce the CV's wording, punctuation, and ordering exactly.
   Do not editorialize, expand, or "fix" anything.
4. **`year` is a string** shown in the left margin gutter: `"2023–2025"`, `"2014"`,
   `"forthcoming"`, `"ongoing"`, `"unpublished"`, or `""` when the CV shows none
   (entries under the same year show it only once — put the year ONLY on the first
   entry of a year group, `""` on the rest, mirroring the CV).
5. **`note` is the right-margin annotation** exactly as printed: `"150+ citations"`,
   `"award-winning; 40+ citations"`, `"bestseller"`, `"> 10k visitors"`, `"signif. revisions"`,
   `"Until DOGE"`. Omit the key when there is none. Multi-line margin notes: keep on
   one line separated by "; " unless the CV separates two distinct notes (then use a list).
6. **`icon: manicule`** where the CV prints the printer's-fist ☞ pointing at the note.
7. **`work:`** — when an entry corresponds to a converted full-text work, give the
   corpus folder name from sbw_map.json's `slug` field (e.g. `work: "Network Turn"`).
   **`sbw:`** — the SBW-ID when one exists (e.g. `sbw: SBW-002`). Match by title/year;
   omit both if no match.

## Generic dated-entry sections
(appointments.yaml, education.yaml, awards.yaml, keynotes and other talk files,
teaching.yaml, projects.yaml, consulting.yaml, service files, grant-affiliations.yaml,
press.yaml, blog-posts.yaml)

```yaml
- year: "2023–2025"
  text: "**National Endowment for the Humanities, United States Government**"
  sub:                                  # optional indented lines under the entry
    - "Inaugural Chief Data Officer"
    - "Inaugural Director, *Office of Data and Evaluation*"
  note: "Until DOGE"                    # optional
  icon: manicule                        # optional
  work: "..."                           # optional
  sbw: SBW-000                          # optional
```

For simple one-line sections, `text` alone suffices. Preserve any trailing period style.

## publications.yaml
A map of subsections, in CV order, each with a `title`, optional `subtitle`
(e.g. "peer reviewed"), and `entries`:

```yaml
sections:
  - key: academic-books
    title: "Academic Books"
    subtitle: "peer reviewed"
    entries:
      - year: "2020"
        citation: "Ahnert, R., Ahnert, S.E., Coleman, N., & Weingart, S.B. (2020). *The Network Turn*. Cambridge: Cambridge University Press. [10.1017/9781108866804](https://doi.org/10.1017/9781108866804)"
        note: "150+ citations"
        work: "Network Turn"
        sbw: SBW-002
```

DOIs printed in the CV become links as shown. Author name "Weingart, S.B." stays
plain text (the site bolds/colors it automatically — do NOT mark it up).

## roles.yaml (Roles & Responsibilities)
```yaml
- institution: "Library of Virginia"
  positions:
    - "**Inaugural Chief Technology Officer**"
  body: |            # markdown; bullets as "- " lists where the CV uses dashes;
    Provides strategic vision ...
```
Underlined lead-ins in the NEH entry ("Executive Leadership.") → bold markdown.

## highlights.yaml
```yaml
- title: "Service-Oriented Leader"
  body: "Four-time inaugural director ..."
```

## profile.yaml (single map, not list)
name, tagline (markdown, e.g. "**Historian** masquerading as a **Chief Technology Officer**"),
phone, email (shown on the page), email_mailto (where the link actually sends,
e.g. a plus-tagged alias), web, mission (the italic two-line statement).

## reviews.yaml (Selected Reviews & Related Consequents)
List of works, each with `work_title`, optional `work`/`sbw`, and `items` (list of
review strings, verbatim, markdown links where the CV shows sources).
Check the actual layout on pages 19–20 and mirror it.

## Prose files (markdown, not YAML)
- biography.md — Extended Biography, single flowing markdown (bold runs preserved).
- by-the-numbers.md — verbatim.
- colophon-notes.md — transcription of the printed colophon page 29 (verbatim,
  including the archaic typography as printed: medial ſ, yᵉ, u/v & i/j transpositions —
  transcribe the *characters actually printed*), plus a note listing the five colors.
