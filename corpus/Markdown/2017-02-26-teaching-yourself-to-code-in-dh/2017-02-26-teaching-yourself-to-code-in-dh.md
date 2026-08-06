---
title: "Teaching Yourself to Code in DH"
authors:
  - { display: "Scott Weingart" }
post_date: "2017-02-26"
post_date_visible: "February 26, 2017"

blog_title: "the scottbot irregular"
blog_url: "http://scottbot.net/"
blog_platform: "WordPress"

categories: ["method"]
tags: ["digital humanities", "methodologies", "pedagogy"]

original_url: "http://scottbot.net/teaching-yourself-to-code-in-dh/"
archive_url: "https://web.archive.org/web/20180211174245/http://scottbot.net/teaching-yourself-to-code-in-dh/"
archive_date: "2018-02-11"
archive_timestamp: "20180211174245"

language: "en"
comments_preserved: true
comment_count: 5

source_pdf: "Weingart - 2017 - Teaching Yourself to Code in DH.pdf"
source_pdf_sha256: "b31b4352b8d1ddac18c0925d889336701fc526dad60fb7eb37eeaf5f7a9a466f"
extraction_date: "2026-08-02"
extraction_tool: "claude scholarly-blog-html-to-markdown skill (from Wayback print PDF)"
extraction_notes: |
  Source is a browser (Firefox/cairo) print-to-PDF, 7 pages, printed
  4/5/2026, of the Wayback snapshot 20180211174245 of
  scottbot.net/teaching-yourself-to-code-in-dh/. Print header/footer
  ("The Wayback Machine - ...", running title, page N of 7, print
  timestamp), the masthead ("the scottbot irregular" / "data are
  everywhen"), the byline block, the comment-section heading
  ("5 thoughts on "Teaching Yourself to Code in DH""), the gravatar
  images, the site footer and the stray "css.php" link were stripped as
  chrome. Post date, category, tags and permalink come from the printed
  p6 byline ("scott b. weingart / February 26, 2017 / method / digital
  humanities, methodologies, pedagogy") — note the quoted tweet is dated
  February 17, 2017 and the comments February 27, 2017.
  Ligature control characters restored (Merriweather-Regular \x02=fl,
  \x03=fi, \x04=ff); non-breaking spaces kept as printed spaces.
  Hyperlinks reconstructed from PDF link annotations with the
  /web/20180211174245/ Wayback prefix stripped.
  The post body is a two-level bullet list (book entries, each with an
  indented comment) under five bold run-in headings ("Historical
  Analysis", "Literary & Linguistic Analysis", "General Digital
  Humanities", "Statistical Methods & Machine Learning", "Data
  Visualization, Web Development, & Related"); those headings print at
  body size in bold, not as theme headings, so they are kept as bold
  paragraphs. Bullet glyphs come from a separate print font and were
  dropped in favour of Markdown list markers.
  The embedded tweet at the head of the post printed as the theme's
  blockquote fallback and is kept as a blockquote; the emoji in the
  author's Twitter display name printed as a literal "?" ("— Scott B.
  Weingart ? (@scott_bot)") and is kept exactly as printed.
  No images in the post body (the only rasters in the print are the
  byline icon and two comment gravatars) and no footnotes. The theme's
  Genericons "post author" badge (private-use glyph U+F304) printed
  beside the author's own reply and was dropped as an icon.
  Comments: the heading read "5 thoughts on "Teaching Yourself to Code
  in DH"" — two reader comments (Arno Bosse; scott b. weingart's reply)
  and three pingbacks, all preserved verbatim; comment_count counts all
  five.
bibkey: "weingartTeachingYourselfCode2017"
---

# Teaching Yourself to Code in DH

tl;dr Book-length introductions to programming or analytic methods (math / statistics / etc.) aimed at or useful for humanists with limited coding experience.

> *What am I missing from this list of systematic (book-length) introductions to analytic programming in DH? Please add* [*https://t.co/tWjtb54q4T*](https://t.co/tWjtb54q4T)
>
> *— Scott B. Weingart ? (@scott_bot)* [*February 17, 2017*](https://twitter.com/scott_bot/status/832645716371709952)

I’m collecting [programming & methodological textbooks for humanists](https://docs.google.com/spreadsheets/d/1lnmu7ET-HD-kPsbgtWVzf4PlhWx3W6LpKhqup3DWzG0/edit#gid=0) as part of a reflective study on DH, but figured it’d also be useful for those interested in teaching themselves to code, or teachers who need a textbook for their class. Though I haven’t read them all yet, I’ve organized them into very imperfect categories and provided (hopefully) some useful comments. Short coding exercises, books that assume some pre-existing knowledge of coding, and theoretical introductions are not listed here.

Thanks to [@Literature_Geek](https://twitter.com/Literature_Geek), [@ProgHist](https://twitter.com/ProgHist), [@heatherfro](https://twitter.com/HeatherFro), [@electricarchaeo](https://twitter.com/electricarchaeo), [@digitaldante](https://twitter.com/digitaldante), [@kintopp](https://twitter.com/kintopp), [@dmimno](https://twitter.com/dmimno), & [@collinj](https://twitter.com/collinj) for their contributions to the [growing list](https://docs.google.com/spreadsheets/d/1lnmu7ET-HD-kPsbgtWVzf4PlhWx3W6LpKhqup3DWzG0/edit#gid=0). In the interest of maintaining scope, not all of their suggestions appear below.

**Historical Analysis**

<!-- page 2 -->

- [The Programming Historian, 1st edition](http://niche-canada.org/wp-content/uploads/2013/09/programming-historian-1.pdf) (2007). William J. Turkel and Alan MacEachern.
    - An open access introduction to programming in Python. Mostly web scraping and basic text analysis. Probably best to look to newer resources, due to the date. Although it’s aimed at historians, the methods are broadly useful to all text-based DH.
- [The Programming Historian, 2nd edition](http://programminghistorian.org/) (ongoing). Afanador-Llach, Maria José, Antonio Rojas Castro, Adam Crymble, Víctor Gayol, Fred Gibbs, Caleb McDaniel, Ian Milligan, Amanda Visconti, and Jeri Wieringa, eds.
    - Constantly updating lessons, ostensibly aimed at historians, but useful to all of DH. Includes introductions to web development, text analysis, GIS, network analysis, etc. in multiple programming languages. Not a monograph, and no real order.
- [Computational Historical Thinking with Applications in R](http://dh-r.lincolnmullen.com/) (ongoing). Lincoln Mullen.
    - A series of lessons in in R, still under development with quite a few chapters missing. Probably the only programming book aimed at historians that actually focuses on historical questions and approaches.
- [The Rubyist Historian](http://hepplerj.github.io/rubyist-historian/) (2004). Jason Heppler.
    - A short introduction to programming in Ruby. Again, ostensibly aimed at historians, but really just focused on the fundamentals of coding, and useful in that context.
- [Natural Language Processing for Historical Texts](http://nlphist.hypotheses.org/) (2012). Michael Piotrowski.
    - About natural language processing, but not an introduction to coding. Instead, an introduction to the methodological approaches of natural language processing specific to historical texts (OCR, spelling normalization, choosing a corpus, part of speech tagging, etc.). Teaches a variety of tools and techniques.
- [The Historian’s Macroscope](http://www.themacroscope.org/2.0/) (2015). Graham, Milligan, & Weingart.
    - Okay I’m cheating a bit here! This isn’t teaching you to program, but Shawn, Ian, and I spent a while writing this intro to digital methods for historians, so I figured I’d sneak a link in.

**Literary & Linguistic Analysis**

<!-- page 3 -->

- [Text Analysis with R for Students of Literature](http://www.matthewjockers.net/text-analysis-with-r-for-students-of-literature/) (2014). Matthew Jockers.
    - Step-by-step introduction to learning R, specifically focused on literary text analysis, both for close and distant reading, with primers on the statistical approaches being used. Includes approaches to, e.g., word frequency distribution, lexical variety, classification, and topic modeling.
- [The Art of Literary Text Analysis](https://github.com/sgsinclair/alta/blob/master/ipynb/ArtOfLiteraryTextAnalysis.ipynb) (ongoing). Stéfan Sinclair & Geoffrey Rockwell.
    - A growing, interactive textbook similar in scope to Jockers’ book (close & distant reading in literary analysis), but in Python rather than R. Heavily focused on the code itself, and includes such methods as topic modeling and sentiment analysis.
- [Statistics for Corpus Linguistics](https://www.amazon.com/Statistics-Linguistics-Edinburgh-Textbooks-Empirical/dp/0748608176) (1998). Michael Oakes.
    - Don’t know anything about this one, sorry!

**General Digital Humanities**

Many of the above books are focused on literary or historical analysis only in name, but are really useful for everyone in DH. The below are similar in scope, but don’t aim themselves at one particular group.

- [Humanities Data in R](http://humanitiesdata.org/) (2015). Lauren Tilton & Taylor Arnold.
    - General introduction to programming through R, and broadly focused on many approaches, including basic statistics, networks, maps, texts, and images. Teaches concepts and programmatic implementations.
- [Digital Research Methods with Mathematica](https://williamjturkel.net/digital-research-methods-with-mathematica/) (2015). William J. Turkel.
    - A Mathematica notebook (thus, not accessible unless you have an appropriate reader) teaching text, image, and geo-based analysis. Mathematica itself is an expensive piece of software without an institutional license, so this resource may be inaccessible to many learners. [NOTE: Arno Bosse wrote positive feedback on this textbook in a comment below.]
- [Exploratory Programming for the Arts and Humanities](https://www.amazon.com/Exploratory-Programming-Arts-Humanities-Press/dp/0262034204/ref=tmm_hrd_swatch_0?_encoding=UTF8&qid=1488129778&sr=1-1) (2016). Nick Montfort.
    - An introduction to the fundamentals of programming specifically for arts and humanities, languages Python and Processing, that goes through statistics, text, sound, animation, images, and so forth. Much more <!-- page 4 --> expansive than many other options listed here, but not as focused on needs of text analysis (which is probably a good thing).
- [An Introduction to Text Analysis: A Coursebook](http://walshbr.com/textanalysiscoursebook/) (2016). Brandon Walsh & Sarah Horowitz.
    - A brief textbook with exercises and explanatory notes specific to text analysis for the study of literature and history. Not an introduction to programming, but covers some of the mathematical and methodological concepts used in these sorts of studies.
- [Python Programming for Humanists](http://www.karsdorp.io/python-course/) (ongoing). Folgert Karsdorp and Maarten van Gompel.
    - Interactive (Jupyter) notebooks teaching Python for statistical text analysis. Quite thorough, teaching methodological reasoning and examples, including quizzes and other lesson helpers, going from basic tokenization up through unsupervised learning, object-oriented programming, etc.
- [Technical Foundations of Informatics](https://info201.github.io/index.html) (2017). Michael Freeman and Joel Ross.
    - Teaches the start-to-finish skills needed to write code to work with data, from command line to markdown to github to R and ggplot2. Not aimed at humanists, but aimed at those with no prior technical experience.

**Statistical Methods & Machine Learning**

- [Statistics for the Humanities](http://statisticsforhumanities.net/book/) (2014). John Canning.
    - Not an introduction to coding of any sort, but a solid intro to statistics geared at the sort of stats needed by humanists (archaeologists, literary theorists, philosophers, historians, etc.). Reading this should give you a solid foundation of statistical methods (sampling, confidence intervals, bias, etc.)
- [Data Mining: Practical Machine Learning Tools and Techniques, 4th edition](https://www.amazon.com/Data-Mining-Fourth-Techniques-Management/dp/0128042915/ref=mt_paperback?_encoding=UTF8&me=) (2016). Witten, Frank, Hall, & Pal.
    - A practical intro to machine learning in Weka, Java-based software for data mining and modeling. Not aimed at humanists, but legible to the dedicated amateur. It really gets into the weeds of how machine learning works.
- [Text Mining with R](http://tidytextmining.com/) (2017). Julia Silge and David Robinson.
    - Introduction to text mining aimed at data scientists in the statistical programming language R. Some knowledge of R is expected; the authors <!-- page 5 --> suggest using [R for Data Science](http://r4ds.had.co.nz/) (2016) by Grolemund & Wickham to get up to speed. This is for those interested in current data science coding best-practices, though it does not get as in-depth as some other texts focused on literary text analysis. Good as a solid base to learn from.
- [The Curious Journalist’s Guide to Data](https://towcenter.gitbooks.io/curious-journalist-s-guide-to-data/content/) (2016). Jonathan Stray.
    - Not an intro to programming or math, but rather a good guide to quantitatively thinking through evidence and argument. Aimed at journalists, but of potential use to more empirically-minded humanists.
- [Six Septembers: Mathematics for the Humanist](http://digitalcommons.unl.edu/zeabook/55/) (2017). Patrick Juola & Stephen Ramsay.
    - Fantastic introduction to simple and advanced mathematics written by and for humanists. Approachable, prose-heavy, and grounded in humanities examples. Covers topics like algebra, calculus, statistics, differential equations. Definitely a foundations text, not an applications one.

**Data Visualization, Web Development, & Related**

- [Data Visualization for Social Science](http://socviz.co/): A practical introduction with R and ggplot2 (2017). Kieran Healy
    - A “hands-on introduction to the principles and practice of looking at and presenting data using R and ggplot” that introduce readers “to both the *ideas* and the *methods* of data visualization in a comprehensible and reproducible way”. Incredibly thorough, painstakingly annotated, and though not aimed directly at humanists, is close enough in scope to be more valuable than a general introduction to data science.
- [Interactive Information Visualization](https://info474-s17.github.io/book/index.html) (2017). Michael Freeman.
    - Introduction to the skills, tools, and setup required to create interactive web visualizations, briefly covering everything from HTML to D3.js. Not aimed at the humanities, but aimed at those with no prior experience with code.
- [D3.js in Action, 2nd edition](https://www.manning.com/books/d3js-in-action-second-edition) (2017). Elijah Meeks.
    - Introduction to programmatic, online data visualization in javascript and the library D3.js. Not aimed at the humanities, but written by a digital humanist; easy to read and follow. The great thing about D3 is it’s a library for visualizing something in whatever fashion you might imagine, so this is a <!-- page 6 --> good book for those who want to design their own visualizations rather than using off-the-shelf tools.
- [Drupal for Humanists](http://drupal.forhumanists.org/book) (2016). Quinn Dombrowski.
    - Full-length introduction to Drupal, a web platform that allows you to build “environments for gathering, annotating, arranging, and presenting their research and supporting materials” on the web. Useful for those interested in getting started with the creation of web-based projects but who don’t want to dive head-first into from-scratch web development.
- [(Xe)LaTeX appliqué aux sciences humaines](http://geekographie.maieul.net/95) (2012). Maïeul Rouquette, Brendan Chabannes et Enimie Rouquette.
    - French introduction to LaTeX for humanists. LaTeX is the primary means scientists use to prepare documents (instead of MS Word or similar software), which allows for more sustainable, robust, and easily typeset scholarly publications. If humanists wish to publish in natural (or some social) science journals, this is an important skill.

---

## Reader Comments

> **Arno Bosse**, February 27, 2017 at 8:51 am
>
> This is an excellent list — thank you! I’d like to add two quick comments to your note on about Bill Turkel’s entry to flesh it out a bit. The commercial version of Mathematica is expensive. On the other hand, many colleges/universities already have institutional licenses which provides free use of the software. Student pricing w/o an institutional license is $150. ‘Digital Research Methods with Mathematica’ is a Mathematica notebook. But it’s also a c. 130 page equiv. <!-- page 7 --> textbook covering a great many DH methods, accompanied by exercies with answer keys, a full syllabus etc. I think it’s a fantastic resource which promotes the kind of interactive teaching platform we’re starting to see people in the DH community begin to explore with Jupytr notebooks.

>> **scott b. weingart**, February 27, 2017 at 2:56 pm
>>
>> Thanks! I’ve updated the post to point to your comment.

> Pingback: [Resource: Teaching Yourself to Code in DH](http://digitalhumanitiesnow.org/2017/03/resource-teaching-yourself-to-code-in-dh/)

> Pingback: [Digital Humanities Training Opportunities and Challenges – ProfHacker - Blogs - The Chronicle of Higher Education](http://www.chronicle.com/blogs/profhacker/digital-humanities-training-opportunities-and-challenges/63709)

> Pingback: [Five Reasons for Historians to Learn R](http://ds.lib.ucdavis.edu/2017/09/26/five-reasons-for-historians-to-learn-r/)
