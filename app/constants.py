CALENDAR_URL_FORMAT = (
    'https://checkout.broadway.com/'
    '{title_slug}/{show_id}/calendar/{year}/{month:02d}/'
)
TICKET_URL_FORMAT = (
    'https://checkout.broadway.com/'
    '{title_slug}/{show_id}/{performance_id}/sections/'
)
PERFORMANCE_ON_SALE_STATUS = 'On Sale'
PERFORMANCE_AVAILABLE_STATUS = 'Open'
FORBIDDEN_STATUS_CODE = 403
TICKETS_API_BUSY_STATUS = 4
