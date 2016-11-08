import unittest
from converter import SparkPythonModelConverter
import os.path
import pickle


class TestConverter(unittest.TestCase):

    # constants
    TEST_FOLDER = 'test_data'
    SPARK_MODEL_FILE = '{}/decision_tree.txt'.format(TEST_FOLDER)
    OUTPUT_CLASS_FILE = '{}/decision_tree.py'.format(TEST_FOLDER)
    OUTPUT_PICKLE_FILE = '{}/decision_tree.p'.format(TEST_FOLDER)

    converter = SparkPythonModelConverter()

    # test conversion tool as a python class
    def test_class_conversion(self):
        to_pickle = False
        self.converter.convert(self.SPARK_MODEL_FILE, self.OUTPUT_CLASS_FILE, to_pickle)
        # check file existence
        self.assertTrue(os.path.exists(self.OUTPUT_CLASS_FILE))
        # check line count in final file
        self.assertEqual(sum(1 for line in open(self.OUTPUT_CLASS_FILE)), 13)
        # import class and check classification
        from test_data.decision_tree import DecisionTree
        decision_tree = DecisionTree()
        self.assertEqual(decision_tree.classify(self.get_features_for_class_0()), 0.0)
        self.assertEqual(decision_tree.classify(self.get_features_for_class_1()), 1.0)

    # test conversion tool as a pickled model
    def test_pickle_conversion(self):
        to_pickle = True
        self.converter.convert(self.SPARK_MODEL_FILE, self.OUTPUT_PICKLE_FILE, to_pickle)
        # check file existence
        self.assertTrue(os.path.exists(self.OUTPUT_PICKLE_FILE))
        # import pickled model and check classification
        decision_tree = pickle.load(open(self.OUTPUT_PICKLE_FILE, "rb"))
        self.assertEqual(decision_tree.classify(self.get_features_for_class_0()), 0.0)
        self.assertEqual(decision_tree.classify(self.get_features_for_class_1()), 1.0)

    def get_features_for_class_0(self):
        features = [0 for _ in range(13)]
        features[12] = 2.0
        features[4] = 1.0

        return features

    def get_features_for_class_1(self):
        features = [0 for _ in range(13)]
        features[12] = 2.0
        features[4] = 300

        return features


if __name__ == '__main__':
    unittest.main()
