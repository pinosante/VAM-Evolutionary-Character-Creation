"""
GUI for VAM Evolutionary Character Creation
By Pino Sante
Please credit me if you change, use or adapt this file.
"""

import tkinter as tk

from ..constants import *
from ...common.utility import *


class AlternativeAppearanceFrame(tk.Frame):
    def __init__(self):
        super().__init__()
        self.favorites_label = tk.Label(self, text="Step 5: Favorited Appearances Chosen",
                                        font=self, bg=BG_COLOR, fg=FG_COLOR)
        self.favorites_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 0))
        self.favorites_info = tk.Label(self, text="", bg=BG_COLOR, fg=FG_COLOR)
        self.favorites_info.grid(row=1, column=0, sticky=tk.W, pady=(0, 0))
        self.grid_remove()  # will be shown when needed
