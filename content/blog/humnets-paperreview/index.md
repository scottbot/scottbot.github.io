---
title: '#humnets paper/review'
date: 2011-10-22
author:
- Scott B. Weingart
worktype: blog
venue: the scottbot irregular
original_url: http://www.scottbot.net/HIAL/?p=80
archive_url: https://web.archive.org/web/20111103061616/http://www.scottbot.net/HIAL/?p=80
sbw: SBW-011
bibkey: weingartHumnetsPaperReview2011
---

by *scottbot* — 2011-10-22 — filed under *Uncategorized*

UCLA’s Networks and [Network Analysis for the Humanities](http://www.ipam.ucla.edu/scheduleprint.aspx?pc=hum2011) this past weekend did not fail to impress. Tim Tangherlini and his mathemagical imps returned in true form, organizing a really impressively realized (and predictably jam-packed) conference that left the participants excited, exhausted, enlightened, and unanimously shouting for more next year (and the year after, and the year after that, and the year after that…) I cannot thank the ODH enough for facilitating this and similar events.

Some particular highlights included Graham Sack’s exceptionally robust comparative analysis of a few hundred early English novels (watch out for him, he’s going to be a Heavy Hitter), [Sarah Horowitz](http://www.wlu.edu/x24952.xml?InsertFile=x24146)‘s really convincing use of epistolary network analysis to weave the importance of women (specifically salonières) in holding together the fabric of French high society, Rob Nelson’s further work on the *always* impressive [Mining the Dispatch](http://dsl.richmond.edu/dispatch/pages/about), [Peter Leonard](http://thegogglesdonothing.com/)‘s thoughtful and important discussion on combining text and network analysis (hint: visuals are the way to go), [Jon Kleinberg](http://www.cs.cornell.edu/home/kleinber/)‘s super fantastic wonderful keynote lecture, [Glen Worthey](http://twitter.com/#!/gworthey)‘s inspiring talk about not needing All Of It, Russell Horton’s rhymes, [Song Chen](http://scholar.harvard.edu/songchen/)‘s rigorous analysis of early Asian family ties, and, well, everyone else’s everything else.

Especially interesting were the discussions, raised most particularly by Kleinberg and [Hoyt Long](http://ealc.uchicago.edu/faculty/long.shtml), about what particularly we were looking at when we constructed these networks. The union of so many subjective experiences surely is not the objective truth, but neither is it a proxy of objective truth – what, then, is it? I’m inclined to say that this Big Data aggregated from individual experiences provides us a baseline subjective reality that provides us local basins of attraction; that is, trends we see are measures of how likely a certain person will experience the world in a certain way when situated in whatever part of the network/world they reside. More thought and research must go into what the global and local meaning of this Big Data, and will definitely reveal very interesting results.

My talk on bias also seemed to stir some discussion. I gave up counting how many participants looked at me during their presentations and said “and *of course* the data is biased, but this is preliminary, and this is what I came up with and what justifies that conclusion.” And of course the issues I raised were not new; further, everybody in attendance was already aware of them. What I hoped my presentation to inspire, and it seems to have been successful, was the open discussion of data biases and constraints it puts on conclusions within the context of the presentation of those conclusions.

Some of us were joking that the issues of bias means “you don’t know, you can’t ever *know* what you don’t know, and you should just give up now.” This is exactly opposite to the point. As long as we’re open an honest about what we do not or cannot know, we can make claims around those gaps, inferring and guessing where we need to, and let the reader decide whether our careful analysis and historical inferences are sufficient to support the conclusions we draw. Honesty is more important than completeness or unshakable proof; indeed, neither of those are yet possible in most of what we study.

There was some twittertalk surrounding my presentation, so here’s my draft/notes for anyone interested:

—–

Note: my summary of the Liben-Nowell and Kleinberg paper is somewhat incomplete compared to the actual bias effects and the claims made by their paper – the crux of the two papers were more about modeling chain letters with or without the network context rather than against the background-space of possible chain letters. However, for the purpose of this survey, the example is still a useful one.

Please see the [previous post](http://www.scottbot.net/HIAL/?p=73) for a list of useful references.

[PPT Presentation (as a pdf)](http://www.scottbot.net/HIAL/wp-content/uploads/2011/10/Sampling-biases-in-humanistic-networks.pdf)

[Slide 1 - intro]

**Systematic Biases in Humanistic Networks**

[Slide 2 - sexy networks]

Networks are sexy. Undeniably sexy. The mathematicians and sociologists seem to have known this for a while, but over the last 20 years a giant cohort of physicists, geneticists, information scientists, economists, computer scientists, epidemiologists, complexity theorists, and most recently humanists seem *also* to have been seduced.

[Slide 3 - ship building]

Network analysis, then, has been built from the ground up, collaboratively, each community adding new structure to the whole. Networks are a lens, much like statistics or critical theory, through which pretty much anything can be studied. That so many have so quickly decided to use this lens is due to a perfect storm of conditions, mostly involving computers. The Internet is just one big network – *everyone* loves the Internet, right? Advanced algorithms have made it easier to study Big Networks faster, and computing in general has made huge network datasets available. Theory has been graciously provided by that long list of disciplines I just mentioned. Basically, we’ve got the tools, the data, the theories, and the power to look at networks in ways we never could before.

[Slide 4 - here be dragons]

We must be cautious. The network waters are perilous, and the map is still covered by dark spots labeled “Here, there be Dragons.” What’s worse, we’re sailing on a ship designed by 20 different builders, each with different backgrounds, different goals, and different definitions of the meaning of “ship-shape.”

[Slide 5 - despair]

With so many different disciplines contributing to network science, all in the last few decades, it has become dangerously easy to forget what methods are viable for what types of networks, and what inferences can or cannot be drawn from certain types of analyses. It is worth remembering that network science is new for *everyone*, and even the pioneers can make mistakes.

[Slide 6 - Liben-Nowell & Kleinberg trees]

You may recall David Liben-Nowell speaking here last year about chain letters, from a paper he co-authored with Jon Kleinberg in 2008. We are lucky to have Kleinberg speaking here tonight, as he has been exceptionally important to the growth of network science. Their paper presented a new model of chain letter propagation through social networks. Traditional models simply did not account for the narrow-but-deep trees found in these chain letters.

[Slide 7 - Full tree set]

There was, unfortunately, a slight problem. Two years later Golub and Jackson found that those narrow-but-deep trees were not, in fact, unpredicted by previous models of information propagation. Instead, they were merely *exceptionally rare cases* of those traditional models. It just so happened, though, that those exceptionally rare cases were also the most visible ones. As the authors of the reply put it, “selection biases of which data we observe can radically change the estimation of classical diffusion processes.”

Essentially, Liben-Nowell and Kleinberg found an interesting process of network interactions, and did a very impressive job modeling those interactions — it just so happened that *what was actually happening* and *what was big enough to be observable* were two very different things. They were different enough that their model explained the latter but not the former. This is just an example of how even the pioneers among us can sometimes overlook subtle biases – it’s just *really hard* to infer mechanisms about processes that cannot be observed.

[Slide 8 - Bias]

It is this problem of bias that I would like to discuss today. Does our data have some systematic bias wherein what is *observable* is different from what *is*? Is that even a meaningful question in the humanities? If even the experts have these difficulties, what hope do we have? And, if this systematic bias exists (spoiler: it does), what inferences from our data are we allowed to draw? Are we discovering things about what is observable, or what *is*?

Let’s take history as an example. This is a problem philosophers of history and historiographers have been tackling since time immemorial; simply, is historical evidence representative? Luckily for the historians, especially those working in microhistories, this problem has never been so overwhelming as to cripple research.

On the small scale, we can ask questions like whether something happened, who influenced whom, and so forth. These are situations where *evidence for* an event is both necessary and sufficient to suggest that the event took place. However, now that we have the interest and capability to look at large-scale processes, positive evidence is necessary but no longer sufficient to identify trends *en masse*.

[Slide 9 - Taxpayers]

As a simple example, we cannot infer the average amount Americans paid in federal taxes in 2010 by adding up all the tax reports and dividing by the number of reports we had.  We also have to take into account the people *who did not send in their tax reports*, whether they were children or simply people who did not file.

[Slide 10 - Children & Taxpayers]

Without those, our average is skewed.

The problem facing historians is not in understanding *that* something is missing, but in knowing exactly *what* is missing and *how much* of it there is. Much of what happened in the past will forever stay there – the evidence simply no longer exists. It has been forgotten in memory and in the physical record. First, much of the private lives of people are never recorded to begin with. Of that which is recorded, some of it is published or otherwise persists – generally the records of the literate and rich. Any inferences we draw must be only on what we have, and it is very difficult to know fully what we are missing.

[Slide 11 - Systematic Bias]

The inadequacies of record-keeping are not the only danger. **Systematic bias in data leads to a systematic bias in conclusions**. Sometimes, turning humanistic *information* into humanistic *data* causes that systematic bias. This is an issue of sampling bias – how we as humanists decide to collect and select our data, if we are not careful, will influence what conclusions are drawn from it. The Humanities are analog and continuous; Networks are digital and discrete. The moral of the story is simply this (*pause*):

[Slide 12 - Cookie Cutters]

**If you take a cookie cutter to your research, don’t be surprised when a plate of cookies comes out of the oven**.

But **There is hope**. If we are careful about how we sample our information, and if we are aware of systematic biases in our records, we can offset those biases using statistical techniques, or at least we can know what is possible to infer from the data and what absolutely is not.

[Slide 13 - Murphey]

For historical data, we first need a good model of the survival of evidence. That is, as Murphey (1973) put it, “Once a document has been created, what is the probability that it will survive for *n* years?”  Unfortunately, “There is, so far as I know, not a single study which affords an empirical basis for answering this question.”

As far as I could find, only one study answered that call. Baretta, Markoff, and Shapiro (1987) looked at what factors influenced the survival of documents from the French Revolution. They had reasonable evidence that 40,000 documents of a certain variety existed; of those, 25,000 survived and were catalogued, and 15,000 were published. They then systematically looked at the reasons for these survivals and publications (and the losses), whether they be political, geographical, accidental, or otherwise. Surprisingly, and against most historical intuition, they found the selection of published material was actually *less biased* than the combination of published and unpublished material.

[Slide 14 - Missing Information]

More empirical studies of this nature are needed if historians are to know exactly what forces are transpiring against the survival of their documents. With this knowledge, **inferences of *missing information* can be drawn, and only with that knowledge should general, large-scale statistical statements be made about historical regularities**.

[Slide 15 - Stuff Happens]

Eventually, a model may exist looking something like this. Stuff happens. Some of that stuff is written down, some of what is written down is published, and (when historians are really lucky) some of *either of those* survive to today. As time passes, the stuff that happened falls from memory and documents are lost. Empirical research into how documents are lost and under what conditions, or on the flip side what sorts of factors make it more likely for a document to survive, will give us insight into what sorts of documents go missing in this stage, and how much of them are gone.

[Slide 15.5 - Research & Archiving]

Realistically, if we’re trying to analyze a *lot* of historical data, we’ll likely pick from information that has already been digitized into collections. Editorial selection of those documents itself will contribute a bias, and then realistic constraints of what is easy or even possible to digitize will offer a further bias, as *information* becomes *data*. Our choice of what collections to use adds another possible bias, as well as our decision of what metric we use as a proxy for what we’re looking for. For example, if we say the existence of a letter is a proxy for a relationship, we’re only allowing relationships to exist between literate people with enough money to buy ink and paper.

If the data we have are vast and hard to handle, how we sample those data can cause further issues. In short, when taking into account systematic biases, we must look at recording, preservation, editorial decisions, information-to-data conversion, and research choices in the study itself.

(*pause*) Did I mention we need some more empirical studies?

[Slide 16 - Biased Data]

So now the question is, **how does biased data affect network analysis**? Unfortunately this is a problem that network scientists are very much still tackling for themselves, however we may be able to draw some inspiration from recent literature. Because we get our data in so many different ways, and because humanists tend to look more closely at the particularities of that data, we as humanists should be in a very good position to offer theoretical contributions to research in bias effects.

[Slide 17 - Network Sampling]

Besides that reply to Liben-Nowell and Kleinberg I mentioned earlier, most discussions of bias effects on network data are about *sampling* rather than *selection*. Much of the recent hard-hitting network research has been on vast, sprawling networks; so large that collecting and analyzing all the data has been computationally infeasible. Especially difficult are studies of Internet connectivity, as information on the Internet and its physical housing is not stored in any one location. As such, research on networks is generally research on *samples* of much larger networks.

The samples created for these analyses are often themselves quite large. It was an assumption of much earlier research on large-scale networks that the larger the sample, the more indicative it is of the network as a whole. Critical reflection over the last decade has shown empirically that this is not often the case.

Sampling strategies commonly come in two flavors, though they are not mutually exclusive: crawling and random node sampling.

[Slide 18 - Crawling]

In crawling, a random starting node is chosen, and then other nodes are selected to join the sample by traversing over that node’s edges, finding one or all of its neighbors, and then crawling the edges of *those* nodes to get the next batch. Thus, to obtain a crawled sample of Wikipedia, one would begin on some random page, click all links on that page, save them, click the links on those pages, and so forth until the sample is so large as to feel representative of Wikipedia in general.

[Slide 23 - Random Sampling]

The other option is random node sampling; this generally (but not always) requires knowledge of the entire network. With random node sampling, you simply have a roulette wheel with all of the nodes already on it, and you save the node and all of its edges every time the wheel stops. To sample Wikipedia in this fashion, one just clicks the “random page” link continuously, saving each page landed on and the list of links they have (without crawling through those links to the subsequent page).

[Slide 29 - Sampling Biases in Networks]

Both of these have their strengths and weaknesses. Traditional crawling techniques tend to bias nodes with high degree; that is, nodes that are better connected will be better represented in the sample. This skews any analysis that relies on degree or degree distribution. Random sampling techniques, on the other hand, while yielding relatively better degree distributions (if anything they positively bias the lower degree nodes), create large biases in community structure, clustering, and connectedness.

Intuitively (and I wish I had empirical evidence to back me up on this) both biases are present in historical networks. Baretta et al. (1987) showed that urban centers tended to preserve more documents than rural centers. It is a trivial but unproven fact that we mostly have records of the interesting, famous, or rich. As such, our networks would be biased toward nodes of high degree. However, historical selection and sampling is less likely to yield *connected* samples, so our notions of average path length, clustering, and connectedness are also likely to be skewed.

As historical research tends to be on both communities and individuals, the communities present in our networks are likely *accurate*, however they probably are not *complete*. That is, those communities we see in our networks probably existed, but there are likely many more that existed which do not show in our networks.

Similar biases occur for humanities data outside of history. Looking at character name co-occurrence as a proxy for social networks in literature may be biased by the binning process used on the text and variations in writing styles and narrative perspective. Document similarity by word use or topic modeling is initially biased by document length and variability within documents, not to mention the use of metaphor. Publication data, co-authorships, and citations are heavily biased by data availability and citation and authoring practices within and across disciplines. After each of these statements I would have included a citation to preliminary research on how that bias affects our research. I did not, because they do not yet exist. That’s your job.

[Slide 30 - Sailing Ships]

These biases are many, but they are not insurmountable. A recent thesis by Maiya (2011) showed how, if biases in network sampling are known, they can actually be harnessed to *improve* understanding of the underlying dataset. We do not need All The Data – what we need is an awareness of what we are missing, and how what is missing affects our research. Once that is known, we can contribute not only to the methodologies of network science, but to knowledge of humanity in ways that were never before possible.
[Slide 31 - Thank You.]
