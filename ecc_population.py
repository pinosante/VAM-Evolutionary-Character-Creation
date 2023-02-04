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
        self.nmorph_display = None
        self.rating = ecc_utility.INITIAL_RATING
        self.rating_buttons = list()

    def initialize_ui(self, frame):
        self.file_button = tk.Button(frame, text="Parent " + str(self.index),
                                                 bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR,
                                                 activebackground=BUTTON_ACTIVE_COLOR,
                                                 command=lambda i=self.index: self.select_file(i), width=10)
        self.file_button.grid(row=self.index + 1, column=0, sticky=tk.W)
        self.file_name_display = tk.Label(frame, text=NO_FILE_SELECTED_TEXT,
                                             font=FILENAME_FONT, width=28, anchor="w", bg=BG_COLOR,
                                             fg=FG_COLOR)
        self.file_name_display.grid(row=self.index + 1, column=1, sticky=tk.W)
        self.nmorph_display = tk.Label(frame, text="N/A", bg=BG_COLOR, fg=FG_COLOR)
        self.nmorph_display.grid(row=i + 1, column=2, sticky=tk.W)
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
        self.nmorph_display.destroy()
        del self.file_button
        del self.file_name_display
        del self.nmorph_display


class Population:
    def __init__(self, size):
        self.chromosomes = [Chromosome(index) for index in range(size)]


