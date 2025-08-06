بما أن مشروعك يستخدم **هيكلة Clean Architecture** (Controllers, Domain, Infrastructure, Repositories, Services, Use Cases)، يمكن تحسين الـ **README.md** ليعكس هذه الهيكلة بوضوح ويُظهر أنك تطبق معايير احترافية في تصميم الـ Backend.

إليك النسخة المعدلة من **README.md**:

---

# 📌 Flask Todo API with JWT & Clean Architecture

A **production-ready RESTful Todo API** built with **Flask**, implementing **JWT Authentication**, **PostgreSQL**, and **Clean Architecture principles** for high scalability and maintainability.

---

## ✨ Features

* 🔐 **JWT Authentication** (Access & Refresh Tokens)
* 🏗️ **Clean Architecture** with well-defined layers (Controllers, Domain, Use Cases, Infrastructure)
* ✅ **Todo CRUD operations** (Create, Read, Update, Delete)
* 🐘 **PostgreSQL database** support via SQLAlchemy
* ⚙️ **Environment configuration** with `.env` file
* 🧪 **Pytest testing** for better code reliability
* 📧 **Email notification service** for task updates
* 🌐 **CORS support** for integration with a Next.js frontend

---

## 📂 Project Structure

```
projects/
│
├── tests/
│   └── test_mail_service.py       # Unit tests for services
│
└── app/
    ├── controllers/               # HTTP request handlers (Flask Blueprints)
    ├── domain/                    # Core business entities and rules
    ├── infrastructure/            # Database config, external services
    ├── repositories/              # Data persistence logic (DB access)
    ├── services/                  # Application services (mail, auth, etc.)
    └── use_cases/                 # Application-specific business logic
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Ishaksmail/flask-todo-backend.git
cd flask-todo-backend
```

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Create `.env` file

```bash
cp .env.example .env
```

Update `.env` with your environment variables.

### 5️⃣ Run database migrations

```bash
flask db upgrade
```

### 6️⃣ Start the server

```bash
flask run
```

---

## 🚀 API Endpoints

| Method | Endpoint         | Description       | Auth Required |
| ------ | ---------------- | ----------------- | ------------- |
| POST   | `/auth/register` | Register new user | ❌             |
| POST   | `/auth/login`    | User login        | ❌             |
| GET    | `/todos`         | Get all todos     | ✅             |
| POST   | `/todos`         | Create a new todo | ✅             |
| PUT    | `/todos/<id>`    | Update a todo     | ✅             |
| DELETE | `/todos/<id>`    | Delete a todo     | ✅             |

---

## 🧪 Running Tests

```bash
pytest
```

---

## 🤝 Contributing

Pull requests are welcome. Please ensure code quality and testing before submitting.

---

## 📜 License

This project is licensed under the MIT License.
