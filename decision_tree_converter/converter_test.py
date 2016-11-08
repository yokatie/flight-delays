import unittest
from converter import SparkPythonModelConverter
import os.path


class TestConverter(unittest.TestCase):

    # constants
    TEST_FOLDER = 'test_data'
    SPARK_MODEL_FILE = '{}/decision_tree.txt'.format(TEST_FOLDER)
    OUTPUT_CLASS_FILE = '{}/decision_tree.py'.format(TEST_FOLDER)
    OUTPUT_PICKLE_FILE = '{}/decision_tree.py'.format(TEST_FOLDER)

    def test_class_conversion(self):
        to_pickle = False
        converter = SparkPythonModelConverter()
        converter.convert(self.SPARK_MODEL_FILE, self.OUTPUT_CLASS_FILE, to_pickle)
        # check file existence
        self.assertTrue(os.path.exists(self.OUTPUT_CLASS_FILE))
        # check line count in final file
        self.assertEqual(sum(1 for line in open(self.OUTPUT_CLASS_FILE)), 13)

    def test_pickle_conversion(self):
        self.assertEqual('foo'.upper(), 'FOO')

        return


if __name__ == '__main__':
    unittest.main()
