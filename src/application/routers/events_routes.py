import uuid
from threading import Thread
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.application.events_sql_repo import EventsRepositorySQLImpl
from src.application.schemas.events_schemas import (
    ScheduleEvent,
    UpdateEventData,
    ReturnableEvent, SortKey,
)
from src.application.services.reminder_service import ReminderServiceImpl
from src.domain.entities.event import Event
from src.domain.reposetories.event_reposetory import EventsRepo
from src.domain.vo.events_args import (
    EventTime,
    Title,
    Location,
    Venue,
    Participants,
)

router = APIRouter(
    prefix="/events",
    tags=["events"],
)

repo = EventsRepositorySQLImpl()
reminder_service_obj = ReminderServiceImpl()
repo.add_observer(reminder_service_obj)
reminder_thread = Thread(
    target=reminder_service_obj.reminder, args=(30,), daemon=True
)
reminder_thread.start()


def get_repo():
    return repo


def sort_events(sort_key: SortKey, events: list[Event]):
    """
    Sort the events by the given key
    :param sort_key: the sort key
    :param events: the list of events to sort
    :return:
    """
    match sort_key:
        case SortKey.DATE:
            events.sort(key=lambda x: x.event_time.value, reverse=True)
        case SortKey.NUMBER_OF_PARTICIPANTS:
            events.sort(key=lambda x: x.number_of_participants.value,
                        reverse=True)
        case SortKey.CREATION_TIME:
            events.sort(key=lambda x: x.creation_time.value, reverse=True)


def parse_event_to_client(event: Event) -> ReturnableEvent:
    """
    Gets an event and make it returnable
    :param event: The event to change
    :return: the changed event
    """
    return ReturnableEvent(
        event_id=str(event.event_id),
        event_title=event.title.value,
        event_location=event.location.value,
        event_venue=event.venue.value,
        number_of_participants=event.number_of_participants.value,
        event_time=event.event_time.value.strftime(
            "%m/%d/%Y, %H:%M:%S"
        ),
    )


@router.get("/")
def get_all_events(repository: Annotated[
    EventsRepositorySQLImpl, Depends(get_repo)],
                   sort_key: SortKey | None = None
                   ):
    """
    Return a list of all the events
    :param repository: The place where the objects are saved in
    :param sort_key: the key to sort the result from
    :return: list of all the events
    """
    events = repository.get_all()
    if sort_key:
        sort_events(sort_key, events)
    return JSONResponse(
        {"message": [dict(parse_event_to_client(event)) for event in events]})


@router.post("/")
def schedule_new_event(
        item: ScheduleEvent,
        repository: Annotated[EventsRepositorySQLImpl, Depends(get_repo)],
):
    """
    Schedule new event
    :param item: the parameters to create with them the new event
    :param repository: The place where the objects are saved in
    :return:
    """
    new_event = Event.create(
        event_time=EventTime(value=item.event_time),
        title=Title(value=item.event_title),
        location=Location(value=item.event_location),
        venue=Venue(value=item.event_venue),
        number_of_participants=Participants(value=item.number_of_participants),
    )
    repository.add(new_event)
    return JSONResponse(
        content={"message": f"Event created with the ID {new_event.event_id}"})


@router.get("/{event_id}")
def get_event_by_id(
        event_id: uuid.UUID,
        repository: Annotated[EventsRepo, Depends(get_repo)],
):
    """
    Get the event details by its ID
    :param event_id: the ID of the event to retrieve
    :param repository: The place where the objects are saved in
    :return: the event details
    """
    event = repository.get_one(event_id)
    if not event:
        return JSONResponse(
            {"message": f"Event {event_id} was not found"},
            status_code=400)
    return JSONResponse(
        {"message": dict(parse_event_to_client(event))})


@router.get("/location/{location}")
def get_events_by_location(
        location: str,
        repository: Annotated[EventsRepo, Depends(get_repo)],
        sort_key: SortKey | None = None

):
    """
    Retrieve the events that are in the given location
    :param location: the location to search
    :param repository: The place where the objects are saved in
    :param sort_key: the key to sort the result from
    :return: the events details
    """
    events = repository.get_by_location(Location(value=location))
    if sort_key:
        sort_events(sort_key, events)
    return JSONResponse(
        {"message": [dict(parse_event_to_client(event)) for event in events]})


@router.get("/venue/{venue}")
def get_events_by_venue(
        venue: str,
        repository: Annotated[EventsRepo, Depends(get_repo)],
        sort_key: SortKey | None = None
):
    """
    Retrieve the events that are in the given venue
    :param venue: the venue to search
    :param repository: The place where the objects are saved in
    :param sort_key: the key to sort the result from
    :return: the events details
    """
    events = repository.get_by_venue(Venue(value=venue))
    if sort_key:
        sort_events(sort_key, events)
    return JSONResponse(
        {"message": [dict(parse_event_to_client(event)) for event in events]})


@router.put("/{event_id}")
def update_event(
        event_id: uuid.UUID,
        item: UpdateEventData,
        repository: Annotated[EventsRepo, Depends(get_repo)],
):
    """
    Update the event with the given ID
    :param event_id: the ID of the event to update
    :param item: the new data of the event
    :param repository: The place where the objects are saved in
    :return:
    """
    event_to_update = repository.get_one(event_id)
    if not event_to_update:
        return JSONResponse(
            {"message": f"Event {event_id} was not found"},
            status_code=400)
    if item.new_event_time:
        event_to_update.update_time(EventTime(value=item.new_event_time))
    if item.new_event_title:
        event_to_update.update_title(Title(value=item.new_event_title))
    if item.new_event_venue:
        event_to_update.update_venue(Venue(value=item.new_event_venue))
    if item.new_event_location:
        event_to_update.update_location(
            Location(value=item.new_event_location)
        )
    if item.new_number_of_participants:
        event_to_update.update_participants(
            Participants(value=item.new_number_of_participants)
        )
    repository.update(event_id, event_to_update)
    return JSONResponse(
        content={"message": f"Event {event_to_update.event_id} was updated"})


@router.delete("/{event_id}")
def delete_event(
        event_id: uuid.UUID,
        repository: Annotated[EventsRepo, Depends(get_repo)],
):
    """
    Delete the event with the given ID
    :param event_id: the ID of the event to delete
    :param repository: The place where the objects are saved in
    :return:
    """
    repository.delete(event_id)
    return JSONResponse(
        content={"message": f"Event {event_id} was deleted"})
