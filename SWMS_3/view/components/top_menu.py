import resources.config as cfg
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox
import view.utils.tkinter_utils as tkutil


class MyMenu:
    def __init__(self, parent):
        self.parent = parent
        self.text = ("Arial", 12)
        self.text_bold = ("Arial", 12, "bold")
        self.heading = ("Arial", 15, "bold")

        self._Menubar = tk.Menu(self.parent, bg="black")
        self._fileMenu = tk.Menu(self._Menubar, tearoff=0)
        self._fileMenu.add_command(label="Options", command=lambda: self._options_menu())
        self._fileMenu.add_separator()
        self._fileMenu.add_command(label="Exit", command=lambda: quit())
        self._Menubar.add_cascade(label="File", menu=self._fileMenu)

        self._helpMenu = tk.Menu(self._Menubar, tearoff=0)
        self._helpMenu.add_command(label="About...", command=lambda: self._help())
        self._Menubar.add_cascade(label="Help", menu=self._helpMenu)

        self.parent.config(menu=self._Menubar)

    # region OPTIONS
    def _options_menu(self):
        self.options_root = tk.Toplevel(self.parent)
        ww = 640
        wh = 640
        items_padding = 10
        tkutil.center_window(self.options_root, ww, wh)

        self.options_root.title("Options")

        frame1 = tk.Frame(self.options_root, borderwidth=3, height=wh / 5)
        frame1.pack(side="top", fill="both", padx=5, pady=20)
        frame2 = ttk.Frame(self.options_root, borderwidth=3, height=wh / 5)
        frame2.pack(side="top", fill="both", padx=5, pady=20)
        frame3 = ttk.Frame(self.options_root, borderwidth=3, height=wh / 5)
        frame3.pack(side="top", fill="both", padx=5, pady=20)
        frame4 = ttk.Frame(self.options_root, borderwidth=3, height=wh / 5)
        frame4.pack(side="top", fill="both", padx=5, pady=20)

        # Enabled/Disabled State
        section_lbl = ttk.Label(frame1, text="Enabled/Disabled Logging", font=self.text_bold)
        section_lbl.pack(side="top", padx=20, pady=items_padding)

        self.log_status_var = tk.StringVar()
        self.log_status_var.set(cfg.LOG_ENABLED)
        enabled_rb = ttk.Radiobutton(frame1, text="Enabled", variable=self.log_status_var, value=True)
        enabled_rb.pack(side="left", fill="none", expand=True, padx=20, pady=items_padding)
        disabled_rb = tk.Radiobutton(frame1, text="Disabled", variable=self.log_status_var, value=False)
        disabled_rb.pack(side="left", fill="none", expand=True, padx=20, pady=items_padding)

        # Rewrite on startup
        section_lbl = ttk.Label(frame2, text="Rewrite on startup", font=self.text_bold)
        section_lbl.pack(side="top", padx=20, pady=items_padding)

        self.log_rewrite_var = tk.StringVar()
        self.log_rewrite_var.set(cfg.REWRITE_LOG_ON_STARTUP)
        enabled_rb = ttk.Radiobutton(frame2, text="Enabled", variable=self.log_rewrite_var, value=True)
        enabled_rb.pack(side="left", fill="none", expand=True, padx=20, pady=items_padding)
        disabled_rb = tk.Radiobutton(frame2, text="Disabled", variable=self.log_rewrite_var, value=False)
        disabled_rb.pack(side="left", fill="none", expand=True, padx=20, pady=items_padding)

        # Logging Level
        section_lbl = ttk.Label(frame3, text="Logging level", font=self.text_bold)
        section_lbl.pack(side="top", padx=20, pady=items_padding)

        self.log_level_var = tk.StringVar()
        self.log_level_var.set(cfg.LOG_LEVEL)
        debug_rb = ttk.Radiobutton(frame3, text="Debug", variable=self.log_level_var, value="DEBUG")
        debug_rb.pack(side="left", fill="none", expand=True, padx=20, pady=items_padding)
        info_rb = tk.Radiobutton(frame3, text="Info", variable=self.log_level_var, value="INFO")
        info_rb.pack(side="left", fill="none", expand=True, padx=20, pady=items_padding)
        warning_rb = tk.Radiobutton(frame3, text="Warning", variable=self.log_level_var, value="WARNING")
        warning_rb.pack(side="left", fill="none", expand=True, padx=20, pady=items_padding)
        error_rb = tk.Radiobutton(frame3, text="Error", variable=self.log_level_var, value="ERROR")
        error_rb.pack(side="left", fill="none", expand=True, padx=20, pady=items_padding)
        critical_rb = tk.Radiobutton(frame3, text="Critical", variable=self.log_level_var, value="CRITICAL")
        critical_rb.pack(side="left", fill="none", expand=True, padx=20, pady=items_padding)

        # Default file
        section_lbl = ttk.Label(frame4, text="Default log file", font=self.text_bold)
        section_lbl.pack(side="top", padx=20, pady=items_padding)

        self.file_var = tk.StringVar()
        self.file_var.set(cfg.DEFAULT_LOG_FILE)
        if self.file_var.get() == "":
            self.file_var.set("log.txt")

        chose_file_btn = ttk.Button(frame4, text="Chose log file", command=lambda: self._select_file())
        chose_file_btn.pack(side="left", pady=items_padding)
        chosen_file_path = ttk.Label(frame4, textvariable=self.file_var, font=self.text, background="lightgray",
                                     anchor="center")
        chosen_file_path.pack(side="right", fill="x", expand=True, padx=20, pady=items_padding)

        self.options_root.update()

        save_btn = ttk.Button(self.options_root, text="Save", command=lambda: self._save())
        save_btn.pack(side="top", fill="none", expand=True)

        # modal - capture visibility
        self.options_root.protocol("WM_DELETE_WINDOW", self.dismiss_options)
        self.options_root.transient(self.parent)
        self.options_root.wait_visibility()
        self.options_root.grab_set()
        self.options_root.wait_window()

        self.options_root.mainloop()

    def _select_file(self):
        dialog_types = (("text files", "*.txt"), ('All files', '*.*'))
        dialog = fd.askopenfilename(title="Chose log file", initialdir="/", filetypes=dialog_types)
        self.file_var.set(dialog)

    def _save(self):
        if self.file_var.get() != "":
            self._rewrite_theme_cfg(self.log_level_var.get(), self.log_rewrite_var.get(), self.log_status_var.get(),
                                    self.file_var.get())
            messagebox.showinfo("Info..", "Settings changed! Restart the program!", parent=self.options_root)

    @staticmethod
    def _rewrite_theme_cfg(level, rewrite, enabled, log_file):
        if rewrite == "1":
            rewrite = True
        elif rewrite == "0":
            rewrite = False
        if enabled == "1":
            enabled = True
        elif enabled == "0":
            enabled = False

        new = f"""# Configuration file

# Logging settings
#      Logging levels:
#          DEBUG -> Lowest level. Used to record simple details.
#          INFO -> Record general information.
#          WARNING -> Potential issues which may not cause errors in the future.
#          ERROR -> Due to a more serious problem, the software has not been able to perform some function
#          CRITICAL -> Highest level. Blockers which fails your whole program. 
LOG_ENABLED = {enabled}
REWRITE_LOG_ON_STARTUP = {rewrite}
LOG_LEVEL = "{level}"
DEFAULT_LOG_FILE = "{log_file}" """

        with open("./resources/config.py", "wt", encoding="utf-8") as file:
            file.write(new)

    # endregion

    # region HELP
    def _help(self):
        self.help_root = tk.Toplevel(self.parent)
        ww = 840
        wh = 640
        tkutil.center_window(self.help_root, ww, wh)
        self.help_root.title("About..")
        with open("./docs/Documentation.txt", "rt", encoding="utf-8") as file:
            info_text = file.readlines()

        y_scroll = tk.Scrollbar(self.help_root, orient="vertical")
        y_scroll.pack(side="right", fill="y")
        x_scroll = tk.Scrollbar(self.help_root, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        frame = ttk.Frame(self.help_root, height=wh)
        frame.pack(side="top", fill="both")

        # label = ctk.CTkEntry(frame, text=info_text, text_color=self.MAIN_COLOR, text_font=self.text_bold)
        textarea = tk.Text(frame, background="lightgray", font=self.heading, height=wh, wrap="none",
                           yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        textarea.pack(side="top", fill="both")
        textarea.insert("end", "".join(info_text))
        textarea.config(state="disabled")

        y_scroll.config(command=textarea.yview)
        x_scroll.config(command=textarea.xview)

        # # modal - capture visibility
        self.help_root.protocol("WM_DELETE_WINDOW", self.dismiss_help)
        self.help_root.transient(self.parent)
        self.help_root.wait_visibility()
        self.help_root.grab_set()
        self.help_root.wait_window()

        self.help_root.mainloop()

    # endregion

    def dismiss_options(self):
        self.options_root.grab_release()
        self.options_root.destroy()

    def dismiss_help(self):
        self.help_root.grab_release()
        self.help_root.destroy()
