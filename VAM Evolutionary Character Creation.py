"""

By Pino Sante

Please credit me if you change, use or adapt this file.

"""

import os
import tkinter as tk

import ecc_gui
import ecc_logic
import ecc_utility

BG_COLOR = "#F9F9F9"
ICON_FILENAME = "VAM Evolutionary Character Creation.ico"


def main():
    """
    create the business logic and the main window and launch them
    """
    settings = ecc_utility.load_settings()

    generator = ecc_logic.Generator(settings)

    main_window = tk.Tk()
    main_window.configure(bg=BG_COLOR)
    main_window.option_add("*font", "Calibri 9")
    main_window.iconbitmap(os.path.join(ecc_utility.DATA_PATH, ICON_FILENAME))

    app = ecc_gui.AppWindow(settings, generator)

    app.initialize()
    main_window.mainloop()

    ecc_utility.save_settings(settings)


if __name__ == '__main__':
    main()
