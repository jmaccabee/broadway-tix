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
            'date': performance_date['date'],
            'time': performance['time'],
            'status': performance['status'],
            'availability': performance['availability'],
            'performance_id': performance['id'],
        }
        for performance_date in performances
        for performance in performance_date['times']
    ]


def parse_ticket_details(tickets_data):
    """
    Extracts the relevant ticket metadata
    from the tickets response JSON object.
    """
    import pdb; pdb.set_trace()
    tickets = calendar_data['data']['tickets']
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

        } 
        for ticket in tickets
    ]
