from Processes.setup import Loggings, Arguments
from Processes.parsing_files import ParseInputFile

def main():

    loggings_setup = Loggings()
    loggings_setup.set_up_logs()
    argument_checks = Arguments()
    filepath = argument_checks.get_filepath()

    file_parser = ParseInputFile()
    file_parser.parse_file(filepath)


if __name__ == '__main__':
    main()