import time

from app import settings, utils, web


def get_performances_in_date_range(start_date, end_date):
    """
    Fetches the performance IDs from the Broadway.com calendar page
    between start_date and end_date. 

    Performance IDs are used to get available ticket prices.
    """
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


def get_available_tickets_for_performance(performance):
    """
    Constructs the tickets_url for the performance, 
    fetches the CSRF Token and price IDs to view available tickets via API,
    and then fetches the available ticket information.
    """
    tickets_url = utils.build_tickets_url(performance['performance_id'])
    performance_metadata = web.get_performance_seating_metadata(
        tickets_url
    )
    available_seats = web.get_available_seats_for_performance(
        tickets_url, 
        performance_metadata['csrf_token'],
        performance_metadata['session_id'],
        performance_metadata['price_ids'],
        performance['performance_id'],
        performance['date'],
        performance['time'],
    )
    time.sleep(settings.REQUEST_SLEEP_TIME_SECONDS)
    return available_seats


if __name__ == '__main__':
    start_date = utils.stringdate_to_datetime(
        settings.START_DATE_INCLUSIVE_STR
    )
    end_date = utils.stringdate_to_datetime(
        settings.END_DATE_EXCLUSIVE_STR
    )
    performances = get_performances_in_date_range(start_date, end_date)
    ticketable_performances = [
        performance
        for performance in performances
        if utils.is_target_performance(performance, start_date, end_date)
    ]
    all_available_seats = []
    for performance in ticketable_performances:
        available_seats = get_available_tickets_for_performance(performance)
        # save intermediate files in case our program fails before finishing
        utils.save_data(available_seats, performance['time'])
        all_available_seats.extend(available_seats)
    # then save the whole file
    utils.save_data(all_available_seats)
