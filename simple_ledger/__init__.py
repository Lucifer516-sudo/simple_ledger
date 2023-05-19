from simple_ledger._log import Logger
from simple_ledger._config import AppConfig as config

ledger_logger = Logger(name="PyLedger", level=config.APP_LOG_LEVEL)


flet_core_logger: Logger = Logger(name="flet_core")
flet_logger: Logger = Logger(name="flet")

sqlalchemy_orm_logger: Logger = (Logger(name="sqlalchemy.orm"),)
sqlalchemy_dialects_logger: Logger = (Logger(name="sqlalchemy.dialects"),)
sqlalchemy_pool_logger: Logger = (Logger(name="sqlalchemy.pool"),)
sqlalchemy_engine_logger: Logger = (Logger(name="sqlalchemy.engine"),)
