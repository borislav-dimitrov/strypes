import tkinter as tk
from gui.creategui import create_gui
from preload.populateData import populate_main
from gui.hookEvents import hook_events_to_gui
from config import *

# populate the data
populate_main()

root = tk.Tk()
root.title("Toners")
root.iconbitmap('./assets/ico.ico')  # set app icon
root.geometry(f"{RES_WIDTH}x{RES_HEIGHT}")


#data = [("header1", "header2", "header3", "edit"),
#        ("a", "b", "c", "btn"),
#        ("d", "e", "f", "btn"),
#        ("g", "h", "i", "btn")]

# t = Table(root, data)

create_gui(root)
hook_events_to_gui(root, tk)

root.mainloop()
