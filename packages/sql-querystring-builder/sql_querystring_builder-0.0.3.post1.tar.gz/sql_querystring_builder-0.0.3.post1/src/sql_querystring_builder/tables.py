from __future__ import annotations
from abc import ABC, abstractmethod
from string import ascii_letters, digits

class AliasException(Exception): pass
class AlreadyExistingFieldException(Exception): pass
class InvalidNameException(Exception): pass
class NonExistingAliasException(Exception): pass
class NonExistingFieldException(Exception): pass
class TableException(Exception): pass


NAMEABLE_CHARS: str = ascii_letters + digits + '_'


def validate_name(name: str, is_hashtag_allowed: bool = False) -> str:
    """Validates if a name can be used as a SQL named element.

    Parameters
    ----------
    name : str
        Table name to validate.
    is_hashtag_allowed : bool, optional
        Specified if a name starting with a hashtag '#' is allowed.

    Returns
    -------
    str
        The name itself, if validated (otherwise, one of the errors will be raised).

    Raises
    ------
    InvalidNameException
        Raised if the name cannot reprensent an element in a strict MS SQL conventions.
    """
    def validate_subname(subname: str, startpos: int = 0, is_temp_table_start: bool = False) -> None:
        max_length: int = 116 if is_temp_table_start else 128
        if len(subname) > max_length:
            raise InvalidNameException(f"The name {name} is too long or has a component that is too long (got {startpos + len(subname)}, max is {max_length}).")
        for pos, c in enumerate(subname):
            if is_temp_table_start and pos == 0 and c == "#":
                continue # is indeed a temp table starting with #
            if c not in NAMEABLE_CHARS:
                if (c != '[' or pos != 0) and (c != ']' or pos != len(subname) - 1):
                    raise InvalidNameException(f"Forbidden character '{c}' was found in the name '{name}' at position {pos + startpos}. Only letters, digits and undersores are allowed.")

    if not name:
        raise InvalidNameException("Empty names are forbidden.")
    if name[0] not in ascii_letters:
        if not is_hashtag_allowed or name[0] != '#':
            raise InvalidNameException(f"The name {name} does not start with a letter.")
    absolute_pos: int = 0
    for i_split, subname in enumerate(name.split('.')):
        is_temp_table_start: bool = i_split == 0 and is_hashtag_allowed
        validate_subname(subname, startpos=absolute_pos, is_temp_table_start=is_temp_table_start)
        absolute_pos += len(subname) + 1  # +1 to account for the '.'
    return name

class Aliasable(ABC):
    def __init__(self, name: str, alias: str|None) -> None:
        self.name: str = name
        self.alias: str|None = alias

    @abstractmethod
    def _base_name(self) -> str: 
        pass

    def build(self, use_name: bool = True, use_alias: bool = False) -> str:
        if use_alias:
            if self.alias is None:
                return self.build(use_name=True, use_alias=False)
            if use_name:
                return self._base_name() + f" AS {self.alias}"
            return self.alias
        if use_name:
            return self._base_name()
        raise AliasException(f"A {self.__class__.__name__} cannot be described if the name of the alias was not used.")


class Field(Aliasable):
    def __init__(self, name: str,  table: Table, alias: str|None = None) -> None:
        super().__init__(name, alias)
        self.table: Table = table

    def __repr__(self) -> str:
        return f"Field(name='{self.name}', alias='{self.alias}', table='{self.table.name}')"

    def set_alias(self, alias: str) -> None:
        self.alias: str = alias

    def _base_name(self) -> str:
        return f"{self.table.build(use_name=False, use_alias=True)}.{self.name}"


class FunctionOnField(Aliasable):
    def __init__(self, name: str, before_field: str, field: Field, after_field: str = "", alias: str|None = None) -> None:
        super().__init__(name, alias)
        self.before_field: str =before_field
        self.field: Field = field
        self.after_field: str = after_field

    def _base_name(self,) -> str:
        return f"{self.before_field}{self.field.build()}{self.after_field}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name})', before_field='{self.before_field}', field={self.field}, after_field='{self.after_field}')"


class AliasableString(Aliasable):
    def __init__(self, name: str, txt: str, alias: str|None = None) -> None:
        super().__init__(name, alias)
        self.txt: str = txt

    def _base_name(self) -> str:
        return self.txt

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', txt='{self.txt}', alias='{self.alias}')"


class Fields:
    def __init__(self, table: Table, fields: list[Field|str]|None = None) -> None:
        self.table: Table = table
        self.fields:dict[str, Field] = {}
        if fields:
            self.add(*fields)

    def add(self, *fields: Field|str) -> None:
        c_fields: list[Field] = [field if isinstance(field, Field) else Field(field, self.table) for field in fields]
        for field in c_fields:
            if field.name in self.fields.keys():
                raise AlreadyExistingFieldException(f"The field '{self.table.name}.field.{field.name}' already exists.")
        for field in c_fields:
            self.fields[field.name] = field

    def as_list(self) -> list[Field]:
        return list(self.fields.values())

    def __getattr__(self, attr_name: str) -> Field:
        res: Field | None = self.fields.get(attr_name)
        if res is None:
            raise NonExistingFieldException(f"No field named '{attr_name}' in the table {self.table}.")
        return res

    def __repr__(self) -> str:
        return f"Fields(table='{self.table.name}', [{','.join(repr(field) for field in self.fields.values())}])"


class Table:
    def __init__(self, name: str, alias: str|None = None, field_names: list[str]|None = None, **kwargs) -> None:
        self.name: str = validate_name(name, kwargs.get("is_hashtag_allowed", False))
        self.alias: str|None = alias
        self.fields: Fields = Fields(self)
        if field_names:
            self.add(*field_names)

    def with_fields(self, *args, **kwargs) -> Table:
        """
        Alias to self.add()
        """
        return self.add(*args, **kwargs)

    def add(self, *fields: Field | str) -> Table:
        self.fields.add(*fields)
        return self

    def extend(self, fields: list[Field|str]) -> Table:
        return self.add(*fields)

    def has_alias(self) -> bool:
        return self.alias is not None

    def build(
        self,
        use_name: bool = False,
        use_alias: bool = True
    ) -> str:
        if not (use_name or use_alias):
            raise TableException("A Table cannot be described if none of the name and the alias are used.")
        ret: list[str] = [self.name] if use_name else []
        if use_alias:
            if self.has_alias():
                ret.append(self.alias)
            elif not use_name :
                ret.append(self.name)
        return ' '.join(ret)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', alias='{self.alias}', fields={self.fields})"


class TempTable(Table):
    def __init__(self, name: str, *fields: str | Field | Fields) -> None:
        if not isinstance(name, str):
            raise Exception("Argument 'name' is not a string.")
        super().__init__(name=f"#{name}", is_hashtag_allowed=True)
        field_names: list[str] = []
        for arg in fields:
            if isinstance(arg, Aliasable):
                field_names.append(arg.name)
            elif isinstance(arg, Fields):
                field_names.extend([field.name for field in arg.as_list()])
            else:
                field_names.append(arg)
        self.with_fields(*field_names)
