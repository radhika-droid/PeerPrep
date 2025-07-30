# 📚 PeerPrep – Student Peer Learning & Resource Hub

PeerPrep is an open-source platform built to empower students to share notes, ask questions, and collaborate through peer-to-peer learning.

---

## 🚀 Features
- 📄 Share notes and study guides with the community  
- 💬 Ask and answer academic questions in a Q&A forum  
- 🤝 Find and connect with study partners who share your interests  
- 🏆 Earn points, badges, and recognition for your contributions  
- 🔍 Search by subject, topic, or user  

---

## 🛠️ Tech Stack
- **Frontend**: HTML, CSS, JavaScript  
- **Backend**: Django  
- **Database**: SQLite

---

## 🧑‍💻 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/peerprep.git
   cd peerprep
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   
   **On Linux/macOS:**
   ```bash
   source venv/bin/activate
   ```
   
   **On Windows:**
   ```bash
   venv\Scripts\activate
   ```

4. **Install dependencies:**

   **Using pip:**
   ```bash
   pip install django
   ```
   
   **Using uv (recommended):**
   ```bash
   uv pip install django
   ```

5. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Open your browser and visit:**
   ```
   http://127.0.0.1:8000/
   ```

### Optional: Create Admin User
To access the Django admin panel, create a superuser:
```bash
python manage.py createsuperuser
```
Then visit: `http://127.0.0.1:8000/admin/`

---

## 🚀 Quick Start (One-liner)
```bash
git clone https://github.com/your-username/peerprep.git && cd peerprep && python3 -m venv venv && source venv/bin/activate && pip install django && python manage.py migrate && python manage.py runserver
```

---

## 📝 Contributing
We welcome contributions! Please feel free to submit a Pull Request.

---

## 📄 License
This project is licensed under the MIT License.
