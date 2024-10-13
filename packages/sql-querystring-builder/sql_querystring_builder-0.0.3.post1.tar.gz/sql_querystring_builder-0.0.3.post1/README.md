# SqlQueryBuilder
Wraps string building of MS SQL queries.
It provides first level validation.

## Current features
1. Provides a string building facility for:
    - [x] Table
    - [x] Temporary Table
    - [x] Field
    - [x] Function on field
    - [x] String
2. Using:
    - [x] Select
    - [x] Update
    - [x] From
    - [x] InnerJoin
    - [x] Where
    - [x] OrderBy
3. Handling automatically:
    - [x] Table aliases
    - [x] Field aliases

## Not implemented (yet)
- [ ] Insert
- [ ] Compound (sub-)queries
- [ ] Functions
- [ ] Proper Conditions

## What it does not do
    Connect to a database server and run the queries by itself.
    It gives you the query as a string, it's then up to yopu to pass it to a SQL engine.

## Example
1. Define the elements of your query:
```
# Defines a Table for customers
customers_table = Table("Customers").add("id", "customerId", "mainPhone")
# Defines a Table for accounts
accounts_table = Table("Accounts", "acc").add("id", "customerId", "accountId")
# Selects the fields
select = Select(customers_table, accounts_table.fields.accountId)
# Sets an alias for an existing field
customers_table.fields.customerId.set_alias("cid")
# Specifies the table to takes as a FROM
from_ = From(customers_table)
# Specifies a temporary table for the select
atemptable = select.to_temptable("a_temp_table")
# Defines the InnerJoin
innerjoin = InnerJoin(accounts_table, accounts_table.fields.customerId, customers_table)
# Defines an Order By a defined field
orderby = OrderBy(accounts_table.fields.accountId)
# Adds a Where filter
where = Where(accounts_table.fields.accountId, "gt 20000 AND", customers_table.fields.mainPhone, "LIKE 001%")
```
2. Inspect what those elements are made of:
```
# See what the object Select looks like
print(select)
# > Select(fields=[Field(name='id', alias='None', table='Customers'),
# ...    Field(name='customerId', alias='cid', table='Customers'),
# ...    Field(name='mainPhone', alias='None', table='Customers'),
# ...    Field(name='accountId', alias='None', table='Accounts')])

# Initializes the QueryBuilder
query_builder = QueryBuilder(select, where, orderby, innerjoin, from_)
```
3. Build your query:
```
# Builds the query
query_str: str = query_builder.build()
print(query_str)
# > SELECT Customers.id, Customers.customerId, Customers.mainPhone, acc.accountId
# > INTO #a_temp_table
# > FROM Customers
# > INNER JOIN Accounts acc on acc.customerId = cid
# > WHERE acc.accountId gt 20000 AND cid LIKE 'A1C%'
# > ORDER BY cid DESC
```
4. Manipulate temporary tables which components are inferred:
```
# Is able to infer fields from temporary tables and use it as with a regular table.
temp_select = Select(atemptable)
print(temp_select)
# > Select(fields=[Field(name='id', alias='None', table='#a_temp_table'),
# ...    Field(name='customerId', alias='None', table='#a_temp_table'),
# ...    Field(name='mainPhone', alias='None', table='#a_temp_table'),
# ...    Field(name='accountId', alias='None', table='#a_temp_table')])

# Builds the query from the temporary table
print(QueryBuilder(
        temp_select,
        From(atemptable)
    ).build())
# > SELECT #a_temp_table.id, #a_temp_table.customerId, #a_temp_table.mainPhone, #a_temp_table.accountId
# > FROM #a_temp_table
```

(Find it directly in the module example.py)

## Compatible versions
Python 3.7 and above.

## Dependencies
(None)

## Authors
Wael GRIBAA
Contact: g.wael@outlook.fr
Made in September 2024