"""
Business logic for VAM Evolutionary Character Creation
By Pino Sante
Please credit me if you change, use or adapt this file.
"""

import os
import sys
import json

from .utility import *


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

    def is_setting_valid(self, setting_name):
        return setting_name in self and len(self[setting_name]) != 0

    def are_settings_valid(self):
        messages = list()

        if not self.is_setting_valid('VAM base dir'):
            messages.append('· Please select the VAM base folder')
        if not self.is_setting_valid('appearance dir'):
            messages.append('· Please select an Appearance folder')
        if not self.is_setting_valid('child template'):
            messages.append('· Please select a child template appearance')
        if 'morph threshold' not in self:
            messages.append('· Please enter a valid value for min morph number')
        if 'min morph threshold' not in self:
            messages.append('· Please enter a valid value for min morph threshold')
        if 'source files' not in self:
            messages.append('· Please have at least 2 Parent files')

        return len(messages) == 0, messages

    def get_vam_path(self, pathstring):
        """ Returns the full path with VAM_BASE_PATH/pathstring and returns False if there was no VAM base dir. """
        if "VAM base dir" not in self:
            return False
        if len(self['VAM base dir']) == 0:
            return False
        return os.path.join(self['VAM base dir'], pathstring)

    def get_vam_default_appearance_path(self):
        """ Returns the path to the default Appearance directory based on the VAM base path, or returns '' if no base path
            is found in settings. """
        path = ''
        if 'VAM base dir' in self:
            if len(self['VAM base dir']) > 0:
                appearance_path = "Custom/Atom/Person/Appearance"
                path = os.path.join(self['VAM base dir'], appearance_path)
        return path
