from dateutil.rrule import rrule, MONTHLY

from app import constants, settings


def generate_month_range(start_date, end_date):
    """
    Given a start date and an end date, 
    generates a list of months where the 
    day of each month is the first.
    """
    dates = [
        dt for dt in rrule(
            MONTHLY, 
            dtstart=start_date, 
            until=end_date
        )
    ]
    return dates


def build_calendar_urls(start_date, end_date):
    """
    Given a start date and an end date,
    generates a list of calendar URLs 
    to fetch performance IDs from.
    """
    month_range = generate_month_range(start_date, end_date)

    calendar_urls = []
    for date in month_range:
        calendar_url = constants.CALENDAR_URL_FORMAT.format(
            title_slug=settings.TITLE_SLUG,
            aristotle_id=settings.ARISTOTLE_ID,
            year=date.year,
            month=date.month,
        )
        calendar_urls.append(calendar_url)

    return calendar_urls


def is_ticketable_performance(performance):
    """
    Ticketable performances have valid 
    availability and status values.
    """
    return (
        performance['availability'] == constants.PERFORMANCE_AVAILABLE_STATUS &
        performance['status'] == constants.PERFORMANCE_ON_SALE_STATUS
    )


def build_tickets_url(performance_id):
    """
    Given a performance ID, create the URL 
    to return information on available tickets.
    """
    tickets_url = constants.TICKET_URL_FORMAT.format(
        title_slug=settings.TITLE_SLUG,
        aristotle_id=settings.ARISTOTLE_ID,
        performance_id=performance_id,
    )
    return tickets_url


def get_price_ids_from_sections(sections):
    """
    Given a sections object, returns a 
    flattened list of unique price_ids.
    """
    section_price_ids = []
    for section in sections:
        price_ids = section.get('price_ids', [])
        section_price_ids.extend(price_ids)
    # make the list of price IDs unique
    return list(set(section_price_ids))
