"""
GUI for VAM Evolutionary Character Creation
By Pino Sante
Please credit me if you change, use or adapt this file.
"""

import tkinter as tk

from ..constants import *


class TitleFrame(tk.Frame):
    def __init__(self):
        super().__init__()
        self.grid(row=0, column=1, padx=10, pady=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.title_label = tk.Label(self, text="Initialization",
                                    font=(DEFAULT_FONT, 14, "bold"),
                                    bg=BG_COLOR, fg=FG_COLOR)
