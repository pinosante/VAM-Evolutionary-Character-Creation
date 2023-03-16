import pathlib
import tkinter as tk
from tkinter import ttk

from ecc_gui_constants import *
from ecc_utility import *


class SelectAppearanceDialog(tk.Frame):
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
        filenames = self.generator.filter_filename_list_on_genders(filenames, genderlist)

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

    def end_file_selection_with_thumbnails(self, filename="", event=None):
        """ Saves settings and returns the filename through self._file_selection """
        self.settings['file selection geometry'] = self.file_selection_popup.winfo_geometry()
        self.settings['thumbnails per row'] = self.thumbnails_per_row
        self._file_selection = str(pathlib.Path(filename))  # use uniform filename formatting
        self.file_selection_popup.destroy()

    def change_popup_width(self, value, filenames):
        """ Changes the amount of images shown on each row. Value is either +1 or -1 depending on which function calls
            this. Filenames is the list of filenames to be displayed in the file selection window. """
        self.remove_all_appearance_widgets()
        self.thumbnails_per_row += value
        height = self.file_selection_popup.winfo_height()
        geometry = str(int(190 * self.thumbnails_per_row + 23)) + "x" + str(height)
        self.file_selection_popup.geometry(geometry)
        self.show_all_appearance_buttons(self.appearancesframe, filenames, self.thumbnails_per_row)

    def show_all_appearance_buttons(self, window, filenames, thumbnails_per_row):
        """ Show all appearance files as image buttons, in the given window. """
        self.all_appearance_widgets = list()
        max_vertical = int(len(filenames) / thumbnails_per_row) + 1
        file_index = 0
        self.appearancebutton = dict()
        self.appearancelabel = dict()
        for row in range(max_vertical):
            for column in range(thumbnails_per_row):
                if file_index >= len(filenames):
                    return
                button, label = self.make_appearance_button(window, filenames[file_index], row, column, file_index)
                self.all_appearance_widgets.extend((button, label))
                file_index += 1

    def make_appearance_button(self, window, file_name, row, column, index):
        """ Make individual appearance button in file selection window. Called by show_all_appearance_buttons. """
        self.appearancebutton[index] = self.make_appearance_button_sub(window, file_name, row, column, index)
        self.appearancelabel[index] = self.make_appearance_button_label(window, file_name, row, column)
        return self.appearancebutton[index], self.appearancelabel[index]

    def make_appearance_button_sub(self, window, file_name, row, column, file_index):
        """ todo """
        thumbnail = self.generator.thumbnails[file_name]
        appearance_button = tk.Button(window, relief=tk.FLAT, bg=BG_COLOR,
                                      command=lambda fn=file_name: self.end_file_selection_with_thumbnails(fn))
        appearance_button.grid(row=row * 2, column=column, padx=0, pady=0)
        appearance_button.configure(image=thumbnail)
        appearance_button.bind("<Enter>", lambda e, index=file_index: self.on_enter_appearancebutton(index, event=e))
        appearance_button.bind("<Leave>", lambda e, index=file_index: self.on_leave_appearancebutton(index, event=e))
        appearance_button.image = thumbnail
        return appearance_button

    def make_appearance_button_label(self, window, file_name, row, column):
        """ todo """
        label_name = os.path.basename(file_name)[7:-4]  # remove Preset_ and .vap
        appearance_label = tk.Label(window, text=label_name, font=FILENAME_FONT, width=26, anchor=tk.W,
                                    bg=BG_COLOR, fg=FG_COLOR, padx=0, pady=0)
        appearance_label.grid(row=row * 2 + 1, column=column, sticky=tk.W)
        return appearance_label

    def on_enter_appearancebutton(self, index, event=None):
        """ Show hover effect when entering mouse over an image file. """
        self.appearancebutton[index][BACKGROUND] = HOVER_COLOR
        self.appearancelabel[index][BACKGROUND] = BG_COLOR
        self.appearancelabel[index][FOREGROUND] = HOVER_COLOR

    def on_leave_appearancebutton(self, index, event=None):
        """ Show hover effect when exiting mouse over an image file. """
        self.appearancebutton[index][BACKGROUND] = BG_COLOR
        self.appearancelabel[index][BACKGROUND] = BG_COLOR
        self.appearancelabel[index][FOREGROUND] = FG_COLOR


if __name__ == '__main__':
    print(f'I am just a module, please launch the main script "{MAIN_SCRIPT_NAME}".')
