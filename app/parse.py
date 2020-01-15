from app import utils


def parse_performances_from_calendar_data(calendar_data):
    """
    Extracts the relevant performance metadata 
    from the calendar response JSON object.
    """
    performances = calendar_data['data']['performances']
    if not performances:
        return []

    return [
        {
            'date': utils.stringdate_to_datetime(performance_date['date']),
            'time': performance['time'],
            'status': performance['status'],
            'availability': performance['availability'],
            'performance_id': performance['id'],
        }
        for performance_date in performances
        for performance in performance_date['times']
    ]


def parse_ticket_details(
        tickets_data,
        performance_id,
        date,
        time,
    ):
    """
    Extracts the relevant ticket metadata
    from the tickets response JSON object.
    """
    tickets = tickets_data['data']['tickets']
    if not tickets:
        return []

    return [
        {
            'area_name': ticket['AreaName'],
            'first_seat': ticket['FirstSeat'],
            'last_seat': ticket['LastSeat'],
            'quantity': ticket['Quantity'],
            'ticket_price': ticket['TicketPrice'],
            'service_fee': ticket['ServiceFee'],
            'row_name': ticket['RowName'],
            'section_name': ticket['SectionName'],
            'quality': ticket['Quality'],
            'section_id': ticket['SectionId'],
            'peformance_id': performance_id,
            'performance_date': date,
            'performance_time': time,
        } 
        for ticket in tickets
    ]
