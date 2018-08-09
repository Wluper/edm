# ======================================================================================================================
#
# IMPORT STATEMENTS
#
# ======================================================================================================================

# >>>> Python Native Imports <<<<
from math import log as ln
from math import sqrt

# >>>> Package Imports <<<<
import numpy as np

# >>>> This Package Imports <<<<
from edm import datastructures


# ======================================================================================================================


# ======================================================================================================================
#
# FUNCTIONS
#
# ======================================================================================================================


def get_class_diversity(labelCounts):
    """
    Calculates Shannon label diversity i.e. the Class Diversity. The Shannon Diversity is the diversity measure used.

    :param labelCounts : dictionary mapping labels to a count of their occurences in the data.
    :type labelCounts  : dict

    :return            : shannon label diversity (class diversity)
    """
    totalLabels = sum([val for key, val in labelCounts.items()])

    shannonDivIndex = 0
    for label, count in labelCounts.items():
        p = count / totalLabels
        shannonDivIndex += p * ln(p)

    shannonDivIndex *= -1

    return shannonDivIndex


def _get_hellinger_distance(ngramCounts1, ngramCounts2):
    """
    Gets the hellinger distance between the two sets of ngrams and counts.

    :param ngramCounts1 : dictionary mapping word to count
    :type ngramCounts1  : dict

    :param ngramCounts2 : dictionary mapping word to count
    :type ngramCounts2  : dict

    :return             : hellinger distance between the classes
    """
    totalWords1 = sum([val for key, val in ngramCounts1.items()])

    totalWords2 = sum([val for key, val in ngramCounts2.items()])

    hellingerDist = 0
    for ngram, count in ngramCounts1.items():
        p = count / totalWords1

        if ngram not in ngramCounts2.keys():
            q = 0
        else:
            q = ngramCounts2[ngram] / totalWords2

        hellingerDist += (sqrt(p) - sqrt(q)) ** 2

    hellingerDist = (1 / sqrt(2)) * sqrt(hellingerDist)

    return hellingerDist


def get_minimum_hellinger_distance(labelBagOfWords):
    """
    Calculates the minimum Hellinger distance between classes.

    :param labelBagOfWords : bag of ngrams in a specific format. Keys are the labels of the dataset, and the values are
                             bag-of-words dictionaries for the sentences in each class.
    :type labelBagOfWords  : dict

    :return                : the minimum Hellinger distance between classes
    """

    done = set()

    hellingerDists = {}

    for label, ngramCounts in labelBagOfWords.items():
        for checkLabel, checkNGramCounts in labelBagOfWords.items():

            if (label, checkLabel) in done or label == checkLabel:
                continue

            dist = _get_hellinger_distance(ngramCounts, checkNGramCounts)

            hellingerDists[(label, checkLabel)] = dist
            done.add((label, checkLabel))
            done.add((checkLabel, label))

    return min([val for _, val in hellingerDists.items()])


def get_mutual_information_from_count_dict(dict1, dict2=None):
    """
    Computes the mutual information of input dict 1 and 2, or entropy of dict1

    :param dict1 : dictionary of keys and counts
    :type  dict1 : dict

    :param dict2 : dictionary of keys and associated probabilities.
    :type  dict2 : dict

    :return      : a matrix of cross mutual informations
    """
    out = 0.0

    # mutual information case
    if dict2:
        total1 = sum([count for _, count in dict1.items()])
        total2 = sum([count for _, count in dict2.items()])

        totalNgrams = set([x for x, _ in dict1.items()] + [x for x, _ in dict2.items()])

        for ngram in totalNgrams:

            if dict1.get(ngram):
                count1 = dict1[ngram]

                if dict2.get(ngram):
                    count2 = dict2[ngram]

                    prob1  = count1 / total1
                    prob2  = count2 / total2
                    prob12 = (count1 + count2) / (total1 + total2)
                    out   += prob12 * (np.log(prob12) - np.log(prob1) - np.log(prob2))

    # entropy case
    else:

        total1 = sum([count for _, count in dict1.items()])

        for _, x in dict1.items():

            prob = x/total1

            out += prob*np.log(prob)

        out = -out

    return out


def get_avg_mutual_information(labelBagOfWords):
    """
    Calculates the average mutual information statistic between classes.

    :param labelBagOfWords : bag of ngrams in a specific format. Keys are the labels of the dataset, and the values are
                             bag-of-words dictionaries for the sentences in each class.
    :type labelBagOfWords  : dict

    :return                : the average mutual information between classes.
    """
    outMat       = np.zeros([len(labelBagOfWords), len(labelBagOfWords)])

    filteredLBow = datastructures.filter_top_words(labelBagOfWords)

    labels       = [key for key, _ in filteredLBow.items()]

    for idx, label in enumerate(labels):

        outMat[idx, idx] = get_mutual_information_from_count_dict(filteredLBow[label])

        if idx < len(filteredLBow) - 1:

            for jdx, label2 in enumerate(labels):

                if jdx > idx:

                    outMat[idx, jdx] = get_mutual_information_from_count_dict(filteredLBow[label], filteredLBow[label2])

                    outMat[jdx, idx] = outMat[idx, jdx]

    return np.mean(outMat)


def get_class_imbalance(labelCounts):
    """
    Calculates the imbalance in classes in the data.

    :param labelCounts : dictionary mapping labels to a count of their occurences in the data.
    :type labelCounts  : dict

    :return         : class imbalance metric
    """

    numClasses = len(labelCounts)
    totalData  = sum([val for key, val in labelCounts.items()])
    classVals  = []

    for lab, count in labelCounts.items():
        classVals.append(abs((1 / numClasses) - (count / totalData)))

    total = np.sum(classVals)

    return total


def get_number_of_classes(labelsCounts):
    """
    Counts how many classes there are in the dataset.

    :param labelsCounts : a dictionary mapping labels to a count of their occurrences.
    :type labelsCounts  : dict

    :return             : the number of different labels in the dataset.
    """
    return len(labelsCounts)


def get_vocab_size(bow):
    """
    Gets the vocab size from a traditional bag of words

    :param bow : traditional bag of words mapping words to a count of their occurences.
    :type  bow : dict

    :return    : the vocab size of the dataset
    """
    return len(bow)


def get_vocab_ratio(bow):
    """
    Gets unique word count from a traditional bag of words

    :param sents : traditional bag of words
    :type  sents : dict

    :return      : the count of unique word
    """
    return len(bow) / sum([val for key, val in bow.items()])


def get_mean_data_items_per_class(labelCounts):
    """
    Gets the mean number of data items per class by dividing the number of data items by the number of classes.

    :param labelCounts : dictionary mapping labels to a count of their occurences in the data.
    :type labelCounts  : dict

    :return            : mean data items per class
    """

    totalItem        = sum([val for key, val in labelCounts.items()])
    meanItemPerClass = totalItem / len(labelCounts)

    return meanItemPerClass


def get_minimum_data_items_in_a_class(labelCounts):
    """
    Calculating which class has the smallest number of data items.

    :param labelCounts : dictionary mapping labels to a count of their occurrences in the data.
    :type labelCounts  : dict

    :return            : minimum data items in classes
    """

    minItem  = min([val for key, val in labelCounts.items()])

    return minItem


def get_average_sentence_length(sentsLenList):
    """
    calculating the average sentence length of the sentences in the dataset.

    :param sentsLenList : a list of sentence length
    :type sentsLenList  : list

    :return             : average sentence length
    """

    return sum(sentsLenList) / len(sentsLenList)

# ======================================================================================================================
