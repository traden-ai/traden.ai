import datetime as dt


def profit_percentage_by_year(initial_value, current_value, time_in_days):
    return (((((current_value - initial_value) / initial_value) + 1) ** (365 / time_in_days)) - 1) * 100


def time_between_days(initial_date, end_date):
    from datetime import date
    year0, month0, day0 = get_year_month_day(initial_date)
    year1, month1, day1 = get_year_month_day(end_date)
    d0 = date(int(year0), int(month0), int(day0))
    d1 = date(int(year1), int(month1), int(day1))
    delta = d1 - d0
    return delta.days


def get_year_month_day(date):
    date_parts = date.split("-")
    year = date_parts[0]
    month = date_parts[1]
    day = date_parts[2]
    return year, month, day


def get_year(date):
    date_parts = date.split("-")
    year = date_parts[0]
    return year


def get_month(date):
    date_parts = date.split("-")
    month = date_parts[1]
    return month


def date_smaller_or_equal(date1: str, date2: str):
    date1_datetime = dt.datetime.strptime(date1, "%Y-%m-%d")
    date2_datetime = dt.datetime.strptime(date2, "%Y-%m-%d")
    return date1_datetime <= date2_datetime


def date_bigger_or_equal(date1: str, date2: str):
    date1_datetime = dt.datetime.strptime(date1, "%Y-%m-%d")
    date2_datetime = dt.datetime.strptime(date2, "%Y-%m-%d")
    return date1_datetime >= date2_datetime


def get_date_index(data_year: list, date: str, date_type: str):
    for index, data_day in enumerate(data_year):
        if date_bigger_or_equal(data_day["date"], date) and date_type == "start" or \
                not date_smaller_or_equal(data_day["date"], date) and date_type == "end":
            break

    return index
