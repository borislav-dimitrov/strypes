Project Title - Simple Warehouse Management System and Sales
	
	1. Project Description:
		1-I This is a simple application that allows users to view reports about stocks of materials, transactions and sell or buy products.
			Administrators are able to create/modify users, products, warehouses, clients and suppliers.

	2. How to use:
		2-I Configuration:
				Here you can set up some settings like resolution, and logging.

		2-II First run:
				On the first startup it will ask you to create the first administrator account, with which you can create other users after that.
				Usernames are key insensitive and passwords are encrypted with python cryptography module.
		
		2-III Menus:
				User Menus:
					View Stock -> Shows reports about current stocks of products by warehouse or by product.
					Transactions -> Shows reports about past transactions (sales or purchases).
					Sales -> Users can sell products to clients.
					Purchases -> Users can purchase products from suppliers.
			
		2-IV Administrator Menus:
				Users -> create/modify/delete another users. (Can't delete currently logged user!)
				Warehouses -> create/modify/delete warehouses.
				Clients -> create/modify/delete clients.
				Suppliers -> create/modify/delete suppliers.
				Products -> create/modify/delete products.