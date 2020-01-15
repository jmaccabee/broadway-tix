import requests

from app import exceptions, parse


def get_performances_from_calendar(calendar_url):
    """
    Given a calendar URL, returns the associated 
    performance metadata.
    """
    calendar_response = requests.get(
        calendar_url,
        headers={
            'authority': 'checkout.broadway.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'referer': calendar_url,
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
        }
    )
    if not calendar_response.ok:
        raise exceptions.CalendarRequestHTTPError()

    calendar_response_data = calendar_response.json()

    return parse.parse_performances_from_calendar_data(
        calendar_response_data
    )
