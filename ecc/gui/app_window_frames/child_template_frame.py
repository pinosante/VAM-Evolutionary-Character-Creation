"""
GUI for VAM Evolutionary Character Creation
By Pino Sante
Please credit me if you change, use or adapt this file.
"""

import tkinter as tk

from ..constants import *
from ...common.utility import *


class ChildTemplateFrame(tk.Frame):
    def __init__(self, font, select_template_strategy):
        super().__init__(bg=BG_COLOR)
        self.select_template_strategy = select_template_strategy
        self.child_template_label = tk.Label(self,
                                             text="Step 3: Select Child Template Appearance", font=font,
                                             bg=BG_COLOR, fg=FG_COLOR)
        self.child_template_label.grid(columnspan=50, row=0, column=0, sticky=tk.W, pady=(0, 0))
        self.child_template_button = {
            FEMALE: self.create_child_template_button(FEMALE, 0),
            MALE: self.create_child_template_button(MALE, 1),
            FUTA: self.create_child_template_button(FUTA, 2)
        }
        self.child_template = dict()
        self.child_template['label'] = tk.Label(self, text=NO_FILE_SELECTED_TEXT,
                                                font=FILENAME_FONT, bg=BG_COLOR, fg=FG_COLOR)
        self.child_template['label'].grid(row=1, column=3, sticky=tk.W, padx=0)

    def create_child_template_button(self, gender_text, column):
        button = tk.Button(self, text=gender_text,
                           bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR,
                           activebackground=BUTTON_ACTIVE_COLOR,
                           command=lambda: self.select_template_strategy([gender_text],
                                                                         'Please Select Parent Template'))
        button.grid(row=1, column=column, sticky=tk.W, padx=0)
        return button
