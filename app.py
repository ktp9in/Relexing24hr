from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
import sqlite3
import os

app = Flask(__name__)
DB_FILE = 'qrcodes.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            qr_code TEXT PRIMARY KEY,
            in_time TEXT,
            out_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_qr():
    data = request.get_json()
    qr_code = data.get('qr_code')

    if not qr_code:
        return jsonify({'error': 'QR code not provided'}), 400

    # Trim the last 5 characters as per your requirement
    qr_code = qr_code[:-5]

    now = datetime.now()
    now_iso = now.isoformat()

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Check if the QR code already exists in the database
    cursor.execute("SELECT in_time, out_time FROM scans WHERE qr_code = ?", (qr_code,))
    row = cursor.fetchone()

    if row:
        in_time, out_time = row

        if in_time and out_time:
            # If both in_time and out_time exist, this means the QR code has already been processed
            # We will simply update the out_time on subsequent scans and recalculate the duration
            cursor.execute("""
                UPDATE scans SET out_time = ? WHERE qr_code = ?
            """, (now_iso, qr_code))
            conn.commit()

            # Calculate duration
            dt_in = datetime.fromisoformat(in_time)
            duration = now - dt_in

            # Return a success message with pass/fail based on 24 hours threshold
            if duration >= timedelta(hours=24):
                return jsonify({'result': 'OK - Passed 3 mins', 'status': 'Pass', 'duration': str(duration)})
            else:
                return jsonify({'result': 'NO - Too early', 'status': 'Fail', 'duration': str(duration)})

        elif in_time and not out_time:
            # If the QR code only has an in_time but no out_time, we update the out_time
            cursor.execute("""
                UPDATE scans SET out_time = ? WHERE qr_code = ?
            """, (now_iso, qr_code))
            conn.commit()

            # Calculate duration
            dt_in = datetime.fromisoformat(in_time)
            duration = now - dt_in

            # Return success message based on duration
            if duration >= timedelta(hours=24):
                return jsonify({'result': 'OK - Passed 3 mins', 'status': 'Pass', 'duration': str(duration)})
            else:
                return jsonify({'result': 'NO - Too early', 'status': 'Fail', 'duration': str(duration)})

    else:
        # First scan (in_time is not set yet)
        cursor.execute("""
            INSERT INTO scans (qr_code, in_time) VALUES (?, ?)
        """, (qr_code, now_iso))
        conn.commit()
        conn.close()
        return jsonify({'result': 'OK - First scan recorded', 'status': 'First Scan'})

    conn.close()

@app.route('/data', methods=['GET'])
def get_all_data():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT qr_code, in_time, out_time FROM scans ORDER BY in_time DESC")
    rows = cursor.fetchall()
    conn.close()

    data = []
    for qr, in_time, out_time in rows:
        diff = ''
        status = 'Pending'
        if in_time and out_time:
            dt_in = datetime.fromisoformat(in_time)
            dt_out = datetime.fromisoformat(out_time)
            duration = dt_out - dt_in
            diff = str(duration)
            status = 'Pass' if duration >= timedelta(hours=24) else 'Fail'
        data.append({
            'qr_code': qr,
            'in_time': in_time,
            'out_time': out_time,
            'duration': diff,
            'status': status
        })
    return jsonify(data)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
