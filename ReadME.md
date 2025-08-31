# FSD-Project (CRUD Application)

This is a Full Stack CRUD application built with **FastAPI (Backend)** and a simple **HTML/JS Frontend**.  
It covers basic **Create, Read, Update, Delete** operations and demonstrates full-stack development skills.

---

## 🚀 Technologies Used
- **Backend**: FastAPI (Python), Uvicorn
- **Database**: SQLite (default, can be changed)
- **Frontend**: HTML, CSS, JavaScript (basic UI)
- **Version Control**: Git & GitHub

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Samyuktha1017/FSD-Project.git
cd FSD-Project
2. Run the Backend
bash
Copy code
cd backend
python -m venv .venv
.venv\Scripts\activate     # On Windows
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
➡️ Backend will start at: http://127.0.0.1:8000

3. Run the Frontend
bash
Copy code
cd frontend
python -m http.server 5500
➡️ Open: http://127.0.0.1:5500

📌 Features
Add new records

View all records

Edit records

Delete records

Fully connected frontend & backend

📷 Screenshot
(Add a screenshot of your app once running)

👩‍💻 Author
Samyuktha

GitHub: Samyuktha1017

yaml
Copy code

---

👉 Next step:  
Run this command in your project root to add the README:  

```bash
echo "# FSD-Project (CRUD Application)" > README.md
(or copy the whole content above into a file named README.md in VS Code).

Then commit & push:

bash
Copy code
git add README.md
git commit -m "Added README with setup instructions"
git push origin main
