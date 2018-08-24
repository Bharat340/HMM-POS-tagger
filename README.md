# HMM-POS-tagger

#Overview

A Hidden Markov Model part-of-speech tagger for English, Chinese, and a surprise language. The training data are provided tokenized and tagged; the test data will be provided tokenized, and your tagger will add the tags. The assignment will be graded based on the performance of your tagger, that is how well it performs on unseen test data compared to the performance of a reference tagger.

#Programs

Two programs: hmmlearn.py will learn a hidden Markov model from the training data, and hmmdecode.py will use the model to tag new data. If using Python 3, you will name your programs hmmlearn3.py and hmmdecode3.py. The learning program will be invoked in the following way:

> python hmmlearn.py /path/to/input

The argument is a single file containing the training data; the program will learn a hidden Markov model, and write the model parameters to a file called hmmmodel.txt. The format of the model is up to you, but it should follow the following guidelines:

The model file should contain sufficient information for hmmdecode.py to successfully tag new data.
The model file should be human-readable, so that model parameters can be easily understood by visual inspection of the file.
The tagging program will be invoked in the following way:

> python hmmdecode.py /path/to/input

The argument is a single file containing the test data; the program will read the parameters of a hidden Markov model from the file hmmmodel.txt, tag each word in the test data, and write the results to a text file called hmmoutput.txt in the same format as the training data.