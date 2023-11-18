from abc import ABC, abstractmethod

from src.domain.event.event_reposetory import Observer


class ReminderService(Observer, ABC):
    @abstractmethod
    def reminder(self, time_before: int):
        """
        Remind before the events starts
        :param time_before: the time before the event starts to remind
        :return: None
        """
        raise NotImplementedError
