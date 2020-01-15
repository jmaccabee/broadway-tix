import requests

from app import constants, exceptions, parse, settings, utils


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


def get_performance_seating_metadata(tickets_url):
    """
    Given a tickets_url, returns the metadata
    required to fetch the available tickets and prices.
    """
    tickets_response = requests.get(
        tickets_url,
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
            'referer': f'https://www.broadway.com/shows/{settings.TITLE_SLUG}/',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
        }
    )
    if not tickets_response.ok:
        raise exceptions.TicketsMetadataRequestHTTPError()

    sections = tickets_response.json()['data']['sections']
    price_ids = utils.get_price_ids_from_sections(sections)

    return {
        'price_ids': price_ids, 
    }


def get_available_seats_for_performance(
        tickets_url, 
        price_ids
    ):
    """
    Given required performance metadata,
    returns a list of available tickets.
    """
    import pdb; pdb.set_trace()
    ticket_criteria = [('quantity', f'{settings.TICKET_QUANTITY}')]
    for price_id in price_ids:
        ticket_criteria.append(('priceid', price_id))
    tickets_response = requests.post(
        tickets_url,
        headers={
            'authority': 'checkout.broadway.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'origin': 'https://checkout.broadway.com',
            'x-csrftoken': f'{settings.CSRF_TOKEN}',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'referer': f'https://www.broadway.com/shows/{settings.TITLE_SLUG}/',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': f'',
        },
        data=ticket_criteria,
    )
    if (
            not tickets_response.ok &
            tickets_response.status_code == constants.FORBIDDEN_STATUS_CODE
        ):
        raise exceptions.TicketsRequestForbiddenError()
    elif not tickets_repsonse.ok:
        raise exceptions.TicketsRequestHTTPError()

    tickets_data = tickets_response.json()
    return parse.parse_ticket_details(tickets_data)
