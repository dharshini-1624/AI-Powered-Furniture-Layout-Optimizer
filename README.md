# 🏠 AI Furniture Layout Optimizer

This project is an AI-powered *Furniture Layout Optimizer* that intelligently arranges furniture in a *2D room layout* based on *room size, obstacles, spacing rules, and functional efficiency. It uses **FastAPI* for backend processing and *Streamlit* for an interactive frontend.

---

## 🚀 Features
✅ *Optimized furniture placement* – No collisions, overlapping, or boundary violations.  
✅ *Obstacle-aware placement* – Avoids placing furniture on obstacles.  
✅ *Functional layout generation* – Pairs furniture logically (e.g., chairs near desks).  
✅ *Dynamic adjustments* – Works with any room size and furniture constraints.  
✅ *FastAPI Backend + Streamlit UI* – Seamless API integration for real-time visualization.  

---

## 🛠 Installation & Setup

1️⃣ Clone the Repository
bash
git clone https://github.com/dharshini-1624/AI-Powered-Furniture-Layout-Optimizer
cd Furniture-Layout-Optimizer

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Replace File Paths 

Make sure to replace the File paths in Model, Backend and Frontend files with your respective system paths 

4️⃣Run the FastAPI Backend

cd Backend
uvicorn furniture_layout_api_optimized:app --host 0.0.0.0 --port 8080 --reload

✅ The API will start at: http://127.0.0.1:8080/docs

5️⃣ Run the Streamlit Frontend

Open a new terminal and run:

cd Frontend
streamlit run furniture_layout_ui_optimized.py

✅ The UI will be available at: http://localhost:8501/


---

🖥 Usage Guide

1️⃣ Enter Room Width & Height.
2️⃣ Select furniture (comma-separated).
3️⃣ Specify obstacles (if any) in x,y format (e.g., 2,3;5,5).
4️⃣ Click "Generate Layout" to see the optimized placement.

🔹 The app will display a 2D visualization of the furniture arrangement.

---

📦 Requirements

Python Version

Python 3.8+ is recommended.


Dependencies

All required dependencies are listed in requirements.txt and can be installed using:

pip install -r requirements.txt

---

❓ Troubleshooting

API not running?
Ensure FastAPI is running before starting Streamlit UI. Use:

uvicorn furniture_layout_api_optimized:app --host 0.0.0.0 --port 8080 --reload

Streamlit UI not loading?

Ensure correct port (8501) is not blocked.

Run streamlit run furniture_layout_ui_optimized.py from the correct directory.

---
