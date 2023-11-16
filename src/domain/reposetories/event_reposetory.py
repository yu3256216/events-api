import uuid
from abc import ABC, abstractmethod
from typing import List

from src.domain.entities.event import Event
from src.domain.vo.events_args import Location, Venue


class AbstractEventsRepo(ABC):
    @abstractmethod
    def add(self, new_event: Event):
        """
        Add new event to the repo
        :param new_event: the new event to add
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, event_id: uuid.UUID):
        """
        delete an event from the repo
        :param event_id: the event's id to delete
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Event]:
        """
        Retrieve all the events from the repo
        :return: the entire events in the repo
        """
        raise NotImplementedError

    @abstractmethod
    def get_one(self, event_id: uuid.UUID) -> Event:
        """
        Retrieve the event with the given id from the repo
        :param event_id: the event id to search
        :return: the event with the given ID
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_location(self, required_location: Location) -> List[Event]:
        """
        Retrieve all the events from the repo that take place in the
        given location
        :return: the found events in the repo
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_venue(self, required_venue: Venue) -> List[Event]:
        """
        Retrieve all the events from the repo that take place in the
        given venue
        :return: the found events in the repo
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, event_id: uuid.UUID, new_event: Event):
        """
        Update the event in the repository
        :param event_id: the id of the event to update
        :param new_event: the new values of the event
        :return: the found events in the repo
        """
        raise NotImplementedError
