# FastAPI User Management

A user management system built with **FastAPI** and **SQLModel**, featuring authentication, role-based access control, and user profile management.

## Features
- ✅ User Registration & Authentication (JWT-based)
- ✅ Password Hashing & Secure Storage
- ✅ Role-Based Access Control (Admin & Regular Users)
- ✅ User Profile Management (Update Name, Email, Password)
- ✅ Pagination, Sorting, and Filtering for Users
- ✅ Email Verification & Password Reset
- ✅ API Rate Limiting & Logging
- ✅ Docker Support for Deployment
- ✅ CI/CD with GitHub Actions & Unit Testing

## Installation

### 1. Clone the Repository
```sh
$ git clone https://github.com/AbdallahM19/fastapi_user_management.git
$ cd fastapi_user_management
```

### 2. Create a Virtual Environment
```sh
$ python -m venv venv
$ source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```sh
$ pip install -r requirements.txt
```

### 4. Initialize Database
```sh
$ python -c 'from app import create_db_and_tables; create_db_and_tables()'
```

### 5. Run the Application
```sh
$ uvicorn app:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Endpoints
| Method | Endpoint            | Description                |
|--------|--------------------|----------------------------|
| GET    | `/users/`          | List all users            |
| GET    | `/users/{id}`      | Get user by ID            |
| POST   | `/users/`          | Create a new user         |
| DELETE | `/users/{id}`      | Delete user by ID         |

## Docker Setup
```sh
$ docker build -t fastapi-user .
$ docker run -p 8000:8000 fastapi-user
```

## License
This project is licensed under the MIT License. See `LICENSE` for details.

## Contributing
Pull requests are welcome! Open an issue to discuss any changes first.

---
### Author
🚀 Created by **Abdallah Mohamed** | [GitHub](https://github.com/AbdallahM19)

