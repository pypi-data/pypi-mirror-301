# SqlQueryBuilder
Wraps string building of MS SQL queries.
It provides first level validation.

## Current features
Providies a string building facility for:
    Table
    Temporary Table
    Field
    Function on field
    String
Using:
    Select
    Update
    From
    InnerJoin
    Where
    OrderBy

## Not implemented (yet)
    Insert
    Compound (sub-)queries
    Functions
    Proper Conditions

## What it does not do
    Connect to a database server and run the queries by itself.
    It gives you the query as a string, it's then up to yopu to pass it to a SQL engine.

## Example
Find it directly in the module example.py

## Compatible versions
Python 3.7 and above.

## Dependencies
(None)

## Authors
Wael GRIBAA
Contact: g.wael@outlook.fr
Made in September 2024