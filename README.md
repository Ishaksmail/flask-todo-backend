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

## 📌 **1. Auth Endpoints (`/auth`)**

| Method | Endpoint    | Description                  | Auth Required | Body Params                     |
| ------ | ----------- | ---------------------------- | ------------- | ------------------------------- |
| POST   | `/register` | Register a new user          | ❌             | `username`, `email`, `password` |
| POST   | `/login`    | User login                   | ❌             | `username`, `password`          |
| POST   | `/refresh`  | Refresh access token         | ✅ (Refresh)   | *None*                          |
| POST   | `/logout`   | Logout and clear JWT cookies | ❌             | *None*                          |

---

## 📌 **2. Group Endpoints (`/api/group`)**

| Method | Endpoint       | Description                | Auth Required | Body Params                                 |
| ------ | -------------- | -------------------------- | ------------- | ------------------------------------------- |
| POST   | `/`            | Create a new group         | ✅             | `name` (required), `description` (optional) |
| GET    | `/`            | Get all groups of the user | ✅             | *None*                                      |
| GET    | `/completed`   | Get completed groups       | ✅             | *None*                                      |
| GET    | `/uncompleted` | Get uncompleted groups     | ✅             | *None*                                      |
| PUT    | `/<group_id>`  | Update a group             | ✅             | `name` (required), `description` (optional) |
| DELETE | `/<group_id>`  | Soft delete a group        | ✅             | *None*                                      |

---

## 📌 **3. Task Endpoints (`/api/task`)**

| Method | Endpoint                | Description               | Auth Required | Body Params                                                   |
| ------ | ----------------------- | ------------------------- | ------------- | ------------------------------------------------------------- |
| POST   | `/`                     | Create a new task         | ✅             | `text` (required), `group_id` (optional), `due_at` (optional) |
| GET    | `/`                     | Get all tasks of the user | ✅             | *None*                                                        |
| DELETE | `/<task_id>`            | Delete a task             | ✅             | *None*                                                        |
| PATCH  | `/complete/<task_id>`   | Mark task as completed    | ✅             | *None*                                                        |
| PATCH  | `/uncomplete/<task_id>` | Mark task as uncompleted  | ✅             | *None*                                                        |

---

## 📌 **4. User Endpoints (`/api/user`)**

| Method | Endpoint           | Description                            | Auth Required | Body Params             |
| ------ | ------------------ | -------------------------------------- | ------------- | ----------------------- |
| POST   | `/forgot-password` | Send password reset link to user email | ❌             | `email`                 |
| POST   | `/reset-password`  | Reset password using a token           | ❌             | `token`, `new_password` |
| POST   | `/reset-username`  | Change username                        | ✅             | `new_username`          |
| POST   | `/email`           | Add a verified email                   | ✅             | `email`                 |
| POST   | `/verify-email`    | Verify email using a token             | ❌             | `token`                 |
| GET    | `/isLogin`         | Check if the user is logged in         | ✅ (Optional)  | *None*                  |


---

## 🧪 Running Tests

```bash
pytest
```

---

## 🤝 Contributing

Pull requests are welcome. Please ensure code quality and testing before submitting.

