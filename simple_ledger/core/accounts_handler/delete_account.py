from typing import Any
from simple_ledger.core.database.db import MasterDB


from simple_ledger.utils.password_auth.password_maker import authenticate


def update_account(
    user_name: str,
    password_hash: str,
):
    __db = MasterDB()

    if authenticate(
        __db.search_user(where_and_to={"user_name": user_name}).password, password_hash
    ):
        return __db.delete_user(where_and_to={"user_name": user_name})
    else:
        return False
