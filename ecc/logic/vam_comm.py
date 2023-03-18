"""
Business logic for VAM Evolutionary Character Creation
By Pino Sante
Please credit me if you change, use or adapt this file.
"""

import copy
import random
import shutil
import os
import time
import json

from collections import defaultdict

import numpy as np

from ..common.utility import *


class VamComm:
    def __init__(self, settings):
        self.settings = settings

    def broadcast_generation_number_to_vam(self, number):
        """ Updates the file
            PATH_TO_VAM\\Custom\\Atom\\UIText\\VAM Evolutionary Character Creation\\Preset_Python2VAMGeneration.vap
            with the generation number, so the Vam Evoluationary Character Creation Companion can display the
            proper generation number. """
        # try to save file
        path = self.settings.get_vam_path(
            r'Custom\Atom\UIText\VAM Evolutionary Character Creation\Preset_Python2VAMGeneration.vap')
        if not path:
            return False
        self.write_value_to_vam_file(path, "Text", "text", "Generation " + str(number))

    def broadcast_last_command_to_vam(self, command):
        # todo: candidate for logic
        """ Updates the file
            PATH_TO_VAM\\Custom\\Atom\\UIText\\VAM Evolutionary Character Creation\\Preset_Python2VAMText.vap
            with the last command, so the Vam Evoluationary Character Creation Companion save can check if the python
            script is still running properly, by comparing the command VAM sent to python, with this broadcast command
            from python back. """
        path = self.settings.get_vam_path(
            r'Custom\Atom\UIText\VAM Evolutionary Character Creation\Preset_Python2VAMText.vap')
        if not path:
            return False
        self.write_value_to_vam_file(path, 'Text', 'text', command)

    def broadcast_message_to_vam_rating_blocker(self, text):
        # todo: candidate for logic
        path = self.settings.get_vam_path(
            r'Custom\Atom\UIButton\VAM Evolutionary Character Creation\Preset_Python2VAMRatingBlocker.vap')
        if not path:
            return False
        self.write_value_to_vam_file(path, 'Text', 'text', text)

    def write_value_to_vam_file(self, path, id_string, needed_key, replacement_string):
        """ Updates the VAM file with path, by loading the storables array inside, and looking for the dictionary with
            ("id", "id_string") as (key, value) pair. Then, within this dictionary, it will overwrite the (key, value)
            pair with ("needed_key", "replacement_string"). Then it will overwrite the VAM file. """
        # todo: candidate for logic
        try:
            with open(path, encoding='utf-8') as f:
                text_json = json.load(f)
            text_json['storables'] = self.replace_value_from_id_in_dict_list(text_json[STORABLES], id_string,
                                                                        needed_key,
                                                                        replacement_string)
            with open(path, 'w', encoding='utf-8') as json_file:
                json.dump(text_json, json_file, indent=3)
        except IOError as e:
            print(e)

    @staticmethod
    def replace_value_from_id_in_dict_list(dict_list, id_string, needed_key, replacement_string):
        for dictionary in dict_list:
            if id_string in dictionary.values():
                if needed_key in dictionary:
                    dictionary[needed_key] = replacement_string
                    return dict_list
        return None



if __name__ == '__main__':
    print(f'I am just a module, please launch the main script "{MAIN_SCRIPT_NAME}".')
