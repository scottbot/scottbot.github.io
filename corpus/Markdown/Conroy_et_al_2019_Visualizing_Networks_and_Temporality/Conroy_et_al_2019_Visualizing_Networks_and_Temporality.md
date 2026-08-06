---
title: "Visualizing Networks and Temporality"
authors:
  - { family: "Conroy", given: "Melanie", affiliation: "University of Memphis, US" }
  - { family: "Elo", given: "Kimmo", affiliation: "University of Turku, FI" }
  - { family: "Heyer", given: "Gerhard", affiliation: "Universität Leipzig, DE" }
  - { family: "Jannidis", given: "Fotis", affiliation: "Universität Würzburg, DE" }
  - { family: "Rehbein", given: "Malte", affiliation: "Universität Passau, DE" }
  - { family: "Symvonis", given: "Antonis", affiliation: "National TU – Athens, GR" }
  - { family: "Weingart", given: "Scott", affiliation: "Carnegie Mellon University – Pittsburgh, US" }
editors:
  - { family: "Börner", given: "K." }
  - { family: "Eide", given: "O." }
  - { family: "Mchedlidze", given: "T." }
  - { family: "Rehbein", given: "M." }
  - { family: "Scheuermann", given: "G." }
publication_type: "report"
container_title: "Network Visualization in the Humanities (Dagstuhl Seminar 18482)"
journal: "Dagstuhl Reports"
volume: "8"
issue: "11"
pages: "139–153"
event: "Dagstuhl Seminar 18482"
year: 2019
doi: "10.4230/DagRep.8.11.139"
language: "en"
license: "Creative Commons BY 3.0 Unported"
source_pdf: "Conroy et al. - 2019 - Visualizing Networks and Temporality.pdf"
source_pdf_sha256: "bb1e34e8010dd34074a818979b12fa335cb4d2a0afe1cc330113338cd319e93b"
page_count: 2
extraction_date: "2026-08-01"
extraction_tool: "claude scholarly-pdf-to-markdown skill"
extraction_notes: |
  Two-page Firefox/cairo print-to-PDF excerpt of Dagstuhl Reports 8(11), printed
  folios 149-150. Scope is section 4.3 only ("Visualizing Networks and
  Temporality", the document named by the coordinator); printed page 150 also
  carries the opening of the following section 4.4 (Börner et al., "Uncertainty
  Visualization in Digital Humanities (DH) Network Data"), which is a different
  report section, truncated mid-sentence at the excerpt's edge, and excluded as
  out of scope. Running heads (editor list on the left-hand folio, seminar
  number and title on the right-hand folio) and the seminar-number page-foot
  stamp were stripped; printed folios preserved as HTML-comment page anchors.
  The text layer encodes ff/fi/ffi ligatures as private-use codepoints; these
  were normalized to letter pairs. Transcription is AS PRINTED: the body's
  first sentence spells two names "Fotis Jannadis" and "Antonic Symvonis"
  (sic, as printed), though the byline gives Jannidis and Antonis Symvonis.
  Byline and license/copyright block reproduced in the body as well as in YAML;
  the byline is set in italic in the source and rendered bold per this
  project's convention. The Creative Commons "CC" badge after the word
  License is a graphic glyph absent from the text layer and is not
  reproduced.
  No figures, tables, footnotes, or references occur in this section; images/
  is intentionally empty. The PDF carries no hyperlink annotations (cairo
  print). Network/Crossref unreachable in this environment: DOI, journal,
  volume/issue, and year come from the coordinator-supplied citation, not the
  PDF; author/editor names, affiliations, pages, seminar number, and license
  come from the printed pages. Full-report DOI given (the section has no DOI
  of its own printed here).
bibkey: "conroyVisualizingNetworksTemporality2019"
---

# 4.3 Visualizing Networks and Temporality

**Melanie Conroy (University of Memphis, US), Kimmo Elo (University of Turku, FI), Gerhard Heyer (Universität Leipzig, DE), Fotis Jannidis (Universität Würzburg, DE), Malte Rehbein (Universität Passau, DE), Antonis Symvonis (National TU – Athens, GR), and Scott Weingart (Carnegie Mellon University – Pittsburgh, US)**

**License** Creative Commons BY 3.0 Unported license\
© Melanie Conroy, Kimmo Elo, Gerhard Heyer, Fotis Jannidis, Malte Rehbein, Antonis Symvonis, and Scott Weingart

The members of the temporality working group were Melanie Conroy, Kimmo Elo, Gerhard Heyer, Fotis Jannadis, Malte Rehbein, Antonic Symvonis, and Scott Weingart. We discussed both ways to graph temporal networks and how to visualize data in the Humanities that include networks. While we discussed problems which could be addressed using temporal graphs, we found that temporal graphs could often not be constructed from the datasets with which we were familiar. Our discussion focused on how to incorporate non-linear time sequences and ways of perceiving time that differ from chronological time into network diagrams and other visualisations. After attempting to construct network graphs for various use cases, we discovered that many problems in the Humanities do not permit the construction of a temporal network graph due to multiple perspectives on the network and variable or uncertain time sequences. While we discussed ways to reduce the number of perspectives and series, however, we rejected the idea of reducing the complexity of data models. We decided that starting with the visualizations that we needed for a number of case studies would be more valuable than attempting to reduce the complexity of humanities research questions to make them graphable as a single network. For this reason, we decided to work backwards from the types of visualisations needed for individual projects to the data model that would be necessary to produce such a visualisation.

Problems that appeared repeatedly in our discussions of the temporality of networks in the Humanities included a mismatch between methodology (data models and metrics) and available technology, different data models and collection practices in various humanities fields, and project-specific data models. We also discussed incomplete or uncertain data and shifting or incommensurable perspectives related to time. We decided that no one visualisation or set of visualisations would be adequate to deal with all of these issues.

We discussed four main use cases for networks in the Humanities:

1. Story vs. Discourse – Literary character networks, in which the nodes are literary characters and the edges are co-occurrences in a series of scenes.
2. Word Co-Occurrence – Evolution of word use over time (word careers), in which the nodes are words and co-occurence in a text is represented by the edges.
3. Republic of Letters – Correspondence networks, in which the nodes are correspondents and the edges are letters.
4. Reports of Secret Police – Network model of the evolving knowledge of investigators into the relations of conspirators, in which each agent has a different view on the network of possible conspirators and nodes in the network appear and disappear as the police discover more about the network.

One idea that recurred frequently in our discussion was “snapshots” of a network which could be arranged into series by linking them to produce sequences instead of graphing a single temporal network. We designed and refined visualizations which could be used in each of these cases. Solutions included a stream graph of centrality and centralization, dyad visualization, temporal / witness matrix, collation networks, and a discourse/story/perspective model of <!-- page 149 --> networks. Our solution to the problems presented by the variety and complexity of humanities data models was to combine network visualizations with representations of how the data was modeled–for example, placing network diagrams in a matrix that shows both the state of the network over time and how the network appears according to various perspectives which are made explicit in witness reports. By using a matrix, for example, we can show the state of a network across time according to various perspectives, such as witnesses to a series of events, or changes in the network.

For all four of our use cases, the combination of multiple visualisations was necessary to convey the most significant information about how the network was structured and how it developed over time; these visualisations could include a timeline or scatterplot to show the place in the temporal sequence of the network currently being visualized. <!-- page 150 -->
