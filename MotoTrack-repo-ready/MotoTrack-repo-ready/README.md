# MotoTrack

MotoTrack is a capstone-ready full-stack web application for motorcycle owners who want to track maintenance history, monitor service intervals, and avoid missed maintenance.

## Features

- User registration and login
- JWT-based authentication
- Motorcycle profile management
- Maintenance log creation, viewing, updating, and deletion
- Mileage-based and date-based service interval tracking
- Dashboard for recent service history and overdue items
- SQLite database persistence
- Simple browser-based frontend for live demos

## Recommended Repository Structure

```text
MotoTrack/
├── client/
│   └── README.md
├── docs/
│   └── api-overview.md
├── server/
│   ├── app/
│   │   ├── routes/
│   │   ├── static/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── extensions.py
│   │   ├── models.py
│   │   └── utils.py
│   ├── requirements.txt
│   └── run.py
├── .env.example
├── .gitignore
└── README.md
```

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Flask
- **Database:** SQLite with SQLAlchemy ORM
- **Authentication:** Flask-JWT-Extended
- **Migrations:** Flask-Migrate

## Quick Start

### 1. Create a virtual environment

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies
```bash
cd server
pip install -r requirements.txt
```

### 3. Configure environment variables
Copy `.env.example` values into your environment or leave defaults for local development.

### 4. Start the server
```bash
python run.py
```

### 5. Open the app
Visit:
```text
http://127.0.0.1:5000
```

## Core User Flows

1. Register or log in
2. Add a motorcycle profile
3. Log maintenance events such as oil changes, tire replacement, or brake service
4. Review overdue items on the dashboard
5. View service history by motorcycle

## Capstone Notes

This version is built to satisfy a strong MVP for a semester project. It demonstrates:

- real data persistence
- multiple user workflows
- CRUD operations
- authentication and ownership enforcement
- business logic for service reminders

## Suggested Next Improvements

- Separate the client into a React frontend later if desired
- Add email or SMS reminder delivery
- Add automated tests
- Add Docker support
- Add production deployment config
