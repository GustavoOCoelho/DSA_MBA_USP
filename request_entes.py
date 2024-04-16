import requests
import csv

url = "http://apidatalake.tesouro.gov.br/ords/siconfi/tt/entes"

# Make a GET request to the API endpoint
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Check if 'items' key exists and it's not empty
    if 'items' in data and data['items']:
        # Extract field names from the first item
        field_names = list(data['items'][0].keys())

        # Define the path to the CSV file
        csv_file_path = "api_data.csv"

        # Write data to CSV file
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=field_names)

            # Write the header
            writer.writeheader()

            # Write all data rows
            writer.writerows(data['items'])

        print("Data has been saved to", csv_file_path)
    else:
        print("No data found in the response.")
else:
    print("Error:", response.status_code)