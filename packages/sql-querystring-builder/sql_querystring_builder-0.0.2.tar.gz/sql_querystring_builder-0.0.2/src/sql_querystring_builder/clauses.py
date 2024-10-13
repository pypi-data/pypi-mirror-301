from __future__ import annotations

from .abstract_clause import Clause
from .tables import Aliasable, Field, Fields, Table, TempTable

class IncorrectUpdateException(Exception): pass

# TODO  Add INSERT
# TODO  Add concept of condition

class Select(Clause):
    def __init__(self, *fields: Fields|Aliasable|Table) -> None:
        self.fields: list[Field] = []
        for el in fields:
            if isinstance(el, Fields):
                self.fields.extend(el.as_list())
            elif isinstance(el, Table):
                self.fields.extend(el.fields.as_list())
            else:
                self.fields.append(el)
        self.temp_table: TempTable | None = None

    @property
    def place(self) -> int:
        return 0

    def build(self) -> str:
        ret : str = "SELECT " if self.fields else "SELECT *"
        ret += ", ".join([field.build(True, True) for field in self.fields])
        if self.temp_table:
            ret += "\nINTO "+ self.temp_table.build()
        return ret

    def to_temptable(self, name: str) -> TempTable:
        self.fields # debug
        self.temp_table: TempTable = TempTable(name, *self.fields)
        return self.temp_table

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(fields={self.fields})"


class From(Clause):
    def __init__(self, table: Table) -> None:
        self.table: Table = table

    @property
    def place(self) -> int:
        return 2

    def build(self) -> str:
        return f"FROM {self.table.build(True)}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(table={self.table})"


class Where(Clause):
    def __init__(self, *conditions: str|Field) -> None:
        self.conditions: list[str|Field] = conditions

    @property
    def place(self) -> int:
        return 4

    def build(self) -> str:
        ret: list[str] = ["WHERE"]
        for condition in self.conditions:
            ret.append(condition.build() if isinstance(condition, Aliasable) else condition)
        return " ".join(ret)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(conditions={self.conditions})"


class InnerJoin(Clause):
    def __init__(self, table: Table, on_left: Field, on_right: Field | Table) -> None:
        self.table: Table = table
        self.on_left: Field = on_left
        self.on_right: Field = on_right if isinstance(on_right, Aliasable) else on_right.fields.__getattr__(on_left.name)

    @property
    def place(self) -> int:
        return 3

    @property
    def is_exclusive(self) -> bool:
        return False

    def build(self) -> str:
        return f"INNER JOIN {self.table.build(use_name=True)} on {self.on_left.build()} = {self.on_right.build()}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(table={self.table}, on_left={self.on_left}, on_right={self.on_right})"


class Update(Clause):
    def __init__(self, updates: dict[Field, str]) -> None:
        if not updates:
            raise IncorrectUpdateException("The Update is empty.")
        self.updates: dict[Field, str] = {}
        table_name: str|None = None
        for field, value in updates.items():
            if table_name and table_name != field.table.name:
                raise IncorrectUpdateException(f"Two different tables cannot be updated in the same Update: '{table_name}' and '{field.table.name}'.")
            table_name = field.table.name
            self.updates[field] = value
        self.table: Table = field.table

    @property
    def place(self) -> int:
        return 0

    def build(self) -> str:
        field_strings: list[str] = [f"{field.build(use_alias=True)}={value}" for field, value in self.updates.items()]
        return f"UPDATE {self.table.build(use_name=False, use_alias=True)}\nSET " + ', '.join(field_strings)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(updates={self.updates})"


class OrderBy(Clause):
    def __init__(self, field: Field, descending: bool = False) -> None:
        self. ordering: list[tuple[Field, bool]] = [(field, descending)]

    @property
    def place(self) -> int:
        return 5

    def add(self, field: Field, descending: bool = False) -> OrderBy:
        self.ordering.append((field, descending))
        return self

    def build(self) -> str:
        ret_list: list[str] = []
        for field, desc in self.ordering:
            ret_list.append(f"{field.build(use_name=False, use_alias=True)}{' DESC' if desc else ''}")
        return "ORDER BY " + ', '.join(ret_list)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(ordering={self.ordering})"