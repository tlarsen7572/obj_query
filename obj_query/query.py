import datetime
from typing import List


class Retriever:
    def __init__(self, operations: List):
        self.Operations = operations

    def get_from(self, obj):
        value = obj
        for operation in self.Operations:
            value = operation(value)
        return value


class Query:
    def __init__(self):
        self.Operations = []

    def get(self, attr_or_key: str):
        def _get(obj):
            if obj is None:
                return None
            if hasattr(obj, attr_or_key):
                return getattr(obj, attr_or_key)
            try:
                return obj[attr_or_key]
            except:
                return None
        self.Operations.append(_get)
        return self

    def index(self, index: int):
        def _index(items):
            try:
                return items[index]
            except:
                return None
        self.Operations.append(_index)
        return self

    def first(self):
        def _first(items):
            try:
                return items[0]
            except:
                return None
        self.Operations.append(_first)
        return self

    def last(self):
        def _last(items):
            try:
                return items[-1]
            except:
                return None
        self.Operations.append(_last)
        return self

    def to_datetime(self, date_format: str):
        def _to_datetime(obj):
            try:
                return datetime.datetime.strptime(obj, date_format)
            except:
                return None
        self.Operations.append(_to_datetime)
        return self

    def finalize(self) -> Retriever:
        return Retriever(self.Operations)
