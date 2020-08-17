def simple_paginate(values, page_limit):
    paginated_values = []
    for i, value in enumerate(values):
        if i % page_limit == 0:
            paginated_values.append([])
        paginated_values[-1].append(value)
    return paginated_values


def paginate_by_date(units, picked_attrs=[], date_limit=12, unit_limit=10):
    # 1. Get all dates
    dates = []
    for unit in units:
        for hours in unit.daily_hours.values():
            if hours.date not in dates:
                dates.append(hours.date)

    # 2. Paginate dates
    date_sets = simple_paginate(dates, date_limit)

    # 3. Set up unit list
    unit_sets = [[] for x in range(len(date_sets))]

    # 4. Add units to correct unit set
    for unit in units:
        added = [False for x in date_sets]
        for hours in unit.daily_hours.values():
            date_index = get_date_index(date_sets, hours.date)

            if not added[date_index]:
                reduced_unit = reduce_unit(unit, date_sets[date_index], picked_attrs)
                unit_sets[date_index].append(reduced_unit)
                added[date_index] = True

    # 5. Bundle dates and units and paginate unit sets
    paginated_data = []
    for date_set, unit_set in zip(date_sets, unit_sets):
        data = {"dates": date_set, "unit_sets": simple_paginate(unit_set, unit_limit)}
        paginated_data.append(data)

    return paginated_data


def get_date_index(date_sets, target_date):
    for i, date_set in enumerate(date_sets):
        if target_date in date_set:
            return i
    return 0


def reduce_unit(unit, date_set, picked_attrs):
    reduced_unit = {}

    for attr in picked_attrs:
        reduced_unit[attr] = getattr(unit, attr)

    reduced_unit["daily_hours"] = []
    for hours in unit.daily_hours.values():
        if hours.date in date_set:
            reduced_unit["daily_hours"].append(hours)

    return reduced_unit
