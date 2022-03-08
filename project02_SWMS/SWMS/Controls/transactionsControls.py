import Services.tkinterServices as TkServ
import Models.Db.fakeDB as DB
import tkinter as tk


def clear_tr_screen(screen):
    clear_all_but = ["sales_btn", "purchases_btn", "header_lbl"]
    for widget in screen.grid_slaves():
        if str(widget).split(".").pop() not in clear_all_but:
            widget.destroy()
        if str(widget).split(".").pop() == "header_lbl":
            widget.config(text="View Transactions")


def sales(screen):
    # Clear the screen
    clear_tr_screen(screen)

    # Change the header
    hdr = screen.nametowidget("header_lbl")
    hdr.config(text="View Sales")

    # Create preview for all existing sales
    # Prepare the Data for the preview
    row_counter = 0

    # The first item in the Data are the column headers
    data = [("Row Num", "Id - Type", "Date", "Total Price", "Buyer Id - Buyer Name", "Products Sold")]
    for transaction in DB.transactions:
        if transaction.tr_type.lower() == "sale":
            buyer_id = transaction.buyer_seller.split("|")[0].strip().split(":")[1].strip()
            buyer_name = transaction.buyer_seller.split("|")[1].strip().split(":")[1].strip()

            products_info = ""
            for product in transaction.assets_traded:
                products_info += product.split("|")[1].strip()
                products_info += " - "
                products_info += product.split("|")[3].strip()
                products_info += " - "
                products_info += product.split("|")[5].strip()
                products_info += " | "

            data.append((row_counter + 1,
                         f"    {transaction.tr_id} - {transaction.tr_type}    ",
                         f"    {transaction.tr_date}    ",
                         transaction.tr_price,
                         f"    {buyer_id} - {buyer_name}    ",
                         f"    {products_info[:-2:]}    "))
            row_counter += 1

    # Initialize the preview
    preview = tk.Frame(screen, name="preview")
    preview.grid(row=6, column=0, columnspan=7)
    TkServ.create_preview(preview, data, columns=len(data[0]))


def purchases(screen):
    # Clear the screen
    clear_tr_screen(screen)

    # Change the header
    hdr = screen.nametowidget("header_lbl")
    hdr.config(text="View Purchases")

    # Create preview for all existing sales
    # Prepare the Data for the preview
    row_counter = 0

    # The first item in the Data are the column headers
    data = [("Row Num", "Id - Type", "Date", "Total Price", "Buyer Id - Buyer Name", "Products Sold")]
    for transaction in DB.transactions:
        if transaction.tr_type.lower() == "purchase":
            buyer_id = transaction.buyer_seller.split("|")[0].strip().split(":")[1].strip()
            buyer_name = transaction.buyer_seller.split("|")[1].strip().split(":")[1].strip()

            products_info = ""
            for product in transaction.assets_traded:
                products_info += product.split("|")[1].strip()
                products_info += " - "
                products_info += product.split("|")[3].strip()
                products_info += " - "
                products_info += product.split("|")[5].strip()
                products_info += " | "

            data.append((row_counter + 1,
                         f"    {transaction.tr_id} - {transaction.tr_type}    ",
                         f"    {transaction.tr_date}    ",
                         transaction.tr_price,
                         f"    {buyer_id} - {buyer_name}    ",
                         f"    {products_info[:-2:]}    "))
            row_counter += 1

    # Initialize the preview
    preview = tk.Frame(screen, name="preview")
    preview.grid(row=6, column=0, columnspan=7)
    TkServ.create_preview(preview, data, columns=len(data[0]))
