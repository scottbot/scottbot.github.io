---
title: Visualizing Networks and Temporality
date: 2019-01-01
yearOnly: true
author:
- Melanie Conroy
- Kimmo Elo
- Gerhard Heyer
- Fotis Jannidis
- Malte Rehbein
- Antonis Symvonis
- Scott B. Weingart
worktype: report
venue: Network Visualization in the Humanities (Dagstuhl Seminar 18482)
doi: 10.4230/DagRep.8.11.139
volume: '8'
issue: '11'
pages: 139–153
sbw: SBW-127
citation: Conroy, Melanie, Kimmo Elo, Gerhard Heyer, et al. 2019. Visualizing Networks and Temporality. Dagstuhl Reports. https://doi.org/10.4230/DagRep.8.11.139.
bibkey: conroyVisualizingNetworksTemporality2019
---

## 4.3 Visualizing Networks and Temporality

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
