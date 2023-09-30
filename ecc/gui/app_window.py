"""
GUI for VAM Evolutionary Character Creation
By Pino Sante
Please credit me if you change, use or adapt this file.
"""

import pathlib
import tkinter as tk

from datetime import datetime
from tkinter import filedialog
from tkinter import messagebox

from .constants import *

from .app_window_frames.alternative_appearance_frame import AlternativeAppearanceFrame
from .app_window_frames.appearance_dir_frame import AppearanceDirFrame
from .app_window_frames.child_template_frame import ChildTemplateFrame
from .app_window_frames.chromosome_list_frame import ChromosomeListFrame
from .app_window_frames.generate_children_frame import GenerateChildrenFrame
from .app_window_frames.method_frame import MethodFrame
from .app_window_frames.options_frame import OptionsFrame
from .app_window_frames.parent_files_frame import ParentsFileFrame
from .app_window_frames.title_frame import TitleFrame
from .app_window_frames.vam_dir_frame import VamDirFrame
from .app_window_frames.overview_frame import OverviewFrame
from .app_window_frames.last_commands_frame import LastCommandsFrame

from .select_appearance import SelectAppearanceDialog
from ..logic.tools import *
from .population import Population

from ..logic.vam_comm import VamComm


class AppWindow(tk.Frame):
    def __init__(self, settings, generator):
        super().__init__()

        self.population = Population(POP_SIZE, settings)
        self.settings = settings
        self.generator = generator
        self.vam_comm = VamComm(settings, self.master,
                                self.execute_vam_command_callback)

        self.subtitle_font = (DEFAULT_FONT, 11, 'bold')
        self.subtitle_padding = 1

        # create a dictionary to select appearances
        self.select_appearances_strategies = {
            CHOOSE_ALL_FAVORITES_TEXT: lambda: self.get_fav_appearance_filenames(),
            CHOOSE_ALL_TEXT: lambda: self.get_all_appearance_filenames(),
            CHOOSE_FILES_TEXT: lambda: self.get_selected_appearance_filenames()
        }

        self.title_frame = TitleFrame()
        self.title_frame.grid(row=0, column=0, sticky=tk.W)

        self.generate_children_frame = GenerateChildrenFrame(
            settings, self.generate_next_population)
        self.generate_children_frame.grid(
            row=8, column=1, padx=10, pady=self.subtitle_padding, sticky=tk.W)

        self.vam_dir_frame = VamDirFrame(
            settings, self.subtitle_font, self.select_vam_dir_callback)
        self.vam_dir_frame.grid(row=1, column=1, padx=10,
                                pady=self.subtitle_padding, sticky=tk.W)

        self.appearance_dir_frame = AppearanceDirFrame(
            self.subtitle_font, self.select_appearance_dir_callback)
        self.appearance_dir_frame.grid(
            row=2, column=1, padx=10, pady=self.subtitle_padding, sticky=tk.W)

        self.child_template_frame = ChildTemplateFrame(
            self.subtitle_font, self.select_template_file)
        self.child_template_frame.grid(
            row=3, column=1, padx=10, pady=self.subtitle_padding, sticky=tk.W)

        self.source_files_frame = ParentsFileFrame(self.subtitle_font,
                                                   self.choose_all_appearances,
                                                   self.choose_all_favorites,
                                                   self.choose_files)
        self.source_files_frame.grid(
            row=4, column=1, padx=10, pady=self.subtitle_padding, sticky=tk.W)

        self.parent_selection_frame = ChromosomeListFrame(
            self.subtitle_font, self.population, self.select_file)
        self.parent_selection_frame.grid(
            row=5, column=1, padx=10, pady=self.subtitle_padding, sticky=tk.W)

        self.favorites_frame = AlternativeAppearanceFrame()
        self.favorites_frame.grid(
            row=5, column=1, padx=10, pady=self.subtitle_padding, sticky=tk.W)

        self.method_frame = MethodFrame(
            self.subtitle_font, settings, self.update_initialize_population_button)
        self.method_frame.grid(row=6, column=1, padx=10,
                               pady=self.subtitle_padding, sticky=tk.W)

        self.options_frame = OptionsFrame(settings, self.subtitle_font,
                                          self.track_threshold_change,
                                          self.track_min_morph_change,
                                          self.use_recursive_directory_search)
        self.options_frame.grid(row=7, column=1, padx=10,
                                pady=self.subtitle_padding, sticky=tk.W)

        self.filler_bottom = tk.Label(self.generate_children_frame, text="", width=1, height=10, bg=BG_COLOR,
                                      fg=FG_COLOR)
        self.filler_bottom.grid(row=0, column=1)

        self.overview_frame = None
        self.last_commands_frame = None

    def initialize(self):
        """ Runs at the start of the app to load all previously saved settings and sets defaults when settings are
            not found """
        self.investigate_appearance_directory()

        if 'recursive directory search' in self.settings:
            self.use_recursive_directory_search(
                self.settings['recursive directory search'])
        else:
            self.use_recursive_directory_search(False)

        if 'VAM base dir' in self.settings:
            if len(self.settings['VAM base dir']) < 1:
                vam_dir = NO_FILE_SELECTED_TEXT
            else:
                vam_dir = strip_dir_string_to_max_length(self.settings['VAM base dir'],
                                                         MAX_VAMDIR_STRING_LENGTH)
                self.vam_dir_frame.vam_dir_button.configure(relief=tk.SUNKEN)
        else:
            vam_dir = NO_FILE_SELECTED_TEXT
        self.vam_dir_frame.vam_dir_label.configure(text=vam_dir)

        if 'child template' in self.settings:
            if os.path.isfile(self.settings['child template']):
                self.child_template_frame.child_template['label'].configure(
                    text=self.create_template_labeltext(self.settings['child template']))
                self.child_template_frame.child_template['gender'] = get_appearance_gender(
                    load_appearance(self.settings['child template']))
                self.press_child_template_button(
                    self.child_template_frame.child_template['gender'])

        if 'morph threshold' in self.settings:
            self.options_frame.threshold_var.set(
                self.settings['morph threshold'])
        else:
            self.settings['morph threshold'] = 0.01

        if 'min morph threshold' in self.settings:
            self.options_frame.min_morph_var.set(
                self.settings['min morph threshold'])
        else:
            self.settings['min morph threshold'] = 150
            self.options_frame.min_morph_var.set(150)

        if 'max kept elites' in self.settings:
            self.options_frame.max_kept_elites_var.set(
                self.settings['max kept elites'])
        else:
            self.settings['max kept elites'] = DEFAULT_MAX_KEPT_ELITES

        for i in range(1, POP_SIZE + 1):
            if 'file ' + str(i) in self.settings:
                if len(self.settings['file ' + str(i)]) > 0:
                    filename = self.settings['file ' + str(i)]
                    self.update_gui_file(i, filename)
                    self.update_morph_info(i)

        if 'source files' in self.settings:
            if self.settings['source files'] == CHOOSE_FILES_TEXT:
                self.choose_files()
            elif self.settings['source files'] == CHOOSE_ALL_FAVORITES_TEXT:
                self.choose_all_favorites()
            elif self.settings['source files'] == CHOOSE_ALL_TEXT:
                self.choose_all_appearances()

        if 'thumbnails per row' not in self.settings:
            self.settings['thumbnails per row'] = 5

        if 'generation counter' in self.settings:
            gc = self.settings["generation counter"]
            answer = messagebox.askquestion('Continue last session?',
                                            f"""Your last session ended at Generation {gc}.
Do you want to continue that session?""")
            if answer == "yes":
                self.generator.gen_counter = self.settings['generation counter']
                self.continue_last_session()
                return
            else:
                del self.settings['generation counter']

        self.update_initialize_population_button()

    def investigate_appearance_directory(self):
        if 'appearance dir' in self.settings:
            if len(self.settings['appearance dir']) < 1:
                appearance_dir = NO_FILE_SELECTED_TEXT
            else:
                appearance_dir = strip_dir_string_to_max_length(self.settings['appearance dir'],
                                                                MAX_APPEARANCEDIR_STRING_LENGTH)
                self.appearance_dir_frame.appearance_dir_button.configure(
                    relief=tk.SUNKEN)
        else:
            appearance_dir = NO_FILE_SELECTED_TEXT
            self.settings['appearance dir'] = ""
        self.appearance_dir_frame.appearance_dir_label.configure(
            text=appearance_dir)

    def use_recursive_directory_search(self, choice):
        """ Called by the use recursive directory button in the app. Depending on the choice, sinks the GUI button
            pressed and raises the other and keeps track of the choice in settings. """
        self.settings['recursive directory search'] = choice
        if choice:
            self.options_frame.recursive_directory_search_yes_button.configure(
                relief=tk.SUNKEN)
            self.options_frame.recursive_directory_search_no_button.configure(
                relief=tk.RAISED)
        else:
            self.options_frame.recursive_directory_search_yes_button.configure(
                relief=tk.RAISED)
            self.options_frame.recursive_directory_search_no_button.configure(
                relief=tk.SUNKEN)
        self.options_frame.recursive_directory_search_yes_button.update()
        self.options_frame.recursive_directory_search_no_button.update()
        self.generator.clear_data_with_all_appearances()
        self.generator.fill_data_with_all_appearances()
        self.update_found_labels()

    def press_child_template_button(self, gender):
        """ Sinks the GUI button for the gender chosen/pressed (female, male, futa) and raises the other buttons. """
        all_genders = ['Female', 'Male', 'Futa']
        remaining_genders = [g for g in all_genders if g != gender]
        if gender in all_genders:
            self.child_template_frame.child_template_button[gender].configure(
                relief=tk.SUNKEN)
        for remaining in remaining_genders:
            self.child_template_frame.child_template_button[remaining].configure(
                relief=tk.RAISED)

    def create_template_labeltext(self, filename):
        """ Returns a formatted label text for a given Appearance file with
            PATH_TO/NAME_OF_APPEARANCE.vap as format """

        template_gender = get_appearance_gender(load_appearance(filename))
        label_txt = os.path.basename(filename)[7:-4]
        self.child_template_frame.child_template['gender'] = template_gender
        return label_txt

    def track_threshold_change(self, var, index, mode):
        """ Keeps track if the user changes the morph threshold value in the GUI.
            If so, validity of the entry is checked. GUI is also updated depending
            on validity, using update_XYZ calls """
        string = self.options_frame.threshold_entry.get()
        try:
            value = float(string)
            if 0.0 <= value < 1.0:
                self.settings['morph threshold'] = value
                self.update_found_labels()
                self.update_initialize_population_button()
            else:
                if 'morph threshold' in self.settings:
                    del self.settings['morph threshold']
                self.update_found_labels()
                self.update_initialize_population_button()
                return
        except ValueError:
            if 'morph threshold' in self.settings:
                del self.settings['morph threshold']
            self.update_found_labels()
            self.update_initialize_population_button()
            return

        for i in range(1, POP_SIZE + 1):
            self.update_morph_info(i)

    def track_min_morph_change(self, var, index, mode):
        """ Keeps track if the user changes the min morph value in the GUI.
            If so, validity of the entry is checked. GUI is also updated depending
            on validity, using update_XYZ calls """
        string = self.options_frame.min_morph_entry.get()
        try:
            value = int(string)
            self.settings['min morph threshold'] = value

            # also update the morph info on Chosen Files
            for i in range(1, POP_SIZE + 1):
                self.update_morph_info(i)
            self.update_found_labels()
            self.update_initialize_population_button()

        except ValueError:
            if 'min morph threshold' in self.settings:
                del self.settings['min morph threshold']
            self.update_found_labels()
            self.update_initialize_population_button()
            return

    def update_found_labels(self):
        """ Depending on the choice for the source files, updates the GUI """
        if 'source files' in self.settings:
            if self.settings['source files'] == CHOOSE_ALL_FAVORITES_TEXT:
                self.update_favorites_found_label()
            elif self.settings['source files'] == CHOOSE_ALL_TEXT:
                self.update_all_appearances_found_label()

    def update_all_appearances_found_label(self):
        """ Counts the amount of appearance available in the default VAM directory and updates the GUI """
        filenames = self.get_all_appearance_filenames()
        self.favorites_frame.favorites_info.configure(
            text=f'{len(filenames)} appearances found')
        self.update_initialize_population_button()
        self.favorites_frame.favorites_label.configure(
            text="Step 5: All Appearances Chosen")

    def update_favorites_found_label(self):
        """ Counts the amount of favorite appearances available in the default VAM directory and updates the GUI """
        filenames = self.get_fav_appearance_filenames()
        self.favorites_frame.favorites_info.configure(
            text=f'{len(filenames)} favorite appearances found')
        self.favorites_frame.favorites_label.configure(
            text="Step 5: All Favorite Appearances Chosen")
        self.update_initialize_population_button()

    def choose_all_appearances(self):
        """ Called when the "choose all appearances" button is pressed. Sinks the corresponding GUI button and raises
            the other options. Updates GUI. Saves choice in settings. """
        self.parent_selection_frame.grid_remove()
        self.favorites_frame.grid()
        self.source_files_frame.all_appearances_button.configure(
            relief=tk.SUNKEN)
        self.source_files_frame.all_favorites_button.configure(
            relief=tk.RAISED)
        self.source_files_frame.choose_files_button.configure(relief=tk.RAISED)
        self.settings['source files'] = CHOOSE_ALL_TEXT
        self.update_found_labels()

    def choose_all_favorites(self):
        """ Called when the "choose all favorite" appearances button is pressed. Sinks the corresponding GUI button and
            raises the other options. Updates GUI. Saves choice in settings. """
        self.parent_selection_frame.grid_remove()
        self.favorites_frame.grid()
        self.source_files_frame.all_appearances_button.configure(
            relief=tk.RAISED)
        self.source_files_frame.all_favorites_button.configure(
            relief=tk.SUNKEN)
        self.source_files_frame.choose_files_button.configure(relief=tk.RAISED)
        self.settings['source files'] = CHOOSE_ALL_FAVORITES_TEXT
        self.update_found_labels()

    def choose_files(self):
        """ Called when the choose files button is pressed. Sinks the corresponding GUI button and raises
            the other options. Updates GUI. Saves choice in settings. """
        self.parent_selection_frame.grid()
        self.favorites_frame.grid_remove()
        self.source_files_frame.all_appearances_button.configure(
            relief=tk.RAISED)
        self.source_files_frame.all_favorites_button.configure(
            relief=tk.RAISED)
        self.source_files_frame.choose_files_button.configure(relief=tk.SUNKEN)
        self.settings['source files'] = CHOOSE_FILES_TEXT
        self.update_initialize_population_button()

    def select_file(self, number):
        """ Called when Choose Files is chosen and one of the 20 parent buttons is pressed. Number is the parent number.
            Will immediately return (do nothing) if there is no child template available. If child is available, will
            show a file selection window filtered for matching genders. Updates the GUI with choices and saves to
            settings. """
        if 'gender' in self.child_template_frame.child_template:
            match = matching_genders(
                self.child_template_frame.child_template['gender'])
        else:
            return

        dialog = SelectAppearanceDialog(self.settings, self.generator)
        filename = dialog.file_selection_with_thumbnails(match, "Please select a parent Appearance",
                                                         filteronmorphcount=False)
        dialog.destroy()

        if filename == '':  # user did not select files
            self.remove_parent_file_from_gui(number)
            return

        # user did select a file, which we are now parsing
        self.settings['file ' + str(number)] = filename
        self.update_gui_file(number, filename)

        # stop hiding the apply changes button if we have at least two appearance files available
        self.update_initialize_population_button()
        self.update_morph_info(number)

    def remove_parent_file_from_gui(self, number):
        """ Removes all internal information for a specific parent file for the chosen parent number. Called when
            loading an appearance file for that parent number is cancelled or invalid """

        c = self.population.get_chromosome(number)
        c.filename = ''
        c.short_filename = ''
        c.appearance = None
        c.file_name_display.configure(text=NO_FILE_SELECTED_TEXT)
        c.can_load = False

        if f'file {number}' in self.settings:
            del self.settings['file ' + str(number)]

        self.update_morph_info(number)
        self.update_initialize_population_button()

    def select_vam_dir_callback(self):
        """ Shows filedialog to find the location of the VAM.exe. Choice is validated, GUI updated and settings
            saved. """
        # try to open the file dialog in the last known location
        vam_dir = ''
        if 'VAM base dir' in self.settings:
            if len(self.settings['VAM base dir']) > 0:
                vam_dir = self.settings['VAM base dir']

        folder_path = tk.filedialog.askdirectory(initialdir=vam_dir,
                                                 title="Please select the folder which has the VAM.exe file")
        if os.path.exists(os.path.join(folder_path, 'vam.exe')):
            self.settings['VAM base dir'] = str(pathlib.Path(folder_path))
            self.vam_dir_frame.vam_dir_label.configure(
                text=strip_dir_string_to_max_length(self.settings['VAM base dir'],
                                                    MAX_VAMDIR_STRING_LENGTH))
            self.vam_dir_frame.vam_dir_button.configure(relief=tk.SUNKEN)
            self.track_min_morph_change("", "", "")  # update
            self.generator.clear_data_with_all_appearances()
            self.generator.fill_data_with_all_appearances()
        else:
            self.settings['VAM base dir'] = ""
            self.vam_dir_frame.vam_dir_label.configure(
                text=NO_FILE_SELECTED_TEXT)
            self.vam_dir_frame.vam_dir_button.configure(relief=tk.RAISED)
            self.generator.clear_data_with_all_appearances()

        self.update_initialize_population_button()
        self.update_found_labels()

    def select_appearance_dir_callback(self):
        """ Shows filedialog to select the appearance directory, GUI updated and settings saved. """
        # try to open the file dialog in the last known location
        appearance_dir = ''
        if 'appearance dir' in self.settings:
            if len(self.settings['appearance dir']) > 0:
                appearance_dir = self.settings['appearance dir']

        folder_path = tk.filedialog.askdirectory(initialdir=appearance_dir,
                                                 title="Please select the appearance folder you would like to use.")
        if folder_path == "":
            self.settings['appearance dir'] = ""
            self.appearance_dir_frame.appearance_dir_label.configure(
                text=NO_FILE_SELECTED_TEXT)
            self.appearance_dir_frame.appearance_dir_button.configure(
                relief=tk.RAISED)
            self.generator.clear_data_with_all_appearances()
        else:
            self.settings['appearance dir'] = str(pathlib.Path(folder_path))
            self.appearance_dir_frame.appearance_dir_label.configure(
                text=strip_dir_string_to_max_length(self.settings['appearance dir'],
                                                    MAX_APPEARANCEDIR_STRING_LENGTH))
            self.appearance_dir_frame.appearance_dir_button.configure(
                relief=tk.SUNKEN)
            self.track_min_morph_change("", "", "")  # update
            self.generator.clear_data_with_all_appearances()
            self.generator.fill_data_with_all_appearances()
        self.update_initialize_population_button()
        self.update_found_labels()

    def update_initialize_population_button(self):
        """ Updates the Initialize Population button, by checking if all necessary files and settings are correct. If
            not, shows in the button what items are missing and makes the button do nothing. If criteria are met, button
            color is changed to green and button functionality is restored. """
        can_generate, messages = self.can_generate_new_population()
        if not can_generate:
            messages = '\n'.join(messages)
            txt = f'Cannot Initialize Population:\n{messages}'
            self.generate_children_frame.generate_children_button.configure(relief=tk.RAISED, bg="#D0D0D0",
                                                                            font=(
                                                                                DEFAULT_FONT, 12, "bold"),
                                                                            width=52, height=6,
                                                                            activebackground="#D0D0D0",
                                                                            text=txt,
                                                                            state='disabled')
        else:
            self.generate_children_frame.generate_children_button.configure(relief="raised",
                                                                            bg="lightgreen",
                                                                            font=(
                                                                                DEFAULT_FONT, 12, "bold"),
                                                                            text="Initialize Population",
                                                                            width=52, height=6,
                                                                            state='normal',
                                                                            command=lambda: self.generate_next_population(
                                                                                self.settings['method']))

    def can_generate_new_population(self):
        """ Function which checks all necessary files and settings for generating a new population. Returns a
            message list with all missing features, or an empty list if all criteria are met. """
        can_generate, messages = self.settings.are_settings_valid()
        try:
            if len(self.select_appearances_strategies[self.settings['source files']]()) < 2:
                can_generate = False
                messages.append('· Please have at least 2 Parent files')
        except:
            pass
        return can_generate, messages

    def update_gui_file(self, number, filename):
        """ Updates the Parent file with 'number' with all information available through the 'filename' """
        if filename in self.generator.appearances:
            self.population.get_chromosome(number).update_gui_file(
                filename, self.generator.appearances[filename])

    def select_template_file(self, gender_list, title):
        """ Called by the Female, Male and Futa load template file buttons. Opens a file selection dialogue which
            specifically filters for the gender of the button clicked. The genderlist only has the chosen gender
            as an item. Updates GUI and settings after (un)succesful template selection. """

        dialog = SelectAppearanceDialog(self.settings, self.generator)
        filename = dialog.file_selection_with_thumbnails(
            gender_list, title, filteronmorphcount=False)
        dialog.destroy()

        if filename == "":  # user did not select files
            self.child_template_frame.child_template['label'].configure(
                text=NO_FILE_SELECTED_TEXT)
            self.press_child_template_button(None)
            if 'gender' in self.child_template_frame.child_template:
                del self.child_template_frame.child_template['gender']
            if 'child template' in self.settings:
                del self.settings['child template']
            self.update_initialize_population_button()
            self.update_found_labels()
            return
        self.child_template_frame.child_template['label'].configure(
            text=self.create_template_labeltext(filename))
        self.child_template_frame.child_template['gender'] = self.generator.gender[filename]
        self.press_child_template_button(
            self.child_template_frame.child_template['gender'])
        self.settings['child template'] = filename
        for i in range(1, POP_SIZE + 1):
            self.update_morph_info(i)
        self.update_initialize_population_button()
        self.update_found_labels()

    def press_change_template_file(self, title):
        """ Called by the change template button in the rating windows. Opens a file selection dialogue which
            specifically filters for the gender of the template which is currently being used. If user does not
            select a valid new template file, the old template file is used. """
        dialog = SelectAppearanceDialog(self.settings, self.generator)
        filename = dialog.file_selection_with_thumbnails(
            matching_genders(
                self.child_template_frame.child_template['gender']), title,
            filteronmorphcount=False)
        dialog.destroy()

        if filename == "":  # user did not select files
            return
        self.change_template_file(filename)

    def change_template_file(self, filename):
        """ Called by either the GUI or as a VAM command. Checks if the gender of the chosen file matches the
            current template gender. Updates the GUI. """
        # todo: split, move parts to logic
        self.vam_comm.broadcast_message_to_vam_rating_blocker(
            "Updating...\nPlease Wait")
        # we need to check if the chosen gender matches the gender of the current population (for example:
        # we can't suddenly switch from a male population to a female population or vice versa).
        gender = get_appearance_gender(load_appearance(filename))
        if not is_compatible_gender(gender, self.child_template_frame.child_template['gender']):
            matches = matching_genders(
                self.child_template_frame.child_template['gender'])
            if len(matches) > 1:  # Female and Futa
                select_msg = "Please select a Female or Futa as template."
            else:
                select_msg = "Please select a Male as template."
            self.vam_comm.broadcast_message_to_vam_rating_blocker(
                "Failure: Gender does not match population.\n\n" + select_msg)
            return
        self.change_template_button_label.configure(
            text=os.path.basename(filename)[7:-4])
        self.settings['child template'] = filename
        self.update_population_with_new_template()
        self.vam_comm.broadcast_message_to_vam_rating_blocker("")

    def switch_layout_to_overview(self):
        """ Called when the user has pressed 'Connect to App' in VAM (resulting in a 'Connect to App' command to this
            app). This method removes the 'please start the vam app' dialogue, and replaces it with an overview window
            showing the user the last five commands received, from the VAM companion save. """
        self.vam_comm.broadcast_generation_number_to_vam(
            self.generator.gen_counter)
        print("VAM is ready, let's go.")
        print("Switching view")
        for widget in self.master.winfo_children():
            widget.grid_forget()

        self.overview_frame = OverviewFrame(self.generator.gen_counter,
                                            self.create_template_labeltext(self.settings['child template']))
        self.overview_frame.grid(
            row=0, column=0, padx=10, pady=0, sticky="nsew")

        self.last_commands_frame = LastCommandsFrame()
        self.last_commands_frame.grid(
            row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")

        print("Resetting ratings")
        self.population.reset_ratings()
        print("Sending generation number")
        self.vam_comm.broadcast_generation_number_to_vam(
            self.generator.gen_counter)
        self.vam_comm.broadcast_message_to_vam_rating_blocker("")

    def update_overview_window(self):
        """ Updates the overview window with generation, template and last five commands information """
        self.overview_frame.generation_number_label.config(
            text=self.generator.gen_counter)
        self.overview_frame.template_file_label.config(
            text=self.create_template_labeltext(self.settings['child template']))
        self.last_commands_frame.commands_label.config(
            text=last_given_commands_to_string(self.generator.last_five_commands))

    def variate_population_with_templates(self):
        """ Replaces all the chromosomes in the population with a randomly chosen templates from all the available
            templates """
        print('variate_population_with_templates')
        self.vam_comm.broadcast_message_to_vam_rating_blocker(
            'Updating...\nPlease Wait')

        filenames = list(self.generator.appearances.keys())
        random.shuffle(filenames)
        filename_generator = generate_list_element(filenames)

        appearance_templates = list()
        for filename in filename_generator:
            if len(appearance_templates) >= POP_SIZE:
                break
            appearance = load_appearance(filename)
            gender = get_appearance_gender(appearance)
            if gender == self.child_template_frame.child_template['gender']:
                appearance_templates.append(appearance)

        for c in self.population.chromosomes:
            morph_list = get_morph_list_from_appearance(
                load_appearance(c.filename))
            updated_appearance = save_morph_to_appearance(
                morph_list, appearance_templates[c.index])
            nude_appearance = remove_clothing_from_appearance(
                updated_appearance)
            save_appearance(nude_appearance, c.filename)

        self.vam_comm.broadcast_message_to_vam_rating_blocker('')

    def update_population_with_new_template(self):
        """ Replaces the template of all the current Children with the new one but keeps the morphs values the same. """
        template_appearance = load_appearance(self.settings['child template'])
        for c in self.population.chromosomes:
            morph_list = get_morph_list_from_appearance(
                load_appearance(c.filename))
            updated_appearance = save_morph_to_appearance(
                morph_list, template_appearance)
            save_appearance(updated_appearance, c.filename)

    def filter_filename_list_on_morph_threshold_and_min_morphs(self, filenames):
        """ For a given list of filenames returns a list of filenames which meet the morph and min morph thresholds.
            Returns an empty list if neither of these settings are available. """
        # todo: to logic

        if 'morph threshold' not in self.settings:
            return list()

        if 'min morph threshold' not in self.settings:
            return list()

        filtered = list()
        for f in filenames:
            appearance = self.generator.appearances[f]
            morph_list = get_morph_list_from_appearance(appearance)
            morph_list = filter_morphs_below_threshold(
                morph_list, self.settings['morph threshold'])
            if len(morph_list) > self.settings['min morph threshold']:
                filtered.append(f)
        return filtered

    def update_morph_info(self, number):
        """ Updates morph info in the GUI for Parent file 'number'. """
        # todo: much of this belongs into BL?
        threshold = self.settings['morph threshold']
        if threshold == "":
            threshold = 0
        else:
            threshold = float(threshold)

        if 'gender' in self.child_template_frame.child_template:
            template_gender = self.child_template_frame.child_template['gender']
        else:
            template_gender = ""

        c = self.population.get_chromosome(number)
        if c.filename != '':
            gender = get_appearance_gender(load_appearance(c.filename))
            if not is_compatible_gender(gender, template_gender):
                self.hide_parent_file_from_view(
                    number)  # hide, but don't delete, in case template later has matching gender
                return

            morph_list_tmp = copy.deepcopy(
                get_morph_list_from_appearance(c.appearance))
            morph_list_tmp = filter_morphs_below_threshold(
                morph_list_tmp, threshold)
            number_of_morphs = str(len(morph_list_tmp))
            if int(number_of_morphs) < self.settings['min morph threshold']:
                if self.generator.gen_counter == 0:  # only do this in the initialization selection step
                    self.hide_parent_file_from_view(number)
                    return
            else:
                if self.generator.gen_counter == 0:  # only do this in the initialization selection step
                    c.file_name_display.configure(text=c.short_filename)
                    c.can_load = True
        else:
            number_of_morphs = "N/A"
        # after the app is initialized, the morph information is not being shown anymore
        if self.generator.gen_counter == 0:
            c.n_morph_display.configure(text=str(number_of_morphs))

    def hide_parent_file_from_view(self, number):
        """ Replaces the file label of the parent file #number with '...'  and 'N/A' but keeps the file info
            dictionary """
        c = self.population.chromosomes[number]
        c.file_name_display.configure(text=NO_FILE_SELECTED_TEXT)
        c.n_morph_display.configure(text='N/A')
        c.can_load = False

    def restart_population(self, method):
        """ Reinitializes the population. Can be called whenver the app is in the rating mode.
            Generation counter is reset to 1. """
        # todo: split into GUI and BL
        print(f'Restarting, with {method}')
        self.vam_comm.broadcast_message_to_vam_rating_blocker(
            'Updating...\nPlease Wait')

        # If the user used CHOOSE_FILES_TEXT as the source, we have to reload them into the chromosomes
        # since the chromosomes now contain the Evolutionary Children files at this stage. Only the
        # files which were saved to settings are loaded into the chromosomes. There is no need to
        # delete the other chromosomes (which contain the Evolutionary Child filenames), because
        # they all have a False flag for self.chromosome[str(i)]['can load'] which is used
        # later on in Gaussian and Crossover generation to skip loading them.
        if self.settings['source files'] == CHOOSE_FILES_TEXT:
            for c in self.population.chromosomes:
                filename = f'file {str(c.index)}'
                if filename in self.settings:
                    if len(self.settings[filename]) > 0:
                        c.filename = self.settings[filename]

        if method == 'Gaussian Samples':
            self.gaussian_initialize_population(
                source_files=self.settings['source files'])
        elif method == "Random Crossover":
            self.crossover_initialize_population(self.settings['source files'])
        self.generator.gen_counter = 1
        self.title_frame.title_label.configure(
            text="Generation " + str(self.generator.gen_counter))
        self.population.reset_ratings()
        self.vam_comm.broadcast_message_to_vam_rating_blocker("")

    def generate_next_population(self, method):
        """ Generates the next population. Switches GUI layout to the Ratings layout when called for the first time
            (self.generator.gencounter == 0). Updates the population in the GUI through self.update_population(). """
        # todo: split to put stuff ino logic
        print(method)
        if self.generator.gen_counter == 0:
            # in case of a bug we want to have the settings saved before we start the algorithm
            self.settings.save()
            if method == 'Gaussian Samples':
                self.gaussian_initialize_population(
                    source_files=self.settings['source files'])
            elif method == 'Random Crossover':
                self.crossover_initialize_population(
                    self.settings['source files'])
            self.change_parent_to_generation_display()
            self.switch_layout_to_rating()
            self.population.reset_ratings()
            self.change_gui_to_show_user_to_start_vam()
            self.vam_comm.scan_vam_for_command_updates('Initialize')
            return

        self.vam_comm.broadcast_message_to_vam_rating_blocker(
            'Updating...\nPlease Wait')

        # Start the new population with the elites from the last generation (depending on settings)
        elites = self.get_elites_from_population()

        # Save elite appearances over child template (we do this, becau^1se the user might have changed the template
        # file)
        elite_morph_lists = [get_morph_list_from_appearance(
            appearance) for appearance in elites if appearance]
        template_appearance = load_appearance(self.settings['child template'])
        new_population = [save_morph_to_appearance(elite_morph_list, template_appearance)
                          for elite_morph_list in elite_morph_lists]

        for i in range(POP_SIZE - len(new_population)):
            random_parents = self.population.weighted_random_selection()
            child_appearance = fuse_characters(random_parents[0].filename, random_parents[1].filename,
                                               self.settings)
            new_population.append(child_appearance)
        self.save_population(new_population)
        self.update_population(new_population)

        self.generator.gen_counter += 1
        self.settings['generation counter'] = self.generator.gen_counter
        self.title_frame.title_label.configure(
            text=f'Generation {self.generator.gen_counter}')
        self.population.reset_ratings()
        self.vam_comm.broadcast_message_to_vam_rating_blocker('')
        self.settings.save()

    def change_gui_to_show_user_to_start_vam(self):
        """ After initialization this method is called, to remove all the setup widgets and replace them with a window
            asking the user to load the VAM Companion Save. """
        for widget in self.master.winfo_children():
            widget.grid_forget()
        self.messageframe = tk.Frame(self.master, bg=BG_COLOR)
        self.messageframe.grid(row=0, column=1, padx=10, pady=0, sticky='nsew')
        self.messagelabel = tk.Label(self.messageframe, text='App is ready. \nPlease start VAM, load the',
                                     font=(DEFAULT_FONT, 14, ''), bg=BG_COLOR, fg=FG_COLOR)
        self.messagelabel.pack(side=tk.TOP)
        self.messagelabel = tk.Label(self.messageframe, text='VAM Evolutionary Character Creation Companion',
                                     font=(DEFAULT_FONT, 14, 'italic'), bg=BG_COLOR, fg=FG_COLOR)
        self.messagelabel.pack(side=tk.TOP)
        self.messagelabel = tk.Label(self.messageframe, text='save, and click on "Connect to App"',
                                     font=(DEFAULT_FONT, 14, ''), bg=BG_COLOR, fg=FG_COLOR)
        self.messagelabel.pack(side=tk.TOP)
        self.warning_label = tk.Label(self.messageframe, text='\nImportant: do NOT close this window.\n ',
                                      font=(DEFAULT_FONT, 14, 'bold'), bg=BG_COLOR, fg='red')
        self.warning_label.pack(side=tk.TOP)
        self.lastmessagelabel = tk.Label(self.messageframe,
                                         text='This app needs to stay active to communicate with VAM.',
                                         font=(DEFAULT_FONT, 14, ''), bg=BG_COLOR, fg=FG_COLOR)
        self.lastmessagelabel.pack(side=tk.TOP)

    def continue_last_session(self):
        """ Skip choosing the settings and continue from the last session. This only means switching the layout to
            the rating window and setting the generation counter to the last known value. """
        path = self.settings.get_vam_default_appearance_path()
        save_path = os.path.join(path, SAVED_CHILDREN_PATH)

        for c in self.population.chromosomes:
            filename = os.path.join(
                save_path, f'Preset_{CHILDREN_FILENAME_PREFIX}{c.index}.vap')
            c.filename = filename
            c.appearance = load_appearance(filename)

        self.change_parent_to_generation_display()
        self.switch_layout_to_rating()
        self.population.reset_ratings()
        self.generate_children_frame.generate_children_button.configure(
            text='Generate Next Population')
        self.change_gui_to_show_user_to_start_vam()
        self.vam_comm.scan_vam_for_command_updates("Initialize")

    def execute_vam_command_callback(self, command):
        # todo: candidate for logic
        """ Tries to parse a command string to execute coming from scan_vam_for_command_updates. These
            command strings are generated by the VAM Evolutionary Character Creation Companion save file,
            and always have either the format:
                "Child 12; Rate 4"
            or
                "Generate Next Population"
            """
        if self.generator.connected_to_VAM:
            # add command to last five commands
            command_dict = {}
            now = datetime.now()
            time_string = now.strftime('%d-%m-%Y %H:%M:%S')
            command_dict['time'] = time_string
            command_dict['command'] = command
            self.generator.last_five_commands.insert(0, command_dict)
            if len(self.generator.last_five_commands) > 5:
                self.generator.last_five_commands.pop()
            self.update_overview_window()

        # parse rate child commands
        commands = command.split(';')
        commands = [x.strip() for x in commands]
        if 'child' in commands[0].lower() and 'rate' in commands[1].lower():
            child = commands[0].split(" ")
            child = int(child[1])
            rating = commands[1].split(" ")
            rating = int(rating[1])
            self.population.get_chromosome(child).update_rating(rating)
        # the random number in commands[1] for the if statements below are not used in any way by this script, except
        # to make sure that in case the user wants to do the same command twice, the lastcommand != command in
        # scan_vam_for_command_updates() sees the commands as different (due to the random numbers in commands[1])
        elif 'use template' in commands[0].lower():
            filename = self.settings.get_vam_path(commands[1])
            # use uniform filename formatting
            filename = str(pathlib.Path(filename))
            self.change_template_file(filename)
        elif 'variate population' in commands[0].lower():
            self.variate_population_with_templates()
        elif 'connect to app' in commands[0].lower():
            self.generator.connected_to_VAM = True
            self.population.reset_ratings()
            self.switch_layout_to_overview()
        elif 'generate next population' in commands[0].lower():
            self.generate_next_population(self.settings['method'])
            self.vam_comm.broadcast_generation_number_to_vam(
                self.generator.gen_counter)
        elif 'reset' in commands[0].lower():
            # in the case of a reset we immediately send the "Reset" command back to VAM to avoid a
            # "Connection Lost" in VAM, since the initialization of a new generation (with the Gaussian Method)
            # takes more than the 5 second Connection-check-timeout in VAM.
            self.press_restart_button(give_warning=False)
            self.vam_comm.broadcast_generation_number_to_vam(
                self.generator.gen_counter)

        if self.generator.connected_to_VAM:
            self.update_overview_window()

    def switch_layout_to_rating(self):
        """ Switches the layout from the GUI from the Initialization Choices layout to the rate children layout. Called
            by generate_next_population when called for the first time. """
        self.vam_dir_frame.grid_remove()
        self.appearance_dir_frame.grid_remove()
        self.child_template_frame.grid_remove()
        self.source_files_frame.grid_remove()
        self.method_frame.grid_remove()
        self.parent_selection_frame.grid()
        self.parent_selection_frame.chromosome_label.configure(
            text='Rate Children')
        self.favorites_frame.grid_remove()
        self.options_frame.grid_remove()

    def get_elites_from_population(self):
        """ Returns the children appearances where the rating is the maximum rating that the user selected.
            If the maximum selected rating is lower than MINIMAL_RATING_FOR_KEEP_ELITES, then no appearances are
            returned. Returns a maximum of appearances equal to user setting 'max kept elites'. """
        # todo: candidate for logic

        max_selected_rating = max(
            c.rating for c in self.population.chromosomes)
        if max_selected_rating < MINIMAL_RATING_FOR_KEEP_ELITES:
            return list()

        # Select all appearances with maximum rating.
        appearances_with_maximum_rating = [c.appearance for c in self.population.chromosomes
                                           if c.rating == max_selected_rating]

        # Limit the list of appearances to a maximum of 'max kept elites' elements and return it.
        return appearances_with_maximum_rating[:self.settings['max kept elites']]

    def get_appearance_filenames(self, get_only_favorites):
        """ Returns a list of all appearance files in the default VAM Appearance directory, after gender and morph
            filters are applied. """
        filenames = list()
        if get_only_favorites:
            filenames = [
                f for f, app in self.generator.appearances.items() if is_favorite(app)]
        else:
            filenames = list(self.generator.appearances.keys())
        filenames = [f for f in filenames if CHILDREN_FILENAME_PREFIX not in f]

        if 'gender' in self.child_template_frame.child_template:
            filenames = self.generator.filter_filename_list_on_genders(filenames,
                                                                       matching_genders(
                                                                           self.child_template_frame.child_template[
                                                                               'gender']))
            filtered = self.filter_filename_list_on_morph_threshold_and_min_morphs(
                filenames)
        else:
            filtered = []
        return filtered

    def get_all_appearance_filenames(self):
        # todo: candidate for logic
        return self.get_appearance_filenames(get_only_favorites=False)

    def get_fav_appearance_filenames(self):
        # todo: candidate for logic
        return self.get_appearance_filenames(get_only_favorites=True)

    def get_selected_appearance_filenames(self):
        filenames = [
            c.filename for c in self.population.chromosomes if c.can_load]
        self.filter_filename_list_on_morph_threshold_and_min_morphs(filenames)
        return filenames

    def crossover_initialize_population(self, source_files):
        """ Initializes the population using random crossover between all Parent files. Only used for initialization.
            Updates population info and the GUI. """
        print('Using random pairwise chromosome crossover for sample initialization.')
        parent_filenames = self.select_appearances_strategies[source_files]()
        print(f'Source files: {source_files} ({len(parent_filenames)} Files)')
        new_population = list()
        for i in range(1, POP_SIZE + 1):
            random_parents = random.sample(parent_filenames, 2)
            child_appearance = fuse_characters(
                random_parents[0], random_parents[1], self.settings)
            new_population.append(child_appearance)
        self.save_population(new_population)
        self.generator.gen_counter += 1
        self.update_population(new_population)
        self.generate_children_frame.display_ready_for_new_generation()

    def gaussian_initialize_population(self, source_files):
        # todo: split the UI and the BL parts
        """ Initializes the population using Gaussian Samples based on all Parent files. Only used for initialization.
            Updates population info and the GUI. """
        print('Using random samples from multivariate gaussian distribution for initialization.')
        self.generate_children_frame.display_progress(
            'Generating Population\n Please be patient!\n')

        # select source files
        filenames = self.select_appearances_strategies[source_files]()
        appearances = [self.generator.appearances[f] for f in filenames]
        print(f"Source files: {source_files} ({len(appearances)} Files)")
        morph_lists = [get_morph_list_from_appearance(
            appearance) for appearance in appearances]
        morph_names = get_all_morph_names_in_morph_lists(morph_lists)
        morph_lists = pad_morph_names_to_morph_lists(
            morph_lists, morph_names, filenames)
        morph_lists = dedupe_morphs(morph_lists)
        means = get_means_from_morphlists(morph_lists)
        means = list(means.values())
        covariances = get_cov_from_morph_lists(morph_lists)
        new_population = list()
        template_file = self.settings['child template']
        threshold = self.settings['morph threshold']

        for i in range(1, POP_SIZE + 1):
            text = f'Generating Population\nPlease be patient!\n({i}/{POP_SIZE})'
            self.generate_children_frame.display_progress(text)
            self.vam_comm.broadcast_message_to_vam_rating_blocker(text)

            sample = np.random.default_rng().multivariate_normal(means, covariances)
            sample = [str(x) for x in sample]
            new_morph_list = copy.deepcopy(morph_lists[0])
            for j, morph in enumerate(new_morph_list):
                morph['value'] = sample[j]
            new_morph_list = filter_morphs_below_threshold(
                new_morph_list, threshold)
            child_appearance = load_appearance(template_file)
            print('Using as appearance template:', template_file)
            child_appearance = save_morph_to_appearance(
                new_morph_list, child_appearance)
            new_population.append(child_appearance)

        self.save_population(new_population)
        self.generator.gen_counter += 1
        self.update_population(new_population)
        self.generate_children_frame.display_ready_for_new_generation()
        return

    def save_population(self, population):
        """ save a population list of child appearances to files """
        path = self.settings.get_vam_default_appearance_path()
        save_path = os.path.join(path, SAVED_CHILDREN_PATH)
        pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)
        for i, child_appearance in enumerate(population):
            save_filename = os.path.join(
                save_path, 'Preset_' + CHILDREN_FILENAME_PREFIX + str(i + 1) + '.vap')
            save_appearance(child_appearance, save_filename)
        return True

    def update_population(self, new_appearances):
        """ update all chromosome appearances with the list of child appearance in population """
        path = self.settings.get_vam_default_appearance_path()
        save_path = os.path.join(path, SAVED_CHILDREN_PATH)
        pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)
        for chromosome, appearance in zip(self.population.chromosomes, new_appearances):
            chromosome.update_appearance(appearance, save_path)

    def change_parent_to_generation_display(self):
        """ Changes the Parent """
        self.title_frame.title_label.configure(
            text='Generation ' + str(self.generator.gen_counter))
        for i in [1, 2, 3]:
            self.parent_selection_frame.column_info[str(i)].destroy()

        self.title_restart_button = tk.Button(self.title_frame, text='Restart', anchor=tk.E, bg=BUTTON_BG_COLOR,
                                              fg=BUTTON_FG_COLOR, relief=tk.RAISED,
                                              command=lambda: self.press_restart_button())
        self.title_restart_button.grid(
            columnspan=10, row=0, column=1, sticky=tk.E)

        self.change_template_frame = tk.Frame(self.master, bg=BG_COLOR)
        self.change_template_frame.grid(
            row=7, column=1, padx=(10, 0), pady=(5, 0), sticky=tk.W)
        self.change_template_button = tk.Button(self.change_template_frame, text='Change template', anchor=tk.W,
                                                bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, relief=tk.RAISED,
                                                command=lambda: self.press_change_template_file(
                                                    'Please Select Parent Template'))
        self.change_template_button.grid(row=0, column=0, sticky=tk.W)

        label_txt = os.path.basename(self.settings['child template'])[7:-4]
        self.change_template_button_label = tk.Label(self.change_template_frame, text=label_txt, width=14, anchor='w',
                                                     font=FILENAME_FONT, bg=BG_COLOR, fg=FG_COLOR)
        self.change_template_button_label.grid(
            row=0, column=1, sticky=tk.W, padx=0)
        self.generate_children_frame.generate_children_button.configure(
            width=27, height=6)
        for c in self.population.chromosomes:
            c.destroy_ui()
            c.initialize_rating_buttons(self.parent_selection_frame)

    def press_restart_button(self, give_warning=True):
        if give_warning:
            answer = messagebox.askquestion('Warning!',
                                            'Warning! This will reset all your current progress, ' +
                                            'reinitialize the app and restart with a (newly generated) Generation 1. ' +
                                            'Are you sure?')
            if answer == "no":
                return False
        print('We are restarting')
        self.restart_population(self.settings['method'])
        return True


if __name__ == '__main__':
    print(
        f'I am just a module, please launch the main script "{MAIN_SCRIPT_NAME}".')
