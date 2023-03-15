from google.cloud import storage
from google.oauth2 import service_account

'''
구글 스토리지에 파일 업로드
'''

def gcs_upload_file():
    KEY_PATH = "../gcp_sa_key/pj-k8s-f59b8185e976.json"
    credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
    client = storage.Client(credentials = credentials, project = credentials.project_id)

    buckets = list(client.list_buckets())
    bucket_name = "gcs-get-resource"

    bucket = client.get_bucket(bucket_name)
    blob_name = "resource_list.csv"
    file_path = "../resource_data/resource_list.csv"

    blob = bucket.blob(blob_name)
    blob.upload_from_filename(file_path)
    print("Success uploadgcs.py") 

