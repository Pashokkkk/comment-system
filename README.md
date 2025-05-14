# 📝 Comment System (Django + Vue + JWT + WebSocket + Docker)

A full-featured comment system with nested replies, JWT authentication, CAPTCHA, file uploads, live updates via WebSocket, and modern Vue.js SPA.

---

## ✅ 1. Clone the repository

```bash
git clone https://github.com/Pashokkkk/comment-system.git
cd comment_system
```

## ✅ 2. Start the project

```bash
docker-compose up --build
```
створив суперкористувача, виконай:
docker exec -it django-app python manage.py createsuperuser

Виконай в контейнері Django такі дві команди:
docker exec -it django-app python manage.py makemigrations
docker exec -it django-app python manage.py migrate


Перейди в frontend/ і виконай:
npm install
npm run dev

This will:

- build Docker images (Django + Vue)
- start backend at http://localhost:8000
- serve frontend SPA at http://localhost:5173/static/
- create Redis container (for Celery/WebSocket)
- enable WebSocket via Daphne

---

## 🔗 Access:

| Service         | URL                                             |
|------------------|--------------------------------------------------|
| 🎨 Frontend SPA  | [http://localhost:5173/static/](http://localhost:5173/static/) |
| ⚙ Django Admin   | [http://localhost:8000/admin/](http://localhost:8000/admin/) |
| 🧠 API           | [http://localhost:8000/api/](http://localhost:8000/api/) |
| 🔐 WebSocket     | `ws://localhost:8000/ws/comments/`             |

---

## ✅ 4. Create a superuser (for admin)

```bash
docker exec -it django-app python manage.py createsuperuser
```

---

## 🔐 JWT Login

```http
POST http://localhost:8000/api/token/
Content-Type: application/json

{
  "username": "root",
  "password": "root"
}
```

Response:

```json
{
  "refresh": "...",
  "access": "..."
}
```

Add this to requests:

```
Authorization: Bearer <access_token>
```

---

## 🔧 Features implemented:

- 📬 Submit comments via form with CAPTCHA
- 🖼 Upload images and files (jpg/png/txt/md)
- ✅ Supports **allowed HTML tags**: `<i>`, `<strong>`, `<code>`, `<a>`
- ✅ Validates correct closing of HTML tags before saving
- 📎 Comment preview before submission
- 🧵 Nested comment replies (hierarchy)
- 🔃 Live updates via **WebSocket**
- 📥 Pagination and sorting (username, email, date)
- 🗃 Django Admin for comment moderation
- ✅ CAPTCHA verification (with key refresh)
- 🔐 JWT login from frontend form
- ✉️ Send email notifications (via Celery)
- 📦 Dockerized setup (runs via Daphne)
- 🧠 Caching (partially using DRF)
- 📡 WebSocket (Channels + Vue.js listener)
- 🗂 File validation: type, size

---

## 📁 Project structure

```
comment_system/
│
├── backend/
│   ├── comments/
│   ├── config/
│   ├── frontend_dist/
│   ├── static/
│   ├── staticfiles/
│   ├── venv/
│   └── manage.py
│
├── frontend/
│   ├── .vscode/
│   ├── dist/
│   ├── frontend/
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   ├── .env
│   ├── index.html
│   ├── jsconfig.json
│   ├── package.json
│   └── vite.config.js
│
├── media/
├── docker-compose.yml
├── Dockerfile
├── README.md
├── .gitignore
└── requirements.txt
```

---

## 🔎 WebSocket check

- Open DevTools > Network > WS
- Confirm connection to: `ws://localhost:8000/ws/comments/`
- Status should be `101 Switching Protocols`
- Create a comment → it should appear live without refreshing

---

## 🛠 Technologies Used

- Python 3.10
- Django + Django REST Framework
- Vue 3 (Vite)
- Channels (ASGI, WebSocket)
- JWT (SimpleJWT)
- Pillow, CAPTCHA
- Celery + Redis
- Docker + Daphne

---

## 📸 Demo

https://youtu.be/8YWVHTzGBq8
