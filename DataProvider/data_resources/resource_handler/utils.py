def intersection(lst1, lst2):
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3


def unite_raw_data(raw_data):
    """Data should have past data in the format
    {ticker : {date: {indicator: data in string format, ...}, ...}, ...}
    """
    final_data = {}
    for data in raw_data:
        for ticker in data:
            if ticker not in final_data:
                final_data[ticker] = {}
            for date in data[ticker]:
                if date not in final_data[ticker]:
                    final_data[ticker][date] = {}
                final_data[ticker][date].update(data[ticker][date])
    return final_data

