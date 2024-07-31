"""
This script defines the TaskMetricsDetails class, which processes log files to
extract detailed metrics for each task. The extracted metrics are saved as a
JSON file. The script includes methods for determining the output file path,
extracting metrics from lines, and populating nested dictionaries with these
metrics. The main method `generate_metrics_file` is responsible for reading
the input log file and generating the detailed metrics output.

Classes:
    TaskMetricsDetails: Processes log files to extract detailed metrics for each task.

Usage:
    Initialize a TaskMetricsDetails object and call the `generate_metrics_file` method
    with the initial line and input file.
"""

import json
from pathlib import Path
import logging

OUTPUT_DIRECTORY = "Output"
OUTPUT_FILENAME = "Detailed_Metrics_per_task.txt"

class TaskMetricsDetails:
    """
    A class to extract and detail metrics for each task from a log file.

    Attributes:
        file_path (Path): The path to the output file.
    """

    def __init__(self):
        self.file_path = self._determine_file_path()

    def _determine_file_path(self):
        """
        Constructs the output file path.

        Returns:
            Path: The path to the output file.
        """
        current_script_path = Path(__file__).resolve()
        parent_directory = current_script_path.parent.parent
        complete_file_path = parent_directory / OUTPUT_DIRECTORY / OUTPUT_FILENAME
        return complete_file_path

    def _fetch_next_line(self, file):
        """
        Args:
            file (file object): The file object to read from.

        Returns:
            str: The next line from the file.
        """
        return file.readline()

    def _extract_metrics_from_line(self, line):
        """
        Args:
            line (str): The line containing the metrics.

        Returns:
            list: A list of extracted metrics.
        """
        return line.replace("INFO  : ", "").split()

    def _split_metrics_into_key_value(self, metrics_list):
        """
        Args:
            metrics_list (list): The list of metrics.

        Returns:
            tuple: A key and a value.
        """
        key = ' '.join(metrics_list[:1])
        value = ' '.join(metrics_list[1:2])
        return key, value

    def _populate_nested_dict(self, nested_dict, key, value):
        """
        Args:
            nested_dict (dict)
            key (str)
            value (str)

        Returns:
            dict: The populated dictionary.
        """
        nested_dict[key] = int(value)
        return nested_dict

    def _extract_key_from_line(self, line):
        """
        Args:
            line (str): The line containing the key.
        Returns:
            str: The extracted key.
        """
        return line.replace("INFO  : ", "").replace(":", "").strip()

    def _is_metric_line(self, line):
        """
        Args:
            line (str): The line to check.

        Returns:
            bool: True if the line contains metrics, False otherwise.
        """
        return ":   " in line

    def generate_metrics_file(self, initial_line, input_file):
        """
        Args:
            initial_line (str): The initial line to start parsing from.
            input_file (file object): The input log file.
        """
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
