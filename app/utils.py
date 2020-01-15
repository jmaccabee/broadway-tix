import datetime
import os

from dateutil.rrule import rrule, MONTHLY
import pandas as pd

from app import constants, settings


def stringdate_to_datetime(dt, date_format='%Y-%m-%d'):
    return datetime.datetime.strptime(
        dt, 
        date_format,
    )


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


def is_target_performance(performance, start_date, end_date):
    """
    Ticketable performances have valid 
    availability and status values and 
    appear within the target window.
    """
    return (
        (performance['availability'] == constants.PERFORMANCE_AVAILABLE_STATUS) &
        (performance['status'] == constants.PERFORMANCE_ON_SALE_STATUS) & 
        (performance['date'] >= start_date) & 
        (performance['date'] < end_date)
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


def make_filepath_to_data(performance_time=''):
    """
    Create a filepath to the location of our data 
    directory to write our ticket files to.
    """
    today_date_str = datetime.datetime.today().strftime('%Y%m%d')
    path_to_app = os.path.dirname(os.path.realpath(__file__))
    path_to_performance = f'{path_to_app}/../data/{settings.TITLE_SLUG}/'
    if not os.path.exists(path_to_performance):
        os.mkdir(path_to_performance)

    path_to_data = f'{path_to_performance}/availability_on_{today_date_str}'

    if performance_time:
        path_to_data += f'_{performance_time}'
    return path_to_data + '.csv'


def save_data(data, performance_time=''):
    """
    Save data to CSV file.
    """
    df = pd.DataFrame.from_dict(data)
    filepath_to_data = make_filepath_to_data(performance_time)    
    print('Saving data to path:', filepath_to_data)
    df.to_csv(filepath_to_data)
