import tkinter as tk
from collections import defaultdict
from datetime import datetime
from fnmatch import fnmatch
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from ecc_utility import *


class SelectAppearance(tk.Frame):
    def __init__(self, settings, generator):
        super().__init__()
        self.file_selection_popup = None
        self._file_selection = None
        self.settings = settings
        self.generator = generator

        # # create a dictionary to select appearances
        # self.select_appearances_strategies = {
        #     CHOOSE_ALL_FAVORITES_TEXT: lambda: self.get_fav_appearance_filenames(),
        #     CHOOSE_ALL_TEXT: lambda: self.get_all_appearance_filenames(),
        #     CHOOSE_FILES_TEXT: lambda: self.get_selected_appearance_filenames()
        # }

    def file_selection_with_thumbnails(self, genderlist, title, filteronmorphcount=True):
        """ Called by select_template_file and select_file. Creates a custom file selection popup window, with icons
            from all the files available. Filters on the genders in the genderlist. When called, pauses the main
            AppWindow window until a choice is made, or the file selection window is closed. Clicking on an image button
            calls end_file_selection_with_thumbnails(). """
        self._file_selection = ""

        self.thumbnails_per_row = self.settings['thumbnails per row']

        filenames = list(self.generator.appearances.keys())
        if filteronmorphcount:
            filenames = self.filter_filename_list_on_morph_threshold_and_min_morphs(filenames)
        filenames = self.filter_filename_list_on_genders(filenames, genderlist)

        # create popup window
        self.file_selection_popup = tk.Toplevel()
        if 'file selection geometry' in self.settings:
            geometry = self.settings['file selection geometry']
        else:
            geometry = str(int(190 * self.thumbnails_per_row + 23)) + "x1000"
        self.file_selection_popup.geometry(geometry)
        self.file_selection_popup.title(title)
        self.file_selection_popup.configure(bg=BG_COLOR)
        self.file_selection_popup.iconbitmap(os.path.join(DATA_PATH, ICON_FILENAME))
        self.file_selection_popup.grab_set()

        #
        # Start of scrollbar hack in Tkinter
        #
        canvasholdingframe = tk.Frame(self.file_selection_popup, bg=BG_COLOR)
        canvasholdingframe.pack(fill=tk.BOTH, expand=1)
        self.my_canvas = tk.Canvas(canvasholdingframe, bg=BG_COLOR)
        self.my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        my_scrollbar = ttk.Scrollbar(canvasholdingframe, orient=tk.VERTICAL, command=self.my_canvas.yview)
        my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.my_canvas.configure(yscrollcommand=my_scrollbar.set)
        self.my_canvas.bind('<Configure>', lambda e: self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all")))
        self.my_canvas.bind_all('<MouseWheel>', lambda e: self.my_canvas.yview_scroll(int(-1 * e.delta / 120), "units"))
        self.my_canvas.bind_all('<Escape>', lambda e: self.file_selection_popup.destroy())

        # we basically have a canvas for the scrollbar, and put this frame in it
        self.appearancesframe = tk.Frame(self.my_canvas, bg=BG_COLOR)
        self.my_canvas.create_window((0, 0), window=self.appearancesframe, anchor="nw")
        #
        # End of scrollbar hack in Tkinter
        #

        self.show_all_appearance_buttons(self.appearancesframe, filenames, self.thumbnails_per_row)

        #
        # Bottomframe of the popup
        #
        bottomframe = tk.Frame(self.file_selection_popup, bg=BG_COLOR)
        bottomframe.pack(fill="both")
        button = tk.Button(bottomframe, text="➖", bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR,
                           activebackground=BUTTON_ACTIVE_COLOR, command=lambda: self.change_popup_width(-1, filenames))
        button.pack(side=tk.LEFT)
        button = tk.Button(bottomframe, text="➕", bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR,
                           activebackground=BUTTON_ACTIVE_COLOR, command=lambda: self.change_popup_width(+1, filenames))
        button.pack(side=tk.LEFT)
        self.filefilter = tk.Entry(bottomframe, fg=BUTTON_FG_COLOR, bg=BUTTON_BG_COLOR, width=20)
        self.filefilter.pack(side=tk.LEFT)
        self.filefilter.bind('<Return>', lambda event, arg=filenames: self.apply_file_filter(arg))
        button = tk.Button(bottomframe, text="Filter", bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR,
                           activebackground=BUTTON_ACTIVE_COLOR, command=lambda: self.apply_file_filter(filenames))
        button.pack(side=tk.LEFT)
        button = tk.Button(bottomframe, text="Cancel", bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR,
                           activebackground=BUTTON_ACTIVE_COLOR, command=self.end_file_selection_with_thumbnails)
        button.pack(side=tk.LEFT)
        self.file_selection_popup.wait_window()
        self.my_canvas.unbind_all('<MouseWheel>')
        self.my_canvas.unbind_all('<Escape>')
        return self._file_selection


if __name__ == '__main__':
    print(f'I am just a module, please launch the main script "{MAIN_SCRIPT_NAME}".')
