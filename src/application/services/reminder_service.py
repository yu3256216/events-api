import logging
import time
from datetime import timedelta, datetime
from typing import Dict

from src.domain.services.reminder import ReminderService
from src.domain.event.events_args import RepoMethod, RepoActionDetails


class ReminderServiceImpl(ReminderService):
    def __init__(self):
        self.events_repo = []

    def get_repo_state(self, repo: list[Dict]):
        self.events_repo = repo

    def update(self, method: RepoMethod, details: RepoActionDetails):
        match method:
            case RepoMethod.CREATE:
                event_to_add = details.event
                event_to_add["checked"] = False
                self.events_repo.append(event_to_add)
            case RepoMethod.DELETE:
                self.events_repo = [e for e in self.events_repo if
                                    e["event_id"] != details.event_id]
            case RepoMethod.UPDATE:
                repo_copy_wo_obj = []
                for e in self.events_repo:
                    if e["event_id"] != details.event_id:
                        repo_copy_wo_obj.append(e)
                    else:
                        if details.event["event_time"] != e["event_time"]:
                            to_check = True
                        else:
                            to_check = not e.get("checked", False)
                event_to_add = details.event
                event_to_add["checked"] = not to_check
                self.events_repo.append(event_to_add)

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
                    if event_time - timedelta(
                            minutes=30) < datetime.utcnow() < event_time \
                            and not event.get("checked", False):
                        print("its time")
                        logging.debug(
                            f"The event {event['title']}"
                            f" will start in 30min")
                        event['checked'] = True
            else:
                time.sleep(1)
