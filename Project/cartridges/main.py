import tkinter as tk
from gui.creategui import create_gui
from preload.populateData import populate_main
from gui.hookEvents import hook_events_to_gui
from config import *

# populate the data
populate_main()

root = tk.Tk()
# set app properties
root.title("Toners")
root.iconbitmap(ICON_PATH)  # set app icon
root.geometry(f"{RES_WIDTH}x{RES_HEIGHT}")


create_gui(root)
hook_events_to_gui(root, tk)

root.mainloop()
