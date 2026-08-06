---
title: "Submissions to DH2016 (pt. 1)"
authors:
  - { display: "Scott Weingart" }
post_date: "2015-12-07"
post_date_visible: ""

blog_title: "the scottbot irregular"
blog_url: "http://www.scottbot.net/HIAL/"
blog_platform: "WordPress"

categories: ["personal research"]
tags: ["data analysis", "dhconf", "digital humanities", "scholarly communication"]

original_url: "http://www.scottbot.net/HIAL/?p=41533"
archive_url: "https://web.archive.org/web/20160304152425/http://www.scottbot.net/HIAL/?p=41533"
archive_date: "2016-03-04"
archive_timestamp: "20160304152425"

language: "en"
comments_preserved: true
comment_count: 4

source_pdf: "Weingart - 2015 - Submissions to DH2016 (pt. 1).pdf"
source_pdf_sha256: "7bcc9289c2581b4f99d49be66857648895c33d5ab9b5f38eee84c6b144c0a316"
extraction_date: "2026-08-02"
extraction_tool: "claude scholarly-blog-html-to-markdown skill (from Wayback print PDF)"
extraction_notes: |
  Post date confirmed as 2015-12-07 from the Wayback capture of the blog's monthly archive
  page (scottbot.net), which prints the dateline the single-post print omitted.
  Source is a browser print (2026-04-05) of Wayback snapshot 20160304152425
  of http://www.scottbot.net/HIAL/?p=41533. The print header truncates the
  URL ("...scottbot.net..."); the post id 41533 was recovered from the
  snapshot's own reply permalinks (?p=41533&replytocom=...).
  POST DATE IS YEAR-ONLY: the Independent Publisher theme printed no dateline.
  The post's four comments are dated December 7-8, 2015, and its images were
  uploaded to wp-content/uploads/2015/12/, so the post is from early December
  2015 (on or just before December 7). The exact day is undeterminable from
  this print, so the folder uses the <year>-<slug> form; the caveat is flagged
  in the review notes.
  Print header/footer, the Wayback banner line, the "Write a Comment"
  headings (Genericons glyph plus label), "Reply to ..." links, the three
  commenter avatars, the "READERS WHO SHARED THIS / THANK YOU!" trackback
  widget and its one entry (DHBENELUX 2016 SUBMISSIONS | MAX KEMMAN,
  http://www.maxkemman.nl/2016/02/dhbenelux-2016-submissions/), the RELATED
  CONTENT BY TAG cloud (moved to YAML tags) and the theme footer credit were
  stripped as chrome. Category "personal research" (?cat=57).
  Images: 3 charts, each hyperlinked in the post to its full-size upload on
  i1.wp.com / i2.wp.com (links preserved on the images). img-003, the tall
  topics chart, prints across pages 3-5; its complete 549x2054 raster is
  embedded on pages 3 and 4 (and a duplicate bottom crop on page 5) and was
  extracted once, from page 3. The two captions the theme printed below
  img-001 and img-002 are kept as italic caption paragraphs.
  Justified-print end-of-line hyphenation dehyphenated (joins logged in the
  review notes). Hyperlinks reconstructed from the PDF link annotations and
  un-rewritten from their /web/<timestamp>/ Wayback form; none guessed.
  Source spellings and typos preserved (the double space in "XML & text
  encoding,  internet & social media-related topics", "It may be while
  before I upload the next section").
  All 4 reader comments preserved with nesting to depth 4; the bare URLs in
  the last comment carry the post's own link annotations.
bibkey: "weingartSubmissionsDH2016Pt2015"
---

# Submissions to DH2016 (pt. 1)

<!-- page 1 -->

tl;dr Basic numbers on DH2016 submissions.

Twice a year I indulge my meta-disciplinary sweet tooth: once to look at who’s submitting what to [ADHO’s annual digital humanities conference](http://adho.org/conference), and once to look at which pieces get accepted (see [the rest of the series](http://www.scottbot.net/HIAL/?tag=dhconf)). This post presents my first look at DH2016 conference submissions, the data for which I scraped from [ConfTool](https://www.conftool.pro/dh2016/) during the open peer review bidding phase. Open peer review bidding began in 2013, so I have 4 years of data. I opt not to publish this data, as most authors submit pieces under an expectation of privacy, and might violently throw things at my face if people find out which submissions weren’t accepted. Also ethics.

## Submission Numbers & Types

The basic numbers: 652 submissions (268 long papers, 223 short papers, 33 panels / multiple paper sessions, 128 posters). For those playing along at home, that’s:

- 2013 Nebraska: 348 (144/118/20/66)
- 2014 Lausanne: 589 (250/198/30/111)
- 2015 Sydney: 360 (192/102/13/53)
- 2016 Kraków: 652 (268/223/33/128)

<!-- page 2 -->

[![Stacked bar chart, 'Submission Types per Year': long papers, short papers, panels and posters as shares of DH2013-DH2016 submissions](images/img-001.png)](http://i2.wp.com/www.scottbot.net/HIAL/wp-content/uploads/2015/12/dh2016-subbytype.png)

*Comparisons of submission types to DH2013-DH2016*

DH2016 submissions are on par to continue the [consistent-ish trend of growth every year since 1999](http://www.scottbot.net/HIAL/?p=41327), the large dip in 2015 unsurprising given its very different author pool, and the fact that it was the first time the conference visited the southern hemisphere or Asia-Pacific. The different author pool in 2015 also likely explains why it was the only conference to deviate from the normal submission-type ratios.

## Co-Authorship

Regarding co-authorship, the number has shifted this year, though not enough to pass any significance tests.

[![Line chart, '% of submissions with x co-authors', one line per year 2013-2016](images/img-002.png)](http://i1.wp.com/www.scottbot.net/HIAL/wp-content/uploads/2015/12/co-author-distribution-16.png)

<!-- page 3 -->

*Co-authorship in DH2013-DH2016 submissions.*

DH2016 has proportionally slightly fewer single authored papers than previous years, and slightly more 2-, 3-, and 4-authored papers. One submission has 17 authors (not quite the [5,154-author record of high energy physics](http://journals.aps.org/prl/abstract/10.1103/PhysRevLett.114.191803), but we’re getting there, eh?), but mostly it’s par for the course here.

## Topics

Topically, DH2016 submissions continue many trends seen previously.

Authors must tag their submissions into multiple categories, or topics, using a controlled vocabulary. The figure presents a list of topics tagged to submissions, ordered top-to-bottom by the largest proportion of submissions with a certain tag for 2016. Nearly 25% of DH2016 submissions, for example, were tagged with “Text Analysis”. The dashed lines represent previous years’ tag proportions, with the darkest representing 2015, getting lighter towards 2013. New topics, those which just entered the controlled vocabulary this year, are listed in red. They are 3D Printing, DH Multilinguality, and DH Diversity.

Scroll past the long figure below to read my analysis:

[![Long horizontal bar chart, 'DH2016 Submission Topics': the share of submissions tagged with each topic in 2016, with dashed outlines for 2013-2015 and new topics in red](images/img-003.png)](http://i1.wp.com/www.scottbot.net/HIAL/wp-content/uploads/2015/12/dh2016-topics.png)

<!-- page 5 -->

In a reveal that will shock all species in the known universe, text analysis dominates DH2016 submissions—the proportion even grew from previous years. Text & data mining, archives, and data visualization aren’t far behind, each growing from previous years.

What did actually (pleasantly) surprise me was that, for the first time since I began counting in 2013, history submissions outnumber literary ones. Compare this to 2013, [when literary studies were twice as well represented as historical](http://www.scottbot.net/HIAL/?p=24437). Other top-level categories experiencing growth include: corpus studies, content analysis, knowledge representation, NLP, and linguistics.

<!-- page 6 -->

Two areas which I’ve pointed out previously as needing better representation, geography and pedagogy, both grew compared to previous years. I’ve also pointed out a lack of discussion of diversity, but part of that lack was that authors had no “diversity” category to label their research with—that is, the issue I pointed out may have been as much a problem with the topic taxonomy as with the research itself. ADHO added “Diversity” and “Multilinguality” as potential topic labels this year, which were tagged to 9.4% and 6.5% of submissions, respectively. One-in-ten submissions dealing specifically with issues of diversity is encouraging to see.

Unsurprisingly, since Sydney, submissions tagged “Asian Studies” have dropped. Other consistent drops over the last few years include software design, A/V & multimedia (sadface), information retrieval, XML & text encoding,  internet & social media-related topics, crowdsourcing, and anthropology. The conference is also getting less self-referential, with a consistent drop in DH histories and meta-analyses (like this one!). Mysteriously, submissions tagged with the category “Other” have dropped rapidly each year, suggesting… dunno, aliens?

I have the suspicion that some numbers are artificially growing because there are more topics tagged per article this year than previous years, which I’ll check and report on in the next post.

It may be while before I upload the next section due to other commitments. In the meantime, you can fill your copious free-time reading [earlier posts on this subject](http://www.scottbot.net/HIAL/?tag=dhconf) or my recent book with Shawn Graham & Ian Milligan, [The Historian’s Macroscope](http://www.themacroscope.org/2.0/). Maybe you can [buy it](http://www.worldscientific.com/worldscibooks/10.1142/p981) for your toddler this holiday season. It fits perfectly in any stocking (assuming your stockings are infinitely deep, like Mary Poppins’ purse, which as a Jew watching Christmas from afar I just always assume is the case).

---

## Reader Comments

> **Stephen Robertson**, December 7, 2015
>
> Are submissions tagged ‘historical studies’ really all history submissions? I’ve never been able to get the proportions in the meta view to jibe with the digital history papers that I can actually find in the program. I wonder, for example, if literary or linguistics papers are tagged ‘historical studies’ if they use historical data?

>> **Scott Weingart**, December 7, 2015
>>
>> Good point, thanks, it’s definitely a poor proxy. I wouldn’t be surprised if, systematically, “historical studies” is less likely to refer to work done by people in history departments than “literary studies” is likely to point to work done by literary scholars. History can be historical linguistics, literary history, etc.
>>
>> That said, unless tagging practices have changed or authors are allowed to use more tags per submission this year than previous years, it’s still worth noting that the “historical studies” tag has grown tremendously. It may be that all the growth statistically depends upon the growth another tag (e.g. linguistics or literature), which I’ll make a point of checking for in the next post now that you bring it up, but I suspect we’ll find that “traditional” history is increasing with the rest of the tag, even if the tag doesn’t always represent it.

>>> [**acrymble**](http://genderedacademia.wordpress.com/), December 8, 2015
>>>
>>> These are submissions, so I’ll be interested to see if this historical turn makes it through the peer review.

>>>> **Scott Weingart**, December 8, 2015
>>>>
>>>> In 2013, 2014, and 2015, “historical studies” have an acceptance rate slightly below average, and literary studies have acceptance rates slightly above average. This is consistent across years. I’d be surprised if that changed this year, even with the larger historical studies tag, but even if it doesn’t, the difference in acceptance rates is small enough that I imagine the historical turn will remain present in the final conference. (see [http://www.scottbot.net/HIAL/wp-content/uploads/2014/04/acceptance-topic-sortbyaccrate.png](http://www.scottbot.net/HIAL/wp-content/uploads/2014/04/acceptance-topic-sortbyaccrate.png) & [http://www.scottbot.net/HIAL/wp-content/uploads/2015/06/AccRateByRate.png](http://www.scottbot.net/HIAL/wp-content/uploads/2015/06/AccRateByRate.png) )
