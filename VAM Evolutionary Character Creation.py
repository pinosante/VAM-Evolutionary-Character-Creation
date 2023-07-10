"""

By Pino Sante

Please credit me if you change, use or adapt this file.

"""

import os
import tkinter as tk

import ecc.common.utility
from ecc.gui.constants import *
from ecc.common.settings import Settings
from ecc.logic.generator import Generator
from ecc.gui.app_window import AppWindow

from ecc.common.ecc_log import ecc_logger as logger


BG_COLOR = "#F9F9F9"
ICON_FILENAME = "VAM Evolutionary Character Creation.ico"


def main():
    """
    create the business logic and the main window and launch them
    """

    logger.info("launching")

    settings = Settings()
    generator = Generator(settings)

    main_window = tk.Tk()
    main_window.configure(bg=BG_COLOR)
    main_window.option_add("*font", "Calibri 9")
    main_window.iconbitmap(os.path.join(ecc.common.utility.DATA_PATH, ICON_FILENAME))
    main_window.title(APP_TITLE)
    main_window.resizable(False, False)

    app = AppWindow(settings, generator)
    app.initialize()
    main_window.mainloop()

    settings.save()

    logger.info("shutting down")


if __name__ == '__main__':
    main()
