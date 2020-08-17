""" Utility functions for various tasks. """
from datetime import datetime

def make_field_name(field, number):
    """ Creates field name, appending an underscore and a zero-padded number. """
    if number < 10:
        return field + "_0" + str(number)
    else:
        return field + "_" + str(number)


def make_field(values, field_name, number, value):
    """ Adds a field name and value pair to the given dictionary. """
    if value is not None:
        name = make_field_name(field_name, number)
        values[name] = value


def rnd(num):
    """ Rounds a number to two decimal places. """
    return round((num + 0.00000001) * 100) / 100


def datetime_from_string(datetime_string, org_format="%Y-%m-%d"):
    """ Returns a datetime object given a date string and format. """
    return datetime.strptime(datetime_string, org_format)


def format_date(datetime_string, dest_format, org_format="%Y-%m-%d"):
    """ Returns a formatted datetime string, given a datetime string and an original format. """
    return datetime_from_string(datetime_string, org_format).strftime(dest_format)
