# Social Media API (Django REST Framework)

A professional, fully-featured Social Media Backend API built with Django and Django REST Framework (DRF). This project demonstrates advanced concepts like JWT authentication, custom permissions, and complex database relationships.

## 🚀 Features

- **User Authentication:** Secure signup and login using **SimpleJWT** (JSON Web Tokens).
- **Post Management:** Full CRUD (Create, Read, Update, Delete) for posts with image support.
- **Like System:** Intelligent Toggle-like functionality (Like/Unlike) for user posts.
- **Follow System:** Users can follow/unfollow each other to build a social network.
- **Personalized Feed:** A dedicated endpoint to fetch posts only from users you follow.
- **Custom Permissions:** Security logic ensuring only authors can edit or delete their own content.
- **Automated API Discovery:** Built using DRF Routers for clean and consistent URL patterns.

## 🛠️ Tech Stack

- **Framework:** Django 4.x
- **API:** Django REST Framework (DRF)
- **Authentication:** SimpleJWT
- **Database:** SQLite (Development) / PostgreSQL (Production ready)
- **Language:** Python 3.x

## 📋 API Endpoints

### Authentication
- `POST /api/login/` - Obtain JWT Access & Refresh tokens.
- `POST /api/token/refresh/` - Refresh the Access token.
- `POST /api/register/` - Register a new user account.

### Posts
- `GET /posts/` - List all posts.
- `POST /posts/` - Create a new post (Authenticated).
- `GET /posts/{id}/` - Retrieve post details.
- `PUT/PATCH /posts/{id}/` - Update a post (Author only).
- `DELETE /posts/{id}/` - Delete a post (Author only).
- `GET /posts/feed/` - Get posts from followed users only.

### Interactions
- `POST /posts/{id}/like/` - Toggle like on a post.
- `POST /follow/{user_id}/` - Follow/Unfollow a user.
## 🏁 Getting Started

### 1. Clone the repository
```bash
git clone [https://github.com/ammar-eid/Social-Media-API-Django.git](https://github.com/ammar-eid/Social-Media-API-Django.git)
cd Social-Media-API-Django
```

### 2. Create a virtual environment
```bash
python -m venv venv
# Activate on Windows:
venv\Scripts\activate
# Activate on Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. start the server 
```bash
python manage.py runserver
```
