import uuid
from typing import List

from src.domain.entities.event import Event
from src.domain.reposetories.event_reposetory import EventsRepo
from src.domain.vo.events_args import Venue, Location


class EventsRepositoryImpl(EventsRepo):
    def __init__(self):
        self.events = []

    def add(self, new_event: Event):
        self.events.append(new_event)

    def delete(self, event_id: uuid.UUID):
        og_len = len(self.events)
        self.events = [event for event in self.events if
                       event.event_id != event_id]
        return og_len != len(self.events)

    def get_all(self) -> List[Event]:
        return self.events

    def get_one(self, event_id: uuid.UUID) -> Event:
        for event in self.events:
            if event.event_id == event_id:
                return event

    def get_by_location(self, required_location: Location) -> List[Event]:
        return [
            event
            for event in self.events
            if event.location == required_location
        ]

    def get_by_venue(self, required_venue: Venue) -> List[Event]:
        return [
            event for event in self.events if event.venue == required_venue
        ]

    def update(self, event_id: uuid.UUID, new_event: Event):
        if self.delete(event_id):
            self.events.append(new_event)
            return True
        else:
            return False
