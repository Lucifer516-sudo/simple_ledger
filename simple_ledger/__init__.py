from simple_ledger.utils._log import Logger
from simple_ledger._config import AppConfig as config

ledger_logger = Logger(name="PyLedger", custom_name_to_message="PyLedger@Core")


flet_core_logger: Logger = Logger(
    name="flet_core", custom_name_to_message="PyLedger@FletCore"
)
flet_logger: Logger = Logger(name="flet", custom_name_to_message="PyLedger@Flet")

sqlalchemy_orm_logger: Logger = Logger(
    name="sqlalchemy.orm", custom_name_to_message="PyLedger@SQLAlchemy.ORM"
)
sqlalchemy_dialects_logger: Logger = Logger(
    name="sqlalchemy.dialects", custom_name_to_message="PyLedger@SQLAlchemy.DIALECT"
)
sqlalchemy_pool_logger: Logger = Logger(
    name="sqlalchemy.pool", custom_name_to_message="PyLedger@SQLAlchemy.POOL"
)
sqlalchemy_engine_logger: Logger = Logger(
    name="sqlalchemy.engine", custom_name_to_message="PyLedger@SQLAlchemy.ENGINE"
)
