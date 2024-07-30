import json
import os
from pathlib import Path
import logging

OUTPUT_DIRECTORY = "Output"
OUTPUT_FILENAME = "Query_Execution_Summary.txt"
DELIMITER = 'INFO  : ----------------------------------------------------------------------------------------------'

class QuerySummary:

    def __init__(self):
        self.delimiter_count = 0
        self.summary_dict = {}

    def _get_output_file_path(self):
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent
        return project_root / OUTPUT_DIRECTORY / OUTPUT_FILENAME

    def _read_line(self, file):
        return file.readline()

    def _within_metric_section(self):
        return self.delimiter_count < 2

    def _parse_line(self, line):
        metrics = line.replace("INFO  : ", "").split()
        key = ' '.join(metrics[:-1])
        value = metrics[-1]
        return key, value

    def create_summary_file(self, input_file):
        output_file_path = self._get_output_file_path()

        with open(output_file_path, 'w') as output_file:
            line = self._read_line(input_file)

            while self._within_metric_section():
                if DELIMITER in line:
                    self.delimiter_count += 1
                else:
                    key, value = self._parse_line(line)
                    self.summary_dict[key] = value

                line = self._read_line(input_file)

            json.dump(self.summary_dict, output_file, indent=2)

        logging.info("Query_Execution_Summary.txt created successfully")
