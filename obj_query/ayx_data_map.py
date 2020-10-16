import datetime
from typing import Dict, Tuple, Callable, Any
from obj_query.data_map import DataMap
from obj_query.query import Retriever
from enum import Enum
import AlteryxPythonSDK as Sdk


class FieldType(Enum):
    Bool = 0
    String = 1
    Integer = 2
    Decimal = 3
    Datetime = 4


class AyxDataMap:
    def __init__(self, engine, source: str, fields: Dict[Tuple[str, FieldType], Retriever]):
        self.Info = Sdk.RecordInfo(engine)
        for field in fields.keys():
            name = field[0]
            field_type = field[1]
            if field_type == FieldType.Bool:
                self.Info.add_field(name, Sdk.FieldType.bool, source=source)
            elif field_type == FieldType.String:
                self.Info.add_field(name, Sdk.FieldType.v_wstring, source=source, size=117374182)
            elif field_type == FieldType.Integer:
                self.Info.add_field(name, Sdk.FieldType.int64, source=source)
            elif field_type == FieldType.Decimal:
                self.Info.add_field(name, Sdk.FieldType.double, source=source)
            elif field_type == FieldType.Datetime:
                self.Info.add_field(name, Sdk.FieldType.datetime, source=source)
        self._Creator = self.Info.construct_record_creator()

        data_map: Dict[Callable[[Any], Any], Retriever] = {}
        for field, retriever in fields.items():
            ayx_field = self.Info.get_field_by_name(field[0])
            field_type = field[1]
            setter = None
            if field_type == FieldType.Bool:
                setter = _set_bool(ayx_field, self._Creator)
            elif field_type == FieldType.String:
                setter = _set_string(ayx_field, self._Creator)
            elif field_type == FieldType.Integer:
                setter = _set_integer(ayx_field, self._Creator)
            elif field_type == FieldType.Decimal:
                setter = _set_decimal(ayx_field, self._Creator)
            elif field_type == FieldType.Datetime:
                setter = _set_datetime(ayx_field, self._Creator)
            data_map[setter] = retriever
        self._DataMap = DataMap(data_map)

    def transfer(self, obj) -> Sdk.RecordRef:
        self._Creator.reset()
        self._DataMap.transfer(obj)
        return self._Creator.finalize_record()


def _set_bool(field: Sdk.Field, creator: Sdk.RecordCreator):
    def _setter(value):
        if value is None or not isinstance(value, bool):
            field.set_null(creator)
            return
        field.set_from_bool(creator, value)
    return _setter


def _set_string(field: Sdk.Field, creator: Sdk.RecordCreator):
    def _setter(value):
        if value is None or not isinstance(value, str):
            field.set_null(creator)
            return
        field.set_from_string(creator, value)
    return _setter


def _set_integer(field: Sdk.Field, creator: Sdk.RecordCreator):
    def _setter(value):
        if value is None or not (isinstance(value, int) or isinstance(value, float)):
            field.set_null(creator)
            return
        field.set_from_int64(creator, int(value))
    return _setter


def _set_decimal(field: Sdk.Field, creator: Sdk.RecordCreator):
    def _setter(value):
        if value is None or not (isinstance(value, int) or isinstance(value, float)):
            field.set_null(creator)
            return
        field.set_from_double(creator, float(value))
    return _setter


def _set_datetime(field: Sdk.Field, creator: Sdk.RecordCreator):
    def _setter(value):
        if value is None or not (isinstance(value, datetime.time) or isinstance(value, datetime.datetime)):
            field.set_null(creator)
            return
        field.set_from_string(creator, value.strftime("%Y-%m-%d %H:%M:%S"))
    return _setter
