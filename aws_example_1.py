import boto3

s3_client = boto3.client('s3')

buckets = s3.list_buckets()


def list_buckets(buckets):
    bucket_names = [bucket["Name"] for bucket in buckets["Buckets"]]
    print(f"names of buckets: {bucket_names})


def exclude_buckets(buckets):
    bucket_names = [bucket["Name"] for bucket in buckets["Buckets"] if bucket["Name"].startswith("prod")]
    print(f"exclude names of buckets: {bucket_names})




if __name__ == '__main__':
    list_buckets(buckets)
    exclude_buckets(buckets)
