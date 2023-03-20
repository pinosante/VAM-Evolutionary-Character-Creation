"""
Business logic for VAM Evolutionary Character Creation
By Pino Sante
Please credit me if you change, use or adapt this file.
"""

import json

from ..common.utility import *


class VamComm:
    def __init__(self, settings, master, execute_vam_command_callback):
        self.master = master
        self.settings = settings
        self.execute_vam_command_callback = execute_vam_command_callback

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

    @staticmethod
    def value_from_id_in_dict_list(dict_list, id_string, needed_key):
        for dictionary in dict_list:
            if id_string in dictionary.values():
                if needed_key in dictionary:
                    return dictionary[needed_key]
        return None

    def scan_vam_for_command_updates(self, lastcommand):
        """ Continously check if
            PATH_TO_VAM\\Custom\\Atom\\UIText\\VAM Evolutionary Character Creation\\Preset_VAM2PythonText.vap
            has a new command string. If so, try to execute that command by calling execute_VAM_command() """
        # todo: candidate for logic
        # try to open file
        path = self.settings.get_vam_path(
                r'Custom\Atom\UIText\VAM Evolutionary Character Creation\Preset_VAM2PythonText.vap')
        if not path:
            return
        try:
            with open(path, encoding='utf-8') as f:
                linestring = f.read()
                lines = linestring.split('\n')
                # print(f"Length of lines {len(lines)}")
                if len(lines) < 70:  # incomplete file
                    raise IOError(f'Not enough lines ({len(lines)}) in the file ')
                # f.seek(0) # back to start of file
                command_json = json.loads(linestring)
                command = self.value_from_id_in_dict_list(command_json['storables'], 'Text', 'text')
                if lastcommand == "Initialize":  # if we Initialize we have to set lastcommand as the file we just read
                    lastcommand = command
                if command != lastcommand:
                    self.broadcast_last_command_to_vam(command)
                    self.execute_vam_command_callback(command)
                    print(f'We have a new command: {command}')
        except IOError as e:
            print(e)
            self.master.after(25, lambda lastcommand=lastcommand: self.scan_vam_for_command_updates(lastcommand))
        else:
            self.master.after(25, lambda lastcommand=command: self.scan_vam_for_command_updates(lastcommand))



if __name__ == '__main__':
    print(f'I am just a module, please launch the main script "{MAIN_SCRIPT_NAME}".')
