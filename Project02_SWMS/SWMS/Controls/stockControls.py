from tkinter import *
import Models.Db.fakeDB as DB
import Services.tkinterServices as TkServ
import Services.productServices as ProdServ


def clear_stock_screen(screen):
    clear_all_but = ["stock_by_prod_btn", "stock_by_wh_btn", "header_lbl"]
    for widget in screen.grid_slaves():
        if str(widget).split(".").pop() not in clear_all_but:
            widget.destroy()
        if str(widget).split(".").pop() == "header_lbl":
            widget.config(text="View Stock")


def clear_selected_wh(screen):
    clear_all_but = ["stock_by_prod_btn", "stock_by_wh_btn", "header_lbl", "!optionmenu"]
    for widget in screen.grid_slaves():
        if str(widget).split(".").pop() not in clear_all_but:
            widget.destroy()
        if str(widget).split(".").pop() == "header_lbl":
            widget.config(text="View stock by Warehouse")


def on_wh_dropdown_change(screen, var):
    clear_selected_wh(screen)

    chosen_wh_name = var.get()
    if "NaN" not in chosen_wh_name:
        chosen_wh_name = var.get().split("-")[1].strip()

    products_in_chosen_wh = ProdServ.get_all_products_assigned_to_wh(chosen_wh_name, DB.products)

    Label(screen, name="child_header_lbl", text=f"Stock in {chosen_wh_name}", font=("Ariel", 12)) \
        .grid(row=5, column=2, columnspan=2, sticky="w")

    # Create preview for all existing products
    # Prepare the Data for the preview
    # The first item in the Data are the column headers
    data = [("Row Num", "Product Id - Name")]
    if len(products_in_chosen_wh) == 0:
        data.append(("1", "None"))
    else:
        for product in range(len(products_in_chosen_wh)):
            data.append((product + 1,
                         f"{products_in_chosen_wh[product].product_id} - "
                         f"{products_in_chosen_wh[product].product_name}"))

    # Initialize the preview
    preview = Frame(screen, name="preview")
    preview.grid(row=6, column=0, columnspan=4, padx=(75, 0))
    TkServ.create_preview(preview, data, columns=len(data[0]))


def stock_by_wh(screen):
    # Clear the screen
    clear_stock_screen(screen)

    # Change the header
    hdr = screen.nametowidget("header_lbl")
    hdr.config(text="View stock by Warehouse")

    # Create DropDown with all existing users
    drop_down_variable = StringVar(screen)
    drop_down_variable.set("Chose a warehouse...")
    drop_down_options = ["NaN"]
    for warehouse in DB.warehouses:
        drop_down_options.append(f"{warehouse.wh_id} - "
                                 f"{warehouse.wh_name}")
    TkServ.create_drop_down(screen, drop_down_variable, drop_down_options,
                            lambda a: on_wh_dropdown_change(screen, drop_down_variable), 4, 1, cspan=2, stick="w")


def stock_by_product(screen):
    # Clear the screen
    clear_stock_screen(screen)

    # Change the header
    hdr = screen.nametowidget("header_lbl")
    hdr.config(text="View stock by Products")

    # Create preview for all existing products
    # Prepare the Data for the preview
    row_counter = 0
    all_warehouses = ["NaN"]
    # The first item in the Data are the column headers
    data = [("Row Num", "Warehouse", "Product Id - Name")]
    for warehouse in DB.warehouses:
        all_warehouses.append(warehouse.wh_name)

    for warehouse in range(len(all_warehouses)):
        current_wh_products = ProdServ.get_all_products_assigned_to_wh(all_warehouses[warehouse], DB.products)
        if len(current_wh_products) > 0:
            for product in range(len(current_wh_products)):
                data.append((row_counter + 1, all_warehouses[warehouse],
                             f"{current_wh_products[product].product_id} - "
                             f"{current_wh_products[product].product_name}"))
                row_counter += 1

    # Initialize the preview
    preview = Frame(screen, name="preview")
    preview.grid(row=5, column=0, columnspan=4, padx=(75, 0))
    TkServ.create_preview(preview, data, columns=len(data[0]))
