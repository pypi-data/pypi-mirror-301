import typing as t
from datetime import datetime
from dateutil.parser import parse
from enum import Enum


class ComObject:
    com_object: t.Any

    def __init__(self, obj):
        self.com_object = obj


Instance = t.TypeVar("Instance")


class ComField(t.Generic[Instance]):

    _com_field: str
    _com_type: t.Any

    def __init__(self, com_field: str, com_type: t.Type[t.Any] = None):
        self._com_field = com_field
        self._com_type = com_type

    def __get__(self, instance: ComObject, owner: t.Type[Instance]):
        value = getattr(instance.com_object, self._com_field)
        if self._com_type:
            return self._com_type(value)
        return value

    def _assert_type(self, value) -> bool:
        if self._com_type:
            return isinstance(value, self._com_type)
        return True

    def __set__(self, obj: ComObject, value: t.Any):
        if isinstance(value, (ComObject, ComField)):
            raise Exception("Attempting to set a com value with a Com Object. Primitive values only.")
        type_okay = self._assert_type(value)
        if type_okay:
            setattr(obj.com_object, self._com_field, value)
            return
        coerced_value = self._com_type(value)
        type_okay = self._assert_type(coerced_value)
        if type_okay:
            setattr(obj.com_object, self._com_field, coerced_value)


def get_local_tz():
    return datetime.now().astimezone().tzinfo


def local_datetime(year, month, day, hour=0, minute=0) -> datetime:
    return datetime(year=year, month=month, day=day, hour=hour, minute=minute, tzinfo=get_local_tz())


class DateTimeComField(t.Generic[Instance]):
    """
    Required date time format: 2010-10-14T17:00:00-07:00

    """
    _com_field: str
    _date_fmt = "%Y-%m-%dT%H:%M:%S"
    _zone_fmt = "%z"

    def __init__(self, com_field: str):
        self._com_field = com_field

    def __get__(self, instance: ComObject, owner: t.Type[Instance]):
        value = getattr(instance.com_object, self._com_field)
        if not value:
            return datetime(1900, 1, 1) 
        return parse(value)

    def __set__(self, obj: ComObject, value: datetime):
        if not isinstance(value, datetime):
            raise Exception(
                "Attempting to set a com value with a Com Object. Datetime values only."
            )
        coerced_value = value.strftime(self._date_fmt)
        zone_format = value.strftime("%z")
        if len(zone_format) == 5:
            zone_format = zone_format[:3] + ":" + zone_format[3:]
            coerced_value = coerced_value + zone_format
        setattr(obj.com_object, self._com_field, coerced_value)



class EnumComField(t.Generic[Instance]):
    _com_field: str
    _enum_type: t.Type[Enum]

    def __init__(self, com_field: str, enum_type: t.Type[Enum]):
        self._com_field = com_field
        self._enum_type = enum_type

    def __get__(self, instance: ComObject, owner: t.Type[Instance]):
        value = getattr(instance.com_object, self._com_field)
        return self._enum_type(value)

    def __set__(self, obj: ComObject, value: Enum):
        if not isinstance(value, self._enum_type):
            raise Exception("Attempting to set a com value with a Com Object. Expecting an Enum type.")
        setattr(obj.com_object, self._com_field, value.value)