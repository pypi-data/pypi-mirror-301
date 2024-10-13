from unittest import TestCase

from src.sql_querystring_builder.clauses import From, InnerJoin, OrderBy, Select, Where
from src.sql_querystring_builder.query_builder import QueryBuilder, UnavailablePlaceException
from src.sql_querystring_builder.tables import AliasableString, FunctionOnField, Table, TempTable


class TestQueries(TestCase):
    def setUp(self) -> None:
        self.table_1 = Table("table1", "t1", field_names=["KeyId", "id", "card", "account"])
        self.table_2 = Table("table2", "t2").with_fields("id", "KeyValue")
        self.table_3 = Table("table3", "t3").with_fields("KeyValue")
        self.table_1.fields.id.set_alias("CustomerId")
        self.table_1.fields.KeyId.set_alias("CustomerKeyId")
        self.agg_func = FunctionOnField("sum of card", "SUM(", self.table_1.fields.card, ')', "total_card")
        self.alias_string = AliasableString("cstring", "Unparseable_Custom_string", "cstring")
        self.where = Where(self.table_1.fields.KeyId, "= 123456")
        self.select = Select(self.table_1, self.table_2.fields.KeyValue, self.agg_func, self.alias_string)
        self.innerjoin = InnerJoin(self.table_2, self.table_2.fields.id, self.table_1)
        self._from = From(self.table_1)
        self.orderby = OrderBy(self.table_1.fields.KeyId, descending=True).add(self.table_2.fields.KeyValue).add(self.alias_string)
        self.temp_table = self.select.to_temptable("Biscuit")
        self.innerjoin2 = InnerJoin(self.table_3, self.table_3.fields.KeyValue, self.table_2)

    def test_query(self):
        expected_result: str = """SELECT t1.KeyId AS CustomerKeyId, t1.id AS CustomerId, t1.card, t1.account, t2.KeyValue, SUM(t1.card) AS total_card, Unparseable_Custom_string AS cstring
INTO #Biscuit
FROM table1 t1
INNER JOIN table2 t2 on t2.id = t1.id
INNER JOIN table3 t3 on t3.KeyValue = t2.KeyValue
WHERE t1.KeyId = 123456
ORDER BY CustomerKeyId DESC, t2.KeyValue, cstring"""
        actual_result: str = QueryBuilder(self.select, self.where, self. innerjoin, self.innerjoin2, self._from, self.orderby).build()
        self.assertEqual(actual_result, expected_result)

    
    def test_unavailable_place(self):
        qb = QueryBuilder(self.select, self._from)
        with self.assertRaises(UnavailablePlaceException) as exc:
            qb.add(From(self.table_2))
        self.assertEqual(
            str(exc.exception),
            "Cannot add a new clause with the same exclusive place in the query. New clause='FROM table2 t2'. Old clause='FROM table1 t1'"
        )
