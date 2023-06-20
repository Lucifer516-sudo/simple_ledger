from pathlib import Path
from simple_ledger.utils.logger import Logger
from simple_ledger.utils.config_handler import AppConfig

app_config: AppConfig = AppConfig()
log_path = Path(app_config.log_file)
import logging

logger = Logger(name="PyLedger", level=logging.DEBUG, log_to_path="test____1.log")


# flet_core_logger: Logger = Logger(name="flet_core", level=logging.DEBUG,log_to_path=log_path)
# flet_logger: Logger = Logger(name="flet", level=logging.DEBUG,log_to_path=log_path)


sqlalchemy_orm_logger: Logger = logger.get_loggers("sqlalchemy.orm")
sqlalchemy_dialects_logger: Logger = logger.get_loggers(name="sqlalchemy.dialects")
sqlalchemy_pool_logger: Logger = logger.get_loggers(name="sqlalchemy.pool")
sqlalchemy_engine_logger: Logger = logger.get_loggers(name="sqlalchemy.engine")
