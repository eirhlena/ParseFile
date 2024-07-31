from Processes.configuration import Loggings, Arguments
from Processes.parsing_files import ParseInputFile

def main():

    loggings = Loggings()
    loggings.set_up_logs()
    arg_check = Arguments()
    filepath = arg_check.get_filepath()

    parser = ParseInputFile()
    parser.parse_file(filepath)


if __name__ == '__main__':
    main()