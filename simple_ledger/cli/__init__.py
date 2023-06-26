from simple_ledger.core.database.db import Ledger, LedgerDB
from simple_ledger import Logger, logger

from simple_ledger.utils.rich_printing import _get_console, _print_tables

from simple_ledger.utils.config.config import create_app_dirs
from simple_ledger.utils.config.config import PRE_CONFIGURED_APP_CONFIG

config = PRE_CONFIGURED_APP_CONFIG
get_console = _get_console.get_console
rich_table = _print_tables.rich_table
rich_table_data = _print_tables.TableData
rich_column = _print_tables.Column
rich_row = _print_tables.Row

db = LedgerDB
table = Ledger
console = get_console()
