from uuid import UUID

from pydantic import BaseModel, PositiveInt, Extra, FutureDatetime


class ReturnableEvent(BaseModel):
    event_id: str
    event_title: str
    event_location: str
    event_venue: str
    number_of_participants: PositiveInt
    event_time: str

    class Config:
        extra = Extra.forbid


class ScheduleEvent(BaseModel):
    event_title: str
    event_location: str
    event_venue: str
    number_of_participants: PositiveInt
    event_time: FutureDatetime

    class Config:
        extra = Extra.forbid


class GetEventsByLocation(BaseModel):
    location: str

    class Config:
        extra = Extra.forbid


class GetEventsByVenue(BaseModel):
    venue: str

    class Config:
        extra = Extra.forbid


class GetEventsDetails(BaseModel):
    event_id: UUID

    class Config:
        extra = Extra.forbid


class UpdateEvent(BaseModel):
    event_id: UUID
    new_event_title: str | None = None
    new_event_location: str | None = None
    new_event_venue: str | None = None
    new_number_of_participants: PositiveInt | None = None
    new_event_time: FutureDatetime | None = None

    class Config:
        extra = Extra.forbid


class UpdateEventData(BaseModel):
    new_event_title: str | None = None
    new_event_location: str | None = None
    new_event_venue: str | None = None
    new_number_of_participants: PositiveInt | None = None
    new_event_time: FutureDatetime | None = None

    class Config:
        extra = Extra.forbid


class DeleteEvent(BaseModel):
    event_id: UUID

    class Config:
        extra = Extra.forbid
