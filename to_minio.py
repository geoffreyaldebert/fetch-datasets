import os
import glob
import boto3

s3 = boto3.client("s3",endpoint_url = "https://" + os.environ["AWS_S3_ENDPOINT"],
                  aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), 
                  aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'), 
                  aws_session_token = os.getenv('AWS_SESSION_TOKEN'))

for file in glob.glob('data/*'):
    s3.upload_file( file, "geoffrey", "covid/"+file.split('/')[-1])
