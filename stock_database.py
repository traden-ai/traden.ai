import os
import csv
import yfinance as yf
import datetime as dt

start_year = 2010          # defaut year from which data is collected 
today = dt.date.today()    # current date

def get_stocks():
    ''' method that loads all stocks from 'symbols.txt' into a list '''
    
    stocks = []
    with open("symbols.txt", "r") as f:
        for line in f:
            stocks.append(line.strip())

    return stocks


def data_clear(year=start_year):
    ''' method that deletes all existing csv data files in the 'data/'
    folder starting from input 'year' '''

    while year <= int(today.strftime("%Y")):

        filepath = f"data/{year}.csv"
        if os.path.exists(filepath):
            os.remove(filepath)

        year += 1


def data_download(year=start_year):
    ''' method that creates a file for each year between input 'year' and 
    the current year, containing all the data from yfinance for each symbol
    in symbols.txt '''

    data_clear(year)

    if not os.path.exists("data/"):
        os.mkdir("data/")

    while year <= int(today.strftime("%Y")):
        
        start_date = f"{year}-01-01"
        end_date = f"{year+1}-01-01"

        if year == int(today.strftime("%Y")):
            end_date = today.strftime("%Y-%m-%d")

        print("\nDownloading data from", year, "...")
        data = yf.download(get_stocks(), start=start_date, end=end_date)

        filepath = f"data/{year}.csv"
        data.to_csv(filepath)

        year += 1


def data_update():
    ''' method that updates the csv data file corresponding to the
    current year '''

    current_year = int(today.strftime("%Y"))
    data_download(current_year)


def data_load_per_year(stocks: list, year: int):
    ''' method that loads the data corresponding to the stocks in 'stocks'
    for a specific year 'year' from the respective csv files to a list '''

    data = []
    indexes = {stock: [] for stock in stocks}

    filename = f"data/{year}.csv"
    with open(filename,'r') as f:
        raw_data = list(csv.reader(f))

    for stock in stocks:
        for index, data_stock in enumerate(raw_data[1]):
            if data_stock == stock:
                indexes[stock].append(index)

    for line in raw_data[4:]:
        data_by_day = {stock: {} for stock in stocks}
        for stock in indexes:
            for index in indexes[stock]:
                data_by_day[stock][raw_data[0][index]] = line[index]
        data_by_day["date"] = line[0]
        data.append(data_by_day)

    return data


def data_load(stocks: list, start: str, end: str):
    ''' method that loads the data corresponding to the stocks in 'stocks'
    between the dates 'start' and 'end' from the csv files to a list '''

    def get_date_index(data_year: list, date: str):
        ''' method that will return on which index of the list 'data_year'
        the data corresponding to date 'date' is '''
        def bigger_or_equal(date1: str, date2: str):
            ''' method that returns if the date 'date1' is equal or comes after
            the date 'date2' '''
            date1_datetime = dt.datetime.strptime(date1, "%Y-%m-%d")
            date2_datetime = dt.datetime.strptime(date2, "%Y-%m-%d")
            return date1_datetime >= date2_datetime            

        for index, data_day in enumerate(data_year):
            if bigger_or_equal(data_day["date"], date):
                break
        return index
        
    data = []
    first_year = int(start.split('-')[0])
    last_year = int(end.split('-')[0])

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
