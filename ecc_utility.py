'''stuff'''

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
