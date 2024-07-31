import os, sys
import logging
from pathlib import Path
DEFAULT_FILE_NAME = 'beeline_consent_query_stderr.txt'

class Arguments:

    def handle_command_line_args(self):
        # Determine if the script was executed with no arguments
        if not sys.argv[1:]:
            # Build the path to the default input file if no arguments are given
            current_script = os.path.abspath(__file__)  # Get the absolute path of the script
            directory_of_script = os.path.dirname(current_script)  # Extract directory path from the script path
            relative_input_folder = "../Input/"
            default_file_path = os.path.join(directory_of_script, relative_input_folder, DEFAULT_FILE_NAME)
            return default_file_path
        else:
            # Log an error message and terminate if extra arguments are present
            logging.critical('Unexpected additional command line arguments detected.')
            sys.exit(1)  # Exit with an error code to signal abnormal termination


    def get_filepath(self):
        filepath = self.handle_command_line_args()
        # self._verify_existance_of_file(filepath)
        logging.info("Arguments verification and filepath retrieval completed succesfully")
        return filepath

class Loggings:

    def configure_logging(self):
        # Determine the absolute path of the current script
        current_script = os.path.abspath(__file__)
        # Extract the directory containing the script
        script_directory = os.path.dirname(current_script)
        # Get the parent directory of the script's directory
        parent_directory = Path(script_directory).parent
        # Define the logs directory and the log file name
        logs_directory = "Logs"
        log_file_name = "logs_info.log"
        # Construct the full path for the log file
        log_file_path = os.path.join(parent_directory, logs_directory, log_file_name)

        # Set up the logging configuration
        logging.basicConfig(
            filename=log_file_path,
            filemode='w',
            format='%(asctime)s,%(msecs)d %(levelname)s %(message)s',
            datefmt='%H:%M:%S',
            level=logging.INFO
        )

    def _set_up_console_logs(self):
        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(asctime)s,%(msecs)d - %(levelname)s - %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(console)

    def set_up_logs(self):
        self.configure_logging()
        self._set_up_console_logs()
        logging.info("Setup of logs file and loggings on console completed succesfully")