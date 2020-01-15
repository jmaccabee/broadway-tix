class CalendarRequestHTTPError(Exception):
    pass


class TicketsRequestHTTPError(Exception):
    pass


class TicketsMetadataRequestHTTPError(Exception):
    pass


class TicketsRequestForbiddenError(Exception):
    pass


class TicketsApiIsBusyError(Exception):
    pass
