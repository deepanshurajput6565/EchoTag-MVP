# 🥷 EchoTag
**Advanced Digital Asset Protection & Piracy Detection** *Built by Team Anbu Code for the Build with AI Solution Challenge 2026*

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-FF4B4B.svg)](https://streamlit.io/)
[![Gemini API](https://img.shields.io/badge/Google%20Gemini-1.5%20Flash-orange.svg)](https://aistudio.google.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green.svg)](https://opencv.org/)

> EchoTag merges steganographic pixel cryptography with generative AI to make the removal of digital tracking data mathematically and contextually impossible.

---

## 📑 Table of Contents
1. [The Problem](#-the-problem)
2. [Our Solution: Dual-Layered Security](#-our-solution-dual-layered-security)
3. [System Architecture](#-system-architecture)
4. [Tech Stack](#-tech-stack)
5. [Live Demo & Links](#-live-demo--links)
6. [Getting Started (Local Setup)](#-getting-started-local-setup)
7. [API Documentation](#-api-documentation)
8. [Project Structure](#-project-structure)
9. [The Team](#-the-team)

---

## ⚠️ The Problem
Digital piracy costs the live sports and high-value media industry billions of dollars annually. While broadcasters use digital watermarks to track the source of leaked streams, pirates easily bypass them using low-tech methods:
* **Cropping** the video frame to remove logos.
* **Applying blur filters** to destroy tracking pixels.
* **Screen-recording** to bypass DRM entirely.

Once the watermark is destroyed, the original leaker becomes untraceable, and automated takedown bots fail to recognize the content as copyrighted.

---

## 💡 Our Solution: Dual-Layered Security
EchoTag solves this by combining low-level computer vision with high-level LLM semantic analysis.

### Layer 1: The Cryptographic Engine (LSB Steganography)
We engineered a custom Python-based Least Significant Bit (LSB) encoder. It modifies the 8th bit of an image's RGB values to hide an encrypted origin payload directly inside the pixel data. 
* **Invisible:** Completely imperceptible to the human eye.
* **Automated:** If a leaked image is uploaded, our FastAPI backend instantly extracts the payload, identifies the leaker, and flags a **🚨 Confirmed Piracy** event.

### Layer 2: Semantic AI Fallback (Google Gemini 1.5 Flash)
If a pirate successfully degrades or crops the image enough to destroy the LSB payload, traditional automated scripts fail. EchoTag automatically routes the degraded media to **Google Gemini 1.5 Flash**. 
* Using a highly tuned semantic prompt, the AI analyzes the visual context (e.g., recognizing a cricket pitch, team jerseys, or broadcast graphics). 
* Even without a watermark, the AI identifies the high-value asset and triggers a **⚠️ Suspected Piracy** alert for manual review.

---

## 📐 System Architecture

1. **User Uploads Media** ➔ Streamlit Frontend.
2. **Media Sent to API** ➔ FastAPI Backend receives the payload via `POST /api/scan-image`.
3. **Primary Scan (Cryptography)** ➔ OpenCV & NumPy attempt to extract the LSB payload.
   * *If Payload Found* ➔ Return **Confirmed Piracy** & Origin Data.
   * *If Payload Missing* ➔ Proceed to AI Fallback.
4. **Secondary Scan (AI)** ➔ Image is encoded and sent to Google Gemini 1.5 Flash API.
   * *If Broadcast Detected* ➔ Return **Suspected Piracy**.
   * *If Standard Image* ➔ Return **Media is Clean**.

---

## ⚙️ Tech Stack
* **AI Model:** Google Gemini 1.5 Flash API *(Semantic Fallback)*
* **Backend:** Python, FastAPI, Uvicorn, Pydantic
* **Computer Vision:** OpenCV (`cv2`), NumPy *(Pixel-level matrix manipulation)*
* **Frontend:** Streamlit *(Rapid UI deployment)*
* **Cloud Infrastructure:** Render (API Hosting), Streamlit Community Cloud (Frontend)

---

## 🚀 Live Demo & Links
* **Live Web App (Frontend):** [Insert your .streamlit.app link here]
* **Cloud API (Backend):** [Insert your .onrender.com link here]
* **Demo Video:** [Insert your YouTube/Loom link here]

---

## 💻 Getting Started (Local Setup)

### Prerequisites
* Python 3.9 or higher installed.
* A valid Google AI Studio API Key.

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/EchoTag-MVP.git](https://github.com/yourusername/EchoTag-MVP.git)
cd EchoTag-MVP

2. Set Up a Virtual Environment
Bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

3. Install Dependencies
Bash
pip install -r requirements.txt

4. Configure Environment Variables
Create a .env file in the root directory and add your Gemini API key:

Code snippet
GEMINI_API_KEY="your_google_ai_api_key_here"

5. Run the Backend Server
Open your first terminal and start the FastAPI server:

Bash
uvicorn main:app --reload --port 10000
The API will be available at http://localhost:10000

6. Run the Frontend UI
Open a second terminal and start the Streamlit app:

Bash
streamlit run app.py
The UI will launch in your browser at http://localhost:8501

🔌 API Documentation
POST /api/scan-image
Analyzes an uploaded image for steganographic watermarks and applies AI fallback if necessary.

Request:

Content-Type: multipart/form-data

Body: file (Image file: .png, .jpg, .jpeg)

Success Response (Watermark Found):

JSON
{
  "status": "piracy_detected",
  "action_triggered": "Automated Takedown Request",
  "detection_method": "Cryptographic Watermark (LSB)",
  "payload": "User_ID: 98765 | IP: 192.168.1.1"
}
Success Response (AI Fallback Triggered):

JSON
{
  "status": "piracy_suspected",
  "action_triggered": "Flagged for Manual Review",
  "detection_method": "Gemini AI Semantic Analysis",
  "confidence": "High"
}
📂 Project Structure
Plaintext
EchoTag-MVP/
│
├── main.py               # FastAPI backend & logic routing
├── app.py                # Streamlit frontend UI
├── core/
│   ├── encoder.py        # LSB steganography insertion script
│   ├── decoder.py        # LSB extraction logic
│   └── ai_engine.py      # Google Gemini API integration
│
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment variables
├── .gitignore            # Git ignore rules
└── README.md             # Project documentation
🥷 The Team
Team Anbu Code ABES Engineering College, Ghaziabad

Deepanshu Rajput - Team Leader & Full Stack Integration
