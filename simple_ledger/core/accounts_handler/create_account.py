from pathlib import Path
from simple_ledger.core.database.db import MasterDB, MasterTable
from simple_ledger import logger


def create_new_account(data: MasterTable) -> bool:
    __db: MasterDB = MasterDB()
    a: bool = __db.add_user(model_object=data)
    return a


mt = MasterTable(
    user_name="TestUser14",
    password="iuiwiuyiuyqw8iuyqwq8ywutyqwiuyiuywqeiuyiuyqweyqiweyqiuweyqiuweyqwuiywqieu",
)

# Path(AppConfig().log_path).mkdir(parents=True, exist_ok=True)
# print(AppConfig().log_path)
# print(Path(AppConfig().log_file))

create_new_account(mt)
