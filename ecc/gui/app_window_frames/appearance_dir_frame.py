"""
GUI for VAM Evolutionary Character Creation
By Pino Sante
Please credit me if you change, use or adapt this file.
"""

import tkinter as tk

from ..constants import *
from ...common.utility import *


class AppearanceDirFrame(tk.Frame):
    def __init__(self, settings, font, select_appearance_dir_callback):
        super().__init__()
        self.settings = settings
        self.appearance_dir_title_label = tk.Label(self,
                                                   text="Step 2: Select Appearance folder to use",
                                                   font=font, bg=BG_COLOR, fg=FG_COLOR)
        self.appearance_dir_title_label.grid(columnspan=50, row=0, column=0, sticky=tk.W)
        self.appearance_dir_button = tk.Button(self, text="Select Folder",
                                               bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR,
                                               activebackground=BUTTON_ACTIVE_COLOR, relief=tk.RAISED,
                                               command=lambda: select_appearance_dir_callback())
        self.appearance_dir_button.grid(row=1, column=0, sticky=tk.W)
        self.appearance_dir_label = tk.Label(self, text=NO_FILE_SELECTED_TEXT,
                                             font=FILENAME_FONT, anchor=tk.W, width=MAX_APPEARANCEDIR_STRING_LENGTH,
                                             bg=BG_COLOR, fg=FG_COLOR)
        self.appearance_dir_label.grid(row=1, column=1, sticky=tk.W)

    def investigate_appearance_directory(self):
        if 'appearance dir' in self.settings:
            if len(self.settings['appearance dir']) < 1:
                appearance_dir = NO_FILE_SELECTED_TEXT
            else:
                appearance_dir = strip_dir_string_to_max_length(self.settings['appearance dir'],
                                                                MAX_APPEARANCEDIR_STRING_LENGTH)
                self.appearance_dir_button.configure(relief=tk.SUNKEN)
        else:
            appearance_dir = NO_FILE_SELECTED_TEXT
            self.settings['appearance dir'] = ""
        self.appearance_dir_label.configure(text=appearance_dir)
