'''stuff'''

import os
import sys
import json

DATA_PATH = "data"
SETTINGS_FILENAME = "settings.json"


def save_settings(settings):
    """ Saves the settings as a json file to DATA_PATH/SETTINGS_FILENAME """
    if getattr(sys, 'frozen', False):
        dir_path = os.path.dirname(sys.executable)
    elif __file__:
        dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(dir_path, DATA_PATH, SETTINGS_FILENAME)
    with open(filename, 'w') as json_file:
        print("Writing settings to:", filename)
        json.dump(settings, json_file, indent=3)


def load_settings():
    """ Fills settings with the settings in the DATA_PATH/SETTINGS_FILENAME json_file """
    settings = {}
    if getattr(sys, 'frozen', False):
        dir_path = os.path.dirname(sys.executable)
    elif __file__:
        dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(dir_path, DATA_PATH, SETTINGS_FILENAME)
    if os.path.isfile(filename):
        with open(filename) as json_file:
            print("Reading settings from:", filename)
            settings = json.load(json_file)
    return settings



def strip_dir_string_to_max_length(dirstring, length):
    """ Takes a string directory, and cuts it at the '/' in the string such that the
        length of the stripped string is as large as possible but stays smaller than
        the total 'length'. A '(…)/' is added if the string had to be cut.

        Example:
        strip_dir_string_to_max_length("C:/456/890/234.txt", 99)
        >C:/456/890/234.txt
        strip_dir_string_to_max_length("C:/456/890/234.txt", 15)
        >(…)/890/234.txt
        strip_dir_string_to_max_length("C:/456/890/234.txt", 14)
        >(…)/234.txt
        """
    if len(dirstring) <= length:
        return dirstring
    parts = dirstring.split("\\")
    stripped_string = ""
    index = len(parts) - 1
    while (len(parts[index]) + 1) <= ((length - 4) - (len(stripped_string) - 1)):
        if index == -1:
            break
        stripped_string = parts[index] + "\\" + stripped_string
        index -= 1
    stripped_string = stripped_string[:-1]  # remove trailing "\"
    return "(…)\\" + stripped_string


if __name__ == '__main__':
    print('I am just a module, please launch the main script "VAM Evolutionary Character Creation.py".')
