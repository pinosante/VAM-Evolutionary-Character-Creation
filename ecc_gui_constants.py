import ecc_utility


ICON_FILENAME = "VAM Evolutionary Character Creation.ico"
APP_TITLE = "VAM Evolutionary Character Creation by Pino Sante"
NO_FILE_SELECTED_TEXT = "…"
SAVED_CHILDREN_PATH = "VAM Evolutionary Character Creation"
CHILDREN_FILENAME_PREFIX = "Evolutionary_Child_"
MINIMAL_RATING_FOR_KEEP_ELITES = 2
DEFAULT_MAX_KEPT_ELITES = 1
DEFAULT_FONT = "Calibri"
FILENAME_FONT = ("Courier", 9)
BG_COLOR = "#F9F9F9"
FG_COLOR = "black"
BUTTON_BG_COLOR = "#ffbeed"
BUTTON_FG_COLOR = "black"
BUTTON_ACTIVE_COLOR = BUTTON_BG_COLOR
HOVER_COLOR = "#f900ff"
MAX_VAMDIR_STRING_LENGTH = 42
MAX_APPEARANCEDIR_STRING_LENGTH = 45
RATING_SUNKEN_BG_COLOR = BUTTON_BG_COLOR
RATING_SUNKEN_FG_COLOR = BUTTON_FG_COLOR
RATING_RAISED_BG_COLOR = BG_COLOR
RATING_RAISED_FG_COLOR = FG_COLOR
RATING_HOVER_BG_COLOR = BUTTON_BG_COLOR
RATING_HOVER_FG_COLOR = BUTTON_FG_COLOR
RATING_ACTIVE_BG_COLOR = BUTTON_BG_COLOR
RATING_ACTIVE_FG_COLOR = BUTTON_FG_COLOR

if __name__ == '__main__':
    print(f'I am just a module, please launch the main script "{ecc_utility.MAIN_SCRIPT_NAME}".')
