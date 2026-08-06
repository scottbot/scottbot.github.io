---
title: "Alchemy, Text Analysis, and Networks! Oh my!"
authors:
  - { name: "Scott B. Weingart", source: "inferred from blog ownership; not bylined in post markup" }
post_date: "2011-11-04"
post_date_raw: "Nov 04 2011"

blog_title: "the scottbot irregular"
blog_tagline: "data are everywhen"
blog_url: "http://www.scottbot.net/"
blog_platform: "WordPress"

categories: ["uncategorized"]
tags: ["alchemy", "history", "history of science", "network analysis", "newton", "sci2", "text analysis", "topic modeling", "unicode"]

original_url: "http://www.scottbot.net/HIAL/?p=129"
archive_url: "https://web.archive.org/web/20120309044743/http://www.scottbot.net/HIAL/?p=129"
archive_date: "2012-03-09"
archive_timestamp: "20120309044743"

language: "en-US"

comments_preserved: false
comment_count: 0
pingback_count: 2

source_html: "HIAL.html"
source_html_sha256: "8dca2e9dd57ea6fafcb27b0c84a1a4097c71c892b1b2e938ea8d45c14bdfcb8c"
extraction_date: "2026-04-26"
extraction_tool: "claude scholarly-blog-html-to-markdown skill"
extraction_notes: |
  Wayback toolbar, injected scripts, and SingleFile chrome removed.
  All 5 embedded images decoded from inline base64 data: URIs and saved to images/ — no live-web fetch was needed.
  2 pingback/trackback entries were present in the comment list and stripped per default policy (reader comments would be preserved; pingbacks are not reader content).
  No reader comments were present (only pingbacks).
  Author byline absent from post markup; "Scott B. Weingart" inferred from blog ownership (domain www.scottbot.net). Treat as inferred, not as a verbatim byline.
bibkey: "weingartAlchemyTextAnalysis2012"
---

# Alchemy, Text Analysis, and Networks! Oh my!

“Newton wrote and transcribed about a million words on the subject of alchemy.” –[chymistry.org](http://www.chymistry.org/)

Beside bringing us things like calculus, universal gravitation, and perhaps the inspiration for [certain Pink Floyd albums](http://en.wikipedia.org/wiki/The_Dark_Side_of_the_Moon), Isaac Newton spent many years researching what was then known as “chymistry,” a multifaceted precursor to, among other things, what we now call chemistry, pharmacology, and alchemy.

[![](images/img-001.png "Dark Side of the Moon")](http://www.scottbot.net/HIAL/wp-content/uploads/2011/11/Dark_Side_of_the_Moon.png)

Pink Floyd and the Occult: Discuss.

Researchers at Indiana University, notably [William R. Newman](http://mypage.iu.edu/~wnewman/), [John A. Walsh](http://www.slis.indiana.edu/faculty/jawalsh/), Dot Porter, and Wallace Hooper, have spent the last several years developing [The Chymistry of Isaac Newton](http://www.chymistry.org/), an absolutely wonderful history of science resource which, as of this past month, has digitized all 59 of Newton’s alchemical manuscripts assembled by John Keynes in 1936. Among the sites features are heavily annotated transcriptions, manuscript images, often scholarly synopses, and examples of alchemical experiments. That you can [try at home](http://webapp1.dlib.indiana.edu/newton/reference/mineral.do). That’s right, you can do *alchemy* with this website. They also managed to [introduce alchemical symbols into unicode](http://std.dkuug.dk/jtc1/sc2/wg2/docs/n3584.pdf) (U+1F700 – U+1F77F), which is just indescribably cool.

[![](images/img-002.jpg "Newton's Alchemy")](http://www.scottbot.net/HIAL/wp-content/uploads/2011/11/newtonalchemy.jpg)

Alchemical experiments at home! http://webapp1.dlib.indiana.edu/newton/reference/mineral.do

What I really want to highlight, though, is a brand new feature introduced by Wallace Hooper: [automated Latent Semantic Analysis (LSA) of the entire corpus](http://www.dlib.indiana.edu/education/brownbags/fall2011/newton/newton.pdf). For those who are not familiar with it, LSA is somewhat similar LDA, the algorithm driving the increasingly popular Topic Models used in Digital Humanities. They both have their strengths and weaknesses, but essentially what they do is show how documents and terms relate to one another.

[![](images/img-003.jpg "Newton Project LSA")](http://www.scottbot.net/HIAL/wp-content/uploads/2011/11/newtonLSA.jpg)

Newton Project LSA

In this case, the entire corpus of Newton’s alchemical texts is fed into the LSA implementation ([try it for yourself](http://webapp1.dlib.indiana.edu/newton/lsa/index.php)), and then based on the user’s preferences, the algorithm spits out a network of terms, documents, or both together. That is, if the user chooses document-document correlations, a list is produced of the documents that are *most similar* to one another based on similar word use within them. That list includes weights – how similar are they to one another? – and those weights can be used to create a network of document similarity.

[![](images/img-004.jpg "Newton Document Similarity")](http://www.scottbot.net/HIAL/wp-content/uploads/2011/11/newtonSimilarity.jpg)

Similar Documents using LSA

One of the really cool features of this new service is that it can export the network either as CSV for the technical among us, or as an [nwb](http://nwb.cns.iu.edu/) file to be loaded into the [Network Workbench](http://nwb.cns.iu.edu/) or the [Sci² Tool](https://sci2.cns.iu.edu/user/index.php). From there, you can analyze or visualize the alchemical networks, or you can export the files into a network format of your choice.

[![](images/img-005.jpg "Newton Document Similarity Network")](http://www.scottbot.net/HIAL/wp-content/uploads/2011/11/newtonDocSimilarityNetwork.jpg)

Network of how Newton's alchemical documents relate to one-another visualized using NWB.

It’s great to see more sophisticated textual analyses being automated and actually used. Amber Welch recently posted on [Moving Beyond the Word Cloud](http://blogs.library.duke.edu/dukelibrariesinstruction/2011/10/31/moving-beyond-the-word-cloud/) using the wonderful [TAPoR](http://portal.tapor.ca/portal/portal), and Michael Widner just posted a [thought-provoking article](http://pedagogy.dwrl.utexas.edu/content/automated-text-analysis-revision) on using [Voyeur Tools](http://voyeurtools.org/) for the process of paper revision. With tools this easy to use, it won’t be long now before the first thing a humanist does when approaching a text (or a million texts) is to glance at all the high-level semantic features and various document visualizations before digging in for the close read.
