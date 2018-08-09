# ======================================================================================================================
#
# IMPORT STATEMENTS
#
# ======================================================================================================================

# >>>> Python Native Imports <<<<
import os
import sys
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path + "/..")
import csv
csv.field_size_limit(sys.maxsize)  # Needed to load the Sougou dataset

# >>>> Package Imports <<<<
# None

# >>>> This Package Imports <<<<
from edm import report

# ======================================================================================================================


# ======================================================================================================================
#
# FUNCTIONS
#
# ======================================================================================================================


def load_data(path):
    """
    Loads the dataset from a .csv file. Assumes that the first item in each row is the text and the second is the
    label.
    """
    data = []

    with open(path, "r") as f:
        reader = csv.reader(f)
        for line in reader:
            if line:
                data.append(line)

    return [x[0] for x in data], [x[2] for x in data]

# ======================================================================================================================

# ======================================================================================================================
#
# MAIN
#
# ======================================================================================================================

TEST_DATA_PATH = ""  # !!!! PATH TO YOUR DATASET GOES HERE !!!!

print("----> Loading data...", end=" ")
sys.stdout.flush()

sents, labels = load_data(TEST_DATA_PATH)

print("Done.")

report = report.get_difficulty_report(sents, labels)

print(report)


# ======================================================================================================================
