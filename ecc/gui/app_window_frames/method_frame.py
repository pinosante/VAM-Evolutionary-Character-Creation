"""
GUI for VAM Evolutionary Character Creation
By Pino Sante
Please credit me if you change, use or adapt this file.
"""


import tkinter as tk

from ..constants import *


class MethodFrame(tk.Frame):
    def __init__(self, font, settings, callback_for_update):
        super().__init__()
        self.settings = settings
        self.callback_for_update = callback_for_update
        self.method_label = tk.Label(self, text="Step 6: Initialization Method", font=font,
                                     bg=BG_COLOR, fg=FG_COLOR)
        self.method_label.grid(columnspan=2, row=0, column=0, sticky=tk.W, pady=(0, 0))
        self.gaussian_button = tk.Button(self, text="Gaussian Samples", bg=BUTTON_BG_COLOR,
                                         fg=BUTTON_FG_COLOR, activebackground=BUTTON_ACTIVE_COLOR,
                                         command=lambda: self.choose_gaussian_samples())
        self.gaussian_button.grid(row=1, column=0, sticky=tk.W)
        self.random_cross_over_button = tk.Button(self, text="Random Crossover", bg=BUTTON_BG_COLOR,
                                                  fg=BUTTON_FG_COLOR, activebackground=BUTTON_ACTIVE_COLOR,
                                                  command=lambda: self.choose_random_crossover())
        self.random_cross_over_button.grid(row=1, column=1, sticky=tk.W)

        if 'method' in self.settings:
            if self.settings['method'] == "Gaussian Samples":
                self.choose_gaussian_samples()
            elif self.settings['method'] == "Random Crossover":
                self.choose_random_crossover()
        else:
            self.choose_random_crossover()

    def choose_gaussian_samples(self):
        """ Called when the Gaussian Samples button is pressed. Raises the random crossover button. Saves choice in
            settings. """
        self.gaussian_button.configure(relief=tk.SUNKEN)
        self.random_cross_over_button.configure(relief=tk.RAISED)
        self.settings['method'] = 'Gaussian Samples'
        self.callback_for_update()

    def choose_random_crossover(self):
        """ Called when the random crossover button is pressed. Raises the Gaussian Samples  button. Saves choice in
            settings. """
        self.gaussian_button.configure(relief=tk.RAISED)
        self.random_cross_over_button.configure(relief=tk.SUNKEN)
        self.settings['method'] = 'Random Crossover'
        self.callback_for_update()
