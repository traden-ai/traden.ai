import os
import csv
import yfinance as yf
import datetime as dt

start_year = 2010       # year from which data is collected 
today = dt.date.today()    # current date

def data_clear():
    ''' method that deletes all existing csv data files in the 'data/'
    folder'''

    year = start_year

    while year <= int(today.strftime("%Y")):

        filepath = "data/" + str(year) + ".csv"
        if os.path.exists(filepath):
            os.remove(filepath)

        year += 1


def data_download():
    ''' method that creates a file for each year between 'start_year' and 
    the current year, containing all the data from yfinance for each symbol
    in symbols.txt '''

    data_clear()
    year = start_year

    stocks = []
    f = open("symbols.txt", "r")
    for line in f:
        stocks.append(line.strip())

    if not os.path.exists("data/"):
        os.mkdir("data/")

    while year <= int(today.strftime("%Y")):
        
        start_date = str(year) + "-01-01"
        end_date = str(year+1) + "-01-01"

        if year == int(today.strftime("%Y")):
            end_date = today.strftime("%Y-%m-%d")

        print("\nDownloading data from", year, "...")
        data = yf.download(stocks, start=start_date, end=end_date)

        filepath = "data/" + str(year) + ".csv"
        data.to_csv(filepath)

        year += 1


def data_update():
    ''' method that updates the csv data file corresponding to the
    current year '''

    current_year = today.strftime("%Y")

    filepath = "data/" + current_year + ".csv"
    if os.path.exists(filepath):
        os.remove(filepath)

    stocks = []
    f = open("symbols.txt", "r")
    for line in f:
        stocks.append(line.strip())

    start_date = current_year + "-01-01"
    end_date = today.strftime("%Y-%m-%d")

    print("\nDownloading data from", current_year, "...")
    data = yf.download(stocks, start=start_date, end=end_date)

    data.to_csv(filepath)


def data_load_per_year(stocks: list, year: int):
    ''' method that loads the data corresponding to the stocks in 'stocks'
    for a specific year 'year' from the respective csv files to a list '''

    data = []
    indexes = {stock: [] for stock in stocks}

    filename = "data/" + str(year) + ".csv"
    raw_data = list(csv.reader(open(filename,'r')))

    for stock in stocks:
        for i in range(len(raw_data[1])):
            if raw_data[1][i] == stock:
                indexes[stock].append(i)

    for line in raw_data[4:]:
        data_by_day = {stock: {} for stock in stocks}
        for stock in indexes:
            for i in indexes[stock]:
                data_by_day[stock][raw_data[0][i]] = line[i]
        data_by_day["date"] = line[0]
        data.append(data_by_day)

    return data


def data_load(stocks: list, start: str, end: str):
    ''' method that loads the data corresponding to the stocks in 'stocks'
    between the dates 'start' and 'end' from the csv files to a list '''

    def get_years(start: str, end: str):
        ''' method that receives two dates and returns the respective years '''
        first_year = int(start.split('-')[0])
        last_year = int(end.split('-')[0])
        return first_year, last_year

    def get_date_index(data_year: list, date: str):
        ''' method that will return on which index of the list 'data_year'
        the data corresponding to date 'date' is '''
        def bigger_or_equal(date1: str, date2: str):
            ''' method that returns if the date 'date1' is equal or comes after
            the date 'date2' '''
            date1_datetime = dt.datetime.strptime(date1, "%Y-%m-%d")
            date2_datetime = dt.datetime.strptime(date2, "%Y-%m-%d")
            return date1_datetime >= date2_datetime            

        for i in range(len(data_year)):
            if bigger_or_equal(data_year[i]["date"], date):
                break
        return i
        
    data = []
    first_year, last_year = get_years(start, end)

    year = first_year
    while year <= last_year:

        data_year = data_load_per_year(stocks, year)

        if year == first_year:
            data_year = data_year[get_date_index(data_year, start):]

        if year == last_year:
            data_year = data_year[:get_date_index(data_year, end)+1]

        data += data_year
        year += 1

    return data
