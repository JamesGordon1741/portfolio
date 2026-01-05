---
title: "My first blog"
excerpt_separator: "<!--more-->"
categories:
  - project1
tags:
  - experiments
  - tests
image: images/my-image.jpg
---
In this more advanced and independent adventure in the Digital Humanities, I aimed to utilize digital humanities methods to visualize certain integral texts related to my thesis. This would be in the form of the different

A project of this variety invariably begins with assembling a corpus of machine-readable text to be subjected to machine-learning processes. The initial project to OCR and then acquire text forms of the files was beset by issues. In the corpus, some strong OCRs fortunately already existed in the form of Gallica OCRs, the French national library's (BnF) service for storing digitized pieces of their collection. However, certain entries, including the Deux Campagnes en Haut-Senegal-Niger by Henri Frey had problems with accuracy, and with translating from OCR to text. An attempt to force another OCR using different means, failed on my laptop because it was too intensive a process for my specs. Instead, it proved more efficient to manually copy the parts of the original OCR of the document I desired, from the 1887-8 period, in to a text file.


Developing a visualization involved researching and testing the python word cloud extension on a small part of my corpus. A frequency table was also added to the code to show the data behind the developed visualizations. 


Making a useful word cloud requires assembling a table with a large amount of excluded words, including definite and indefinite articles, preopositional and conjunctions and other grammar words of little analytical value. Many prebuilt ones already exist, fine tuned for doing just this kind of frequency analysis. I was able to find one online on a github repository, and  after formatting with chat GPT, add it as a function of words to ignore in python.


While my current table has shown marked imrpovemenets over previoud frequency generations, what I would do in the future, as seen in an example from my current tables, is further include variants of these excluded words which appeared in my text due to spelling errors and consequences of the process of normilization, namely  the treatment of articles like l' and d' behind apostrophes as distinct words.


The world cloud at first looked at the words, primarily names like Mahmadou, Lamine, and Dramé for the leader I wanted to look at, Diana his capital, Soybou his son and deputy ruler of his state, and Ahmadou his strongest indigenous rival ruler. This also inclues terms which are shorthand for other rulers such as al-Hadj, the influential cleric and father of Ahmadou and le marabout, which was extensively used as shorthand to refer to Mahmadou in the 1887-9 period. e
Dramé eventually was dropped by me for its comparative rarity in most of the texts, being an important lineage name used by Soninké sources to refer to Mahmadou but not commonly used by the French.



The original plan was to add each paragraph containing a keyword I mentioned. However, the documents in their .txt form had often erratic spacing. I mitigated the obscurity of paragraphs in some of the documents by instead opting to gather chunks of 200 words which mentioned the keywords, along with gaps of 50 words if terms appear across chunks . 
A further iteration on the code was so that it looped to find each of the text chunks for each term and made seperate word clouds for them.
In the end, I was left with several incomplete, though analytically interesting, word clouds for each of the key terms mentioned before. Word clouds and the basic word frequency analyses behind them definitely have limitations to beware when drawing conclusions, especially when using a few, very specific texts. However, general themes related to the words seem interesting to explore. One of these is a surpising comparative lack of Mahmadou's numerous letters to French officials, with his regional rival Ahmadou, the erstwhile French ally, more strongly linked to letters and correspondance in the corpus. I think that rethinking parts of my thesis was a helpful part of this exercise, and a more finished exclusion table, corpus of OCR, and a different set of keywords would probably prove benefecial to looking at these texts from other angles.
