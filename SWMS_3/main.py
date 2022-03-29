from model.dao.id_generator_int import IdGeneratorInt
from model.dao.generic_repo import GenericRepository
from model.entities.invoices import Invoice
from model.entities.user import User

usr_id_seq = IdGeneratorInt()
user_repo = GenericRepository(usr_id_seq)

new_user1 = User("Poncho", "!@#asd", "Administrator", "Enabled", "")
new_user2 = User("Ivan", "asd#@!", "Operator", "Enabled", "")

user_repo.create(new_user1)
user_repo.create(new_user2)

inv_id_seq = IdGeneratorInt()
inv_repo = GenericRepository(inv_id_seq)

new_invoice1 = Invoice(123, "gosho", "PESHO", "dneska", "utre", ["item1", "item2"], 20.0, "", "", "Pending")
new_invoice2 = Invoice(125, "gosho", "PESHKO", "dneska", "utre", ["item1", "item2"], 20.0, "", "", "Pending")
inv_repo.create(new_invoice1)
inv_repo.create(new_invoice2)

found = user_repo.find_by_attribute("name", "poncho")
for i in user_repo.find_all():
    print(vars(i))