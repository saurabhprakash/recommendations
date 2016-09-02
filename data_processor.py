import ast
import logging

array = []

class DataProcessor:

    def __init__(self):
        pass

    def line_processor(self, line):
        """Processes line data to map it to dictionary
            :parameter line: raw line string

            :outputs: processed line data added in dictionary
        """
        line = line.replace('\n', '').split('###')
        if line and line != ['']:
            try:
                line = [line[0], line[1] if 'None' in line[2] else '%s %s' % (line[1],
                                                                              ' '.join(ast.literal_eval(line[2])))]
            except UnicodeDecodeError:
                logging.debug('#TODO: UnicodeDecodeError needs handling')
            array.append({'id': line[0], 'line': line[1]})

    def read_data_file(self):
        """Reads file and pre-processes data for logic implementation"""
        with open('data_sample', 'r') as ins:
            for line in ins:
                self.line_processor(line)
        return array
