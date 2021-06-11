from database_handler.connection import get_client
from database_handler.constants import TABLE_NAME
from boto3.dynamodb.conditions import Key
import json


def insert_items(items, batch_size=25):
    client = get_client()
    for item in items:
        batch = []
        for date in item["Data"]:
            new_item = {"Symbol": {"S": item["Symbol"]},
                        "Date": {"S": date},
                        "Data": {"S": json.dumps(item["Data"][date])}}
            batch.append({"PutRequest" : {"Item": new_item}})
            if len(batch) == batch_size:
                client.batch_write_item(RequestItems={TABLE_NAME : batch})
                batch = []
        if len(batch) != 0:
            client.batch_write_item(RequestItems={TABLE_NAME: batch})


def remove_item(ticker):
    client = get_client()
    item = query_item(ticker)
    for date in item["Data"]:
        client.delete_item(TableName=TABLE_NAME, Key={"Symbol": {"S": ticker}, "Date": {"S": date}})


def query_item(ticker, start_date, end_date, exclusive_start_key=None):
    client = get_client()
    if exclusive_start_key:
        response = client.query(TableName=TABLE_NAME, KeyConditions={
            "Symbol": {"ComparisonOperator": "EQ", "AttributeValueList": [{"S": ticker}]},
            "Date": {"ComparisonOperator": "BETWEEN", "AttributeValueList": [{"S": start_date}, {"S": end_date}]}},
            ExclusiveStartKey=exclusive_start_key)
    else:
        response = client.query(TableName=TABLE_NAME, KeyConditions={
            "Symbol": {"ComparisonOperator": "EQ", "AttributeValueList": [{"S": ticker}]},
            "Date": {"ComparisonOperator": "BETWEEN", "AttributeValueList": [{"S": start_date}, {"S": end_date}]}})
    new_item = {"Symbol": ticker, "Data": {}}
    for item in response['Items']:
        new_item["Data"][item["Date"]["S"]] = json.loads(item["Data"]["S"])
    if "LastEvaluatedKey" in response:
        new_item["Data"].update(query_item(ticker,start_date,end_date, exclusive_start_key=response["LastEvaluatedKey"])["Data"])
    return new_item

