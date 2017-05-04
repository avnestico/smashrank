import boto3
import sys


def is_local():
    return "local" in sys.argv


def is_dev():
    return is_local() and "dev" in sys.argv


def dynamodb():
    if is_local():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")
    else:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    return dynamodb

def dynamodb_client():
    if is_local():
        client = boto3.client('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")
    else:
        client = boto3.client('dynamodb', region_name='us-east-1')
    return client