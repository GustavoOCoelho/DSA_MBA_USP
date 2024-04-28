import requests
import csv
from classes import CsvWriter

URL = "http://apidatalake.tesouro.gov.br/ords/siconfi/tt/entes"

# Make a GET request to the API endpoint
response = requests.get(URL)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Check if 'items' key exists and it's not empty
    if 'items' in data and data['items']:
        # Extract field names from the first item
        field_names = list(data['items'][0].keys())
        data = data['items']
        # Define the path to the CSV file
        csv_file_path = "api_data"

        CsvWriter(data, field_names).export_data_to_file(csv_file_path)

    else:
        print("No data found in the response.")
else:
    print("Error:", response.status_code)