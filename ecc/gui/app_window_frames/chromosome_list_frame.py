"""
GUI for VAM Evolutionary Character Creation
By Pino Sante
Please credit me if you change, use or adapt this file.
"""

import tkinter as tk

from ..constants import *
from ...common.utility import *
from ..population import Population


class ChromosomeListFrame(tk.Frame):
    def __init__(self, settings, select_file_strategy):
        super().__init__()
        self.column_info = dict()
        self.column_info['1'] = tk.Label(self, text="Parent Number", bg=BG_COLOR, fg=FG_COLOR)
        self.column_info['1'].grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.column_info['2'] = tk.Label(self, text="Filename", bg=BG_COLOR, fg=FG_COLOR)
        self.column_info['2'].grid(row=1, column=1, sticky=tk.W)
        self.column_info['3'] = tk.Label(self, text="Total Morphs", bg=BG_COLOR, fg=FG_COLOR)
        self.column_info['3'].grid(row=1, column=2, sticky=tk.W)
        # initialize population and chromosomes
        self.population = Population(POP_SIZE, settings)
        for chromo in self.population.chromosomes:
            chromo.initialize_ui(self, select_file_strategy)