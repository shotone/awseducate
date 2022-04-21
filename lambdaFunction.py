import io
import json
from pprint import pprint
from urllib.request import urlopen, Request
from datetime import datetime
import boto3

API_TOKEN = "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"

headers = {"Authorization": f"Bearer {API_TOKEN}"}
API_URL = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"

s3_client = boto3.client("s3")


def query_image(f):
    http_request = Request(API_URL, data=f.read(), headers=headers)
    with urlopen(http_request) as response:
        result = response.read().decode()
        print(result)
    return result


def download_file_from_bucket(bucket, key):
    # Download file from bucket
    file = io.BytesIO()
    s3_client.download_fileobj(Bucket=bucket, Key=key, Fileobj=file)
    file.seek(0)
    return file


def delete_file_from_bucket(bucket, key):
    return True if s3_client.delete_object(Bucket=bucket, Key=key) else False


def check_validate_numeric_name(name):
    # check if some file with this name is already numbered , return true

    if name.split("_")[0].isdigit():
        if type(datetime.fromtimestamp(int(name.split("_")[0]))) == datetime:
            return True
    return False


def check_validate_file_name(name):
    # File names Must be start with upper case and length must be between 6 and 9 letters.
    print("name", name)

    if name[0].isupper() and 6 <= len(name.split(".")[0]) <= 9:
        return True
    return False


def upload_file_with_numeric_name(bucket, key, hugging_result):
    # Upload file with modified name
    modified_name = str(round(datetime.timestamp(datetime.now()))) + "_" + key
    file = io.BytesIO()
    file.write(hugging_result.encode("utf-8"))
    file.seek(0)

    return True if s3_client.upload_fileobj(file, bucket, modified_name) else False


def lambda_handler(event, _):
    pprint(event)
    for record in event.get("Records"):
        bucket = record.get("s3").get("bucket").get("name")
        key = record.get("s3").get("object").get("key")

        if check_validate_numeric_name(key):
            return {"statusCode": 200, "body": json.dumps("This file is already numbered")}

        if not check_validate_file_name(key):
            # remove this file from bucket. because of non validation
            if delete_file_from_bucket(bucket, key):
                print("Deleted", key)
                return {"statusCode": 200, "body": json.dumps("File was removed, because of NonValidation")}
            return {"statusCode": 409, "body": json.dumps("Something went wrong")}

        file = download_file_from_bucket(bucket, key)

        # Send file to Huggingface API
        result = query_image(file)
        print("result", result)

        if upload_file_with_numeric_name(bucket, key, result):
            print("uploaded")
            return {"statusCode": 200, "body": json.dumps("File was uploaded")}
        return {"statusCode": 409, "body": json.dumps("Something went wrong")}
