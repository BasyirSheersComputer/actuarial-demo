import logging
import azure.functions as func
import pandas as pd
from azure.storage.filedatalake import DataLakeServiceClient
import os
from io import StringIO

def get_datalake_client():
    account_name = os.environ["STORAGE_ACCOUNT_NAME"]
    account_key = os.environ["STORAGE_ACCOUNT_KEY"]
    return DataLakeServiceClient(account_url=f"https://{account_name}.dfs.core.windows.net", credential=account_key)

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        input_path = req.params.get("inputPath") or req.get_json().get("inputPath")
        output_path = req.params.get("outputPath") or req.get_json().get("outputPath")
        file_system = "raw"  # change if needed

        # Connect to Data Lake
        dl_client = get_datalake_client()
        file_system_client = dl_client.get_file_system_client(file_system)

        # Read raw file
        raw_file = file_system_client.get_file_client(input_path)
        download = raw_file.download_file().readall()
        df = pd.read_csv(StringIO(download.decode('utf-8')))

        # Sample transformation
        df = df.drop(columns=["region"])
        df["charges"] = df["charges"].round(2)

        # Write cleaned file to /processed/
        csv_out = df.to_csv(index=False)
        processed_path = output_path or input_path.replace("/raw/", "/processed/")
        processed_file = file_system_client.get_file_client(processed_path)
        processed_file.create_file()
        processed_file.append_data(data=csv_out, offset=0, length=len(csv_out))
        processed_file.flush_data(len(csv_out))

        return func.HttpResponse(f"File transformed and saved to {processed_path}", status_code=200)

    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
