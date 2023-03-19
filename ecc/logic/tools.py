"""
Business logic for VAM Evolutionary Character Creation
By Pino Sante
Please credit me if you change, use or adapt this file.
"""

import copy
import random
import shutil
import os
import time
import json

from collections import defaultdict

import numpy as np

from ..common.utility import *


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
            thumbnail_path = os.path.splitext(filename)[0] + '.jpg'
            shutil.copyfile(os.path.join(DATA_PATH, CHILD_THUMBNAIL_FILENAME), thumbnail_path)
            return True
        except Exception as exception:
            print(f'{exception=}')
            print(f"Error while trying to save {filename}, trying again in 2 seconds.")
            time.sleep(2)
    raise Exception(f"Can't save appearance {filename}")


def get_morph_names(morph_list):
    """ returns a list with all morph names found in the list of morphs """
    return [morph['name'] for morph in morph_list]


def is_morph_name_in_morph_list(morph_name, morph_list):
    """ return True if morph is in morph_list """
    return any(morph['name'] == morph_name for morph in morph_list)


def get_uid_from_morph_name(morph_name, morph_lists, filenames=None):
    """ look through list of morph_lists for morph_name and returns the first found corresponding uid """
    for idx, morph_list in enumerate(morph_lists):
        for m in morph_list:
            if m['name'] == morph_name:
                if 'uid' in m:
                    return m['uid']
                else:
                    if filenames is None:  # this is the case when called from fuse_characters()
                        raise KeyError("Could not find a morph with key 'uid'")
                    else:
                        raise KeyError(f"Could not find a morph with key 'uid' in file: {filenames[idx]}")
    return False


def pad_morph_names_to_morph_lists(morph_lists, morph_names, filenames=None):
    """ adds uid keys to each morph_list in morph_lists and sets the values to 0 if uid key doesn't exist """
    morph_lists = copy.deepcopy(morph_lists)

    for morph_list in morph_lists:
        morphs_to_add = []
        for morph_name in morph_names:
            if is_morph_name_in_morph_list(morph_name, morph_list):
                continue
            else:
                new_morph = {
                    'uid': get_uid_from_morph_name(morph_name, morph_lists, filenames),
                    'name': morph_name,
                    'value': '0.0'
                }
                morphs_to_add.append(new_morph)
        morph_list.extend(morphs_to_add)
    return morph_lists


def intuitive_crossover(morph_list1, morph_list2):
    """ returns a new morph which is the combined morph of morph_list1 and morph_list2 where each gene has 0.5 chance to
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
    random_morph['value'] = calculate_single_mutation(random_morph['value'])
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
    if gender == FUTA:
        target_morphs = "morphsOtherGender"
    else:
        target_morphs = "morphs"
    char_index = get_morph_index_with_character_info_from_appearance(appearance)
    return appearance[STORABLES][char_index][target_morphs]


def get_morph_index_with_character_info_from_appearance(appearance):
    """ Looks through all storables in the appearance, and returns the index which contains the morphs values """
    character_key_found = False
    for dictionary in appearance[STORABLES]:
        if "character" in dictionary:
            character_key_found = True
    if not character_key_found:
        return None
    for index, dictionary in enumerate(appearance[STORABLES]):
        if "morphs" in dictionary and dictionary['id'] == "geometry":
            return index
    return None


def uses_female_morphs_on_male(appearance):
    char_index = get_morph_index_with_character_info_from_appearance(appearance)
    return appearance[STORABLES][char_index]['useFemaleMorphsOnMale'] == "true"


def is_anatomy_enabled(appearance, anatomy_key):
    return get_value_for_key_and_id_in_appearance(appearance, anatomy_key, 'enabled') == "true"


def is_female_anatomy(appearance):
    return is_anatomy_enabled(appearance, 'FemaleAnatomy')


def is_alt_female_anatomy(appearance):
    return is_anatomy_enabled(appearance, 'FemaleAnatomyAlt')


def is_male_anatomy(appearance):
    return is_anatomy_enabled(appearance, 'MaleAnatomy')


def is_alt_male_anatomy(appearance):
    return is_anatomy_enabled(appearance, 'MaleAnatomyAlt')


def has_female_text(appearance):
    char_index = get_morph_index_with_character_info_from_appearance(appearance)
    return FEMALE in appearance[STORABLES][char_index]['character']


def has_male_text(appearance):
    char_index = get_morph_index_with_character_info_from_appearance(appearance)
    return MALE in appearance[STORABLES][char_index]['character']


def is_futa(appearance):
    """ determine futa """
    char_index = get_morph_index_with_character_info_from_appearance(appearance)
    morph_list = appearance[STORABLES][char_index]["morphs"]
    morph_names = {morph['name'] for morph in morph_list}
    return "MVR_G2Female" in morph_names and uses_female_morphs_on_male(appearance)


def is_female(appearance):
    """ determine female """
    return is_female_anatomy(appearance) \
        or is_alt_female_anatomy(appearance) \
        or has_female_text(appearance)


def is_male(appearance):
    """ determine male """
    if uses_female_morphs_on_male(appearance):
        return False

    return has_male_text(appearance) \
        or is_male_anatomy(appearance) \
        or is_alt_male_anatomy(appearance)


def get_appearance_gender(appearance):
    """ Return the gender of the appearance, or False if it could not be determined """
    if is_futa(appearance):
        return FUTA

    if is_female(appearance):
        return FEMALE

    if is_male(appearance):
        return MALE

    return False


def get_value_for_key_and_id_in_appearance(appearance, idx, key):
    """ Loops through the appearance json to match a dictionary with id = idx and then returns the value of ['key'] """
    for item in appearance[STORABLES]:
        if 'id' in item:
            if item['id'] == idx:
                if key in item:
                    return item[key]
    return False


def remove_clothing_from_appearance(appearance):
    """ Removes the clothing and references to the clothing from the appearance. """
    clothing = list()
    for dictionary in appearance[STORABLES]:
        if dictionary['id'] == 'geometry':
            clothing = dictionary['clothing']
            dictionary['clothing'] = list()
    if len(clothing) == 0:
        return appearance
    ids_to_delete = [item['internalId'] for item in clothing if 'internalId' in item]

    indexes_to_delete = []
    for idx, dictionary in enumerate(appearance[STORABLES]):
        for id2 in ids_to_delete:
            if id2 in dictionary['id']:
                indexes_to_delete.append(idx)
    indexes_to_delete = list(set(indexes_to_delete))
    for index in sorted(indexes_to_delete, reverse=True):
        del appearance[STORABLES][index]
    return appearance


def save_morph_to_appearance(morph_list, appearance):
    """ Depending on gender, replace the corresponding morph with the morph_list """
    appearance = copy.deepcopy(appearance)
    gender = get_appearance_gender(appearance)
    target_morphs = "morphsOtherGender" if gender == FUTA else "morphs"
    char_index = get_morph_index_with_character_info_from_appearance(appearance)
    appearance[STORABLES][char_index][target_morphs] = morph_list
    return appearance


def dedupe_morphs(morph_lists):
    """ removes duplicate morphs from each morph_list in morph_lists """

    # suggestion from GPT-3.5 -- do not understand yet. :) todo: test
    # return [
    #     [morph for i, morph in enumerate(morph_list) if morph['name'] not in morph_list[:i]]
    #     for morph_list in morph_lists
    # ]

    # another suggestion by GPT-4
    # new_morph_lists = []
    # for morph_list in morph_lists:
    #     found_morphs = {morph['name']: morph for morph in morph_list if morph['name'] not in found_morphs}
    #     new_morph = list(found_morphs.values())
    #     new_morph_lists.append(new_morph)
    # return new_morph_lists

    new_morph_lists = list()
    for morph_list in morph_lists:
        new_morph = list()
        found = list()
        found_morphs = dict()
        for morph in morph_list:
            if morph['name'] not in found:
                found.append(morph['name'])
                found_morphs[morph['name']] = morph
                new_morph.append(morph)
        new_morph_lists.append(new_morph)
    return new_morph_lists


def count_morph_values_below_threshold(morph_list, threshold):
    """ checks for each morph in morph_list if the absolut value is below the threshold and returns a count and
        percentage """
    count = 0
    for morph in morph_list:
        if abs(float(morph['value'])) < threshold:
            count += 1
    percentage = count / len(morph_list)
    return count, percentage


def filter_morphs_below_threshold(morph_list, threshold):
    """ goes through each morph in each morph_list in the list of morph_lists and only keeps morphs with values above
        threshold """
    new_morph_list = []
    for morph in morph_list:
        if 'value' in morph and abs(float(morph['value'])) >= threshold:
            new_morph_list.append(morph)
    return new_morph_list


def get_all_morph_names_in_morph_lists(morph_lists):
    """ returns a list of alle morph_names found in the morph_lists """

    # suggestion ChatGPT, also rename to get_unique_morph_names
    # morph_names = list(set(name for morph_list in morph_lists for name in get_morph_names(morph_list)))
    # return morph_names

    morph_names = list()
    for morph_list in morph_lists:
        morph_names.extend(get_morph_names(morph_list))
    return list(dict.fromkeys(morph_names))  # remove duplicates but keep the same order


def select_child_template(child_morph_list, settings):
    template_file = settings['child template']
    child_appearance = load_appearance(template_file)
    print('Using as appearance template:', template_file)
    child_appearance = save_morph_to_appearance(child_morph_list, child_appearance)
    return child_appearance


def fuse_characters(filename1, filename2, settings):
    """ Load both filename1 and filename2, and do an intuitive crossover between the two, and finally a
        non_uniform_mutation. Returns the child created by these procedures. """
    threshold = settings['morph threshold']
    files = [filename1, filename2]
    morph_lists = list()
    for i, f in enumerate(files):
        print('Reading appearance:', f)
        appearance = load_appearance(f)
        morph_list = get_morph_list_from_appearance(appearance)
        morph_list = filter_morphs_below_threshold(morph_list, threshold)
        morph_lists.append(morph_list)
    morph_lists = dedupe_morphs(morph_lists)

    morph_names = get_all_morph_names_in_morph_lists(morph_lists)
    morph_lists = pad_morph_names_to_morph_lists(morph_lists, morph_names)

    sorted_morph_lists = []
    for morph_list in morph_lists:
        sorted_morph_lists.append(sorted(morph_list, key=lambda d: d['name']))

    child_morph_list = intuitive_crossover(sorted_morph_lists[0], sorted_morph_lists[1])
    child_morph_list = non_uniform_mutation(child_morph_list)

    return select_child_template(child_morph_list, settings)


def matching_genders(gender):
    """ returns list of matching genders for a given gender (Female, Male, Futa) """
    gender_names = [[MALE], [FEMALE, FUTA]]
    for gn in gender_names:
        if gender in gn:
            return gn
    return list()


def is_compatible_gender(gender1, gender2):
    """ returns True if gender1 (Male, Female, Futa) is compatible with gender2 (Male, Female, Futa) """
    if gender1 == gender2:
        return True
    if gender1 == FEMALE and gender2 == FUTA:
        return True
    if gender1 == FUTA and gender2 == FEMALE:
        return True
    return False


def get_means_from_morphlists(morph_lists):
    """ returns a dictionary of morph means for each morph found in the morphlists """
    means = defaultdict(lambda: 0.0)
    for morph_list in morph_lists:
        for morph in morph_list:
            if 'value' in morph:
                means[morph['name']] += np.nan_to_num(float(morph['value'])) * 1 / len(morph_lists)
            else:
                means[morph['name']] += 0 / len(morph_lists)  # just assume missing values to be 0
    return means


def get_cov_from_morph_lists(morphlists):
    """ Returns covariances of all morphlist. Used by the Random Gaussian sample method. """
    values = defaultdict(lambda: [])
    for morph_list in morphlists:
        for morph in morph_list:
            values[morph['name']].append(np.nan_to_num(float(morph['value'])))
    list_of_values = []
    for key, value in values.items():
        list_of_values.append(value)
    covariances = np.array(list_of_values)
    return np.cov(covariances)


def last_given_commands_to_string(list_of_commands):
    """ Converts a list of commands (5) (where each command is dictionary with 'time' and 'command' as keys
        to a string with \n for line separation
        to do: simplify this"""
    # todo: to logic
    string = ''
    for command_dict in list_of_commands:
        line = command_dict['time'] + ': ' + command_dict['command'] + "\n"
        string = string + line
    string = string[:-1]  # remove the extra \n at the end
    return string



if __name__ == '__main__':
    print(f'I am just a module, please launch the main script "{MAIN_SCRIPT_NAME}".')
