from unittest import TestCase

from src.sql_querystring_builder.clauses import InnerJoin, OrderBy, Select, Update, Where
from src.sql_querystring_builder.clauses import IncorrectUpdateException
from src.sql_querystring_builder.tables import Field, Table, TempTable
from src.sql_querystring_builder.tables import NonExistingFieldException


class TestClauses(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None

        self.table1: Table = Table(
            name="TestTable", 
            alias="TT",
            field_names=["TestField1", "TestField2"])
        self.table2: Table = Table(
            name="TestTable2", 
            alias="TT2",
            field_names=["TestField21", "TestField22"])

        self.select: Select = Select(
            self.table1.fields.TestField2,
            self.table2)
        self.testtemptable: TempTable = self.select.to_temptable("ttt")
        self.table1field1: Field = self.table1.fields.TestField1
        self.table1field2: Field = self.table1.fields.TestField2
        self.table2field21: Field = self.table2.fields.TestField21
        self.table2field22: Field = self.table2.fields.TestField22

    def test_init_select(self):
        self.assertEqual(
            self.select.fields,
            [self.table1field2,
             self.table2field21,
             self.table2field22]
        )

    def test_select_build(self):
        expected_result: str = "SELECT TT.TestField1, TT.TestField2, TT2.TestField21"
        actual_result: str = Select(self.table1, self.table2.fields.TestField21).build()
        self.assertEqual(actual_result, expected_result)

    def test_from_build(self):
        expected_result: str = "WHERE TT.TestField2 has a very unique condition"
        actual_result: str = Where(self.table1field2, "has a very unique condition").build()
        self.assertEqual(actual_result, expected_result)

    def test_innerjoin_ok(self):
        expected_result: str = "INNER JOIN TestTable2 TT2 on TT2.TestField22 = TT.TestField2"
        actual_result: str = InnerJoin(self.table2, self.table2field22, self.table1field2).build()
        self.assertEqual(actual_result, expected_result)

    def test_innerjoin_unexisting_infered_field(self):
        expected_err_msg: str = "No field named 'TestField22' in the table "\
            "Table(name='TestTable', alias='TT', fields=Fields(table='TestTable', "\
            "[Field(name='TestField1', alias='None', table='TestTable'),"\
            "Field(name='TestField2', alias='None', table='TestTable')]))."
        with self.assertRaises(NonExistingFieldException) as exc:
            InnerJoin(self.table2, self.table2field22, self.table1)
        self.assertEqual(str(exc.exception), expected_err_msg)

    def test_update_ok(self):
        expected_result: str = "UPDATE TT\nSET TT.TestField1='hello', TT.TestField2='world'"
        actual_result: str = Update({self.table1field1: "'hello'", self.table1field2: "'world'"}).build()
        self.assertEqual(actual_result, expected_result)

    def test_different_tables(self):
        expected_err_msg: str = "Two different tables cannot be updated in the same Update: 'TestTable' and 'TestTable2'."
        with self.assertRaises(IncorrectUpdateException) as exc:
            Update({self.table1field1: "'hello'", self.table2field21: "'world'"}).build()
        self.assertEqual(str(exc.exception), expected_err_msg)

    def test_descending(self):
        anonymous_field: Field = Field("anonymous", self.table1)
        anonymous_field2: Field = Field("anonymous2", self.table2)

        self.assertEqual(
            OrderBy(self.table1field1, True).add(anonymous_field2).build(),
            "ORDER BY TT.TestField1 DESC, TT2.anonymous2"
        )
        self.assertEqual(
            OrderBy(self.table2field21).add(anonymous_field, True).build(),
            "ORDER BY TT2.TestField21, TT.anonymous DESC"
        )
