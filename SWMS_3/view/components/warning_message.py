import customtkinter as ctk
import view.utils.tkinter_utils as tkutil


class MyWarningMessage:
    def __init__(self, message: str):
        self.root = ctk.CTk()
        self.rows = 6
        self.cols = 6
        self.FONT = ("Arial", 18, "bold")

        # Set Geometry
        self.w = 400
        self.h = 200
        tkutil.center_window(self.root, self.w, self.h)
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        # Set Title
        self.root.title("Warning")

        # Set Icon
        self.root.iconbitmap("resources/icons/w.ico")

        # Set Grid
        tkutil.setup_grid(self.root, self.rows, self.cols)

        self.info = ctk.CTkLabel(self.root, text=message, text_color="black", text_font=self.FONT, wraplength=300)
        self.info.grid(row=1, column=1, rowspan=self.rows - 2, columnspan=self.cols - 2, sticky="nsew")

        self.root.protocol("WM_DELETE_WINDOW", lambda: self.on_exit())
        self.root.mainloop()

    def on_exit(self):
        self.root.destroy()
