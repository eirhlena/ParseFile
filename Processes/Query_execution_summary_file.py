"""
This script defines the QuerySummary class, which processes log files to extract
and summarize query execution metrics. The extracted metrics are saved as a JSON file.
The script includes methods for determining the output file path, reading lines,
parsing lines to extract key-value pairs, and generating the summary file.

Classes:
    QuerySummary: Processes log files to extract and summarize query execution metrics.

Usage:
    Initialize a QuerySummary object and call the `create_summary_file` method
    with the input file.
"""

import json
from pathlib import Path
import logging

OUTPUT_DIRECTORY = "Output"
OUTPUT_FILENAME = "Query_Execution_Summary.txt"
DELIMITER = 'INFO  : ----------------------------------------------------------------------------------------------'

class QuerySummary:
    """
    A class to summarize query execution metrics from a log file.

    Attributes:
        delimiter_count (int): Tracks the number of delimiters encountered.
        summary_dict (dict): Stores the summary of metrics extracted from the log file.
    """

    def __init__(self):
        self.delimiter_count = 0
        self.summary_dict = {}

    def _get_output_file_path(self):
        """
        Constructs the output file path.

        Returns:
            Path: The path to the output file.
        """
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent
        return project_root / OUTPUT_DIRECTORY / OUTPUT_FILENAME

    def _read_line(self, file):
        """
        Reads the next line from the file.

        Args:
            file (file object): The file object to read from.

        Returns:
            str: The next line from the file.
        """
        return file.readline()

    def _within_metric_section(self):
        """
        Checks if the current position is within the metric section.

        Returns:
            bool: True if within the metric section, False otherwise.
        """
        return self.delimiter_count < 2

    def _parse_line(self, line):
        """
        Parses a line to extract the metric key and value.

        Args:
            line (str): The line containing the metrics.

        Returns:
            tuple: A key and a value.
        """
        metrics = line.replace("INFO  : ", "").split()
        key = ' '.join(metrics[:-1])
        value = metrics[-1]
        return key, value

    def create_summary_file(self, input_file):
        """
        Creates the query execution summary file from the input log file.

        Args:
            input_file (file object): The input log file.
        """
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
