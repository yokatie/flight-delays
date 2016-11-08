# see http://stackoverflow.com/questions/701802/how-do-i-execute-a-string-containing-python-code-in-python
# for input on reflection in python
import pickle


class SparkPythonModelConverter:

    BASE_INDENTATION = 4 * 2  # 4 is at function level, 8 is when inside a class

    def convert(self, spark_model_file, output_file, to_pickle):
        python_class_code = self.translate_tree(spark_model_file, self.BASE_INDENTATION)
        # if needs to be pickled, instantiate the class and pickle it
        if to_pickle:
            # execute class code
            exec python_class_code
            # TODO: look at compile method
            # to help pickling/unpikcling assign a global name
            globals()['DecisionTree'] = DecisionTree
            decision_tree_classifier = DecisionTree()
            pickle.dump(decision_tree_classifier, open(output_file, "wb"))
        # otherwise, save the file as a .py file
        else:
            self.dump_python_class(output_file, python_class_code)

        return

    def dump_python_class(self, output_file, python_class_code):
        with open(output_file, 'w') as f:
            f.write(python_class_code)

        return

    def parse_line(self, line):
        # each line is made by: conditional instruction + ( + feature + operator + number|list +)
        # eliminate insignicant spaces and remove parenthesis
        line = line.replace('feature ', 'feature').replace('(', '').replace(')', '')
        return line.lstrip().split()

    def translate_split_line(self, parsed_line):
        # this is a split, so a if clause
        # instructions are the same in Python, just need to lower case
        instruction = parsed_line[0].lower().replace('else', 'elif')
        # features need to be replaced with an item from the feature array
        feature = parsed_line[1].replace('feature', 'features[') + ']'
        operator = ' '.join(parsed_line[2:-1])
        # if it is a number, it's just the target itself, if it is a list, need to replace parenthesis
        variable = parsed_line[-1].replace('{', '[').replace('}', ']')

        return '{0} {1} {2} {3}:\n'.format(instruction, feature, operator, variable)

    def translate_prediction_line(self, parsed_line):
        # this is the end of the tree, just return the target category
        return 'return {0}\n'.format(parsed_line[1])

    def translate_parsed_line(self, parsed_line):
        # each split line is [ instruction, feature, operator, number|list ]
        # each prediction line is [ instruction, prediction ]
        # find out which type of line is and translate accordingly
        if parsed_line[0] == 'Predict:':
            return self.translate_prediction_line(parsed_line)
        elif parsed_line[0] in ['If', 'Else']:
            return self.translate_split_line(parsed_line)
        else:
            raise 'Instruction not recognized'

    def get_indentation_length(self,line):
        return len(line) - len(line.lstrip())

    def translate_tree(self, input_file, base_indentation):
        final_code = []
        # get lines from file and skip header
        lines = []
        with open(input_file) as f:
            lines = [line for line in f][1:]
        # get start_indentation
        start_indentation = self.get_indentation_length(lines[0])
        # loop over the lines and parse them
        for line in lines:
            line_indentation = self.get_indentation_length(line) - start_indentation
            indentation = ' ' * (base_indentation + (line_indentation * 2))
            final_code.append(indentation + self.translate_parsed_line(self.parse_line(line)))

        return self.get_class_and_function_header() + ''.join(final_code)

    def get_class_and_function_header(self):
        class_header = 'class DecisionTree():\n\n'
        function_header = '    def classify(self, features):\n'

        return class_header + function_header
