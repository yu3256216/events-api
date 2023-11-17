import uuid
from datetime import datetime

from src.domain.vo.events_args import (
    EventTime,
    Venue,
    Location,
    Title,
    Time,
    Participants,
)


class Event:
    def __init__(
        self,
        event_id: uuid,
        event_time: Time,
        title: Title,
        location: Location,
        venue: Venue,
        number_of_participants: Participants,
        creation_time: Time,
        modify_time: Time,
    ):
        self.event_id = event_id
        self.event_time = event_time
        self.title = title
        self.number_of_participants = number_of_participants
        self.location = location
        self.venue = venue
        self.creation_time = creation_time
        self.modify_time = modify_time

    def update_time(self, new_time: EventTime):
        """
        Update event's time
        :param new_time: the new event's time
        :return:
        """
        self.event_time = new_time
        self.modify_time = Time(value=datetime.now())

    def update_title(self, new_title: Title):
        """
        Update event's title
        :param new_title: the event's new title
        :return:
        """
        self.title = new_title
        self.modify_time = Time(value=datetime.now())

    def update_participants(self, new_number_of_participants: Participants):
        """
        Update event's number of participants
        :param new_number_of_participants: the new number of participants in
        the event
        :return:
        """
        self.number_of_participants = new_number_of_participants
        self.modify_time = Time(value=datetime.now())

    def update_location(self, new_location: Location):
        """
        Update event's location
        :param new_location:
        :return:
        """
        self.location = new_location
        self.modify_time = Time(value=datetime.now())

    def update_venue(self, new_venue: Venue):
        """
        Update event's venue
        :param new_venue: the new event's venue
        :return:
        """
        self.venue = new_venue
        self.modify_time = Time(value=datetime.now())

    def as_dict(self):
        """
        :return: The Objects values in a dict
        """
        return {
            "event_id": str(self.event_id),
            "event_time": self.event_time.value.strftime(
                "%m/%d/%Y, %H:%M:%S"
            ),
            "title": self.title.value,
            "number_of_participants": self.number_of_participants.value,
            "location": self.location.value,
            "venue": self.venue.value,
            "creation_time": self.creation_time.value.strftime(
                "%m/%d/%Y, %H:%M:%S"
            ),
            "modify_time": self.modify_time.value.strftime(
                "%m/%d/%Y, %H:%M:%S"
            ),
        }

    @classmethod
    def create(
        cls,
        event_time: EventTime,
        title: Title,
        location: Location,
        venue: Venue,
        number_of_participants: Participants,
    ):
        """
        Function to create a new event
        :param event_time: the time of the event
        :param title: the event's title
        :param location: the event's location
        :param venue: the venue that the event going to take place in
        :param number_of_participants: the number of participants
        :return: instance of the event
        """
        creation_time = Time(value=datetime.now())
        instance = cls(
            uuid.uuid4(),
            event_time,
            title,
            location,
            venue,
            number_of_participants,
            creation_time,
            creation_time,
        )
        return instance
