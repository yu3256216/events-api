import uuid
from datetime import datetime
from typing import List, Dict

from src.application.utils.sqlite_handler import SQLiteHandler
from src.domain.entities.event import Event
from src.domain.reposetories.event_reposetory import EventsRepo, Observer
from src.domain.vo.events_args import Venue, Location, Title, \
    Participants, Time, RepoMethod, RepoActionDetails


class EventsRepositorySQLImpl(EventsRepo):
    def __init__(self):
        self.db_name = "events.db"
        self.table_name = "events"
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
        item_to_insert = new_event.as_dict()
        SQLiteHandler.insert(self.db_name, self.table_name, item_to_insert)
        self.notify_observers(RepoMethod.CREATE,
                              RepoActionDetails(event_id=new_event.event_id,
                                                event=item_to_insert))

    def delete(self, event_id: uuid.UUID):
        SQLiteHandler.delete(
            self.db_name, self.table_name, "event_id", str(event_id)
        )
        self.notify_observers(RepoMethod.DELETE,
                              RepoActionDetails(event_id=new_event.event_id))

    def get_all(self) -> List[Event]:
        data = SQLiteHandler.read_all_table(self.db_name, self.table_name)
        return [self.from_row_to_event(row) for row in data]

    def get_one(self, event_id: uuid.UUID) -> Event:
        res = SQLiteHandler.read_with_conditions(
            self.db_name, self.table_name, "event_id", str(event_id)
        )[0]
        return self.from_row_to_event(res)

    def get_by_location(self, required_location: Location) -> List[Event]:
        res = SQLiteHandler.read_with_conditions(
            self.db_name, self.table_name, "location", required_location.value
        )
        return [self.from_row_to_event(row) for row in res]

    def get_by_venue(self, required_venue: Venue) -> List[Event]:
        res = SQLiteHandler.read_with_conditions(
            self.db_name, self.table_name, "venue", required_venue.value
        )
        return [self.from_row_to_event(row) for row in res]

    def update(self, event_id: uuid.UUID, new_event: Event):
        item_to_insert = new_event.as_dict()
        SQLiteHandler.update(
            self.db_name,
            self.table_name,
            "event_id",
            str(event_id),
            item_to_insert,
        )
        self.notify_observers(RepoMethod.UPDATE,
                              RepoActionDetails(event_id=new_event.event_id,
                                                event=item_to_insert))

    @staticmethod
    def from_row_to_event(row: tuple) -> Event:
        """
        Gets a row that retrieved from the db and parse it to load it to event
        object
        :param row: the row that retrieved
        :return: the object with the data from the DB
        """
        return Event(
            event_id=row[0],
            event_time=Time(
                value=datetime.strptime(row[1], "%m/%d/%Y, %H:%M:%S")),
            title=Title(value=row[2]),
            location=Location(value=row[3]),
            venue=Venue(value=row[4]),
            number_of_participants=Participants(value=row[5]),
            creation_time=Time(
                value=datetime.strptime(row[6], "%m/%d/%Y, %H:%M:%S")),
            modify_time=Time(
                value=datetime.strptime(row[7], "%m/%d/%Y, %H:%M:%S")),
        )
