"""
Business logic for VAM Evolutionary Character Creation
By Pino Sante
Please credit me if you change, use or adapt this file.
"""

import copy
import glob
import json
import os
import pathlib
import random
import shutil
import time

from PIL import ImageTk, Image, UnidentifiedImageError

THUMBNAIL_SIZE = 184, 184
NO_THUMBNAIL_FILENAME = "no_thumbnail.jpg"
CHILD_THUMBNAIL_FILENAME = "child_thumbnail.jpg"
NO_FILE_SELECTED_TEXT = "…"
SETTINGS_FILENAME = "settings.json"
DATA_PATH = "data"
SAVED_CHILDREN_PATH = "VAM Evolutionary Character Creation"
CHILDREN_FILENAME_PREFIX = "Evolutionary_Child_"
POP_SIZE = 20
MINIMAL_RATING_FOR_KEEP_ELITES = 2
INITIAL_RATING = 3
DEFAULT_MAX_KEPT_ELITES = 1
MAX_VAMDIR_STRING_LENGTH = 42
MAX_APPEARANCEDIR_STRING_LENGTH = 45


class Morph:
    """ replaces the dict based morph data structure.
        What properties has a morph?
        - name
        - uid
        - value
        later (blacklist):
        - is_allowed
        - min_value
        - max_value
    """

    def __init__(self, name='', uid='', value=0.0):
        """ init a Morph object with values
            look, default parameters! :)
        """
        self.name = name if name else ''
        self.uid = uid if uid else ''
        self.value = value if value else 0.0

# sketch


class Appearance:
    # storables
    pass


class Generator:
    def __init__(self, settings):
        self.settings = settings
        self.gencounter = 0
        self.appearances = dict()
        self.gender = dict()
        self.thumbnails = dict()
        self.lastfivecommands = list()
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
        # path = self.get_vam_default_appearance_path()
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
                print(f"Loading file {f} into database.")
                self.thumbnails[f] = self.get_thumbnail_for_filename(f)
                self.gender[f] = get_appearance_gender(self.appearances[f])

    # to do: does this belong into GUI?
    @staticmethod
    def get_thumbnail_for_filename(filename):
        """ Returns the corresponding thumbnail as a tk.Image for a given Appearance file with
            PATH_TO/NAME_OF_APPEARANCE.vap as format """
        thumbnailpath = os.path.splitext(filename)[0] + '.jpg'
        if not os.path.exists(thumbnailpath):
            thumbnailpath = os.path.join(DATA_PATH, NO_THUMBNAIL_FILENAME)

        image = None
        jpg_loaded = False
        try:
            image = Image.open(thumbnailpath)
            jpg_loaded = True
        except UnidentifiedImageError as e:
            print(f'*** Warning! {e}')
            print(f'*** The thumbnail file cannot be read, using dummy image instead.')

        if not jpg_loaded:
            try:
                thumbnailpath = os.path.join(DATA_PATH, NO_THUMBNAIL_FILENAME)
                image = Image.open(thumbnailpath)
            except Exception as e:
                print(f'*** Error! {e}')

        image = image.resize(THUMBNAIL_SIZE, Image.ANTIALIAS)
        thumbnail = ImageTk.PhotoImage(image)
        return thumbnail


def load_appearance(filename):
    """ Loads appearance from filename and returns it, or returns False if the appearance couldn't be loaded """
    if os.path.isfile(filename):
        with open(filename, encoding="utf-8") as f:
            print(f'load_appearance: loading file {filename}')
            return json.load(f)
    return False


def save_appearance(appearance, filename):
    """ Saves the appearance as a json to the filename """
    # The code below is needed in case the user somehow clicks on a number in the companion app
    # exactly at the same time, as this script is trying to save the new generation. This happens very
    # very very rarely, but if it does, it ruins the progress. The code below makes sure to wait a
    # few seconds and try again. The three repeats is a failsafe to avoid looping to eternity.
    for x in range(3):
        try:
            with open(filename, 'w', encoding="utf-8") as json_file:
                print("Writing appearance to:", filename)
                json.dump(appearance, json_file, indent=3)
            # copy a vam character fusion thumbnail as well
            thumbnailpath = os.path.splitext(filename)[0] + '.jpg'
            shutil.copyfile(os.path.join(DATA_PATH, CHILD_THUMBNAIL_FILENAME), thumbnailpath)
            return True
        except Exception as exception:
            print(f'{exception=}')
            print(f"Error while trying to save {filename}, trying again in 2 seconds.")
            time.sleep(2)
    raise Exception(f"Can't save appearance {filename}")


def get_morph_names(morph_list):
    """ returns a list with all morph names found in the list of morphs """
    return [morph.name for morph in morph_list]


def is_morph_name_in_morph_list(morph_name, morph_list):
    """ return True if morph is in morphlist
    to do: should be easy to simplify"""
    for morph in morph_list:
        if morph.name == morph_name:
            return True
    return False


def get_uid_from_morph_name(morph_name, morph_lists, file_names=None):
    """ look through list of morph_lists for morph_name and returns the first found corresponding uid
    to do: refactor after having understood what really could go wrong below"""
    for idx, morph_list in enumerate(morph_lists):
        for morph in morph_list:
            if morph.name == morph_name:
                if morph.uid != '':
                    return morph.uid
                else:
                    if file_names is None:  # this is the case when called from fuse_characters()
                        raise KeyError("Could not find a morph with key 'uid'")
                    else:
                        raise KeyError(f"Could not find a morph with key 'uid' in file: {file_names[idx]}")
    return False


def pad_morph_names_to_morph_lists(morph_lists, morph_names, file_names=None):
    """ adds uid keys to each morph_list in morph_lists and sets the values to 0 if uid key doesn't exist """
    morph_lists = copy.deepcopy(morph_lists)
    for morph_list in morph_lists:
        morphs_to_add = list()
        for morph_name in morph_names:
            if not is_morph_name_in_morph_list(morph_name, morph_list):
                new_morph = Morph(morph_name, get_uid_from_morph_name(morph_name, morph_lists, file_names))
                morphs_to_add.append(new_morph)
        morph_list.extend(morphs_to_add)
    return morph_lists


def intuitive_crossover(morph_list1, morph_list2):
    """ returns a new morph which is the combined morph of morphlist1 and morphlist2 where each gene has 0.5 chance to
        be selected
        reference: https://towardsdatascience.com/unit-3-genetic-algorithms-part-1-986e3b4666d7
        """
    zipped_morphs = zip(morph_list1, morph_list2)
    return [random.choice(morph_pair) for morph_pair in zipped_morphs]


def non_uniform_mutation(morph_list):
    """ select a random gene, and apply non_uniform mutation to it """
    # reference: https://www.geeksforgeeks.org/mutation-algorithms-for-real-valued-parameters-ga/
    morph_list = copy.deepcopy(morph_list)
    random_morph = random.choice(morph_list)
    random_morph.value = calculate_single_mutation(random_morph.value)
    return morph_list


def calculate_single_mutation(value, b=0.5):
    """ Create random mutation based on a value and b """
    r1 = random.random()
    r2 = random.random()

    if r1 >= 0.5:
        return (1.0 - float(value)) * r2 * b
    else:
        return (0.0 + float(value)) * r2 * b


def get_morph_list_from_appearance(appearance):
    """ Based on gender, either returns the morphs or morphsOtherGender from the appearance json """
    gender = get_appearance_gender(appearance)
    if gender == "Futa":
        target_morphs = "morphsOtherGender"
    else:
        target_morphs = "morphs"
    char_index = get_morph_index_with_character_info_from_appearance(appearance)
    return appearance['storables'][char_index][target_morphs]


def get_morph_index_with_character_info_from_appearance(appearance):
    """ Looks through all storables in the appearance, and returns the index which contains the morphs values """
    character_key_found = False
    for dictionary in appearance['storables']:
        if "character" in dictionary:
            character_key_found = True
    if not character_key_found:
        return None
    for index, dictionary in enumerate(appearance['storables']):
        if "morphs" in dictionary and dictionary['id'] == "geometry":
            return index
    return None


def value_from_id_in_dict_list(dict_list, id_string, needed_key):
    for dictionary in dict_list:
        if id_string in dictionary.values():
            if needed_key in dictionary:
                return dictionary[needed_key]
    return None


def replace_value_from_id_in_dict_list(dict_list, id_string, needed_key, replacement_string):
    for dictionary in dict_list:
        if id_string in dictionary.values():
            if needed_key in dictionary:
                dictionary[needed_key] = replacement_string
                return dict_list
    return None


def get_appearance_gender(appearance):
    """ Return the gender of the appearance, or False if it could not be determined """
    # determine futa
    char_index = get_morph_index_with_character_info_from_appearance(appearance)
    morph_list = appearance['storables'][char_index]["morphs"]
    morph_names = [morph.name for morph in morph_list]

    if "MVR_G2Female" in morph_names and appearance['storables'][char_index]['useFemaleMorphsOnMale'] == "true":
        return 'Futa'

    # determine female
    if get_value_for_key_and_id_in_appearance(appearance, 'FemaleAnatomyAlt', 'enabled') == "true" or \
            get_value_for_key_and_id_in_appearance(appearance, 'FemaleAnatomy', 'enabled') == "true" or \
            'Female' in appearance['storables'][char_index]['character']:
        return 'Female'

    # determine male
    if appearance['storables'][char_index]['useFemaleMorphsOnMale'] == "false" and \
            ('Male' in appearance['storables'][char_index]['character'] or
             get_value_for_key_and_id_in_appearance(appearance, 'MaleAnatomy', 'enabled') == "true" or
             get_value_for_key_and_id_in_appearance(appearance, 'MaleAnatomyAlt', 'enabled') == "true"):
        return 'Male'
    return False


def get_value_for_key_and_id_in_appearance(appearance, idx, key):
    """ Loops through the appearance json to match a dictionary with id = idx and then returns the value of ['key'] """
    storables = appearance['storables']
    for item in storables:
        if 'id' in item:
            if item['id'] == idx:
                if key in item:
                    return item[key]
    return False


def remove_clothing_from_appearance(appearance):
    """ Removes the clothing and references to the clothing from the appearance. """
    clothing = list()
    for dictionary in appearance['storables']:
        if dictionary['id'] == 'geometry':
            clothing = dictionary['clothing']
            dictionary['clothing'] = list()
    if len(clothing) == 0:
        return appearance
    ids_to_delete = [item['internalId'] for item in clothing if 'internalId' in item]

    indexes_to_delete = []
    for idx, dictionary in enumerate(appearance['storables']):
        for some_id in ids_to_delete:
            if some_id in dictionary['id']:
                indexes_to_delete.append(idx)
    indexes_to_delete = list(set(indexes_to_delete))
    for index in sorted(indexes_to_delete, reverse=True):
        del appearance['storables'][index]
    return appearance


def save_morph_to_appearance(morph_list, appearance):
    """ Depending on gender, replace the corresponding morph with the morph_list """
    appearance = copy.deepcopy(appearance)
    gender = get_appearance_gender(appearance)
    if gender == "Futa":
        target_morphs = "morphsOtherGender"
    else:
        target_morphs = "morphs"

    char_index = get_morph_index_with_character_info_from_appearance(appearance)
    appearance['storables'][char_index][target_morphs] = morph_list
    return appearance


def dedupe_morphs(morph_lists):
    """ removes duplicate morphs from each morph_list in morph_lists """
    new_morph_lists = []
    for morph_list in morph_lists:
        new_morphs = []
        found = set()
        for morph in morph_list:
            if morph.name not in found:
                found.add(morph.name)
                # to do: is it important to keep order here? otherwise a set would be sufficient
                new_morphs.append(morph)
        new_morph_lists.append(new_morphs)
    return new_morph_lists


def count_morph_values_below_threshold(morph_list, threshold):
    """ checks for each morph in morph_list if the absolut value is below the threshold and returns a count and
        percentage """
    count = 0
    for morph in morph_list:
        if abs(morph.value) < threshold:
            count += 1
    percentage = count / len(morph_list)
    return count, percentage


def filter_morphs_below_threshold(morph_list, threshold):
    """ goes through each morph in each morph_list in the list of morph_lists and only keeps morphs with values above
        threshold """
    return [morph for morph in morph_list if abs(morph.value) >= threshold]


def get_all_morph_names_in_morph_lists(morph_lists):
    """ returns a list of alle morph_names found in the morph_lists """
    morph_names = []
    for morph_list in morph_lists:
        morph_names.extend(get_morph_names(morph_list))
    morph_names = list(dict.fromkeys(morph_names))  # remove duplicates but keep the same order
    return morph_names


def fuse_characters(filename1, filename2, settings):
    """ Load both filename1 and filename2, and do an intuitive crossover between the two, and finally a
        non_uniform_mutation. Returns the child created by these procedures. """
    threshold = settings['morph threshold']
    files = [filename1, filename2]
    morph_lists = []
    for f in files:
        print("Reading appearance:", f)
        appearance = load_appearance(f)
        morph_list = get_morph_list_from_appearance(appearance)
        morph_list = filter_morphs_below_threshold(morph_list, threshold)
        morph_lists.append(morph_list)
    morph_lists = dedupe_morphs(morph_lists)

    morph_names = get_all_morph_names_in_morph_lists(morph_lists)
    morph_lists = pad_morph_names_to_morph_lists(morph_lists, morph_names)

    sorted_morph_lists = []
    for morph_list in morph_lists:
        sorted_morph_lists.append(sorted(morph_list, key=lambda morph: morph.name))

    child_morph_list = intuitive_crossover(sorted_morph_lists[0], sorted_morph_lists[1])
    child_morph_list = non_uniform_mutation(child_morph_list)

    # select child template
    template_file = settings['child template']
    child_appearance = load_appearance(template_file)
    print("Using as appearance template:", template_file)
    child_appearance = save_morph_to_appearance(child_morph_list, child_appearance)
    return child_appearance


def matching_genders(gender):
    """ returns list of matching genders for a given gender (Female, Male, Futa) """
    gender_names = [['Male'], ['Female', 'Futa']]
    for gn in gender_names:
        if gender in gn:
            return gn
    return list()


def can_match_genders(gender1, gender2):
    """ returns True if gender1 (Male, Female, Futa) is compatible with gender2 (Male, Female, Futa) """
    if gender1 == gender2:
        return True
    if gender1 == 'Female' and gender2 == 'Futa':
        return True
    if gender1 == 'Futa' and gender2 == 'Female':
        return True
    return False


if __name__ == '__main__':
    print('I am just a module, please launch the main script "VAM Evolutionary Character Creation.py".')
