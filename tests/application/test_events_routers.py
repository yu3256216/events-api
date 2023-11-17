import uuid
from datetime import datetime, timezone
from typing import Dict

import pytest
from fastapi.testclient import TestClient

from src.application.routers.events_routes import router
from src.domain.entities.event import Event
from tests.adapters.generator import event_generator
from tests.adapters.repository_implementation import EventsRepositoryImpl


class TestEventsRoutes:
    test_repo = EventsRepositoryImpl()

    @staticmethod
    def expected_returns_event(event: Event) -> Dict[str, str | int]:
        """
        Gets an event and return how it should be returned to the use
        :param event: The event to change
        :return: the changed event
        """
        return {
            "event_id": str(event.event_id),
            "event_title": event.title.value,
            "event_location": event.location.value,
            "event_venue": event.venue.value,
            "number_of_participants": event.number_of_participants.value,
            "event_time": event.event_time.value.strftime("%m/%d/%Y, %H:%M:%S")
        }

    @pytest.fixture(autouse=True)
    def generate_events_to_repo(self):
        self.test_repo.add(event_generator())

    @pytest.fixture
    def client(self):
        return TestClient(router)

    def test_get_all_events(self, client, mocker):
        mocker.patch(
            'src.application.events_sql_repo.EventsRepositorySQLImpl.get_all',
            self.test_repo.get_all,
        )
        response = client.get("/events")
        content = response.json()
        assert response.status_code == 200 and content["message"] == [
            self.expected_returns_event(event) for event
            in self.test_repo.get_all()
        ]

    def test_schedule_new_event(self, client, mocker):
        mocker.patch(
            'src.application.events_sql_repo.EventsRepositorySQLImpl.add',
            self.test_repo.add,
        )
        response = client.post("/events",
                               json={
                                   "event_title": "Yuv1",
                                   "event_location": "Ramat Hasharon",
                                   "event_venue": "Mi Casa",
                                   "number_of_participants": 10,
                                   "event_time": "2023-12-10T10:51:36.347Z"
                               })
        assert response.status_code == 200

    def test_schedule_new_event_with_exists_details(self, client, mocker):
        mocker.patch(
            'src.application.events_sql_repo.EventsRepositorySQLImpl.add',
            self.test_repo.add,
        )
        current_repo = self.test_repo.get_all()
        event = current_repo[0]
        response = client.post("/events",
                               json={
                                   "event_title": event.title.value,
                                   "event_location": event.location.value,
                                   "event_venue": event.venue.value,
                                   "number_of_participants":
                                       event.number_of_participants.value,
                                   "event_time": str(event.event_time.value)
                               })
        assert response.status_code == 200 and response.content

    def test_get_event_by_id(self, client, mocker):
        mocker.patch(
            'src.application.events_sql_repo.EventsRepositorySQLImpl.get_one',
            self.test_repo.get_one,
        )
        current_repo = self.test_repo.get_all()
        event = current_repo[0]
        response = client.get(f"/events/{str(event.event_id)}")
        assert response.status_code == 200 and \
               response.json()["message"] == self.expected_returns_event(event)

    def test_get_event_by_new_id(self, client, mocker):
        mocker.patch(
            'src.application.events_sql_repo.EventsRepositorySQLImpl.get_one',
            self.test_repo.get_one,
        )
        response = client.get(f"/events/{str(uuid.uuid4())}")
        assert response.status_code == 400

    def test_get_events_by_location(self, client, mocker):
        mocker.patch(
            'src.application.events_sql_repo.EventsRepositorySQLImpl.'
            'get_by_location',
            self.test_repo.get_by_location,
        )
        current_repo = self.test_repo.get_all()
        event = current_repo[0]
        response = client.get(f"/events/location/{event.location.value}")
        assert response.status_code == 200 \
               and response.json()["message"] == [
                   self.expected_returns_event(e)
                   for e in current_repo if e.location == event.location]

    def test_get_events_by_new_location(self, client, mocker):
        mocker.patch(
            'src.application.events_sql_repo.EventsRepositorySQLImpl.'
            'get_by_location',
            self.test_repo.get_by_location,
        )
        response = client.get(f"/events/location/{str(uuid.uuid4())}")
        assert response.status_code == 200 and response.json()["message"] == []

    def test_get_events_by_venue(self, client, mocker):
        mocker.patch(
            'src.application.events_sql_repo.EventsRepositorySQLImpl.'
            'get_by_venue',
            self.test_repo.get_by_venue,
        )
        current_repo = self.test_repo.get_all()
        event = current_repo[0]
        response = client.get(f"/events/venue/{event.venue.value}")
        assert response.status_code == 200 \
               and response.json()["message"] == [
                   self.expected_returns_event(e)
                   for e in current_repo if e.venue == event.venue]

    def test_get_events_by_new_venue(self, client, mocker):
        mocker.patch(
            'src.application.events_sql_repo.EventsRepositorySQLImpl.'
            'get_by_venue',
            self.test_repo.get_by_venue,
        )
        response = client.get(f"/events/venue/{str(uuid.uuid4())}")
        assert response.status_code == 200

    def test_update_event(self, client, mocker):
        mocker.patch(
            'src.application.events_sql_repo.EventsRepositorySQLImpl.get_one',
            self.test_repo.get_one,
        )
        mocker.patch(
            'src.application.events_sql_repo.EventsRepositorySQLImpl.update',
            self.test_repo.update,
        )
        current_repo = self.test_repo.get_all()
        event = current_repo[0]
        new_nop = event.number_of_participants.value + 1
        response = client.put(f"/events/{str(event.event_id)}",
                              json={
                                   "new_event_title": "changed",
                                   "new_event_location": "changed",
                                   "new_event_venue": "changed",
                                   "new_number_of_participants": new_nop,
                                   "new_event_time": "2600-12-10T10:51:36.347Z"
                               })
        updated_event = self.test_repo.get_one(event.event_id)
        assert response.status_code == 200 and\
               updated_event.event_time.value == \
               datetime.fromisoformat("2600-12-10T10:51:36.347").\
                   replace(tzinfo=timezone.utc) \
               and updated_event.title.value == "changed" \
               and updated_event.location.value == "changed" \
               and updated_event.venue.value == "changed" \
               and updated_event.number_of_participants.value == new_nop

    def test_update_new_event(self, client, mocker):
        mocker.patch(
            'src.application.events_sql_repo.EventsRepositorySQLImpl.get_one',
            self.test_repo.get_one,
        )
        mocker.patch(
            'src.application.events_sql_repo.EventsRepositorySQLImpl.update',
            self.test_repo.update,
        )
        response = client.put(f"/events/{str(uuid.uuid4())}",
                              json={
                                  "new_event_title": "changed",
                                  "new_event_location": "changed",
                                  "new_event_venue": "changed",
                              })
        assert response.status_code == 400

    def test_delete_event(self, client, mocker):
        mocker.patch(
            'src.application.events_sql_repo.EventsRepositorySQLImpl.delete',
            self.test_repo.delete,
        )
        current_repo = self.test_repo.get_all()
        event = current_repo[0]
        response = client.delete(f"/events/{str(event.event_id)}")
        repo_after_change = self.test_repo.get_all()
        assert response.status_code == 200 and not any([
            e.event_id == event.event_id for e in repo_after_change])

    # def test_delete_new_event(self, client, mocker):
    #     mocker.patch(
    #         'src.application.events_sql_repo.EventsRepositorySQLImpl.get_all',
    #         self.test_repo.get_all,
    #     )
    #     response = client.post("/events",
    #                            data={
    #                                "event_title": "Yuv1",
    #                                "event_location": "Ramat Hasharon",
    #                                "event_venue": "Mi Casa",
    #                                "number_of_participants": 10,
    #                                "event_time": "2023-12-10T10:51:36.347Z"
    #                            })
    #     assert response.status_code == 200


