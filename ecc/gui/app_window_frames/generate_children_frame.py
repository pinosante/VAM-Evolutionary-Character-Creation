"""
GUI for VAM Evolutionary Character Creation
By Pino Sante
Please credit me if you change, use or adapt this file.
"""

import tkinter as tk

from ..constants import *


class GenerateChildrenFrame(tk.Frame):
    def __init__(self, settings, command):
        super().__init__()
        self.settings = settings
        self.generate_children_button = tk.Button(
            self, text="Initialize Population", bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR,
            activebackground=BUTTON_ACTIVE_COLOR,
            command=lambda: command(self.settings['method']),
            relief="flat", font=(DEFAULT_FONT, 15, "bold")
        )
        self.generate_children_button.grid(row=0, column=0, sticky=tk.W)
