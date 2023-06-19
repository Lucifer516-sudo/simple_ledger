from pathlib import Path
from simple_ledger.utils.logger import Logger
from simple_ledger.utils.config_handler import AppConfig

app_config: AppConfig = AppConfig()
log_path = Path(app_config.log_file)


logger = Logger(name="PyLedger", log_to_path=log_path)


# flet_core_logger: Logger = Logger(name="flet_core", log_to_path=log_path)
# flet_logger: Logger = Logger(name="flet", log_to_path=log_path)

sqlalchemy_orm_logger: Logger = logger.get_logger("sqlalchemy.orm")
sqlalchemy_dialects_logger: Logger = logger.get_logger(name="sqlalchemy.dialects")
sqlalchemy_pool_logger: Logger = logger.get_logger(name="sqlalchemy.pool")
sqlalchemy_engine_logger: Logger = logger.get_logger(name="sqlalchemy.engine")
sqlalchemy_dialects_logger.info("hiiiiii")
