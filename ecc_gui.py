'''
GUI for VAM Evolutionary Character Creation 
By Pino Sante
Please credit me if you change, use or adapt this file.
'''
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

THUMBNAIL_SIZE = 184, 184
NO_THUMBNAIL_FILENAME = "no_thumbnail.jpg"
CHILD_THUMBNAIL_FILENAME = "child_thumbnail.jpg"
ICON_FILENAME = "VAM Evolutionary Character Creation.ico"
APP_TITLE = "VAM Evolutionary Character Creation by Pino Sante"
NO_FILE_SELECTED_TEXT = "…"
SETTINGS_FILENAME = "settings.json"
DATA_PATH = "data"
SAVED_CHILDREN_PATH = "VAM Evolutionary Character Creation"
CHILDREN_FILENAME_PREFIX = "Evolutionary_Child_"
POP_SIZE = 20
MINIMAL_RATING_FOR_KEEP_ELITES = 2
INITIAL_RATING = 3
DEFAULT_MAX_KEPT_ELITES = 1
DEFAULT_FONT = "Calibri"
FILENAME_FONT = ("Courier", 9)
BG_COLOR = "#F9F9F9"
FG_COLOR = "black"
BUTTON_BG_COLOR = "#ffbeed"
BUTTON_FG_COLOR = "black"
BUTTON_ACTIVE_COLOR = BUTTON_BG_COLOR
HOVER_COLOR = "#f900ff"
MAX_VAMDIR_STRING_LENGTH = 42
MAX_APPEARANCEDIR_STRING_LENGTH = 45
RATING_SUNKEN_BG_COLOR = BUTTON_BG_COLOR
RATING_SUNKEN_FG_COLOR = BUTTON_FG_COLOR
RATING_RAISED_BG_COLOR = BG_COLOR
RATING_RAISED_FG_COLOR = FG_COLOR
RATING_HOVER_BG_COLOR = BUTTON_BG_COLOR
RATING_HOVER_FG_COLOR = BUTTON_FG_COLOR
RATING_ACTIVE_BG_COLOR = BUTTON_BG_COLOR
RATING_ACTIVE_FG_COLOR = BUTTON_FG_COLOR

# selection of appearances method texts
CHOOSE_ALL_FAVORITES_TEXT = "Choose All Favorites"
CHOOSE_ALL_TEXT = "Choose All Appearances"
CHOOSE_FILES_TEXT = "Choose Files"

###
### Below are the settings for a dark theme
###
# BG_COLOR = "black"
# FG_COLOR = "white"
# BUTTON_BG_COLOR = "#fc84ff"
# BUTTON_FG_COLOR = "black"
# BUTTON_ACTIVE_COLOR = BUTTON_BG_COLOR
# HOVER_COLOR = "#fc84ff"
# RATING_SUNKEN_BG_COLOR = BUTTON_BG_COLOR
# RATING_SUNKEN_FG_COLOR = BUTTON_FG_COLOR
# RATING_RAISED_BG_COLOR = "#F9F9F9"
# RATING_RAISED_FG_COLOR = "black"
# RATING_HOVER_BG_COLOR = BUTTON_BG_COLOR
# RATING_HOVER_FG_COLOR = BUTTON_FG_COLOR
# RATING_ACTIVE_BG_COLOR = BUTTON_BG_COLOR
# RATING_ACTIVE_FG_COLOR = BUTTON_FG_COLOR


class AppWindow(tk.Frame):
    def __init__(self, settings, generator):
        super().__init__()
        self.settings = settings
        self.generator = generator

        # create a dictionary to select appearances
        self.select_appearances_strategies = {
            CHOOSE_ALL_FAVORITES_TEXT: lambda: self.get_fav_appearance_filenames(),
            CHOOSE_ALL_TEXT: lambda: self.get_all_appearance_filenames(),
            CHOOSE_FILES_TEXT: lambda: self.get_selected_appearance_filenames()
        }

        self.initUI()

    def initUI(self):
        self.master.title(APP_TITLE)

        subtitlefont = (DEFAULT_FONT, 11, "bold")
        subtitlepadding = 1

        ###
        ### TITLE
        ###
        self.titleframe = tk.Frame(self.master, bg=BG_COLOR)
        self.titleframe.grid(row=0, column=1, padx=10, pady=0, sticky="nsew")
        self.titleframe.grid_columnconfigure(0, weight=1)
        self.titlelabel = tk.Label(self.titleframe, text="Initialization",
                            font=(DEFAULT_FONT, 14, "bold"), bg=BG_COLOR, fg=FG_COLOR)
        self.titlelabel.grid(row=0, column=0, sticky=tk.W)

        ###
        ### VAM DIRECTORY
        ###
        self.vamdirframe = tk.Frame(self.master, bg=BG_COLOR)
        self.vamdirframe.grid(row=1, column=1, padx=10, pady=subtitlepadding, sticky=tk.W)
        self.vamdirtitlelabel = tk.Label(self.vamdirframe,
                            text="Step 1: Select VAM Base Folder (with VaM.exe)",
                            font=subtitlefont, bg=BG_COLOR, fg=FG_COLOR)
        self.vamdirtitlelabel.grid(columnspan=50, row=0, column=0, sticky=tk.W)
        self.vamdirbutton = tk.Button(self.vamdirframe, text="VAM Base Folder", bg=BUTTON_BG_COLOR,
                            fg=BUTTON_FG_COLOR,
                            activebackground=BUTTON_ACTIVE_COLOR, relief=tk.RAISED,
                            command=lambda: self.select_vamdir())
        self.vamdirbutton.grid(row=1, column=0, sticky=tk.W)
        self.vamdirlabel = tk.Label(self.vamdirframe, text=NO_FILE_SELECTED_TEXT,
                            font=FILENAME_FONT, anchor=tk.W, width=MAX_VAMDIR_STRING_LENGTH,
                            bg=BG_COLOR, fg=FG_COLOR)
        self.vamdirlabel.grid(row=1, column=1, sticky=tk.W)

        ###
        ### APPEARANCE DIRECTORY
        ###
        self.appearancedirframe = tk.Frame(self.master, bg=BG_COLOR)
        self.appearancedirframe.grid(row=2, column=1, padx=10, pady=subtitlepadding, sticky=tk.W)
        self.appearancedirtitlelabel = tk.Label(self.appearancedirframe,
                            text="Step 2: Select Appearance folder to use",
                            font=subtitlefont, bg=BG_COLOR, fg=FG_COLOR)
        self.appearancedirtitlelabel.grid(columnspan=50, row=0, column=0, sticky=tk.W)
        self.appearancedirbutton = tk.Button(self.appearancedirframe, text="Select Folder",
                            bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR,
                            activebackground=BUTTON_ACTIVE_COLOR, relief=tk.RAISED,
                            command=lambda: self.select_appearancedir())
        self.appearancedirbutton.grid(row=1, column=0, sticky=tk.W)
        self.appearancedirlabel = tk.Label(self.appearancedirframe, text=NO_FILE_SELECTED_TEXT,
                            font=FILENAME_FONT, anchor=tk.W, width=MAX_APPEARANCEDIR_STRING_LENGTH,
                            bg=BG_COLOR, fg=FG_COLOR)
        self.appearancedirlabel.grid(row=1, column=1, sticky=tk.W)

        ###
        ### CHILD TEMPLATE
        ###
        self.childtemplateframe = tk.Frame(self.master, bg=BG_COLOR)
        self.childtemplateframe.grid(row=3, column=1, padx=10, pady=subtitlepadding, sticky=tk.W)
        self.childtemplatelabel = tk.Label(self.childtemplateframe,
                            text="Step 3: Select Child Template Appearance", font=subtitlefont,
                            bg=BG_COLOR, fg=FG_COLOR)
        self.childtemplatelabel.grid(columnspan=50, row=0, column=0, sticky=tk.W, pady=(0, 0))

        self.childtemplatebutton = {}
        self.childtemplatebutton['Female'] = tk.Button(self.childtemplateframe, text="Female",
                            bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, activebackground=BUTTON_ACTIVE_COLOR,
                            command=lambda: self.select_template_file(["Female"],
                            "Please Select Parent Template"))
        self.childtemplatebutton['Female'].grid(row=1, column=0, sticky=tk.W, padx=0)
        self.childtemplatebutton['Male'] = tk.Button(self.childtemplateframe, text="Male",
                            bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, activebackground=BUTTON_ACTIVE_COLOR,
                            command=lambda: self.select_template_file(["Male"],
                            "Please Select Parent Template"))
        self.childtemplatebutton['Male'].grid(row=1, column=1, sticky=tk.W, padx=0)
        self.childtemplatebutton['Futa'] = tk.Button(self.childtemplateframe, text="Futa",
                            bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, activebackground=BUTTON_ACTIVE_COLOR,
                            command=lambda: self.select_template_file(["Futa"],
                            "Please Select Parent Template"))
        self.childtemplatebutton['Futa'].grid(row=1, column=2, sticky=tk.W, padx=0)
        self.childtemplate = dict()
        self.childtemplate['label'] = tk.Label(self.childtemplateframe, text=NO_FILE_SELECTED_TEXT,
                            font=FILENAME_FONT, bg=BG_COLOR, fg=FG_COLOR)
        self.childtemplate['label'].grid(row=1, column=3, sticky=tk.W, padx=0)

        ###
        ### PARENT FILES
        ###
        self.sourcefilesframe = tk.Frame(self.master, bg=BG_COLOR)
        self.sourcefilesframe.grid(row=4, column=1, padx=10, pady=subtitlepadding, sticky=tk.W)
        self.sourcefileslabel = tk.Label(self.sourcefilesframe, text="Step 4: Select Parent File Source",
                                         font=subtitlefont, bg=BG_COLOR, fg=FG_COLOR)
        self.sourcefileslabel.grid(columnspan=2, row=0, column=0, sticky=tk.W, pady=(0, 0))
        self.allappearancesbutton = tk.Button(self.sourcefilesframe, text="All Appearances", bg=BUTTON_BG_COLOR,
                                              fg=BUTTON_FG_COLOR, activebackground=BUTTON_ACTIVE_COLOR,
                                              command=lambda: self.choose_all_appearances())
        self.allappearancesbutton.grid(row=1, column=0, sticky=tk.W)
        self.allfavoritesbutton = tk.Button(self.sourcefilesframe, text="All Favorited Appearances", bg=BUTTON_BG_COLOR,
                                            fg=BUTTON_FG_COLOR, activebackground=BUTTON_ACTIVE_COLOR,
                                            command=lambda: self.choose_all_favorites())
        self.allfavoritesbutton.grid(row=1, column=1, sticky=tk.W)
        self.choosefilesbutton = tk.Button(self.sourcefilesframe, text=CHOOSE_FILES_TEXT, bg=BUTTON_BG_COLOR,
                                           fg=BUTTON_FG_COLOR, activebackground=BUTTON_ACTIVE_COLOR,
                                           command=lambda: self.choose_files())
        self.choosefilesbutton.grid(row=1, column=2, sticky=tk.W)

        ###
        ### CHROMOSOMELIST
        ###
        self.parentselectionframe = tk.Frame(self.master, bg=BG_COLOR)
        self.parentselectionframe.grid(row=5, column=1, padx=10, pady=subtitlepadding, sticky=tk.W)
        self.chromosomelabel = tk.Label(self.parentselectionframe, text="Step 5: Select Parent Files",
                                        font=subtitlefont, bg=BG_COLOR, fg=FG_COLOR)
        self.chromosomelabel.grid(columnspan=2, row=0, column=0, sticky=tk.W, pady=(0, 0))

        self.columninfo = dict()
        self.columninfo['1'] = tk.Label(self.parentselectionframe, text="Parent Number", bg=BG_COLOR, fg=FG_COLOR)
        self.columninfo['1'].grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.columninfo['2'] = tk.Label(self.parentselectionframe, text="Filename", bg=BG_COLOR, fg=FG_COLOR)
        self.columninfo['2'].grid(row=1, column=1, sticky=tk.W)
        self.columninfo['3'] = tk.Label(self.parentselectionframe, text="Total Morphs", bg=BG_COLOR, fg=FG_COLOR)
        self.columninfo['3'].grid(row=1, column=2, sticky=tk.W)

        self.chromosome = dict()
        for i in range(1, POP_SIZE + 1):
            new_chromosome = dict()
            new_chromosome['filebutton'] = tk.Button(self.parentselectionframe, text="Parent " + str(i),
                                                              bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR,
                                                              activebackground=BUTTON_ACTIVE_COLOR,
                                                              command=lambda i=i: self.select_file(i), width=10)
            new_chromosome['filebutton'].grid(row=i + 1, column=0, sticky=tk.W)
            new_chromosome['filenamedisplay'] = tk.Label(self.parentselectionframe, text=NO_FILE_SELECTED_TEXT,
                                                                  font=FILENAME_FONT, width=28, anchor="w", bg=BG_COLOR,
                                                                  fg=FG_COLOR)
            new_chromosome['filenamedisplay'].grid(row=i + 1, column=1, sticky=tk.W)
            new_chromosome['nmorphdisplay'] = tk.Label(self.parentselectionframe, text="N/A", bg=BG_COLOR,
                                                                fg=FG_COLOR)
            new_chromosome['nmorphdisplay'].grid(row=i + 1, column=2, sticky=tk.W)
            new_chromosome['can load'] = False

            self.chromosome[str(i)] = new_chromosome

        ###
        ### ALTERNATIVE SHOW FAVORITE APPEARANCES FILE INFORMATION (AT SAME ROW AS CHROMOSOMELIST)
        ###
        self.favoritesframe = tk.Frame(self.master, bg=BG_COLOR)
        self.favoritesframe.grid(row=5, column=1, padx=10, pady=subtitlepadding, sticky=tk.W)
        self.favoriteslabel = tk.Label(self.favoritesframe, text="Step 5: Favorited Appearances Chosen",
                                       font=subtitlefont, bg=BG_COLOR, fg=FG_COLOR)
        self.favoriteslabel.grid(row=0, column=0, sticky=tk.W, pady=(0, 0))
        self.favoritesinfo = tk.Label(self.favoritesframe, text="", bg=BG_COLOR, fg=FG_COLOR)
        self.favoritesinfo.grid(row=1, column=0, sticky=tk.W, pady=(0, 0))
        self.favoritesframe.grid_remove()  # will be shown when needed

        ###
        ### INITIALIZATION METHOD
        ###
        self.methodframe = tk.Frame(self.master, bg=BG_COLOR)
        self.methodframe.grid(row=6, column=1, padx=10, pady=subtitlepadding, sticky=tk.W)
        self.methodlabel = tk.Label(self.methodframe, text="Step 6: Initialization Method", font=subtitlefont,
                                    bg=BG_COLOR, fg=FG_COLOR)
        self.methodlabel.grid(columnspan=2, row=0, column=0, sticky=tk.W, pady=(0, 0))
        self.gaussianbutton = tk.Button(self.methodframe, text="Gaussian Samples", bg=BUTTON_BG_COLOR,
                                        fg=BUTTON_FG_COLOR, activebackground=BUTTON_ACTIVE_COLOR,
                                        command=lambda: self.choose_gaussian_samples())
        self.gaussianbutton.grid(row=1, column=0, sticky=tk.W)
        self.randomcrossoverbutton = tk.Button(self.methodframe, text="Random Crossover", bg=BUTTON_BG_COLOR,
                                               fg=BUTTON_FG_COLOR, activebackground=BUTTON_ACTIVE_COLOR,
                                               command=lambda: self.choose_random_crossover())
        self.randomcrossoverbutton.grid(row=1, column=1, sticky=tk.W)

        ###
        ### OPTIONS
        ###
        self.optionsframe = tk.Frame(self.master, bg=BG_COLOR)
        self.optionsframe.grid(row=7, column=1, padx=10, pady=subtitlepadding, sticky=tk.W)

        option_row_number = 1
        options_label = tk.Label(self.optionsframe, text="Step 7: Options", font=subtitlefont, bg=BG_COLOR, fg=FG_COLOR)
        options_label.grid(columnspan=9, row=option_row_number, sticky=tk.W, pady=(0, 0))

        option_row_number += 1  # go to next row of the options menu
        self.threshold_label = tk.Label(self.optionsframe, text="A) Remove morphs with absolute value below:",
                                        anchor='w', bg=BG_COLOR, fg=FG_COLOR)
        self.threshold_label.grid(columnspan=5, row=option_row_number, column=0, sticky=tk.W, padx=(0, 0))

        # track if the threshold values are changed by the user and if so, update the morph info based on the setting
        self.threshold_var = tk.DoubleVar()
        self.threshold_var.set(0.01)
        self.threshold_var.trace_add("write", self.track_threshold_change)

        self.threshold_entry = tk.Entry(self.optionsframe, textvariable=self.threshold_var, fg=BUTTON_FG_COLOR,
                                        bg=BUTTON_BG_COLOR, width=7)
        self.threshold_entry.grid(columnspan=2, row=option_row_number, column=10, sticky=tk.W)

        self.threshold_label = tk.Label(self.optionsframe, text="(0 = keep all)", bg=BG_COLOR, fg=FG_COLOR)
        self.threshold_label.grid(row=option_row_number, column=12, sticky=tk.W)

        # minimum morphs needed in appearance to be available in file selection
        option_row_number += 1  # go to next row of the options menu
        self.minmorph_label = tk.Label(self.optionsframe, text="B) Only show appearances with morph count above:",
                                       anchor='w', bg=BG_COLOR, fg=FG_COLOR)
        self.minmorph_label.grid(columnspan=5, row=option_row_number, column=0, sticky=tk.W, padx=(0, 0))

        # track if the threshold values are changed by the user and if so, update the morph info based on the setting
        self.minmorph_var = tk.IntVar()
        self.minmorph_var.set(0)
        self.minmorph_var.trace_add("write", self.track_minmorph_change)

        self.minmorph_entry = tk.Entry(self.optionsframe, textvariable=self.minmorph_var, fg=BUTTON_FG_COLOR,
                                       bg=BUTTON_BG_COLOR, width=7)
        self.minmorph_entry.grid(columnspan=2, row=option_row_number, column=10, sticky=tk.W)

        self.minmorph_infolabel = tk.Label(self.optionsframe, text="(0 = show all)", bg=BG_COLOR, fg=FG_COLOR)
        self.minmorph_infolabel.grid(row=option_row_number, column=12, sticky=tk.W)

        option_row_number += 1  # go to next row of the options menu
        self.maxkeptelites_label = tk.Label(self.optionsframe, text="C) Max kept elites (highest rated):", anchor='w',
                                            bg=BG_COLOR, fg=FG_COLOR)
        self.maxkeptelites_label.grid(columnspan=5, row=option_row_number, column=0, sticky=tk.W, padx=(0, 0))

        # track if the maxkeptelites values are changed by the user
        self.maxkeptelites_var = tk.IntVar()
        self.maxkeptelites_var.set(DEFAULT_MAX_KEPT_ELITES)
        self.maxkeptelites_var.trace_add("write", self.track_maxkeptelites_change)

        self.maxkeptelites_entry = tk.Entry(self.optionsframe, textvariable=self.maxkeptelites_var, fg=BUTTON_FG_COLOR,
                                            bg=BUTTON_BG_COLOR, width=7)
        self.maxkeptelites_entry.grid(columnspan=2, row=option_row_number, column=10, sticky=tk.W)

        option_row_number += 1  # go to next row of the options menu
        self.recursivedirectorysearch_label = tk.Label(self.optionsframe,
                                                       text="D) Also read subdirectories in file selection:",
                                                       anchor='w', bg=BG_COLOR, fg=FG_COLOR)
        self.recursivedirectorysearch_label.grid(columnspan=5, row=option_row_number, column=0, sticky=tk.W)
        self.recursivedirectorysearch_yesbutton = tk.Button(self.optionsframe, text="Yes", bg=BUTTON_BG_COLOR,
                                                            fg=BUTTON_FG_COLOR, activebackground=BUTTON_ACTIVE_COLOR,
                                                            command=lambda: self.use_recursive_directory_search(True))
        self.recursivedirectorysearch_yesbutton.grid(row=option_row_number, column=10, sticky=tk.W)
        self.recursivedirectorysearch_nobutton = tk.Button(self.optionsframe, text="No", bg=BUTTON_BG_COLOR,
                                                           fg=BUTTON_FG_COLOR, activebackground=BUTTON_ACTIVE_COLOR,
                                                           command=lambda: self.use_recursive_directory_search(False))
        self.recursivedirectorysearch_nobutton.grid(row=option_row_number, column=11, sticky=tk.W)

        ###
        ### GENERATE CHILD BUTTON
        ###
        self.bottomframe = tk.Frame(self.master, bg=BG_COLOR)
        self.bottomframe.grid(row=8, column=1, padx=(10, 0), pady=0, sticky=tk.W)

        self.generatechild = tk.Button(
            self.bottomframe, text="Initialize Population", bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR,
            activebackground=BUTTON_ACTIVE_COLOR,
            command=lambda: self.generate_next_population(self.settings['method']),
            relief="flat", font=(DEFAULT_FONT, 15, "bold")
        )
        self.generatechild.grid(row=0, column=0, sticky=tk.W)

        self.filler_bottom = tk.Label(self.bottomframe, text="", width=1, height=10, bg=BG_COLOR, fg=FG_COLOR)
        self.filler_bottom.grid(row=0, column=1)


    def initialize(self):
        """ Runs at the start of the app to load all previously saved settings and sets defaults when settings are
            not found """
        if 'appearance dir' in self.settings:
            if len(self.settings['appearance dir']) < 1:
                appearancedir = NO_FILE_SELECTED_TEXT
            else:
                appearancedir = ecc_utility.strip_dir_string_to_max_length(self.settings['appearance dir'],
                                                               MAX_APPEARANCEDIR_STRING_LENGTH)
                self.appearancedirbutton.configure(relief=tk.SUNKEN)
        else:
            appearancedir = NO_FILE_SELECTED_TEXT
            self.settings['appearance dir'] = ""
        self.appearancedirlabel.configure(text=appearancedir)

        if 'recursive directory search' in self.settings:
            self.use_recursive_directory_search(self.settings['recursive directory search'])
        else:
            self.use_recursive_directory_search(False)

        if 'VAM base dir' in self.settings:
            if len(self.settings['VAM base dir']) < 1:
                vamdir = NO_FILE_SELECTED_TEXT
            else:
                vamdir = ecc_utility.strip_dir_string_to_max_length(self.settings['VAM base dir'], MAX_VAMDIR_STRING_LENGTH)
                self.vamdirbutton.configure(relief=tk.SUNKEN)
        else:
            vamdir = NO_FILE_SELECTED_TEXT
        self.vamdirlabel.configure(text=vamdir)

        if 'child template' in self.settings:
            if os.path.isfile(self.settings['child template']):
                self.childtemplate['label'].configure(
                    text=self.create_template_labeltext(self.settings['child template']))
                self.childtemplate['gender'] = ecc_logic.get_appearance_gender(ecc_logic.load_appearance(self.settings['child template']))
                self.press_childtemplate_button(self.childtemplate['gender'])

        if 'morph threshold' in self.settings:
            self.threshold_var.set(self.settings['morph threshold'])
        else:
            self.settings['morph threshold'] = 0.01

        if 'min morph threshold' in self.settings:
            self.minmorph_var.set(self.settings['min morph threshold'])
        else:
            self.settings['min morph threshold'] = 150
            self.minmorph_var.set(150)

        if 'max kept elites' in self.settings:
            self.maxkeptelites_var.set(self.settings['max kept elites'])
        else:
            self.settings['max kept elites'] = DEFAULT_MAX_KEPT_ELITES

        for i in range(1, POP_SIZE + 1):
            if 'file ' + str(i) in self.settings:
                if len(self.settings['file ' + str(i)]) > 0:
                    filename = self.settings['file ' + str(i)]
                    self.update_GUI_file(i, filename)
                    self.update_morph_info(i)

        if 'source files' in self.settings:
            if self.settings['source files'] == CHOOSE_FILES_TEXT:
                self.choose_files()
            elif self.settings['source files'] == CHOOSE_ALL_FAVORITES_TEXT:
                self.choose_all_favorites()
            elif self.settings['source files'] == CHOOSE_ALL_TEXT:
                self.choose_all_appearances()

        if 'method' in self.settings:
            if self.settings['method'] == "Gaussian Samples":
                self.choose_gaussian_samples()
            elif self.settings['method'] == "Random Crossover":
                self.choose_random_crossover()
        else:
            self.choose_random_crossover()

        if 'thumbnails per row' not in self.settings:
            self.settings['thumbnails per row'] = 5

        if 'generation counter' in self.settings:
            answer = messagebox.askquestion("Continue last session?",
                                            f"Your last session ended at Generation {self.settings['generation counter']}. Do you want to continue that session?")
            if answer == "yes":
                self.generator.gencounter = self.settings['generation counter']
                self.continue_last_session()
                return
            else:
                del self.settings['generation counter']

        self.update_initialize_population_button()

    def use_recursive_directory_search(self, choice):
        """ Called by the use recursive directory button in the app. Depending on the choice, sinks the GUI button
            pressed and raises the other and keeps track of the choice in settings. """
        self.settings['recursive directory search'] = choice
        if choice:
            self.recursivedirectorysearch_yesbutton.configure(relief=tk.SUNKEN)
            self.recursivedirectorysearch_nobutton.configure(relief=tk.RAISED)
        else:
            self.recursivedirectorysearch_yesbutton.configure(relief=tk.RAISED)
            self.recursivedirectorysearch_nobutton.configure(relief=tk.SUNKEN)
        self.recursivedirectorysearch_yesbutton.update()
        self.recursivedirectorysearch_nobutton.update()
        self.generator.clear_data_with_all_appearances()
        self.generator.fill_data_with_all_appearances()
        self.update_found_labels()

    def press_childtemplate_button(self, gender):
        """ Sinks the GUI button for the gender chosen/pressed (female, male, futa) and raises the other buttons. """
        all_genders = ['Female', 'Male', 'Futa']
        remaining_genders = [g for g in all_genders if g != gender]
        if gender in all_genders:
            self.childtemplatebutton[gender].configure(relief=tk.SUNKEN)
        for remaining in remaining_genders:
            self.childtemplatebutton[remaining].configure(relief=tk.RAISED)

    def create_template_labeltext(self, filename):
        """ Returns a formatted label text for a given Appearance file with
            PATH_TO/NAME_OF_APPEARANCE.vap as format """
        template_gender = ecc_logic.get_appearance_gender(ecc_logic.load_appearance(filename))
        # labeltxt = os.path.basename(filename)[7:-4] + " (" + template_gender + " Template)"
        labeltxt = os.path.basename(filename)[7:-4]
        self.childtemplate['gender'] = template_gender
        return labeltxt

    def track_threshold_change(self, var, index, mode):
        """ Keeps track if the user changes the morph threshold value in the GUI.
            If so, validity of the entry is checked. GUI is also updated depending
            on validity, using update_XYZ calls """
        string = self.threshold_entry.get()
        try:
            value = float(string)
            if 0.0 <= value < 1.0:
                self.settings['morph threshold'] = value
                self.update_found_labels()
                self.update_initialize_population_button()
            else:
                if 'morph threshold' in self.settings:
                    del self.settings['morph threshold']
                self.update_found_labels()
                self.update_initialize_population_button()
                return
        except ValueError:
            if 'morph threshold' in self.settings:
                del self.settings['morph threshold']
            self.update_found_labels()
            self.update_initialize_population_button()
            return

        for i in range(1, POP_SIZE + 1):
            self.update_morph_info(i)

    def track_minmorph_change(self, var, index, mode):
        """ Keeps track if the user changes the min morph value in the GUI.
            If so, validity of the entry is checked. GUI is also updated depending
            on validity, using update_XYZ calls """
        string = self.minmorph_entry.get()
        try:
            value = int(string)
            self.settings['min morph threshold'] = value

            # also update the morph info on Chosen Files
            for i in range(1, POP_SIZE + 1):
                self.update_morph_info(i)
            self.update_found_labels()
            self.update_initialize_population_button()

        except ValueError:
            if 'min morph threshold' in self.settings:
                del self.settings['min morph threshold']
            self.update_found_labels()
            self.update_initialize_population_button()
            return

    def track_maxkeptelites_change(self, var, index, mode):
        """ Keeps track if the user changes the 'max kept elites' value in the GUI.
            If an invalid value is chosen, then we use the default value.
            """
        string = self.maxkeptelites_entry.get()
        try:
            value = int(string)

            if 0 <= value <= POP_SIZE:
                self.settings['max kept elites'] = value
            else:
                self.settings['max kept elites'] = DEFAULT_MAX_KEPT_ELITES

        except ValueError:
            self.settings['max kept elites'] = DEFAULT_MAX_KEPT_ELITES
            return

    def update_found_labels(self):
        """ Depending on the choice for the source files, updates the GUI """
        if 'source files' in self.settings:
            if self.settings['source files'] == CHOOSE_ALL_FAVORITES_TEXT:
                self.update_favorites_found_label()
            elif self.settings['source files'] == CHOOSE_ALL_TEXT:
                self.update_all_appearances_found_label()

    def update_all_appearances_found_label(self):
        """ Counts the amount of appearance available in the default VAM directory and updates the GUI """
        filenames = self.get_all_appearance_filenames()
        txt = str(len(filenames)) + " appearances found"
        self.favoritesinfo.configure(text=txt)
        self.update_initialize_population_button()
        self.favoriteslabel.configure(text="Step 5: All Appearances Chosen")

    def update_favorites_found_label(self):
        """ Counts the amount of favorited appearances available in the default VAM directory and updates the GUI """
        #filenames = self.get_favorited_appearance_files()
        filenames = self.get_fav_appearance_filenames()
        txt = str(len(filenames)) + " favorite appearances found"
        self.favoritesinfo.configure(text=txt)
        self.favoriteslabel.configure(text="Step 5: All Favorited Appearances Chosen")
        self.update_initialize_population_button()

    def choose_all_appearances(self):
        """ Called when the choose all appearances button is pressed. Sinks the corresponding GUI button and raises
            the other options. Updates GUI. Saves choice in settings. """
        self.parentselectionframe.grid_remove()
        self.favoritesframe.grid()
        self.allappearancesbutton.configure(relief=tk.SUNKEN)
        self.allfavoritesbutton.configure(relief=tk.RAISED)
        self.choosefilesbutton.configure(relief=tk.RAISED)
        self.settings['source files'] = CHOOSE_ALL_TEXT
        self.update_found_labels()

    def choose_all_favorites(self):
        """ Called when the choose all favorite appearances button is pressed. Sinks the corresponding GUI button and
            raises the other options. Updates GUI. Saves choice in settings. """
        self.parentselectionframe.grid_remove()
        self.favoritesframe.grid()
        self.allappearancesbutton.configure(relief=tk.RAISED)
        self.allfavoritesbutton.configure(relief=tk.SUNKEN)
        self.choosefilesbutton.configure(relief=tk.RAISED)
        self.settings['source files'] = CHOOSE_ALL_FAVORITES_TEXT
        self.update_found_labels()

    def choose_files(self):
        """ Called when the choose files button is pressed. Sinks the corresponding GUI button and raises
            the other options. Updates GUI. Saves choice in settings. """
        self.parentselectionframe.grid()
        self.favoritesframe.grid_remove()
        self.allappearancesbutton.configure(relief=tk.RAISED)
        self.allfavoritesbutton.configure(relief=tk.RAISED)
        self.choosefilesbutton.configure(relief=tk.SUNKEN)
        self.settings['source files'] = CHOOSE_FILES_TEXT
        self.update_initialize_population_button()

    def choose_gaussian_samples(self):
        """ Called when the Gaussian Samples button is pressed. Raises the random crossover button. Saves choice in
            settings. """
        self.gaussianbutton.configure(relief=tk.SUNKEN)
        self.randomcrossoverbutton.configure(relief=tk.RAISED)
        self.settings['method'] = "Gaussian Samples"
        self.update_initialize_population_button()

    def choose_random_crossover(self):
        """ Called when the random crossover button is pressed. Raises the Gaussian Samples  button. Saves choice in
            settings. """
        self.gaussianbutton.configure(relief=tk.RAISED)
        self.randomcrossoverbutton.configure(relief=tk.SUNKEN)
        self.settings['method'] = "Random Crossover"
        self.update_initialize_population_button()

    def select_file(self, number):
        """ Called when Choose Files is chosen and one of the 20 parent buttons is pressed. Number is the parent number.
            Will immediately return (do nothing) if there is no child template available. If child is available, will
            show a file selection window filtered for matching genders. Updates the GUI with choices and saves to
            settings. """
        if 'gender' in self.childtemplate:
            match = ecc_logic.matching_genders(self.childtemplate['gender'])
        else:
            return

        filename = self.file_selection_with_thumbnails(match, "Please select a parent Appearance")

        if filename == "":  # user did not select files
            self.remove_parentfile_from_GUI(number)
            return

        # user did select a file, which we are now parsing
        self.settings['file ' + str(number)] = filename
        self.update_GUI_file(number, filename)

        # stop hiding the apply changes button if we have at least two appearance files available
        self.update_initialize_population_button()
        self.update_morph_info(number)

    def remove_parentfile_from_GUI(self, number):
        """ Removes all internal information for a specific parent file for the chosen parent number. Called when
            loading an appearance file for that parent number is cancelled or invalid """
        keylist = ['shortfilename', 'appearance', 'filename']
        for key in keylist:
            if key in self.chromosome[str(number)]:
                del self.chromosome[str(number)][key]
        if 'file ' + str(number) in self.settings:
            del self.settings['file ' + str(number)]
        self.chromosome[str(number)]['filenamedisplay'].configure(text=NO_FILE_SELECTED_TEXT)
        self.chromosome[str(number)]['can load'] = False
        self.update_morph_info(number)
        self.update_initialize_population_button()

    def select_vamdir(self):
        """ Shows filedialog to find the location of the VAM.exe. Choice is validated, GUI updated and settings
            saved. """
        # try to open the file dialog in the last known location
        vamdir = ""
        if 'VAM base dir' in self.settings:
            if len(self.settings['VAM base dir']) > 0:
                vamdir = self.settings['VAM base dir']

        folder_path = tk.filedialog.askdirectory(initialdir=vamdir,
                                                 title="Please select the folder which has the VAM.exe file")
        if os.path.exists(os.path.join(folder_path, "vam.exe")):
            self.settings['VAM base dir'] = str(pathlib.Path(folder_path))
            self.vamdirlabel.configure(
                text=ecc_utility.strip_dir_string_to_max_length(self.settings['VAM base dir'], MAX_VAMDIR_STRING_LENGTH))
            self.vamdirbutton.configure(relief=tk.SUNKEN)
            self.track_minmorph_change("", "", "")  # update
            self.generator.clear_data_with_all_appearances()
            self.generator.fill_data_with_all_appearances()
        else:
            self.settings['VAM base dir'] = ""
            self.vamdirlabel.configure(text=NO_FILE_SELECTED_TEXT)
            self.vamdirbutton.configure(relief=tk.RAISED)
            self.generator.clear_data_with_all_appearances()
        self.update_initialize_population_button()
        self.update_found_labels()

    def select_appearancedir(self):
        """ Shows filedialog to select the appearance directory, GUI updated and settings saved. """
        # try to open the file dialog in the last known location
        appearancedir = ""
        if 'appearance dir' in self.settings:
            if len(self.settings['appearance dir']) > 0:
                appearancedir = self.settings['appearance dir']

        folder_path = tk.filedialog.askdirectory(initialdir=appearancedir,
                                                 title="Please select the appearance folder you would like to use.")
        if folder_path == "":
            self.settings['appearance dir'] = ""
            self.appearancedirlabel.configure(text=NO_FILE_SELECTED_TEXT)
            self.appearancedirbutton.configure(relief=tk.RAISED)
            self.generator.clear_data_with_all_appearances()
        else:
            self.settings['appearance dir'] = str(pathlib.Path(folder_path))
            self.appearancedirlabel.configure(
                text=ecc_utility.strip_dir_string_to_max_length(self.settings['appearance dir'],
                                                                MAX_APPEARANCEDIR_STRING_LENGTH))
            self.appearancedirbutton.configure(relief=tk.SUNKEN)
            self.track_minmorph_change("", "", "")  # update
            self.generator.clear_data_with_all_appearances()
            self.generator.fill_data_with_all_appearances()
        self.update_initialize_population_button()
        self.update_found_labels()

    def get_vam_default_appearance_path(self):
        """ Returns the path to the default Appearance directory based on the VAM base path, or returns '' if no base path
            is found in settings. """
        path = ""
        if "VAM base dir" in self.settings:
            if len(self.settings['VAM base dir']) > 0:
                appearance_path = "Custom/Atom/Person/Appearance"
                path = os.path.join(self.settings['VAM base dir'], appearance_path)
        return path

    def update_initialize_population_button(self):
        """ Updates the Initialize Population button, by checking if all necessary files and settings are correct. If
            not, shows in the button what items are missing and makes the button do nothing. If criteria are met, button
            color is changed to green and button functionality is restored. """
        isok, missing = self.can_generate_new_population()
        if isok:
            self.generatechild.configure(relief="raised",
                                         bg="lightgreen", font=(DEFAULT_FONT, 12, "bold"), text="Initialize Population",
                                         width=52, height=6,
                                         state='normal',
                                         command=lambda: self.generate_next_population(self.settings['method']))
        else:
            txt = ("Cannot Initialize Population:\n" + missing).rstrip()
            self.generatechild.configure(relief=tk.RAISED, bg="#D0D0D0",
                                         font=(DEFAULT_FONT, 12, "bold"),
                                         width=52, height=6,
                                         activebackground="#D0D0D0",
                                         text=txt,
                                         state='disabled',
                                         command=None)

    def can_generate_new_population(self):
        """ Function which checks all necessary files and settings for generating a new population. Returns a
            False and string 'missing' with all missing features, or True if all criteria are met. """
        missing = ""

        if 'VAM base dir' in self.settings:
            if len(self.settings['VAM base dir']) > 0:
                pass
            else:
                missing += "· Please select the VAM base folder\n"
        else:
            missing += "· Please select the VAM base folder\n"

        if 'appearance dir' in self.settings:
            if len(self.settings['appearance dir']) > 0:
                pass
            else:
                missing += "· Please select an Appearance folder\n"
        else:
            missing += "· Please select an Appearance folder\n"

        if 'child template' not in self.settings:
            missing += "· Please select a child template appearance\n"

        if 'source files' in self.settings:
            if self.settings['source files'] == CHOOSE_ALL_FAVORITES_TEXT:
                source_files = self.get_fav_appearance_filenames()
            elif self.settings['source files'] == CHOOSE_ALL_TEXT:
                source_files = self.get_all_appearance_filenames()
            elif self.settings['source files'] == CHOOSE_FILES_TEXT:
                source_files = [self.chromosome[str(i)]['filename'] for i in range(1, POP_SIZE + 1) if
                                self.chromosome[str(i)]['can load']]
            else:
                source_files = []
            if len(source_files) >= 2:
                pass
            else:
                missing += "· Please have at least 2 Parent files\n"
        else:
            missing += "· Please have at least 2 Parent files\n"

        if 'morph threshold' not in self.settings:
            missing += "· Please enter correct value for option A\n"

        if 'min morph threshold' not in self.settings:
            missing += "· Please enter correct value for option B\n"

        if len(missing) == 0:
            return True, ""
        else:
            return False, missing

    def update_GUI_file(self, number, filename):
        """ Updates the Parent file with 'number' with all information available through the 'filename' """
        if filename not in self.generator.appearances:
            return
        chromosome = self.chromosome[str(number)]
        chromosome['filename'] = filename
        chromosome['shortfilename'] = os.path.basename(filename)[7:-4]  # remove Preset_ and .vap
        chromosome['filenamedisplay'].configure(text=chromosome['shortfilename'])
        chromosome['appearance'] = self.generator.appearances[filename]
        chromosome['can load'] = True

    def select_template_file(self, genderlist, title):
        """ Called by the Female, Male and Futa load template file buttons. Opens a file selection dialogue which
            specifically filters for the gender of the button clicked. The genderlist only has the chosen gender
            as an item. Updates GUI and settings after (un)succesful template selection. """
        filename = self.file_selection_with_thumbnails(genderlist, title, filteronmorphcount=False)

        if filename == "":  # user did not select files
            self.childtemplate['label'].configure(text=NO_FILE_SELECTED_TEXT)
            self.press_childtemplate_button(None)
            if 'gender' in self.childtemplate:
                del self.childtemplate['gender']
            if 'child template' in self.settings:
                del self.settings['child template']
            self.update_initialize_population_button()
            self.file_selection_popup.destroy()
            self.update_found_labels()
            return
        self.childtemplate['label'].configure(text=self.create_template_labeltext(filename))
        self.childtemplate['gender'] = self.generator.gender[filename]
        self.press_childtemplate_button(self.childtemplate['gender'])
        self.settings['child template'] = filename
        for i in range(1, POP_SIZE + 1):
            self.update_morph_info(i)
        self.update_initialize_population_button()
        self.update_found_labels()

    def press_change_template_file(self, title):
        """ Called by the change template button in the rating windows. Opens a file selection dialogue which
            specifically filters for the gender of the template which is currently being used. If user does not
            select a valid new template file, the old template file is used. """
        filename = self.file_selection_with_thumbnails(ecc_logic.matching_genders(self.childtemplate['gender']), title,
                                                       filteronmorphcount=False)
        if filename == "":  # user did not select files
            return
        self.change_template_file(filename)

    def change_template_file(self, filename):
        """ Called by either the GUI or as a VAM command. Checks if the gender of the chosen file matches the
            current template gender. Updates the GUI. """
        self.broadcast_message_to_VAM_rating_blocker("Updating...\nPlease Wait")
        # we need to check if the chosen gender matches the gender of the current population (for example:
        # we can't suddenly switch from a male population to a female population or vice versa).
        gender = ecc_logic.get_appearance_gender(ecc_logic.load_appearance(filename))
        if not ecc_logic.can_match_genders(gender, self.childtemplate['gender']):
            matches = ecc_logic.matching_genders(self.childtemplate['gender'])
            if len(matches) > 1:  # Female and Futa
                selectmsg = "Please select a Female or Futa as template."
            else:
                selectmsg = "Please select a Male as template."
            self.broadcast_message_to_VAM_rating_blocker("Failure: Gender does not match population.\n\n" + selectmsg)
            return
        self.changetemplatebuttonlabel.configure(text=os.path.basename(filename)[7:-4])
        self.settings['child template'] = filename
        self.update_population_with_new_template()
        self.broadcast_message_to_VAM_rating_blocker("")

    def switch_layout_to_overview(self):
        """ Called when the user has pressed 'Connect to App' in VAM (resulting in a 'Connect to App' command to this
            app. This method removes the 'please start the vam app' dialogue, and replaces it with an overview window
            showing the user the last five commands received, from the VAM companion save. """
        self.broadcast_generation_number_to_VAM(self.generator.gencounter)
        print("VAM is ready, let's go.")
        print("Switching view")
        for widget in self.master.winfo_children():
            widget.grid_forget()
        self.overviewframe = tk.Frame(self.master, bg=BG_COLOR)
        self.overviewframe.grid(row=0, column=0, padx=10, pady=0, sticky="nsew")
        self.warninglabel = tk.Label(self.overviewframe, text="Important: do NOT close this window!",
                                     font=(DEFAULT_FONT, 14, "bold"), bg=BG_COLOR, fg="red")
        self.warninglabel.grid(row=0, columnspan=2, column=0, padx=(10, 10), pady=(10, 0), sticky="w")
        self.overviewlabel = tk.Label(self.overviewframe, text="Overview:", font=(DEFAULT_FONT, 14, "bold"),
                                      bg=BG_COLOR, fg=FG_COLOR)
        self.overviewlabel.grid(row=1, columnspan=2, column=0, padx=(10, 0), pady=(10, 0), sticky="w")
        self.generationlabel = tk.Label(self.overviewframe, text="Generation:", bg=BG_COLOR, fg=FG_COLOR)
        self.generationlabel.grid(row=2, column=0, padx=(10, 0), pady=(0, 0), sticky="w")
        self.generationnumberlabel = tk.Label(self.overviewframe, text=self.generator.gencounter, font=FILENAME_FONT, bg=BG_COLOR,
                                              fg=FG_COLOR, anchor="w", justify=tk.LEFT)
        self.generationnumberlabel.grid(row=2, column=1, padx=0, pady=(0, 0), sticky="w")
        self.templatelabel = tk.Label(self.overviewframe, text="Current template:", bg=BG_COLOR, fg=FG_COLOR)
        self.templatelabel.grid(row=3, column=0, padx=(10, 0), pady=(0, 0), sticky="w")
        self.templatefilelabel = tk.Label(self.overviewframe, text="", font=FILENAME_FONT, bg=BG_COLOR, fg=FG_COLOR,
                                          anchor="w", justify=tk.LEFT)
        self.templatefilelabel.grid(row=3, column=1, padx=0, pady=(0, 0), sticky="w")
        self.templatefilelabel.configure(text=self.create_template_labeltext(self.settings['child template']))
        self.lastcommandsframe = tk.Frame(self.master, bg=BG_COLOR)
        self.lastcommandsframe.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.lastcommandslabel = tk.Label(self.lastcommandsframe, text="Last five commands:",
                                          font=(DEFAULT_FONT, 14, "bold"), bg=BG_COLOR, fg=FG_COLOR)
        self.lastcommandslabel.grid(row=0, column=0, padx=10, pady=0, sticky="w")
        self.commandslabel = tk.Label(self.lastcommandsframe, text="...", font=FILENAME_FONT, bg=BG_COLOR, fg=FG_COLOR,
                                      justify=tk.LEFT, anchor="w")
        self.commandslabel.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="w")
        print("Resetting ratings")
        self.reset_ratings()
        print("Sending generation number")
        self.broadcast_generation_number_to_VAM(self.generator.gencounter)
        self.broadcast_message_to_VAM_rating_blocker("")

    def update_overview_window(self):
        """ Updates the overview window with generation, template and last five commands information """
        self.generationnumberlabel.config(text=self.generator.gencounter)
        self.templatefilelabel.config(text=self.create_template_labeltext(self.settings['child template']))
        self.commandslabel.config(text=self.lastgivecommands_to_string(self.generator.lastfivecommands))

    def lastgivecommands_to_string(self, list_of_commands):
        """ Converts a list of commands (5) (where each command is dictionary with 'time' and 'command' as keys
            to a string with \n for line separation """
        string = ""
        for command_dict in list_of_commands:
            line = command_dict['time'] + ": " + command_dict['command'] + "\n"
            string = string + line
        string = string[:-1]  # remove the extra \n at the end
        return string

    def variate_population_with_templates(self):
        """ Replaces all the chromosomes in the population with a randomly chosen templates from all the available
            templates """
        print('variate_population_with_templates')
        self.broadcast_message_to_VAM_rating_blocker("Updating...\nPlease Wait")

        filenames = list(self.generator.appearances.keys())
        random.shuffle(filenames)
        filename_generator = ecc_utility.generate_list_element(filenames)    

        appearance_templates = list()
        for filename in filename_generator:
            if len(appearance_templates) >= POP_SIZE:
                break
            appearance = ecc_logic.load_appearance(filename)
            gender = ecc_logic.get_appearance_gender(appearance)
            if gender == self.childtemplate['gender']:
                appearance_templates.append(appearance)

        for i in range(1, POP_SIZE + 1):
            morphlist = ecc_logic.get_morphlist_from_appearance(ecc_logic.load_appearance(self.chromosome[str(i)]['filename']))
            updated_appearance = ecc_logic.save_morph_to_appearance(morphlist, appearance_templates[i - 1])
            nude_appearance = ecc_logic.remove_clothing_from_appearance(updated_appearance)
            ecc_logic.save_appearance(nude_appearance, self.chromosome[str(i)]['filename'])
        
        self.broadcast_message_to_VAM_rating_blocker("")

    def update_population_with_new_template(self):
        """ Replaces the template of all the current Children with the new one but keeps the morphs values the same. """
        template_appearance = ecc_logic.load_appearance(self.settings['child template'])
        for i in range(1, POP_SIZE + 1):
            morphlist = ecc_logic.get_morphlist_from_appearance(ecc_logic.load_appearance(self.chromosome[str(i)]['filename']))
            updated_appearance = ecc_logic.save_morph_to_appearance(morphlist, template_appearance)
            ecc_logic.save_appearance(updated_appearance, self.chromosome[str(i)]['filename'])

    def file_selection_with_thumbnails(self, genderlist, title, filteronmorphcount=True):
        """ Called by select_template_file and select_file. Creates a custom file selection popup window, with icons
            from all the files available. Filters on the genders in the genderlist. When called, pauses the main
            AppWindow window until a choice is made, or the file selection window is closed. Clicking on an image button
            calls end_file_selection_with_thumbnails(). """
        self._file_selection = ""

        self.thumbnails_per_row = self.settings['thumbnails per row']

        filenames = list(self.generator.appearances.keys())
        if filteronmorphcount:
            filenames = self.filter_filenamelist_on_morph_threshold_and_min_morphs(filenames)
        filenames = self.filter_filenamelist_on_genders(filenames, genderlist)

        # create popup window
        self.file_selection_popup = tk.Toplevel()
        if 'file selection geometry' in self.settings:
            geometry = self.settings['file selection geometry']
        else:
            geometry = str(int(190 * self.thumbnails_per_row + 23)) + "x1000"
        self.file_selection_popup.geometry(geometry)
        self.file_selection_popup.title(title)
        self.file_selection_popup.configure(bg=BG_COLOR)
        self.file_selection_popup.iconbitmap(os.path.join(DATA_PATH, ICON_FILENAME))
        self.file_selection_popup.grab_set()

        #
        # Start of scrollbar hack in Tkinter
        #
        canvasholdingframe = tk.Frame(self.file_selection_popup, bg=BG_COLOR)
        canvasholdingframe.pack(fill=tk.BOTH, expand=1)
        self.my_canvas = tk.Canvas(canvasholdingframe, bg=BG_COLOR)
        self.my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        my_scrollbar = ttk.Scrollbar(canvasholdingframe, orient=tk.VERTICAL, command=self.my_canvas.yview)
        my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.my_canvas.configure(yscrollcommand=my_scrollbar.set)
        self.my_canvas.bind('<Configure>', lambda e: self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all")))
        self.my_canvas.bind_all('<MouseWheel>', lambda e: self.my_canvas.yview_scroll(int(-1 * e.delta / 120), "units"))
        self.my_canvas.bind_all('<Escape>', lambda e: self.file_selection_popup.destroy())

        # we basically have a canvas for the scrollbar, and put this frame in it
        self.appearancesframe = tk.Frame(self.my_canvas, bg=BG_COLOR)
        self.my_canvas.create_window((0, 0), window=self.appearancesframe, anchor="nw")
        #
        # End of scrollbar hack in Tkinter
        #

        self.show_all_appearance_buttons(self.appearancesframe, filenames, self.thumbnails_per_row)

        #
        # Bottomframe of the popup
        #
        bottomframe = tk.Frame(self.file_selection_popup, bg=BG_COLOR)
        bottomframe.pack(fill="both")
        button = tk.Button(bottomframe, text="➖", bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR,
                           activebackground=BUTTON_ACTIVE_COLOR, command=lambda: self.change_popup_width(-1, filenames))
        button.pack(side=tk.LEFT)
        button = tk.Button(bottomframe, text="➕", bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR,
                           activebackground=BUTTON_ACTIVE_COLOR, command=lambda: self.change_popup_width(+1, filenames))
        button.pack(side=tk.LEFT)
        self.filefilter = tk.Entry(bottomframe, fg=BUTTON_FG_COLOR, bg=BUTTON_BG_COLOR, width=20)
        self.filefilter.pack(side=tk.LEFT)
        self.filefilter.bind('<Return>', lambda event, arg=filenames: self.apply_file_filter(arg))
        button = tk.Button(bottomframe, text="Filter", bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR,
                           activebackground=BUTTON_ACTIVE_COLOR, command=lambda: self.apply_file_filter(filenames))
        button.pack(side=tk.LEFT)
        button = tk.Button(bottomframe, text="Cancel", bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR,
                           activebackground=BUTTON_ACTIVE_COLOR, command=self.end_file_selection_with_thumbnails)
        button.pack(side=tk.LEFT)
        self.file_selection_popup.wait_window()
        self.my_canvas.unbind_all('<MouseWheel>')
        self.my_canvas.unbind_all('<Escape>')
        return self._file_selection

    def filter_filenamelist_on_morph_threshold_and_min_morphs(self, filenames):
        """ For a given list of filenames returns a list of filenames which meet the morph and min morph thresholds.
            Returns an empty list if neither of these settings are available. """
        if 'morph threshold' not in self.settings:
            return []
        elif 'min morph threshold' not in self.settings:
            return []

        filtered = []
        for f in filenames:
            appearance = self.generator.appearances[f]
            morphlist = ecc_logic.get_morphlist_from_appearance(appearance)
            morphlist = ecc_logic.filter_morphs_below_threshold(morphlist, self.settings['morph threshold'])
            if len(morphlist) > self.settings['min morph threshold']:
                filtered.append(f)
        return filtered

    def filter_filenamelist_on_genders(self, filenames, genderlist):
        """ For a give list of filenames, filters on gender. """
        filtered = []
        for f in filenames:
            gender = self.generator.gender[f]
            if gender:
                if gender in genderlist:
                    filtered.append(f)
        return filtered

    def end_file_selection_with_thumbnails(self, filename="", event=None):
        """ Saves settings and returns the filename through self._file_selection """
        self.settings['file selection geometry'] = self.file_selection_popup.winfo_geometry()
        self.settings['thumbnails per row'] = self.thumbnails_per_row
        self._file_selection = str(pathlib.Path(filename))  # use uniform filename formatting
        self.file_selection_popup.destroy()

    def remove_all_appearance_widgets(self):
        """ Used by file_selection_with_thumbnails function to clear the popup window if the amount of thumbnails per
            row is changed. After clearing, builds the images up again with the new thumbnails per row settings. """
        for widget in self.all_appearance_widgets:
            widget.destroy()

    def change_popup_width(self, value, filenames):
        """ Changes the amount of images shown on each row. Value is either +1 or -1 depending on which function calls
            this. Filenames is the list of filenames to be displayed in the file selection window. """
        self.remove_all_appearance_widgets()
        self.thumbnails_per_row += value
        height = self.file_selection_popup.winfo_height()
        geometry = str(int(190 * self.thumbnails_per_row + 23)) + "x" + str(height)
        self.file_selection_popup.geometry(geometry)
        self.show_all_appearance_buttons(self.appearancesframe, filenames, self.thumbnails_per_row)

    def show_all_appearance_buttons(self, window, filenames, thumbnails_per_row):
        """ Show all appearance files as image buttons, in the given window. """
        self.all_appearance_widgets = []
        max_vertical = int(len(filenames) / thumbnails_per_row) + 1
        fileindex = 0
        self.appearancebutton = {}
        self.appearancelabel = {}
        for j in range(max_vertical):
            for i in range(thumbnails_per_row):
                if fileindex < len(filenames):
                    button, label = self.make_appearance_button(window, filenames[fileindex], j, i, fileindex)
                    self.all_appearance_widgets.extend([button, label])
                    fileindex += 1

    def apply_file_filter(self, filenames):
        """ Applies file filter to file selection window. """
        self.my_canvas.yview_moveto('0.0')  # scroll to top
        filtertxt = self.filefilter.get()
        globfilter = "*preset_*" + filtertxt + "*.vap"
        filtered = [file for file in filenames if fnmatch(file.lower(), globfilter)]
        self.remove_all_appearance_widgets()
        self.show_all_appearance_buttons(self.appearancesframe, filtered, self.thumbnails_per_row)

    def make_appearance_button(self, window, filename, row, column, fileindex):
        """ Make individual appearance button in file selection window. Called by show_all_appearance_buttons. """
        thumbnail = self.generator.thumbnails[filename]
        name = os.path.basename(filename)[7:-4]  # remove Preset_ and .vap

        self.appearancebutton[str(fileindex)] = tk.Button(window, relief=tk.FLAT, bg=BG_COLOR, command=lambda
                                                filename=filename: self.end_file_selection_with_thumbnails(filename))
        self.appearancebutton[str(fileindex)].grid(row=row * 2, column=column, padx=0, pady=0)
        self.appearancebutton[str(fileindex)].configure(image=thumbnail)
        self.appearancebutton[str(fileindex)].bind("<Enter>",
                                                   lambda e, index=fileindex: self.on_enter_appearancebutton(index,
                                                                                                             event=e))
        self.appearancebutton[str(fileindex)].bind("<Leave>",
                                                   lambda e, index=fileindex: self.on_leave_appearancebutton(index,
                                                                                                             event=e))
        self.appearancebutton[str(fileindex)].image = thumbnail
        self.appearancelabel[str(fileindex)] = tk.Label(window, text=name, font=FILENAME_FONT, width=26, anchor=tk.W,
                                                        bg=BG_COLOR, fg=FG_COLOR, padx=0, pady=0)
        self.appearancelabel[str(fileindex)].grid(row=row * 2 + 1, column=column, sticky=tk.W)
        return self.appearancebutton[str(fileindex)], self.appearancelabel[str(fileindex)]

    def on_enter_appearancebutton(self, index, event=None):
        """ Show hover effect when entering mouse over an image file. """
        self.appearancebutton[str(index)]['background'] = HOVER_COLOR
        self.appearancelabel[str(index)]['background'] = BG_COLOR
        self.appearancelabel[str(index)]['foreground'] = HOVER_COLOR

    def on_leave_appearancebutton(self, index, event=None):
        """ Show hover effect when exiting mouse over an image file. """
        self.appearancebutton[str(index)]['background'] = BG_COLOR
        self.appearancelabel[str(index)]['background'] = BG_COLOR
        self.appearancelabel[str(index)]['foreground'] = FG_COLOR

    def update_morph_info(self, number):
        """ Updates morph info in the GUI for Parent file 'number'. """
        threshold = self.settings['morph threshold']
        if threshold == "":
            threshold = 0
        else:
            threshold = float(threshold)

        if 'gender' in self.childtemplate:
            template_gender = self.childtemplate['gender']
        else:
            template_gender = ""

        if 'filename' in self.chromosome[str(number)]:
            gender = ecc_logic.get_appearance_gender(ecc_logic.load_appearance(self.chromosome[str(number)]['filename']))
            if not ecc_logic.can_match_genders(gender, template_gender):
                self.hide_parentfile_from_view(
                    number)  # hide, but don't delete, in case template later has matching gender
                return

            morphlist_tmp = copy.deepcopy(ecc_logic.get_morphlist_from_appearance(self.chromosome[str(number)]['appearance']))
            morphlist_tmp = ecc_logic.filter_morphs_below_threshold(morphlist_tmp, threshold)
            nmorphs = str(len(morphlist_tmp))
            if int(nmorphs) < self.settings['min morph threshold']:
                if self.generator.gencounter == 0:  # only do this in the initialization selection step
                    self.hide_parentfile_from_view(number)
                    return
            else:
                if self.generator.gencounter == 0:  # only do this in the initialization selection step
                    self.chromosome[str(number)]['filenamedisplay'].configure(
                        text=self.chromosome[str(number)]['shortfilename'])
                    self.chromosome[str(number)]['can load'] = True
        else:
            nmorphs = "N/A"
        if self.generator.gencounter == 0:  # after the app is initialized, the morph information is not being shown anymore
            self.chromosome[str(number)]['nmorphdisplay'].configure(text=str(nmorphs))

    def hide_parentfile_from_view(self, number):
        """ Replaces the filelable of the parent file #number with '...'  and 'N/A' but keeps the file info
            dictionary """
        chromosome = self.chromosome[str(number)]
        chromosome['filenamedisplay'].configure(text=NO_FILE_SELECTED_TEXT)
        chromosome['nmorphdisplay'].configure(text="N/A")
        chromosome['can load'] = False

    def restart_population(self, method):
        """ Reinitializes the population. Can be called whenver the app is in the rating mode.
            Generation counter is reset to 1. """
        print(f"Restarting, with {method}")
        self.broadcast_message_to_VAM_rating_blocker("Updating...\nPlease Wait")

        # If the user used CHOOSE_FILES_TEXT as the source, we have to reload them into the chromosomes
        # since the chromosomes now contain the Evolutionary Children files at this stage. Only the
        # files which were saved to settings are loaded into the chromosomes. There is no need to
        # delete the other chromosomes (which contain the Evolutionary Child filenames), because
        # they all have a False flag for self.chromosome[str(i)]['can load'] which is used
        # later on in Gaussian and Crossover generation to skip loading them.
        if self.settings['source files'] == CHOOSE_FILES_TEXT:
            for i in range(1, POP_SIZE + 1):
                if 'file ' + str(i) in self.settings:
                    if len(self.settings['file ' + str(i)]) > 0:
                        self.chromosome[str(i)]['filename'] = self.settings['file ' + str(i)]

        if method == "Gaussian Samples":
            self.gaussian_initialize_population(source_files=self.settings['source files'])
        elif method == "Random Crossover":
            self.crossover_initialize_population(self.settings['source files'])
        self.generator.gencounter = 1
        self.titlelabel.configure(text="Generation " + str(self.generator.gencounter))
        self.reset_ratings()
        self.broadcast_message_to_VAM_rating_blocker("")

    def generate_next_population(self, method):
        """ Generates the next population. Switches GUI layout to the Ratings layout when called for the first time
            (self.generator.gencounter == 0). Updates the population in the GUI through self.update_population(). """
        print(method)
        if self.generator.gencounter == 0:
            ecc_utility.save_settings(self.settings)  # in case of a bug we want to have the settings saved before we start the algorithm
            if method == "Gaussian Samples":
                self.gaussian_initialize_population(source_files=self.settings['source files'])
            elif method == "Random Crossover":
                self.crossover_initialize_population(self.settings['source files'])
            self.change_parent_to_generation_display()
            self.switch_layout_to_rating()
            self.reset_ratings()
            self.change_GUI_to_show_user_to_start_VAM()
            self.scan_vam_for_command_updates("Initialize")
            return

        self.broadcast_message_to_VAM_rating_blocker("Updating...\nPlease Wait")

        # Start the new population with the elites from the last generation (depending on settings)
        elites = self.get_elites_from_population()

        # Save elite appearances over child template (we do this, because the user might have changed the template file)
        elite_morph_lists = [ecc_logic.get_morphlist_from_appearance(appearance) for appearance in elites]
        template_appearance = ecc_logic.load_appearance(self.settings['child template'])
        new_population = [ecc_logic.save_morph_to_appearance(elite_morph_list, template_appearance) for elite_morph_list in
                          elite_morph_lists]

        for i in range(POP_SIZE - len(new_population)):
            random_parents = self.weighted_random_selection()
            child_appearance = ecc_logic.fuse_characters(random_parents[0]['filename'], random_parents[1]['filename'],
                                               self.settings)
            new_population.append(child_appearance)
        self.save_population(new_population)
        self.update_population(new_population)

        self.generator.gencounter += 1
        self.settings['generation counter'] = self.generator.gencounter
        self.titlelabel.configure(text="Generation " + str(self.generator.gencounter))
        self.reset_ratings()
        self.broadcast_message_to_VAM_rating_blocker("")
        ecc_utility.save_settings(self.settings)

    def change_GUI_to_show_user_to_start_VAM(self):
        """ After initialization this method is called, to remove all the setup widgets and replace them with a window
            asking the user to load the VAM Companion Save. """
        for widget in self.master.winfo_children():
            widget.grid_forget()
        self.messageframe = tk.Frame(self.master, bg=BG_COLOR)
        self.messageframe.grid(row=0, column=1, padx=10, pady=0, sticky="nsew")
        self.messagelabel = tk.Label(self.messageframe, text="App is ready. \nPlease start VAM, load the",
                                     font=(DEFAULT_FONT, 14, ""), bg=BG_COLOR, fg=FG_COLOR)
        self.messagelabel.pack(side=tk.TOP)
        self.messagelabel = tk.Label(self.messageframe, text="VAM Evolutionary Character Creation Companion",
                                     font=(DEFAULT_FONT, 14, "italic"), bg=BG_COLOR, fg=FG_COLOR)
        self.messagelabel.pack(side=tk.TOP)
        self.messagelabel = tk.Label(self.messageframe, text="save, and click on 'Connect to App'",
                                     font=(DEFAULT_FONT, 14, ""), bg=BG_COLOR, fg=FG_COLOR)
        self.messagelabel.pack(side=tk.TOP)
        self.warninglabel = tk.Label(self.messageframe, text="\nImportant: do NOT close this window.\n ",
                                     font=(DEFAULT_FONT, 14, "bold"), bg=BG_COLOR, fg="red")
        self.warninglabel.pack(side=tk.TOP)
        self.lastmessagelabel = tk.Label(self.messageframe,
                                         text="This app needs to stay active to communicate with VAM.",
                                         font=(DEFAULT_FONT, 14, ""), bg=BG_COLOR, fg=FG_COLOR)
        self.lastmessagelabel.pack(side=tk.TOP)

    def continue_last_session(self):
        """ Skip choosing the settings and continue from the last session. This only means switching the layout to
            the rating window and setting the generation counter to the last known value. """
        path = self.get_vam_default_appearance_path()
        save_path = os.path.join(path, SAVED_CHILDREN_PATH)
        for i in range(1, POP_SIZE + 1):
            filename = os.path.join(save_path, "Preset_" + CHILDREN_FILENAME_PREFIX + str(i) + ".vap")
            self.chromosome[str(i)]['filename'] = filename
            self.chromosome[str(i)]['appearance'] = ecc_logic.load_appearance(filename)
        self.change_parent_to_generation_display()
        self.switch_layout_to_rating()
        self.reset_ratings()
        self.generatechild.configure(text="Generate Next Population")
        self.change_GUI_to_show_user_to_start_VAM()
        self.scan_vam_for_command_updates("Initialize")

    def get_VAM_path(self, pathstring):
        """ Returns the full path with VAM_BASE_PATH/pathstring and returns False if there was no VAM base dir. """
        if "VAM base dir" not in self.settings:
            return False
        if len(self.settings['VAM base dir']) == 0:
            return False
        return os.path.join(self.settings['VAM base dir'], pathstring)

    def scan_vam_for_command_updates(self, lastcommand):
        """ Continously check if
            PATH_TO_VAM\\Custom\\Atom\\UIText\\VAM Evolutionary Character Creation\\Preset_VAM2PythonText.vap
            has a new command string. If so, try to execute that command by calling execut_VAM_command() """
        # try to open file
        path = self.get_VAM_path(r'Custom\Atom\UIText\VAM Evolutionary Character Creation\Preset_VAM2PythonText.vap')
        if not path:
            return
        try:
            with open(path, encoding="utf-8") as f:
                linestring = f.read()
                lines = linestring.split('\n')
                # print(f"Length of lines {len(lines)}")
                if len(lines) < 70:  # incomplete file
                    raise IOError(f"Not enough lines ({len(lines)}) in the file ")
                # f.seek(0) # back to start of file
                command_json = json.loads(linestring)
                command = ecc_logic.value_from_id_in_dict_list(command_json['storables'], "Text", "text")
                if lastcommand == "Initialize":  # if we Initialize we have to set lastcommand as the file we just read
                    lastcommand = command
                if command != lastcommand:
                    self.broadcast_last_command_to_VAM(command)
                    self.execute_VAM_command(command)
                    print("We have a new command: {}".format(command))
        except IOError as e:
            print(e)
            self.master.after(25, lambda lastcommand=lastcommand: self.scan_vam_for_command_updates(lastcommand))
        else:
            self.master.after(25, lambda lastcommand=command: self.scan_vam_for_command_updates(lastcommand))

    def execute_VAM_command(self, command):
        """ Tries to parse a command string to execute coming from scan_vam_for_command_updates. These
            command strings are generated by the VAM Evolutionary Character Creation Companion save file,
            and always have either the format:
                "Child 12; Rate 4"
            or
                "Generate Next Population"
            """
        if self.generator.connected_to_VAM:
            # add command to last five commands
            command_dict = {}
            now = datetime.now()
            time_string = now.strftime("%d-%m-%Y %H:%M:%S")
            command_dict['time'] = time_string
            command_dict['command'] = command
            self.generator.lastfivecommands.insert(0, command_dict)
            if len(self.generator.lastfivecommands) > 5:
                self.generator.lastfivecommands.pop()
            self.update_overview_window()

        # parse rate child commands
        commands = command.split(";")
        commands = [x.lstrip().rstrip() for x in commands]
        if "child" in commands[0].lower() and "rate" in commands[1].lower():
            child = commands[0].split(" ")
            child = int(child[1])
            rating = commands[1].split(" ")
            rating = int(rating[1])
            self.press_rating_button(child, rating)
        # the random number in commands[1] for the if statements below are not used in any way by this script, except
        # to make sure that in case the user wants to do the same command twice, the lastcommand != command in
        # scan_vam_for_command_updates() sees the commands as different (due to the random numbers in commands[1])
        elif "use template" in commands[0].lower():
            filename = self.get_VAM_path(commands[1])
            filename = str(pathlib.Path(filename))  # use uniform filename formatting
            self.change_template_file(filename)
        elif "variate population" in commands[0].lower():
            self.variate_population_with_templates()
        elif "connect to app" in commands[0].lower():
            self.generator.connected_to_VAM = True
            self.reset_ratings()
            self.switch_layout_to_overview()
        elif "generate next population" in commands[0].lower():
            self.generate_next_population(self.settings['method'])
            self.broadcast_generation_number_to_VAM(self.generator.gencounter)
        elif "reset" in commands[0].lower():
            # in the case of a reset we immediately send the "Reset" command back to VAM to avoid a
            # "Connection Lost" in VAM, since the initialization of a new generation (with the Gaussian Method)
            # takes more than the 5 second Connection-check-timeout in VAM.
            self.press_restart_button(givewarning=False)
            self.broadcast_generation_number_to_VAM(self.generator.gencounter)

        if self.generator.connected_to_VAM:
            self.update_overview_window()

    def broadcast_generation_number_to_VAM(self, number):
        """ Updates the file
            PATH_TO_VAM\\Custom\\Atom\\UIText\\VAM Evolutionary Character Creation\\Preset_Python2VAMGeneration.vap
            with the generation number, so the Vam Evoluationary Character Creation Companion can display the
            proper generation number. """
        # try to save file
        path = self.get_VAM_path(
            r'Custom\Atom\UIText\VAM Evolutionary Character Creation\Preset_Python2VAMGeneration.vap')
        if not path:
            return False
        self.write_value_to_VAM_file(path, "Text", "text", "Generation " + str(number))

    def broadcast_last_command_to_VAM(self, command):
        """ Updates the file
            PATH_TO_VAM\\Custom\\Atom\\UIText\\VAM Evolutionary Character Creation\\Preset_Python2VAMText.vap
            with the last command, so the Vam Evoluationary Character Creation Companion save can check if the python
            script is still running properly, by comparing the command VAM sent to python, with this broadcast command
            from python back. """
        path = self.get_VAM_path(r'Custom\Atom\UIText\VAM Evolutionary Character Creation\Preset_Python2VAMText.vap')
        if not path:
            return False
        self.write_value_to_VAM_file(path, "Text", "text", command)

    def broadcast_message_to_VAM_rating_blocker(self, text):
        path = self.get_VAM_path(
            r'Custom\Atom\UIButton\VAM Evolutionary Character Creation\Preset_Python2VAMRatingBlocker.vap')
        if not path:
            return False
        self.write_value_to_VAM_file(path, "Text", "text", text)

    def write_value_to_VAM_file(self, path, id_string, needed_key, replacement_string):
        """ Updates the VAM file with path, by loading the storables array inside, and looking for the dictionary with
            ("id", "id_string") as (key, value) pair. Then, within this dictionary, it will overwrite the (key, value)
            pair with ("needed_key", "replacement_string"). Then it will overwrite the VAM file. """
        try:
            with open(path, encoding="utf-8") as f:
                text_json = json.load(f)
            text_json['storables'] = ecc_logic.replace_value_from_id_in_dict_list(text_json['storables'], id_string, needed_key,
                                                                        replacement_string)
            with open(path, "w", encoding="utf-8") as json_file:
                json.dump(text_json, json_file, indent=3)
        except IOError as e:
            print(e)

    def switch_layout_to_rating(self):
        """ Switches the layout from the GUI from the Initialization Choices layout to the rate children layout. Called
            by generate_next_population when called for the first time. """
        self.vamdirframe.grid_remove()
        self.appearancedirframe.grid_remove()
        self.childtemplateframe.grid_remove()
        self.sourcefilesframe.grid_remove()
        self.methodframe.grid_remove()
        self.parentselectionframe.grid()
        self.chromosomelabel.configure(text="Rate Children")
        self.favoritesframe.grid_remove()
        self.optionsframe.grid_remove()

    def weighted_random_selection(self):
        """ using roulette wheel selection, returns a randomly (weighted by rating) chosen appearance from the
            population

            reference: https://stackoverflow.com/questions/10324015/fitness-proportionate-selection-roulette-wheel-selection-in-python
            """

        total_ratings = sum([self.chromosome[str(i)]['rating'] for i in range(1, POP_SIZE + 1)])
        choices = []

        while len(choices) < 2:
            pick = random.uniform(0, total_ratings)
            current = 0
            for i in range(1, POP_SIZE + 1):
                chromosome = self.chromosome[str(i)]
                current += chromosome['rating']
                if current > pick:
                    if not chromosome in choices:
                        choices.append(chromosome)
                    break
        return choices

    def get_elites_from_population(self):
        """ Returns the children appearances where the rating is the maximum rating that the user selected.
            If the maximum selected rating is lower than MINIMAL_RATING_FOR_KEEP_ELITES, then no appearances are
            returned. Returns a maximum of appearances equal to user setting 'max kept elites'. """
        max_selected_rating = max([chromosomeValue['rating'] for chromosomeValue in self.chromosome.values()])

        if max_selected_rating < MINIMAL_RATING_FOR_KEEP_ELITES:
            return []

        # Select all appearances with maximum rating.
        appearances_with_maximum_rating = [chromosomeValue['appearance'] for chromosomeValue in self.chromosome.values()
                                           if chromosomeValue['rating'] == max_selected_rating]

        # Limit the list of appearances to a maximum of 'max kept elites' elements and return it.
        return appearances_with_maximum_rating[:self.settings['max kept elites']]

    def reset_ratings(self):
        """ Clear all ratings in the GUI. """
        for i in range(1, POP_SIZE + 1):
            self.press_rating_button(i, INITIAL_RATING)

    def get_appearance_filenames(self, get_only_favorites):
        """ Returns a list of all appearance files in the default VAM Appearance directory, after gender and morph
            filters are applied. """
        filenames = list()
        if get_only_favorites:
            filenames = [f for f, app in self.generator.appearances.items() if ecc_utility.is_favorite(app)]
        else:
            filenames = list(self.generator.appearances.keys())
        filenames = [f for f in filenames if CHILDREN_FILENAME_PREFIX not in f]

        if 'gender' in self.childtemplate:
            filenames = self.filter_filenamelist_on_genders(filenames,
                                                            ecc_logic.matching_genders(self.childtemplate['gender']))
            filtered = self.filter_filenamelist_on_morph_threshold_and_min_morphs(filenames)
        else:
            filtered = []
        return filtered

    def get_all_appearance_filenames(self):
        return self.get_appearance_filenames(get_only_favorites=False)

    def get_fav_appearance_filenames(self):
        return self.get_appearance_filenames(get_only_favorites=True)

    def get_selected_appearance_filenames(self):
        filenames = [self.chromosome[str(i)]['filename'] for i in range(1, POP_SIZE + 1) if
                     self.chromosome[str(i)]['can load']]
        self.filter_filenamelist_on_morph_threshold_and_min_morphs(filenames)
        return filenames


    def crossover_initialize_population(self, source_files):
        """ Initializes the population using random crossover between all Parent files. Only used for initialization.
            Updates population info and the GUI. """
        print("Using random pairwise chromosome crossover for sample initialization.")

        # select source files
        parent_filenames = self.select_appearances_strategies[source_files]()

        print("Source files: {} ({} Files)".format(source_files, len(parent_filenames)))

        new_population = []
        for i in range(1, POP_SIZE + 1):
            random_parents = random.sample(parent_filenames, 2)
            child_appearance = ecc_logic.fuse_characters(random_parents[0], random_parents[1], self.settings)
            new_population.append(child_appearance)
        self.save_population(new_population)
        self.generator.gencounter += 1
        self.update_population(new_population)
        self.generatechild.configure(bg="lightgreen", text="")
        # to do: why two lines?
        self.generatechild.configure(text="Generate Next Population")
        self.generatechild.update()
        return

    def gaussian_initialize_population(self, source_files):
        # todo: split the UI and the BL parts
        """ Initializes the population using Gaussian Samples based on all Parent files. Only used for initialization.
            Updates population info and the GUI. """
        print("Using random samples from multivariate gaussian distribution for initialization.")
        self.generatechild.configure(text="Generating Population\n Please be patient!\n", bg="red")
        self.generatechild.update()

        # select source files
        filenames = self.select_appearances_strategies[source_files]()

        appearances = [self.generator.appearances[f] for f in filenames]

        print(f"Source files: {source_files} ({len(appearances)} Files)")

        morphlists = [ecc_logic.get_morphlist_from_appearance(appearance) for appearance in appearances]
        morphnames = ecc_logic.get_all_morphnames_in_morphlists(morphlists)
        morphlists = ecc_logic.pad_morph_names_to_morph_lists(morphlists, morphnames, filenames)
        morphlists = ecc_logic.dedupe_morphs(morphlists)
        means = self.get_means_from_morphlists(morphlists)
        means = list(means.values())

        covariances = self.get_cov_from_morphlists(morphlists)
        new_population = []
        templatefile = self.settings['child template']
        threshold = self.settings['morph threshold']

        for i in range(1, POP_SIZE + 1):
            txt = "Generating Population\n" + "Please be patient!\n" + "(" + str(i) + "/" + str(POP_SIZE) + ")"
            self.generatechild.configure(text=txt, bg="red")
            self.generatechild.update()
            self.broadcast_message_to_VAM_rating_blocker(txt)

            sample = np.random.default_rng().multivariate_normal(means, covariances)
            sample = [str(x) for x in sample]
            new_morphlist = copy.deepcopy(morphlists[0])
            for i, morph in enumerate(new_morphlist):
                morph['value'] = sample[i]
            new_morphlist = ecc_logic.filter_morphs_below_threshold(new_morphlist, threshold)
            child_appearance = ecc_logic.load_appearance(templatefile)
            print("Using as appearance template:", templatefile)
            child_appearance = ecc_logic.save_morph_to_appearance(new_morphlist, child_appearance)
            new_population.append(child_appearance)

        self.save_population(new_population)
        self.generator.gencounter += 1

        self.update_population(new_population)
        self.generatechild.configure(bg="lightgreen", text="")
        self.generatechild.configure(text="Generate Next Population")
        self.generatechild.update()
        return


    def get_means_from_morphlists(self, morphlists):
        """ returns a dictionary of morph means for each morph found in the morphlists """
        means = defaultdict(lambda: 0.0)
        for morphlist in morphlists:
            for morph in morphlist:
                if 'value' in morph:
                    means[morph['name']] += np.nan_to_num(float(morph['value'])) * 1 / len(morphlists)
                else:
                    means[morph['name']] += 0 / len(morphlists)  # just assume missing values to be 0
        return means

    def get_cov_from_morphlists(self, morphlists):
        """ Returns covariances of all morphlist. Used by the Random Gaussian sample method. """
        values = defaultdict(lambda: [])
        for morphlist in morphlists:
            for morph in morphlist:
                values[morph['name']].append(np.nan_to_num(float(morph['value'])))
        listofvalues = []
        for key, value in values.items():
            listofvalues.append(value)
        covariances = np.array(listofvalues)
        return np.cov(covariances)

    def save_population(self, population):
        """ save a population list of child appearances to files """
        path = self.get_vam_default_appearance_path()
        save_path = os.path.join(path, SAVED_CHILDREN_PATH)
        pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)
        for i, child_appearance in enumerate(population):
            savefilename = os.path.join(save_path, "Preset_" + CHILDREN_FILENAME_PREFIX + str(i + 1) + ".vap")
            ecc_logic.save_appearance(child_appearance, savefilename)
        return True

    def update_population(self, population):
        """ update all chromosome appearances with the list of child appearance in population """
        path = self.get_vam_default_appearance_path()
        save_path = os.path.join(path, SAVED_CHILDREN_PATH)
        pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)
        for i, child in enumerate(population):
            self.chromosome[str(i + 1)]['appearance'] = child
            filename = os.path.join(save_path, "Preset_" + CHILDREN_FILENAME_PREFIX + str(i + 1) + ".vap")
            self.chromosome[str(i + 1)]['filename'] = filename

    def change_parent_to_generation_display(self):
        """ Changes the Parent """
        self.titlelabel.configure(text="Generation " + str(self.generator.gencounter))
        self.columninfo['1'].destroy()
        self.columninfo['2'].destroy()
        self.columninfo['3'].destroy()

        self.titlerestartbutton = tk.Button(self.titleframe, text="Restart", anchor=tk.E, bg=BUTTON_BG_COLOR,
                                            fg=BUTTON_FG_COLOR, relief=tk.RAISED,
                                            command=lambda: self.press_restart_button())
        self.titlerestartbutton.grid(columnspan=10, row=0, column=1, sticky=tk.E)

        self.changetemplateframe = tk.Frame(self.master, bg=BG_COLOR)
        self.changetemplateframe.grid(row=7, column=1, padx=(10, 0), pady=(5, 0), sticky=tk.W)
        self.changetemplatebutton = tk.Button(self.changetemplateframe, text="Change template", anchor=tk.W,
                                              bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, relief=tk.RAISED,
                                              command=lambda: self.press_change_template_file(
                                                  "Please Select Parent Template"))
        self.changetemplatebutton.grid(row=0, column=0, sticky=tk.W)

        labeltxt = os.path.basename(self.settings['child template'])[7:-4]
        self.changetemplatebuttonlabel = tk.Label(self.changetemplateframe, text=labeltxt, width=14, anchor="w",
                                                  font=FILENAME_FONT, bg=BG_COLOR, fg=FG_COLOR)
        self.changetemplatebuttonlabel.grid(row=0, column=1, sticky=tk.W, padx=0)

        rating_font_size = 13
        self.generatechild.configure(width=27, height=6)

        for i in range(1, POP_SIZE + 1):
            chromosome = self.chromosome[str(i)]
            chromosome['filebutton'].destroy()
            chromosome['filenamedisplay'].destroy()
            chromosome['nmorphdisplay'].destroy()
            del chromosome['filebutton']
            del chromosome['filenamedisplay']
            del chromosome['nmorphdisplay']

        for i in range(1, POP_SIZE + 1):
            chromosome = self.chromosome[str(i)]
            chromosome['childlabel'] = tk.Label(self.parentselectionframe, text="Child " + str(i),
                                        font=(DEFAULT_FONT, 11, "bold"), width=10, anchor="w",
                                        bg=BG_COLOR, fg=FG_COLOR)
            chromosome['childlabel'].grid(row=i + 1, column=0, sticky=tk.W)
            chromosome['rating'] = INITIAL_RATING
            for j in range(1, 6):
                chromosome['rating button ' + str(j)] = \
                    tk.Button(self.parentselectionframe, width=2,
                              font=(
                                  DEFAULT_FONT, rating_font_size,
                                  "bold"),
                              bg=RATING_RAISED_BG_COLOR,
                              fg=RATING_RAISED_FG_COLOR,
                              activebackground=RATING_ACTIVE_BG_COLOR,
                              activeforeground=RATING_ACTIVE_FG_COLOR,
                              text=str(j), command=lambda i=i, j=j: self.press_rating_button(i, j))
                chromosome['rating button ' + str(j)].grid(row=i + 1, column=j)
                chromosome['rating button ' + str(j)].bind("<Enter>",
                                                   lambda e, i=i, j=j: self.on_enter_rating_button(
                                                                            i, j, event=e))
                chromosome['rating button ' + str(j)].bind("<Leave>",
                                                   lambda e, i=i, j=j: self.on_leave_rating_button(
                                                                            i, j, event=e))

    def press_restart_button(self, givewarning=True):
        if givewarning:
            answer = messagebox.askquestion("Warning!",
                                            "Warning! This will reset all your current progress, " +
                                            "reinitialize the app and restart with a (newly generated) Generation 1. " +
                                            "Are you sure?")
            if answer == "no":
                return False
        print("We are restarting")
        self.restart_population(self.settings['method'])
        return True

    def on_enter_rating_button(self, child, rating, event=None):
        """ Show hover effect when entering mouse over a rating button. """
        chromosome = self.chromosome[str(child)]
        if rating == chromosome['rating']:
            return
        chromosome['rating button ' + str(rating)]['background'] = RATING_HOVER_BG_COLOR
        chromosome['rating button ' + str(rating)]['foreground'] = RATING_HOVER_FG_COLOR

    def on_leave_rating_button(self, child, rating, event=None):
        """ Show hover effect when exiting mouse over a rating button. """
        chromosome = self.chromosome[str(child)]
        if rating == chromosome['rating']:
            return
        chromosome['rating button ' + str(rating)]['background'] = RATING_RAISED_BG_COLOR
        chromosome['rating button ' + str(rating)]['foreground'] = RATING_RAISED_FG_COLOR

    def press_rating_button(self, child, rating):
        """ Presses the rating button. """
        chromosome = self.chromosome[str(child)]
        chromosome['rating button ' + str(rating)].configure(relief=tk.SUNKEN,
                                                         bg=RATING_SUNKEN_BG_COLOR,
                                                         fg=RATING_SUNKEN_FG_COLOR)
        chromosome['rating'] = rating

        # reset unchosen buttons
        rest = [x for x in range(1, 6) if x != rating]
        for n in rest:
            chromosome['rating button ' + str(n)].configure(relief=tk.RAISED,
                                                        bg=RATING_RAISED_BG_COLOR,
                                                        fg=RATING_RAISED_FG_COLOR)


if __name__ == '__main__':
    print('I am just a module, please launch the main script "VAM Evolutionary Character Creation.py".')
