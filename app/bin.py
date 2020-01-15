import datetime
import time

from app import settings, utils, web


def get_performances_in_date_range(
        start_date_inclusive_str, 
        end_date_exclusive_str, 
        date_format='%Y-%m-%d',
    ):
    """
    Fetches the performance IDs from the Broadway.com calendar page
    between start_date_inclusive_str and end_date_exclusive_str, 
    parsed to dates using date_format.

    Performance IDs are used to get available ticket prices.
    """
    # parse date strings to datetimes
    start_date = datetime.datetime.strptime(
        start_date_inclusive_str, 
        date_format,
    )
    end_date = datetime.datetime.strptime(
        end_date_exclusive_str, 
        date_format,
    )

    # build the list of calendar URLs you need to fetch to get
    # the list of performance IDs from start_date to end_date
    calendar_urls = utils.build_calendar_urls(
        start_date, 
        end_date,
    )

    # fetch the performance IDs, with a time to sleep
    # between requests so we don't cause issues for the site.
    performances_in_date_range = []
    for calendar_url in calendar_urls:
        performances_for_month = web.get_performances_from_calendar(
            calendar_url
        )
        performances_in_date_range.extend(performances_for_month)
        time.sleep(settings.REQUEST_SLEEP_TIME_SECONDS)
    return performances_in_date_range


if __name__ == '__main__':
    # performances = get_performances_in_date_range(
    #     settings.START_DATE_INCLUSIVE_STR,
    #     settings.END_DATE_EXCLUSIVE_STR,
    # )
    # ticketable_performances = [
    #     performance
    #     for performance in performances
    #     if utils.is_ticketable_performance(performance)
    # ]
    # for performance in ticketable_performances:
    performance = {'performance_id': '950700'}
    tickets_url = utils.build_tickets_url(performance['performance_id'])
    performance_metadata = web.get_performance_seating_metadata(
        tickets_url
    )
    import pdb; pdb.set_trace()
    available_seats = web.get_available_seats_for_performance(
        tickets_url, 
        performance_metadata['price_ids'],
    )
