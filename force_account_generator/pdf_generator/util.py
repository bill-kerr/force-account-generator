from datetime import datetime


def rnd(num):
    return round((num + 0.00000001) * 100) / 100


def datetime_from_string(datetime_string, org_format='%Y-%m-%d'):
    return datetime.strptime(datetime_string, org_format)


def format_date(datetime_string, dest_format, org_format='%Y-%m-%d'):
    return datetime_from_string(datetime_string, org_format).strftime(dest_format)


def decimal_formatter(val): return f'{val:.2f}'


def decimal_comma_formatter(val): return f'{val:,.2f}'


def currency_formatter(val): return f'$ {val:,.2f}'


def percent_formatter(val): return f'{val * 100:.3f}%'


def two_decimal_percent_formatter(val): return f'{val * 100:.2f}%'


def whole_number_formatter(val): return f'{val:.0f}'


def three_decimal_formatter(val): return f'{val:,.3f}'
