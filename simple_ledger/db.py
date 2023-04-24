import datetime
from pathlib import Path
import time
from typing import Any, Literal, Optional
from sqlmodel import SQLModel, Field
from simple_ledger._db import DB
from rich import print


class Ledger(SQLModel, table=True):  # One and only table/model : `Ledger`
    id: Optional[int] = Field(default=None, primary_key=True)
    transaction_noted_on: datetime.date = Field(
        default_factory=datetime.datetime.now().date, nullable=False
    )
    transaction_noted_time: datetime.time = Field(
        default_factory=datetime.datetime.now().time, nullable=False
    )
    from_person: str = Field(nullable=False, max_length=30)
    to_person: str = Field(nullable=False, max_length=30)
    description: Optional[str] = Field(nullable=False, max_length=400)
    amount: float = Field(nullable=False)
    tag: str = Field(nullable=False, index=True)


class LedgerDB(DB):
    """DB for the Ledger . Inherits from DB"""

    def __init__(
        self,
    ) -> None:
        self.allowed_tags: list[str] = [
            "CREDIT",
            "DEBIT",
        ]

        self.database_config: dict[str, Any] = {
            "db_api": "sqlite",
            "db_name": "simple_ledger.db",
            "db_dir": Path(".simple_ledger/DB"),
            "echo": False,
            "hide_parameters": False,
        }

        super().__init__(
            db_api=self.database_config["db_api"],
            db_name=self.database_config["db_name"],
            db_dir=self.database_config["db_dir"],
            echo=self.database_config["echo"],
            hide_parameters=self.database_config["hide_parameters"],
        )

    def add_ledger_info(self, *, ledger: SQLModel) -> bool:
        return super().insert_records(model_object=ledger)

    def add_ledger_infos(self, *, ledgers: list[SQLModel]) -> bool:
        return super().insert_records(model_object=ledgers)

    def read_ledger_info(
        self,
        ledger_class: SQLModel = Ledger,
        *,
        where_and_to: dict[str, Any] | None = None,
        fetch_mode: Literal["all", "one", "many"] | None = "all",
        how_many: int | None = 10,
    ) -> Any:
        return super().read_records(
            model_class=ledger_class,
            where_and_to=where_and_to,
            fetch_mode=fetch_mode,
            how_many=how_many,
        )

    def update_ledger_info(
        self,
        *,
        ledger_class: SQLModel = Ledger,
        where_and_to: dict[str, Any],
        with_what: dict[str, Any],
    ) -> None:
        return super().update_records(
            model_class=ledger_class,
            where_and_to=where_and_to,
            with_what=with_what,
        )

    def delete_ledger_records(
        self,
        *,
        ledger_class: SQLModel = Ledger,
        where_and_to: dict[str, Any],
    ) -> bool:
        return super().delete_records(
            model_class=ledger_class,
            where_and_to=where_and_to,
        )

    def summary(self, from_: datetime.date, to_: datetime.date) -> dict:
        total_transactions: int = 0
        total_credit: float = 0.0
        total_debit: float = 0.0
        from_whom_names: set[str] = ""
        to_whom_names: set[str] = ""
        amount_credited_by: list[dict[str, float]] = []
        amount_debited_by: list[dict[str, float]] = []

        # read everything about ledger from the database
        result: list[Ledger] = self.read_ledger_info()
        total_transactions = len([x.id for x in result])
        total_credit = len(
            self.read_ledger_info(where_and_to={"tag": "CREDIT"})
        )
        total_debit = len(self.read_ledger_info(where_and_to={"tag": "DEBIT"}))
        from_whom_names = set(x.from_person for x in result)
        to_whom_names = set(x.to_person for x in result)

        set_of_froms = set(from_whom_names)

        for name in set_of_froms:
            amount_credited_by.append({name: 0.0})
            amount_debited_by.append({name: 0.0})

        for name in set_of_froms:
            for users in amount_credited_by:
                users[name] = sum(
                    [
                        x.amount
                        for x in self.read_ledger_info(
                            where_and_to={"from_person": name, "tag": "CREDIT"}
                        )
                    ]
                )
            for users in amount_debited_by:
                users[name] = sum(
                    [
                        x.amount
                        for x in self.read_ledger_info(
                            where_and_to={"from_person": name, "tag": "DEBIT"}
                        )
                    ]
                )

        return {
            "total_transactions": total_transactions,
            "total_credit": total_credit,
            "total_debit": total_debit,
            "from_whom_names": from_whom_names,
            "to_whom_names": to_whom_names,
            "amount_credited_by": amount_credited_by,
            "amount_debited_by": amount_debited_by,
        }


db: LedgerDB = LedgerDB()
from time import perf_counter
from random import choice, randint

_: list[float | int] = []


random_from_names: list[str] = ["Rudran", "Siva Balan", "Yogi"]
random_to_names: list[str] = ["Parvathi", "Shakthi", "Devi"]
random_tag: list[str] = ["CREDIT", "DEBIT"]
for i in range(10):
    from_: str = choice(random_from_names)
    to_: str = choice(random_to_names)
    db.add_ledger_info(
        ledger=Ledger(
            from_person=from_,
            to_person=to_,
            description=f"Transaction of Money Between {from_} and {to_}",
            amount=randint(1, 100000),
            tag=choice(random_tag),
        )
    )
    print(f"Added Entry: {i+1}")

print(db.summary(datetime.date.today(), datetime.date.today()))

db.add_ledger_infos(
    ledgers=[
        Ledger(
            from_person=from_,
            to_person=to_,
            description=f"Transaction of Money Between {from_} and {to_}",
            amount=randint(1, 100000),
            tag=choice(random_tag),
        ),
        Ledger(
            from_person=from_,
            to_person=to_,
            description=f"Transaction of Money Between {from_} and {to_}",
            amount=randint(1, 100000),
            tag=choice(random_tag),
        ),
    ]
)

print(db.summary(datetime.date.today(), datetime.date.today()))

db.update_ledger_info(
    where_and_to={"from_person": "Rudran"}, with_what={"amount": 0.0}
)

print(
    db.read_ledger_info(where_and_to={"from_person": "Rudran", "amount": 0.0})
)

db.delete_ledger_records(where_and_to={"from_person": "Rudran"})
print(db.summary(datetime.date.today(), datetime.date.today()))
