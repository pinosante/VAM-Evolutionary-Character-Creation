import copy
import json
import os
import pathlib
import random
import tkinter as tk
from collections import defaultdict
from datetime import datetime
from fnmatch import fnmatch
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

import numpy as np

import ecc_logic
import ecc_utility
from ecc_gui_constants import *


class Chromosome:
    def __init__(self, index):
        self.index = index
        self.filename = ''
        self.short_filename = ''
        self.appearance = None
        self.can_load = False
        self.file_button = None
        self.file_name_display = None
        self.child_label = None
        self.n_morph_display = None
        self.rating = ecc_utility.INITIAL_RATING
        self.rating_buttons = list()

    def initialize_ui(self, frame):
        index = self.index + 1
        self.file_button = tk.Button(frame, text=f'Parent {index}',
                                     bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR,
                                     activebackground=BUTTON_ACTIVE_COLOR,
                                     command=lambda i=index: self.select_file(i), width=10)
        self.file_button.grid(row=index, column=0, sticky=tk.W)
        self.file_name_display = tk.Label(frame, text=NO_FILE_SELECTED_TEXT,
                                          font=FILENAME_FONT, width=28, anchor='w', bg=BG_COLOR,
                                          fg=FG_COLOR)
        self.file_name_display.grid(row=index, column=1, sticky=tk.W)
        self.n_morph_display = tk.Label(frame, text="N/A", bg=BG_COLOR, fg=FG_COLOR)
        self.n_morph_display.grid(row=index + 1, column=2, sticky=tk.W)
        self.can_load = False

    def update_gui_file(self, filename, appearance):
        self.filename = filename
        self.short_filename = os.path.basename(filename)[7:-4]  # remove Preset_ and .vap
        self.file_name_display.configure(text=self.short_filename)
        self.appearance = appearance
        self.can_load = True

    def destroy_ui(self):
        self.file_button.destroy()
        self.file_name_display.destroy()
        self.n_morph_display.destroy()
        del self.file_button
        del self.file_name_display
        del self.n_morph_display

    def get_rating_button(self, rating):
        """rating button now are kept inside a zero based list, so decrement the one-based rating"""
        assert MIN_RATING <= rating <= MAX_RATING
        return self.rating_buttons[rating - 1]


class Population:
    def __init__(self, size):
        self.chromosomes = [Chromosome(index) for index in range(size)]

    def get_chromosome(self, index):
        """index is one-based, but chromosomes are inside a zero-based list"""
        assert 1 <= index <= ecc_utility.POP_SIZE
        c = self.chromosomes[index - 1]
        assert c.index == index - 1
        return c


if __name__ == '__main__':
    print(f'I am just a module, please launch the main script "{MAIN_SCRIPT_NAME}".')
