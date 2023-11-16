import uuid
from datetime import datetime, timedelta

import pytest

from src.domain.entities.event import Event
from src.domain.vo.events_args import (
    Venue,
    Location,
    Title,
    EventTime,
    Participants,
)
from tests.adapters.generator import event_generator


class TestEvent:
    @pytest.fixture
    def event(self):
        return event_generator()

    def test_event_creation(self):
        event_time = EventTime(value=datetime.now() + timedelta(days=100))
        title = Title(value="test_title")
        location = Location(value="test_location")
        venue = Venue(value="test_venue")
        number_of_participants = Participants(value=100)
        event_instance = Event.create(
            event_time, title, location, venue, number_of_participants
        )
        assert type(event_instance.event_id) is uuid.UUID
        assert event_instance.event_time == event_time
        assert event_instance.title == title
        assert event_instance.location == location
        assert event_instance.venue == venue
        assert event_instance.number_of_participants == number_of_participants
        assert (
            event_instance.creation_time.value - datetime.now()
            == timedelta(minutes=0)
        )
        assert event_instance.creation_time == event_instance.modify_time

    def test_update_time(self, event):
        """
        Test that the update time method updates the time and change the
        modify time
        :return:
        """
        new_time = EventTime(value=datetime.now() + timedelta(days=150))
        event.update_time(new_time)
        assert (
            event.event_time == new_time
            and event.modify_time.value - datetime.now()
            == timedelta(minutes=0)
        )

    def test_update_title(self, event):
        """
        Test that the update title method updates the title and change the
        modify time
        :return:
        """
        new_title = Title(value="new_title")
        event.update_title(new_title)
        assert (
            event.title == new_title
            and event.modify_time.value - datetime.now()
            == timedelta(minutes=0)
        )

    def test_update_participants(self, event):
        """
        Test that the update participants method updates the participants
        and change the modify time
        :return:
        """
        new_nop = Participants(value=200)
        event.update_participants(new_nop)
        assert (
            event.number_of_participants == new_nop
            and event.modify_time.value - datetime.now()
            == timedelta(minutes=0)
        )

    def test_update_location(self, event):
        """
        Test that the update location method updates the location and change
        the modify time
        :return:
        """
        new_location = Location(value="new_place")
        event.update_location(new_location)
        assert (
            event.location == new_location
            and event.modify_time.value - datetime.now()
            == timedelta(minutes=0)
        )

    def test_update_venue(self, event):
        """
        Test that the update venue method updates the venue and change the
        modify time
        :return:
        """
        new_venue = Venue(value="new_venue")
        event.update_venue(new_venue)
        assert (
            event.venue == new_venue
            and event.modify_time.value - datetime.now()
            == timedelta(minutes=0)
        )
