---
title: "Digitisation Project"
excerpt_separator: "<!--more-->"
categories:
  - project1
tags:
  - OCR
  - python
  - digitisation
image: images/my-image.jpg
---

Our first mini digitization project had two purposes. One was the immediate objective of the work, to accomplish the eventual digitization of an intriguing Persian work of Ismai’li esotericism. The other goal of the exercise was to provide an instructive experience to myself and other students about many of the specifics of the manuscript digitization process. Participants were given practical experience in the various programs and methods used during digitization, including scanning, the use of EScriptorium, the application and fine-tuning of OCR models, and complex python functions to measure the efficacy of these models.

The book we digitized, entitled In ketaab-e mostatāb seest majmū‘eh-ye moshtamel bar do resāleh-ye mokhtasar dar haqīqat-e mazhab-e Esmā‘īliyah, but referred to in its English title and by the class as the Two Early Ismaili Treatises (henceforth TEIT) is an interesting text dating from 1933. The book, published in Mumbai and written in Persian script along with a short introduction written in English, is a document of historical value. The text shows us the author, an educated Indian Ismai’ili, and his perspectives on esotericism and theology, giving the AKU library in London, and perhaps someday a researcher, a perspective about the Ismai’ili written culture and religion in South Asia during the early 20th century.


Any digitization process starts with the conversion of physical material to digital material. This is accomplished through scanning the wanted material with a machine. Scanning is done through the use of a scanner which isolates the page and produces a PDF or JPG image file. As a rule, only exceptional, valuable and original texts are digitized, because scanning an entire book is a repetitive and labor intensive process, which can largely only be done by a human. For us, the task was made easy by the amount of students cooperating in the process. However, after scanning, quality control is necessary to make sure that the uploaded images are free from anything which might obstruct or complicate the view of a reader, whether human or automated. A pair of students was responsible for making sure the orientation, clarity, and legibility of the document were unimpaired, which included cropping out extraneous parts of the image such as a scanner's hand, rotating pages to be oriented correctly, or rescanning entire problematic pages. In addition, the proper sequence of the book had to be respected, meaning other mistakes such as duplicates and missing images or faulty numbering of the image files had to be corrected. Completing this task was important to make sure the next step, the OCR process, could proceed.

  Four transcription models, developed by kraken for transcribing Arabic and Persian scripts, were tested on a three-page sample from the book.  Their performance, represented by CER (Character Error Rate) and WER (Word Error Rate) values, was measured with the usage of a Python script developed by instructors and students at the AKU-ISMC. The script also includes normalisation tables, which are used to further qualify the WER and CER results. 
  Based on another Python script (built with the assistance of ChatGPT) involving basic and easily replicable functions – such as split and len– the highest-performing transcription model was concluded to be kraken-gen2-print-n7m5-union-ft_best. The results were then authenticated against calculations made on an excel spreadsheet.
  After determining the most accurate model with the lowest WER and CER values, were able to begin the OCR process. This involved using EScriptorium, which is able to apply these models by automatically segmenting texts, or dividing in to its constituent parts, such as main body, footnotes, and page numbers. This importantly ensures that when iti s translated to text, everything appears where it should on the page, instead of all together in a single mess. Then, it can apply the transcription model, producing the transcribed data which is the aspiration of the digitization process.

The digitization project gave myself and the other students valuable, hands-on experience in working with a manuscript. It also helped myself and the other participants become comfortable in applying an array of specific digital humanities skills, such as applying and training OCR models involving both segmentation and transcription. Finally, the benefits of becoming acquainted and confident in using some basic python coding to accomplish tasks, as well as in working through a sizable digital humanities project as a team, is very useful. This basic knowledge provides us an essential experiential background, allowing us to be confident and imagine ways to tackle larger and/or more difficult problems.


