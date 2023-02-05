"""todo"""
import tkinter as tk
from ecc_gui_constants import *
from ecc_utility import *


class Chromosome:
    """todo: split chromosome into GUI, BL and DAL part"""
    def __init__(self, index, settings):
        # data -- todo: decide if indices should be start with 0 or with 1
        self.index = index
        self.settings = settings
        self.appearance = None
        self.rating = INITIAL_RATING
        # file access
        self.filename = ''
        self.short_filename = ''
        self.can_load = False
        # UI stuff
        self.file_button = None
        self.file_name_display = None
        self.child_label = None
        self.n_morph_display = None
        self.rating_buttons = list()

    def initialize_ui(self, frame, select_file_callback):
        index = self.index + 1
        self.file_button = tk.Button(frame, text=f'Parent {index}',
                                     bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR,
                                     activebackground=BUTTON_ACTIVE_COLOR,
                                     # todo: fix this! select_file is still from gui, but cannot be accessed here
                                     command=lambda s=select_file_callback: self.select_file(s), width=10)
        self.file_button.grid(row=index, column=0, sticky=tk.W)
        self.file_name_display = tk.Label(frame, text=NO_FILE_SELECTED_TEXT,
                                          font=FILENAME_FONT, width=28, anchor='w', bg=BG_COLOR,
                                          fg=FG_COLOR)
        self.file_name_display.grid(row=index, column=1, sticky=tk.W)
        self.n_morph_display = tk.Label(frame, text="N/A", bg=BG_COLOR, fg=FG_COLOR)
        self.n_morph_display.grid(row=index + 1, column=2, sticky=tk.W)
        self.can_load = False

    def update_gui_file(self, filename, appearance):
        self.filename = filename
        self.short_filename = os.path.basename(filename)[7:-4]  # remove Preset_ and .vap
        self.file_name_display.configure(text=self.short_filename)
        self.appearance = appearance
        self.can_load = True

    def destroy_ui(self):
        self.file_button.destroy()
        self.file_name_display.destroy()
        self.n_morph_display.destroy()
        del self.file_button
        del self.file_name_display
        del self.n_morph_display

    def get_rating_button(self, rating):
        """rating button now are kept inside a zero based list, so decrement the one-based rating"""
        assert MIN_RATING <= rating <= MAX_RATING
        return self.rating_buttons[rating - 1]

    def on_enter_rating_button(self, rating):
        """ Show hover effect when entering mouse over a rating button. """
        if rating == self.rating:
            return
        crb = self.get_rating_button(rating)
        crb.configure(bg=RATING_HOVER_BG_COLOR, fg=RATING_HOVER_FG_COLOR)

    def on_leave_rating_button(self, rating):
        """ Show hover effect when exiting mouse over a rating button. """
        if rating == self.rating:
            return
        crb = self.get_rating_button(rating)
        crb.configure(bg=RATING_RAISED_BG_COLOR, fg=RATING_RAISED_FG_COLOR)

    def update_rating(self, rating):
        """ Presses the rating button. """
        if rating == self.rating:
            return
        for i, rb in enumerate(self.rating_buttons):
            if i + 1 != rating:
                rb.configure(relief=tk.RAISED, bg=RATING_RAISED_BG_COLOR, fg=RATING_RAISED_FG_COLOR)
            else:
                rb.configure(relief=tk.SUNKEN, bg=RATING_SUNKEN_BG_COLOR, fg=RATING_SUNKEN_FG_COLOR)
                self.rating = rating

    def initialize_rating_buttons(self, frame):
        index = self.index + 1
        self.child_label = tk.Label(frame, text=f'Child {index}',
                                    font=(DEFAULT_FONT, 11, 'bold'), width=10, anchor='w',
                                    bg=BG_COLOR, fg=FG_COLOR)
        self.child_label.grid(row=index + 1, column=0, sticky=tk.W)
        self.rating = INITIAL_RATING
        self.rating_buttons = list()
        for j in range(MIN_RATING, MAX_RATING + 1):
            new_rating_button = tk.Button(frame, width=2,
                                          font=(DEFAULT_FONT, RATING_FONT_SIZE, 'bold'),
                                          bg=RATING_RAISED_BG_COLOR,
                                          fg=RATING_RAISED_FG_COLOR,
                                          activebackground=RATING_ACTIVE_BG_COLOR,
                                          activeforeground=RATING_ACTIVE_FG_COLOR,
                                          text=str(j), command=lambda r=j: self.update_rating(r))
            new_rating_button.grid(row=index, column=j)
            new_rating_button.bind('<Enter>', lambda r=j: self.on_enter_rating_button(r))
            new_rating_button.bind('<Leave>', lambda r=j: self.on_leave_rating_button(r))
            self.rating_buttons.append(new_rating_button)

    def update_appearance(self, appearance, filename):
        self.appearance = appearance
        self.filename = os.path.join(filename, f'Preset_{CHILDREN_FILENAME_PREFIX}{self.index + 1}.vap')

    def select_file(self, select_file_callback):
        """event handler. this is required because the gui has some work to do if a file is selected"""
        select_file_callback(self.index + 1)


class Population:
    def __init__(self, size, settings):
        self.settings = settings
        self.chromosomes = [Chromosome(index, settings) for index in range(size)]

    def get_chromosome(self, index):
        """index is one-based, but chromosomes are inside a zero-based list"""
        assert 1 <= index <= POP_SIZE
        c = self.chromosomes[index - 1]
        assert c.index == index - 1
        return c


if __name__ == '__main__':
    print(f'I am just a module, please launch the main script "{MAIN_SCRIPT_NAME}".')
