QR Code Scanner Web App
This project is a QR code scanner web application built with Flask. It allows users to scan or enter QR codes, track the scanning times, and check the time difference between the "in" and "out" times to determine whether a scan passes or fails based on a 24-hour threshold. The results are displayed in a user-friendly interface with QR code history and pass/fail status.

Company
This project is developed and used by Thai Sukeno Knit Co., Ltd..

Features
QR Code Scanning: Users can scan or manually enter QR codes.

Pass/Fail Logic: Checks if the QR code scan is valid based on the time difference between the "in" and "out" times, passing if the difference is greater than 24 hours.

Data Persistence: Scanning data is stored in a local SQLite database for history tracking.

Interactive Interface: View the list of all scans, including QR codes, in-time, out-time, duration, and pass/fail status.

Project Setup
Requirements
Python 3.x

Flask

SQLite3

Installation
Clone the repository:

bash
Copy
Edit
git clone <repository-url>
cd <project-directory>
Install the required dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Create the SQLite database:

bash
Copy
Edit
python app.py
Running the Application
Run the Flask application:

bash
Copy
Edit
python app.py
Open your browser and go to http://127.0.0.1:5000/.

Enter or scan a QR code, and the results will be displayed.

Database
The application uses an SQLite database (qrcodes.db) to store the scan data. The database has the following table:

scans:

qr_code: The scanned QR code.

in_time: The timestamp when the QR code was first scanned.

out_time: The timestamp when the QR code was scanned again.

File Structure
app.py: Main Flask application file.

index.html: The HTML template for the web interface.

static/script.js: JavaScript for handling user interactions.

qrcodes.db: SQLite database to store scan data.

How It Works
First Scan: When a QR code is first scanned, it is recorded with the current time as the "in-time".

Subsequent Scans: On a subsequent scan, the "out-time" is recorded. The duration between the "in-time" and "out-time" is calculated.

Pass/Fail: If the duration between the "in-time" and "out-time" is greater than 24 hours, the scan is marked as "Pass". If it's less than 24 hours, it is marked as "Fail".

API Endpoints
POST /scan: Accepts a JSON payload with a QR code and processes it.

GET /data: Retrieves all scan data, including the QR code, in-time, out-time, duration, and status.

Technologies Used
Flask: A lightweight Python web framework.

SQLite3: A self-contained SQL database for storing scan data.

Bootstrap: For a responsive and simple UI.

License
This project is licensed under the MIT License - see the LICENSE file for details.
