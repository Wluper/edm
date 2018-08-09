# ======================================================================================================================
#
# IMPORT STATEMENTS
#
# ======================================================================================================================

# >>>> Python Native Imports <<<<
# None

# >>>> Package Imports <<<<
# None

# >>>> This Package Imports <<<<
from edm import metrics, datastructures

# ======================================================================================================================

# Found during the research presented alongside this code
MEASURE_MEANS_AND_SIGMAS = {
    "DISTINCT_WORDS__TOTAL_WORDS" : (0.06664684568510734    , 0.05277364684092249),
    "CLASS_IMBAL"                 : (0.5034068136913944     , 0.3649967978917931),
    "CLASS_DIVERSITY"             : (0.9050458532039865     , 0.7588044194950574),
    "MIN_HELL_DIST"               : (0.5537154390242968     , 0.16502094329623587),
    "MUTUAL_INFO"                 : (1.230268703408238      , 0.4304696206798072),
    "DIFFICULTY"                  : (3.2590836550130224     , 0.8036059012169776)
}


class Color:
    BLUE      = '\033[94m'
    GREEN     = '\033[92m'
    ORANGE    = '\033[93m'
    RED       = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'

# ======================================================================================================================
#
# FUNCTIONS
#
# ======================================================================================================================


def _compare_to_mean(stat, whichStatistic):
    """
    Compares a statistic to the mean value and returns a severity level of difference. Severity is defined as follows:

    - stat > mu + 2 * sigma : VERY HIGH
    - stat > mu + sigma     : HIGH
    - stat > mu + sigma / 2 : SOMEWHAT HIGH
    - stat < mu             : GOOD

    :param stat          : the value of the statistic to compare
    :type stat           : float

    :param whichStatistic : which statistic to compare this one to on mean
    :type whichStatistic  : str

    :return               : a coloured string severity level
    """
    mu, sigma = MEASURE_MEANS_AND_SIGMAS[whichStatistic]

    if stat > mu + 2 * sigma:

        severity = Color.RED + "VERY HIGH" + Color.ENDC

    elif stat > mu + sigma:

        severity = Color.ORANGE + "HIGH" + Color.ENDC

    elif stat > mu + sigma / 2:

        severity = Color.BLUE + "SOMEWHAT HIGH" + Color.ENDC

    else:

        severity = Color.GREEN + "GOOD" + Color.ENDC

    return severity


def get_difficulty_estimate(labelBow, wordCounts, labelCounts):
    """
    Calculates the five statistics proposed as components of our difficulty measure.

    :param labelBow    : bag of ngrams in a specific format. Keys are the labels of the dataset, and the values are
                         bag-of-words dictionaries for the sentences in each class.
    :type labelBow     : dict

    :param wordCounts  : a dictionary mapping words to a count of their occurrences in the data.
    :type wordCounts   : dict

    :param labelCounts : a dictionary mapping labels to a count of their occurrences in the data.
    :type labelCounts  : dict

    :return            : a list of tuples with all of the components of the difficulty measure.
    """
    vocabRatio     = metrics.get_vocab_ratio(wordCounts)
    sevVocab       = _compare_to_mean(vocabRatio, "DISTINCT_WORDS__TOTAL_WORDS")

    classImbalance = metrics.get_class_imbalance(labelCounts)
    sevClassImabl  = _compare_to_mean(classImbalance, "CLASS_IMBAL")

    classDiversity = metrics.get_class_diversity(labelCounts)
    sevClassDiv    = _compare_to_mean(classDiversity, "CLASS_DIVERSITY")

    minHellDist    = 1 - metrics.get_minimum_hellinger_distance(labelBow)
    sevMinHellDist = _compare_to_mean(minHellDist, "MIN_HELL_DIST")

    minfo          = metrics.get_avg_mutual_information(labelBow)
    sevMinfo       = _compare_to_mean(minfo, "MUTUAL_INFO")

    difficulty     = vocabRatio + classImbalance + classDiversity + minHellDist + minfo
    sevDiff        = _compare_to_mean(difficulty, "DIFFICULTY")

    valueList      = [
        ("Distinct Words : Total Words" , vocabRatio     , sevVocab       ),
        ("Class Imbalance"              , classImbalance , sevClassImabl  ),
        ("Class Diversity"              , classDiversity , sevClassDiv    ),
        ("Max. Hellinger Similarity"    , minHellDist    , sevMinHellDist ),
        ("Mutual Information"           , minfo          , sevMinfo       ),
        ("Difficulty"                   , difficulty     , sevDiff        )
    ]

    return valueList


def get_generic_statistics(wordCounts, labelCounts, sentsLens):
    """
    Gets generic dataset statistics such as average sentence length.

    :param wordCounts  : a dictionary mapping words to a count of their occurrences in the data.
    :type wordCounts   : dict

    :param labelCounts : a dictionary mapping labels to a count of their occurrences in the data.
    :type labelCounts  : dict

    :param sentsLens   : a list of the lengths of sentences.
    :type sentsLens    : list

    :return            : a dictionary with all of the components of a difficulty measure.
    """
    vocabSize        = metrics.get_vocab_size(wordCounts)

    numClasses       = metrics.get_number_of_classes(labelCounts)

    meanItemPerClass = metrics.get_mean_data_items_per_class(labelCounts)

    minItemInClass   = metrics.get_minimum_data_items_in_a_class(labelCounts)

    if minItemInClass > meanItemPerClass / 2:
        severity = Color.GREEN + "GOOD" + Color.ENDC
    elif meanItemPerClass / 4 < minItemInClass < meanItemPerClass / 2:
        severity = Color.ORANGE + "SLIGHTLY LOW" + Color.ENDC
    elif minItemInClass < meanItemPerClass / 4:
        severity = Color.RED + "EXTREMELY LOW" + Color.ENDC

    averageSentLen   = metrics.get_average_sentence_length(sentsLens)

    valueList = [
        ("Dataset Size"            , len(sentsLens)   , "-"),
        ("Vocab Size"              , vocabSize        , "-"),
        ("Number of Classes"       , numClasses       , "-"),
        ("Mean Items Per Class"    , meanItemPerClass , "-"),
        ("Min. Items in a Class"   , minItemInClass   , severity),
        ("Average Sentence Length" , averageSentLen   , "-")
    ]

    return valueList


def generate_report(statsList):
    """
    Generates a string representation of a list of stats.

    :param statsList : list of stats to go in a report. They are a list of tuples where each tuple has a string
                       description and a float value.
    :type statsList  : list

    :return          : a string report of the statistics.
    """
    report = "\n\n"

    maxStatLen = max([len(x) for x, _, _ in statsList]) + 1
    maxValLen  = max([len(str(y)) for _, y, _ in statsList]) + 1

    for stat, value, sev in statsList:

        report += stat

        added = len(stat)

        while added < maxStatLen:

            report  += " "
            added   += 1

        report += str(value)

        added = len(str(value))

        while added < maxValLen:

            report += " "
            added  += 1

        report += sev + "\n"

    report += "\n\n"

    return report


def get_difficulty_report(sents, labels):
    """
    Coordinates the creation of a difficulty report for a sentence classification task.

    :param sents  : a list of the sentences in the dataset. Each sentence is an untokenized string.
    :type sents   : list

    :param labels : a list of the labels in the dataset. There is one label for every sentence.
    :type labels  : list

    :return       : a string describing the difficulty of a dataset.
    """
    print("----> Building bag of words representations...")
    labelBow, wordCounts, labelCounts, sentsLenList = datastructures.get_bags_of_words(sents, labels)
    print("----> Done.")

    print("----> Getting difficulty metrics...")
    difficultyAnalysis = get_difficulty_estimate(labelBow, wordCounts, labelCounts)
    print("----> Done.")

    print("----> Getting generic statistics...")
    genericStats       = get_generic_statistics(wordCounts, labelCounts, sentsLenList)
    print("----> Done.")

    report = generate_report(genericStats + difficultyAnalysis)

    return report


def get_difficulty_components_dict(sents, labels):
    """
    Coordinates the creation of a difficulty report for a sentence classification task, but returns the results as a
    dictionary rather than a string.

    :param sents  : a list of the sentences in the dataset. Each sentence is an untokenized string.
    :type sents   : list

    :param labels : a list of the labels in the dataset. There is one label for every sentence.
    :type labels  : list

    :return       : a dictionary of difficulty statistics about the dataset.
    """

    print("----> Building bag of words representations...")
    labelBow, wordCounts, labelCounts, sentsLenList = datastructures.get_bags_of_words(sents, labels)
    print("----> Done.")

    print("----> Getting difficulty metrics...")
    difficultyAnalysis = get_difficulty_estimate(labelBow, wordCounts, labelCounts)
    print("----> Done.")

    return {name : (val, sev) for name, val, sev in difficultyAnalysis}

# ======================================================================================================================
