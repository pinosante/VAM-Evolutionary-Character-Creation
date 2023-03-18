"""
GUI for VAM Evolutionary Character Creation
By Pino Sante
Please credit me if you change, use or adapt this file.
"""

import tkinter as tk

from ..constants import *
from ...common.utility import *


class OptionsFrame(tk.Frame):
    def __init__(self, settings, font,
                 track_threshold_change_strategy,
                 track_min_morph_change_strategy,
                 use_recursive_directory_search_strategy):
        super().__init__()
        self.settings = settings
        option_row_number = 1
        options_label = tk.Label(self, text="Step 7: Options", font=font, bg=BG_COLOR,
                                 fg=FG_COLOR)
        options_label.grid(columnspan=9, row=option_row_number, sticky=tk.W, pady=(0, 0))
        option_row_number += 1  # go to next row of the options menu
        self.threshold_label = tk.Label(self, text="A) Remove morphs with absolute value below:",
                                        anchor='w', bg=BG_COLOR, fg=FG_COLOR)
        self.threshold_label.grid(columnspan=5, row=option_row_number, column=0, sticky=tk.W, padx=(0, 0))
        # track if the threshold values are changed by the user and if so, update the morph info based on the setting
        self.threshold_var = tk.DoubleVar()
        self.threshold_var.set(0.01)
        self.threshold_var.trace_add("write", track_threshold_change_strategy)
        self.threshold_entry = tk.Entry(self, textvariable=self.threshold_var, fg=BUTTON_FG_COLOR,
                                        bg=BUTTON_BG_COLOR, width=7)
        self.threshold_entry.grid(columnspan=2, row=option_row_number, column=10, sticky=tk.W)
        self.threshold_label = tk.Label(self, text="(0 = keep all)", bg=BG_COLOR, fg=FG_COLOR)
        self.threshold_label.grid(row=option_row_number, column=12, sticky=tk.W)
        # minimum morphs needed in appearance to be available in file selection
        option_row_number += 1  # go to next row of the options menu
        self.min_morph_label = tk.Label(self, text="B) Only show appearances with morph count above:",
                                        anchor='w', bg=BG_COLOR, fg=FG_COLOR)
        self.min_morph_label.grid(columnspan=5, row=option_row_number, column=0, sticky=tk.W, padx=(0, 0))
        # track if the threshold values are changed by the user and if so, update the morph info based on the setting
        self.min_morph_var = tk.IntVar()
        self.min_morph_var.set(0)
        self.min_morph_var.trace_add("write", track_min_morph_change_strategy)
        self.min_morph_entry = tk.Entry(self, textvariable=self.min_morph_var, fg=BUTTON_FG_COLOR,
                                        bg=BUTTON_BG_COLOR, width=7)
        self.min_morph_entry.grid(columnspan=2, row=option_row_number, column=10, sticky=tk.W)
        self.min_morph_info_label = tk.Label(self, text="(0 = show all)", bg=BG_COLOR, fg=FG_COLOR)
        self.min_morph_info_label.grid(row=option_row_number, column=12, sticky=tk.W)
        option_row_number += 1  # go to next row of the options menu
        self.max_kept_elites_label = tk.Label(self, text="C) Max kept elites (highest rated):",
                                              anchor='w',
                                              bg=BG_COLOR, fg=FG_COLOR)
        self.max_kept_elites_label.grid(columnspan=5, row=option_row_number, column=0, sticky=tk.W, padx=(0, 0))
        # track if the max_kept_elites values are changed by the user
        self.max_kept_elites_var = tk.IntVar()
        self.max_kept_elites_var.set(DEFAULT_MAX_KEPT_ELITES)
        self.max_kept_elites_var.trace_add("write", self.track_max_kept_elites_change)
        self.max_kept_elites_entry = tk.Entry(self, textvariable=self.max_kept_elites_var,
                                              fg=BUTTON_FG_COLOR,
                                              bg=BUTTON_BG_COLOR, width=7)
        self.max_kept_elites_entry.grid(columnspan=2, row=option_row_number, column=10, sticky=tk.W)
        option_row_number += 1  # go to next row of the options menu
        self.recursive_directory_search_label = tk.Label(self,
                                                         text="D) Also read subdirectories in file selection:",
                                                         anchor='w', bg=BG_COLOR, fg=FG_COLOR)
        self.recursive_directory_search_label.grid(columnspan=5, row=option_row_number, column=0, sticky=tk.W)
        self.recursive_directory_search_yes_button = tk.Button(self, text="Yes", bg=BUTTON_BG_COLOR,
                                                               fg=BUTTON_FG_COLOR, activebackground=BUTTON_ACTIVE_COLOR,
                                                               command=lambda: use_recursive_directory_search_strategy(
                                                                   True))
        self.recursive_directory_search_yes_button.grid(row=option_row_number, column=10, sticky=tk.W)
        self.recursive_directory_search_no_button = tk.Button(self, text="No", bg=BUTTON_BG_COLOR,
                                                              fg=BUTTON_FG_COLOR, activebackground=BUTTON_ACTIVE_COLOR,
                                                              command=lambda: use_recursive_directory_search_strategy(
                                                                  False))
        self.recursive_directory_search_no_button.grid(row=option_row_number, column=11, sticky=tk.W)

    def track_max_kept_elites_change(self, var, index, mode):
        """ Keeps track if the user changes the 'max kept elites' value in the GUI.
            If an invalid value is chosen, then we use the default value.
            """
        string = self.max_kept_elites_entry.get()
        try:
            value = int(string)

            if 0 <= value <= POP_SIZE:
                self.settings['max kept elites'] = value
            else:
                self.settings['max kept elites'] = DEFAULT_MAX_KEPT_ELITES

        except ValueError:
            self.settings['max kept elites'] = DEFAULT_MAX_KEPT_ELITES
            return
