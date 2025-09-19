# Embedded Intelligent Microscopy System for Identification and Counting of Microscopic Marine Organisms

**Problem proposed by:** Ministry of Earth Sciences  

**Project type:** Group Project (Smart India Hackathon 2025 — SIH25043)  

## 👥 Team Members
- Suhani Mishra (Team Leader)  
- Divyanshi Rajotia  
- Netra Jain  
- Sukriti Pandey  
- Aradhna Lal  
- Muskan  

---

## 📌 Short Description
This repository contains the software prototype for an **embedded intelligent microscopy system** that:
- Captures live images from a USB microscope camera  
- Counts microscopic organisms (OpenCV contour-based counting)  
- Classifies species using a trained CNN model (TensorFlow/Keras)  
- Logs results to CSV  
- Sends output to Arduino via serial for further hardware interaction/display  

---

## 🛠️ Main Tech Stack
- **AI / ML:** TensorFlow / Keras (`microbe_model.h5`)  
- **Computer Vision & Capture:** OpenCV (cv2)  
- **Numerical Computing:** NumPy  
- **I/O:** JSON (class mappings), CSV (results logging)  
- **Hardware Integration:** PySerial + Arduino  
- **Runtime:** Python 3.8+  

---

## 🚀 Quick Start (Local Setup)
1. **Clone the repo** (or initialize and push your local project).  
2. **Create a Python virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS / Linux:
   source venv/bin/activate
Install dependencies:

pip install -r requirements.txt


Ensure trained model + labels are available in organism_detection/:

organism_detection/microbe_model.h5

organism_detection/class_indices.json

Connect your USB microscope and Arduino (if used). Run the main script:

python src/main.py


Press s → capture & analyze current frame

Press q → quit

📂 Notes on Large Files

GitHub blocks files >100 MB. If your .h5 model is large, use Git LFS:

git lfs install
git lfs track "*.h5"
git add .gitattributes
git add organism_detection/microbe_model.h5
git commit -m "Add model via Git LFS"
git push origin main


Alternatively: upload large models/datasets in GitHub Releases, or store them in cloud storage (Google Drive, AWS S3, etc.).

⚙️ Suggested .gitignore
venv/
__pycache__/
*.pyc
*.pkl
*.h5
.DS_Store
.env
.vscode/
.idea/
data/


ℹ️ If you’re using Git LFS for .h5 files, remove *.h5 from .gitignore.

🎥 Usage & Demo

Run live capture:

python src/main.py


Press s to analyze → results are shown, logged to CSV, and sent via serial to Arduino.

Project presentation:
presentation/SIH2025-IDEA-Presentation.pptx (include in repo root or docs/ folder).

📜 License & Attribution

Choose a license (MIT / Apache-2.0 recommended) and add it as LICENSE in repo root.

This project was developed as part of the Smart India Hackathon 2025.
Problem statement proposed by the Ministry of Earth Sciences.

📧 Contact

Project Lead: Suhani Mishra
📩 Email: btbtc23195_suhani@banasthali.in


---