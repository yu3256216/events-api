from datetime import timedelta, datetime, timezone

from src.domain.entities.event import Event
from src.domain.vo.events_args import (
    EventTime,
    Title,
    Location,
    Venue,
    Participants,
)


def event_generator() -> Event:
    """
    Generate an event
    :return: the generated event
    """
    event_time = datetime.now().replace(
        tzinfo=timezone.utc) + timedelta(days=100)
    return Event.create(
        event_time=EventTime(value=event_time),
        title=Title(value="test_title"),
        location=Location(value="test_location"),
        venue=Venue(value="test_venue"),
        number_of_participants=Participants(value=100),
    )
