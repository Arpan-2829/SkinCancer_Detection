from flask import (
    Flask,
    render_template,
    Response,
    jsonify,
    send_file
)

import cv2
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    GlobalAveragePooling2D,
    Dropout,
    BatchNormalization,
    Dense
)

import numpy as np
import os
import sqlite3
from datetime import datetime
from io import BytesIO



# ==========================================
# Flask App
# ==========================================

app = Flask(__name__)



# ==========================================
# Load Model
# ==========================================

print("Loading ResNet50 model...")

resnet = ResNet50(
    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3)
)

model = Sequential([
    resnet,
    GlobalAveragePooling2D(),
    Dropout(0.5),
    BatchNormalization(),
    Dense(2, activation="softmax")
])

model.load_weights("weights.best.keras")

classes = [
    "BENIGN",
    "MALIGNANT"
]

print("Model loaded successfully.")



# ==========================================
# Webcam
# ==========================================

camera = cv2.VideoCapture(0)

current_frame = None



# ==========================================
# Create Folders
# ==========================================

os.makedirs(
    "database",
    exist_ok=True
)

os.makedirs(
    "static/captures",
    exist_ok=True
)



# ==========================================
# SQLite Database
# ==========================================

conn = sqlite3.connect(
    "database/scans.db",
    check_same_thread=False
)

cursor = conn.cursor()


cursor.execute(
"""
CREATE TABLE IF NOT EXISTS scans(

id INTEGER PRIMARY KEY AUTOINCREMENT,

image TEXT,

prediction TEXT,

confidence REAL,

timestamp TEXT

)
"""
)

conn.commit()



# ==========================================
# Page Routes
# ==========================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )



@app.route("/history_page")
def history_page():

    return render_template(
        "history.html"
    )



@app.route("/analytics")
def analytics():

    return render_template(
        "analytics.html"
    )



@app.route("/reports")
def reports():

    return render_template(
        "reports.html"
    )



@app.route("/settings")
def settings():

    return render_template(
        "settings.html"
    )
# ==========================================
# Generate Frames
# ==========================================

def generate_frames():

    global current_frame

    while True:

        success, frame = camera.read()

        if not success:
            break

        current_frame = frame.copy()

        _, buffer = cv2.imencode(
            ".jpg",
            frame
        )

        frame_bytes = buffer.tobytes()

        yield (

            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'

            + frame_bytes +

            b'\r\n'

        )


# ==========================================
# Video Feed Route
# ==========================================

@app.route("/video_feed")
def video_feed():

    return Response(

        generate_frames(),

        mimetype=
        'multipart/x-mixed-replace; boundary=frame'

    )
# ==========================================
# Capture Scan
# ==========================================

@app.route("/capture")
def capture():

    global current_frame

    if current_frame is None:

        return jsonify({
            "status": "error"
        })


    # Copy current frame
    frame = current_frame.copy()


    # Resize image for model
    resized = cv2.resize(
        frame,
        (224,224)
    )


    # Convert to numpy array
    img = np.expand_dims(
        resized,
        axis=0
    )


    # Predict
    prediction = model.predict(
        img,
        verbose=0
    )


    confidence = float(
        np.max(prediction)
    )

    predicted_class = np.argmax(
        prediction
    )

    label = classes[
        predicted_class
    ]


    # Timestamp
    timestamp = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )


    # Image filename
    filename = datetime.now().strftime(
        "%Y%m%d_%H%M%S.jpg"
    )


    # Save captured image
    image_path = os.path.join(
        "static/captures",
        filename
    )

    cv2.imwrite(
        image_path,
        frame
    )


    # Save to database
    cursor.execute(
        """
        INSERT INTO scans
        (
            image,
            prediction,
            confidence,
            timestamp
        )
        VALUES(?,?,?,?)
        """,

        (
            filename,
            label,
            round(
                confidence*100,
                2
            ),
            timestamp
        )

    )

    conn.commit()


    # Return result
    return jsonify({

        "image": filename,

        "result": label,

        "confidence": round(
            confidence*100,
            2
        ),

        "time": timestamp

    })
# ==========================================
# History API
# ==========================================

@app.route("/history")
def history():

    cursor.execute(
        """
        SELECT
            image,
            prediction,
            confidence,
            timestamp
        FROM scans
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    data = []

    for row in rows:

        data.append({

            "image": row[0],

            "result": row[1],

            "confidence": row[2],

            "time": row[3]

        })

    return jsonify(data)



# ==========================================
# Statistics API
# ==========================================

@app.route("/stats")
def stats():

    # Total scans
    cursor.execute(
        "SELECT COUNT(*) FROM scans"
    )

    total = cursor.fetchone()[0]


    # Benign scans
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM scans
        WHERE prediction='BENIGN'
        """
    )

    benign = cursor.fetchone()[0]


    # Malignant scans
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM scans
        WHERE prediction='MALIGNANT'
        """
    )

    malignant = cursor.fetchone()[0]


    return jsonify({

        "total": total,

        "benign": benign,

        "malignant": malignant

    })



# ==========================================
# Download Report API
# ==========================================

@app.route("/download_report")
def download_report():

    cursor.execute(
        """
        SELECT
            prediction,
            confidence,
            timestamp
        FROM scans
        ORDER BY id DESC
        LIMIT 1
        """
    )

    row = cursor.fetchone()

    if row is None:

        return "No scans available"


    prediction = row[0]

    confidence = row[1]

    timestamp = row[2]


    report = f"""
=========================================
AI SKIN CANCER DETECTION REPORT
=========================================

Prediction:
{prediction}

Confidence:
{confidence} %

Date:
{timestamp}

Model:
ResNet50

Dataset:
HAM10000

Framework:
TensorFlow + Flask

Generated By:
AI Skin Cancer Detection Dashboard

=========================================
"""


    buffer = BytesIO()

    buffer.write(
        report.encode()
    )

    buffer.seek(0)


    return send_file(

        buffer,

        as_attachment=True,

        download_name="report.txt",

        mimetype="text/plain"

    )



# ==========================================
# Run Application
# ==========================================

if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000

    )