import uuid
from abc import ABC, abstractmethod
from typing import List, Dict

from src.domain.event.event import Event
from src.domain.event.events_args import Location, Venue, RepoMethod, \
    RepoActionDetails


class Observer(ABC):

    @abstractmethod
    def get_repo_state(self, repo: list[Dict]):
        """
        Gets the current state of the repo
        :param repo: the full repo
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, method: RepoMethod, details: RepoActionDetails):
        """
        Gets the current state of the repo
        :param method: the method that occurred
        :param details: the method details
        :return: None
        """
        raise NotImplementedError


class EventsRepo(ABC):
    @abstractmethod
    def add_observer(self, observer: Observer):
        """
        Add observer
        :param observer: the observer to add
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def remove_observer(self, observer: Observer):
        """
        remove observer of the repo
        :param observer: the observer to remove
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def notify_observers(self, method: RepoMethod, details: RepoActionDetails):
        """
        Notify Observers of the change
        :param method: the method that occurred
        :param details: the method details
        :return: None
        """
        raise NotImplementedError

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
        :raises: EventDoesntExists: if the event wasn't found
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
        :raises: EventDoesntExists: if the event wasn't found
        """
        raise NotImplementedError
