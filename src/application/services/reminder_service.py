import logging
import time
from datetime import timedelta, datetime, timezone
from typing import Dict

from src.domain.services.reminder import ReminderService
from src.domain.vo.events_args import RepoMethod, RepoActionDetails


class ReminderServiceImpl(ReminderService):
    def __init__(self):
        self.events_repo = []

    def get_repo_state(self, repo: list[Dict]):
        self.events_repo = repo

    def update(self, method: RepoMethod, details: RepoActionDetails):
        match method:
            case RepoMethod.CREATE:
                self.events_repo.append(details.event)
            case RepoMethod.DELETE:
                self.events_repo = [e for e in self.events_repo if
                                    e["event_id"] != details.event_id]
            case RepoMethod.UPDATE:
                self.events_repo = [e for e in self.events_repo if
                                    e["event_id"] != details.event_id]
                self.events_repo.append(details.event)

    def reminder(self, time_before: int):
        """
        Remind before the events starts
        :param time_before: the time before the event starts to remind
        :return: None
        """
        check_time = datetime.now()
        print("started")
        logging.debug(msg="Start checking the events for the reminder")
        while True:
            if check_time + timedelta(minutes=1):
                check_time = datetime.now()
                for event in self.events_repo:
                    event_time = datetime.strptime(
                        event["event_time"], "%m/%d/%Y, %H:%M:%S")
                    if event_time - timedelta(minutes=30) == datetime.utcnow():
                        print("its time")
                        logging.debug(
                            f"The event {event.title.value}"
                            f" will start in 30min")
            else:
                time.sleep(1)
