"""
Business logic for VAM Evolutionary Character Creation
By Pino Sante
Please credit me if you change, use or adapt this file.
"""

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
