# 🎟️ Eventify

## 📌 Project Overview

This project is a **FastAPI-based backend** for an event ticket management system. It provides a **secure, scalable, and efficient** platform for event organizers and attendees. The system is designed for three user roles:

- **👨‍💼 Admin**: Manages clients, oversees event statistics, and maintains the system.
- **🎭 Client**: Hosts multiple events, manages event inventory, and schedules event times.
- **👤 User**: Searches, filters, and books events, manages cart, selects seats, and makes payments.

---

## 🚀 Features

### ✅ **Admin Panel**
- 📊 Dashboard for business statistics
- 👥 Manage clients (add, remove, update)

### ✅ **Client Panel**
- 🎪 Host multiple events simultaneously
- 🕒 Manage event schedules and inventory
- 🔄 Modify and delete events

### ✅ **User Panel**
- 🔍 Search, sort, and filter events
- 🎟️ Book tickets and select seats
- 💰 Payment processing and refunds
- 🔄 Cancel and manage bookings
- 🔐 User authentication (login, register, forgot password, etc.)

---

## 🛠️ Tech Stack
- **Backend**: FastAPI (Python)
- **Database**: MySQL using SQLalchemy
- **Authentication**: OAuth

---

## 🏗️ Folder Structure
```
python-fastapi-boilerplate/
├─ apps/versions/apis    # Main application files
├─ config/               # Configuration files
├─ core/                 # Core utilities and services
├─ middleware/           # Custom middlewares
├─ log_service/          # Logging system
├─ assets/               # Static assets like images/templates
├─ .env                  # Environment variables
├─ pyproject.toml        # Dependencies and project metadata
└─ README.md             # Project documentation
```

---

## 🔧 Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/gojiyashailesh/Eventify.git
cd Eventify
```

## Setting Up a Virtual Environment in Different Ways

## 1️⃣ Using Python's Built-in `venv`

### 🐍 For Windows (Command Prompt)
```cmd
python -m venv venv
venv\Scripts\activate
```

### 🐧 For macOS/Linux 
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 2️⃣ Using `uv` (Fast Python Package Manager - Preffered To use)

### 🐍 For Windows (Command Prompt)
```cmd
uv venv uv
uv\Scripts\activate
```

### 🐧 For macOS/Linux 
```bash
uv venv uv
source uv/bin/activate
```

---

## 3️⃣ Using `conda` (Anaconda)

### 🐍 For Windows (Command Prompt)
```cmd
conda create --name myenv python=3.10 -y
conda activate myenv
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 5️⃣ Run the Application
```bash
uvicorn asgi:app --reload
```

### 6️⃣ Access the API Documentation
- Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API documentation.

---

## 🤝 Contribution Guidelines For Team

1. Fork the repository and clone it locally.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit your changes using conventional commit messages (`git commit -m ":sparkles: Add new feature"` 🎉).
4. Push to your branch and create a pull request.
5. Team For any Query or Workflow Go to [View Documentation](Docs.md)


---

## 🔗 Useful Links
- 📖 [FastAPI Documentation](https://fastapi.tiangolo.com/)
- 🐍 [Python Official Docs](https://docs.python.org/3/)

---
## 💡 Best Practices
- Follow **PEP 8** coding standards.
- Use **Gitmoji** for commit messages.
- Write **unit tests** before pushing new features.(optional as of now not including it)

🎯 Eventify ! 🚀
