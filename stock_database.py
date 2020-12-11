import os
import yfinance as yf
from datetime import date

start_year = 2010       # year from which data is collected 
today = date.today()    # current date

def data_clear():
    ''' method that deletes all existing csv data files '''

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

    year = start_year

    stocks = []
    f = open("symbols.txt", "r")
    for line in f:
        stocks.append(line.strip())

    if not os.path.exists("data/"):
        os.mkdir("data/")

    while year <= int(today.strftime("%Y")):
        
        start_date = str(year) + "-01-01"
        end_date = str(year) + "-12-31"

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

if __name__ == "__main__":
    data_update()