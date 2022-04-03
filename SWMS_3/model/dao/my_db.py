from model.dao.logger import MyLogger
from model.service.modules.sales_module import SalesModule
from model.service.modules.users_module import UserModule
from model.service.modules.warehousing_module import WarehousingModule

# Modules
user_module: UserModule = None
warehousing_module: WarehousingModule = None
sales_module: SalesModule = None

# Services
logger: MyLogger = None
