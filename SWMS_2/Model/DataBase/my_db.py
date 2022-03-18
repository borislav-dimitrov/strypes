from Model.Entities.logger import MyLogger
import Resources.config as cfg

# region Tracking
my_logger = ""
curr_user = ""
opened_pages = []
# endregion

# region Entities
login_users = []
products = []
suppliers = []
clients = []
warehouses = []
transactions = []


# endregion


def spawn_logger():
    logger = MyLogger(cfg.LOG_ENABLED, cfg.DEFAULT_LOG_FILE,
                      cfg.LOG_LEVEL, cfg.REWRITE_LOG_ON_STARTUP)
    return logger
