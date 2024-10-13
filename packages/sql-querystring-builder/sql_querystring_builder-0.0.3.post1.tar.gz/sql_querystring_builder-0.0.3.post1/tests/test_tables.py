from unittest import TestCase

from src.sql_querystring_builder.clauses import Select
from src.sql_querystring_builder.tables import AliasableString, FunctionOnField, Table, TempTable
from src.sql_querystring_builder.tables import AlreadyExistingFieldException, InvalidNameException, NonExistingFieldException, TableException


class TestTables(TestCase):
    def setUp(self):
        self.table1: Table = Table("testtable", "TT", field_names = ["field1", "field2])"])
        self.ttable1: TempTable = TempTable("TempT")

    def test_non_existing_field(self):
        expected_err_msg: str = "No field named 'NonExistingField' in the table "\
            "TempTable(name='#TempT', alias='None', fields=Fields(table='#TempT', []))."
        with self.assertRaises(NonExistingFieldException) as exc:
            self.ttable1.fields.NonExistingField
        self.assertEqual(str(exc.exception), expected_err_msg)

    def test_already_existing_field(self):
        expected_err_msg: str = "The field 'testtable.field.field1' already exists."
        with self.assertRaises(AlreadyExistingFieldException) as exc:
            self.table1.add("field1")
        self.assertEqual(str(exc.exception), expected_err_msg)

    def test_build_autoname(self):
        expected_result: str = "TT"
        actual_result: str = self.table1.build()
        self.assertEqual(actual_result, expected_result)

    def test_build_auto_with_name(self):
        expected_result: str = "testtable TT"
        actual_result: str = self.table1.build(use_name=True)
        self.assertEqual(actual_result, expected_result)

    def test_build_proper_name(self):
        expected_result: str = ""
        actual_result: str = self.table1.build(use_name=True, use_alias=False)
        self.assertEqual(actual_result, expected_result)

    def test_build_proper_name(self):
        expected_result: str = "TT"
        actual_result: str = self.table1.build(use_name=False, use_alias=True)
        self.assertEqual(actual_result, expected_result)

    def test_build_no_name_nor_alias(self):
        expected_err_msg: str = "A Table cannot be described if none of the name and the alias are used."
        with self.assertRaises(TableException) as exc:
            self.table1.build(use_name=False, use_alias=False)
        self.assertEqual(str(exc.exception), expected_err_msg)

    def test_valid_name(self):
        try:
            Table("a"*128)
        except InvalidNameException as exc:
            self.fail(f"Table() with name length 128 unexpectedly raised an InvalidNameException.\nException:\n{exc.exception}")
        try:
            TempTable("a"*115)
        except InvalidNameException as exc:
            self.fail(f"TempTable() with name length 115 (+1 for #) unexpectedly raised an InvalidNameException.\nException:\n{exc.exception}")

    def test_invalid_name(self):
        with self.assertRaises(InvalidNameException):
            Table("0aaa")
        with self.assertRaises(InvalidNameException):
            Table("")
        with self.assertRaises(InvalidNameException):
            Table("a"*129)
        with self.assertRaises(InvalidNameException):
            TempTable("a"*116)
        with self.assertRaises(InvalidNameException):
            Table("split name")
        with self.assertRaises(InvalidNameException):
            Table("#NotATempTable")
        with self.assertRaises(InvalidNameException) as exc:
            Table("avcà2")
        self.assertEqual(
            str(exc.exception),
            "Forbidden character 'à' was found in the name 'avcà2' at position 3. Only letters, digits and undersores are allowed."
        )

    def test_function_on_field(self):
        expected_result: str = "super_func(TT.field1some_option='good')"
        actual_result: str = FunctionOnField("some_func", "super_func(", self.table1.fields.field1, "some_option='good')", "sf").build()
        self.assertEqual(actual_result, expected_result)

    def test_aliasable_string(self):
        expected_result: str = "This txt is <hard> to parse"
        actual_result: str = AliasableString("difficult_to_parse_string", expected_result, "unparseable").build()
        self.assertEqual(actual_result, expected_result)

    def test_none_alias(self):
        table_without_alias: Table = Table("testtable", None, field_names = ["field1", "field2"])
        select = Select(table_without_alias)
        
        expected_result: str = "SELECT testtable.field1, testtable.field2"
        self.assertEqual(
            select.build(),
            expected_result
        )
