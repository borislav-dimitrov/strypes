import helpers.tkinterHelpers as tkHelp
from config import *
from preload.populateData import all_cc, all_users, all_prn, all_crt


def prep_data_for_preview():
    preview_data = [("id", "type", "serial", "barcode", "cost centre", "bought date", "scrap date", "remark", "status")]
    for crt in all_crt:
        preview_data.append((crt.asset_id, crt.crt_type, crt.serial_number, crt.barcode,
                             f"{crt.cost_centre.number} | {crt.cost_centre.name}",
                             crt.date_bought, crt.date_scrap, crt.remark, crt.status))
    return preview_data


def init_user_controls(body, tk):
    actions_frame = tk.Frame(body)
    actions_frame.grid(column=0, row=0, sticky='w')
    actions_frame.grid_columnconfigure(1, minsize=50)

    new_btn = tk.Button(actions_frame, fg="black", cursor="hand2", bg="lightblue", justify="center", text="New",
                        name="btn_new_crt",
                        font=("Arial", 18))
    new_btn.grid(row=0, column=0)

    edit_btn = tk.Button(actions_frame, fg="black", cursor="hand2", bg="lightblue", justify="center", text="Edit",
                         name="btn_edit_crt",
                         font=("Arial", 18))
    edit_btn.grid(row=0, column=2)


def nav_crt(root, tk):
    tkHelp.clear_body(root)
    body = root.nametowidget("body")
    # change header
    header = root.nametowidget("header")
    header.config(text="Cartridges Menu")

    init_user_controls(body, tk)
    preview_data = prep_data_for_preview()
    tkHelp.create_preview(body, preview_data)
