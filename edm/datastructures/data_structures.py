# ======================================================================================================================
#
# IMPORT STATEMENTS
#
# ======================================================================================================================

# >>>> Python Native Imports <<<<
import string
import collections
import time
import operator

# >>>> Package Imports <<<<
# None

# >>>> This Package Imports <<<<
# None

# ======================================================================================================================

STOPWORDS = {'for', 'am', 'doesn', 'each', 'will', 'above', 'yourselves', 'same', 'o', 'does', 't', 'again', 'at',
             'should', 'further', 'other', 'did', 'm', 'they', 'hadn', 'hasn', 'we', 'who', 'both', 'as', 'being',
             'shouldn', 'but', 'yours', 'do', 'and', 'here', 'ain', 'didn', 'are', 'to', 'when', 'only', 'out', 'her',
             'my', 'she', 'haven', 'now', 'won', 'y', 'those', 'too', 'no', 'herself', 'our', 'after', 'some', 'shan',
             'had', 'the', 'wouldn', 'ma', 'between', 'its', 'in', 'these', 'own', 'can', 'most', 'needn', 'weren',
             'if', 'mustn', 'ourselves', 'you', 'before', 'below', 'don', 's', 'ours', 'has', 'them', 'yourself',
             'than', 'where', 'd', 'because', 'a', 'couldn', 'into', 'from', 'i', 'was', 'mightn', 'what', 'during',
             'have', 'an', 'once', 'by', 'it', 'more', 'be', 'few', 'itself', 'not', 'himself', 'with', 're', 'over',
             'under', 'so', 'through', 'were', 'wasn', 'll', 'how', 'their', 'there', 'isn', 'your', 'hers', 'against',
             'themselves', 'all', 'down', 'until', 'aren', 'up', 'doing', 'such', 'is', 'that', 'which', 'whom', 'just',
             'then', 've', 'his', 'theirs', 'about', 'why', 'or', 'nor', 'very', 'he', 'of', 'off', 'while', 'having',
             'any', 'me', 'been', 'myself', 'on', 'this', 'him'}


# ======================================================================================================================
#
# FUNCTIONS
#
# ======================================================================================================================


def tokenize_sentence(sentence):
    """
    Splits a sentence into words, strips punctuation and turns it to lowercase.

    :param sentence           : the sentence to tokenize.
    :type sentence            : str

    :return                   : list of words
    """

    # Get rid of non-ascii characters to avoid errors with unrecognised characters
    sentence = "".join([c for c in sentence if 0 < ord(c) < 127])

    sentence = sentence.encode("ascii", errors="ignore").decode()

    # Only works in Python 3
    sentenceNoPunctuation = sentence.translate(str.maketrans("", "", string.punctuation))

    sentenceLower         = sentenceNoPunctuation.lower()
    sentenceWords         = sentenceLower.split()

    return sentenceWords


def get_bags_of_words(sents, labels):
    """
    Creates a "label bag-of-words" representation of the dataset and a normal bag of words for the dataset.
    Also counts the occurences of each class. A "label bag-of-words" is a dictionary where the keys are the labels of
    the dataset, and the values are bag-of-words dictionaries for the sentences in each class. For example for a
    sentiment analysis task this could be:

    {
        "positive": {"good": 10, "great": 5, "awesome": 7, ...},
        "negative": {"bad": 12, "awful": 3, "abismal": 5, ...}
    }

    A bag-of-words dictionary has keys as words and values as the count of occurrences of those words in the dataset.

    :param sents  : a list of the sentences in the dataset. Each sentence is an untokenized string.
    :type sents   : list

    :param labels : a list of the labels in the dataset. There is one label for every sentence.
    :type labels  : list

    :return       : a label bag-of-words dictionary, a traditional bag of words, count of the labels, a list of sentence lengths
    """

    assert len(sents) > 0           , "You must provide at least one item of data"
    assert len(sents) == len(labels), "The lists of sentences and labels must be the same length"
    assert isinstance(sents[0], str), "The sentence list must be a list of strings"

    labelBow                   = collections.defaultdict(lambda: collections.defaultdict(int))
    bow                        = collections.defaultdict(int)
    labelCount                 = collections.defaultdict(int)
    sentsLenList               = []
    count, numSents, startTime = 0, len(sents), time.time()

    for sent, label in zip(sents, labels):

        count = _loading_bar(count, 30, numSents, startTime)

        words = tokenize_sentence(sent)

        labelCount[label] += 1

        sentsLenList.append(len(sent))

        for word in words:

            labelBow[label][word] += 1
            bow[word]             += 1

    print()

    return labelBow, bow, labelCount, sentsLenList


def count_labels(labels):
    """
    Counts the occurrences of labels in the dataset.

    :param labels : a list of the labels in the dataset. There is one label for every sentence.
    :type labels  : list

    :return       : a mapping from classes to the count of their occurences.
    """
    labelCount = collections.defaultdict(int)

    count, numLabels, startTime = 0, len(labels), time.time()

    for label in labels:

        count = _loading_bar(count, 30, numLabels, startTime)

        labelCount[label] += 1

    print()

    return labelCount


def filter_top_words(labelBagOfWords, filterNum=10):
    """
    Filters all words out of the bag of words counts for each bag of words in the provided dictionary except for the
    top N words. After this function runs, only the top N most frequent words will remain. Only non-stopword words will
    be retained.

    :param labelBagOfWords : bag of ngrams in a specific format. Keys are the labels of the dataset, and the values are
                             bag-of-words dictionaries for the sentences in each class.
    :type labelBagOfWords  : dict

    :param filterNum       : top N frequent words to keep, default 10.
    :type filterNum        : int

    :return                : labelBagOfWords with filtered counts.
    """
    filteredBow = collections.defaultdict(dict)

    for label, bow in labelBagOfWords.items():

        sortedBowList = sorted([(key, val) for key, val in bow.items()], key=operator.itemgetter(1), reverse=True)
        newBowList    = [x for x in sortedBowList if x[0] not in STOPWORDS][:filterNum]
        filteredBow[label] = dict(newBowList)

    return filteredBow

# ======================================================================================================================

# ======================================================================================================================
#
# DISPLAY FUNCTIONS - NO ACTUAL FUNCTIONALITY HERE
#
# ======================================================================================================================


def _loading_bar(count, numSections, total, startTime):
    """
    Prints a loading bar.
    """
    numPerSection = int(total / numSections)

    sections = 0
    i = 0
    while i < count:
        sections += 1
        i        += numPerSection

    print("[", end="")

    numPrinted = 0
    while numPrinted < sections:
        print("-", end="")
        numPrinted += 1

    while numPrinted < numSections:
        print(" ", end="")
        numPrinted += 1

    percentDone = round(count * 100 / total, 1)

    if percentDone > 0:

        timeTaken = time.time() - startTime

        secsRemaining = (((100 / percentDone) * timeTaken) - timeTaken)

        minsRemaining = round(secsRemaining / 60, 1)

        print("] : {} of {}, {}% : Est. {} mins Remaining".format(count, total, percentDone, minsRemaining), end="\r")

    else:

        print("] : {} of {} {}% : Est. -- mins Remaining".format(count, total, percentDone), end="\r")

    return count + 1

# ======================================================================================================================
