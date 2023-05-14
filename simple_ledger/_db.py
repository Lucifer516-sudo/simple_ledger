import os
from pathlib import Path
from typing import Any, Literal, Optional, Type, Union
from sqlmodel import SQLModel, Session, create_engine, select
from pprint import pformat
from simple_ledger._log import Logger
from simple_ledger._config import AppConfig as config

logger = Logger(name="PyLedger", level=config.APP_LOG_LEVEL)


class DB:
    """
    The DB class provides methods for creating, reading, updating, and deleting records in a database
    using SQLAlchemy.
    """

    def __init__(
        self,
        *,
        db_api: str,
        db_name: str,
        db_dir: Union[str, Path],
        echo: Union[bool, str],
        hide_parameters: bool,
    ) -> None:
        """
        This is a constructor function that initializes a database connection and creates tables in the
        database.

        Args:
          db_api (str): A string representing the database API to be used (e.g. "sqlite", "mysql",
        "postgresql").
          db_name (str): The name of the database that will be created or used.
          db_dir (Union[str, Path]): The `db_dir` parameter is a string or `Path` object that represents the
        directory where the database file will be stored. It is used in the `__init__` method to create the
        directory if it does not exist and to construct the engine URL.
          echo (Union[bool, str]): A boolean or string value that determines whether or not to echo SQL
        statements generated by the engine. If set to True, all SQL statements will be printed to the
        console. If set to False, no SQL statements will be printed. If set to a string, only SQL statements
        matching the string will be
          hide_parameters (bool): A boolean parameter that determines whether or not to hide the parameters
        in the SQL queries executed by the engine. If set to True, the parameters will be replaced with
        question marks in the query.
        """
        self.db_api: str = db_api
        self.db_name: str = db_name
        self.db_dir: str | Path = db_dir

        # Engine:
        # Engine: Pre Init Works
        try:
            """
            if (self.db_api != None) and (self.db_name != None):
            This code block is creating a directory for the database file if it does not exist and
            creating the database file using the `touch` command. If an exception occurs during this
            process, it logs the error and raises a critical error message.
            """
            logger.info("DB@Init: Creating the DB Directory")
            logger.debug(
                f"DB@Init: DB Directory - {self.db_dir} | DB API - {self.db_api} | DB Name - {self.db_name}"
            )
            if Path(self.db_dir).exists() == False:
                Path(self.db_dir).mkdir(parents=True, exist_ok=True)
                os.system(
                    f"touch {str(self.db_dir)}{os.path.sep}{self.db_name}"
                )
        except Exception as e:
            logger.error(e)
            logger.critical(
                f"Unable to Create DB File: {str(self.db_dir)}{os.path.sep}{self.db_name}"
            )

        self.engine_url: str = (
            f"{self.db_api}:///{str(self.db_dir)}{os.path.sep}{self.db_name}"
        )
        logger.info("DB@Init: Created Engine URL")
        logger.debug(f"DB@Init: Engine URL - {self.engine_url}")
        self.engine: Any = create_engine(
            self.engine_url, echo=False, hide_parameters=hide_parameters
        )
        logger.info("DB@Init: Creating tables in the DB")
        self.create_table_metadata()

    def create_table_metadata(self) -> bool:
        """
        This function creates metadata for a database using a bound engine and returns a boolean
        indicating success or failure.

        Returns:
          a boolean value. If the metadata creation is successful, it returns True. If there is an
        exception, it prints the error message and returns False.
        """
        try:
            logger.debug(
                f"DB@MetaDataCreation: Creating metadata with binded Engine - {self.engine}"
            )
            SQLModel.metadata.create_all(self.engine)
            return True
        except Exception as e:
            print(e)
            return False

    def insert_records(
        self, *, model_object: Union[list[SQLModel], SQLModel]
    ) -> bool:
        """
        The function inserts one or more SQLModel objects into a database session and returns a boolean
        indicating success or failure.

        Args:
          model_object (Union[list[SQLModel], SQLModel]): The `model_object` parameter is a required
        keyword-only argument of the `insert_records` method. It can either be a single instance of a
        `SQLModel` object or a list of `SQLModel` objects. These objects represent the data that needs
        to be inserted into the database. The method

        Returns:
          a boolean value. If the records are successfully inserted into the database, it returns True.
        If there is an exception during the insertion process, it returns False.
        """
        try:
            logger.info("DB@INSERT: CREATE Working")
            with Session(self.engine) as session:
                if type(model_object) == list:
                    session.add_all(model_object)
                    logger.info(
                        "Session@INSERT: Added list of SQLModel Objects"
                    )
                    logger.debug(
                        f"Session@INSERT: Added Objects - {model_object}"
                    )
                else:
                    session.add(model_object)
                    logger.info("Session@INSERT: Added SQLModel Object")
                    logger.debug(
                        f"Session@INSERT: Added Object - {model_object}"
                    )
                session.commit()
                logger.debug("Session@INSERT: Committed Session ")
                return True
        except Exception as e:
            return False

    def read_records(
        self,
        *,
        model_class: SQLModel,
        where_and_to: Optional[dict[str, Any]] = None,
        fetch_mode: Optional[Literal["all", "one", "many"]] = "many",
        how_many: Optional[int] = 10,
    ) -> Any:
        """
        This function reads records from a SQL database based on specified parameters and returns the
        results in a specified fetch mode.

        Args:
          model_class (SQLModel): The SQLAlchemy model class representing the database table to read
        records from.
          where_and_to (Optional[dict[str, Any]]): `where_and_to` is a dictionary that contains the
        conditions to filter the records to be fetched. The keys of the dictionary represent the
        attributes of the model class and the values represent the values that the attributes should
        have. If `where_and_to` is None, all records will be fetched.
          fetch_mode (Optional[Literal["all", "one", "many"]]): `fetch_mode` is an optional parameter
        that specifies how the records should be fetched from the database. It can take one of three
        values: "all", "one", or "many". If "all" is specified, all the records that match the query
        will be fetched. If "one". Defaults to many
          how_many (Optional[int]): `how_many` is an optional integer parameter that specifies the
        number of records to fetch when `fetch_mode` is set to "many". If `how_many` is not specified or
        is set to None, the default value of 10 will be used. If `fetch_mode` is not set. Defaults to 10

        Returns:
          The function `read_records` returns the result of executing a SQL query on a database using
        the provided `model_class` and `where_and_to` parameters. The result is fetched based on the
        `fetch_mode` and `how_many` parameters, and the fetched data is returned. The return type can be
        any depending on the `fetch_mode` and the fetched data.
        """

        with Session(self.engine) as session:
            logger.info("Session@READ: READ Work")
            if where_and_to != None:
                if len(list(where_and_to.keys())) == 1:
                    statement: Type[select] = select(model_class).where(
                        getattr(model_class, list(where_and_to.keys())[0])
                        == list(where_and_to.values())[0]
                    )
                    logger.info(
                        "Session@READ: Reading records with the given where info"
                    )
                    logger.debug(
                        f"Session@READ: Exec - {statement} \nwhere: {pformat(where_and_to, indent=2)}"
                    )
                if len(list(where_and_to.keys())) > 1:
                    statement: Type[select] = select(model_class)
                    logger.info(
                        "Session@READ: Multiple where and to keys are given"
                    )
                    for attribute, value in list(where_and_to.items()):
                        statement = statement.where(
                            getattr(model_class, attribute) == value
                        )
                        logger.info(
                            "Session@READ: Reading records with the given where info"
                        )
                        logger.debug(
                            f"Session@READ: Exec - {statement} \nwhere: {pformat(where_and_to, indent=2)}"
                        )

            else:
                statement: Type[select] = select(model_class)
            result = session.exec(statement)
            logger.info("DB@READ: Fetching data")
            logger.debug(f"DB@READ: Fetch Mode - {fetch_mode}")
            if fetch_mode == "all":
                return result.all()
            elif fetch_mode == "one":
                try:
                    return result.one()  # handle error
                except Exception:
                    pass
                    # return result[
                    #     0
                    # ]  # not the best way need to handle the exception here
            elif (
                (fetch_mode == "many")
                and (how_many != None)
                and (how_many > 0)
            ):
                return result.fetchmany(how_many)
            else:  # if no fetch_mode specified
                return result.all()

    def update_records(
        self,
        *,
        model_class: SQLModel,
        where_and_to: dict[str, Any],
        with_what: dict[str, Any],
    ) -> None:
        """
        This function updates records in a database using SQLAlchemy ORM.

        Args:
          model_class (SQLModel): The SQLModel class that represents the database table to be updated.
          where_and_to (dict[str, Any]): `where_and_to` is a dictionary that specifies the conditions to
        locate the record(s) to be updated in the database table. The keys of the dictionary represent
        the column names and the values represent the values to be matched. For example, if the table
        has columns "id", "name", and
          with_what (dict[str, Any]): `with_what` is a dictionary containing the attributes and their
        updated values that you want to update in the database table. The keys of the dictionary
        represent the attribute names and the values represent the updated values for those attributes.
        """
        with Session(self.engine) as session:
            logger.info(
                "Session@UPDATE: Update Work - Refreshing and committing to the database"
            )

            try:
                result = self.read_records(
                    model_class=model_class,
                    where_and_to=where_and_to,
                    fetch_mode="one",
                )
                logger.debug(f"DB@UPDATE: result - \n{result}")

                for attribute, value in with_what.items():
                    setattr(
                        result,
                        attribute,
                        value,
                    )
                    # locals()[f"result.{attribute}"] = value
                    logger.info("DB@UPDATE: Updating Records")
                    logger.debug(
                        f"DB@UPDATE: Updating {result} with {attribute} being changed to {value}"
                    )
            except Exception as e:
                logger.error(f"DB@UPDATE: {e}")

                self.insert_records(model_object=result)

            # session.refresh(result)
            session.close()

    def delete_records(
        self,
        *,
        model_class: SQLModel,
        where_and_to: dict[str, Any],
        delete_mode: Literal["all", "one"] = "one",
    ) -> bool:
        """
        The function deletes records from a SQL database based on a given model class and a dictionary
        of where conditions, with the option to delete all matching records or just one.

        Args:
          model_class (SQLModel): The SQLModel class representing the database table from which records
        will be deleted.
          where_and_to (dict[str, Any]): `where_and_to` is a dictionary that contains the condition(s)
        to be used in the `WHERE` clause of the SQL `DELETE` statement. The keys of the dictionary
        represent the column names and the values represent the values to be matched. For example, if
        `where_and_to` is
          delete_mode (Literal["all", "one"]): The `delete_mode` parameter is a string literal that
        specifies the mode of deletion. It can be either "one" or "all". If it is set to "one", only one
        record that matches the given condition will be deleted. If it is set to "all", all records that
        match. Defaults to one

        Returns:
          a boolean value indicating whether the deletion of records was successful or not. True is
        returned if the deletion was successful, and False is returned if there was an error.
        """
        try:
            with Session(self.engine) as session:
                logger.info("Session@DELETE: DELETE Work")
                statement = select(model_class).where(
                    getattr(model_class, list(where_and_to.keys())[0])
                    == list(where_and_to.values())[0]
                )
                logger.debug(f"Session@DELETE: Delete Mode: {delete_mode}")
                result = session.exec(statement)
                if delete_mode == "one":
                    session.delete(list(result)[0])
                    logger.debug("Session@DELETE: Deleted one result")
                elif delete_mode == "all":
                    session.delete(result)
                    logger.debug("Session@DELETE: Deleted all results")

                logger.info("Session@DELETE: Committing Session")
                session.commit()
                return True
        except Exception as e:
            logger.debug(f"Session@DELETE: Error deleting records: {e}")
            return False
