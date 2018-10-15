# Evolutionary Data Measures: Understanding the Difficulty of Text Classification Tasks

**Authors:** _Ed Collins, Nikolai Rozanov, Bingbing Zhang_

**Contact:** _contact@wluper.com_

In the paper of the corresponding name, we discuss how we used an evolutionary algorithm to discover which statistics about a text classification dataset most accurately represent how difficult that dataset is likely to be for machine learning models to learn. We presented there the difficulty measure which we discovered and have provided this Python package of code which can calculate it.

## Installation

This code is pip-installable so can be installed on your machine by running:

`pip3 install edm`

The code requires Python 3 and NumPy.

It is recommended that you install this code in a `virtualenv`:

```commandline
$ mkdir myvirtualenv/
$ virtualenv -p python3 myvirtualenv/
$ source bin/activate
(myvirtualenv) $ pip3 install edm
```

## Running

To calculate the difficulty of a text classification dataset, you will need to provide two lists: one of sentences and one of labels. These two lists need to be the same length - i.e. every sentence has a label. Each item of data should be an untokenized string and each label a string.

```python
>>> sents, labels = your_own_loading_function(PATH_TO_DATA_FILE)
>>> sents
["this is a positive sentence", "this is a negative sentence", ...]
>>> labels
["positive", "negative", ...]
>>> assert len(sents) == len(labels)
True
```

This code does **not** support the loading of data files (e.g. csv files) into memory - you will need to do this separately.

Once you have loaded your dataset into memory, you can receive a "difficulty report" by running the code as follows:

```python
from edm import report

sents, labels = your_own_loading_function(PATH_TO_DATA_FILE)

print(report.get_difficulty_report(sents, labels))
```

Note that if your dataset is very large, then counting the words of the dataset may take several minutes. The Amazon Reviews dataset from _Character-level Convolutional Networks for Text
Classification_ by Xiang Zhang, Junbo Zhao and Yann LeCun, 2015 which contains 3.6 million Amazon reviews takes approximately 15 minutes to be processed and the difficulty report created. A loading bar will be displayed while the words are counted.
