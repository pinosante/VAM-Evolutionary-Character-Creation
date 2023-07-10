"""
GUI for VAM Evolutionary Character Creation
By Pino Sante
Please credit me if you change, use or adapt this file.
"""

import tkinter as tk

from ...common.utility import *
from ..constants import *


class GenerateChildrenFrame(tk.Frame):
    def __init__(self, settings, command):
        super().__init__(bg=BG_COLOR)
        self.settings = settings
        self.generate_children_button = tk.Button(
            self, text="Initialize Population", bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR,
            activebackground=BUTTON_ACTIVE_COLOR,
            command=lambda: command(self.settings['method']),
            relief="flat", font=(DEFAULT_FONT, 15, "bold")
        )
        self.generate_children_button.grid(row=0, column=0, sticky=tk.W)

    def display_ready_for_new_generation(self):
        self.generate_children_button.configure(bg='lightgreen', text='')
        self.generate_children_button.configure(text='Generate Next Population')
        self.generate_children_button.update()

    def display_progress(self, text):
        self.generate_children_button.configure(text=text, bg='red')
        self.generate_children_button.update()

    def update_initialize_population_button(self, can_generate, messages, generation_callback):
        """ Updates the Initialize Population button, by checking if all necessary files and settings are correct. If
            not, shows in the button what items are missing and makes the button do nothing. If criteria are met, button
            color is changed to green and button functionality is restored. """
        if not can_generate:
            messages = '\n'.join(messages)
            txt = f'Cannot Initialize Population:\n{messages}'
            self.generate_children_button.configure(relief=tk.RAISED, bg="#D0D0D0",
                                                    font=(DEFAULT_FONT, 12, "bold"),
                                                    width=52, height=6,
                                                    activebackground="#D0D0D0",
                                                    text=txt,
                                                    state='disabled')
        else:
            self.generate_children_button.configure(relief="raised",
                                                    bg="lightgreen",
                                                    font=(DEFAULT_FONT, 12, "bold"),
                                                    text="Initialize Population",
                                                    width=52, height=6,
                                                    state='normal',
                                                    command=lambda: generation_callback(
                                                        self.settings['method']))


if __name__ == '__main__':
    print(f'I am just a module, please launch the main script "{MAIN_SCRIPT_NAME}".')
