from model.dao.id_generator_int import IdGeneratorInt
from model.dao.repositories.generic_repo import GenericRepository
from model.dao.repositories.invoice_repo import InvoiceRepository
from model.entities.invoices import Invoice
from model.entities.user import User

usr_id_seq = IdGeneratorInt()
user_repo = GenericRepository(usr_id_seq)

new_user1 = User("Poncho", "Pervenche", "Administrator", "Enabled", "")
new_user2 = User("Ivan", "Ivanov", "Operator", "Enabled", "")

user_repo.create(new_user1)
user_repo.create(new_user2)

inv_id_seq = IdGeneratorInt()
inv_repo = InvoiceRepository(inv_id_seq)

new_invoice1 = Invoice(123, "gosho", "pesho", "dneska", "utre", ["item1", "item2"], 20.0, "", "", "Pending")
new_invoice2 = Invoice(125, "gosho", "pesho", "dneska", "utre", ["item1", "item2"], 20.0, "", "", "Pending")

inv_repo.create(new_invoice1)
inv_repo.create(new_invoice2)
inv = inv_repo.find_by_inv_number(125)
