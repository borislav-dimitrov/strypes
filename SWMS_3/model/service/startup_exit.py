"""Functions to execute on Startup and before Exit"""

import resources.config as cfg

# DAO's
from model.dao.id_generator_int import IdGeneratorInt
from model.dao.logger import MyLogger
from model.dao.password_manager import PasswordManager
from model.dao.repositories.generic_repo import GenericRepository
from model.dao.repositories.invoice_repo import InvoiceRepository

# Modules
from model.service.modules.sales_module import SalesModule
from model.service.modules.users_module import UserModule
from model.service.modules.warehousing_module import WarehousingModule

# Controllers
from controler.user_controller import UserController
from controler.warehousing_controller import WarehousingController
from controler.sales_controller import SalesController


def init():
    """Initialize all repositories, modules, etc."""
    # OTHER
    logger = MyLogger(cfg.LOG_ENABLED, cfg.DEFAULT_LOG_FILE, cfg.LOG_LEVEL, cfg.REWRITE_LOG_ON_STARTUP)

    # REPOSITORIES
    usr_id_seq = IdGeneratorInt()
    usr_repo = GenericRepository(usr_id_seq, logger)

    wh_id_seq = IdGeneratorInt()
    wh_repo = GenericRepository(wh_id_seq, logger)

    pr_id_seq = IdGeneratorInt()
    pr_repo = GenericRepository(pr_id_seq, logger)

    cpty_id_seq = IdGeneratorInt()
    cpty_repo = GenericRepository(cpty_id_seq, logger)

    tr_id_seq = IdGeneratorInt()
    tr_repo = GenericRepository(tr_id_seq, logger)

    inv_id_seq = IdGeneratorInt()
    inv_repo = InvoiceRepository(inv_id_seq, logger)

    # MODULES
    user_module = UserModule(usr_repo, PasswordManager(), logger)
    warehousing_module = WarehousingModule(pr_repo, wh_repo, logger)
    sales_module = SalesModule(cpty_repo, tr_repo, inv_repo, logger)

    # CONTROLLERS
    user_controller = UserController(user_module, logger)
    warehousing_controller = WarehousingController(warehousing_module, logger)
    sales_controller = SalesController(sales_module, logger)

    return user_controller, warehousing_controller, sales_controller, logger


def start_up():
    """Execute on Startup"""
    usr_ctrl, wh_ctrl, sls_ctrl, logger = init()

    # Load entities from file
    usr_ctrl.load()
    wh_ctrl.load_all()
    sls_ctrl.load_all()

    return usr_ctrl, wh_ctrl, sls_ctrl, logger


def before_exit(usr_ctrl, wh_ctrl, sls_ctrl):
    """Execute before exit"""
    usr_ctrl.save()
    wh_ctrl.save_all()
    sls_ctrl.save_all()
