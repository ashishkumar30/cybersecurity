import csv
import requests


def ingest_logs(file_path):
    """
    Ingests logs from a CSV file and sends them as POST requests to a remote API.

    This function reads a CSV file where each row represents a log entry.
    For each row, it sends a POST request with the log data in JSON format to a specified API endpoint.

    Args:
        file_path (str): The path to the CSV file containing raw log data. The file should have headers
                         corresponding to the fields expected by the API.
    """
    with open(file_path, 'r') as csvfile:
        # Use DictReader to read the CSV as a dictionary
        reader = csv.DictReader(csvfile)

        # Loop through each row in the CSV
        for row in reader:
            # Send the log data as a POST request to the API endpoint
            response = requests.post('http://localhost:8000/api/logs', json=row)

            # Print the status code and response from the API
            print(response.status_code, response.json())


if __name__ == '__main__':
    # Call the ingest_logs function with the path to the CSV file
    ingest_logs('raw_logs_input.csv')
