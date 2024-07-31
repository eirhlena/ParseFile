"""
This script defines the TaskSummary class, which processes log files to extract
and summarize key metrics. The summary is then saved as a JSON file. The script
includes methods for determining the output file path, parsing keys and metrics,
and populating a summary dictionary. The main method `create_summary_file` is
responsible for reading the input log file and generating the summary output.

Classes:
    TaskSummary: Processes log files to extract and summarize key metrics.

Usage:
    Initialize a TaskSummary object and call the `create_summary_file` method with
    the starting line and input file.
"""

import json
from pathlib import Path
import logging

OUTPUT_DIRECTORY = "Output"
OUTPUT_FILENAME = "Task_Execution_Summary.txt"
DELIMITER = 'INFO  : ----------------------------------------------------------------------------------------------'

class TaskSummary:
    """
    A class to summarize task execution metrics from a log file.

    Attributes:
        separator_count (int): Tracks the number of delimiters encountered.
        summary_dict (dict): Stores the summary of metrics extracted from the log file.
    """

    def __init__(self):
        self.separator_count = 0
        self.summary_dict = {}

    def _get_output_file_path(self):
        """
        Constructs the output file path.

        Returns:
            Path: The path to the output file.
        """
        current_file_path = Path(__file__).resolve()
        project_root = current_file_path.parent.parent
        output_file_path = project_root / OUTPUT_DIRECTORY / OUTPUT_FILENAME
        return output_file_path

    def _parse_keys(self, line):
        """
        Parses the keys from the given line.

        Args:
            line (str): The line containing the keys.

        Returns:
            list: A list of keys.
        """
        return line.replace("INFO  :   VERTICES      ", "").split()

    def _parse_metrics(self, line):
        """
        Parses the metrics from the given line.

        Args:
            line (str): The line containing the metrics.

        Returns:
            list: A list of metrics.
        """
        return line.replace("INFO  : ", "").replace(",", "").split()

    def _extract_key_value(self, metrics_list):
        """
        Extracts the key and values from the metrics list.

        Args:
            metrics_list (list): The list of metrics.

        Returns:
            tuple: A key and a list of values.
        """
        key = ' '.join(metrics_list[:2])
        values = [int(value) if "." not in value else value for value in metrics_list[2:]]
        return key, values

    def _populate_summary_dict(self, keys, metrics):
        """
        Populates the summary dictionary with keys and metrics.

        Args:
            keys (list): The list of keys.
            metrics (list): The list of metrics.
        """
        key, values = self._extract_key_value(metrics)
        self.summary_dict[key] = dict(zip(keys, values))

    def create_summary_file(self, start_line, input_file):
        """
        Creates the summary file from the input log file.

        Args:
            start_line (str): The line to start parsing from.
            input_file (file): The input log file.
        """
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
