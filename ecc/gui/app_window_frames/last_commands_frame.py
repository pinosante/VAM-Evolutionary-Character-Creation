"""
GUI for VAM Evolutionary Character Creation
By Pino Sante
Please credit me if you change, use or adapt this file.
"""

import tkinter as tk

from ..constants import *

class LastCommandsFrame(tk.Frame):
    def __init__(self):
        super().__init__()
        self.last_commands_label = tk.Label(self, text="Last five commands:",
                                            font=(DEFAULT_FONT, 14, "bold"), bg=BG_COLOR, fg=FG_COLOR)
        self.last_commands_label.grid(row=0, column=0, padx=10, pady=0, sticky="w")
        self.commands_label = tk.Label(self, text="...", font=FILENAME_FONT, bg=BG_COLOR,
                                       fg=FG_COLOR,
                                       justify=tk.LEFT, anchor="w")
        self.commands_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="w")
