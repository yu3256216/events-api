import uuid
from typing import List

from src.domain.entities.event import Event
from src.domain.reposetories.event_reposetory import EventsRepo, Observer
from src.domain.vo.events_args import Venue, Location, RepoMethod, \
    RepoActionDetails


class EventsRepositoryImpl(EventsRepo):
    def __init__(self):
        self.events = []
        self.observers = []

    def add_observer(self, observer: Observer):
        if observer not in self.observers:
            self.observers.append(observer)
            events = self.get_all()
            observer.get_repo_state([event.as_dict() for event in events])

    def remove_observer(self, observer: Observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self, method: RepoMethod, details: RepoActionDetails):
        for observer in self.observers:
            observer.update(self, method, details)

    def add(self, new_event: Event):
        self.events.append(new_event)
        self.notify_observers(RepoMethod.CREATE,
                              RepoActionDetails(event_id=new_event.event_id,
                                                event=new_event.as_dict()))

    def delete(self, event_id: uuid.UUID):
        og_len = len(self.events)
        self.events = [event for event in self.events if
                       event.event_id != event_id]
        self.notify_observers(RepoMethod.DELETE,
                              RepoActionDetails(event_id=event_id))
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
        og_len = len(self.events)
        self.events = [event for event in self.events if
                       event.event_id != event_id]
        if og_len != len(self.events):
            self.events.append(new_event)
            self.notify_observers(RepoMethod.UPDATE,
                                  RepoActionDetails(
                                      event_id=new_event.event_id,
                                      event=new_event.as_dict()))
            return True
        else:
            return False
