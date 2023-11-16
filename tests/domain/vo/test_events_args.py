from datetime import datetime, timedelta
import time

import pytest

from src.domain.vo.events_args import Title, Location, Venue, EventTime, Time


@pytest.mark.parametrize("title", ("test_title", ""))
def test_create_valid_titles(title: str):
    """
    test the creation of valid options of titles
    :param title: the title's values
    """
    instance = Title(value=title)
    assert instance.value == title


@pytest.mark.parametrize("title", (None, 123123, []))
def test_create_invalid_titles(title: str):
    """
    test the creation of valid options of titles
    :param title: the title's values
    """
    with pytest.raises(ValueError):
        _ = Title(value=title)


@pytest.mark.parametrize("location", ("Berlin", "", "sdsdsa"))
def test_create_valid_location(location: str):
    """
    test the creation of valid options of locations
    :param location: the location's values
    """
    instance = Location(value=location)
    assert instance.value == location


@pytest.mark.parametrize("location", (None, 123123, []))
def test_create_invalid_locations(location: str):
    """
    test the creation of valid options of location
    :param location: the location's values
    """
    with pytest.raises(ValueError):
        _ = Location(value=location)


@pytest.mark.parametrize("venue", ("O2 arena", "", "sdsdsa"))
def test_create_valid_venues(venue: str):
    """
    test the creation of valid options of titles
    :param venue: the venue's values
    """
    instance = Venue(value=venue)
    assert instance.value == venue


@pytest.mark.parametrize("venue", (None, 123123, []))
def test_create_invalid_venues(venue: str):
    """
    test the creation of valid options of titles
    :param venue: the venue's values
    """
    with pytest.raises(ValueError):
        _ = Venue(value=venue)


def test_create_valid_time():
    """
    test the creation of valid options of titles
    """
    time_value = datetime.now()
    instance = Time(value=time_value)
    assert instance.value == time_value


def test_create_invalid_time():
    """
    test the creation of valid options of titles
    """
    time_value = time.time()
    with pytest.raises(ValueError):
        _ = Time(value=time_value)


def test_create_valid_event_time():
    """
    test the creation of valid options of event times
    """
    time_value = datetime.now() + timedelta(minutes=10)
    instance = EventTime(value=time_value)
    assert instance.value == time_value


def test_create_invalid_event_time():
    """
    test the creation of invalid options of event times
    """
    time_value = datetime.now() - timedelta(minutes=10)
    with pytest.raises(ValueError):
        _ = EventTime(value=time_value)
