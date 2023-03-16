"""some helpers"""

import os
import sys
import json

DATA_PATH = 'data'
SETTINGS_FILENAME = '..\\..\\..\\data\\settings.json'
POP_SIZE = 20
INITIAL_RATING = 3
MALE = 'Male'
FEMALE = 'Female'
FUTA = 'Futa'
MAIN_SCRIPT_NAME = "VAM Evolutionary Character Creation.py"
STORABLES = 'storables'

THUMBNAIL_SIZE = 184, 184
NO_THUMBNAIL_FILENAME = "no_thumbnail.jpg"
CHILD_THUMBNAIL_FILENAME = "child_thumbnail.jpg"


class Settings(dict):
    def __init__(self):
        super().__init__()
        self.load()

    def save(self):
        """ Saves the settings as a json file to DATA_PATH/SETTINGS_FILENAME """
        dir_path = ''
        if getattr(sys, 'frozen', False):
            dir_path = os.path.dirname(sys.executable)
        elif __file__:
            dir_path = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(dir_path, DATA_PATH, SETTINGS_FILENAME)
        with open(filename, 'w') as json_file:
            print("Writing settings to:", filename)
            json.dump(self, json_file, indent=3)

    def load(self):
        """ Fills settings with the settings in the DATA_PATH/SETTINGS_FILENAME json_file """
        dir_path = ''
        settings = dict()
        if getattr(sys, 'frozen', False):
            dir_path = os.path.dirname(sys.executable)
        elif __file__:
            dir_path = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(dir_path, DATA_PATH, SETTINGS_FILENAME)
        if os.path.isfile(filename):
            with open(filename) as json_file:
                print("Reading settings from:", filename)
                data = json.load(json_file)
                self.update(data)

def strip_dir_string_to_max_length(dir_string, length):
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
    if len(dir_string) <= length:
        return dir_string
    parts = dir_string.split("\\")
    stripped_string = ""
    index = len(parts) - 1
    while (len(parts[index]) + 1) <= ((length - 4) - (len(stripped_string) - 1)):
        if index == -1:
            break
        stripped_string = parts[index] + "\\" + stripped_string
        index -= 1
    stripped_string = stripped_string[:-1]  # remove trailing "\"
    return "(…)\\" + stripped_string


def is_favorite(appearance):
    return appearance['is_fav']


def generate_list_element(lst):
    """ Returns one element of the list, starts again if list is depleted """
    while True:
        for element in lst:
            yield element


if __name__ == '__main__':
    print(f'I am just a module, please launch the main script "{MAIN_SCRIPT_NAME}".')
