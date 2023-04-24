import os
from pathlib import Path
from typing import Any, Literal, Optional, Type, Union
from sqlmodel import SQLModel, Session, and_, create_engine, select


class DB:
    def __init__(
        self,
        *,
        db_api: str,
        db_name: str,
        db_dir: Union[str, Path],
        echo: Union[bool, str],
        hide_parameters: bool,
    ) -> None:
        self.db_api: str = db_api
        self.db_name: str = db_name
        self.db_dir: str | Path = db_dir

        # Engine:
        # Engine: Pre Init Works
        if (self.db_api != None) and (self.db_name != None):
            try:
                Path(self.db_dir).resolve().mkdir(parents=True)
            except:
                pass
        self.engine_url: str = f"{self.db_api}:///{str(self.db_dir.resolve())}{os.path.sep}{self.db_name}"
        self.engine: Any = create_engine(
            self.engine_url, echo=echo, hide_parameters=hide_parameters
        )
        self.create_table_metadata()

    def create_table_metadata(self):
        try:
            SQLModel.metadata.create_all(self.engine)
        except Exception as e:
            print(e, "eeee haa")

    def insert_records(
        self, *, model_object: Union[list[SQLModel], SQLModel]
    ) -> bool:
        try:
            with Session(self.engine) as session:
                if type(model_object) == list:
                    session.add_all(model_object)
                else:
                    session.add(model_object)

                session.commit()
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
        select(model).where(model.attribute == value)
        """
        with Session(self.engine) as session:
            if where_and_to != None:
                if len(list(where_and_to.keys())) == 1:
                    statement = select(model_class).where(
                        getattr(model_class, list(where_and_to.keys())[0])
                        == list(where_and_to.values())[0]
                    )
                if len(list(where_and_to.keys())) > 1:
                    statement: Type[select] = select(model_class)
                    for attribute, value in list(where_and_to.items()):
                        statement = statement.where(
                            getattr(model_class, attribute) == value
                        )

            else:
                statement = select(model_class)
            result = session.exec(statement)
            if fetch_mode == "all":
                return result.all()
            elif fetch_mode == "one":
                print("ONE")
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
        result = self.read_records(
            model_class=model_class,
            where_and_to=where_and_to,
            fetch_mode="one",
        )

        for attribute, value in with_what.items():
            setattr(
                result,
                attribute,
                value,
            )
        self.insert_records(model_object=result)
        with Session(self.engine) as session:
            session.refresh(result)
            session.close()

    def delete_records(
        self, *, model_class: SQLModel, where_and_to: dict[str, Any]
    ) -> bool:
        try:
            with Session(self.engine) as session:
                statement = select(model_class).where(
                    getattr(model_class, list(where_and_to.keys())[0])
                    == list(where_and_to.values())[0]
                )
                result = session.exec(statement).one()
                session.delete(result)
                session.commit()
                return True
        except Exception as e:
            print(f"Error deleting records: {e}")
            return False
