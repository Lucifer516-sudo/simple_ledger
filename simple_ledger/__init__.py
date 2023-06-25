from pathlib import Path
from simple_ledger.more.debugging.logger import Logger

logger = Logger("PyLedger")

# flet_core_logger: Logger = Logger(name="flet_core", level=logging.DEBUG,log_to_path=log_path)
# flet_logger: Logger = Logger(name="flet", level=logging.DEBUG,log_to_path=log_path)


sqlalchemy_orm_logger: Logger = logger.get_logger("sqlalchemy.orm")
sqlalchemy_dialects_logger: Logger = logger.get_logger(name="sqlalchemy.dialects")
sqlalchemy_pool_logger: Logger = logger.get_logger(name="sqlalchemy.pool")
sqlalchemy_engine_logger: Logger = logger.get_logger(name="sqlalchemy.engine")
