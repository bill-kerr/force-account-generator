def get_dates(row):
    dates = []
    for value in row:
        dates.append(value.strftime('%Y-%m-%d') if value is not None else None)
    return dates


def get_hours(primary_row, secondary_row, dates, primary_label='st', secondary_label='ot'):
    daily_hours = []
    for pri, sec, date in zip(primary_row, secondary_row, dates):
        if date is None or (pri is None and sec is None):
            continue

        hours = {
            'date': date
        }
        if pri is not None:
            hours[primary_label] = pri
        if sec is not None:
            hours[secondary_label] = sec
        daily_hours.append(hours)

    return daily_hours
