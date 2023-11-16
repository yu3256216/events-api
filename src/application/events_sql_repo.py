import uuid
from typing import List

from src.domain.entities.event import Event
from src.domain.reposetories.event_reposetory import AbstractEventsRepo
from src.domain.vo.events_args import Venue, Location


class EventsRepositorySQLImpl(AbstractEventsRepo):
    def add(self, new_event: Event):
        pass

    def delete(self, event_id: uuid.UUID):
        pass

    def get_all(self) -> List[Event]:
        pass

    def get_one(self, event_id: uuid.UUID) -> Event:
        pass

    def get_by_location(self, required_location: Location) -> List[Event]:
        pass

    def get_by_venue(self, required_venue: Venue) -> List[Event]:
        pass

    def update(self, event_id: uuid.UUID, new_event: Event):
        pass
