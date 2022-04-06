import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import view.utils.tkinter_utils as tkutil
from controler.user_controller import UserController
from view.base_view import BaseView


class UserManagementView(BaseView):
    def __init__(self, m_screen, page_name, controller: UserController, resolution: tuple = (1280, 728), grid_rows=30,
                 grid_cols=30,
                 icon=None):
        super().__init__(m_screen, page_name, resolution, grid_rows, grid_cols, icon)
        self._controller = controller

        # Create GUI

