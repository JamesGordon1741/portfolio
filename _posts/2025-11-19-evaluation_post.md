---
title: "Evaluations: The HTR Values"
excerpt_separator: "<!--more-->"
categories:
  - project1
tags:
  - experiments
  - tests
image: images/NLPNERIMAGE.jpeg
---



Several numerical values are used to evaluate HTR. These are WAR, CAR, CER, and WER, which all are a way of mathetmatically representing the difference between a ground truth, or an accurate, manual transcription of document, and the automatic transcription attempted by a given model. HTR values are sufficient, broadly, for providing feedback to develop a model for general use of texts in a given language. They provide those in the digital humanities with a sense of how accurate, overall, a transcription model is for the different texts or corpuses it is used for.

These values, though simple to calculaate and easy to understand, might cover up certain factors which can be useful when analyzing texts. It is common to have different expectations for different kind of texts when the relative effeciency of a model based on its CER, or other HTR value. For some standardized texts, such as those written on a typewriter or printed from computer text in a common, romanized language, nothing less than a CER of 1% can be considered a good outcome. Conversely, [a benchmark of 20% can be good]( https://towardsdatascience.com/evaluating-ocr-output-quality-with-character-error-rate-cer-and-word-error-rate-wer-853175297510/)  for those documents with idiosyncratically handwritten or obscured linguistic content, whether this be a problem of lesser-known language and slang or orthographical errors. The reasoning for mistakes made by the model, however, are  leftunclear according to these values. Some scribal traditions might be less known to models, due to language or orthographic practices, and resistant to models despite their uniformity to eachother. In this case, knowing the cause behind the mistakes made by the model would not tell you alot about why a model is struggling with a certain text or group of texts– and you would be unable to know– unless you painstakingly compare yourself  both the ground truth and the model-transcribed text. This would, in turn, prove complicated for larger jobs, of texts hundreds of pages in length, which are common in the digital humanities fields. It is best, therefore, for CER and other values to be utilzized with other strategies to ascertain the source of these problems.
