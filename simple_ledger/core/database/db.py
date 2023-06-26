import datetime
from typing import Any, Literal, Optional, Type
from sqlmodel import SQLModel, Field
from simple_ledger.core.database._db import DB

from simple_ledger.utils.config.config import PRE_CONFIGURED_APP_CONFIG

# from simple_ledger.utils.config_handler import AppDBConfig, UserDBConfig

# The above code is importing necessary modules and defining classes and functions for a database
# backend using SQLModel. It is defining a database class DB, which is used to connect to a SQLite
# database and perform CRUD operations. It also defines a model class SQLModel, which is used to
# define the structure of the database tables. The code also imports a logger and the application
# configuration from a separate module.


class Ledger(SQLModel, table=True):
    """
    This is a Python class representing a ledger table/model with various fields such as transaction
    date and time, persons involved, description, amount, and tag.

    The above code defines a Python class called `LedgerObject` with several attributes such as
    `id`, `transaction_noted_on`, `transaction_noted_time`, `from_person`, `to_person`,
    `description`, `amount`, and `tag`. These attributes are defined using the `Field` class from
    the `pydantic` library, which provides validation and serialization of data. The `logger` object
    is used to log an informational message when a new `LedgerObject` is created.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    transaction_noted_on: datetime.date = Field(
        default_factory=datetime.datetime.now().date, nullable=False
    )
    transaction_noted_time: datetime.time = Field(
        default_factory=datetime.datetime.now().time, nullable=False
    )
    customer_name: str = Field(nullable=False, max_length=50)
    customer_mobile: str = Field(nullable=False, max_length=50)
    amount_charged: float = Field(nullable=False)
    # tag: str = Field(nullable=False, index=True)


class LedgerDB(DB):  # The class LedgerDB is a subclass of DB.
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
            return super().__new__(cls)
        else:
            return cls.__instance

    def __init__(
        self,
    ) -> None:
        """
        This is a constructor function that initializes some variables and calls the constructor of a
        parent class with some arguments.
        """
        self.user_name = "Harish"
        self.allowed_tags: list[str] = [
            "CREDIT",
            "DEBIT",
        ]

        self.database_config = PRE_CONFIGURED_APP_CONFIG

        super().__init__(
            db_api=self.database_config.DB_API,
            db_name=self.user_name.upper() + ".db",
            db_dir=self.database_config.DB_DIR_PATH,
            echo=self.database_config.DB_ECH0,
            hide_parameters=self.database_config.DB_HIDE_PARAMETERS,
        )
        # The above code is calling the constructor of a class and passing in several arguments. The
        # arguments are values from a dictionary called `database_config`. The `db_api`, `db_name`,
        # `db_dir`, `echo`, and `hide_parameters` arguments are being passed to the constructor using
        # the `self` keyword.

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
