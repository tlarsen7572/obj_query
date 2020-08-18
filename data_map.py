from query import Retriever
from typing import Callable, Any, Dict


class DataMap:
    def __init__(self, queries: Dict[Callable[[Any], Any], Retriever]):
        self.Queries: Dict[Callable[[Any], Any], Retriever] = queries

    def transfer(self, obj):
        for setter, getter in self.Queries.items():
            setter(getter.get_from(obj))
