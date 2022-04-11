import view.utils.tkinter_utils as tkutil
import tkinter as tk
from tkinter import ttk

from view.components.top_menu import MyMenu


class BaseView:
    def __init__(self, m_screen, page_name, resolution: tuple, grid_rows=30, grid_cols=30, icon=None):
        self.parent = m_screen
        self.page_name = page_name
        self.rows = grid_rows
        self.cols = grid_cols
        self.width = resolution[0]
        self.height = resolution[1]

        self.text = ("Arial", 12)
        self.text_bold = ("Arial", 12, "bold")
        self.heading = ("Arial", 15, "bold")
        self.colors = {"BLUE": "#1C94CF", "RED": "#871313", "LRED": "#823030", "DRED": "#731616"}

        # Center window
        tkutil.center_window(self.parent, self.width, self.height)

        # Set title
        self.parent.title(self.page_name)

        # Set icon
        if icon:
            self.parent.iconbitmap(icon)

        # Setup Grid
        tkutil.setup_grid(self.parent, self.cols, self.rows)

        # Setup Top Menu
        MyMenu(self.parent)

        # Header
        self.header = ttk.Label(self.parent, text=self.page_name, font=self.heading, anchor="center")
        self.header.grid(row=0, rowspan=2, column=0, columnspan=self.cols, sticky="we")
