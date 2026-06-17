# User Management System with Authentication

## Features

- User Registration
- User Login
- User Profile
- Logout Functionality
- Email Validation
- Password Hashing
- Session Management
- SQLite Database Storage

## Technology Stack

### Frontend
- HTML
- Bootstrap 5

### Backend
- Flask (Python)

### Database
- SQLite

### Libraries
- Werkzeug
- Email Validator

## Setup Instructions

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python app.py
```

## Assumptions

- Each user must register using a unique email.
- Password must contain at least 8 characters.
- Password must contain one uppercase letter and one number.
- User authentication is managed using Flask sessions.