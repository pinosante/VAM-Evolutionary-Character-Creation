'''

By Pino Sante

Please credit me if you change, use or adapt this file.

'''

import os
import sys
import json
import tkinter as tk

import GUI
import Logic


BG_COLOR = "#F9F9F9"
DATA_PATH = "data"
SETTINGS_FILENAME = "settings.json"
ICON_FILENAME = "VAM Evolutionary Character Creation.ico"


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


def main():
    '''
    create the business logic and the main window and launch them
    '''
    settings = load_settings()

    main_window = tk.Tk()
    main_window.configure(bg=BG_COLOR)
    main_window.option_add("*font", "Calibri 9")
    main_window.iconbitmap(os.path.join(DATA_PATH, ICON_FILENAME))

    app = GUI.AppWindow(settings)

    app.initialize()
    main_window.mainloop()

    save_settings(settings)


if __name__ == '__main__':
    main()
