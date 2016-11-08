# see http://stackoverflow.com/questions/701802/how-do-i-execute-a-string-containing-python-code-in-python
# for input on reflection in python

"""
    The command-line script convert the content of a txt file to a pickled python class
    that can be used for real-time classification.

    The txt file contains a Spark description of a decision tree, that will be mapped to a
    corresponding set of rules and prediction in Python code.
"""

import sys
import getopt
from spark_python_dtree_converter import SparkPythonModelConverter


def explain_usage():
    print ''
    return


def main(argv):
    to_pickle = True
    spark_model_file = ''
    output_file = ''
    try:
        opts, args = getopt.getopt(argv, "hs:o:c", ["help", "spark_model_file=", "output_file="])
    except getopt.GetoptError:
        print 'ERROR: wrong format'
        explain_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', 'help'):
            explain_usage()
            sys.exit()
        elif opt in ("-s", "--spark_model_file"):
            spark_model_file = arg
        elif opt in ("-o", "--output_file"):
            output_file = arg
        elif opt == "-c":
            # output the conversion as a python class (.py class), not pickled object
            to_pickle = False

    # make the conversion with the provided options
    converter = SparkPythonModelConverter()
    converter.convert(spark_model_file, output_file, to_pickle)

    return


if __name__ == "__main__":
    main(sys.argv[1:])
