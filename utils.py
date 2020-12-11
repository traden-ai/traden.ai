import datetime

def adding_days_to_date(date, days):
    date_1 = datetime.datetime.strptime(date, "%m/%d/%y")
    end_date = date_1 + datetime.timedelta(days=days)
    return end_date.strftime("%m/%d/%y")