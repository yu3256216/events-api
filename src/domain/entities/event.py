import uuid
from datetime import datetime

from src.domain.vo.events_args import EventTime, Venue, Location, Title, Time, \
    Participants


class Event:
    def __init__(
        self,
        event_id: uuid,
        event_time: EventTime,
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
