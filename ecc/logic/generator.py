"""
Business logic for VAM Evolutionary Character Creation
By Pino Sante
Please credit me if you change, use or adapt this file.
"""

import glob
import pathlib

from PIL import ImageTk, Image, UnidentifiedImageError

from .tools import *


class Generator:
    def __init__(self, settings):
        self.settings = settings
        self.gen_counter = 0
        self.appearances = dict()
        self.gender = dict()
        self.thumbnails = dict()
        self.last_five_commands = list()
        self.connected_to_VAM = False

    def clear_data_with_all_appearances(self):
        """ Clears the data stored in the data dictionaries. This is called when loading the VAM
            directory fails, to delete old data. """
        self.appearances.clear()
        self.thumbnails.clear()
        self.gender.clear()

    def fill_data_with_all_appearances(self):
        """ Loads all available presets found in the default VAM directory into dictionaries
            to save loading-times when using the app """
        path = self.settings['appearance dir']

        if self.settings['recursive directory search']:
            filenames = glob.glob(os.path.join(path, "**", "Preset_*.vap"), recursive=True)
        else:
            filenames = glob.glob(os.path.join(path, "Preset_*.vap"), recursive=False)

        for f in filenames:
            f = str(pathlib.Path(f))  # since we use path names as keys, we need to have a uniform formatting
            appearance = load_appearance(f)
            if get_morph_index_with_character_info_from_appearance(appearance) is None:
                # just calling this function since it looks for morphs
                print(f"File {f} is not a valid Appearance file, skipping.")
            else:
                f_fav = f + '.fav'
                appearance['is_fav'] = os.path.isfile(f_fav)
                if appearance['is_fav']:
                    print(f"###### is_fav = {appearance['is_fav']} {f_fav}")
                self.appearances[f] = appearance
                # print(f"Loading file {f} into database.")
                self.thumbnails[f] = self.get_thumbnail_for_filename(f)
                self.gender[f] = get_appearance_gender(self.appearances[f])

    # to do: does this belong into GUI?
    @staticmethod
    def get_thumbnail_for_filename(filename):
        """ Returns the corresponding thumbnail as a tk.Image for a given Appearance file with
            PATH_TO/NAME_OF_APPEARANCE.vap as format """
        thumbnail_path = os.path.splitext(filename)[0] + '.jpg'
        if not os.path.exists(thumbnail_path):
            thumbnail_path = os.path.join(DATA_PATH, NO_THUMBNAIL_FILENAME)

        image = None
        jpg_loaded = False
        try:
            image = Image.open(thumbnail_path)
            jpg_loaded = True
        except UnidentifiedImageError as e:
            print(f'*** Warning! {e}')
            print(f'*** The thumbnail file cannot be read, using dummy image instead.')

        if not jpg_loaded:
            try:
                thumbnail_path = os.path.join(DATA_PATH, NO_THUMBNAIL_FILENAME)
                image = Image.open(thumbnail_path)
            except Exception as e:
                print(f'*** Error! {e}')

        image = image.resize(THUMBNAIL_SIZE, Image.ANTIALIAS)
        thumbnail = ImageTk.PhotoImage(image)
        return thumbnail

    def filter_filename_list_on_genders(self, filenames, genderlist):
        """ For a give list of filenames, filters on gender. """
        filtered = []
        for f in filenames:
            gender = self.gender[f]
            if gender:
                if gender in genderlist:
                    filtered.append(f)
        return filtered


if __name__ == '__main__':
    print(f'I am just a module, please launch the main script "{MAIN_SCRIPT_NAME}".')
