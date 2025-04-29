import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Fill thông tin Bucket
R2_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
R2_ACCOUNT_ID = os.getenv('R2_ACCOUNT_ID')
R2_BUCKET_NAME = 'hopehub-storage'

r2_client = boto3.client('s3',
    endpoint_url=f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY
)

def upload_to_r2(filename, data):
    r2_client.put_object(
        Bucket=R2_BUCKET_NAME,
        Key=f"BIN/{filename}",
        Body=data,
        ContentType='application/json'
    )

def list_bins_from_r2():
    try:
        res = r2_client.get_object(Bucket=R2_BUCKET_NAME, Key="BIN/bins_real_full.json")
        data = res['Body'].read().decode('utf-8')
        bins = json.loads(data)
        return bins
    except Exception as e:
        print(f"[Error] Cannot fetch BINs from R2: {e}")
        return []
