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

    def display_ready_for_new_generation(self):
        self.generate_children_button.configure(bg='lightgreen', text='')
        self.generate_children_button.configure(text='Generate Next Population')
        self.generate_children_button.update()

    def display_progress(self, text):
        self.generate_children_button.configure(text=text, bg='red')
        self.generate_children_button.update()


if __name__ == '__main__':
    print(f'I am just a module, please launch the main script "{MAIN_SCRIPT_NAME}".')
