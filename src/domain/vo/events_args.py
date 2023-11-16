from abc import ABC
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BaseVO(ABC):
    def type_validator(self):
        """
        Validate the types of the dataclass arguments
        :return: True if valid, false either
        """
        for field_name, field_def in self.__dataclass_fields__.items():
            actual_type = type(getattr(self, field_name))
        if actual_type != field_def.type:
            return False
        return True

    def __post_init__(self):
        if not self.type_validator():
            raise ValueError("Wrong types")


@dataclass
class Title(BaseVO):
    value: str


@dataclass
class Location(BaseVO):
    value: str


@dataclass
class Venue(BaseVO):
    value: str


@dataclass
class Participants(BaseVO):
    value: int

    def __post_init__(self):
        """
        Validate that the number is positive
        :return:
        """
        if type(self.value) is not int or self.value < 0 or \
                self.value > 10 ** 200:
            raise ValueError


@dataclass
class Time(BaseVO):
    value: datetime


@dataclass
class EventTime(Time):
    def __post_init__(self):
        """
        validate that the event date is in the future
        :return: None (void function)
        """
        if self.value < datetime.now():
            # TODO new exception
            raise ValueError
