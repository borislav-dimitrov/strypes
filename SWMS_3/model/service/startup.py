import model.dao.my_db as db

# DAO's
from model.dao.id_generator_int import IdGeneratorInt
from model.dao.password_manager import PasswordManager
from model.dao.repositories.generic_repo import GenericRepository
from model.dao.repositories.invoice_repo import InvoiceRepository

# Modules
from model.service.modules.sales_module import SalesModule
from model.service.modules.users_module import UserModule
from model.service.modules.warehousing_module import WarehousingModule


def start_up():
    # region INIT
    # region INIT REPOS
    usr_id_seq = IdGeneratorInt()
    usr_repo = GenericRepository(usr_id_seq)

    wh_id_seq = IdGeneratorInt()
    wh_repo = GenericRepository(wh_id_seq)

    pr_id_seq = IdGeneratorInt()
    pr_repo = GenericRepository(pr_id_seq)

    cpty_id_seq = IdGeneratorInt()
    cpty_repo = GenericRepository(cpty_id_seq)

    tr_id_seq = IdGeneratorInt()
    tr_repo = GenericRepository(tr_id_seq)

    inv_id_seq = IdGeneratorInt()
    inv_repo = InvoiceRepository(inv_id_seq)
    # endregion

    # region INIT MODULES
    db.user_module = UserModule(usr_repo, PasswordManager())
    db.warehousing_module = WarehousingModule(pr_repo, wh_repo)
    db.sales_module = SalesModule(cpty_repo, tr_repo, inv_repo)
    # endregion

    # endregion

    # Load entities from file
    db.user_module.load()
    db.warehousing_module.load_all()
    db.sales_module.load_all()


def before_exit():
    pass
