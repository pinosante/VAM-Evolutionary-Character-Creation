"""
GUI for VAM Evolutionary Character Creation
By Pino Sante
Please credit me if you change, use or adapt this file.
"""

import tkinter as tk

from ..constants import *
from ...common.utility import *


class VamDirFrame(tk.Frame):
    def __init__(self, settings, font, select_vam_dir_callback):
        super().__init__()
        self.settings = settings
        self.vam_dir_title_label = tk.Label(self,
                                            text="Step 1: Select VAM Base Folder (with VaM.exe)",
                                            font=font, bg=BG_COLOR, fg=FG_COLOR)
        self.vam_dir_title_label.grid(columnspan=50, row=0, column=0, sticky=tk.W)
        self.vam_dir_button = tk.Button(self, text="VAM Base Folder", bg=BUTTON_BG_COLOR,
                                        fg=BUTTON_FG_COLOR,
                                        activebackground=BUTTON_ACTIVE_COLOR, relief=tk.RAISED,
                                        command=lambda: select_vam_dir_callback())
        self.vam_dir_button.grid(row=1, column=0, sticky=tk.W)
        self.vam_dir_label = tk.Label(self, text=NO_FILE_SELECTED_TEXT,
                                      font=FILENAME_FONT, anchor=tk.W, width=MAX_VAMDIR_STRING_LENGTH,
                                      bg=BG_COLOR, fg=FG_COLOR)
        self.vam_dir_label.grid(row=1, column=1, sticky=tk.W)
