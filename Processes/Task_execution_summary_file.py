import json
from pathlib import Path
import logging

OUTPUT_DIRECTORY = "Output"
OUTPUT_FILENAME = "Task_Execution_Summary.txt"
DELIMITER = 'INFO  : ----------------------------------------------------------------------------------------------'

class TaskSummary:

    def __init__(self):
        self.separator_count = 0
        self.summary_dict = {}

    def _get_output_file_path(self):
        current_file_path = Path(__file__).resolve()
        project_root = current_file_path.parent.parent
        output_file_path = project_root / OUTPUT_DIRECTORY / OUTPUT_FILENAME
        return output_file_path

    def _parse_keys(self, line):
        return line.replace("INFO  :   VERTICES      ", "").split()

    def _parse_metrics(self, line):
        return line.replace("INFO  : ", "").replace(",", "").split()

    def _extract_key_value(self, metrics_list):
        key = ' '.join(metrics_list[:2])
        values = [int(value) if "." not in value else value for value in metrics_list[2:]]
        return key, values

    def _populate_summary_dict(self, keys, metrics):
        key, values = self._extract_key_value(metrics)
        self.summary_dict[key] = dict(zip(keys, values))

    def create_summary_file(self, start_line, input_file):
        output_file_path = self._get_output_file_path()
        keys = self._parse_keys(start_line)

        with open(output_file_path, 'w') as output_file:
            for line in input_file:
                if DELIMITER in line:
                    self.separator_count += 1
                if self.separator_count >= 2:
                    break
                if DELIMITER not in line:
                    metrics = self._parse_metrics(line)
                    self._populate_summary_dict(keys, metrics)

            json.dump(self.summary_dict, output_file, indent=2)

        logging.info("File Task_Execution_Summary.txt created successfully")
