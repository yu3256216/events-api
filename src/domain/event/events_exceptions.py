
class InvalidEventTime(ValueError):
    """
    raised if the time of the event is not future time
    """
    def __init__(self, message: str = "The event time should be future date"):
        super(InvalidEventTime, self).__init__(message)


class EventDoesntExists(Exception):
    """
        raised if the time of the event is not future time
        """
    def __init__(self, message: str = "An event with the given ID wasn't "
                                      "found in the repo"):
        super(EventDoesntExists, self).__init__(message)


class QueryException(Exception):
    """
    Raised if there was exception querying the repo
    """
    def __init__(self, message: str = "There was an exception while "
                                      "querying the repo"):
        super(QueryException, self).__init__(message)
