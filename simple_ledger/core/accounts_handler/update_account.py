from typing import Any
from simple_ledger.core.database.db import MasterDB


from simple_ledger.utils.password_maker import authenticate


def update_account(
    user_name: str,
    password_hash: str,
    where_and_to: dict[str, Any],
    with_what: dict[str, Any],
):
    __db = MasterDB()

    if authenticate(
        __db.search_user(where_and_to={"user_name": user_name}).password, password_hash
    ):
        __db.update_user(where_and_to=where_and_to, with_what=with_what)
        return True
    else:
        return False
