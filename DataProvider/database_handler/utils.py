from DataProvider.database_handler.connection import get_client
from DataProvider.database_handler.constants import STOCK_TABLE_NAME, METADATA_TABLE_NAME, INDICATORS_TABLE_NAME, \
    TICKERS_TABLE_NAME
from datetime import datetime
import json


def insert_items(items, batch_size=25):
    client = get_client()
    for ticker in items:
        batch = []
        for date in items[ticker]:
            old_item = get_item(ticker, date, serialized=True)
            new_item = {"Symbol": {"S": ticker},
                        "Date": {"S": date}}
            for indicator in items[ticker][date]:
                new_item[indicator] = {"S": json.dumps(items[ticker][date][indicator])}
            old_item.update(new_item)
            batch.append({"PutRequest": {"Item": old_item}})
            if len(batch) == batch_size:
                client.batch_write_item(RequestItems={STOCK_TABLE_NAME: batch})
                batch = []
        if len(batch) != 0:
            client.batch_write_item(RequestItems={STOCK_TABLE_NAME: batch})


def insert_items_metadata(items, batch_size=25):
    client = get_client()
    start_date, end_date = get_start_and_end_date(items)
    for ticker in items:
        batch = []
        for indicator in start_date[ticker]:
            item_metadata = get_item_metadata(ticker, indicator)
            if item_metadata["StartDate"] is not None:
                new_start_date = min(item_metadata["StartDate"], start_date[ticker][indicator])
            else:
                new_start_date = start_date[ticker][indicator]
            if item_metadata["EndDate"] is not None:
                new_end_date = max(item_metadata["EndDate"], end_date[ticker][indicator])
            else:
                new_end_date = end_date[ticker][indicator]
            if new_start_date != item_metadata["StartDate"] or \
                    new_end_date != item_metadata["EndDate"]:
                new_item = {"Symbol": {"S": ticker},
                            "Indicator": {"S": indicator},
                            "StartDate": {"S": new_start_date},
                            "EndDate": {"S": new_end_date},
                            "LastUpdate": {"S": str(datetime.now())}}
                batch.append({"PutRequest": {"Item": new_item}})
            if len(batch) == batch_size:
                client.batch_write_item(RequestItems={METADATA_TABLE_NAME: batch})
                batch = []
        if len(batch) != 0:
            client.batch_write_item(RequestItems={METADATA_TABLE_NAME: batch})


def insert_stocks(tickers, type, batch_size=25):
    client = get_client()
    batch = []
    for ticker in tickers:
        new_item = {"Ticker": {"S": ticker},
                    "Type": {"S": type}}
        batch.append({"PutRequest": {"Item": new_item}})
        if len(batch) == batch_size:
            client.batch_write_item(RequestItems={TICKERS_TABLE_NAME: batch})
            batch = []
    if len(batch) != 0:
        client.batch_write_item(RequestItems={TICKERS_TABLE_NAME: batch})


def insert_indicators_for_resource_identifier(indicators, resource_identifier, batch_size=25):
    client = get_client()
    batch = []
    for indicator in indicators:
        new_item = {"Identifier": {"S": resource_identifier},
                    "Name": {"S": indicator}}
        batch.append({"PutRequest": {"Item": new_item}})
        if len(batch) == batch_size:
            client.batch_write_item(RequestItems={INDICATORS_TABLE_NAME: batch})
            batch = []
    if len(batch) != 0:
        client.batch_write_item(RequestItems={INDICATORS_TABLE_NAME: batch})


def get_indicators(resource_identifier=None):
    client = get_client()
    if resource_identifier:
        response = client.scan(TableName=INDICATORS_TABLE_NAME, ScanFilter={
            "Identifier": {"ComparisonOperator": "EQ", "AttributeValueList": [{"S": resource_identifier}]}},
                               )
    else:
        response = client.scan(TableName=INDICATORS_TABLE_NAME)
    items = response['Items']
    final_items = []
    for item in items:
        final_items.append(item["Name"]["S"])
    return final_items


def get_stocks(type=None):
    client = get_client()
    if type:
        response = client.scan(TableName=TICKERS_TABLE_NAME, ScanFilter={
            "Type": {"ComparisonOperator": "EQ", "AttributeValueList": [{"S": type}]}})
    else:
        response = client.scan(TableName=TICKERS_TABLE_NAME)
    items = response['Items']
    final_items = []
    for item in items:
        final_items.append(item["Ticker"]["S"].replace(" ", ""))
    return final_items


def get_item(ticker, date, indicators=None, serialized=None):
    client = get_client()
    if indicators:
        response = client.query(TableName=STOCK_TABLE_NAME, AttributesToGet=["Symbol", "Date"] + indicators,
                                KeyConditions={
                                    "Symbol": {"ComparisonOperator": "EQ", "AttributeValueList": [{"S": ticker}]},
                                    "Date": {"ComparisonOperator": "EQ", "AttributeValueList": [{"S": date}]}})
    else:
        response = client.query(TableName=STOCK_TABLE_NAME,
                                KeyConditions={
                                    "Symbol": {"ComparisonOperator": "EQ", "AttributeValueList": [{"S": ticker}]},
                                    "Date": {"ComparisonOperator": "EQ", "AttributeValueList": [{"S": date}]}})
    new_item = {"Symbol": ticker, "Date": date}
    items = response['Items']
    for item in items:
        for indicator in item:
            if indicator != "Symbol" and indicator != "Date":
                if serialized is None:
                    new_item[indicator] = json.loads(item[indicator]["S"])
                else:
                    new_item[indicator] = {"S": item[indicator]["S"]}
    return new_item


def get_item_metadata(ticker, indicator):
    client = get_client()
    response = client.query(TableName=METADATA_TABLE_NAME, KeyConditions={
        "Symbol": {"ComparisonOperator": "EQ", "AttributeValueList": [{"S": ticker}]},
        "Indicator": {"ComparisonOperator": "EQ", "AttributeValueList": [{"S": indicator}]}})
    new_item = {"Symbol": ticker, "Indicator": indicator, "StartDate": None, "EndDate": None, "LastUpdate": None}
    for item in response['Items']:
        new_item["StartDate"] = item["StartDate"]["S"]
        new_item["EndDate"] = item["EndDate"]["S"]
        new_item["LastUpdate"] = item["LastUpdate"]["S"]
    return new_item


def remove_item(ticker):
    client = get_client()
    item = query_item(ticker)
    for date in item["Data"]:
        client.delete_item(TableName=STOCK_TABLE_NAME, Key={"Symbol": {"S": ticker}, "Date": {"S": date}})


def remove_item_metadata(ticker):
    client = get_client()
    item = query_item_metadata(ticker)
    for indicator in item["IndicatorData"]:
        client.delete_item(TableName=METADATA_TABLE_NAME, Key={"Symbol": {"S": ticker}, "Indicator": {"S": indicator}})


def query_item(ticker, indicators, start_date, end_date, exclusive_start_key=None):
    client = get_client()
    if exclusive_start_key:
        response = client.query(TableName=STOCK_TABLE_NAME, AttributesToGet=["Symbol", "Date"] + indicators,
                                KeyConditions={
                                    "Symbol": {"ComparisonOperator": "EQ", "AttributeValueList": [{"S": ticker}]},
                                    "Date": {"ComparisonOperator": "BETWEEN",
                                             "AttributeValueList": [{"S": start_date}, {"S": end_date}]}},
                                ExclusiveStartKey=exclusive_start_key)
    else:
        response = client.query(TableName=STOCK_TABLE_NAME, AttributesToGet=["Symbol", "Date"] + indicators,
                                KeyConditions={
                                    "Symbol": {"ComparisonOperator": "EQ", "AttributeValueList": [{"S": ticker}]},
                                    "Date": {"ComparisonOperator": "BETWEEN",
                                             "AttributeValueList": [{"S": start_date}, {"S": end_date}]}})
    new_item = {"Symbol": ticker, "Data": {}}
    for item in response['Items']:
        new_item["Data"][item["Date"]["S"]] = {}
        for indicator in indicators:
            new_item["Data"][item["Date"]["S"]][indicator] = json.loads(item[indicator]["S"])
    if "LastEvaluatedKey" in response:
        new_item["Data"].update(
            query_item(ticker, start_date, end_date, exclusive_start_key=response["LastEvaluatedKey"])["Data"])
    return new_item


def query_item_metadata(ticker, exclusive_start_key=None):
    client = get_client()
    if exclusive_start_key:
        response = client.query(TableName=METADATA_TABLE_NAME, KeyConditions={
            "Symbol": {"ComparisonOperator": "EQ", "AttributeValueList": [{"S": ticker}]}},
                                ExclusiveStartKey=exclusive_start_key)
    else:
        response = client.query(TableName=METADATA_TABLE_NAME, KeyConditions={
            "Symbol": {"ComparisonOperator": "EQ", "AttributeValueList": [{"S": ticker}]}})
    new_item = {"Symbol": ticker, "IndicatorData": {}}
    for item in response['Items']:
        new_item["IndicatorData"][item["Indicator"]["S"]] = {"StartDate": item["StartDate"]["S"]
            , "EndDate": item["EndDate"]["S"]
            , "LastUpdate": item["LastUpdate"]["S"]}
    if "LastEvaluatedKey" in response:
        new_item["IndicatorData"].update(
            query_item_metadata(ticker, exclusive_start_key=response["LastEvaluatedKey"])["IndicatorData"])
    return new_item


def get_start_and_end_date(items):
    start_date = {}
    end_date = {}
    for ticker in items:
        if ticker not in start_date:
            start_date[ticker] = {}
        if ticker not in end_date:
            end_date[ticker] = {}
            for date in items[ticker]:
                current_date = date
                for indicator in items[ticker][date]:
                    if indicator not in start_date[ticker]:
                        start_date[ticker][indicator] = current_date
                    if indicator not in end_date[ticker]:
                        end_date[ticker][indicator] = current_date
                    if start_date[ticker][indicator] > current_date:
                        start_date[ticker][indicator] = current_date
                    if end_date[ticker][indicator] < current_date:
                        end_date[ticker][indicator] = current_date
    return start_date, end_date


def convert_to_data_by_date(raw_data):
    final_data = {}
    for data in raw_data:
        for ticker in data:
            for date in data[ticker]:
                if date not in final_data:
                    final_data[date] = {}
                if ticker not in final_data[data]:
                    final_data[date][ticker] = {}
                final_data[date][ticker].update(data[ticker][date])
    return final_data
