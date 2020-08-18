""" Utility functions for various tasks. """
from datetime import datetime

def rnd(num):
    """ Rounds a number to two decimal places. """
    return round((num + 0.00000001) * 100) / 100


def datetime_from_string(datetime_string, org_format="%Y-%m-%d"):
    """ Returns a datetime object given a date string and format. """
    return datetime.strptime(datetime_string, org_format)


def format_date(datetime_string, dest_format, org_format="%Y-%m-%d"):
    """ Returns a formatted datetime string, given a datetime string and an original format. """
    return datetime_from_string(datetime_string, org_format).strftime(dest_format)

decimal_formatter = lambda val: f'{val:.2f}'
decimal_comma_formatter = lambda val: f'{val:,.2f}'
currency_formatter = lambda val: f'$ {val:,.2f}'
