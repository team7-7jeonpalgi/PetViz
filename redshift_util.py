import os
import traceback
import requests
import pandas as pd
import boto3
from botocore.exceptions import NoCredentialsError

from redshift_config import download_files, PATH_DOWNLOAD, PATH_CSV, S3_BUCKET_NAME, S3_PROJECT_PATH, AWS_ACCESS_KEY, \
    AWS_SECRET_KEY, addr_to_code


def download_file(save_path, download_url):
    try:
        # Send HTTP GET request to download the file
        response = requests.get(download_url, stream=True)
        response.raise_for_status()  # Raise HTTPError for bad responses (e.g., 404, 403)

        # Write file content to disk
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"File downloaded successfully: {save_path}")
        return save_path

    except requests.RequestException as e:
        print(f"Error downloading file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def animal_hospital_addr_to_code():
    df = pd.read_csv('data/csv/animal_hospital.csv')
    df['location_code'] = df['addr'].astype(str).apply(lambda x: addr_to_code.get(x.split()[0], 'not found'))
    df.to_csv('data/csv/animal_hospital.csv', index=False)
    print('location_code added to animal_hospital.csv')


def excel_to_csv(input_excel_path: str, output_parquet_path: str,
                 dtype, index_col=None):
    try:
        df = pd.read_excel(input_excel_path, names=dtype.keys(), dtype=dtype, index_col=index_col)
        for col in df.columns:
            if df[col].dtype == 'object':  # Check for string type columns
                df[col] = df[col].astype(str).str.replace('\n', '', regex=False)
        print(f"엑셀 파일 '{input_excel_path}'을 성공적으로 읽었습니다. (행 개수: {len(df)}), (열 개수: {len(df.columns)})")
        df.to_csv(output_parquet_path, index=False)
        print(f"csv 파일로 저장되었습니다: {output_parquet_path}")
        return df

    except Exception as e:
        print(traceback.format_exc())
        print(f"오류가 발생했습니다: {e}")


def upload_folder_to_s3(local_folder, bucket_name, s3_folder, aws_access_key, aws_secret_key):
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )
    try:
        # Iterate over all files in the local directory
        for root, dirs, files in os.walk(local_folder):
            for file_name in files:
                # Construct the full local file path
                local_file_path = os.path.join(root, file_name)

                # Construct the S3 destination key (folder + file name)
                # Remove the local folder prefix from file path to get relative path
                relative_path = os.path.relpath(local_file_path, local_folder)
                s3_file_path = os.path.join(s3_folder, relative_path).replace("\\", "/")  # Use Unix-style S3 paths

                # Upload the file
                s3.upload_file(local_file_path, bucket_name, s3_file_path)
                print(f"Uploaded '{local_file_path}' to 's3://{bucket_name}/{s3_file_path}'")

    except NoCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print(f"An error occurred: {e}")

    s3.close()


def redshift_setting():
    for name, info in download_files.items():
        dtype, url = info
        download_path = os.path.join(PATH_DOWNLOAD, f'{name}.xls')
        csv_path = os.path.join(PATH_CSV, f'{name}.csv')

        download_file(download_path, url)
        excel_to_csv(download_path, csv_path, dtype)

    animal_hospital_addr_to_code()
    upload_folder_to_s3(PATH_CSV, S3_BUCKET_NAME, S3_PROJECT_PATH, AWS_ACCESS_KEY, AWS_SECRET_KEY)
