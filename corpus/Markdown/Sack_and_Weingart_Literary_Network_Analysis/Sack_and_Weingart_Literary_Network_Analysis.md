---
title: "Literary Network Analysis"
authors:
  - family: "Sack"
    given: "Graham Alexander"
    affiliation: ""
  - family: "Weingart"
    given: "Scott B."
    affiliation: ""

publication_type: "book_chapter"
manuscript_status: "unpublished manuscript / accepted chapter typescript"
container_title: "Digital Humanities for Literary Studies: Theories, Methods, and Practices"
publisher: "Pennsylvania State University Press"
publisher_place: ""

year: 2018
issued: "2018"

doi: ""
language: "en"

source_pdf: "Sack and Weingart - 2018 - Literary Network Analysis.pdf"
source_pdf_sha256: "110953a183b2cbe3ab5c021cfa5af13e722f366edf43e9a8aff1cd402a3b177e"
page_count: 17
extraction_date: "2026-08-02"
extraction_tool: "claude scholarly-pdf-to-markdown skill"
extraction_notes: |
  Word-derived PDF (Acrobat PDFMaker 11 for Word; PDF created 2018-02-21),
  digital-native text layer, no OCR. This is an AUTHOR TYPESCRIPT, not a
  typeset publication: 17 pages, double-spaced, 12pt Times New Roman, ragged
  bottom, no running heads, no printed folios, no journal/publisher masthead.
  Page anchors therefore use PDF page numbers, not printed folios.

  No bibliographic identifier of any kind is printed in the file (no DOI, ISBN,
  ISSN, publisher line, volume, or copyright statement) and the PDF's own
  metadata carries no title/author fields. Network access is not available, so
  no external record was consulted: every metadata field above is transcribed
  from what is PRINTED in the typescript (title, the two author names) or from
  the file's own creation date (2018). Container title, editor, publisher, and
  pages are deliberately left empty rather than invented. The supplied
  curriculum-vitae context (chapter for J. O'Sullivan, ed., "Digital Humanities
  for Literary Studies", Texas A&M University Press; marked UNPUBLISHED) is
  recorded here as external context only and is NOT asserted in the YAML fields.

  Manuscript markup preserved/translated as follows. The typescript uses
  angle-bracket typesetting instructions rather than typographic headings:
  "< Section >" marks a first-level heading and "< < Subsection > >" a
  second-level heading. These are rendered as Markdown "##" and "###"
  respectively (structural markup translated to the target syntax, exactly as a
  bullet glyph would be); the heading wording is verbatim. Figure placeholders
  ("&lt;figure 1 here&gt;", "&lt;Figure 7 here&gt;" - the typescript's own
  inconsistent capitalisation is preserved) are kept verbatim as standalone
  lines. The PDF contains NO figure images at all: nine figures are called for
  by placeholder and none is embedded, so images/ is empty and no figure
  captions exist in the source.

  Underlining is semantically load-bearing in this typescript - the opening
  paragraph states that the companion website "contains a glossary defining
  underlined phrases" - so the 39 underlined glossary terms are preserved with
  &lt;u&gt;...&lt;/u&gt;. Superscript ordinals set by Word ("19&lt;sup&gt;th&lt;/sup&gt;
  century") are preserved with &lt;sup&gt;. Italic and bold-italic runs are
  preserved verbatim.

  Two endnotes sit below Word's footnote-separator rule on the last page; they
  are numbered 1-2 in the source and are emitted under "## Notes" with their
  original numbering. Their in-text markers (superscript 1 after the byline,
  superscript 2 on PDF p. 3) carry internal PDF link annotations to the note
  page; the links are structural, not content, and are not reproduced.

  Whitespace: runs of two or more spaces (Word's double space after sentences)
  are collapsed to one; line-ending hyphens in "hand-coded", "non-verbal", and
  "Rydberg-Cox" are real compound hyphens and were rejoined without a space.
  Angle brackets belonging to the source text are escaped as &amp;lt;/&amp;gt;
  for renderer safety. Bibliography reproduced verbatim, entry order and
  three-em-dash repeated-author form preserved. MANIFEST.txt included.
---

# Literary Network Analysis

<!-- page 1 -->

**Graham Alexander Sack[^1] & Scott B. Weingart**

We live in an interconnected world. The humanities and sciences are converging on an awareness that the world is too complex for reductionist explanations. Context matters, and the connections between entities are as vital to understand as the entities themselves. Network analysis is the formal approach to exploring connectivity, and literary network analysis (<u>LNA</u>) is the application of that method to literary studies. How characters interact in Shakespeare, how social ties drive narrative structure in 19<sup>th</sup> century fiction, how novels cluster based on authorial influence, and how bibliographic content flows through global networks of translation are all questions that can be addressed using LNA.

This chapter divides LNA into two categories: ***textual networks***—<!-- -->that is, networks *within* literary works encompassing properties such as characterization and plot—and ***contextual networks***—that is, networks *outside* of literary works encompassing concerns such as reception and influence. Other forms of LNA (e.g., <u>word co-occurrence networks</u> focused on linguistic properties) exist but are outside the scope of this survey. More information on each can be found at the companion website, which also will be referenced in parentheticals when the site contains expanded material on a given subject. The companion website additionally contains a glossary defining <u>underlined</u> phrases and an expanded bibliography.

Since 2010, precipitated in part by an NEH Advanced Summer Institute in Network Analysis organized by Timothy Tangherlini at UCLA, a surge of network analyses have appeared from different corners of the humanities, ranging from history to linguistics to cultural studies. Though formal literary network analysis rarely appears before 2005, one can trace the sensibility to post-war structuralism.

<!-- page 2 -->

&lt;figure 1 here&gt;

The core assumption of network theory is that systems are composed of entities (<u>nodes</u>) and relationships between them (<u>edges</u>). Like most simplifying assumptions about humanities categories (e.g., the presumed coherence of historical periods or literary genres), this assumption is too reductive, yet provides a useful starting point for interpreting and discussing a text. Nodes may be characters, books, or authors; edges connect nodes, and may describe character interactions, textual similarity, or co-authorship. Network analysis is the application of mathematics to network data in order to learn about the topology of the network as a whole as well as the structural role of individual nodes. LNA may be applied to find structurally central characters, detect hidden communities of authors, or track the changing density of characterization across a Victorian serial.

## Textual Networks

### Theoretical Issues

All network analyses of text begin with some form of <u>entity extraction</u>: characters, objects, actions, place names, or key vocabulary must be identified before the relationships between these entities can be determined. The extraction of characters has been comparatively popular due to the direct applicability of social network analysis (SNA) and the methodological toolbox it provides.

Networks of character interactions can be understood as a means of analyzing the *artificial society* represented by the text. This paradigm entails viewing narratives not merely as depictions of individual experience in language but also as *imaginary social forms*. This perspective has deep historical roots in literary criticism. In *The Country and the City*, for <!-- page 3 --> example, Marxist literary critic Raymond Williams argues that “most novels are in some sense knowable communities” (Williams 1975, 165) and analyzes differences between the forms of social interaction rendered narratable by various British novelists. In *Imagined Communities,* Benedict Anderson argues that, by juxtaposing simultaneous character trajectories, the novel “provided the technical means for re-presenting the kind of imagined community that is the nation” (Anderson 1983, 30). In *The Field of Cultural Production*, Pierre Bourdieu analyzes Flaubert’s *Sentimental Education* as a ‘field of power’ consisting of characters representing competing social positions and literary movements with varying levels of economic and cultural capital (Bourdieu, 1993). In *The One vs. The Many*, Alex Woloch argues that literary characters and their attributes ought to be understood based on their position and structural relations in a socio-narratological field, what he refers to “character-spaces” composing a “character-system” (Woloch 2003).

&lt;Figure 2 here&gt;

Social network analysis provides a means of visualizing and quantifying imaginary social forms and instantiating, measuring, and testing concepts such as Williams’ “knowable communities,” Anderson’s “imagined communities,” Bourdieu’s “fields of power,” or Woloch’s “character spaces.”

Character interactions can also be used to explore *plot*, insofar as character interactions are generally a key narrative element. However, character networks also capture aspects of characterization, social form, and setting, while generally de-emphasizing narrative actions that are solitary or psychological and do not entail social interaction and, as such, should not be used uncritically as proxies for plot.[^2]

<!-- page 4 -->

The construction of character networks as datasets implicitly depends upon a theory of character, a fact sometimes naïvely taken for granted. A crucial question that researchers must answer is what entities ought to count as characters. The following taxonomy may be useful to keep in mind: (1) individualized named characters (e.g., “Esther Summerson”); (2) choral named characters (e.g., “The Poysers”); (3) the unnamed (e.g., “the servant”); (4) the unreferenced, (e.g., characters excluded from direct representation that exist only as a matter of inference—such as the plantation slaves financially supporting Jane Austen’s *Mansfield Park*, famously inferred by cultural critic Edward Said (1993)).

Each category poses practical and theoretical issues and researchers vary in where they draw the line. And where researchers differ, datasets differ, as do conclusions. Because exhaustive lists of characters are rare, even for canonical literary works, a common fallback is the use of named entity recognition (<u>NER</u>), a method of computationally guessing proper names from any chunk of text. This approach generally captures only the first category—individualized named characters. Data and conclusions drawn from such an approach will differ from hand-coded datasets (see the companion website).

A second key question in the construction of character networks is what to count as an an edge. In plays and films, many studies connect characters who appear together or exchange dialogue (see the companion website). In novels, co-occurrence of names or interaction in non-verbal social events may be more relevant (see the companion website). Another question is whether to base connections on the text or the fabula. For example, if Hamlet’s father is murdered by Claudius in the backstory, but these characters never interact during the plot, a network based on the fabula will connect them, while a network based on the text will not. LNA, then, is strongly contingent on researchers’ decisions in creating a dataset.

<!-- page 5 -->

### Narratological Perspectives: Dialogue Networks

As an interdisciplinary mode of inquiry, LNA has appeared from several corners of academia. Mathematicians, physicists, and social scientists often approach literary networks from a ‘mimetic perspective,’ insofar as they are principally concerned with whether the networks in fictional narratives mimic the known properties of real social networks (see the companion website).

By contrast, an emerging body of research published by computational narratologists and digital humanists use network analysis to study the formal properties of narratives.

Franco Moretti’s “Network Theory, Plot Analysis” is intended as a proof-of-concept for literary critics and historians. At its opening, Moretti argues that social network analysis is a crucial new method by which to quantify plot: “What about plot – how can that be quantified? This paper is the beginning of an answer, and the beginning of the beginning is network theory” (Moretti 2011, 80). As a case study, Moretti manually constructs and visually inspects network diagrams for *Hamlet.* Nodes are *dramatis personae*; an edge connects two characters if words pass between them. Moretti emphasizes the position of the characters in the resulting dialogue network, noting that the dramatic status of protagonists is manifested through their central location. Similar to Moretti’s experiments with Shakespeare, in “Social Networks and the Language of Greek Tragedy” (2011), Jeff Rydberg-Cox extracts dialogue networks from classical plays using manual annotations created as part of the Perseus Project.

&lt;Figure 3 here&gt;

In “The Small World of Shakespeare’s Plays,” Stiller, Nettle, and Dunbar (2003) likewise constructed networks of Shakespearean characters based on the criterion that if two characters appear in the same scene, they are connected by an edge. Moretti’s criterion is defined more <!-- page 6 --> narrowly, requiring that the characters speak in succession (a proxy for exchanging dialogue). The methodological differences affect the resulting structures: Moretti’s networks necessarily have lower <u>graph density</u> than Stiller et al.’s. Moreover, since the excluded links disproportionately involve the play’s smaller, more peripheral speaking parts, Moretti’s networks necessarily have more pronounced <u>hubs</u>. <u>Clustering</u> and <u>node centrality</u> also differ. This is important insofar as several of Moretti’s claims hinge on the relative centrality of characters such as Hamlet and MacBeth and the different ways the graphs for the plays fracture if these characters are removed.

Both Moretti and Stiller et al. define edges as social interaction or co-presence between different characters, which necessarily excludes portions of the discourse, notably the soliloquies. In a play such as *Hamlet*, this is a substantial excision. <u>Self-edges</u> could be introduced to represent this component of the text, but with the expense that certain network metrics cannot be calculated. This point highlights the tension between network representation and certain forms of narrative discourse. When using network properties as evidence, scholars may wish to check for invariance under modest modifications to the node and edge extraction criteria. And even when results seem robust, scholars must keep in mind the affordances of the network paradigm; for example, they downplay the role of soliloquies.

In “Extracting Social Networks from Literary Fiction,” Elson, Dames, and McKeown (2010) construct dialogue networks for sixty 19<sup>th</sup> century British novels. Elson et al. differ from Moretti and Rydberg-Cox in their methodology in several ways. While Moretti and Rydberg-Cox manually constructed their networks, Elson et al. uses automatic named entity recognition (<u>NER</u>) and <u>quoted speech attribution</u>. This is necessary both because of the larger size of the corpus and because Elson et al. extract dialogue from novels, which are significantly less <!-- page 7 --> structured than plays. The dialogue networks constructed by Elson et al. rely on methods described in a companion paper, “Automatic Attribution of Quoted Speech in Literary Narrative” (2010). In “The Actor-Topic Model for Extracting Social Networks in Literary Narrative” (2010), Celikyilmaz et al. offer an alternative method for the extraction of dialogue networks based on the *content* of the quote, rather than its context.

Unlike Moretti and Rydberg-Cox, Elson et al. rely on quantitative metrics summarizing network properties rather than on visualization (see the companion website). This difference in methodology reflects a difference in intention: while Moretti and Rydberg-Cox use networks for exploration and hypothesis *discovery*, Elson et al. use networks for hypothesis *testing* and *falsification* (see the companion website). Specifically, they test and find evidence to contradict claims by cultural critic Raymond Williams that novels set in the city have fewer face-to-face interactions than rural novels, which they measure using the prevalence of dialogue as a proxy. Their paper demonstrates the usefulness of LNA as a means of testing and filtering literary and cultural theories about characterization, plot structure, and genre.

Film studies also provides ground for the study of dialogue networks (see the companion website).

### Narratological Perspectives: Networks Based on Description and Narration

The networks constructed by Moretti; Elson et al.; and Celikyilmaz et al. are based on exchanged dialogue between characters. Dialogue, however, is only one mode of narrative discourse. While it accounts for the majority of text in plays and films (excluding, for example, stage directions), it accounts for a minority of most novels. In the novels of Sir Walter Scott, for <!-- page 8 --> example, less than 5% of the text is dialogue. Many examples of LNA extract networks from description and narration.

In “Quantifying Imaginary Social Forms” (2012), Graham Sack constructed social networks of characters across a corpus of sixty 19th century British novels. Like Elson et al., Sack used NER to extract a list of character names within the texts. Two characters were connected if their names co-occurred in the same paragraph, and the edges between them were weighted by frequency of co-occurrences. Sack then calculated network metrics for each novel and regressed them against potential explanatory variables, showing that social network properties of a text are closely related to plot structure and genre. For example, *picaresque* novels tend to have diffuse character networks with low graph <u>density</u>, while *Bildungsromane* tend to have highly <u>centralized</u> networks.

&lt;Figure 4 here&gt;

In “Social Network Analysis of Alice in Wonderland” (2012), Agarwal et al. extract networks from novels using an algorithm detecting social events of two types: (1) A *observes* B, (2) A *interacts* with B. Whereas Sack only requires that two characters be mentioned together in close proximity (capturing an omniscient narratorial view), Agarwal et al. require that the content of the sentence indicate the characters are *aware* of one another (capturing character point of view). By contrasting the position of characters in the network of interactions vs. the network of observations, Agarwal et al. identify differences in the roles of characters in the narratological discourse of *Alice in Wonderland*.

## Relationship Tagging

The edges in Moretti (2011) are <u>unweighted</u> and <u>undirected</u>; those in Sack (2012) are <u>undirected</u> but <u>weighted</u> by frequency; those in Elson et al. (2010) are <u>weighted</u> and <u>directed</u> by <!-- page 9 --> the order of speech. While the edges may differ in strength or direction, in all of these studies the edges are all of the same basic type. Researchers, however, can glean additional insight by constructing networks that capture more nuanced information about the category of social interaction.

In “Facebook for Vikings” (2011), folklorist Timothy Tangherlini argues that the plot structures of Scandinavian story cycles can be understood in terms of shifting alliances and enmities. To represent this in network form, annotators hand-coded relationships between Saga actants into categories such as family, friend, and enemy along with the signifying actions performed, such as “gift-giving” and “lethal hostility.”

Tangherlini’s network analysis is notable as one of the first efforts to describe a narrative using a <u>signed graph</u>, with edge valences indicating amity vs. enmity. <u>Structural balance theory</u> (SBT) (see the companion website) provides a mechanism for evaluating the stability of signed graphs. Unstable relationships may be the basis for narrative event sequences, such as the famous “head ransom” episode in *Egil’s Saga*.

Beyond positive and negative valences, edges can be coded for more sophisticated categories of social interaction. In *Bleak House and Weak Social Networks* (2011), Graham Sack constructed detailed character interaction networks for 19<sup>th</sup> century novels. Edges were classified into <u>strong ties</u>, which included family, profession, neighborhood, and romance, and <u>weak ties</u>, which represented a variety of modern forms of social interaction that emerged in mid-19<sup>th</sup> century England. *Bleak House* is shown to have a disproportionately high prevalence of such weak ties relative to contemporaneous 19<sup>th</sup> century novels.

&lt;figure 5 here&gt;

<!-- page 10 -->

Both Tangherlini (2010) and Sack (2011) hand-coded their complex character relationships. To duplicate these methods on a larger scale, computational methods for relationship classification will need to be developed. <u>Topic analysis</u>, <u>crowdsourcing</u>, and <u>sentiment analysis</u> offer a potential means to do so (see the companion website).

## Contextual Networks

The studies considered above all extract networks from individual texts as a means of representing and analyzing narrative features. LNA, however, is also useful as a means for studying the *context* surrounding individual narratives.

### Influence

The question of how authors influence one another intellectually, socially, and stylistically is an active area of research in contextual network analysis.

In “Network Analysis and the Sociology of Modernism” (2013), Richard So and Hoyt Long construct a network of early 20<sup>th</sup> century American Modernist poets connected by edges to the literary journals in which they published. Their paper is part of a larger endeavor, the University of Chicago’s *Global Literary Networks* project. They use this network to advance arguments regarding the structural roles played by various poets in the development of American Modernism, measuring “influence” with network centrality. So and Long’s analysis of literary influence is based exclusively on publication metadata, not on the content of the texts.

&lt;Figure 6 here&gt;

In *Macroanalysis* (2013)*,* on the other hand, literary historian Matthew Jockers utilizes network analysis to study similarity in style and theme between 19<sup>th</sup> century novelists. For each of 3,346 novels, Jockers extracts (1) relative frequencies of function words (“and,” “of,” “the”, etc.), and (2) the prevalence of various <u>LDA</u>-derived <u>topics</u>. The distance between each novel in <!-- page 11 --> <u>feature space</u> is used as a proxy for similarity and only relationships that go forward in time (*from* novels published earlier *to* novels published later) are preserved. Finally, Jockers colorizes the nodes based on year of publication and author gender. The visualization shows striking ‘macrostructural’ properties: the novels cluster by publication date and author gender despite the fact that the <u>feature vectors</u> contain information on only style and theme (see the companion website).

The objective of Jockers’ study is the examination of *influence*, which has causal implications, while the network constructed represents stylistic and thematic *similarity*, which is correlational: one novel is judged to exert influence on another if it precedes it in publication date and is sufficiently close in feature space. Influence and similarity are difficult to untangle, but future studies may be built on Jockers’ to address potential confounding factors (see the companion website).

### Reception

In “Becoming Yourself: The Afterlife of Reception” (2011), Ed Finn uses LNA to examine the public reception of contemporary literary works through reviews and website recommendations such as on Amazon.com. Finn explores how texts accumulate “prestige” and become canonized through their association with other works in a broader literary field defined by the publishing industry and the internet marketplace. As a case study, Finn constructs a series of <u>egonets</u> for the novels of David Foster Wallace: (a) books that are <u>co-referenced</u> in reviews by professional critics, (b) books that are co-referenced in amateur reviews by consumers on amazon.com, (c) books that are recommended for purchase by amazon.com when users place one of Wallace’s novels in their shopping cart.

<!-- page 12 -->

Finn implicitly equates two different concepts of “<u>prestige</u>.” One definition is used by network theorists and is a measure for centrality in directed graphs. The other definition refers to literary “prestige” in the sense of accumulated cultural capital, as in James English’s work on literary prizes. Future studies may build on Finn’s work by regressing network centrality against data on literary prizes or more recognized measurements for literary prestige.

&lt;Figure 7 here&gt;

### Translation

A third application of contextual network analysis is translation. In “On the Uses and Abuses of ‘Literary Capital’: Culturomics, Translation Networks, and *The World Republic of Letters*” (2014), Graham Sack analyzes the flow of bibliographic content between languages and countries using data from UNESCO’s translation database, covering 700 languages and 2 million book entries. Each language is represented as a node and the volume of bibliographic content translated from one language to another is represented by a weighted and directed edge. The resulting global translation network operationalizes theories of literary and linguistic capital, such as the ‘center-periphery model’ proposed by Pascale Casanova in *The World Republic of Letters* (2004), and conveys differences in the structural roles played by languages as importers, exporters, hubs, and bridges in the global circulation of bibliographic material. The directed networks also illustrate asymmetries in the dynamics of literary translation, representing what linguistic communities *get translated* and which *do the translating*.

&lt;Figure 8 here&gt;

## Conclusion and Future Directions

There are a variety of promising research directions that are all but unexplored in LNA. <!-- page 13 --> First, few published studies meaningfully incorporate node attribute data into the analysis of a narrative’s network. Most analyses treat characters homogeneously: each narrative actant is modeled as an identical node without concern for differences in class, gender, profession, or personality. By including this data in the network representations, it becomes possible to explore the relationship between the structural role that a character plays in a narrative’s network and that character’s attributes. The approach would be particularly fruitful if combined with the use of <u>structural equivalence modeling</u> to identify characters that have similar structural functions in the network (e.g., hubs, welds, bridges, brokers, periphery, or isolates). Likewise, one could examine <u>assortativity</u>, that is, the tendency of nodes to connect with others that are like or unlike themselves. One could then explore questions regarding to whom social power is accorded in a narrative; what attributes are associated with narrative centrality vs. periphery; and what character types tend to function as bridges between disparate plot lines.

Second, if network analysis is to be useful as a mechanism for quantifying plot, it will be necessary to move from *static* to *dynamic* networks. Most studies currently aggregate interactions across the entire text into a single summary network that is backward-looking and static in time. It is possible, however, to represent temporal evolution by applying the techniques to *sequential segments* of a narrative (e.g., each chapter of a novel or scene of a play or film). This substantially expands the explanatory power of LNA. Given that plot is a *pattern in time*, temporal networks are much better-suited to the task of description and analysis. A related area for future exploration is the <u>path dependency</u> of network growth of time; that is, the ways in which early actant interactions constrain the set of possibilities later in the narrative. Such an approach would help to shed light on the way that, for example, the network properties of a narrative’s beginning or middle constrain the properties for its closure and ending. It will also <!-- page 14 --> become possible to examine the evolution of characterization—how particular node-characters accumulate connections and arrive at structural roles in the narrative.

&lt;Figure 9 here&gt;

A third unexplored area is the application of <u>network flows</u> to narrative. In many other types of networks, edges serve as *channels*. In power grids, electricity flows through cables; in traffic networks, vehicles flow through streets. LNA studies have not yet taken this perspective. Edges are treated as static and summative, rather than as infrastructural channels. Tangherlini’s action tagging of *Egil’s Saga* provides a first step here for how one might begin to apply such a perspective to narrative, with edges between characters functioning as channels through which particular forms of action and dialogue flow.

Virtually all extant research applying network analysis to narratives is *descriptive*, involving the extraction of networks from existing narratives. Network structures, however, also have the potential to be deployed for narrative *generation*. Graph structures are widely used in AI planning systems for the representation of causal dependencies (see the companion website). In “Character Networks for Narrative Generation: Structural Balance Theory and the Emergence of Proto-Narratives” (2013), Graham Sack models narrative as a complex system in which the temporal sequence of events constituting a story emerges out of cascading local interactions between nodes in a signed social network. The stability rules of structural balance theory are used as a causal mechanism for narrative events in a network-based simulation. This results in the computational generation of plot structures (see the companion website). Future work in this area may provide a bridge between literary studies, computational narratology, and complex systems theory.

<!-- page 15 -->

The systematic study of networks within and between literary narratives is still in its infancy, and many of its earliest proponents are disconnected from one another by discipline and goals. This critical review offers a path to unify efforts, introduce new practitioners, and build upon some of the earliest groundbreaking work. The companion website expands on important theoretical and methodological concepts, extends the literature review to other varieties of narratives (e.g. film) and disciplinary outlooks (e.g. social sciences), extends the bibliography, and points to tools and instructional resources for getting started in Literary Network Analysis.

## Bibliography

Agarwal, Apoorv, Augusto Corvalan, Jacob Jensen, and Owen Rambow. 2012. Social Network Analysis of Alice in Wonderland. In *Workshop on Computational Linguistics for Literature*, 88–96. Montreal, Canada: Association for Computational Linguistics.

Anderson, Benedict. 1983. *Imagined Communities: Reflections on the Origin and Spread of Nationalism*. New York: Verso.

Bourdieu, Pierre. 1993. *The Field of Cultural Production: Essays on Art and Literature*. Columbia University Press.

Casanova, Pascale. 2004. *The World Republic of Letters*. Harvard University Press.

Celikyilmaz, Asli, Dilek Hakkani-tur, Hua He, Greg Kondrak, and Denilson Barbosa. 2010. The Actor-Topic Model for Extracting Social Networks in Literary Narrative.

Dickens, Charles. 2003. *Bleak House*. Rev Ed edition. New York: Penguin Classics.

Elson, David K, Nicholas Dames, and Kathleen R McKeown. 2010. Extracting Social Networks from Literary Fiction. In *Proceedings of the 48th Annual Meeting of the Association for Computational Linguistics*, 138–47. Association for Computational Linguistics.

Elson, David K., and Kathleen R. Mckeown. 2010. “Automatic Attribution of Quoted Speech in Literary Narrative.” In *Proceedings of the Twenty-Fourth AAAI Conference on Artificial Intelligence*. Atlanta, GA: Association for the Advancement of Artificial Intelligence.

Finn, Ed. 2011. Becoming Yourself: The Afterlife of Reception. *Stanford Literary Lab*, Pamphlets of the Stanford Literary Lab, Pamphlet 3.

Granovetter, Mark S. 1973. The Strength of Weak Ties. *American Journal of Sociology* 78 (6): 1360–80.

<!-- page 16 -->

Jockers, Matthew L. 2013. Influence. In *Macroanalysis: Digital Methods and Literary History*. University of Illinois Press.

Moretti, Franco. 2011. Network Theory, Plot Analysis. *New Left Review* 68: 80–102.

———. 2013. ‘Operationalizing’. *New Left Review*, II (84): 103–19.

Network Analysis for the Humanities. August 15-27, 2010. ODH Institute for Advanced Topics in the Digital Humanities: HT-50016-09. Timothy Tangherlini, PI. UCLA (Los Angeles, CA). https://securegrants.neh.gov/PublicQuery/main.aspx?f=1&gn=HT-50016-09.

Rydberg-Cox, Jeff. 2011. Social Networks and the Language of Greek Tragedy. *Journal of the Chicago Colloquium on Digital Humanities and Computer Science* 1 (3). https://letterpress.uchicago.edu/index.php/jdhcs/article/view/86.

Sack, Graham. 2011a. “Bleak House and Weak Social Networks.” presented at the International Conference on Narrative, St. Louis, MO.

———. 2011b. Simulating Plot: Towards a Generative Model of Narrative Structure. In *Proceedings from the 2011 Association for the Advancement of Artificial Intelligence (AAAI) Fall Symposium (FS-11-03)*.

———. 2012. Quantifying Imaginary Social Forms: Character Networks in the 19th Century British Novel. presented at the North American Victorian Studies Association, Madison, WI.

———. 2013a. Character Networks for Narrative Generation: Structural Balance Theory and the Emergence of Proto-Narratives. In *Proceedings of 2013 Workshop on Computational Models of Narrative*, edited by Mark A. Finlayson, Bernhard Fisseni, Benedikt Lowe, and Jan Christoph Meister, 32. OASICS. Hamburg, Germany: Schloss Dagstuhl--Leibniz-Zentrum fuer Informatik. doi:10.4230/OASIcs.CMN.2013.183.

———. 2013b. Social Network Analysis and Narrative: Reflections on Recent Literature. *Sprache Und Datenverarbeitung* 37.

———. 2014. On the Uses and Abuses of ‘Literary Capital’: Culturomics, Translation Networks, and The World Republic of Letters. presented at the Annual conference of Canadian Society for the Digital Humanities, Brock University, Ontario. http://www.aaai.org/ocs/index.php/FSS/FSS11/paper/view/4230.

Said, Edward W. 1993. *Culture and Imperialism*. Vintage Books.

So, Richard Jean, and Hoyt Long. 2013. Network Analysis and the Sociology of Modernism.” *Boundary 2* 40 (2): 147–82. doi:10.1215/01903659-2151839.

Stiller, James, Daniel Nettle, and Robin I. M. Dunbar. 2003. The Small World of Shakespeare’s Plays. *Human Nature* 14 (4): 397–408. doi:10.1007/s12110-003-1013-1.

<!-- page 17 -->

Tangherlini, Timothy. 2011. Facebook for Vikings. In *Proc Society for the Advancement of Scandinavian Study 2011*. Chicago, IL.

Williams, Raymond. 1975. Knowable Communities. In *The Country and the City*. Oxford: Oxford University Press.

Woloch, Alex. 2003. *The One vs. the Many: Minor Characters and the Space of the Protagonist in the Novel*. Princeton University Press.

## Notes

[^1]: Parts of this chapter appeared in Sack’s 2013 article “Social Network Analysis and Narrative: Reflections on Recent Literature” in *Sprache Und Datenverarbeitung* 37, and are reprinted here with permission.

[^2]: For more discussion of instrumental variables for quantifying plot, see “Simulating Plot: Towards a Generative Model of Narrative Structure” (Sack 2011) or “‘Operationalizing’” (Moretti 2013).

