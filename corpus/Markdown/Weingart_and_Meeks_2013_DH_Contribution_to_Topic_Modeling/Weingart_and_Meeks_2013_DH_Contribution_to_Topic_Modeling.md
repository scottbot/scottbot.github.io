---
title: "The Digital Humanities Contribution to Topic Modeling"
authors:
  - { family: "Meeks", given: "Elijah", affiliation: "Stanford University" }
  - { family: "Weingart", given: "Scott B.", affiliation: "Indiana University" }
publication_type: "article"
container_title: "Journal of Digital Humanities"
journal: "Journal of Digital Humanities"
volume: "2"
issue: "1"
issued: "2013"
year: 2013
url: "https://journalofdigitalhumanities.org/2-1/dh-contribution-to-topic-modeling/"
language: "en"
license: "CC BY 3.0 Unported"
source_pdf: "Weingart and Meeks - 2013 - The Digital Humanities Contribution to Topic Modeling.pdf"
source_pdf_sha256: "83316c429ecbb13f8d3726704d66741daf891cedb2850668f963b3e84d3d1e92"
page_count: 6
extraction_date: "2026-08-01"
extraction_tool: "claude scholarly-pdf-to-markdown skill"
extraction_notes: |
  Source is a Firefox 141/cairo "Print to PDF" of the article page on
  journalofdigitalhumanities.org (snapshot printed 2025-08-11), single column,
  6 printed pages. Web and print chrome stripped: browser print header/footer
  (page title + URL, "N of 6" folio, print timestamp), JDH masthead logo and
  search box, site navigation lists, the issue table-of-contents block on
  page 1, and the PressForward / Roy Rosenzweig CHNM footer logos on page 6.
  Hyperlink targets reconstructed from the PDF's link annotations (Firefox
  preserved them). Footnote markers are printed as superscript bracketed
  numerals [1]-[7]; rendered as Markdown footnotes [^N]. The endnotes are
  printed as an ordered list, each entry prefixed by a superscript bracketed
  numeral and closed by a return-arrow glyph (WordPress footnote-plugin
  chrome); list numbering is carried by the [^N] definitions and the arrows
  are dropped. The two author-portrait images on page 5 were broken (empty
  placeholder boxes) in the snapshot and are not extracted; the page carries
  no other figures, so images/ is empty. The journal masthead dates the issue
  "Vol. 2, No. 1 Winter 2012"; the issue was published in 2013 (the article
  page and CV cite 2013). No DOI printed. Crossref/network not reachable;
  metadata transcribed from the PDF itself.
bibkey: "weingartDigitalHumanitiesContribution2013"
---


# The Digital Humanities Contribution to Topic Modeling

[**Elijah Meeks**](https://journalofdigitalhumanities.org/author/emeeks/) **and** [**Scott B. Weingart**](https://journalofdigitalhumanities.org/author/sweingart/)

Topic modeling could stand in as a synecdoche of digital humanities. It is distant reading in the most pure sense: focused on corpora and not individual texts, treating the works themselves as unceremonious “buckets of words,” and providing seductive but obscure results in the forms of easily interpreted (and manipulated) “topics.” In its most commonly used tool, it runs in the command line. To achieve its results, it leverages occult statistical methods like “dirichlet priors” and “bayesian models.” Were a critic of digital humanities to dream up the worst stereotype of the field, he or she would likely create something very much like this, and then name a popular implementation of it after a hammer.

Since 2010, introductions to topic modeling for humanists have appeared with increasing frequency. Most offer you a list of words, all apparently related yet in no discernible order, identified as a “topic.” You’re introduced to topics, and how a computer came to generate them automatically without any prior knowledge of word definitions or grammar. It’s amazing, you read, but not magic: a simple algorithm that can be understood easily if only you are willing to dedicate an hour or two to learn it. The results would speak for themselves, and a decade ago you would have been forgiven if you imagined only a human could have produced the algorithm’s output. You would marvel at the output, for a moment, before realizing there isn’t much immediately apparent you can actually do with it, and the article would list a few potential applications along with a slew of caveats and dangers. We are ready, now, for a more sustained and thorough exploration of topic modeling. <!-- page 1 -->

In our role as guest editors, we have designed this issue of the *Journal of Digital Humanities* to push the conversation on topic modeling and also to reflect on the larger community in which it is situated. We believe the rapid pace of communication about topic modeling, the focus on workshops and gray literature and snippets of code, the mixed methods invoked and used, are an ideal introduction to what it means to be a digital humanist in a networked world. This is not to say that the issue is another round in defining the digital humanities — far from it — the pieces herein provide an understanding of how to do topic modeling, what to use, its dangers, and some excellent examples of topic models in practice.

Just as tools are enshrined methodologies, methods like topic modeling are reflections of movements. Topic modeling itself is about 15 years old, arriving from the world of computer science, machine learning, and information retrieval. It describes a method of extracting clusters of words from sets of documents. Topic modeling has been applied to datasets in multiple domains, from bioinformatics to comparative literature, and to documents ranging in size from monographs to tweets. One particular variety of topic model, an approach called Latent Dirichlet Allocation (LDA), along with its various derivatives, has been the most popular approach to topic modeling in the humanities.

LDA originated in Michael I. Jordan’s computer science lab in 2002/2003 in collaboration with David M. Blei and Andrew Y. Ng,[^1] and the term LDA has since become nearly synonymous with topic modeling in general. Over the last several years, LDA crept slowly into the humanities world. The software team behind MALLET, by far the most popular tool for topic modeling in the humanities, was led by computer scientist Andrew McCallum and eventually included David Mimno, a researcher with a background in digital humanities. Around the same time, computer scientist David J. Newman and historian Sharon Block collaborated on topic modeling an eighteenth century newspaper,[^2] a project culminating in the history article “Doing More with Digitization”[^3] in 2006. Others at Stanford and elsewhere continued working fairly quietly combining topic modeling with digital humanities for some time, before the explosion of interest that began in 2010.

Two widely circulated blog posts first introduced topic modeling to the broader digital humanities community: Matthew L. Jockers on [topic modeling a Day of DH](http://www.matthewjockers.net/2010/03/19/whos-your-dh-blog-mate-match-making-the-day-of-dh-bloggers-with-topic-modeling/) and Cameron Blevins on [a late eighteenth century diary](http://dh2011abstracts.stanford.edu/xtf/view?docId=tei/ab-173.xml;query=;brand=default). Then at one of the first NEH-funded Institutes for Advanced Topics in the Digital Humanities, held at UCLA in August 2010 and focusing on [network analysis](http://www.ipam.ucla.edu/programs/hum2010/), Mimno, Blei, and David Smith introduced many digital humanists to topic modeling for the first time.[^4] Since that time, dozens of tutorials, walkthroughs, techniques, implementations, and cries of frustration have been posted through various web outlets, often inspiring multithreaded conversations, reply posts, or backchannel Twitter chatter.

In this additional way topic modeling typifies digital humanities: the work is almost entirely represented in that gray literature. While there is a hefty bibliography for spatial analysis in humanities scholarship, for example, in order to follow research that deploys topic modeling for humanities inquiry you must read blogs and attend conference presentations and workshops. For those not already participating in the conversation, this dispersed discussion can be a circuitous and imposing barrier to entry. In addition to sprawling across blogs, tweets, and comment threads, contributions also span methods and disciplines, employ sophisticated visualizations, sometimes delve into statistics and code, and other times adopt the language of literary critique.

This topical issue of the *Journal of Digital Humanities* is meant to catch and present the most salient elements of the topic modeling conversation: a comprehensive introduction, technical details, applications, and critiques from a humanistic perspective. By doing so, we hope to make topic modeling more accessible for new digital humanities scholars, highlight the need for existing practitioners to continue to develop their theoretical approaches, and further sketch out the relationship between this particular method and those of the broader digital humanities community. <!-- page 2 -->

This issue also features an experimental this-space-left-intentionally-blank section; any conversation inspired by this issue over the next month, either [posted as a comment](http://journalofdigitalhumanities.org/2-1/respond-to-jdh-2-1/) or tagged [on Twitter](http://journalofdigitalhumanities.org/2-1/responses-from-twitter/) using [#JDHTopics](https://twitter.com/search?q=%23jdhtopics&src=hash), will eventually be folded into the issue itself as supplemental material. Naturally, this forthcoming section also will include some topic modeling of that material. While we hope the engagement with this issue continues for some time, only material submitted by May 11, 2013 will be included in the final addition to the issue.

## Section 1: Concepts

The creator of LDA, David M. Blei, opens the issue with an original article offering a [grand narrative of topic modeling and its application in the humanities](http://journalofdigitalhumanities.org/2-1/topic-modeling-and-digital-humanities-by-david-m-blei/). He explains the basic principles behind topic modeling, frames it in relation to probabilistic modeling as a field, and explores modeling as a tool for finding and expressing meaning. Blei urges humanities scholars to focus on the model in topic modeling, echoing Willard McCarty’s claim that “modeling points the way to a computing that is *of* as well as *in* the humanities: a continual process of coming to know by manipulating representations.”[^5]

A more [instructional piece](http://journalofdigitalhumanities.org/2-1/topic-modeling-a-basic-introduction-by-megan-r-brett/) is presented by Megan R. Brett, to frame the conversations appearing in this issue. Originally written to introduce students to topic modeling, Brett brings together many invaluable resources and examples. Those unfamiliar with topic modeling will find this piece particularly helpful context for the remaining articles in this special issue.

Next [David Mimno’s presentation](http://journalofdigitalhumanities.org/2-1/the-details-by-david-mimno/), given at the Maryland Institute of Technology and the Humanities (MITH) [topic modeling workshop](http://mith.umd.edu/topicmodeling/) in November 2012, provides the most accessible introduction to the math behind topic modeling available. Mimno argues that those intending to implement topic modeling should understand the details of behind topic modeling, and offers an insightful presentation about how topic models are trained, evaluated, and visualized.

## Section 2: Applications and Critiques

If topic modeling has recently inspired a wealth of introductions for humanists, actual applications written in humanities channels have been harder to come by until very recently. Perhaps two of the most notable projects are Matthew L. Jockers’ forthcoming book *Macroanalysis*, which explores literature using — among other methods — topic modeling,[^6] and David Mimno’s recent article on topic modeling the last century of classics journals.[^7]

Lisa M. Rhody provides a long piece drawn from her dissertation research project that [extends the traditionally thematic-oriented topic modeling to figurative and poetic language](http://journalofdigitalhumanities.org/2-1/topic-modeling-and-figurative-language-by-lisa-m-rhody/). She explores the productive failure of topic modeling, which highlights the processual nature of topic modeling, and reinforces the dialectic with traditional reading. Rhody’s work is perhaps the best evidence thus-far that what we might have identified as cohesive “topics” are more complex than simple thematic connections; indeed, “topics” are more closely related to what Ted Underwood calls “discourses,” a comparison discussed in greater detail within the article. Some of her raw model data is available in an [appendix](http://journalofdigitalhumanities.org/2-1/topic-model-data-for-topic-modeling-and-figurative-language-by-lisa-m-rhody/).

Andrew Goldstone and Ted Underwood offer a [history of literary criticism through topic models of *PMLA*](http://journalofdigitalhumanities.org/2-1/what-can-topic-models-of-pmla-teach-us-by-ted-underwood-and-andrew-goldstone/). In this piece, originally cross-posted on their blogs, they integrate network analysis and representation to better understand and simultaneously complicate the results of the topic models they run. By highlighting the process of topic modeling, Goldstone and Underwood reveal how different methodological choices may lead to contrasting results.

Because topic modeling transforms or compresses free data (raw narrative text) into structured data (topics as a ratio of word tokens and their strength of representation in documents) it is tempting to think of it as <!-- page 3 --> “solving” text. Ben Schmidt [addresses this in an expansion and revision of his earlier critiques of topic modeling and its use in the humanities](http://journalofdigitalhumanities.org/2-1/words-alone-by-benjamin-m-schmidt/). As with other pieces in this edition, his research integrates what are becoming less and less distinct computational methods — in this case data visualization and spatial analysis — to better understand the strengths and weaknesses of topic models. The result is a call for caution in the use of topic modeling because it moves scholars away from interpreting language — their great strength — toward interpreting “topics,” an ill-defined act which might provide the false security of having resolved the distinction between a word and the thing that it represents. Schmidt’s code is available in an [appendix](http://journalofdigitalhumanities.org/2-1/code-appendix-for-words-alone-by-benjamin-m-schmidt/).

## Section 3: Tools

Two tools in particular have enjoyed wide adoption among digital humanists: [MALLET](http://mallet.cs.umass.edu/), produced by Andrew McCallum and computer scientists, and [Paper Machines](https://github.com/chrisjr/papermachines), created and developed by Jo Guldi and Chris Johnson-Roberson. For those looking to try their hand at topic modeling their own sets of documents, the *Programming Historian* includes a [tutorial on MALLET](http://programminghistorian.org/lessons/topic-modeling-and-mallet) by Shawn Graham, Scott B. Weingart, and Ian Milligan; and Sarita Alami of the Emory Digital Scholarship Commons offers a two-part series ([Part I](http://web.library.emory.edu/blog/supercharge-your-zotero-library-using-paper-machines-part-i), [Part II](http://web.library.emory.edu/blog/supercharge-your-zotero-library-using-paper-machines-part-ii-6)) introducing Paper Machines.

Ian Milligan and Shawn Graham, authors of the *Programming Historian*’s [tutorial on MALLET](http://programminghistorian.org/lessons/topic-modeling-and-mallet) (with Scott B. Weingart), offer here [a review not only of how the tool works, but what it means as an instantiation of a method](http://journalofdigitalhumanities.org/2-1/review-mallet-by-ian-milligan-and-shawn-graham/). The review includes links to tutorials and guides to get started, as well as some rumination on the “magic” of topic modeling.

Adam Crymble provides [a review of Paper Machines](http://journalofdigitalhumanities.org/2-1/review-papermachines-by-adam-crymble/), an open source tool which connects with Zotero to analyze sets of documents collected therein. Crymble situates topic modeling in a typical research ecosystem of analysis and search, and ties into the growing prevalence of information visualization techniques of digital humanities work.

## Critical Engagement

In digital humanities research we use tools, make tools, and theorize tools not because we are all information scientists, but because tools are the formal instantiation of methods. That is why MALLET often stands in for topic modeling and topic modeling often stands in for the digital humanities.

The work in this issue integrates the Natural Language Processing technique of topic modeling with network representation, GIS, and information visualization. This approach takes advantage of the growing accessibility of tools and methods that had until recently required great resources (technical, professional, and financial). MALLET is an argument about text using topic modeling that a scholar employs. Scholars can choose to engage with and adjust the algorithms in MALLET. But the tool itself also allows for uncritical use of machinery built for Natural Language Processing.

The humanities is unused to such formal simulacra, however, and so a journal about scholarship might appear to be a journal about tools and software. But none of the authors in this issue simply run and accept the results as “useful” or “interesting” for humanities scholarship. Instead, they critically wrestle with the process. Their work is done with as much of a focus on what the computational techniques obscure as reveal.

Traditional humanities scholars often equate digital humanities with technological optimism. Rather the opposite is true: digital humanists offer the jaundiced realization that computational techniques like topic modeling — long held inaccessible and unapproachable and therefore unassailable — are not an upgrade from simplistic human-driven research, but merely more tools in the ever-growing shed. Whether as part of a particular research agenda, or the method as enshrined in tools, or as a part of a larger movement toward <!-- page 4 --> modeling in the humanities, topic modeling in the humanities has been deployed critically. The adoption of “critical technique” is just what you would expect from scholars accustomed to “critical reading.”

## About Elijah Meeks, and Scott B. Weingart

Elijah Meeks is the Digital Humanities Specialist at Stanford University, where he helps bring network analysis, text analysis, and spatial analysis to bear on traditional humanities research questions. He has worked as the technical lead on The Digital Gazetteer of the Song Dynasty, Authorial London, and ORBIS: The Stanford Geospatial Network Model of the Roman World. In his time at Stanford, he's worked with Mapping the Republic of Letters, the Stanford Literary Lab, and the Spatial History Lab, as well as individual faculty and graduate students, to explore a wide variety of digital humanities research questions.

Scott B. Weingart is an NSF Graduate Research Fellow and PhD student at Indiana University, where he studies Information Science and History of Science. His research focuses on the intersection of historiographic and quantitative methodologies, particularly as they can be used to study scholarly communications in the past and present. He also writes a blog called the [scottbot irregular](http://www.scottbot.net/HIAL/), aiming to make computational tools and big data analytics accessible to a wider, humanities-oriented audience. When not researching, Scott fights for open access and the reform of modern scholarly communication. <!-- page 5 -->

[Creative Commons License](http://creativecommons.org/licenses/by/3.0/)This work is licensed under a [Creative Commons Attribution 3.0 Unported License](http://creativecommons.org/licenses/by/3.0/). <!-- page 6 -->

[^1]: David M. Blei, Andrew Y. Ng, and Michael I. Jordan, “Latent Dirichlet allocation,” *Journal of Machine Learning Research* 3 (4–5) (2003): 993–1022. doi:10.1162/jmlr.2003.3.4-5.993.

[^2]: D.J. Newman and S. Block, [Probabilistic topic decomposition of an eighteenth-century American newspaper](http://www.ics.uci.edu/~newman/pubs/JASIST_Newman.pdf), *Journal of the American Society for Information Science and Technology* 57(6) (2006): 753–767. doi:10.1002/asi.20342.

[^3]: S. Block, “[Doing More with Digitization](http://www.common-place.org/vol-06/no-02/tales/),” *Common-Place* 6(2) (2006).

[^4]: Clay Templeton describes this narrative in more detail at the [MITH blog](http://mith.umd.edu/topic-modeling-in-the-humanities-an-overview/).

[^5]: W. McCarty, “Modeling: A Study in Words and Meanings,” in *A Companion to Digital Humanities*, ed. Susan Schreibman, Ray Siemens, John Unsworth (Oxford: Blackwell, 2004) [http://www.digitalhumanities.org/companion/](http://www.digitalhumanities.org/companion/).

[^6]: M. L. Jockers, *Macroanalysis: Digital Methods and Literary History*  (University of Illinois Press, 2013).

[^7]: D. Mimno, “Computational historiography: Data mining in a century of classics journals,” *Journal on Computing and Cultural Heritage* 5 (1) (2012): 3:1–3:19. doi:10.1145/2160165.2160168.
