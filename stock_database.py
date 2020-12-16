import os
import csv
import yfinance as yf
import datetime as dt
from utils import get_date_index, get_year_month_day

start_year = 2010          # defaut year from which data is collected 
today = dt.date.today()    # current date

def get_stocks():
    ''' method that loads all stocks from 'data/symbols.txt' into a list '''

    stocks = []
    with open("data/symbols.txt", "r") as f:
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
    in data/symbols.txt '''

    data_clear(year)

    if not os.path.exists("data/"):
        os.mkdir("data/")

    while year <= int(today.strftime("%Y")):
        
        start_date = str(year) + "-01-01"
        end_date = str(year+1) + "-01-01"

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
        if not (line[0] == "2018-12-05" or line[0] == "2017-02-20" or line[0] == "2016-01-18"):
            data.append(data_by_day)
    return data


def data_load(stocks: list, start: str, end: str):
    ''' method that loads the data corresponding to the stocks in 'stocks'
    between the dates 'start' and 'end' from the csv files to a list '''
        
    data = []
    first_year, *_ = get_year_month_day(start)
    last_year, *_ = get_year_month_day(end)

    year = int(first_year)
    while year <= int(last_year):
        data += data_load_per_year(stocks, year)
        year += 1

    return data[get_date_index(data, start, "start"):get_date_index(data, end, "end")]
