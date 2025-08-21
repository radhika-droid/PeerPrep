# PeerPrep – Collaborative Learning Platform 📚🤝

![License](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Django](https://img.shields.io/badge/Django-4.x-green.svg)

PeerPrep is an **innovative collaborative learning platform** that connects students across the globe for **peer-to-peer study sessions**, resource sharing, and progress tracking.  
Our mission is to **empower learners** to achieve their academic goals through community-driven learning. 🤝

---

## 📋Table of Contents
1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Getting Started](#getting-started)
5. [Contributing](#contributing)
6. [License](#license)
7. [Contact](#contact)

---

## 🚀 Features
- **Collaborative Learning** – Connect with peers worldwide for effective study sessions.  
- **Structured Content** – Access curated learning materials and practice problems.  
- **Goal Tracking** – Monitor your progress with analytics and insights.  
- **Live Chat** – Get instant support from peers or mentors.  
- **Planned Features**:
  - AI-powered study partner matching  
  - Gamification with badges and leaderboards  
  - Integration with popular note-taking tools  



---

## 🛠 Tech Stack
- **Frontend:** HTML5, CSS3, JavaScript (vanilla)  
- **Backend:** Django 4.x (Python 3.12)  
- **Database:** SQLite (default)  
- **Environment:** Virtualenv  
- **Other:** Responsive design, smooth animations, MIT License  

---
## 🗂 Project Structure
```
PeerPrep/
├── core/                     # Main application logic (Django core configs)
├── peerprep/                 # Project-specific app (settings, URLs, WSGI, ASGI)
├── static/                   # Static files (CSS, JS, Images)
├── templates/                # HTML templates for frontend
├── venv/                     # Virtual environment (should be excluded in .gitignore)
│
├── db.sqlite3                # SQLite database (default for dev)
├── manage.py                 # Django project management script
│
├── .gitignore                # Git ignore rules
├── CODE_OF_CONDUCT.md        # Contributor code of conduct
├── LICENSE                   # Project license
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies

```
---

## 🏁 Getting Started

Follow these steps to get the project up and running locally:
1. Clone the Repository
```bash
git clone https://github.com/yourusername/peerprep.git
cd peerprep
```
2. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```
3. Install Dependencies
```bash
pip install -r requirements.txt
```
4. Apply Migrations
```bash
python manage.py migrate
```
5. Run the Development Server
```bash
python manage.py runserver
```
Visit http://127.0.0.1:8000 in your browser to start using PeerPrep. 🚀.

---

## 🤝 Contributing
We welcome contributions from everyone! 🙌

Steps to contribute:

- Fork the repository
- Create a new branch (git checkout -b feature-name)
- Make your changes and commit (git commit -m "Add feature")
- Push to your branch (git push origin feature-name)
- Open a Pull Request
- 
Please follow our Code of Conduct to ensure a safe and respectful environment.
Please read our [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a positive and respectful community.

---

## License
This project is licensed under the [MIT License](License) – see the LICENSE file for details.

---

**🙌 Thank You, Contributors!**
> Thank you once again to all our contributors! Your efforts are truly appreciated. 💖👏
<p align="center">
  <a href="https://github.com/radhika-droid/PeerPrep/graphs/contributors">
    <img src="https://api.vaunt.dev/v1/github/entities/radhika-droid/repositories/PeerPrep/contributors?format=svg&limit=54" width="700" height="250" />
  </a>
</p>

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">


## 📬 Contact
>  If you like this project, consider giving it a  ⭐ and sharing it with friends!

<p align="center">
Maintained with ❤️ by the radhika-droid/PeerPrep
</p>

<p align="center">
  <a href="#top" style="font-size: 18px; padding: 8px 16px; display: inline-block; border: 1px solid #ccc; border-radius: 6px; text-decoration: none;">
    ⬆️ Back to Top
  </a>
</p>
