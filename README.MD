# Cybersecurity Threat Detection System

### **PFA of Screenshots of API testing in 'API testing Screenshot folder'

## Overview

The **Cybersecurity Threat Detection System** is designed to detect and visualize cybersecurity threats. It provides a web-based interface to view detected threats, along with a secure API for managing threat data. This project consists of two main applications: `Log_ingestor` and `Threat_analyzer`.

- **Log_ingestor**: Handles the ingestion of raw log data.
- **Threat_analyzer**: Analyzes logs to detect potential threats based on predefined criteria.

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL

## Project Structure

The project is divided into the following components:

1. **cybersecurity**: The main application containing settings, URLs, and server configurations.
2. **log_ingestor**: Contains models, serializers, views, and components for handling log data.
3. **threat_analyzer**: Analyzes log data to detect potential threats.

## Project Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone git@github.com:ashishkumar30/cybersecurity-threat-detection.git
   cd cybersecurity-threat-detection
   cd cybersecurity
   ```
2. Now you are in the project directory and these files are available here
   1. raw_logs_input.csv
   2. manage.py
   3. requirements.txt
   4. cybersecurity
   5. log_ingestor
   6. threat_analyzer
   7. upload_data.py
   8. db.sqlite3
   9. API testing Screenshot
   10. README.MD


1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL**:
   Ensure you have PostgreSQL installed and set up a database for the project. Update the database configuration in `settings.py` to match your PostgreSQL setup.

3. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Run the server**:
   Start the Django development server using the following command:
   ```bash
   python manage.py runserver 8000
   ```

   The application will now be running on `http://localhost:8000`.

5. Open Another tab and Upload the data using the following command
   ```bash
   python3 upload_data.py
   ```
   
## Uploading Data Using `upload_data.py`

The **`upload_data.py`** script allows you to insert bulk log data into the database by sending a POST request to the `log_ingestor` API.

### Steps:

1. Ensure your server is running on `http://localhost:8000` using the command:
   ```bash
   python manage.py runserver 8000
   ```

2. **Create or use a CSV file** (`raw_logs_input.csv`) containing raw log data.

3. **Run the `upload_data.py` script** to insert the data into the database:
   ```bash
   python3 upload_data.py
   ```

   The script will read the data from the CSV file and send POST requests to insert the data into the log ingestion API. It will also print the response status code and message for each POST request.

   **Example of CSV file format
## Applications Overview

### 1. **Log_ingestor**: 
This module handles the ingestion of raw log data, providing APIs to retrieve and insert logs.

#### API Endpoints:

- **GET /api/logs**: Retrieve all logs.
    ```json
    [
        {
            "id": 1,
            "timestamp": "2025-04-01T17:40:05.023874Z",
            "user_id": "admin42",
            "ip_address": "192.168.1.20",
            "action": "database_query",
            "file_name": "",
            "database_query": ""
        },
        {
            "id": 2,
            "timestamp": "2025-04-01T17:40:05.028323Z",
            "user_id": "guest99",
            "ip_address": "192.168.1.20",
            "action": "network_request",
            "file_name": "/confidential/design.pdf",
            "database_query": ""
        }
    ]
    ```

- **POST /api/logs**: Insert a log into the system.
    **Request**:
    ```json
    {
        "user_id": "user1xxx23",
        "ip_address": "172.16.0.0",
        "action": "network_request",
        "file_name": "/logs/system.log",
        "database_query": "DELETE TABLE"
    }
    ```

    **Response**:
    ```json
    {
        "id": 2009,
        "timestamp": "2025-04-01T17:46:24.063346Z",
        "user_id": "user1xxx23",
        "ip_address": "172.16.0.0",
        "action": "network_request",
        "file_name": "/logs/system.log",
        "database_query": "DELETE TABLE"
    }
    ```

- **GET /api/logs/{id}**: Retrieve a log by ID (e.g., `/api/logs/5`).
    **Response**:
    ```json
    {
        "id": 5,
        "timestamp": "2025-04-01T17:40:05.038066Z",
        "user_id": "admin42",
        "ip_address": "8.8.8.8",
        "action": "file_access",
        "file_name": "/secure/payroll.csv",
        "database_query": "DROP TABLE transactions;"
    }
    ```

- **POST /api/logs/search**: Search for logs based on parameters.
    **Request**:
    ```json
    {
        "timestamp": "2025-03-26T14:35:21Z",
        "userId": "user123",
        "ipAddress": "192.168.1.10"
    }
    ```

    **Response**:
    ```json
    [
        {
            "id": 47,
            "timestamp": "2025-04-01T17:40:05.135443Z",
            "user_id": "user123",
            "ip_address": "192.168.1.10",
            "action": "file_access",
            "file_name": "/logs/system.log",
            "database_query": ""
        },
        {
            "id": 54,
            "timestamp": "2025-04-01T17:40:05.150751Z",
            "user_id": "user123",
            "ip_address": "192.168.1.10",
            "action": "file_access",
            "file_name": "/secure/payroll.csv",
            "database_query": ""
        },
        {
            "id": 67,
            "timestamp": "2025-04-01T17:40:05.179866Z",
            "user_id": "user123",
            "ip_address": "192.168.1.10",
            "action": "network_request",
            "file_name": "",
            "database_query": ""
        }
    ]
    ```

### 2. **Threat_analyzer**: 
This module analyzes logs to detect potential cybersecurity threats.

#### API Endpoints:

- **POST /api/threats**: Detect threats from uploaded log file.
    **Request**: Upload a CSV file containing log data.

    **Response**:
    ```json
    {
        "message": "Threats detected",
        "Total no of Threats detected": 109,
        "threats": {
            "1d871349-1cfc-40bb-974f-862ec3530339": {
                "timestamp": "2025-03-26T00:04:00",
                "user_id": "employee7",
                "ip_address": "192.168.1.10",
                "action": "file_access",
                "file_name": "/confidential/design.pdf",
                "threat_type": "InsiderThreat",
                "severity": "Medium"
            },
            "111b3754-1703-4068-95db-779bec3e0a94": {
                "timestamp": "2025-03-26T00:07:00",
                "user_id": "root",
                "ip_address": "192.168.1.10",
                "action": "file_access",
                "file_name": null,
                "threat_type": "InsiderThreat",
                "severity": "Medium"
            }
        }
    }
    ```

- **GET /api/threats/{id}**: Retrieve a threat by ID.
    **Response**:
    ```json
    {
        "id": 6,
        "timestamp": "2025-03-26T00:40:00Z",
        "user_id": "guest99",
        "ip_address": "192.168.1.20",
        "action": "file_access",
        "file_name": "/db_dump.sql",
        "threat_type": "InsiderThreat",
        "severity": "Medium"
    }
    ```

- **POST /api/threats/search**: Search for threats based on parameters.
    **Request**:
    ```json
    {
        "timestamp": "2025-03-26T00:40:00Z",
        "userId": "guest99",
        "ipAddress": "192.168.1.20"
    }
    ```

    **Response**:
    ```json
    [
        {
            "id": 1,
            "timestamp": "2025-03-26T00:04:00Z",
            "user_id": "employee7",
            "ip_address": "192.168.1.10",
            "action": "file_access",
            "file_name": "/confidential/design.pdf",
            "threat_type": "InsiderThreat",
            "severity": "Medium"
        },
        {
            "id": 2,
            "timestamp": "2025-03-26T00:07:00Z",
            "user_id": "root",
            "ip_address": "192.168.1.10",
            "action": "file_access",
            "file_name": "nan",
            "threat_type": "InsiderThreat",
            "severity": "Medium"
        }
    ]
    ```

