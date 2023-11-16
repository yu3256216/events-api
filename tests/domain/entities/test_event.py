import uuid
from datetime import datetime, timedelta

from src.domain.entities.event import Event
from src.domain.vo.events_args import Venue, Location, Title, EventTime


def test_event_creation():
    event_time = EventTime(value=datetime.now() + timedelta(days=100))
    title = Title(value="test_title")
    location = Location(value="test_location")
    venue = Venue(value="test_venue")
    event_instance = Event.create(event_time, title, location, venue)
    assert type(event_instance.event_id) is uuid.UUID
    assert event_instance.event_time == event_time
    assert event_instance.title == title
    assert event_instance.location == location
    assert event_instance.venue == venue
    assert event_instance.creation_time.value - datetime.now() == timedelta(
        minutes=0
    )
    assert event_instance.creation_time == event_instance.modify_time
