def create_dict(objects):
    new_dict = {}
    for i, obj in enumerate(objects):
        new_dict[i] = obj
    return new_dict


def make_field_name(field, number):
    if number < 10:
        return field + "_0" + str(number)
    else:
        return field + "_" + str(number)


def make_field(values, field_name, number, value):
    if value is not None:
        name = make_field_name(field_name, number)
        values[name] = value


def paginate(values, page_limit):
    paginated_values = []
    for i, value in enumerate(values):
        if i % page_limit == 0:
            paginated_values.append([])
        paginated_values[-1].append(value)
    return paginated_values
