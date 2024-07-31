"""
arguments_and_logging.py

This script defines the Arguments and Loggings classes, which handle command line
arguments and configure logging respectively. The Arguments class processes command line
arguments to determine the input file path. The Loggings class sets up logging to a file
and the console.

Classes:
    Arguments: Processes command line arguments to determine the input file path.
    Loggings: Configures logging to a file and the console.

Usage:
    - Initialize an Arguments object and call the `get_filepath` method to get the input file path.
    - Initialize a Loggings object and call the `set_up_logs` method to configure logging.
"""

import os
import sys
import logging
from pathlib import Path

DEFAULT_FILE_NAME = 'beeline_consent_query_stderr.txt'

class Arguments:
    """
    A class to handle command line arguments and determine the input file path.

    Methods:
        handle_command_line_args: Processes command line arguments to determine the input file path.
        get_filepath: Returns the determined input file path.
    """

    def handle_command_line_args(self):
        """
        Returns:
            str: The path to the default input file if no arguments are given.

        Raises:
            SystemExit: If unexpected additional command line arguments are detected.
        """
        if not sys.argv[1:]:
            current_script = os.path.abspath(__file__)
            directory_of_script = os.path.dirname(current_script)
            relative_input_folder = "../Input/"
            default_file_path = os.path.join(directory_of_script, relative_input_folder, DEFAULT_FILE_NAME)
            return default_file_path
        else:
            logging.critical('Unexpected additional command line arguments detected.')
            sys.exit(1)

    def get_filepath(self):
        """
        Returns:
            str: The path to the input file.
        """
        filepath = self.handle_command_line_args()
        logging.info("Arguments verification and filepath retrieval completed successfully")
        return filepath

class Loggings:
    """
    A class to configure logging to a file and the console.

    Methods:
        configure_logging: Sets up logging to a file.
        configure_console_logging: Sets up logging to the console.
        set_up_logs: Configures both file and console logging.
    """

    def configure_logging(self):
        """
        Sets up logging to a file.
        """
        current_script = os.path.abspath(__file__)
        script_directory = os.path.dirname(current_script)
        parent_directory = Path(script_directory).parent
        logs_directory = "Logs"
        log_file_name = "logs_info.log"
        log_file_path = os.path.join(parent_directory, logs_directory, log_file_name)

        logging.basicConfig(
            filename=log_file_path,
            filemode='w',
            format='%(asctime)s,%(msecs)d %(levelname)s %(message)s',
            datefmt='%H:%M:%S',
            level=logging.INFO
        )

    def configure_console_logging(self):
        """
        Sets up logging to the console.
        """
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s,%(msecs)d - %(levelname)s - %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

    def set_up_logs(self):
        """
        Configures both file and console logging.
        """
        self.configure_logging()
        self.configure_console_logging()
        logging.info("Setup of logs file and console logging completed successfully")
