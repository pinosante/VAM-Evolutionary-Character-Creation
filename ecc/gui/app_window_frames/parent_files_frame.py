"""
GUI for VAM Evolutionary Character Creation
By Pino Sante
Please credit me if you change, use or adapt this file.
"""

import tkinter as tk

from ..constants import *


class ParentsFileFrame(tk.Frame):
    def __init__(self, font, choose_all_appearances_strategy, choose_all_favorites_strategy, choose_files_strategy):
        super().__init__()
        self.source_files_label = tk.Label(self, text="Step 4: Select Parent Appearances",
                                           font=font, bg=BG_COLOR, fg=FG_COLOR)
        self.source_files_label.grid(columnspan=2, row=0, column=0, sticky=tk.W, pady=(0, 0))
        self.all_appearances_button = tk.Button(self, text="All Appearances", bg=BUTTON_BG_COLOR,
                                                fg=BUTTON_FG_COLOR, activebackground=BUTTON_ACTIVE_COLOR,
                                                command=lambda: choose_all_appearances_strategy())
        self.all_appearances_button.grid(row=1, column=0, sticky=tk.W)
        self.all_favorites_button = tk.Button(self, text="All Favorited Appearances",
                                              bg=BUTTON_BG_COLOR,
                                              fg=BUTTON_FG_COLOR, activebackground=BUTTON_ACTIVE_COLOR,
                                              command=lambda: choose_all_favorites_strategy())
        self.all_favorites_button.grid(row=1, column=1, sticky=tk.W)
        self.choose_files_button = tk.Button(self, text=CHOOSE_FILES_TEXT, bg=BUTTON_BG_COLOR,
                                             fg=BUTTON_FG_COLOR, activebackground=BUTTON_ACTIVE_COLOR,
                                             command=lambda: choose_files_strategy())
        self.choose_files_button.grid(row=1, column=2, sticky=tk.W)


if __name__ == '__main__':
    print(f'I am just a module, please launch the main script "{MAIN_SCRIPT_NAME}".')
