def parse_performances_from_calendar_data(calendar_data):
    """
    Extracts the relevant performance metadata 
    from the calendar response object.
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
