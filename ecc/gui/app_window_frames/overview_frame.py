"""
GUI for VAM Evolutionary Character Creation
By Pino Sante
Please credit me if you change, use or adapt this file.
"""

import tkinter as tk

from ..constants import *


class OverviewFrame(tk.Frame):
    def __init__(self, gen_counter, label_text):
        super().__init__()
        self.warning_label = tk.Label(self, text="Important: do NOT close this window!",
                                      font=(DEFAULT_FONT, 14, "bold"), bg=BG_COLOR, fg="red")
        self.warning_label.grid(row=0, columnspan=2, column=0, padx=(10, 10), pady=(10, 0), sticky="w")
        self.overview_label = tk.Label(self, text="Overview:", font=(DEFAULT_FONT, 14, "bold"),
                                       bg=BG_COLOR, fg=FG_COLOR)
        self.overview_label.grid(row=1, columnspan=2, column=0, padx=(10, 0), pady=(10, 0), sticky="w")
        self.generation_label = tk.Label(self, text="Generation:", bg=BG_COLOR, fg=FG_COLOR)
        self.generation_label.grid(row=2, column=0, padx=(10, 0), pady=(0, 0), sticky="w")
        self.generation_number_label = tk.Label(self, text=gen_counter,
                                                font=FILENAME_FONT,
                                                bg=BG_COLOR,
                                                fg=FG_COLOR, anchor="w", justify=tk.LEFT)
        self.generation_number_label.grid(row=2, column=1, padx=0, pady=(0, 0), sticky="w")
        self.template_label = tk.Label(self, text="Current template:", bg=BG_COLOR, fg=FG_COLOR)
        self.template_label.grid(row=3, column=0, padx=(10, 0), pady=(0, 0), sticky="w")
        self.template_file_label = tk.Label(self, text="", font=FILENAME_FONT, bg=BG_COLOR, fg=FG_COLOR,
                                            anchor="w", justify=tk.LEFT)
        self.template_file_label.grid(row=3, column=1, padx=0, pady=(0, 0), sticky="w")
        self.template_file_label.configure(text=label_text)

