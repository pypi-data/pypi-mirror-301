from __future__ import annotations
from operator import attrgetter

from .abstract_clause import Clause

class UnavailablePlaceException(Exception): pass

class QueryBuilder:
    def __init__(self, *initial_clauses:list[Clause]) -> None:
        self.places: dict[int, list[Clause]] = {}
        if initial_clauses:
            self.extend(initial_clauses)

    def add(self, clause: Clause) -> QueryBuilder:
        old_clause: Clause|None = self._place_is_unavailable(clause)
        if old_clause:
            raise UnavailablePlaceException(f"Cannot add a new clause with the same exclusive place in the query. New clause='{clause.build()}'. Old clause='{old_clause.build()}'")
        self.places[clause.place] = self.places.get(clause.place, []) + [clause]
        return self

    def extend(self, clauses: list[Clause]) -> QueryBuilder:
        for clause in clauses:
            self.add(clause)
        return self

    def build(self) -> str:
        return "\n".join(clause.build() for clause in self._sorted_clauses())

    def _place_is_unavailable(self, clause: Clause) -> Clause|None:
        if clause.place in self.places and clause.is_exclusive:
            return self.places[clause.place][0]

    def _sorted_clauses(self) -> list[Clause]:
        return [clause for _, clauses in sorted(self.places.items()) for clause in clauses]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(str(clause) for clause in self._sorted_clauses())})"
