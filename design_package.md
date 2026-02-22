# MotoTrack — System Architecture Design Package

---

## 1. System Overview

MotoTrack is a full-stack web application designed to help motorcycle owners track maintenance history, monitor service intervals, and prevent missed maintenance. Users can create motorcycle profiles, log service events (oil changes, chain adjustments, tire replacements, brake inspections, etc.), and view dashboards that display maintenance history and upcoming recommended services based on mileage and/or time intervals.

The primary users are everyday motorcycle riders who want a lightweight, centralized, and easy-to-use maintenance tracking system.

### High-Level Workflows

- User registration and login  
- Motorcycle profile creation  
- Logging maintenance events  
- Viewing maintenance history and dashboard summaries  
- Receiving in-app (and optional email/SMS) reminders  

---

## 2. High-Level Architecture

### Component Responsibilities

#### Front-End / Client
- Handles UI rendering (forms, dashboards, service history)
- Sends authenticated API requests to server
- Displays API responses to user

#### Back-End / Server (REST API)
- Implements authentication (JWT)
- Validates requests
- Enforces ownership rules
- Executes maintenance interval logic
- Handles CRUD operations
- Sends reminder notifications

#### Database
- Stores users, motorcycles, maintenance logs, service rules, and reminders
- Enforces relational constraints

#### External Services (Optional Enhancements)
- Email/SMS provider (e.g., SendGrid, Twilio)
- Used for reminder notifications

---

### Data Flow

1. User interacts with UI  
2. UI sends HTTPS request to API  
3. API validates authentication  
4. API reads/writes database  
5. API returns JSON response  
6. UI updates display  
7. Scheduled reminder job checks database and triggers notifications  

---

## 3. Layering / Code Organization Plan

MotoTrack follows a layered architecture to reduce coupling and improve maintainability.

### Layers

- Presentation Layer (UI)  
- API/Controller Layer  
- Business Logic Layer (Services)  
- Data Access Layer (Models/ORM)  

### Suggested Repository Structure

```
/client
  /src
    /components
    /pages
    /services
    /styles

/server
  /src
    /controllers
    /routes
    /middleware
    /services
    /models
    /utils
    /tests

/db
  /migrations
  /seed

/docs
  design_package.md
```

### Why This Improves Maintainability

Separating UI, API routing, business logic, and database access ensures that changes in one layer do not directly impact others. Database schema changes affect only the model layer, not the UI. Business logic is centralized in service modules, making it easier to test independently and reducing duplication.

---

## 4. Database Schema

### Users

| Field | Type | Constraints |
|-------|------|------------|
| user_id | PK | Auto-generated |
| email | VARCHAR | NOT NULL, UNIQUE |
| password_hash | VARCHAR | NOT NULL |
| display_name | VARCHAR | NOT NULL |
| created_at | DATETIME | NOT NULL |

---

### Motorcycles

| Field | Type | Constraints |
|-------|------|------------|
| motorcycle_id | PK | Auto-generated |
| user_id | FK → users.user_id | NOT NULL |
| nickname | VARCHAR | NOT NULL |
| make | VARCHAR | NOT NULL |
| model | VARCHAR | NOT NULL |
| year | INT | NOT NULL |
| current_mileage | INT | NOT NULL (default 0) |
| created_at | DATETIME | NOT NULL |

**Relationship:** One User → Many Motorcycles

---

### Maintenance Logs

| Field | Type | Constraints |
|-------|------|------------|
| log_id | PK | Auto-generated |
| motorcycle_id | FK → motorcycles.motorcycle_id | NOT NULL |
| service_type | VARCHAR | NOT NULL |
| service_date | DATE | NOT NULL |
| mileage_at_service | INT | NOT NULL |
| notes | TEXT | Optional |
| cost | DECIMAL | Optional |
| created_at | DATETIME | NOT NULL |

**Relationship:** One Motorcycle → Many Maintenance Logs

---

### Service Rules

| Field | Type | Constraints |
|-------|------|------------|
| rule_id | PK | Auto-generated |
| user_id | FK → users.user_id | Nullable (global default if NULL) |
| service_type | VARCHAR | NOT NULL |
| interval_miles | INT | Optional |
| interval_days | INT | Optional |

Constraint: At least one of interval_miles or interval_days must be provided.

---

### Reminders

| Field | Type | Constraints |
|-------|------|------------|
| reminder_id | PK | Auto-generated |
| motorcycle_id | FK → motorcycles.motorcycle_id | NOT NULL |
| service_type | VARCHAR | NOT NULL |
| due_mileage | INT | Optional |
| due_date | DATE | Optional |
| status | VARCHAR | NOT NULL (PENDING, SENT, COMPLETED, DISMISSED) |
| last_sent_at | DATETIME | Optional |

---

## 5. API / Interface Plan

All endpoints return JSON. Authentication via Bearer JWT.

### POST /api/auth/register
Input: email, password, displayName  
Success: 201 Created  
Errors: 409 Conflict, 400 Bad Request  

### POST /api/auth/login
Input: email, password  
Success: JWT token + user object  
Error: 401 Unauthorized  

### GET /api/motorcycles
Input: Authorization header  
Output: List of motorcycles  
Error: 401 Unauthorized  

### POST /api/motorcycles
Input: nickname, make, model, year, currentMileage  
Output: 201 Created  
Error: 400 Bad Request  

### POST /api/motorcycles/:motorcycleId/logs
Input: serviceType, serviceDate, mileageAtService, notes (optional), cost (optional)  
Output: 201 Created  
Errors: 404 Not Found, 400 Bad Request  

### GET /api/motorcycles/:motorcycleId/dashboard
Output: currentMileage, recentLogs, upcoming reminders  
Errors: 404 Not Found, 401 Unauthorized  

---

## 6. Technical Risk List

### Risk 1: Complex Interval Calculations  
Why: Service intervals may depend on mileage and/or time.  
Mitigation: Build a dedicated interval service module with unit tests.

### Risk 2: Authentication & Authorization Errors  
Why: Incorrect ownership checks could expose data.  
Mitigation: Use JWT middleware and enforce ownership validation.

### Risk 3: Deployment Configuration Issues  
Why: Environment variables and database setup may fail in production.  
Mitigation: Use staging environment and maintain a `.env.example` file.

### Risk 4: Data Integrity & Validation  
Why: Invalid mileage entries could break reminder logic.  
Mitigation: Enforce server-side validation and database constraints.

---

## 7. Design Review Checklist

**Does each component have a clear responsibility?**  
Yes. UI handles presentation, API handles routing/authentication, services handle logic, and the database handles persistence.

**Where are the biggest dependencies?**  
The back-end depends heavily on the database schema and authentication middleware.

**What part of the system is most complex?**  
Reminder calculation logic combining mileage and time intervals.

**What can you simplify right now?**  
Limit initial release to in-app reminders only and core service types (oil, chain, tires, brakes).