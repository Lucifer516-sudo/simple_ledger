import datetime
from pathlib import Path
from typing import Any, Literal, Optional, Type
from sqlmodel import SQLModel, Field
from simple_ledger.backend._db import DB, logger
from simple_ledger._config import AppConfig as config


class Ledger(SQLModel, table=True):  # One and only table/model : `Ledger`

    """
    This code block is defining a SQLModel class called `Ledger` with several fields/columns that will
    be used to create a table in a database. Each field is defined using the `Field` class from the
    `sqlmodel` library, which allows for specifying various properties such as data type, default value,
    and whether the field is nullable or not.
    """

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

    logger.info("LedgerObject: Creating Ledger Object")


class LedgerDB(DB):
    """DB for the Ledger . Inherits from DB"""

    def __init__(
        self,
    ) -> None:
        """
        This is a constructor function that initializes some variables and calls the constructor of a
        parent class with some arguments.
        """
        self.allowed_tags: list[str] = [
            "CREDIT",
            "DEBIT",
        ]

        # `self.database_config` is a dictionary that stores the configuration details for the
        # database used in the `LedgerDB` class. It contains the following keys and values:
        # - `db_api`: a string that specifies the type of database API to use (in this case, SQLite)
        # - `db_name`: a string that specifies the name of the database file (in this case,
        # "simple_ledger.db")
        # - `db_dir`: a `Path` object that specifies the directory where the database file should be
        # stored (in this case, ".simple_ledger/DB")
        # - `echo`: a boolean that specifies whether or not to enable logging of SQL statements (in
        # this case, True)
        # - `hide_parameters`: a boolean that specifies whether or not to hide sensitive information
        # (such as passwords) in SQL statements (in this case, False)
        self.database_config: dict[str, Any] = config().APP_DB_CONFIG

        super().__init__(
            db_api=self.database_config["db_api"],
            db_name=self.database_config["db_name"],
            db_dir=self.database_config["db_dir"],
            echo=self.database_config["echo"],
            hide_parameters=self.database_config["hide_parameters"],
        )

    def add_ledger_info(self, *, ledger: SQLModel) -> bool:
        """
        This function adds ledger information to a database using SQLModel and returns a boolean value
        indicating success or failure.

        Args:
          ledger (SQLModel): The `ledger` parameter is a SQLModel object that contains information about
        a ledger. This method `add_ledger_info` inserts the `ledger` object into a database table.

        Returns:
          The `add_ledger_info` method returns a boolean value indicating whether the insertion of the
        `ledger` object into the database was successful or not. It calls the `insert_records` method of
        the parent class (which is not shown in the code snippet) and passes the `ledger` object as a
        parameter.
        """
        return super().insert_records(model_object=ledger)

    def add_ledger_infos(self, *, ledgers: list[SQLModel]) -> bool:
        """
        This function adds a list of ledger information to a database using SQLModel.

        Args:
          ledgers (list[SQLModel]): `ledgers` is a list of `SQLModel` objects that contain information
        about ledger entries. This function adds these ledger entries to a database table using the
        `insert_records` method of the parent class. The function returns a boolean value indicating
        whether the insertion was successful or not.

        Returns:
          The `add_ledger_infos` method returns a boolean value indicating whether the insertion of the
        provided `ledgers` list was successful or not. It calls the `insert_records` method of the
        parent class (presumably a database access object) and passes the `ledgers` list as a parameter.
        """
        return super().insert_records(model_object=ledgers)

    def read_ledger_info(
        self,
        ledger_class: SQLModel = Ledger,
        *,
        where_and_to: dict[str, Any] | None = None,
        fetch_mode: Literal["all", "one", "many"] | None = "all",
        how_many: int | None = 10,
    ) -> list[Type[Ledger]] | Type[Ledger] | None:
        """
        This function reads ledger information from a SQL database using specified parameters.

        Args:
            ledger_class (SQLModel): The model class to use for reading ledger information. By default, it
        is set to `Ledger`.
            where_and_to (dict[str, Any] | None): `where_and_to` is a dictionary that specifies the
                conditions to filter the records in the database. The keys of the dictionary represent the
                column names and the values represent the values to filter by. For example, if you want to
                filter by the `name` column and only retrieve records where the name
            fetch_mode (Literal["all", "one", "many"] | None): The `fetch_mode` parameter specifies how
                many records should be fetched from the database. It can have one of the following values:.
                Defaults to all
            how_many (int | None): The `how_many` parameter is an optional integer that specifies the
                maximum number of records to fetch from the database. If `how_many` is not provided or is set to
                `None`, the function will fetch all records that match the specified criteria. If `how_many` is
                provided, the function. Defaults to 10

        Returns:
            The `read_ledger_info` function is returning the result of calling the `read_records` method
            of the parent class (which is not shown in the code snippet). The `read_records` method is
            expected to return a result based on the parameters passed to it, which include the
            `model_class` (a SQLModel class), `where_and_to` (a dictionary of conditions to filter the
        """
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
        """
        This function updates records in a ledger table using the provided parameters.

        Args:
          ledger_class (SQLModel): The model class that represents the ledger table in the database. It
        is a required parameter and its default value is set to SQLModel.
          where_and_to (dict[str, Any]): `where_and_to` is a dictionary that specifies the conditions
        for updating records in the database. The keys of the dictionary represent the column names and
        the values represent the values to be matched. For example, if we want to update records where
        the `id` column is equal to 1, we
          with_what (dict[str, Any]): `with_what` is a dictionary containing the key-value pairs of the
        fields and their updated values that need to be updated in the database table.

        Returns:
          `None`.
        """
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
        """
        This function deletes ledger records based on a given where clause.

        Args:
          ledger_class (SQLModel): The `ledger_class` parameter is a SQLModel class that represents the
        table in the database where ledger records are stored. It is used to specify which table to
        delete records from.
          where_and_to (dict[str, Any]): where_and_to is a dictionary that contains the conditions to
        filter the records to be deleted and the values to update in the remaining records after the
        deletion. The keys of the dictionary represent the column names and the values represent the
        values to be matched or updated. For example, if we want to delete all

        Returns:
          a boolean value indicating whether the deletion of ledger records was successful or not.
        """
        return super().delete_records(
            model_class=ledger_class,
            where_and_to=where_and_to,
        )

    def summary(self) -> dict:
        """
        The function summarizes ledger information by calculating total transactions, total credit and
        debit amounts, and amounts credited and debited by each person.

        Args:
          from_ (datetime.date): The start date for the summary period, represented as a datetime.date
        object.
          to_ (datetime.date): The `to_` parameter is a `datetime.date` object representing the end date
        of the time period for which the summary is being generated.

        Returns:
          A dictionary containing various summary information about the ledger transactions, such as
        total number of transactions, total credit and debit amounts, names of people who made
        transactions, and amounts credited and debited by each person.
        """
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
        total_credit = len(self.read_ledger_info(where_and_to={"tag": "CREDIT"}))
        total_debit = len(self.read_ledger_info(where_and_to={"tag": "DEBIT"}))
        from_whom_names = set(x.from_person for x in result)
        to_whom_names = set(x.to_person for x in result)

        set_of_froms = set(from_whom_names)

        # The above code is initializing two empty lists `amount_credited_by` and `amount_debited_by`
        # and then iterating over a set of names `set_of_froms`. For each name in the set, it is
        # adding a dictionary with the name as key and 0.0 as value to both `amount_credited_by` and
        # `amount_debited_by`.
        # The above code is iterating over a set of values called `set_of_froms` using a `for` loop.
        # For each value in the set, the loop assigns the value to the variable `name` and executes
        # the code block that follows the colon.
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
