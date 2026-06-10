# 🩺 AI Skin Cancer Detection System

An AI-powered Skin Cancer Detection Dashboard built using **TensorFlow, ResNet50, Flask, OpenCV, and SQLite** for real-time skin lesion analysis and classification.

---

# 🚀 Features

* 🎥 Real-time webcam streaming
* 📷 Capture skin lesion images
* 🧠 Deep learning-based classification using ResNet50
* 🔬 Benign vs Malignant prediction
* 📊 Confidence score visualization
* 📈 Analytics dashboard with charts
* 🗂 Detection history tracking
* 📄 Downloadable scan reports
* 💾 SQLite database integration
* 🌐 Modern Flask-based dashboard
* 📱 Responsive UI

---

# 🛠 Technologies Used

* Python
* TensorFlow
* Keras
* ResNet50
* Flask
* OpenCV
* SQLite
* HTML
* CSS
* JavaScript
* Bootstrap 5
* Chart.js

---

# 📂 Project Structure

```text
Skin-Cancer-Detection-System
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── models
│     └── weights.best.keras
│
├── database
│     └── scans.db
│
├── templates
│     ├── index.html
│     ├── history.html
│     ├── analytics.html
│     ├── reports.html
│     └── settings.html
│
├── static
│     ├── css
│     │     └── style.css
│     │
│     ├── js
│     │     └── script.js
│     │
│     └── captures
│
└── notebook
      Skin_Cancer_Model_Training.ipynb
```

---

# 🧠 Model Architecture

* Base Model: **ResNet50**

* Input Size: **224 × 224**

* Output Classes:

  * BENIGN
  * MALIGNANT

* Framework: TensorFlow + Keras

---

# 📊 Dataset

### HAM10000 Dataset

* 10,015 dermatoscopic images
* Binary Classification
* Medical skin lesion dataset

---

# 📥 Download Pretrained Model

The trained model file is not included in this repository because of GitHub file size limitations.

Download the pretrained model from:

### Google Drive

https://drive.google.com/file/d/1K7FahYSRzOXMeaytPBp7itzXpXYOgg4J/view?usp=drive_link

Place the downloaded file inside:

```text
models/weights.best.keras
```

Directory structure:

```text
models
│
└── weights.best.keras
```

---

# ⚙ Installation

Clone the repository:

```bash
git clone https://github.com/Arpan-2829/SkinCancer_Detection.git
```

Move into project directory:

```bash
cd SkinCancer_Detection
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

# 📈 Dashboard Features

### Dashboard

* Live webcam feed
* Capture scan
* Prediction confidence
* Download reports

### History

* View previous scans
* Confidence values
* Timestamp records

### Analytics

* Pie charts
* Confidence trend visualization

### Reports

* Export reports

### Settings

* Model information
* System information

---

# 🔮 Future Improvements

* Grad-CAM Heatmaps
* PDF Report Generation
* CSV Export
* Search and Pagination
* Explainable AI
* Dark/Light Mode
* Multi-class Classification

---

# ⚠ Disclaimer

This project is intended for educational and research purposes only.

It is **not a substitute for professional medical diagnosis or treatment**. Always consult qualified healthcare professionals for clinical decisions.

---

# 👨‍💻 Author

### Arpan Patil

Computer Science Engineer | AI & Data Science Enthusiast

GitHub:

https://github.com/Arpan-2829

---

⭐ If you found this project useful, consider giving the repository a star.
