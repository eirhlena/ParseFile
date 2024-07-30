import json
import os
from pathlib import Path
import logging

OUTPUT_DIRECTORY = "Output"
OUTPUT_FILENAME = "Detailed_Metrics_per_task.txt"


class TaskMetricsDetails:

    def __init__(self):
        self.file_path = self._determine_file_path()

    def _determine_file_path(self):
        current_script_path = Path(__file__).resolve()
        parent_directory = current_script_path.parent.parent
        complete_file_path = parent_directory / OUTPUT_DIRECTORY / OUTPUT_FILENAME
        return complete_file_path

    def _fetch_next_line(self, file):
        return file.readline()

    def _extract_metrics_from_line(self, line):
        return line.replace("INFO  : ", "").split()

    def _split_metrics_into_key_value(self, metrics_list):
        key = ' '.join(metrics_list[:1])
        value = ' '.join(metrics_list[1:2])
        return key, value

    def _populate_nested_dict(self, nested_dict, key, value):
        nested_dict[key] = int(value)
        return nested_dict

    def _extract_key_from_line(self, line):
        return line.replace("INFO  : ", "").replace(":", "").strip()

    def _is_metric_line(self, line):
        return ":   " in line

    def generate_metrics_file(self, initial_line, input_file):
        with open(self.file_path, 'w') as output_file:
            current_key = self._extract_key_from_line(initial_line)

            while 'Completed' not in current_key:
                line = self._fetch_next_line(input_file)
                metrics_data = {}
                nested_dict = {}

                while self._is_metric_line(line):
                    metrics_list = self._extract_metrics_from_line(line)
                    nested_key, nested_value = self._split_metrics_into_key_value(metrics_list)
                    nested_dict = self._populate_nested_dict(nested_dict, nested_key, nested_value)
                    metrics_data[current_key] = nested_dict
                    line = self._fetch_next_line(input_file)

                json.dump(metrics_data, output_file, indent=2)
                current_key = self._extract_key_from_line(line)

        logging.info("File Detailed_Metrics_per_task.txt created successfully")
