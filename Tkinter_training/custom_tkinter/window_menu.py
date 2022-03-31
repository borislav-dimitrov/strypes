import tkinter as tk
import customtkinter as ctk
import theme_cfg as cfg


class MyMenu:
    def __init__(self, master):
        self._master = master
        self.text = ("Arial", 12)
        self.text_bold = ("Arial", 12, "bold")
        self.heading = ("Arial", 15, "bold")
        self.MAIN_COLOR = cfg._MAIN_COLOR
        self.HOVER_COLOR = cfg._HOVER_COLOR
        self.TEXT_COLOR = cfg._TEXT_COLOR

        self._Menubar = tk.Menu(self._master, bg="black")
        self._fileMenu = tk.Menu(self._Menubar, tearoff=0)
        self._fileMenu.add_command(label="Options", command=lambda: self._options())
        self._fileMenu.add_separator()
        self._fileMenu.add_command(label="Exit", command=lambda: quit())
        self._Menubar.add_cascade(label="File", menu=self._fileMenu)

        self._helpMenu = tk.Menu(self._Menubar, tearoff=0)
        self._helpMenu.add_command(label="About...", command=lambda: self._help())
        self._Menubar.add_cascade(label="Help", menu=self._helpMenu)

        self._master.config(menu=self._Menubar)

    # region OPTIONS
    def _options(self):
        root = ctk.CTkToplevel(self._master)
        ww = 640
        wh = 640
        root.geometry(f"{ww}x{wh}")
        root.attributes("-topmost", True)
        root.iconbitmap("sett_ico.ico")
        root.title("Options")
        header = ctk.CTkLabel(root, text="Options", text_color=self.TEXT_COLOR, text_font=self.heading)
        header.pack(side="top", pady=20)

        frame_theme = ctk.CTkFrame(root, border_color=self.TEXT_COLOR, border_width=3, height=wh / 3)
        frame_theme.pack(side="top", fill="both", padx=5, pady=20)
        frame_2 = ctk.CTkFrame(root, border_color=self.TEXT_COLOR, border_width=3, height=wh / 3)
        frame_2.pack(side="top", fill="both", padx=5, pady=20)

        # region THEME
        section_lbl = ctk.CTkLabel(frame_theme, text="Chose a theme", text_color=self.TEXT_COLOR,
                                   text_font=self.heading)
        section_lbl.pack(side="top", padx=20, pady=20)

        theme_var = tk.StringVar()
        theme_var.set(ctk.get_appearance_mode())
        light_rb = ctk.CTkRadioButton(frame_theme, text="Light", variable=theme_var, value="Light",
                                      text_font=self.text_bold, text_color=self.TEXT_COLOR)
        light_rb.pack(side="left", fill="none", expand=True, padx=20, pady=20)
        dark_rb = ctk.CTkRadioButton(frame_theme, text="Dark", variable=theme_var, value="Dark",
                                     text_font=self.text_bold, text_color=self.TEXT_COLOR)
        dark_rb.pack(side="right", fill="none", expand=True, padx=20, pady=20)
        root.update()
        # endregion

        info_lbl = ctk.CTkLabel(root, text="", text_font=self.heading, text_color=self.TEXT_COLOR)
        info_lbl.pack(side="top", fill="both", pady=10)
        save_btn = ctk.CTkButton(root, text="Save", text_font=self.text_bold,
                                 fg_color=self.MAIN_COLOR, hover_color=self.HOVER_COLOR,
                                 command=lambda: self._change_theme(theme_var, info_lbl))
        save_btn.pack(side="bottom", fill="none", expand=True, pady=(0, 20))
        root.mainloop()

    def _change_theme(self, state, label):
        self._rewrite_theme_cfg(state.get())
        label.config(text="Theme changed! Please restart the program!")

    @staticmethod
    def _rewrite_theme_cfg(state):
        text_clr = ""
        main_clr = ""
        hover_clr = ""
        if state == "Dark":
            text_clr = cfg._DARK_TEXT_COLOR
            main_clr = cfg._DARK_MAIN_COLOR
            hover_clr = cfg._DARK_HOVER_COLOR
        elif state == "Light":
            text_clr = cfg._LIGHT_TEXT_COLOR
            main_clr = cfg._LIGHT_MAIN_COLOR
            hover_clr = cfg._LIGHT_HOVER_COLOR

        new = f'_THEME = "{state}"\n_TEXT_COLOR = "{text_clr}"\n_MAIN_COLOR = "{main_clr}"\n' \
              f'_HOVER_COLOR = "{hover_clr}"\n_DARK_MAIN_COLOR = "#1C94CF"\n_DARK_HOVER_COLOR = "#186b94"\n' \
              f'_DARK_TEXT_COLOR = "#1C94CF"\n_LIGHT_MAIN_COLOR = "#5fd963"\n_LIGHT_HOVER_COLOR = "#318534"\n' \
              f'_LIGHT_TEXT_COLOR = "#318534"\n'

        with open("theme_cfg.py", "wt", encoding="utf-8") as file:
            file.write(new)

    # endregion

    # region HELP
    def _help(self):
        root = ctk.CTkToplevel(self._master)
        ww = 840
        wh = 640
        root.geometry(f"{ww}x{wh}")
        root.attributes("-topmost", True)
        root.iconbitmap("i.ico")
        root.title("About..")
        info_text = """
        Simple Warehouse Management System (SWMS) is a software application 
        to support and optimize warehouse functionality. 
        The system will be developed as a MVC using Tkinter as front-end, 
        and JSON file persistence technologies. 
        
        Menus:
        1.1.	 Home 
                    Presents some information about the program and buttons to access
                    the other views.
        1.2.	 Manage Users, Warehouses, Products, Suppliers, Clients
                    Provides ability to create/modify/delete users, warehouses, products,
                    suppliers, clients.
        1.3.	 View and Manage Warehouse
                    Presents warehouses stocks and give the ability to manage them.
        1.4.	 Purchases
                    Provides ability to purchase new products from suppliers.
        1.5.	 Sales
                    Provides ability to sell products to clients.
        1.6.	 Transactions
                    Presents existing transactions (purchases & sales) history.
                    Generate Invoice for desired transaction.

        """

        y_scroll = tk.Scrollbar(root, orient="vertical")
        y_scroll.pack(side="right", fill="y")
        x_scroll = tk.Scrollbar(root, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        frame = ctk.CTkFrame(root, height=wh)
        frame.pack(side="top", fill="both")

        # label = ctk.CTkEntry(frame, text=info_text, text_color=self.MAIN_COLOR, text_font=self.text_bold)
        textarea = tk.Text(frame, background="lightgray", font=self.heading, height=wh, wrap="none",
                           yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        textarea.pack(side="top", fill="both")
        textarea.insert("end", info_text)
        textarea.config(state="disabled")

        y_scroll.config(command=textarea.yview)
        x_scroll.config(command=textarea.xview)

        root.mainloop()

    # endregion
